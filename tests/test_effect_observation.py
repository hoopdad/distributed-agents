"""Offline public pinned SDK/transport fixtures; never live effect evidence."""
from __future__ import annotations

import asyncio
import io
import json
import os
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import FrozenInstanceError, asdict
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock, patch

os.environ.setdefault("FOUNDRY_PROJECT_ENDPOINT", "https://example.services.ai.azure.com/api/projects/example-project")
os.environ.setdefault("SPECIALIST_MODEL_DEPLOYMENT", "synthetic-worker")
os.environ.setdefault("DECISION_MODEL_DEPLOYMENT", "synthetic-decision")

import httpx2
from agent_framework import AgentSession
from agent_framework.exceptions import ChatClientException
from agent_framework_foundry import FOUNDRY_HOSTED_AGENT_SESSION_ID_KEY
from azure.core.credentials import AccessToken
from azure.core.exceptions import ServiceRequestError
from azure.core.pipeline.transport import AioHttpTransport, AsyncHttpTransport, AsyncHttpResponse

from demo import effect_observation as e
from demo.contracts import AGENTS, PROJECT, Child, DemoError
from demo.foundry import OriginTransport, ProjectClient, RemoteAgents
from live_acceptance import stop_hosting_for_acceptance


class JSONResponse(AsyncHttpResponse):
    def __init__(self, request, payload, status=201):
        super().__init__(request, None)
        self.status_code = status
        self.reason = "Synthetic"
        self.headers = {"content-type": "application/json"}
        self.content_type = "application/json"
        self.payload = json.dumps(payload).encode()

    def body(self):
        return self.payload

    def json(self):
        return json.loads(self.payload)


class RawBytes(httpx2.AsyncByteStream):
    """Like a real final HTTP transport, return unread bytes to the SDK."""
    def __init__(self, value):
        self.value = value

    async def __aiter__(self):
        yield self.value


class ProjectWire(AsyncHttpTransport):
    """Real Azure Core pipeline final boundary with no sockets/real credential."""
    def __init__(self, failure=None):
        self.failure = failure
        self.requests = []
        self.options = []
        self.lifecycle = []
        self.connection_config = AioHttpTransport(connection_timeout=10, read_timeout=120).connection_config

    async def open(self):
        self.lifecycle.append("open")

    async def close(self):
        self.lifecycle.append("close")

    async def __aenter__(self):
        await self.open()
        return self

    async def __aexit__(self, *args):
        self.lifecycle.append("exit")
        await self.close()

    async def sleep(self, duration):
        self.lifecycle.append(("sleep", duration))

    async def send(self, request, **kwargs):
        self.requests.append(request)
        self.options.append(kwargs)
        await asyncio.sleep(0)
        if self.failure:
            raise self.failure
        return JSONResponse(request, {
            "agent_session_id": json.loads(request.body)["agent_session_id"],
            "version_indicator": {"agent_version": "7"}, "status": "active",
        })


class Bytes(httpx2.AsyncByteStream):
    def __init__(self, *, block=False, failure=None):
        self.pulls = self.closes = 0
        self.block, self.failure = block, failure
        self.entered = asyncio.Event()

    async def __aiter__(self):
        self.pulls += 1
        yield b"private-body-never-logged"
        self.entered.set()
        if self.block:
            await asyncio.Event().wait()
        if self.failure:
            raise self.failure
        self.pulls += 1
        yield b"second"

    async def aclose(self):
        self.closes += 1


def binding(action="send", role="architect", operation="synthetic-operation", target="synthetic-child"):
    return e.Binding(operation, role, target, "7", action)


def child():
    session = AgentSession()
    session.state[FOUNDRY_HOSTED_AGENT_SESSION_ID_KEY] = "synthetic-child"
    return Child(role="architect", name=AGENTS["architect"], version="7",
                 hosted_id="synthetic-child", framework=session.to_dict(), bound=True)


