from __future__ import annotations

from contextlib import ExitStack
import json
import os
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

os.environ.setdefault("FOUNDRY_PROJECT_ENDPOINT", "https://example.services.ai.azure.com/api/projects/example-project")
os.environ.setdefault("SPECIALIST_MODEL_DEPLOYMENT", "synthetic-worker")
os.environ.setdefault("DECISION_MODEL_DEPLOYMENT", "decision-1")
os.environ.setdefault("EXPECTED_AZURE_TENANT_ID", "11111111-1111-1111-1111-111111111111")

import httpx2
from agent_framework import FileSessionStore, InMemoryCheckpointStorage
from azure.ai.agentserver.core import get_request_context
from azure.ai.agentserver.responses.store._file import FileResponseStore
from azure.ai.agentserver.responses import ResponsesServerOptions
from azure.ai.projects.models import A2AToolboxTool
from mcp.shared.exceptions import McpError
from mcp.types import ErrorData

from demo.artifacts import ArtifactError
from demo.contracts import AGENTS, PROJECT
from demo.host import ProbeResponsesHostServer
from demo.identity_probe import (
    ProbeChild, ProbeObservation, ProbeRequest, ProbeResult, invoke_probe, register_identity_probe,
    DiscoveryFailure, DiscoveryRequest, DiscoveryResult, discover_delegation,
    create_host_workflow, parse_host_turn, invoke_response_discovery_probe,
)
from demo.workflow import create_workflow, parse_turn


SESSION = "a" * 32
PROBE = "b" * 32
USER = "synthetic-user"


def observation(role="architect", *, status="verified", **changes):
    return ProbeObservation(
        probe_id=PROBE, role=role, version="41", status=status,
        has_principal=True, has_call_id=True, session_matches=True, principal_matches=True,
    ).model_copy(update=changes)


class PinnedInvocationsProbeTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.stack = ExitStack()
        root = self.stack.enter_context(tempfile.TemporaryDirectory())
        self.stack.enter_context(patch.dict(os.environ, {
            "FOUNDRY_HOSTING_ENVIRONMENT": "synthetic", "AGENTSERVER_TASKS_BACKEND": "local",
            "AGENTSERVER_STATE_ROOT": root, "OTEL_SDK_DISABLED": "true",
            "FOUNDRY_AGENT_VERSION": "41", "FOUNDRY_AGENT_SESSION_ID": SESSION,
        }))
        self.addCleanup(self.stack.close)

    def server(self, role="architect"):
        with patch.dict(os.environ, {"FOUNDRY_AGENT_NAME": AGENTS[role]}):
            server = ProbeResponsesHostServer(
                workflow=create_workflow, parse_response=parse_turn,
                response_store=FileResponseStore(), configure_observability=None,
            )
        register_identity_probe(server)
        return server

    async def post(self, server, probe=None, *, headers=None, query=None, raw=None):
        probe = probe or ProbeRequest(
            probe_id=PROBE, action="inspect", session_id=SESSION, expected_principal=USER,
        )
        headers = headers if headers is not None else {
            "x-agent-user-id": USER, "x-agent-foundry-call-id": "synthetic-call",
        }
        async with httpx2.AsyncClient(
            transport=httpx2.ASGITransport(app=server), base_url="http://synthetic",
        ) as client:
            return await client.post(
                "/invocations", params=query if query is not None else {"agent_session_id": SESSION},
                content=raw if raw is not None else probe.model_dump_json(), headers=headers,
            )

    async def test_real_dual_host_preserves_responses_and_uses_sdk_invocations_context(self):
        server = self.server()
        paths = {route.path for route in server.routes}
        self.assertIn("/responses", paths)
        self.assertIn("/invocations", paths)
        with patch("demo.identity_probe.ManagedIdentityCredential") as credential, patch(
            "demo.workflow.WorkflowRuntime",
        ) as workflow:
            response = await self.post(server)
        self.assertEqual(response.status_code, 200)
        result = ProbeResult.model_validate(response.json())
        self.assertEqual(result.observation, observation())
        self.assertEqual(result.children, [])
        self.assertTrue(result.diagnostic_only)
        credential.assert_not_called()
        workflow.assert_not_called()
        self.assertIsNone(get_request_context().user_id)
        self.assertNotIn(USER, response.text)
        self.assertNotIn("synthetic-call", response.text)
        response = await self.post(server, query=[])
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["observation"]["session_matches"])

    async def test_missing_trusted_user_cannot_be_repaired_by_body_or_delegation_header(self):
        server = self.server()
        with patch("demo.identity_probe.ManagedIdentityCredential") as credential:
            for headers in (
                {"x-agent-foundry-call-id": "synthetic-call", "x-ms-user-identity": USER},
                {"x-agent-foundry-call-id": "synthetic-call", "x-agent-user-id": ""},
            ):
                response = await self.post(server, headers=headers)
                self.assertEqual(response.status_code, 403)
                result = ProbeResult.model_validate(response.json())
                self.assertEqual(result.observation.status, "rejected")
                self.assertEqual(result.observation.check, "NATIVE_HOST_PRINCIPAL")
                credential.assert_not_called()
        self.assertIsNone(get_request_context().user_id)

    async def test_missing_call_context_is_rejected_even_with_a_user(self):
        response = await self.post(self.server(), headers={"x-agent-user-id": USER})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()["observation"]["check"], "NATIVE_HOST_CALL")

    async def test_scope_query_principal_and_action_fail_closed_before_effects(self):
        server = self.server()
        for changes, query, expected in (
            ({"session_id": "c" * 32}, None, "NATIVE_HOST_SESSION"),
            ({}, [("agent_session_id", SESSION), ("agent_session_id", SESSION)], "NATIVE_HOST_SESSION"),
            ({"expected_principal": "other-user"}, None, "PROBE_PRINCIPAL"),
            ({"action": "delegate"}, None, "PROBE_ACTION"),
        ):
            probe = ProbeRequest(
                probe_id=PROBE, action="inspect", session_id=SESSION, expected_principal=USER,
            ).model_copy(update=changes)
            with self.subTest(changes=changes, query=query), patch(
                "demo.identity_probe.ManagedIdentityCredential",
            ) as credential:
                response = await self.post(server, probe, query=query)
                self.assertEqual(response.status_code, 403)
                self.assertEqual(response.json()["observation"]["check"], expected)
                credential.assert_not_called()

    async def test_invalid_duplicate_and_oversized_payloads_are_not_executed(self):
        for raw, status in (
            (b'{"probe_id":"a","probe_id":"b"}', 400),
            (b'{"kind":"unrecognized"}', 400),
            (b"x" * 4097, 413),
        ):
            with self.subTest(status=status), patch("demo.identity_probe.ManagedIdentityCredential") as credential:
                response = await self.post(self.server(), raw=raw)
                self.assertEqual(response.status_code, status)
                credential.assert_not_called()

    async def test_coordinator_delegates_only_trusted_context_to_both_pinned_new_sessions(self):
        probe = ProbeRequest(
            probe_id=PROBE, action="delegate", session_id=SESSION,
            children=[ProbeChild(role=role, version="41", session_id=identifier * 32)
                      for role, identifier in (("architect", "c"), ("reviewer", "d"))],
        )
        project = MagicMock()
        project.__aenter__ = AsyncMock(return_value=project)
        project.__aexit__ = AsyncMock(return_value=False)
        project.agents.get = AsyncMock(return_value=SimpleNamespace(
            versions=SimpleNamespace(latest=SimpleNamespace(version="41", status="active")),
        ))
        project.agents.create_session = AsyncMock(side_effect=lambda _name, **kwargs: SimpleNamespace(
            agent_session_id=kwargs["agent_session_id"],
        ))

        async def child_result(_http, _credential, role, request, *, headers):
            self.assertEqual(headers, {
                "x-agent-foundry-call-id": "synthetic-call", "x-ms-user-identity": USER,
            })
            self.assertEqual(request.expected_principal, USER)
            self.assertEqual(request.action, "inspect")
            self.assertEqual(request.session_id, next(c.session_id for c in probe.children if c.role == role))
            return ProbeResult(observation=observation(role))

        with patch("demo.identity_probe.ManagedIdentityCredential"), patch(
            "demo.identity_probe.data_client",
        ), patch("demo.identity_probe.ProjectClient", return_value=project), patch(
            "demo.identity_probe.invoke_probe", new=AsyncMock(side_effect=child_result),
        ) as invoke:
            response = await self.post(self.server("coordinator"), probe)
        self.assertEqual(response.status_code, 200)
        result = ProbeResult.model_validate(response.json())
        self.assertEqual([child.role for child in result.children], ["architect", "reviewer"])
        self.assertEqual(invoke.await_count, 2)
        self.assertEqual(project.agents.create_session.await_count, 2)

        project.agents.create_session.reset_mock(side_effect=True)
        project.agents.create_session.side_effect = TimeoutError
        with patch("demo.identity_probe.ManagedIdentityCredential"), patch(
            "demo.identity_probe.data_client",
        ), patch("demo.identity_probe.ProjectClient", return_value=project), patch(
            "demo.identity_probe.invoke_probe", new=AsyncMock(),
        ) as invoke:
            response = await self.post(self.server("coordinator"), probe)
        self.assertEqual(response.status_code, 500)
        project.agents.create_session.assert_awaited_once()
        invoke.assert_not_awaited()

    async def test_rpc_preserves_headers_and_selector_and_rejects_response_rebinding_without_retry(self):
        sent = []

        async def respond(request):
            sent.append(request)
            return httpx2.Response(200, json=ProbeResult(observation=observation()).model_dump(mode="json"))

        credential = SimpleNamespace(get_token=AsyncMock(return_value=SimpleNamespace(token="synthetic-token")))
        probe = ProbeRequest(
            probe_id=PROBE, action="inspect", session_id=SESSION, expected_principal=USER,
        )
        async with httpx2.AsyncClient(transport=httpx2.MockTransport(respond)) as http:
            await invoke_probe(http, credential, "architect", probe, headers={"x-ms-user-identity": USER})
            with self.assertRaisesRegex(ArtifactError, "PROBE_RESPONSE_BINDING"):
                await invoke_probe(
                    http, credential, "architect", probe.model_copy(update={"probe_id": "e" * 32}),
                    headers={"x-ms-user-identity": USER},
                )
        self.assertEqual(len(sent), 2)
        self.assertEqual(sent[0].url.params["agent_session_id"], SESSION)
        self.assertEqual(sent[0].headers["x-ms-user-identity"], USER)
        self.assertNotIn("x-agent-user-id", sent[0].headers)

    def discovery(self):
        return DiscoveryRequest(
            probe_id=PROBE, session_id=SESSION, toolbox_name="synthetic-probe", toolbox_version="2",
            specialist_versions={"architect": "41", "reviewer": "41"},
        )

    async def response_probe(self, *, role="coordinator", headers=None, changes=None):
        headers = headers if headers is not None else {
            "x-agent-user-id": USER, "x-agent-foundry-call-id": "synthetic-call",
        }
        body = {
            "input": self.discovery().model_dump_json(), "store": True, "background": False, "stream": False,
            "metadata": {"demo_probe_kind": "delegation-discovery-v1"},
        }
        body.update(changes or {})
        items = {}
        state_store = MagicMock()
        state_store.__aenter__ = AsyncMock(return_value=state_store)
        state_store.__aexit__ = AsyncMock(return_value=False)
        async def get_item(key, **_kwargs):
            return items.get(key)
        async def save_item(key, value, **kwargs):
            if kwargs.get("if_match") is not None:
                self.assertEqual(kwargs["if_match"], items[key].etag)
            item = SimpleNamespace(value=value, etag=str(len(items) + 1))
            items[key] = item
            return item
        state_store.get_item = AsyncMock(side_effect=get_item)
        state_store.create_item = AsyncMock(side_effect=save_item)
        state_store.set_item = AsyncMock(side_effect=save_item)
        with patch.dict(os.environ, {"FOUNDRY_AGENT_NAME": AGENTS[role]}), patch(
            "azure.ai.agentserver.core.storage.FoundryStateStore.get_or_create",
            new=AsyncMock(return_value=state_store),
        ):
            server = ProbeResponsesHostServer(
                workflow=create_host_workflow, parse_response=parse_host_turn,
                response_store=FileResponseStore(), configure_observability=None,
                options=ResponsesServerOptions(resilient_background=True), unsupported_options="error",
                agent_session_store_provider=SimpleNamespace(get_store=lambda **_: FileSessionStore(
                    Path(os.environ["AGENTSERVER_STATE_ROOT"]) / "native-sessions",
                )),
                checkpoint_store_provider=SimpleNamespace(get_store=lambda **_: InMemoryCheckpointStorage()),
            )
            async with httpx2.AsyncClient(
                transport=httpx2.ASGITransport(app=server), base_url="http://synthetic",
            ) as client:
                return await client.post("/responses", json=body, headers=headers)

    async def test_native_responses_discovery_uses_real_scope_and_no_business_runtime(self):
        async def discover(probe, observed, context):
            self.assertEqual(context.user_id, USER)
            self.assertEqual(context.call_id, "synthetic-call")
            self.assertEqual(probe, self.discovery())
            return DiscoveryResult(
                observation=observed, discovery_status="blocked", phase="configuration",
                failure=DiscoveryFailure(classes=["RuntimeError"], codes=[], mcp_code=None, sources=[]),
            )

        with patch("demo.identity_probe.discover_delegation", new=AsyncMock(side_effect=discover)) as discovery, patch(
            "demo.workflow.WorkflowRuntime",
        ) as business:
            response = await self.response_probe()
        self.assertEqual(response.status_code, 200, response.text)
        body = response.json()
        self.assertEqual(body["status"], "completed", body)
        result = DiscoveryResult.model_validate_json(body["output"][0]["content"][0]["text"])
        self.assertEqual(result.observation.status, "verified")
        self.assertFalse(result.user_propagation_verified)
        discovery.assert_awaited_once()
        business.assert_not_called()
        self.assertNotIn(USER, response.text)
        self.assertNotIn("synthetic-call", response.text)
        self.assertIsNone(get_request_context().user_id)

    async def test_responses_diagnostic_rejects_untrusted_scope_bad_options_and_schema(self):
        for kwargs in (
            {"role": "architect"},
            {"headers": {"x-agent-foundry-call-id": "synthetic-call", "x-ms-user-identity": USER}},
            {"headers": {"x-agent-user-id": USER}},
            {"changes": {"input": self.discovery().model_copy(update={"session_id": "f" * 32}).model_dump_json()}},
            {"changes": {"input": '{"kind":"delegation-discovery-v1","kind":"delegation-discovery-v1"}'}},
            {"changes": {"input": "x" * 4097}},
            {"changes": {"store": False}},
            {"changes": {"metadata": {"demo_probe_kind": "other"}}},
        ):
            with self.subTest(kwargs=kwargs), patch(
                "demo.identity_probe.discover_delegation", new=AsyncMock(),
            ) as discovery, patch("demo.workflow.WorkflowRuntime") as business:
                response = await self.response_probe(**kwargs)
                self.assertTrue(response.status_code >= 400 or response.json().get("status") == "failed", response.text)
                discovery.assert_not_awaited()
                business.assert_not_called()

        for changes in (
            {"background": True}, {"stream": True}, {"previous_response_id": "existing"},
            {"conversation": "existing"},
        ):
            request = SimpleNamespace(
                request={"metadata": {"demo_probe_kind": "delegation-discovery-v1"}, "store": True, **changes},
                get_input_text=AsyncMock(),
            )
            for callback in (create_host_workflow, parse_host_turn):
                with self.assertRaisesRegex(ArtifactError, "PROBE_RESPONSE_OPTIONS"):
                    await callback(request)
            request.get_input_text.assert_not_awaited()

    async def test_ordinary_responses_delegate_to_unchanged_workflow_and_parser(self):
        request = SimpleNamespace(request={"metadata": {"other": "value"}})
        original = object()
        with patch("demo.workflow.create_workflow", return_value=original) as factory, patch(
            "demo.workflow.parse_turn", new=AsyncMock(return_value=original),
        ) as parser, patch("demo.identity_probe.discover_delegation", new=AsyncMock()) as discovery:
            self.assertIs(await create_host_workflow(request), original)
            self.assertIs(await parse_host_turn(request), original)
        factory.assert_called_once_with(request)
        parser.assert_awaited_once_with(request)
        discovery.assert_not_awaited()

    async def test_responses_client_remembers_known_id_before_failure_and_never_retries(self):
        sent, remembered = [], []
        expected = DiscoveryResult(
            observation=observation("coordinator", principal_matches=None),
            discovery_status="blocked", phase="configuration",
            failure=DiscoveryFailure(classes=["RuntimeError"], codes=[], mcp_code=None, sources=[]),
        )
        document = {
            "id": "resp_synthetic", "agent_session_id": SESSION, "status": "completed", "output": [{
                "type": "message", "role": "assistant",
                "content": [{"type": "output_text", "text": expected.model_dump_json()}],
            }],
        }
        async def respond(request):
            sent.append(request)
            return httpx2.Response(200, json=document)
        async def remember(identifier):
            remembered.append(identifier)
        credential = SimpleNamespace(get_token=AsyncMock(return_value=SimpleNamespace(token="synthetic-token")))
        async with httpx2.AsyncClient(transport=httpx2.MockTransport(respond)) as http:
            result = await invoke_response_discovery_probe(
                http, credential, self.discovery(), on_response_id=remember,
            )
            self.assertEqual(result, expected)
            document["status"] = "failed"
            with self.assertRaisesRegex(ArtifactError, "PROBE_RESPONSE_INCOMPLETE"):
                await invoke_response_discovery_probe(http, credential, self.discovery(), on_response_id=remember)
        self.assertEqual(remembered, ["resp_synthetic", "resp_synthetic"])
        self.assertEqual(len(sent), 2)
        self.assertTrue(sent[0].url.path.endswith("/endpoint/protocols/openai/responses"))
        self.assertEqual(sent[0].url.params["agent_session_id"], SESSION)
        self.assertFalse(json.loads(sent[0].content)["background"])
        self.assertNotIn("x-agent-user-id", sent[0].headers)

    async def test_discovery_requires_genuine_coordinator_principal_call_and_session(self):
        for role, headers, query, check in (
            ("architect", None, None, "PROBE_ACTION"),
            ("coordinator", {"x-agent-foundry-call-id": "synthetic-call", "x-ms-user-identity": USER}, None, "NATIVE_HOST_PRINCIPAL"),
            ("coordinator", {"x-agent-user-id": USER}, None, "NATIVE_HOST_CALL"),
            ("coordinator", None, {"agent_session_id": "f" * 32}, "NATIVE_HOST_SESSION"),
        ):
            with self.subTest(check=check), patch("demo.identity_probe.discover_delegation", new=AsyncMock()) as discover:
                response = await self.post(self.server(role), self.discovery(), headers=headers, query=query)
                self.assertEqual(response.status_code, 403)
                result = DiscoveryResult.model_validate(response.json())
                self.assertEqual(result.observation.check, check)
                self.assertEqual(result.discovery_status, "rejected")
                discover.assert_not_awaited()

    async def test_discovery_route_captures_trusted_context_without_business_workflow(self):
        async def discover(probe, observed, context):
            self.assertEqual(context.user_id, USER)
            self.assertEqual(context.platform_headers(), {"x-agent-foundry-call-id": "synthetic-call"})
            self.assertEqual(probe, self.discovery())
            return DiscoveryResult(
                observation=observed, discovery_status="blocked", phase="configuration",
                failure=DiscoveryFailure(classes=["RuntimeError"], codes=[], mcp_code=None, sources=[]),
            )

        with patch("demo.identity_probe.discover_delegation", new=AsyncMock(side_effect=discover)), patch(
            "demo.workflow.WorkflowRuntime",
        ) as workflow:
            response = await self.post(self.server("coordinator"), self.discovery())
        result = DiscoveryResult.model_validate(response.json())
        self.assertEqual(result.observation.status, "verified")
        self.assertFalse(result.user_propagation_verified)
        self.assertNotIn(USER, response.text)
        self.assertNotIn("synthetic-call", response.text)
        workflow.assert_not_called()

    async def discovery_boundary(self, *, blocked=False, version_changed=False):
        project = MagicMock()
        project.__aenter__ = AsyncMock(return_value=project)
        project.__aexit__ = AsyncMock(return_value=False)
        tools, connections = [], {}
        for role in ("architect", "reviewer"):
            identifier = "/synthetic/connections/" + role
            tools.append(A2AToolboxTool(
                name="probe_" + role, project_connection_id=identifier,
                send_credentials_for_agent_card=True, a2a_version="1.0",
            ))
            connections[role] = SimpleNamespace(
                id=identifier, name=role, type="RemoteA2A", credentials=SimpleNamespace(type="UserEntraToken"),
                metadata={"ApiType": "Azure"}, target=PROJECT + f"/agents/{AGENTS[role]}/endpoint/protocols/a2a",
            )
        project.toolboxes.get_version = AsyncMock(return_value=SimpleNamespace(version="2", tools=tools))
        project.connections.get = AsyncMock(side_effect=lambda name, **kwargs: connections[name])
        project.agents.get = AsyncMock(return_value=SimpleNamespace(
            versions=SimpleNamespace(latest=SimpleNamespace(version="42" if version_changed else "41", status="active")),
        ))
        project.agents.create_session = AsyncMock()
        credential = MagicMock()
        credential.__aenter__ = AsyncMock(return_value=credential)
        credential.__aexit__ = AsyncMock(return_value=False)
        credential.get_token = AsyncMock(return_value=SimpleNamespace(token="private-synthetic-token"))
        sent = []

        def respond(request):
            sent.append(request)
            self.assertEqual(request.headers["x-agent-foundry-call-id"], "synthetic-call")
            self.assertEqual(request.headers["Authorization"], "Bearer private-synthetic-token")
            self.assertNotIn("x-ms-user-identity", request.headers)
            self.assertNotIn("x-agent-user-id", request.headers)
            return httpx2.Response(200)

        http = httpx2.AsyncClient(transport=httpx2.MockTransport(respond))

        class Tool:
            functions = [object(), object()]

            async def __aenter__(self):
                await http.post(
                    PROJECT + "/toolboxes/synthetic-probe/versions/2/mcp?api-version=v1",
                    json={"method": "tools/list"},
                )
                if blocked:
                    raise McpError(ErrorData(code=-32007, message="synthetic-private-error", data={
                        "errors": [{"name": role, "error": {"code": "PERMISSION_DENIED", "message": "403 (Forbidden)"}}
                                   for role in ("architect", "reviewer")],
                    }))
                return self

            async def __aexit__(self, *args):
                return False

        with patch("demo.identity_probe.ManagedIdentityCredential", return_value=credential), patch(
            "demo.identity_probe.data_client", return_value=http,
        ), patch("demo.identity_probe.ProjectClient", return_value=project), patch(
            "demo.identity_probe.MCPStreamableHTTPTool", return_value=Tool(),
        ) as tool:
            result = await discover_delegation(
                self.discovery(), observation("coordinator", principal_matches=None),
                SimpleNamespace(call_id="synthetic-call", platform_headers=lambda: {"x-agent-foundry-call-id": "synthetic-call"}),
            )
        project.agents.create_session.assert_not_awaited()
        project.get_openai_client.assert_not_called()
        self.assertNotIn("private-synthetic-token", result.model_dump_json())
        self.assertNotIn("synthetic-private-error", result.model_dump_json())
        self.assertNotIn("synthetic-call", result.model_dump_json())
        if version_changed:
            tool.assert_not_called()
            self.assertEqual(sent, [])
        return result

    async def test_hosted_discovery_forwards_only_genuine_call_and_no_user_substitution(self):
        result = await self.discovery_boundary()
        self.assertEqual(result.discovery_status, "discovered")
        self.assertTrue(result.wire_authenticated)
        self.assertTrue(result.wire_call_matches_context)
        self.assertTrue(result.source_bindings_verified)
        self.assertEqual(result.tool_count, 2)
        self.assertFalse(result.user_propagation_verified)

    async def test_hosted_discovery_preserves_structured_rejection_and_version_gate(self):
        result = await self.discovery_boundary(blocked=True)
        self.assertEqual(result.discovery_status, "blocked")
        self.assertEqual([source.reported_http_status for source in result.failure.sources], [403, 403])
        result = await self.discovery_boundary(version_changed=True)
        self.assertEqual(result.discovery_status, "blocked")
        self.assertIn("DIAGNOSTIC_SPECIALIST_VERSION_CHANGED", result.failure.codes)
        self.assertFalse(result.wire_authenticated)


