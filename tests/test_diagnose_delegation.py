from __future__ import annotations

from argparse import Namespace
import asyncio
from contextlib import ExitStack, redirect_stdout
import io
import json
import os
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock, patch

import httpx2
from azure.ai.projects.models import A2AToolboxTool
from mcp.shared.exceptions import McpError
from mcp.types import ErrorData

os.environ.setdefault("FOUNDRY_PROJECT_ENDPOINT", "https://example.services.ai.azure.com/api/projects/example-project")
os.environ.setdefault("SPECIALIST_MODEL_DEPLOYMENT", "synthetic-worker")
os.environ.setdefault("DECISION_MODEL_DEPLOYMENT", "synthetic-decision")

from demo.contracts import AGENTS, PROJECT, DemoError
from demo.foundry import OriginTransport
from scripts import diagnose_delegation as diagnostic

SUBSCRIPTION = "00000000-0000-0000-0000-000000000001"
PROJECT_ID = (
    f"/subscriptions/{SUBSCRIPTION}/resourceGroups/example/providers/"
    "Microsoft.CognitiveServices/accounts/example/projects/" + PROJECT.rsplit("/", 1)[-1]
)
PRIVATE = "synthetic-private-token-identity-endpoint"
REQUEST_ID = "11111111-1111-4111-8111-111111111111"


