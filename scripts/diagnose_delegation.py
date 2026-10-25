from __future__ import annotations

import argparse
import asyncio
from datetime import datetime, timezone
import json
import logging
from pathlib import Path
import re
import sys
import time
from urllib.parse import quote, urlsplit
import uuid

import httpx2
from agent_framework import MCPStreamableHTTPTool
from azure.ai.projects.models import A2AToolboxTool
from mcp.shared.exceptions import McpError

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

ROLES = ("architect", "reviewer")
REQUEST_IDS = (
    "apim-request-id", "x-ms-request-id", "x-ms-correlation-request-id",
    "request-id", "x-request-id", "x-ms-activity-id",
)
ERROR_CODES = {
    "PERMISSION_DENIED", "UNAUTHENTICATED", "NOT_FOUND", "INVALID_ARGUMENT",
    "INTERNAL", "UNAVAILABLE", "DEADLINE_EXCEEDED", "RESOURCE_EXHAUSTED",
}
RPC_METHODS = {"initialize", "notifications/initialized", "notifications/cancelled", "tools/list", "ping"}


def correlation_ids(headers) -> dict:
    result = {}
    for name in REQUEST_IDS:
        value = headers.get(name, "")
        if re.fullmatch(r"[0-9a-fA-F]{32}|[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}", value):
            result[name] = value
    value = headers.get("traceparent", "")
    if re.fullmatch(r"00-[0-9a-f]{32}-[0-9a-f]{16}-0[01]", value):
        result["traceparent"] = value
    return result


def failure(error: BaseException, names: dict[str, str]) -> dict:
    """Retain error classes/codes, never exception text, identities or URLs."""
    pending, seen, classes, codes, sources = [error], set(), set(), set(), []
    rpc_code = None
    while pending and len(seen) < 32:
        current = pending.pop()
        if id(current) in seen:
            continue
        seen.add(id(current))
        classes.add(type(current).__name__)
        code = getattr(current, "code", None)
        if isinstance(code, str) and (
            re.fullmatch(r"DIAGNOSTIC_[A-Z_]{1,64}", code)
            or code in {"CLIENT_CONFIGURATION", "LAB_AUTH_REQUIRED", "LAB_SCOPE", "AZD_MISSING", "SOCKS_SCOPE"}
        ):
            codes.add(code)
        for nested in (current.__cause__, current.__context__, getattr(current, "inner_exception", None)):
            if isinstance(nested, BaseException):
                pending.append(nested)
        if isinstance(current, BaseExceptionGroup):
            pending.extend(current.exceptions)
        if not isinstance(current, McpError):
            continue
        rpc_code = current.error.code
        data = current.error.data
        if not isinstance(data, dict) or "errors" not in data:
            message = current.error.message
            start = message.find('{"errors":')
            if start < 0 or len(message) > 131072:
                continue
            try:
                data = json.loads(message[start:])
            except ValueError:
                continue
        rows = data.get("errors")
        if not isinstance(rows, list) or len(rows) > 16:
            continue
        for row in rows:
            if not isinstance(row, dict) or not isinstance(row.get("error"), dict):
                continue
            detail = row["error"]
            code = detail.get("code")
            message = detail.get("message")
            status = None
            if isinstance(message, str):
                match = re.search(
                    r"\b(400|401|403|404|408|429|500|502|503|504) "
                    r"\((?:Bad Request|Unauthorized|Forbidden|Not Found|Request Timeout|"
                    r"Too Many Requests|Internal Server Error|Bad Gateway|Service Unavailable|Gateway Timeout)\)",
                    message,
                )
                status = int(match[1]) if match else None
            role = names.get(row.get("name")) if isinstance(row.get("name"), str) else None
            sources.append({
                "role": role or "unrecognized-source",
                "code": code if isinstance(code, str) and code in ERROR_CODES else "UNRECOGNIZED",
                "reported_http_status": status,
            })
    result = {"classes": sorted(classes), "codes": sorted(codes), "mcp_code": rpc_code, "sources": sources}
    response = getattr(error, "response", None)
    if response is not None:
        result["http_status"] = response.status_code
        result["request_ids"] = correlation_ids(response.headers)
    return result


