"""Offline ASGI parity and actual pinned resilient-host observation fixtures."""
from __future__ import annotations

import asyncio
from contextlib import ExitStack, redirect_stdout
import io
import json
import logging
import os
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID

import httpx2
from agent_framework_foundry_hosting import ResponsesHostServer
from azure.ai.agentserver.core import AgentConfig, get_request_context
from azure.ai.agentserver.core.streaming import streams, EventStreamNotFoundError
from azure.ai.agentserver.core.tasks import resilient_tasks_enabled, set_resilient_tasks_enabled
from azure.ai.agentserver.responses import ResponsesServerOptions
from azure.ai.agentserver.responses.store._file import FileResponseStore

from demo import diagnostics as diag
from demo.host import (
    IngressDiagnostics, WorkflowPreparationDiagnostics, context_checkpoint,
    main, prepare_diagnostic_options,
)
from demo.workflow import create_workflow, parse_turn
from demo.artifacts import ArtifactError
from demo.contracts import AGENTS, PROJECT


class HostProfileProjectionTests(unittest.TestCase):
    def event(self):
        return diag.event_fields(diag.Event(
            diag.Role.ARCHITECT, diag.Stage.INGRESS, diag.Kind.CONTEXT,
            binding=diag.Binding(UUID("12345678-1234-4234-8234-123456789abc")),
            platform=diag.observe_value(None), delegation=diag.observe_value(""),
        ))

    def test_strict_projection_raw_and_wrapped(self):
        from live_acceptance import project_profile_event
        event = self.event()
        for text in (json.dumps(event), json.dumps({"message": json.dumps(event), "ignored": "private"})):
            self.assertEqual(project_profile_event(text, "architect"), event)
        self.assertIsNone(project_profile_event(json.dumps(event), "coordinator"))

    def test_malformed_private_or_extra_data_never_escapes(self):
        from live_acceptance import project_profile_event
        event = self.event()
        variants = [
            event | {"secret": "private-sentinel"},
            event | {"schema_version": True}, event | {"route": "https://private"},
            event | {"binding": {"observation": "private-sentinel"}},
            event | {"platform": {"coverage": "observed", "presence": "absent", "value": "private"}},
            event | {"status": True}, event | {"duration_ms": float("nan")},
            event | {"scope_user": {"coverage": "unavailable", "presence": "absent"}},
        ]
        for value in variants:
            with self.subTest(value=value):
                self.assertIsNone(project_profile_event(json.dumps(value), "architect"))
        for text in ("private-sentinel", "[]", "{}", "x" * 8193):
            self.assertIsNone(project_profile_event(text, "architect"))


class HostProfileStreamTests(unittest.IsolatedAsyncioTestCase):
    async def collect(self, chunks):
        from live_acceptance import observe_host_failure

        async def stream():
            for chunk in chunks:
                yield chunk
        response = SimpleNamespace(
            status_code=200, headers={"content-type": "text/event-stream"}, aiter_bytes=stream,
        )
        manager = MagicMock()
        manager.__aenter__ = AsyncMock(return_value=response)
        manager.__aexit__ = AsyncMock(return_value=False)
        http = SimpleNamespace(stream=MagicMock(return_value=manager))
        credential = SimpleNamespace(get_token=AsyncMock(return_value=SimpleNamespace(token="private-token")))
        result = await observe_host_failure(
            http, credential, "bound-session", "19", role="architect",
            response_id="known-response", structured=True,
        )
        self.assertEqual(http.stream.call_args.args[0], "GET")
        self.assertIn("/versions/19/sessions/bound-session:logstream", http.stream.call_args.args[1])
        manager.__aexit__.assert_awaited_once()
        self.assertNotIn("private-token", json.dumps(result))
        return result

    async def test_fragmented_occurrences_not_deduplicated_or_response_claimed(self):
        event = HostProfileProjectionTests().event()
        line = ("data: " + json.dumps({"message": json.dumps(event)}) + "\n\n").encode()
        result = await self.collect([line[:20], line[20:], line, b"data: private-sentinel\n\n"])
        self.assertEqual(result["structured_profiles"], [event, event])
        self.assertIn("not independently joined", result["structured_scope"])
        self.assertNotIn("private-sentinel", json.dumps(result))

    async def test_record_and_byte_limits_close_stream(self):
        event = HostProfileProjectionTests().event()
        line = ("data: " + json.dumps(event) + "\n\n").encode()
        result = await self.collect([line] * 513)
        self.assertEqual(result["limit"], "records")
        self.assertEqual(len(result["structured_profiles"]), 512)
        result = await self.collect([b"x" * 2097153])
        self.assertEqual(result["limit"], "bytes")
        self.assertEqual(result["structured_profiles"], [])


