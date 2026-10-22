from __future__ import annotations

import asyncio
from contextlib import redirect_stdout
import io
import json
import os
import time
import unittest
from unittest.mock import patch
from uuid import uuid4

os.environ.setdefault("FOUNDRY_PROJECT_ENDPOINT", "https://example.services.ai.azure.com/api/projects/example-project")
os.environ.setdefault("SPECIALIST_MODEL_DEPLOYMENT", "synthetic-worker")
os.environ.setdefault("DECISION_MODEL_DEPLOYMENT", "synthetic-decision")

import httpx2
from azure.ai.projects.models import VersionRefIndicator
from azure.core.credentials import AccessToken
from azure.core.exceptions import ServiceRequestError, HttpResponseError
from azure.core.pipeline import AsyncPipeline
from azure.core.pipeline.transport import AsyncHttpTransport, AsyncHttpResponse, HttpRequest
from azure.identity.aio import ManagedIdentityCredential

from demo import diagnostics as d
from demo.artifact_store import (
    BlobArtifacts, SDKDiagnosticsPolicy, SDKDiagnosticsTransport,
    blob_diagnostics_transport, credential_diagnostics_transport,
)
from demo.foundry import ProjectClient
from demo.contracts import AGENTS


class Response(AsyncHttpResponse):
    def __init__(self, request, status=200, payload=None):
        super().__init__(request, None)
        self.status_code = status
        self.reason = "Synthetic"
        self.headers = {"content-type": "application/json", "etag": '"synthetic-etag"',
                        "content-length": "0", "last-modified": "Wed, 21 Oct 2026 00:00:00 GMT"}
        self.content_type = "application/json"
        self.content = json.dumps(payload or {}).encode()
        self.is_closed = False
        self.body_reads = 0

    def body(self):
        self.body_reads += 1
        return self.content

    def json(self):
        return json.loads(self.content)

    async def read(self):
        return self.body()

    async def close(self):
        self.is_closed = True


class Transport(AsyncHttpTransport):
    def __init__(self, *, failure=None, payload=None, status=200, block=False, statuses=None, pause=False):
        self.failure, self.payload, self.status = failure, payload, status
        self.requests = []
        self.options = []
        self.responses = []
        self.lifecycle = []
        self.block = block
        self.pause = pause
        self.statuses = list(statuses or [])
        self.entered = asyncio.Event()

    async def open(self):
        self.lifecycle.append("open")

    async def close(self):
        self.lifecycle.append("close")

    async def __aenter__(self):
        await self.open()
        return self

    async def __aexit__(self, *args):
        self.lifecycle.append(("exit", args))
        await self.close()

    async def sleep(self, duration):
        self.lifecycle.append(("sleep", duration))

    async def send(self, request, **kwargs):
        self.requests.append(request)
        self.options.append(kwargs)
        self.entered.set()
        if self.pause:
            await asyncio.sleep(0)
        if self.block:
            await asyncio.Event().wait()
        if self.failure:
            raise self.failure
        status = self.statuses.pop(0) if self.statuses else self.status
        response = Response(request, status, self.payload)
        self.responses.append(response)
        return response


class Credential:
    def __init__(self):
        self.calls = 0

    async def get_token(self, *args, **kwargs):
        self.calls += 1
        return AccessToken("synthetic-bearer-secret", int(time.time()) + 3600)


class SDKDiagnosticTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.events = []
        self.sink = patch.object(d, "emit", side_effect=lambda e: self.events.append(d.event_fields(e)))
        self.sink.start()
        self.addCleanup(self.sink.stop)

    def wrapped(self, inner, stage=d.Stage.STORAGE, route=d.Route.BLOB, role="coordinator"):
        return SDKDiagnosticsTransport(inner, stage=stage, route=route, role=role)

    def kinds(self):
        return [e["kind"] for e in self.events]

    async def test_project_real_create_lookup_and_metadata_pipeline(self):
        inner, credential = Transport(payload={"agent_session_id": "synthetic-session-secret"}, status=201), Credential()
        async with httpx2.AsyncClient(transport=httpx2.MockTransport(
            lambda r: self.fail("Project Azure Core operation escaped to httpx2")
        )) as http:
            async with ProjectClient(credential, http, {}, transport=inner) as project:
                result = await project.agents.create_session(
                    AGENTS["architect"], version_indicator=VersionRefIndicator(agent_version="2"),
                )
                self.assertEqual(result.agent_session_id, "synthetic-session-secret")
                inner.status = 200
                await project.agents.get_session(AGENTS["architect"], "synthetic-session-secret")
                await project.agents.get(AGENTS["architect"])
        self.assertEqual(self.kinds(), ["send", "response_headers"] * 3)
        self.assertEqual([e["route"] for e in self.events[::2]],
                         ["sessions", "sessions/{session}", "other"])
        self.assertEqual(len(inner.requests), 3)
        self.assertGreater(credential.calls, 0)
        self.assertTrue(all(r.headers["Authorization"] == "Bearer synthetic-bearer-secret"
                            for r in inner.requests))
        self.assertTrue(all(e["delegation"]["presence"] == "absent" for e in self.events))
        self.assertNotIn("synthetic-session-secret", json.dumps(self.events))

    async def test_project_failure_no_retry_and_sink_failure_preserves_exception(self):
        failure = ServiceRequestError("synthetic-private-url?token=secret")
        inner = Transport(failure=failure)
        async with httpx2.AsyncClient() as http:
            async with ProjectClient(Credential(), http, {}, transport=inner) as project:
                with self.assertRaises(ServiceRequestError) as caught:
                    await project.agents.get_session(AGENTS["architect"], "secret-session")
                self.assertIs(caught.exception, failure)
                self.assertEqual(self.kinds(), ["send", "error"])
                self.assertEqual(len(inner.requests), 1)
                with patch.object(d, "emit", side_effect=RuntimeError("sink-secret")):
                    with self.assertRaises(ServiceRequestError) as caught:
                        await project.agents.get_session(AGENTS["architect"], "secret-session")
                    self.assertIs(caught.exception, failure)

    async def test_http_rejection_is_not_suppressed_or_execution_success(self):
        inner = Transport(status=403, payload={"error": {"code": "Forbidden", "message": "synthetic"}})
        async with httpx2.AsyncClient() as http:
            async with ProjectClient(Credential(), http, {}, transport=inner) as project:
                with self.assertRaises(HttpResponseError):
                    await project.agents.get_session(AGENTS["architect"], "secret-session")
        self.assertEqual(self.kinds(), ["send", "response_headers"])
        self.assertEqual(self.events[-1]["status"], 403)
        self.assertEqual(len(inner.requests), 1)

    async def test_blob_default_factory_actual_read_write_pipeline(self):
        inner = Transport()
        # The scope is never consulted by the SDK constructor or these synthetic
        # direct service calls; application scope/ETag gates retain baseline tests.
        with patch("demo.artifact_store.AioHttpTransport", return_value=inner) as factory:
            artifacts = BlobArtifacts(
                role="reviewer", scope=None, endpoint="https://examplestorage.blob.core.windows.net",
                containers={"control": "control", "candidates": "candidates", "reviews": "reviews"},
                credential=Credential(), expected_private_ips=["10.0.0.1"],
            )
        factory.assert_called_once_with(use_env_settings=False)
        async with artifacts:
            blob = artifacts.service.get_blob_client("reviews", "synthetic-private-blob")
            await blob.get_blob_properties()
            inner.status = 201
            await blob.upload_blob(b"synthetic-private-body", overwrite=False)
        self.assertEqual(self.kinds(), ["send", "response_headers"] * 2)
        self.assertTrue(all(e["role"] == "reviewer" and e["stage"] == "storage"
                            and e["route"] == "blob/{container}/{blob}" for e in self.events))
        self.assertEqual(len(inner.requests), 2)
        self.assertNotIn("synthetic-private", json.dumps(self.events))

    async def test_blob_pipeline_exception_is_observed_once(self):
        failure = ServiceRequestError("synthetic-private-error")
        inner = Transport(failure=failure)
        with patch("demo.artifact_store.AioHttpTransport", return_value=inner):
            artifacts = BlobArtifacts(
                role="coordinator", scope=None, endpoint="https://examplestorage.blob.core.windows.net",
                containers={"control": "control", "candidates": "candidates", "reviews": "reviews"},
                credential=Credential(), expected_private_ips=["10.0.0.1"],
            )
        async with artifacts:
            with self.assertRaises(ServiceRequestError) as caught:
                await artifacts.service.get_blob_client("control", "secret").get_blob_properties()
        self.assertIs(caught.exception, failure)
        self.assertEqual(self.kinds(), ["send", "error"])
        self.assertEqual(len(inner.requests), 1)

    async def test_identity_public_transport_imds_and_appservice_and_cache_gap(self):
        for environment in ({}, {"IDENTITY_ENDPOINT": "https://synthetic.invalid/token",
                                 "IDENTITY_HEADER": "synthetic-identity-header-secret"}):
            self.events.clear()
            inner = Transport(payload={"access_token": "synthetic-token-response-secret",
                                       "expires_in": 3600, "resource": "https://management.azure.com"})
            with patch.dict(os.environ, environment, clear=True), patch(
                "demo.artifact_store.AioHttpTransport", return_value=inner
            ) as factory:
                async with ManagedIdentityCredential(
                    transport=credential_diagnostics_transport(role="architect")
                ) as credential:
                    result = await credential.get_token("https://management.azure.com/.default")
                    count = len(inner.requests)
                    await credential.get_token("https://management.azure.com/.default")
            factory.assert_called_once_with()
            self.assertEqual(result.token, "synthetic-token-response-secret")
            self.assertEqual(len(inner.requests), count, "cache hit must not create fake send event")
            self.assertGreater(count, 0)
            self.assertEqual(self.kinds(), ["send", "response_headers"] * count)
            self.assertTrue(all(e["stage"] == "credential" and e["role"] == "architect"
                                and e["delegation"]["coverage"] == "unavailable"
                                for e in self.events))
            self.assertNotIn("synthetic-token-response-secret", json.dumps(self.events))
            self.assertNotIn("synthetic-identity-header-secret", json.dumps(self.events))

    async def test_wrapper_preserves_request_response_options_and_body_ownership(self):
        inner = Transport()
        request = HttpRequest("PUT", "https://private.invalid/secret?sig=private", data=b"secret-body")
        wrapper = self.wrapped(inner)
        marker = object()
        async with wrapper:
            response = await wrapper.send(request, stream=True, custom=marker)
            self.assertIs(response, inner.responses[0])
            self.assertIs(request, inner.requests[0])
            self.assertIs(inner.options[0]["custom"], marker)
            self.assertTrue(inner.options[0]["stream"])
            self.assertEqual(response.body_reads, 0)
            await wrapper.sleep(0.125)
        self.assertEqual(inner.lifecycle, ["open", ("sleep", 0.125), ("exit", (None, None, None)), "close"])
        self.assertEqual(self.kinds(), ["send", "response_headers"])
        self.assertEqual(self.events[0]["binding"], self.events[1]["binding"])

    async def test_identity_default_retry_chain_remains_owned_by_sdk(self):
        inner = Transport(statuses=[500, 200], payload={
            "access_token": "synthetic-token-response-secret",
            "expires_in": 3600, "resource": "https://management.azure.com",
        })
        environment = {"IDENTITY_ENDPOINT": "https://synthetic.invalid/token",
                       "IDENTITY_HEADER": "synthetic-identity-header-secret"}
        with patch.dict(os.environ, environment, clear=True):
            async with ManagedIdentityCredential(transport=self.wrapped(
                inner, d.Stage.CREDENTIAL, d.Route.TOKEN
            )) as credential:
                await credential.get_token("https://management.azure.com/.default")
        self.assertEqual(len(inner.requests), 2)
        self.assertEqual(self.kinds(), ["send", "response_headers"] * 2)
        self.assertEqual([e["status"] for e in self.events if e["kind"] == "response_headers"],
                         [500, 200])
        self.assertEqual(len({e["binding"]["observation"] for e in self.events}), 2)

    async def test_invalid_diagnostic_role_cannot_stop_sdk_operation(self):
        inner = Transport()
        with patch.dict(os.environ, {"DEMO_ROLE": "invalid-diagnostic-role"}):
            async with AsyncPipeline(inner, [SDKDiagnosticsPolicy()]) as pipeline:
                response = await pipeline.run(HttpRequest("GET", "https://private.invalid/sessions"))
        self.assertIs(response.http_response, inner.responses[0])
        self.assertEqual(self.events, [])

    async def test_policy_preserves_request_and_public_pipeline(self):
        inner = Transport()
        request = HttpRequest("GET", "https://private.invalid/agents/secret/sessions/private?secret=q")
        async with AsyncPipeline(inner, [SDKDiagnosticsPolicy()]) as pipeline:
            response = await pipeline.run(request, stream=True)
        self.assertIs(response.http_response, inner.responses[0])
        self.assertIs(inner.requests[0], request)
        self.assertEqual(response.http_response.body_reads, 0)
        self.assertEqual(self.events[0]["route"], "sessions/{session}")

    async def test_concurrent_bindings_and_header_states(self):
        async def send(value):
            binding = d.new_binding(operation=uuid4(), response=uuid4())
            inner = Transport(pause=True)
            with d.bind(binding):
                request = HttpRequest("GET", "https://private.invalid/blob")
                if value is not None:
                    request.headers["X-MS-USER-IDENTITY"] = value
                async with self.wrapped(inner) as wrapper:
                    await wrapper.send(request)
            return binding
        bindings = await asyncio.gather(send(None), send(""), send("synthetic-user-secret"))
        self.assertIsNone(d.current_binding())
        self.assertEqual([e["delegation"]["presence"] for e in self.events if e["kind"] == "send"],
                         ["absent", "empty", "nonempty"])
        self.assertEqual({e["binding"]["operation"] for e in self.events},
                         {str(b.operation) for b in bindings})
        self.assertEqual(len({e["binding"]["observation"] for e in self.events}), 3)
        for binding in bindings:
            pair = [e for e in self.events if e["binding"]["operation"] == str(binding.operation)]
            self.assertEqual([e["kind"] for e in pair], ["send", "response_headers"])
            self.assertEqual(pair[0]["binding"], pair[1]["binding"])

    async def test_shared_project_policy_concurrent_operation_isolation(self):
        inner = Transport(pause=True)
        async with AsyncPipeline(inner, [SDKDiagnosticsPolicy()]) as pipeline:
            async def send():
                binding = d.new_binding(operation=uuid4())
                with d.bind(binding):
                    await pipeline.run(HttpRequest("GET", "https://private.invalid/sessions"))
                return binding
            bindings = await asyncio.gather(send(), send())
        self.assertEqual(self.kinds(), ["send", "send", "response_headers", "response_headers"])
        for binding in bindings:
            pair = [e for e in self.events if e["binding"]["operation"] == str(binding.operation)]
            self.assertEqual([e["kind"] for e in pair], ["send", "response_headers"])
            self.assertEqual(pair[0]["binding"], pair[1]["binding"])
        self.assertIsNone(d.current_binding())

    async def test_cancel_propagation_in_policy_and_transport(self):
        for use_policy in (False, True):
            self.events.clear()
            inner = Transport(block=True)
            pipeline = AsyncPipeline(inner, [SDKDiagnosticsPolicy()]) if use_policy else AsyncPipeline(
                self.wrapped(inner), []
            )
            async with pipeline:
                task = asyncio.create_task(pipeline.run(HttpRequest("GET", "https://private.invalid/sessions")))
                await inner.entered.wait()
                task.cancel()
                with self.assertRaises(asyncio.CancelledError):
                    await task
            self.assertEqual(self.kinds(), ["send", "cancelled"])
            self.assertEqual(len(inner.requests), 1)

    async def test_redaction_real_logger_and_machine_stdout(self):
        self.sink.stop()
        stdout = io.StringIO()
        with self.assertLogs(d._logger, level="INFO") as logs, redirect_stdout(stdout):
            request = HttpRequest("POST", "https://private.invalid/private-path?token=private-query",
                                  headers={"Authorization": "Bearer private-bearer",
                                           "x-ms-user-identity": "private-user",
                                           "x-agent-user-id": "private-platform",
                                           "x-agent-foundry-call-id": "private-call"},
                                  data=b"private-body")
            async with self.wrapped(Transport()) as wrapper:
                await wrapper.send(request)
            async with self.wrapped(Transport(failure=ValueError("private-exception"))) as wrapper:
                with self.assertRaises(ValueError):
                    await wrapper.send(request)
        self.assertEqual(stdout.getvalue(), "")
        for secret in ("private.invalid", "private-path", "private-query", "private-bearer",
                       "private-user", "private-platform", "private-call", "private-body", "private-exception"):
            self.assertNotIn(secret, "\n".join(logs.output))

    async def test_broken_logger_does_not_replace_response_or_exception(self):
        for failure in (None, ValueError("original-rejection")):
            inner = Transport(failure=failure)
            with patch.object(d, "emit", side_effect=RuntimeError("broken-sink")):
                async with self.wrapped(inner) as wrapper:
                    if failure:
                        with self.assertRaises(ValueError) as caught:
                            await wrapper.send(HttpRequest("GET", "https://private.invalid"))
                        self.assertIs(caught.exception, failure)
                    else:
                        response = await wrapper.send(HttpRequest("GET", "https://private.invalid"))
                        self.assertIs(response, inner.responses[0])

    async def test_blob_helper_is_public_and_preserves_transport_configuration(self):
        with patch("demo.artifact_store.AioHttpTransport") as factory:
            transport = blob_diagnostics_transport(role="architect")
        factory.assert_called_once_with(use_env_settings=False)
        self.assertIs(transport.inner, factory.return_value)
        self.assertEqual(transport.role, "architect")


if __name__ == "__main__":
    unittest.main()