class WireCapture:
    def __init__(self, targets: dict[str, str], report: dict, persist):
        self.targets, self.report, self.persist = targets, report, persist
        self.sent = set()

    async def request(self, request):
        from demo.contracts import DemoError

        route = self.targets.get(str(request.url).split("?", 1)[0])
        if route is None:
            raise DemoError("DIAGNOSTIC_TARGET_CHANGED")
        rpc = None
        if route == "toolbox":
            if request.method == "POST":
                payload = json.loads(await request.aread())
                rpc = payload.get("method")
                if rpc not in RPC_METHODS:
                    raise DemoError("DIAGNOSTIC_RPC_NOT_READ_ONLY")
            elif request.method not in ("GET", "DELETE"):
                raise DemoError("DIAGNOSTIC_METHOD_NOT_READ_ONLY")
        elif request.method != "GET":
            raise DemoError("DIAGNOSTIC_METHOD_NOT_READ_ONLY")
        key = (route, request.method, rpc)
        if key in self.sent:
            raise DemoError("DIAGNOSTIC_REPEAT_REFUSED")
        self.sent.add(key)
        client_id = str(uuid.uuid4())
        request.headers["x-ms-client-request-id"] = client_id
        row = {
            "route": route, "method": request.method, "rpc": rpc,
            "client_request_id": client_id, "authorization_present": bool(request.headers.get("Authorization")),
            "sent_at": datetime.now(timezone.utc).isoformat(), "status": None,
        }
        request.extensions["delegation_diagnostic"] = (row, time.monotonic())
        self.report["http"].append(row)
        self.persist()

    async def response(self, response):
        row, started = response.request.extensions["delegation_diagnostic"]
        row.update(
            status=response.status_code, request_ids=correlation_ids(response.headers),
            duration_ms=round((time.monotonic() - started) * 1000, 1),
        )
        self.persist()


def network_summary(properties: dict) -> dict:
    acls = properties.get("networkAcls") or {}
    injections = properties.get("networkInjections") or []
    return {
        "public_network_access": next(
            (value for value in ("Enabled", "Disabled") if properties.get("publicNetworkAccess") == value), "unobserved",
        ),
        "network_default_action": next(
            (value for value in ("Allow", "Deny") if acls.get("defaultAction") == value), "unobserved",
        ),
        "bypass": next(
            (value for value in ("None", "AzureServices") if acls.get("bypass") == value), "unobserved",
        ),
        "restrict_outbound_network_access": properties.get("restrictOutboundNetworkAccess")
        if type(properties.get("restrictOutboundNetworkAccess")) is bool else None,
        "private_endpoint_count": len(properties["privateEndpointConnections"])
        if isinstance(properties.get("privateEndpointConnections"), list) else None,
        "agent_subnet_configured": any(
            row.get("scenario") == "agent" and bool(row.get("subnetArmId"))
            for row in injections if isinstance(row, dict)
        ),
        "reachability_verified": False,
    }


def findings(report: dict) -> list[str]:
    result = []
    if any(row["route"] == "toolbox" and row["status"] in (401, 403) for row in report["http"]):
        result.append("TOOLBOX_ENTRY_AUTH_REJECTED")
    sources = [source for error in report["errors"] for source in error["sources"]]
    if any(source["reported_http_status"] == 403 for source in sources):
        result.append("MANAGED_AGENT_CARD_FORBIDDEN")
        result.append("MANAGED_CARD_REQUEST_ROUTE_AND_CORRELATION_NOT_OBSERVED")
    if all(report["cards"].get(role, {}).get("http_status") == 200 for role in ROLES):
        result.append("DIRECT_SIGNED_IN_USER_CARDS_ACCESSIBLE")
    if report.get("network", {}).get("agent_subnet_configured"):
        result.append("AGENT_SUBNET_CONFIGURATION_PRESENT_NOT_REACHABILITY_PROOF")
    if report.get("tool_count", 0):
        result.append("TOOL_DISCOVERY_ONLY_NOT_USER_PROPAGATION_OR_APPLICATION_ACCEPTANCE")
    return result


async def read_network(credential, account_id: str) -> dict:
    token = await credential.get_token("https://management.azure.com/.default")
    async with httpx2.AsyncClient(
        transport=httpx2.AsyncHTTPTransport(verify=True, trust_env=False, retries=0),
        trust_env=False, follow_redirects=False, timeout=30,
    ) as arm:
        response = await arm.get(
            "https://management.azure.com" + quote(account_id, safe="/"),
            params={"api-version": "2025-06-01"},
            headers={"Authorization": "Bearer " + token.token},
        )
        response.raise_for_status()
        result = network_summary(response.json()["properties"])
        result["request_ids"] = correlation_ids(response.headers)
        return result


