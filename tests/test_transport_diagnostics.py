from __future__ import annotations

import asyncio
from contextlib import redirect_stdout
import io
import json
import os
from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock, patch
from uuid import uuid4

os.environ.setdefault("FOUNDRY_PROJECT_ENDPOINT", "https://example.services.ai.azure.com/api/projects/example-project")
os.environ.setdefault("SPECIALIST_MODEL_DEPLOYMENT", "synthetic-worker")
os.environ.setdefault("DECISION_MODEL_DEPLOYMENT", "synthetic-decision")

import httpx2
from agent_framework import AgentSession
from agent_framework_foundry import FOUNDRY_HOSTED_AGENT_SESSION_ID_KEY
from demo import diagnostics as d
from demo.contracts import AGENTS, ORIGIN, PROJECT, Child, DemoError
from demo.foundry import OriginTransport, ProjectClient, RemoteAgents, data_client
from demo.routing import DecisionClient


class Chunks(httpx2.AsyncByteStream):
    def __init__(self, failure=None, block=False):
        self.pulls = 0
        self.closes = 0
        self.failure = failure
        self.block = block
        self.entered = asyncio.Event()
        self.first = b"data: synthetic-body-secret\n\n"

    async def __aiter__(self):
        self.pulls += 1
        yield self.first
        self.entered.set()
        if self.block:
            await asyncio.Event().wait()
        if self.failure:
            raise self.failure
        self.pulls += 1
        yield b"second"

    async def aclose(self):
        self.closes += 1


class TransportDiagnosticTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.events = []
        self.sink = patch.object(d, "emit", side_effect=lambda event: self.events.append(d.event_fields(event)))
        self.sink.start()
        self.addCleanup(self.sink.stop)

    def client(self, stream=None, handler=None, **kwargs):
        self.stream = stream if stream is not None else Chunks()
        self.requests = []
        def send(request):
            self.requests.append(request)
            return handler(request) if handler else httpx2.Response(200, stream=self.stream)
        return httpx2.AsyncClient(transport=OriginTransport(httpx2.MockTransport(send), **kwargs))

    def kinds(self):
        return [event["kind"] for event in self.events]

    async def test_final_headers_case_empty_duplicate_and_defaults(self):
        for headers, expected in (
            ([], "absent"), ([("X-MS-USER-IDENTITY", "")], "empty"),
            ([("X-Ms-User-Identity", "synthetic-user-secret")], "nonempty"),
            ([("x-ms-user-identity", "one"), ("X-MS-USER-IDENTITY", "two")], "malformed/duplicate"),
        ):
            self.events.clear()
            async with self.client() as http:
                await http.post(PROJECT + "/openai/v1/responses", headers=headers)
            event = self.events[0]
            self.assertEqual(event["delegation"]["presence"], expected)
            self.assertEqual(event["platform"]["presence"], "absent")
            self.assertEqual(event["route"], "model/responses")
            self.assertEqual(self.requests[0].headers.get_list("x-ms-user-identity"),
                             [value for _, value in headers])
        async with self.client() as http:
            http.headers["x-ms-user-identity"] = "default-secret"
            await http.post(PROJECT + "/responses", headers={"X-MS-USER-IDENTITY": ""})
        self.assertEqual(self.events[-3]["delegation"]["presence"], "empty")

    async def test_no_readahead_chunk_identity_and_lifecycle(self):
        async with self.client() as http:
            async with http.stream("POST", PROJECT + "/openai/v1/responses") as response:
                self.assertEqual(self.stream.pulls, 0)
                self.assertEqual(self.kinds(), ["send", "response_headers"])
                iterator = response.aiter_raw()
                self.assertIs(await anext(iterator), self.stream.first)
                self.assertEqual(self.stream.pulls, 1)
                self.assertEqual(await anext(iterator), b"second")
                with self.assertRaises(StopAsyncIteration):
                    await anext(iterator)
        self.assertEqual(self.stream.closes, 1)
        self.assertEqual(self.kinds(), ["send", "response_headers", "stream_complete"])
        self.assertEqual(len({event["binding"]["observation"] for event in self.events}), 1)
        self.assertTrue(all(0 <= event["duration_ms"] <= 86400000 for event in self.events))
        self.assertNotIn("execution_complete", self.kinds())

    async def test_early_close_delegated_once_without_reading(self):
        async with self.client() as http:
            async with http.stream("GET", PROJECT + "/responses/secret-response"):
                pass
        self.assertEqual(self.stream.pulls, 0)
        self.assertEqual(self.stream.closes, 1)
        self.assertEqual(self.kinds(), ["send", "response_headers", "stream_closed"])

    async def test_stream_error_identity_propagates_and_no_retry(self):
        failure = RuntimeError("synthetic-exception-secret")
        async with self.client(Chunks(failure)) as http:
            with self.assertRaises(RuntimeError) as caught:
                async with http.stream("GET", PROJECT + "/openai/v1/responses") as response:
                    await response.aread()
        self.assertIs(caught.exception, failure)
        self.assertEqual(self.stream.closes, 1)
        self.assertEqual(len(self.requests), 1)
        self.assertEqual(self.kinds(), ["send", "response_headers", "error"])

    async def test_consumer_cancellation_preserves_cleanup(self):
        stream = Chunks(block=True)
        async with self.client(stream) as http:
            async def consume():
                async with http.stream("GET", PROJECT + "/openai/v1/responses") as response:
                    await response.aread()
            task = asyncio.create_task(consume())
            await stream.entered.wait()
            task.cancel()
            with self.assertRaises(asyncio.CancelledError):
                await task
        self.assertEqual(stream.closes, 1)
        self.assertEqual(self.kinds(), ["send", "response_headers", "cancelled"])

    async def test_send_error_timeout_and_cancel_propagate(self):
        for failure, kind, category in (
            (httpx2.ConnectError("secret"), "error", "transport"),
            (httpx2.ReadTimeout("secret"), "error", "timeout"),
            (asyncio.CancelledError("secret"), "cancelled", "cancelled"),
        ):
            self.events.clear()
            def fail(request):
                raise failure
            async with self.client(handler=fail) as http:
                with self.assertRaises(type(failure)) as caught:
                    await http.get(PROJECT + "/openai/v1/responses")
            self.assertIs(caught.exception, failure)
            self.assertEqual(self.kinds(), ["send", kind])
            self.assertEqual(self.events[-1]["category"], category)
            self.assertEqual(len(self.requests), 1)

    async def test_close_failure_propagates_without_duplicate_terminal_event(self):
        stream = Chunks()
        failure = RuntimeError("close-secret")
        stream.aclose = AsyncMock(side_effect=failure)
        async with self.client(stream) as http:
            response = await http.send(http.build_request("GET", PROJECT + "/responses"), stream=True)
            with self.assertRaises(RuntimeError) as caught:
                await response.aclose()
            self.assertIs(caught.exception, failure)
            await response.aclose()
        stream.aclose.assert_awaited_once()
        self.assertEqual(self.kinds(), ["send", "response_headers", "error"])

    async def test_origin_gate_still_rejects_before_send_even_if_logger_broken(self):
        async with self.client() as http:
            with self.assertRaises(DemoError), patch.object(d, "emit", side_effect=RuntimeError("secret")):
                await http.get("https://unauthorized.invalid/responses")
        self.assertEqual(self.requests, [])
        self.assertEqual(self.events, [])
        for url in (ORIGIN.replace("https:", "http:") + "/responses",
                    ORIGIN + ":444/responses"):
            async with self.client() as http:
                with self.assertRaisesRegex(DemoError, "UNAUTHORIZED_ORIGIN"):
                    await http.get(url)
            self.assertFalse(self.requests)

    async def test_redirect_not_followed_and_tls_retry_configuration_preserved(self):
        async with self.client(handler=lambda _: httpx2.Response(
            307, headers={"Location": "https://unauthorized.invalid/secret"}, stream=Chunks(),
        )) as http:
            result = await http.post(PROJECT + "/responses")
        self.assertEqual(result.status_code, 307)
        self.assertEqual(len(self.requests), 1)
        with patch("demo.foundry.httpx2.AsyncHTTPTransport") as inner:
            inner.return_value.aclose = AsyncMock()
            async with data_client():
                pass
            inner.assert_called_once_with(proxy=None, verify=True, trust_env=False, retries=0)

    async def test_diagnostic_failure_cannot_change_stream_or_original_transport_failure(self):
        with patch.object(d, "emit", side_effect=RuntimeError("logger-secret")), \
                patch("demo.foundry.OUTBOUND_CONTEXT_LOGGER.info", side_effect=RuntimeError("legacy-secret")):
            async with self.client(expected_call_id="call", response_id="parent") as http:
                result = await http.post(PROJECT + f"/agents/{AGENTS['architect']}/endpoint/protocols/openai/responses")
            self.assertEqual(result.content, self.stream.first + b"second")
            failure = httpx2.ConnectError("original-secret")
            def fail(_):
                raise failure
            async with self.client(handler=fail) as http:
                with self.assertRaises(httpx2.ConnectError) as caught:
                    await http.get(PROJECT + "/responses")
            self.assertIs(caught.exception, failure)

    async def test_redaction_and_stdout_isolation(self):
        # Use the real JSON serializer/logger, not the test event collector.
        self.sink.stop()
        output = io.StringIO()
        with redirect_stdout(output), self.assertLogs("demo.diagnostics.private", level="INFO") as logs:
            async with self.client() as http:
                await http.post(PROJECT + "/openai/v1/responses?secret-query=secret-value",
                                headers={"Authorization": "Bearer secret-token",
                                         "x-ms-user-identity": "secret-user"},
                                content=b"secret-request-body")
        self.assertEqual(output.getvalue(), "")
        text = "\n".join(logs.output)
        for secret in ("secret", "example.services", "example-project", "Authorization",
                       "Bearer", "synthetic-body", "https://"):
            self.assertNotIn(secret, text)

    async def test_concurrency_and_request_snapshot_after_context_exit(self):
        release = asyncio.Event()
        async def handler(request):
            await release.wait()
            return httpx2.Response(200, stream=Chunks())
        async with self.client(handler=handler) as http:
            async def send():
                alias = uuid4()
                with d.bind(d.new_binding(operation=alias)):
                    task = asyncio.create_task(http.get(PROJECT + "/responses"))
                return task, str(alias)
            first, a = await send()
            second, b = await send()
            release.set()
            await asyncio.gather(first, second)
        groups = {}
        for event in self.events:
            groups.setdefault(event["binding"]["operation"], []).append(event)
        self.assertEqual(set(groups), {a, b})
        self.assertIsNone(d.current_binding())
        for events in groups.values():
            self.assertEqual(len({event["binding"]["observation"] for event in events}), 1)
            self.assertEqual([event["kind"] for event in events],
                             ["send", "response_headers", "stream_complete"])

    async def test_response_alias_is_bound_to_retained_exact_response_parser(self):
        from live_acceptance import outbound_identity
        async with self.client(expected_call_id="call-secret", response_id="response-secret") as http:
            with self.assertLogs("demo.foundry.outbound_context", level="INFO") as logs:
                await http.post(PROJECT + f"/agents/{AGENTS['architect']}/endpoint/protocols/openai/responses",
                                headers={"x-agent-foundry-call-id": "call-secret"})
        self.assertTrue(outbound_identity(logs.output[0], "response-secret")["call_matches_context"])
        alias = self.events[0]["binding"]["response"]
        self.assertIn("response_alias=" + alias, logs.output[0])
        self.assertNotIn("call-secret", logs.output[0])

    async def test_known_response_recovery_issues_only_get_and_still_rejects_incomplete(self):
        session = AgentSession()
        session.state[FOUNDRY_HOSTED_AGENT_SESSION_ID_KEY] = "child"
        child = Child(role="architect", name=AGENTS["architect"], version="1",
                      hosted_id="child", framework=session.to_dict())
        base = PROJECT + f"/agents/{child.name}/endpoint/protocols/openai/responses"
        async with self.client() as http:
            remote = RemoteAgents(SimpleNamespace(openai_clients={}), {})
            remote._check = AsyncMock()
            remote._client = lambda _: None
            state = {"status": "completed"}
            async def retrieve(response_id, **kwargs):
                await http.get(base + "/" + response_id, params=kwargs["extra_query"])
                return SimpleNamespace(id=response_id, output_text="Recovered",
                                       status=state["status"])
            remote.project.openai_clients[child.name] = SimpleNamespace(
                responses=SimpleNamespace(retrieve=retrieve))
            self.assertEqual(await remote.recover(child, "known-response"), "Recovered")
            state["status"] = "failed"
            with self.assertRaisesRegex(DemoError, "SPECIALIST_INCOMPLETE"):
                await remote.recover(child, "known-response")
        self.assertEqual([request.method for request in self.requests], ["GET", "GET"])
        self.assertTrue(all(event["route"] == "responses/{response}" for event in self.events))
        self.assertNotIn("execution_complete", self.kinds())

    async def test_decision_client_uses_actual_transport_after_token_gate(self):
        payload = {"model": "Microsoft-Decision-1", "answers": {"next_action": {
            "type": "choice", "choice": "ask_architect", "confidence": 0.9,
            "probabilities": {"ask_architect": 0.9, "request_input": 0.1},
        }}}
        credential = SimpleNamespace(get_token=AsyncMock(return_value=SimpleNamespace(token="secret-token")))
        # A real transport returns an unread byte stream, not a preloaded mock.
        class JSONChunks(Chunks):
            async def __aiter__(self):
                yield json.dumps(payload).encode()
        async with self.client(stream=JSONChunks()) as http:
            client = DecisionClient(http=http, credential=credential, origin=ORIGIN,
                                    deployment="synthetic", headers={})
            result, _ = await client.score({}, ["ask_architect", "request_input"])
            self.assertEqual(result.model, "Microsoft-Decision-1")
        self.assertEqual(self.events[0]["route"], "model/decision")
        self.assertEqual(self.kinds(), ["send", "response_headers", "stream_complete"])
        credential.get_token.assert_awaited_once()

    async def test_openai_model_constructor_retains_instrumented_http_and_zero_retry(self):
        with patch("azure.ai.projects.aio.AIProjectClient.get_openai_client", return_value=object()) as factory:
            async with self.client() as http:
                project = ProjectClient(SimpleNamespace(), http, {"x-agent-user-id": "secret"})
                try:
                    project.get_openai_client()
                    self.assertIs(factory.call_args.kwargs["http_client"], http)
                    self.assertEqual(factory.call_args.kwargs["max_retries"], 0)
                finally:
                    await project.close()

    async def test_real_pinned_openai_model_request_reaches_instrumented_transport(self):
        from azure.core.credentials import AccessToken
        payload = {
            "id": "model-response-secret", "object": "response", "created_at": 1,
            "model": "synthetic", "status": "completed", "output": [],
        }
        class JSONChunks(Chunks):
            async def __aiter__(self):
                yield json.dumps(payload).encode()
        credential = SimpleNamespace(get_token=AsyncMock(
            return_value=AccessToken("synthetic-token-secret", 4102444800)))
        async with self.client(stream=JSONChunks()) as http:
            project = ProjectClient(credential, http, {"x-agent-user-id": "synthetic-user-secret"})
            try:
                model = project.get_openai_client()
                response = await model.responses.create(model="synthetic", input="synthetic-body-secret")
                self.assertEqual(response.id, payload["id"])
                self.assertEqual(self.requests[0].headers["x-agent-user-id"], "synthetic-user-secret")
                self.assertEqual(self.events[0]["route"], "model/responses")
                self.assertEqual(self.kinds(), ["send", "response_headers", "stream_complete"])
            finally:
                await project.close()