@unittest.skipUnless(os.name == "nt", "Client session leases are Windows-specific.")
class ProbeUncertaintyTests(unittest.IsolatedAsyncioTestCase):
    async def test_responses_timeout_preserves_known_id_and_cannot_be_resent(self):
        from live_acceptance import run_identity_probe
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "probe.json"
            args = SimpleNamespace(
                scenario="delegation-discovery-responses", toolbox_name="synthetic-probe", toolbox_version="2",
                session_file=str(path), evidence=str(Path(directory) / "evidence.json"), socks=None,
            )
            async def create(*_args, **_kwargs):
                return {"agent_session_id": json.loads(path.read_text())["request"]["session_id"]}
            async def invoke(*_args, on_response_id, **_kwargs):
                await on_response_id("resp_synthetic")
                raise TimeoutError
            with patch("live_acceptance.acceptance_credential"), patch("live_acceptance.data_client"), patch(
                "live_acceptance.rest", new=AsyncMock(side_effect=create),
            ) as rest, patch(
                "demo.identity_probe.invoke_response_discovery_probe", new=AsyncMock(side_effect=invoke),
            ) as dispatched:
                observed = {role: {"version": "41"} for role in AGENTS}
                with self.assertRaises(TimeoutError):
                    await run_identity_probe(args, observed, "tenant", "subscription", USER)
                state = json.loads(path.read_text())
                self.assertEqual(state["phase"], "invocation_dispatched")
                self.assertEqual(state["response_id"], "resp_synthetic")
                self.assertEqual(state["transport"], "responses")
                with self.assertRaisesRegex(RuntimeError, "NEW_IDENTITY_PROBE_REQUIRED_NO_RESEND"):
                    await run_identity_probe(args, observed, "tenant", "subscription", USER)
                rest.assert_awaited_once()
                dispatched.assert_awaited_once()

    async def test_discovery_timeout_cannot_be_resent_or_create_specialist_sessions(self):
        from live_acceptance import run_identity_probe
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "probe.json"
            args = SimpleNamespace(
                scenario="delegation-discovery", toolbox_name="synthetic-probe", toolbox_version="2",
                session_file=str(path), evidence=str(Path(directory) / "evidence.json"), socks=None,
            )
            async def create(*_args, **_kwargs):
                state = json.loads(path.read_text())
                self.assertEqual(state["phase"], "parent_create_dispatched")
                self.assertNotIn("children", state["request"])
                return {"agent_session_id": state["request"]["session_id"]}

            with patch("live_acceptance.acceptance_credential"), patch("live_acceptance.data_client"), patch(
                "live_acceptance.rest", new=AsyncMock(side_effect=create),
            ) as rest, patch("demo.identity_probe.invoke_discovery_probe", new=AsyncMock(side_effect=TimeoutError)) as invoke:
                observed = {role: {"version": "41"} for role in AGENTS}
                with self.assertRaises(TimeoutError):
                    await run_identity_probe(args, observed, "tenant", "subscription", USER)
                self.assertEqual(json.loads(path.read_text())["phase"], "invocation_dispatched")
                with self.assertRaisesRegex(RuntimeError, "NEW_IDENTITY_PROBE_REQUIRED_NO_RESEND"):
                    await run_identity_probe(args, observed, "tenant", "subscription", USER)
                rest.assert_awaited_once()
                invoke.assert_awaited_once()

    async def test_timeout_preserves_reserved_ids_and_prevents_another_create_or_send(self):
        from live_acceptance import run_identity_probe
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "probe.json"
            args = SimpleNamespace(
                session_file=str(path), evidence=str(Path(directory) / "evidence.json"), socks=None,
            )
            observed = {role: {"version": "41"} for role in AGENTS}

            async def create(*_args, **_kwargs):
                state = json.loads(path.read_text())
                self.assertEqual(state["phase"], "parent_create_dispatched")
                request = state["request"]
                self.assertEqual(len({request["session_id"], *(c["session_id"] for c in request["children"])}), 3)
                return {"agent_session_id": request["session_id"]}

            with patch("live_acceptance.acceptance_credential"), patch("live_acceptance.data_client"), patch(
                "live_acceptance.rest", new=AsyncMock(side_effect=create),
            ) as rest, patch("demo.identity_probe.invoke_probe", new=AsyncMock(side_effect=TimeoutError)) as invoke:
                with self.assertRaises(TimeoutError):
                    await run_identity_probe(args, observed, "tenant", "subscription", USER)
                self.assertEqual(json.loads(path.read_text())["phase"], "invocation_dispatched")
                with self.assertRaisesRegex(RuntimeError, "NEW_IDENTITY_PROBE_REQUIRED_NO_RESEND"):
                    await run_identity_probe(args, observed, "tenant", "subscription", USER)
                rest.assert_awaited_once()
                invoke.assert_awaited_once()
