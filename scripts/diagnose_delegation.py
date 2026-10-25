from __future__ import annotations

import argparse
import asyncio
from datetime import datetime, timezone
import json
import logging
from pathlib import Path
import re
import sys
from urllib.parse import quote, urlsplit

import httpx2
from agent_framework import MCPStreamableHTTPTool
from azure.ai.projects.models import A2AToolboxTool

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from demo.delegation_diagnostics import ROLES, RPC_METHODS, WireCapture, correlation_ids, failure


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
                "remote_a2a", "user_entra_token", "azure_target_metadata", "a2a_version_1",
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