def scope(headers=(), **kwargs):
    return {
        "type": "http", "method": "POST", "path": "/responses",
        "query_string": b"private=QUERY_SENTINEL", "headers": list(headers), **kwargs,
    }


class MiddlewareTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.stack = ExitStack()
        self.events = []
        self.stack.enter_context(patch("demo.diagnostics.emit", side_effect=self.events.append))
        self.stack.enter_context(patch.dict(os.environ, {"DEMO_ROLE": "architect"}))
        self.addCleanup(self.stack.close)

    async def test_raw_presence_casing_duplicates_redaction_and_scope_unchanged(self):
        cases = (
            ([], diag.Presence.ABSENT),
            ([(b"x-agent-user-id", b"")], diag.Presence.EMPTY),
            ([(b"X-AGENT-USER-ID", b"IDENTITY_SENTINEL")], diag.Presence.NONEMPTY),
            ([(b"x-agent-user-id", b"first"), (b"X-Agent-User-Id", b"second")],
             diag.Presence.MALFORMED_DUPLICATE),
            ([(b"x-agent-user-id", b"\xff")], diag.Presence.MALFORMED_DUPLICATE),
        )
        for headers, expected in cases:
            with self.subTest(expected=expected):
                request = scope(headers + [
                    (b"x-ms-user-identity", b"DELEGATION_SENTINEL"),
                    (b"authorization", b"Bearer TOKEN_SENTINEL"),
                ])
                before = repr(request)
                async def app(raw, receive, send):
                    self.assertIs(raw, request)
                    await send({"type": "http.response.start", "status": 200, "headers": []})
                    await send({"type": "http.response.body", "body": b"BODY_SENTINEL"})
                async def unused_receive():
                    self.fail("diagnostics must not read ahead")
                async def send(message):
                    pass
                start = len(self.events)
                await IngressDiagnostics(app, role="architect")(request, unused_receive, send)
                emitted = self.events[start:]
                self.assertEqual(emitted[0].platform.presence, expected)
                self.assertEqual(emitted[0].delegation.presence, diag.Presence.NONEMPTY)
                self.assertEqual(repr(request), before)
                self.assertEqual([e.kind for e in emitted], [
                    diag.Kind.SEND, diag.Kind.RESPONSE_HEADERS, diag.Kind.ASGI_FINAL_BODY,
                ])
                payload = json.dumps([diag.event_fields(e) for e in emitted])
                for secret in ("IDENTITY_SENTINEL", "DELEGATION_SENTINEL", "TOKEN_SENTINEL",
                               "BODY_SENTINEL", "QUERY_SENTINEL"):
                    self.assertNotIn(secret, payload)
                self.assertNotIn(diag.Kind.EXECUTION_COMPLETE, [e.kind for e in emitted])
        self.assertIsNone(diag.current_binding())

    async def test_receive_send_stream_disconnect_identity_and_no_buffering(self):
        incoming = [
            {"type": "http.request", "body": b"first", "more_body": True},
            {"type": "http.request", "body": b"second", "more_body": False},
            {"type": "http.disconnect"},
        ]
        outgoing = [
            {"type": "http.response.start", "status": 201, "headers": [(b"x", b"v")]},
            {"type": "http.response.body", "body": b"chunk-one", "more_body": True},
            {"type": "http.response.body", "body": b"chunk-two"},
        ]
        received, sent, bindings = [], [], []
        async def receive():
            return incoming[len(received)]
        async def send(message):
            sent.append(message)
        async def app(raw, recv, snd):
            for index, message in enumerate(outgoing):
                value = await recv()
                received.append(value)
                self.assertIs(value, incoming[index])
                await snd(message)
                self.assertIs(sent[-1], message)  # forwarded before next chunk
                bindings.append(diag.current_binding())
                await asyncio.sleep(0)
        await IngressDiagnostics(app, role="reviewer")(scope(), receive, send)
        self.assertEqual(received, incoming)
        self.assertEqual(sent, outgoing)
        self.assertEqual(len(set(bindings)), 1)
        self.assertIsNotNone(bindings[0])
        self.assertIn(diag.Kind.DISCONNECT, [e.kind for e in self.events])
        self.assertIsNone(diag.current_binding())

    async def test_exception_cancellation_and_failing_logger_preserve_original(self):
        for failure in (RuntimeError("PRIVATE_EXCEPTION_SENTINEL"), asyncio.CancelledError()):
            for failing_sink in (False, True):
                with self.subTest(failure=type(failure), failing_sink=failing_sink):
                    async def app(raw, receive, send):
                        raise failure
                    async def unused(*args):
                        self.fail("must not call receive/send")
                    with patch("demo.diagnostics.emit", side_effect=(
                        RuntimeError("PRIVATE_LOGGER_SENTINEL") if failing_sink else self.events.append
                    )):
                        with self.assertRaises(type(failure)) as caught:
                            await IngressDiagnostics(app, role="architect")(scope(), unused, unused)
                    self.assertIs(caught.exception, failure)
                    self.assertIsNone(diag.current_binding())

    async def test_cancel_during_receive_or_send_is_not_swallowed(self):
        for boundary in ("receive", "send"):
            async def receive():
                if boundary == "receive":
                    raise asyncio.CancelledError()
                return {"type": "http.request", "body": b""}
            async def send(message):
                raise asyncio.CancelledError()
            async def app(raw, recv, snd):
                await recv()
                await snd({"type": "http.response.body", "body": b"x"})
            with self.assertRaises(asyncio.CancelledError):
                await IngressDiagnostics(app, role="architect")(scope(), receive, send)
            self.assertIsNone(diag.current_binding())
        self.assertEqual(sum(e.kind is diag.Kind.CANCELLED for e in self.events), 2)
        self.assertNotIn(diag.Kind.ASGI_FINAL_BODY, [e.kind for e in self.events])

    async def test_concurrent_bindings_and_background_survive_request_exit(self):
        release = asyncio.Event()
        tasks, observed = [], []
        async def app(raw, receive, send):
            binding = diag.current_binding()
            async def background():
                await release.wait()
                observed.append((binding, diag.current_binding()))
            tasks.append(asyncio.create_task(background()))
            await asyncio.sleep(0)
        async def unused(*args):
            self.fail("no extra IO")
        await asyncio.gather(*(
            IngressDiagnostics(app, role="coordinator")(scope(), unused, unused) for _ in range(2)
        ))
        self.assertIsNone(diag.current_binding())
        release.set()
        await asyncio.gather(*tasks)
        self.assertEqual(len({before for before, after in observed}), 2)
        self.assertTrue(all(before is after for before, after in observed))

    async def test_non_http_scope_is_passed_through_without_observation(self):
        async def receive():
            return {"type": "lifespan.startup"}
        async def send(message):
            pass
        request = {"type": "lifespan"}
        async def app(raw, recv, snd):
            self.assertIs(raw, request)
            self.assertIs(recv, receive)
            self.assertIs(snd, send)
        await IngressDiagnostics(app, role="architect")(request, receive, send)
        self.assertEqual(self.events, [])

    async def test_context_presence_equality_unavailable_and_failure_isolation(self):
        for left, right, match in (
            (None, None, diag.Match.NOT_COMPARABLE),
            ("", "", diag.Match.NOT_COMPARABLE),
            ("user-one", "user-one", diag.Match.TRUE),
            ("user-one", "user-two", diag.Match.FALSE),
            (b"user-one", "user-one", diag.Match.NOT_COMPARABLE),
        ):
            request = SimpleNamespace(scope=SimpleNamespace(user_id=left))
            with patch("demo.host.get_request_context", return_value=SimpleNamespace(user_id=right, call_id=None)):
                context_checkpoint(diag.Stage.PREPARATION, request)
                self.assertEqual(self.events[-1].scope_request_match, match)
                self.assertEqual(self.events[-1].scope_user, diag.observe_value(left))
                context_checkpoint(diag.Stage.PREPARATION)
                self.assertEqual(self.events[-1].scope_user.coverage, diag.Coverage.UNAVAILABLE)
        with patch("demo.host.get_request_context", side_effect=RuntimeError("PRIVATE")):
            context_checkpoint(diag.Stage.PREPARATION)
        options = {"temperature": 0.2}
        request = SimpleNamespace(request={"background": True}, scope=SimpleNamespace(user_id=None))
        with patch("demo.diagnostics.emit", side_effect=RuntimeError("PRIVATE")):
            self.assertIs(prepare_diagnostic_options(request, options), options)

    async def test_application_preparation_and_parser_still_reject_with_logger_failure(self):
        request = SimpleNamespace(
            scope=SimpleNamespace(is_hosted=False, user_id=None, call_id=None, session_id="s"),
            request={"store": False, "background": False},
        )
        config = SimpleNamespace(
            session_id="s", project_endpoint=PROJECT,
            agent_name=AGENTS["architect"], agent_version="1",
        )
        with patch("demo.diagnostics.emit", side_effect=RuntimeError("PRIVATE")), patch(
            "demo.workflow.AgentConfig.from_env", return_value=config,
        ):
            with self.assertRaises(ArtifactError) as caught:
                create_workflow(request)
            self.assertEqual(caught.exception.code, "NATIVE_HOST_PLATFORM")
            with self.assertRaisesRegex(ArtifactError, "STORED_RESILIENT_BACKGROUND_REQUIRED"):
                await parse_turn(request)

    async def test_main_registers_public_middleware_and_options_before_run(self):
        logger = logging.getLogger("agent_framework_foundry_hosting._workflow_responses")
        original_filters = logger.filters[:]
        self.addCleanup(setattr, logger, "filters", original_filters)
        for runtime in ("native", "legacy"):
            with patch.dict(os.environ, {
                "DEMO_RUNTIME": runtime, "AGENTSERVER_TASKS_BACKEND": "hosted",
            }), patch("demo.host.ResponsesHostServer") as server:
                main()
                instance = server.return_value
                instance.add_middleware.assert_called_once_with(IngressDiagnostics, role="architect")
                instance.run.assert_called_once_with()
                self.assertEqual([call[0] for call in instance.mock_calls], ["add_middleware", "run"])
                if runtime == "native":
                    self.assertIs(server.call_args.kwargs["prepare_options"], prepare_diagnostic_options)