def credential():
    return SimpleNamespace(get_token=AsyncMock(
        return_value=AccessToken("private-bearer-never-logged", 4102444800)))


def response_path(role="architect"):
    return PROJECT + f"/agents/{AGENTS[role]}/endpoint/protocols/openai/responses"


class EffectObservationTests(unittest.IsolatedAsyncioTestCase):
    async def test_real_project_create_concurrent_background_and_duplicates(self):
        receipts, wire = [], ProjectWire()
        async with httpx2.AsyncClient() as http:
            async with ProjectClient(credential(), http, {}, transport=wire) as project:
                remote = RemoteAgents(project, {})

                async def create(operation, target, twice=False):
                    selected = child()
                    selected.hosted_id = target
                    with e.dispatch(binding("create", operation=operation, target=target)) as window:
                        await remote.create(selected)
                        if twice:
                            await remote.create(selected)
                    return window

                with e.private_sink(receipts.append):
                    # Actual task inheritance, not a globally mutable binding.
                    one, two = await asyncio.gather(
                        asyncio.create_task(create("operation-one", "child-one", twice=True)),
                        asyncio.create_task(create("operation-two", "child-two")),
                    )
        attempts = [r for r in receipts if r.phase == "request"]
        self.assertEqual(len(wire.requests), 3)
        self.assertEqual(len(attempts), 3)
        self.assertEqual(len({r.occurrence for r in attempts}), 3)
        self.assertEqual([r.binding.target for r in attempts if r.binding.operation == "operation-one"],
                         ["child-one", "child-one"])
        self.assertEqual([r.binding.target for r in attempts if r.binding.operation == "operation-two"], ["child-two"])
        self.assertEqual((one.requests, two.requests), (2, 1))
        self.assertTrue(one.capture_complete and two.capture_complete)
        self.assertEqual(len([r for r in receipts if r.phase == "headers" and r.status == 201]), 3)
        self.assertIn("exit", wire.lifecycle)

    async def test_real_project_error_zero_retry_and_redaction(self):
        receipts = []
        failure = ServiceRequestError("private-exception-never-logged")
        wire = ProjectWire(failure=failure)
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err), e.private_sink(receipts.append):
            async with httpx2.AsyncClient() as http:
                async with ProjectClient(credential(), http, {
                    "x-agent-user-id": "private-identity-never-logged",
                }, transport=wire) as project:
                    with e.dispatch(binding("create")) as window:
                        with self.assertRaises(ServiceRequestError) as raised:
                            await RemoteAgents(project, {}).create(child())
        self.assertIs(raised.exception, failure)
        self.assertEqual(len(wire.requests), 1)
        self.assertTrue(window.capture_complete)  # Observed error is not success.
        self.assertEqual([r.phase for r in receipts], ["window_open", "request", "error", "window_closed"])
        text = json.dumps([asdict(r) for r in receipts]) + out.getvalue() + err.getvalue()
        for forbidden in ("private-exception", "private-identity", "private-bearer", "Authorization", "api-version"):
            self.assertNotIn(forbidden, text)

    async def test_real_foundry_stream_send_then_known_response_get_is_not_send(self):
        text = "Synthetic output."
        payload = {
            "id": "resp_synthetic", "object": "response", "created_at": 1, "model": "",
            "status": "completed", "agent_session_id": "synthetic-child",
            "output": [{"type": "message", "id": "msg_synthetic", "role": "assistant",
                        "status": "completed", "content": [
                            {"type": "output_text", "text": text, "annotations": []}]}],
        }
        events = [
            {"type": "response.created", "response": {**payload, "status": "in_progress", "output": []}},
            {"type": "response.output_text.delta", "item_id": "msg_synthetic", "output_index": 0,
             "content_index": 0, "delta": text},
            {"type": "response.completed", "response": payload},
        ]
        seen, receipts = [], []

        def handle(request):
            seen.append(request.method)
            if request.method == "GET":
                return httpx2.Response(200, json=payload)
            return httpx2.Response(200, headers={"content-type": "text/event-stream"},
                                   stream=RawBytes("".join(
                                       "data: " + json.dumps(event) + "\n\n" for event in events).encode()))

        async with httpx2.AsyncClient(transport=OriginTransport(httpx2.MockTransport(handle))) as http:
            async with ProjectClient(credential(), http, {}) as project:
                remote = RemoteAgents(project, {})
                project.agents.get_session = AsyncMock(return_value=SimpleNamespace(
                    status="active", version_indicator=SimpleNamespace(agent_version="7")))
                selected = child()
                with e.private_sink(receipts.append), e.dispatch(binding()) as window:
                    self.assertEqual(await remote.invoke(selected, {"synthetic": True}, AsyncMock()), text)
                    self.assertEqual(await remote.recover(selected, "resp_synthetic"), text)
        self.assertEqual(seen, ["POST", "GET"])
        self.assertEqual(window.requests, 1)
        self.assertTrue(window.capture_complete)
        self.assertEqual([r.phase for r in receipts],
                         ["window_open", "request", "headers", "stream_complete", "window_closed"])
        # No consumed-model-history assertion can be derived from these receipts.
        self.assertNotIn("history", asdict(receipts[1]))

    async def test_http_status_does_not_suppress_sdk_rejection(self):
        receipts, seen = [], []

        def handle(request):
            seen.append(request.method)
            return httpx2.Response(418, stream=RawBytes(json.dumps(
                {"error": {"message": "private-error-body", "type": "synthetic"}}).encode()))

        async with httpx2.AsyncClient(transport=OriginTransport(httpx2.MockTransport(handle))) as http:
            async with ProjectClient(credential(), http, {}) as project:
                remote = RemoteAgents(project, {})
                project.agents.get_session = AsyncMock(return_value=SimpleNamespace(
                    status="active", version_indicator=SimpleNamespace(agent_version="7")))
                with e.private_sink(receipts.append), e.dispatch(binding()):
                    with self.assertRaises(ChatClientException):
                        await remote.invoke(child(), {}, AsyncMock())
        self.assertEqual(seen, ["POST"])
        self.assertEqual([r.status for r in receipts if r.phase == "headers"], [418])
        self.assertNotIn("private-error-body", repr(receipts))

    async def test_unbuffered_stream_cancel_and_close(self):
        stream, receipts = Bytes(block=True), []
        async with httpx2.AsyncClient(transport=OriginTransport(httpx2.MockTransport(
                lambda request: httpx2.Response(200, stream=stream)))) as http:
            with e.private_sink(receipts.append), e.dispatch(binding()) as window:
                response = await http.send(http.build_request("POST", response_path()), stream=True)
                self.assertEqual(stream.pulls, 0)

                async def consume():
                    async for _ in response.aiter_bytes():
                        pass

                task = asyncio.create_task(consume())
                await stream.entered.wait()
                task.cancel()
                with self.assertRaises(asyncio.CancelledError):
                    await task
                await response.aclose()
                await response.aclose()
        self.assertEqual(stream.closes, 1)
        self.assertTrue(window.capture_complete)
        self.assertEqual([r.category for r in receipts if r.phase == "error"], ["cancelled"])

    async def test_early_close_and_open_stream_are_incomplete(self):
        for close in (True, False):
            receipts, stream = [], Bytes()
            async with httpx2.AsyncClient(transport=OriginTransport(httpx2.MockTransport(
                    lambda request: httpx2.Response(200, stream=stream)))) as http:
                with e.private_sink(receipts.append), e.dispatch(binding()) as window:
                    response = await http.send(http.build_request("POST", response_path()), stream=True)
                    if close:
                        await response.aclose()
                self.assertFalse(window.capture_complete)
                self.assertEqual(receipts[-1].category, "incomplete")
                await response.aclose()
            self.assertFalse(window.capture_complete)

    async def test_stream_and_dispatch_errors_preserve_original_exception(self):
        for failure in (httpx2.ReadTimeout("private-error"), RuntimeError("private-error")):
            receipts, stream = [], Bytes(failure=failure)
            async with httpx2.AsyncClient(transport=OriginTransport(httpx2.MockTransport(
                    lambda request: httpx2.Response(200, stream=stream)))) as http:
                with e.private_sink(receipts.append), e.dispatch(binding()) as window:
                    with self.assertRaises(type(failure)) as raised:
                        await http.post(response_path(), content=b"private-input")
                self.assertIs(raised.exception, failure)
                self.assertTrue(window.capture_complete)
            self.assertNotIn("private-error", repr(receipts))

    async def test_missing_sink_mismatch_and_late_background_capture_is_incomplete(self):
        self.assertIsNone(e.request_attempt("POST", response_path(), "responses"))
        receipts = []
        with e.private_sink(receipts.append):
            with e.dispatch(binding()) as window:
                async def late():
                    await ready.wait()
                    return e.request_attempt("POST", response_path(), "responses")
                ready = asyncio.Event()
                task = asyncio.create_task(late())
                for method, url in (
                    ("GET", response_path()), ("POST", response_path("reviewer")),
                    ("POST", "https://untrusted.example/responses"),
                    ("POST", response_path().replace("https:", "http:")),
                ):
                    self.assertIsNone(e.request_attempt(method, url, "responses"))
            ready.set()
            attempt = await task
            self.assertIsNotNone(attempt)
            attempt.finish("stream_complete", 200)
        self.assertFalse(window.capture_complete)
        self.assertEqual(window.requests, 1)
        self.assertEqual(window.pending, 0)
        self.assertEqual([r.phase for r in receipts], [
            "window_open", "window_closed", "request_late", "request", "stream_complete",
        ])
        self.assertEqual(receipts[1].category, "incomplete")
        self.assertEqual(receipts[2].category, "incomplete")

    async def test_public_transports_keep_completed_then_late_inherited_occurrences(self):
        for action in ("create", "send"):
            with self.subTest(action=action):
                receipts, seen, wire, ready = [], [], ProjectWire(), asyncio.Event()

                def handle(request):
                    seen.append(request)
                    return httpx2.Response(200, stream=RawBytes(json.dumps({
                        "id": "resp_synthetic", "object": "response", "created_at": 1,
                        "model": "", "status": "completed", "output": [],
                    }).encode()))

                async with httpx2.AsyncClient(transport=OriginTransport(
                        httpx2.MockTransport(handle))) as http:
                    async with ProjectClient(credential(), http, {}, transport=wire) as project:
                        client = project.get_openai_client(agent_name=AGENTS["architect"])

                        async def send():
                            if action == "create":
                                await RemoteAgents(project, {}).create(child())
                            else:
                                await client.responses.create(input="private-input")

                        async def late():
                            await ready.wait()
                            await send()

                        with e.private_sink(receipts.append):
                            with e.dispatch(binding(action)) as window:
                                await send()
                                task = asyncio.create_task(late())
                            self.assertTrue(window.capture_complete)
                            closed = next(r for r in receipts if r.phase == "window_closed")
                            self.assertIsNone(closed.category)
                            # A different caller context must not rebind the
                            # inherited task or absorb its late occurrence.
                            with e.dispatch(binding(action, operation="unrelated")) as other:
                                ready.set()
                                await task
                            self.assertEqual(other.requests, 0)
                            self.assertFalse(window.capture_complete)

                self.assertEqual(len(wire.requests if action == "create" else seen), 2)
                self.assertEqual((window.requests, window.pending), (2, 0))
                self.assertTrue(window.truncated)
                requests = [r for r in receipts if r.phase == "request"]
                self.assertEqual(len(requests), 2)
                self.assertEqual(len({r.occurrence for r in requests}), 2)
                self.assertTrue(all(r.binding == binding(action) for r in requests))
                late_marker, = [r for r in receipts if r.phase == "request_late"]
                self.assertEqual(late_marker.occurrence, requests[1].occurrence)
                self.assertEqual(late_marker.category, "incomplete")
                self.assertLess(receipts.index(closed), receipts.index(late_marker))
                terminals = [r for r in receipts if r.phase == (
                    "headers" if action == "create" else "stream_complete")]
                self.assertEqual([r.occurrence for r in terminals],
                                 [r.occurrence for r in requests])
                self.assertNotIn("private-input", repr(receipts))

    async def test_actual_openai_concurrent_and_duplicate_sends_keep_all_occurrences(self):
        receipts, seen = [], []

        async def handle(request):
            seen.append(request)
            await asyncio.sleep(0)
            return httpx2.Response(200, stream=RawBytes(json.dumps({
                "id": "resp_synthetic", "object": "response", "created_at": 1, "model": "",
                "status": "completed", "output": [],
            }).encode()))

        async with httpx2.AsyncClient(transport=OriginTransport(httpx2.MockTransport(handle))) as http:
            async with ProjectClient(credential(), http, {}) as project:
                client = project.get_openai_client(agent_name=AGENTS["architect"])

                async def send(operation, target, count):
                    with e.dispatch(binding(operation=operation, target=target)) as window:
                        for _ in range(count):
                            await client.responses.create(input="private-input", extra_query={
                                "agent_session_id": target,
                            })
                    return window

                with e.private_sink(receipts.append):
                    first, second = await asyncio.gather(
                        send("operation-one", "child-one", 2), send("operation-two", "child-two", 1))
        self.assertEqual(len(seen), 3)
        self.assertEqual((first.requests, second.requests), (2, 1))
        self.assertTrue(first.capture_complete and second.capture_complete)
        requests = [r for r in receipts if r.phase == "request"]
        self.assertEqual(len({r.occurrence for r in requests}), 3)
        self.assertEqual([r.binding.target for r in requests if r.binding.operation == "operation-one"],
                         ["child-one", "child-one"])
        self.assertNotIn("private-input", repr(receipts))
        self.assertNotIn("agent_session_id", repr(receipts))

    async def test_cancel_before_headers_records_once_without_retry(self):
        receipts, seen, entered = [], [], asyncio.Event()

        async def handle(request):
            seen.append(request)
            entered.set()
            await asyncio.Event().wait()

        async with httpx2.AsyncClient(transport=OriginTransport(httpx2.MockTransport(handle))) as http:
            async def send():
                with e.dispatch(binding()):
                    await http.post(response_path())

            with e.private_sink(receipts.append):
                task = asyncio.create_task(send())
                await entered.wait()
                task.cancel()
                with self.assertRaises(asyncio.CancelledError):
                    await task
        self.assertEqual(len(seen), 1)
        self.assertEqual([r.phase for r in receipts], ["window_open", "request", "error", "window_closed"])
        self.assertEqual(receipts[2].category, "cancelled")

    async def test_late_completion_cannot_repair_closed_window_and_close_failure_survives(self):
        receipts = []
        with e.private_sink(receipts.append):
            with e.dispatch(binding()) as window:
                attempt = e.request_attempt("POST", response_path(), "responses")
            attempt.finish("stream_complete", 200)
            self.assertFalse(window.capture_complete)

            failure = RuntimeError("private-close-error")

            class BrokenClose(RawBytes):
                async def aclose(self):
                    raise failure

            with e.dispatch(binding()) as window:
                attempt = e.request_attempt("POST", response_path(), "responses")
                stream = e.ResponseStream(BrokenClose(b"private-body"), attempt, 200)
                self.assertEqual([chunk async for chunk in stream], [b"private-body"])
                with self.assertRaises(RuntimeError) as raised:
                    await stream.aclose()
                self.assertIs(raised.exception, failure)
            self.assertFalse(window.capture_complete)
        self.assertIn("close_error", [r.phase for r in receipts])
        self.assertNotIn("private-close-error", repr(receipts))

    async def test_stop_match_is_exact_and_redirect_is_not_followed(self):
        seen, receipts = [], []
        async with httpx2.AsyncClient(transport=OriginTransport(httpx2.MockTransport(
                lambda request: seen.append(request) or httpx2.Response(
                    302, headers={"location": "https://untrusted.example"}, stream=RawBytes(b"")))),
                follow_redirects=False) as http:
            with e.private_sink(receipts.append), e.dispatch(binding(
                    "stop", "coordinator", target="synthetic-parent")) as window:
                base = PROJECT + f"/agents/{AGENTS['coordinator']}/endpoint/sessions/"
                await http.post(base + "other-parent:stop")
                await http.post(base + "synthetic-parent:stop")
        self.assertEqual(len(seen), 2)
        self.assertEqual(window.requests, 1)
        self.assertEqual([r.status for r in receipts if r.phase == "headers"], [302])

    async def test_broken_private_sink_never_changes_send_or_origin_rejection(self):
        for failure in (OSError("synthetic sink failure"), asyncio.CancelledError()):
            def broken(receipt):
                raise failure

            seen = []
            async with httpx2.AsyncClient(transport=OriginTransport(httpx2.MockTransport(
                    lambda req: seen.append(req) or httpx2.Response(200, stream=RawBytes(b"ok"))))) as http:
                with e.private_sink(broken), e.dispatch(binding()) as window:
                    self.assertEqual((await http.post(response_path())).status_code, 200)
                    with self.assertRaisesRegex(DemoError, "UNAUTHORIZED_ORIGIN"):
                        await http.post("https://untrusted.example/responses")
            self.assertFalse(window.capture_complete)
            self.assertTrue(window.sink_failed)
            self.assertEqual(len(seen), 1)

    async def test_actual_stop_boundary_once_only_and_unknown_hold(self):
        for uncertain in (False, True):
            receipts, seen = [], []
            state = {
                "runtime": "native", "bound": True, "pending": False, "version": "7",
                "framework": {"state": {FOUNDRY_HOSTED_AGENT_SESSION_ID_KEY: "synthetic-parent"}},
            }
            active = {"agent_session_id": "synthetic-parent", "version_indicator": {"agent_version": "7"},
                      "status": "active", "stopped_at": 100}
            idle = dict(active, status="idle", stopped_at=200)
            with tempfile.TemporaryDirectory() as temporary:
                path = Path(temporary) / "parent.json"

                def handle(request):
                    seen.append(request)
                    # Intent is durable before the actual transport invocation.
                    journal = json.loads(Path(str(path) + ".hosting-restart.json").read_text())
                    self.assertEqual(journal["phase"], "stop_pending")
                    if uncertain:
                        raise httpx2.ReadTimeout("private-stop-error")
                    return httpx2.Response(204, stream=RawBytes(b""))

                async with httpx2.AsyncClient(transport=OriginTransport(httpx2.MockTransport(handle))) as http:
                    with e.private_sink(receipts.append):
                        if uncertain:
                            with patch("live_acceptance.rest", return_value=active):
                                with self.assertRaises(httpx2.ReadTimeout):
                                    await stop_hosting_for_acceptance(http, credential(), state, path)
                            before = len(receipts)
                            with patch("live_acceptance.rest", return_value=idle):
                                proof = await stop_hosting_for_acceptance(http, credential(), state, path)
                            self.assertEqual(before, len(receipts))
                            self.assertNotIn("stop_http_status", proof)
                        else:
                            with patch("live_acceptance.rest", side_effect=[active, idle]):
                                proof = await stop_hosting_for_acceptance(http, credential(), state, path)
                            self.assertEqual(proof["stop_http_status"], 204)
                actual = [r for r in receipts if r.phase == "request"]
                self.assertEqual(len(actual), 1)
                self.assertEqual(len(seen), 1)
                self.assertEqual(actual[0].binding.operation, proof["operation_id"])
                self.assertEqual(actual[0].binding.target, "synthetic-parent")

    async def test_nested_windows_and_response_occurrences_are_immutable(self):
        receipts = []
        with e.private_sink(receipts.append), e.dispatch(binding(operation="outer")) as outer:
            with e.dispatch(binding(operation="inner")) as inner:
                attempt = e.request_attempt("POST", response_path(), "responses")
                attempt.finish("headers", 202)
            attempt = e.request_attempt("POST", response_path(), "responses")
            attempt.finish("headers", 200)
        self.assertTrue(outer.capture_complete and inner.capture_complete)
        self.assertEqual([r.binding.operation for r in receipts if r.phase == "request"], ["inner", "outer"])
        with self.assertRaises(FrozenInstanceError):
            receipts[1].status = 999

    async def test_project_transport_configuration_and_lifecycle_are_delegated(self):
        wire = ProjectWire()
        wrapper = e.ProjectTransport(wire)
        self.assertIs(wrapper.connection_config, wire.connection_config)
        self.assertEqual(wrapper.connection_config.timeout, 10)
        self.assertEqual(wrapper.connection_config.read_timeout, 120)
        async with wrapper as opened:
            self.assertIs(opened, wrapper)
            await wrapper.sleep(0)
        self.assertEqual(wire.lifecycle, ["open", ("sleep", 0), "exit", "close"])

    async def test_workflow_dispatch_uses_durable_exact_effect_and_assignment_before_wire(self):
        # Reuse retained in-memory storage/router fixtures, not a new integration
        # contract. Output generation is synthetic; the transports are real.
        from test_workflow import (
            FakeRemote, FakeRouter, MemoryBackend, TestRuntime, make_store, synthetic_calibration,
        )
        backend, receipts, wire = MemoryBackend(), [], ProjectWire()
        actual_ops = []
        test = self
        async with httpx2.AsyncClient(transport=OriginTransport(httpx2.MockTransport(
                lambda request: httpx2.Response(200, stream=RawBytes(b"synthetic-ack"))))) as http:
            async with ProjectClient(credential(), http, {}, transport=wire) as project:
                class Remote(FakeRemote):
                    async def create(self, selected):
                        store = make_store(backend, runtime.scope, "coordinator")
                        effect = (await store.read_manifest()).effect
                        test.assertEqual(effect.status, "dispatched")
                        actual_ops.append(effect.operation_id)
                        await RemoteAgents(project, {}).create(selected)
                        await super().create(selected)

                    async def invoke(self, selected, locator, callback):
                        store = make_store(backend, runtime.scope, "coordinator")
                        effect = (await store.read_manifest()).effect
                        test.assertEqual(effect.status, "dispatched")
                        test.assertEqual(effect.operation_id, locator["operation_id"])
                        assignment = await store.read_assignment(effect.operation_id)
                        test.assertEqual(assignment.producer.session_id, selected.hosted_id)
                        actual_ops.append(effect.operation_id)
                        await http.post(response_path(selected.role))
                        return await super().invoke(selected, locator, callback)

                runtime = TestRuntime(backend, Remote(backend))
                with patch.dict(os.environ, {"DECISION_REQUESTS_PER_MINUTE": "17"}), \
                        patch("demo.workflow.DecisionClient", return_value=FakeRouter()), \
                        patch("demo.workflow.load_calibration", return_value=synthetic_calibration()), \
                        e.private_sink(receipts.append):
                    await runtime.begin("Synthetic requirements.")
                    action, result = await runtime.route(runtime.response_id)
                    self.assertIsNone(result)
                    await runtime.execute(action)
        observed = [r.binding for r in receipts if r.phase == "request"]
        self.assertEqual([b.operation for b in observed], actual_ops)
        self.assertEqual([b.action for b in observed], ["create", "send"])
        self.assertEqual(len({b.target for b in observed}), 1)
        self.assertTrue(all(b.role == "architect" and b.version == "2" for b in observed))


if __name__ == "__main__":
    unittest.main()