async def collect(args) -> dict:
    from demo.contracts import AGENTS, PROJECT, DemoError
    from demo.foundry import ProjectClient, data_client
    from demo.terminal import client_credential, private_state_path, verify_lab, write_state
    from azure.core.pipeline.transport import AioHttpTransport

    if not re.fullmatch(r"[A-Za-z0-9_-]{1,128}", args.toolbox) or not re.fullmatch(r"[1-9][0-9]{0,8}", args.version):
        raise DemoError("DIAGNOSTIC_TOOLBOX_SELECTOR")
    if not Path(args.evidence).is_absolute():
        raise DemoError("DIAGNOSTIC_EVIDENCE_PATH")
    path = private_state_path(args.evidence)
    report = {
        "schema_version": 1, "started_at": datetime.now(timezone.utc).isoformat(),
        "phase": "authentication", "outcome": "incomplete", "http": [], "cards": {},
        "toolbox_version": args.version, "deployments": {}, "configuration": {}, "errors": [],
        "root_cause": "NOT_ESTABLISHED",
        "trusted_user_propagation_verified": False, "application_acceptance_verified": False,
    }
    write_state(path, report, new=True)
    persist = lambda: write_state(path, report)
    names = {}
    try:
        _, subscription, _ = verify_lab(credential_source=args.credential_source)
        toolbox_url = PROJECT + f"/toolboxes/{args.toolbox}/versions/{args.version}/mcp"
        targets = {toolbox_url: "toolbox"}
        for role in ROLES:
            targets[PROJECT + f"/agents/{AGENTS[role]}/endpoint/protocols/a2a/agentCard/v1.0"] = role
        for role, name in AGENTS.items():
            targets[PROJECT + "/agents/" + name] = role + "-metadata"
        capture = WireCapture(targets, report, persist)
        async with client_credential(subscription, source=args.credential_source) as credential, data_client(
            socks=args.socks,
        ) as http, ProjectClient(
            credential, http, {},
            transport=AioHttpTransport(use_env_settings=False, connection_timeout=10, read_timeout=120),
        ) as project:
            http.event_hooks["request"].append(capture.request)
            http.event_hooks["response"].append(capture.response)
            report["phase"] = "configuration"
            persist()
            toolbox = await project.toolboxes.get_version(args.toolbox, args.version)
            if str(toolbox.version) != args.version or len(toolbox.tools) != 2:
                raise DemoError("DIAGNOSTIC_TOOLBOX_CONFIGURATION")
            project_ids = set()
            for tool in toolbox.tools:
                role = next((role for role in ROLES if tool.name == "probe_" + role), None)
                if not isinstance(tool, A2AToolboxTool) or role is None or role in report["configuration"]:
                    raise DemoError("DIAGNOSTIC_TOOLBOX_SOURCE")
                connection_id = tool.project_connection_id
                if not isinstance(connection_id, str):
                    raise DemoError("DIAGNOSTIC_CONNECTION_ID")
                connection = await project.connections.get(connection_id.rsplit("/", 1)[-1])
                expected = PROJECT + f"/agents/{AGENTS[role]}/endpoint/protocols/a2a"
                if (
                    connection.target != expected or connection_id not in (connection.id, connection.name)
                    or tool.base_url not in (None, expected)
                    or tool.agent_card_path not in (None, "agentCard/v1.0", "/agentCard/v1.0", "/.well-known/agent-card.json")
                ):
                    raise DemoError("DIAGNOSTIC_SOURCE_TARGET_CHANGED")
                project_id = connection.id.rsplit("/connections/", 1)[0]
                project_pattern = (
                    rf"/subscriptions/{re.escape(subscription)}/resourceGroups/[^/]+/providers/"
                    r"Microsoft\.CognitiveServices/accounts/[^/]+/projects/"
                    + re.escape(urlsplit(PROJECT).path.rsplit("/", 1)[-1])
                )
                if not re.fullmatch(project_pattern, project_id, re.IGNORECASE) or ".." in project_id.split("/"):
                    raise DemoError("DIAGNOSTIC_CONNECTION_SCOPE")
                project_ids.add(project_id)
                names[connection.name] = names[tool.name] = role
                report["configuration"][role] = {
                    "remote_a2a": connection.type == "RemoteA2A",
                    "user_entra_token": connection.credentials.type == "UserEntraToken",
                    "azure_target_metadata": connection.metadata.get("ApiType") == "Azure",
                    "authenticated_card_fetch": tool.send_credentials_for_agent_card is True,
                    "card_path": "service-default" if tool.agent_card_path is None else "explicit",
                    "a2a_version_1": tool.a2a_version == "1.0",
                    "target_matches_existing_role": True,
                }
            if len(project_ids) != 1:
                raise DemoError("DIAGNOSTIC_CONNECTION_SCOPE")
            persist()
            report["phase"] = "network-configuration"
            try:
                account_id = project_ids.pop().rsplit("/projects/", 1)[0]
                report["network"] = await read_network(credential, account_id)
            except asyncio.CancelledError as error:
                report["errors"].append({"phase": report["phase"], **failure(error, names)})
                report.update(outcome="cancelled", findings=findings(report), finished_at=datetime.now(timezone.utc).isoformat())
                persist()
                raise
            except Exception as error:
                report["errors"].append({"phase": report["phase"], **failure(error, names)})
            token = await credential.get_token("https://ai.azure.com/.default")
            user_headers = {"Authorization": "Bearer " + token.token}
            headers = {**user_headers, "Foundry-Features": "Toolboxes=V1Preview"}
            report["phase"] = "role-metadata"
            for role, name in AGENTS.items():
                try:
                    response = await http.get(
                        PROJECT + "/agents/" + name, params={"api-version": "v1"}, headers=user_headers,
                    )
                    response.raise_for_status()
                    agent = response.json()
                    latest = agent["versions"]["latest"]
                    version = latest["version"]
                    if not isinstance(version, str) or not re.fullmatch(r"[1-9][0-9]{0,8}", version):
                        raise DemoError("DIAGNOSTIC_DEPLOYMENT_SCHEMA")
                    archive_hash = latest["definition"]["code_configuration"].get("content_hash")
                    report["deployments"][role] = {
                        "version": version, "active": latest["status"] == "active",
                        "entra_authorization_preserved": agent["agent_endpoint"]["authorization_schemes"] == [{"type": "Entra"}],
                        "archive_sha256": archive_hash
                        if isinstance(archive_hash, str) and re.fullmatch(r"[a-fA-F0-9]{64}", archive_hash) else None,
                    }
                    if not report["deployments"][role]["entra_authorization_preserved"]:
                        raise DemoError("DIAGNOSTIC_ROLE_AUTHORIZATION")
                except Exception as error:
                    report["errors"].append({"phase": report["phase"], "role": role, **failure(error, names)})
            report["phase"] = "direct-agent-cards"
            for url, role in targets.items():
                if role not in ROLES:
                    continue
                try:
                    response = await http.get(url, params={"api-version": "v1"}, headers=user_headers)
                    report["cards"][role] = {"http_status": response.status_code}
                    response.raise_for_status()
                    if not isinstance(response.json(), dict):
                        raise DemoError("DIAGNOSTIC_CARD_SCHEMA")
                except Exception as error:
                    report["errors"].append({"phase": report["phase"], "role": role, **failure(error, names)})
            if not all(all(row[field] for field in (
                "remote_a2a", "user_entra_token", "azure_target_metadata", "authenticated_card_fetch", "a2a_version_1",
            )) for row in report["configuration"].values()):
                raise DemoError("DIAGNOSTIC_DELEGATION_CONFIGURATION")
            report["phase"] = "tool-discovery"
            persist()
            http.headers.update(headers)
            async with asyncio.timeout(120):
                async with MCPStreamableHTTPTool(
                    name="delegation-diagnostic", url=toolbox_url + "?api-version=v1",
                    http_client=http, static_headers=headers, load_prompts=False, request_timeout=120,
                ) as tool:
                    report["tool_count"] = len(tool.functions)
                    if not tool.functions:
                        raise DemoError("DIAGNOSTIC_NO_DISCOVERED_TOOLS")
            if not report["errors"]:
                report["outcome"] = "discovery-succeeded"
    except Exception as error:
        report["errors"].append({"phase": report["phase"], **failure(error, names)})
        report["outcome"] = "blocked"
    report["findings"] = findings(report)
    report["finished_at"] = datetime.now(timezone.utc).isoformat()
    persist()
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only delegation discovery; never invokes a tool, model or application session.")
    parser.add_argument("--toolbox", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--evidence", required=True, help="New private JSON path outside the repository.")
    parser.add_argument("--credential-source", choices=("azure-cli", "azd"), default="azd")
    route = parser.add_mutually_exclusive_group(required=True)
    route.add_argument("--direct", action="store_true")
    route.add_argument("--socks")
    args = parser.parse_args()
    # MCP errors may embed remote URLs/text; only the closed report goes to stdout.
    logging.disable(logging.CRITICAL)
    try:
        report = asyncio.run(collect(args))
    except Exception as error:
        print(json.dumps({"outcome": "diagnostic-failed", "error": failure(error, {})}))
        return 2
    print(json.dumps({key: report[key] for key in ("outcome", "phase", "findings", "errors", "root_cause")}))
    return 0 if report["outcome"] == "discovery-succeeded" else 2


if __name__ == "__main__":
    raise SystemExit(main())