class PinnedHostTests(unittest.IsolatedAsyncioTestCase):
    """No private SDK methods patched: real ASGI endpoint and durable dispatcher.

    Local file state and a synthetic executor replace cloud effects only. These
    tests prove process-local background dispatch, not crash recovery or cloud
    trust. The early-hosted rejection case never reaches a cloud store.
    """

    async def asyncSetUp(self):
        self.stack = ExitStack()
        self.owned_response_ids = []
        self.stack.callback(set_resilient_tasks_enabled, resilient_tasks_enabled())
        self.root = self.stack.enter_context(tempfile.TemporaryDirectory())
        self.stack.enter_context(patch.dict(os.environ, {
            "DEMO_ROLE": "architect", "FOUNDRY_HOSTING_ENVIRONMENT": "",
            "FOUNDRY_PROJECT_ENDPOINT": "https://example.services.ai.azure.com/api/projects/example-project",
            "FOUNDRY_AGENT_NAME": "synthetic-agent", "FOUNDRY_AGENT_VERSION": "1",
            "FOUNDRY_AGENT_SESSION_ID": "synthetic-parent",
            "AGENTSERVER_TASKS_BACKEND": "local", "AGENTSERVER_STATE_ROOT": self.root,
            "OTEL_SDK_DISABLED": "true",
        }))
        self.events, self.fields = [], []
        def capture(event):
            self.events.append(event)
            self.fields.append(diag.event_fields(event))
        self.stack.enter_context(patch("demo.diagnostics.emit", side_effect=capture))
        self.addCleanup(self.stack.close)

    async def asyncTearDown(self):
        for response_id in self.owned_response_ids:
            try:
                await streams.delete(response_id)
            except EventStreamNotFoundError:
                pass
        streams.use_in_memory_live()

    async def terminal_snapshot(self, client, response_id, headers):
        async def retrieve():
            while True:
                found = await client.get("/responses/" + response_id, headers=headers)
                self.assertEqual(found.status_code, 200)
                if found.json()["status"] not in ("queued", "in_progress"):
                    return found
                await asyncio.sleep(0.01)
        return await asyncio.wait_for(retrieve(), 10)

    def server(self, factory, parser=parse_turn):
        server = ResponsesHostServer(
            workflow=factory, parse_response=parser,
            prepare_options=prepare_diagnostic_options,
            options=ResponsesServerOptions(resilient_background=True),
            response_store=FileResponseStore(), configure_observability=None,
        )
        server.add_middleware(IngressDiagnostics, role="architect")
        return server

    async def test_real_resilient_nonstream_dispatch_retains_context_after_http_exit_and_isolates(self):
        release = asyncio.Event()
        entered = [asyncio.Event(), asyncio.Event()]
        finished = [asyncio.Event(), asyncio.Event()]
        samples = []
        def factory(request):
            self.owned_response_ids.append(request.response_id)
            index = int(request.scope.user_id[-1])
            async def specialize(text):
                entered[index].set()
                await release.wait()
                current = get_request_context()
                samples.append((request.scope.user_id, current.user_id, current.call_id))
                context_checkpoint(diag.Stage.EXECUTION, request)
                finished[index].set()
                return "synthetic result"
            # Only the application's cloud business runtime is synthetic. Use
            # its real factory, parser and specialist executor with the pinned
            # SDK's unmodified endpoint/durable dispatch/context reconstruction.
            runtime = SimpleNamespace(role="architect", request=request, specialize=specialize)
            with patch("demo.workflow.WorkflowRuntime", return_value=runtime):
                return create_workflow(request)

        server = self.server(factory)
        async with server.router.lifespan_context(server):
            async with httpx2.AsyncClient(
                transport=httpx2.ASGITransport(app=server), base_url="http://synthetic",
            ) as client:
                responses = await asyncio.gather(*(
                    client.post("/responses", json={
                        "input": "synthetic turn", "background": True, "store": True,
                    }, headers={"x-agent-user-id": f"synthetic-user-{index}",
                                "x-agent-foundry-call-id": f"synthetic-call-{index}"})
                    for index in range(2)
                ))
                self.assertTrue(all(r.status_code == 200 for r in responses))
                self.assertTrue(all(r.json()["status"] in ("queued", "in_progress") for r in responses))
                await asyncio.wait_for(asyncio.gather(*(e.wait() for e in entered)), 10)
                self.assertEqual(samples, [])  # both HTTP requests exited before observation
                self.assertEqual(sum(e.kind is diag.Kind.ASGI_FINAL_BODY for e in self.events), 2)
                self.assertIsNone(get_request_context().user_id)
                self.assertIsNone(diag.current_binding())
                release.set()
                await asyncio.wait_for(asyncio.gather(*(e.wait() for e in finished)), 10)
                self.assertEqual(set(samples), {
                    ("synthetic-user-0", "synthetic-user-0", "synthetic-call-0"),
                    ("synthetic-user-1", "synthetic-user-1", "synthetic-call-1"),
                })
                execution = [e for e in self.events if e.stage is diag.Stage.EXECUTION]
                self.assertEqual(len(execution), 4)  # executor entry plus after HTTP exit
                self.assertTrue(all(e.scope_request_match is diag.Match.TRUE for e in execution))
                ingress_aliases = {
                    e["binding"]["observation"] for e in self.fields
                    if e["stage"] == "ingress" and e["kind"] == "send"
                }
                execution_aliases = {
                    e["binding"]["observation"] for e in self.fields
                    if e["stage"] == "execution"
                }
                self.assertEqual(len(ingress_aliases), 2)
                self.assertEqual(execution_aliases, ingress_aliases)
                # Retrieval is known-response-only, never another POST/effect.
                for index, response in enumerate(responses):
                    found = await self.terminal_snapshot(client, response.json()["id"], {
                        "x-agent-user-id": f"synthetic-user-{index}",
                        "x-agent-foundry-call-id": f"synthetic-call-{index}",
                    })
                    self.assertEqual(found.json()["status"], "completed")
                payload = json.dumps(self.fields)
                self.assertNotIn("synthetic-user-", payload)
                self.assertNotIn("synthetic-call-", payload)
                self.assertNotIn("synthetic turn", payload)
                self.assertNotIn("synthetic result", payload)

    async def test_actual_pinned_host_missing_empty_principal_rejects_before_public_hooks(self):
        for user in (None, ""):
            with self.subTest(user=user), patch.dict(os.environ, {"FOUNDRY_HOSTING_ENVIRONMENT": "synthetic"}):
                called = []
                def factory(request):
                    called.append(True)
                    raise AssertionError("factory must not run")
                server = self.server(factory)
                logger = logging.getLogger("agent_framework_foundry_hosting._workflow_responses")
                diagnostic = WorkflowPreparationDiagnostics(AgentConfig.from_env())
                logger.addFilter(diagnostic)
                try:
                    async with server.router.lifespan_context(server):
                        async with httpx2.AsyncClient(
                            transport=httpx2.ASGITransport(app=server), base_url="http://synthetic",
                        ) as client:
                            headers = {"x-agent-foundry-call-id": "synthetic-call"}
                            if user is not None:
                                headers["x-agent-user-id"] = user
                            before = len(self.events)
                            response = await client.post("/responses", json={
                                "input": "synthetic", "store": False,
                            }, headers=headers)
                            self.assertEqual(response.status_code, 200)  # SDK envelope, NOT success
                            self.assertEqual(response.json()["status"], "failed")
                            emitted = self.events[before:]
                            raw = next(e for e in emitted if e.kind is diag.Kind.SEND)
                            self.assertEqual(raw.platform.presence, (
                                diag.Presence.ABSENT if user is None else diag.Presence.EMPTY
                            ))
                            rejected = next(e for e in emitted if e.kind is diag.Kind.EXECUTION_REJECTED)
                            self.assertEqual(rejected.scope_user.coverage, diag.Coverage.UNAVAILABLE)
                            self.assertEqual(rejected.request_user.presence, diag.Presence.ABSENT)
                            self.assertFalse(called)
                            self.assertNotIn(diag.Stage.REQUEST, [e.stage for e in emitted])
                finally:
                    logger.removeFilter(diagnostic)

    async def test_actual_resilient_stream_disconnect_keeps_background_context_and_execution(self):
        release, entered, finished = asyncio.Event(), asyncio.Event(), asyncio.Event()
        disconnected = asyncio.Event()
        samples, wire, response_ids = [], [], []

        def factory(request):
            response_ids.append(request.response_id)
            self.owned_response_ids.append(request.response_id)
            async def specialize(text):
                entered.set()
                await release.wait()
                current = get_request_context()
                samples.append((request.scope.user_id, current.user_id, current.call_id))
                context_checkpoint(diag.Stage.EXECUTION, request)
                finished.set()
                return "synthetic result"
            runtime = SimpleNamespace(role="architect", request=request, specialize=specialize)
            with patch("demo.workflow.WorkflowRuntime", return_value=runtime):
                return create_workflow(request)

        server = self.server(factory)
        sent_body = False
        raw_body = json.dumps({
            "input": "synthetic turn", "background": True, "store": True, "stream": True,
        }).encode()
        request = scope([
            (b"content-type", b"application/json"),
            (b"x-agent-user-id", b"synthetic-stream-user"),
            (b"x-agent-foundry-call-id", b"synthetic-stream-call"),
        ], asgi={"version": "3.0", "spec_version": "2.3"},
            http_version="1.1", scheme="http", server=("synthetic", 80),
            client=("synthetic", 1), root_path="")

        async def receive():
            nonlocal sent_body
            if not sent_body:
                sent_body = True
                return {"type": "http.request", "body": raw_body, "more_body": False}
            await disconnected.wait()
            return {"type": "http.disconnect"}

        async def send(message):
            wire.append(message)
            if b"response.in_progress" in message.get("body", b""):
                disconnected.set()

        async with server.router.lifespan_context(server):
            await asyncio.wait_for(server(request, receive, send), 10)
            await asyncio.wait_for(entered.wait(), 10)
            self.assertTrue(disconnected.is_set())
            self.assertEqual(samples, [])  # streaming request has exited
            self.assertTrue(any(e.kind is diag.Kind.DISCONNECT for e in self.events))
            self.assertIsNone(get_request_context().user_id)
            self.assertIsNone(diag.current_binding())
            release.set()
            await asyncio.wait_for(finished.wait(), 10)
            self.assertEqual(samples, [
                ("synthetic-stream-user", "synthetic-stream-user", "synthetic-stream-call"),
            ])
            self.assertTrue(any(
                e.stage is diag.Stage.EXECUTION and e.scope_request_match is diag.Match.TRUE
                for e in self.events
            ))
            self.assertTrue(any(m["type"] == "http.response.start" for m in wire))
            # Wait on public known-response retrieval before lifespan shutdown.
            async with httpx2.AsyncClient(
                transport=httpx2.ASGITransport(app=server), base_url="http://synthetic",
            ) as client:
                found = await self.terminal_snapshot(client, response_ids[0], {
                    "x-agent-user-id": "synthetic-stream-user",
                    "x-agent-foundry-call-id": "synthetic-stream-call",
                })
                self.assertEqual(found.json()["status"], "completed")

    async def test_actual_background_application_rejection_survives_failed_diagnostic_sink(self):
        completed = asyncio.Event()

        def factory(request):
            self.owned_response_ids.append(request.response_id)
            try:
                # Local SDK scope is valid; real application trusted-platform
                # checks still reject it. Logging may not authorize it.
                return create_workflow(request)
            finally:
                completed.set()

        server = self.server(factory)
        stdout = io.StringIO()
        async with server.router.lifespan_context(server):
            async with httpx2.AsyncClient(
                transport=httpx2.ASGITransport(app=server), base_url="http://synthetic",
            ) as client:
                with patch("demo.diagnostics.emit", side_effect=RuntimeError("LOGGER_SECRET")), redirect_stdout(stdout):
                    headers = {"x-agent-user-id": "synthetic-user", "x-agent-foundry-call-id": "synthetic-call"}
                    response = await asyncio.wait_for(client.post("/responses", json={
                        "input": "synthetic", "background": True, "store": True,
                    }, headers=headers), 10)
                    self.assertEqual(response.status_code, 200)
                    await asyncio.wait_for(completed.wait(), 10)
                    found = await self.terminal_snapshot(client, response.json()["id"], headers)
                    self.assertEqual(found.json()["status"], "failed")
        self.assertEqual(stdout.getvalue(), "")

    async def test_actual_resilient_cancellation_propagates_and_resets_request_context(self):
        entered, cancelled = asyncio.Event(), asyncio.Event()
        samples = []

        def factory(request):
            self.owned_response_ids.append(request.response_id)
            async def specialize(text):
                entered.set()
                try:
                    await asyncio.Event().wait()
                except asyncio.CancelledError:
                    current = get_request_context()
                    samples.append((request.scope.user_id, current.user_id))
                    context_checkpoint(diag.Stage.EXECUTION, request)
                    cancelled.set()
                    raise
            runtime = SimpleNamespace(role="architect", request=request, specialize=specialize)
            with patch("demo.workflow.WorkflowRuntime", return_value=runtime):
                return create_workflow(request)

        server = self.server(factory)
        async with server.router.lifespan_context(server):
            async with httpx2.AsyncClient(
                transport=httpx2.ASGITransport(app=server), base_url="http://synthetic",
            ) as client:
                headers = {"x-agent-user-id": "synthetic-user", "x-agent-foundry-call-id": "synthetic-call"}
                response = await asyncio.wait_for(client.post("/responses", json={
                    "input": "synthetic", "background": True, "store": True,
                }, headers=headers), 10)
                await asyncio.wait_for(entered.wait(), 10)
                result = await asyncio.wait_for(client.post(
                    "/responses/" + response.json()["id"] + "/cancel", headers=headers,
                ), 10)
                self.assertEqual(result.status_code, 200)
                await asyncio.wait_for(cancelled.wait(), 10)
                found = await self.terminal_snapshot(client, response.json()["id"], headers)
                self.assertEqual(found.json()["status"], "cancelled")
                self.assertEqual(samples, [("synthetic-user", "synthetic-user")])
                self.assertIsNone(get_request_context().user_id)
                self.assertIsNone(diag.current_binding())


if __name__ == "__main__":
    unittest.main()