class DelegationDiagnosticTests(unittest.IsolatedAsyncioTestCase):
    def sources(self):
        return [{"name": role + "-connection", "error": {
            "code": "PERMISSION_DENIED",
            "message": "403 (Forbidden) https://" + PRIVATE + "/?token=" + PRIVATE,
            "details": {"authorization": PRIVATE},
        }} for role in diagnostic.ROLES]

    def test_error_graph_and_embedded_service_json_are_redacted(self):
        for embedded in (False, True):
            with self.subTest(embedded=embedded):
                rows = {"errors": self.sources()}
                error = McpError(ErrorData(
                    code=-32603, message="tools/list failed " + (json.dumps(rows) if embedded else PRIVATE),
                    data=None if embedded else rows,
                ))
                outer = RuntimeError(PRIVATE)
                outer.__cause__ = ExceptionGroup(PRIVATE, [error])
                report = diagnostic.failure(outer, {role + "-connection": role for role in diagnostic.ROLES})
                self.assertEqual({row["role"] for row in report["sources"]}, set(diagnostic.ROLES))
                self.assertEqual([row["reported_http_status"] for row in report["sources"]], [403, 403])
                self.assertNotIn(PRIVATE, json.dumps(report))
                self.assertEqual(report["mcp_code"], -32603)

    def test_correlation_header_allowlist(self):
        result = diagnostic.correlation_ids({
            "apim-request-id": REQUEST_ID, "Authorization": PRIVATE,
            "x-ms-request-id": PRIVATE, "request-id": REQUEST_ID + "\n" + PRIVATE,
            "x-agent-user-id": PRIVATE, "set-cookie": PRIVATE,
            "traceparent": "00-" + "1" * 32 + "-" + "2" * 16 + "-01",
        })
        self.assertEqual(set(result), {"apim-request-id", "traceparent"})
        self.assertNotIn(PRIVATE, json.dumps(result))

    def test_network_observation_is_not_reachability_or_missing_subnet_diagnosis(self):
        result = diagnostic.network_summary({
            "publicNetworkAccess": "Disabled", "restrictOutboundNetworkAccess": True,
            "networkAcls": {"defaultAction": "Deny", "bypass": "None", "ipRules": [PRIVATE]},
            "networkInjections": [{"scenario": "agent", "subnetArmId": PRIVATE}],
            "privateEndpointConnections": [{"id": PRIVATE}, {"id": PRIVATE}],
        })
        self.assertTrue(result["agent_subnet_configured"])
        self.assertFalse(result["reachability_verified"])
        self.assertEqual(result["private_endpoint_count"], 2)
        self.assertNotIn(PRIVATE, json.dumps(result))

    async def test_wire_rejects_invocation_redirect_and_duplicate_before_dispatch(self):
        report = {"http": []}
        capture = diagnostic.WireCapture({PROJECT + "/mcp": "toolbox"}, report, lambda: None)
        for method in ("tools/call", "sampling/createMessage"):
            with self.subTest(method=method), self.assertRaisesRegex(DemoError, "RPC_NOT_READ_ONLY"):
                await capture.request(httpx2.Request("POST", PROJECT + "/mcp", json={"method": method}))
        with self.assertRaisesRegex(DemoError, "TARGET_CHANGED"):
            await capture.request(httpx2.Request("GET", "https://example.invalid/mcp"))
        await capture.request(httpx2.Request("POST", PROJECT + "/mcp", json={"method": "tools/list"}))
        with self.assertRaisesRegex(DemoError, "REPEAT_REFUSED"):
            await capture.request(httpx2.Request("POST", PROJECT + "/mcp", json={"method": "tools/list"}))
        self.assertEqual(len(report["http"]), 1)

    async def run_collection(
        self, *, source_failure=False, entry_status=None, changed_target=False,
        network_error=False, cancelled=False,
    ):
        requests = []
        connections = {}
        tools = []
        for role in diagnostic.ROLES:
            name = role + "-connection"
            connection_id = PROJECT_ID + "/connections/" + name
            target = PROJECT + f"/agents/{AGENTS[role]}/endpoint/protocols/a2a"
            tools.append(A2AToolboxTool(
                name="probe_" + role, a2a_version="1.0", project_connection_id=connection_id,
                send_credentials_for_agent_card=True,
            ))
            connections[name] = SimpleNamespace(
                id=connection_id, name=name, type="RemoteA2A", target=target,
                metadata={"ApiType": "Azure", "private": PRIVATE},
                credentials=SimpleNamespace(type="UserEntraToken", private=PRIVATE),
            )
        if changed_target:
            connections["architect-connection"].target = "https://example.invalid/" + PRIVATE
        project = SimpleNamespace(
            toolboxes=SimpleNamespace(get_version=AsyncMock(return_value=SimpleNamespace(version="2", tools=tools))),
            connections=SimpleNamespace(get=AsyncMock(side_effect=lambda name: connections[name])),
        )
        credential = SimpleNamespace(get_token=AsyncMock(return_value=SimpleNamespace(token=PRIVATE)))

        class Context:
            def __init__(self, value):
                self.value = value

            async def __aenter__(self):
                return self.value

            async def __aexit__(self, *args):
                return False

        def wire(request):
            requests.append(request)
            self.assertEqual(request.headers["Authorization"], "Bearer " + PRIVATE)
            headers = {"apim-request-id": REQUEST_ID, "set-cookie": PRIVATE}
            if request.method == "GET" and any(request.url.path.endswith("/agents/" + name) for name in AGENTS.values()):
                self.assertEqual(request.url.params["api-version"], "v1")
                return httpx2.Response(200, headers=headers, json={
                    "versions": {"latest": {
                        "version": "1", "status": "active",
                        "definition": {"code_configuration": {"content_hash": "a" * 64}},
                    }},
                    "agent_endpoint": {"authorization_schemes": [{"type": "Entra"}]},
                    "private": PRIVATE,
                })
            if request.method == "GET" and "/agentCard/" in request.url.path:
                self.assertEqual(request.url.params["api-version"], "v1")
                return httpx2.Response(200, json={"name": PRIVATE}, headers=headers)
            if entry_status is not None:
                return httpx2.Response(entry_status, json={"message": PRIVATE}, headers=headers)
            if request.method == "GET":
                return httpx2.Response(405)
            if request.method == "DELETE":
                return httpx2.Response(200)
            payload = json.loads(request.content)
            method = payload.get("method")
            self.assertIn(method, diagnostic.RPC_METHODS)
            if method == "notifications/initialized":
                return httpx2.Response(202)
            if method == "initialize":
                result = {
                    "protocolVersion": payload["params"]["protocolVersion"],
                    "capabilities": {"tools": {}}, "serverInfo": {"name": "synthetic", "version": "1"},
                }
            elif method == "ping":
                result = {}
            elif method == "tools/list":
                if source_failure:
                    return httpx2.Response(200, headers=headers, json={
                        "jsonrpc": "2.0", "id": payload["id"],
                        "error": {"code": -32603, "message": "tools/list failed " + json.dumps({"errors": self.sources()})},
                    })
                result = {"tools": [{
                    "name": "probe_" + role, "description": PRIVATE,
                    "inputSchema": {"type": "object", "properties": {}},
                } for role in diagnostic.ROLES]}
            else:
                self.fail("Unexpected RPC")
            return httpx2.Response(200, headers=headers, json={"jsonrpc": "2.0", "id": payload["id"], "result": result})

        def client(**kwargs):
            return httpx2.AsyncClient(
                transport=OriginTransport(httpx2.MockTransport(wire)), follow_redirects=False, trust_env=False,
            )

        network = AsyncMock(return_value={"agent_subnet_configured": True, "reachability_verified": False})
        if network_error:
            network.side_effect = httpx2.ConnectError(PRIVATE)
        if cancelled:
            network.side_effect = asyncio.CancelledError()
        with tempfile.TemporaryDirectory() as directory, ExitStack() as stack:
            path = Path(directory) / "evidence.json"
            args = Namespace(toolbox="synthetic-probe", version="2", evidence=str(path), socks=None, credential_source="azd")
            stack.enter_context(patch("demo.terminal.verify_lab", return_value=("tenant", SUBSCRIPTION, PRIVATE)))
            stack.enter_context(patch("demo.terminal.client_credential", return_value=Context(credential)))
            stack.enter_context(patch("demo.foundry.ProjectClient", return_value=Context(project)))
            stack.enter_context(patch("demo.foundry.data_client", side_effect=client))
            stack.enter_context(patch.object(diagnostic, "read_network", network))
            stack.enter_context(patch("demo.diagnostics.emit"))
            if cancelled:
                with self.assertRaises(asyncio.CancelledError):
                    await diagnostic.collect(args)
                result = json.loads(path.read_text())
            else:
                result = await diagnostic.collect(args)
            self.assertEqual(json.loads(path.read_text()), result)
            self.assertNotIn(PRIVATE, json.dumps(result))
            original = path.read_bytes()
            with self.assertRaises(FileExistsError):
                await diagnostic.collect(args)
            self.assertEqual(original, path.read_bytes())
        return result, requests

    async def test_real_pinned_mcp_discovery_has_safe_ids_and_no_tool_or_model_calls(self):
        report, requests = await self.run_collection()
        self.assertEqual(report["outcome"], "discovery-succeeded")
        self.assertEqual(report["tool_count"], 2)
        self.assertFalse(report["application_acceptance_verified"])
        self.assertFalse(report["trusted_user_propagation_verified"])
        self.assertEqual(set(report["deployments"]), set(AGENTS))
        self.assertTrue(all(row["active"] and row["entra_authorization_preserved"] for row in report["deployments"].values()))
        self.assertTrue(all(row["authorization_present"] for row in report["http"]))
        self.assertTrue(all("x-ms-client-request-id" in request.headers for request in requests))
        self.assertTrue(any(row.get("request_ids", {}).get("apim-request-id") == REQUEST_ID for row in report["http"]))
        self.assertEqual(
            [json.loads(request.content)["method"] for request in requests if request.method == "POST"],
            ["initialize", "notifications/initialized", "ping", "tools/list"],
        )

    async def test_managed_source_denial_is_distinct_from_entry_auth_denial(self):
        report, _ = await self.run_collection(source_failure=True)
        self.assertEqual(report["outcome"], "blocked")
        self.assertIn("MANAGED_AGENT_CARD_FORBIDDEN", report["findings"])
        self.assertIn("DIRECT_SIGNED_IN_USER_CARDS_ACCESSIBLE", report["findings"])
        self.assertNotIn("TOOLBOX_ENTRY_AUTH_REJECTED", report["findings"])
        self.assertEqual(report["root_cause"], "NOT_ESTABLISHED")

    async def test_entry_auth_failure_is_not_reported_as_remote_card_denial(self):
        report, _ = await self.run_collection(entry_status=403)
        self.assertEqual(report["outcome"], "blocked")
        self.assertIn("TOOLBOX_ENTRY_AUTH_REJECTED", report["findings"])
        self.assertNotIn("MANAGED_AGENT_CARD_FORBIDDEN", report["findings"])
        self.assertEqual(sum(row["route"] == "toolbox" for row in report["http"]), 1)

    async def test_changed_target_stops_before_discovery_or_card_get(self):
        report, requests = await self.run_collection(changed_target=True)
        self.assertEqual(report["outcome"], "blocked")
        self.assertEqual(requests, [])
        self.assertIn("DIAGNOSTIC_SOURCE_TARGET_CHANGED", report["errors"][0]["codes"])

    async def test_network_read_failure_is_explicit_and_does_not_hide_independent_evidence(self):
        report, _ = await self.run_collection(network_error=True)
        self.assertEqual(report["outcome"], "incomplete")
        self.assertEqual(report["errors"][0]["phase"], "network-configuration")
        self.assertEqual(report["tool_count"], 2)
        self.assertIn("DIRECT_SIGNED_IN_USER_CARDS_ACCESSIBLE", report["findings"])

    async def test_cancellation_is_persisted_and_propagated_without_application_work(self):
        report, requests = await self.run_collection(cancelled=True)
        self.assertEqual(report["outcome"], "cancelled")
        self.assertEqual(report["phase"], "network-configuration")
        self.assertEqual(requests, [])
        self.assertIn("CancelledError", report["errors"][0]["classes"])

    def test_cli_rejection_is_nonzero_with_closed_output(self):
        report = {
            "outcome": "blocked", "phase": "tool-discovery", "findings": ["MANAGED_AGENT_CARD_FORBIDDEN"],
            "errors": [], "root_cause": "NOT_ESTABLISHED", "private": PRIVATE,
        }
        output = io.StringIO()
        with (
            patch("sys.argv", [
                "diagnose_delegation.py", "--toolbox", "synthetic-probe", "--version", "2",
                "--evidence", "unused-private-path", "--direct",
            ]),
            patch.object(diagnostic, "collect", new=AsyncMock(return_value=report)),
            patch.object(diagnostic.logging, "disable"),
            redirect_stdout(output),
        ):
            self.assertEqual(diagnostic.main(), 2)
        self.assertNotIn(PRIVATE, output.getvalue())
