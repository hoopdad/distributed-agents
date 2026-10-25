from __future__ import annotations

import asyncio
import os
from typing import Literal

from agent_framework import Executor, MCPStreamableHTTPTool, WorkflowBuilder, WorkflowContext, handler
from agent_framework_foundry_hosting import WorkflowTurn
from azure.ai.agentserver.core import AgentConfig, get_request_context
from azure.ai.projects.models import A2APreviewToolboxTool, A2AToolboxTool, VersionRefIndicator
from azure.identity.aio import ManagedIdentityCredential
from pydantic import Field, ValidationError, model_validator
from starlette.responses import JSONResponse

from .artifacts import (
    ArtifactError, BoundedId, Identifier, ImmutableModel, Role, ScopeBinding, decode_document,
)
from .config import required
from .contracts import AGENTS, PROJECT, DemoError
from .delegation_diagnostics import WireCapture, failure
from .foundry import ProjectClient, data_client, specialist_identity_headers


class ProbeChild(ImmutableModel):
    role: Literal["architect", "reviewer"]
    version: BoundedId
    session_id: Identifier


class ProbeRequest(ImmutableModel):
    kind: Literal["identity-probe-v1"] = "identity-probe-v1"
    probe_id: Identifier
    action: Literal["delegate", "inspect"]
    session_id: Identifier
    expected_principal: BoundedId | None = None
    children: list[ProbeChild] = Field(default_factory=list, max_length=2)
    identity_forwarding: Literal["platform-and-user", "user-only"] = "platform-and-user"
    specialist_protocol: Literal["invocations", "responses"] = "invocations"
    session_creation: Literal["explicit", "first-response"] = "explicit"

    @model_validator(mode="after")
    def supported_session_creation(self):
        if self.session_creation == "first-response" and (
            self.specialist_protocol != "responses" or self.action != "delegate"
        ):
            raise ValueError("First-response creation requires a Responses delegation probe.")
        return self


class ProbeObservation(ImmutableModel):
    probe_id: Identifier
    role: Role
    version: BoundedId
    status: Literal["verified", "rejected"]
    has_principal: bool
    has_call_id: bool
    session_matches: bool
    principal_matches: bool | None
    check: str | None = Field(default=None, max_length=64)


class ProbeResponseReceipt(ImmutableModel):
    role: Literal["architect", "reviewer"]
    requested_version: BoundedId
    response_id: BoundedId
    status: Literal["completed", "failed", "incomplete", "cancelled", "in_progress", "queued"]


class ProbeResult(ImmutableModel):
    kind: Literal["identity-probe-v1"] = "identity-probe-v1"
    diagnostic_only: Literal[True] = True
    observation: ProbeObservation
    children: list[ProbeObservation] = Field(default_factory=list, max_length=2)
    child_responses: list[ProbeResponseReceipt] = Field(default_factory=list, max_length=2)


class DiscoveryRequest(ImmutableModel):
    kind: Literal["delegation-discovery-v1"] = "delegation-discovery-v1"
    probe_id: Identifier
    session_id: Identifier
    toolbox_name: str = Field(pattern=r"^[A-Za-z0-9_-]{1,128}$")
    toolbox_version: str = Field(pattern=r"^[1-9][0-9]{0,8}$")
    specialist_versions: dict[Literal["architect", "reviewer"], BoundedId] = Field(min_length=2, max_length=2)


class DiscoverySourceFailure(ImmutableModel):
    role: Literal["architect", "reviewer", "unrecognized-source"]
    code: BoundedId
    reported_http_status: int | None


class DiscoveryFailure(ImmutableModel):
    classes: list[BoundedId]
    codes: list[BoundedId]
    mcp_code: int | None
    sources: list[DiscoverySourceFailure]
    http_status: int | None = None
    request_ids: dict[str, BoundedId] = Field(default_factory=dict)


class DiscoveryResult(ImmutableModel):
    kind: Literal["delegation-discovery-v1"] = "delegation-discovery-v1"
    diagnostic_only: Literal[True] = True
    observation: ProbeObservation
    discovery_status: Literal["discovered", "blocked", "rejected"]
    phase: Literal["preparation", "configuration", "tool-discovery"]
    tool_count: int = Field(default=0, ge=0)
    source_bindings_verified: bool = False
    wire_authenticated: bool = False
    wire_call_matches_context: bool = False
    wire_request_count: int = Field(default=0, ge=0)
    platform_toolbox_features_present: bool = False
    request_ids: list[dict[str, BoundedId]] = Field(default_factory=list)
    failure: DiscoveryFailure | None = None
    user_propagation_verified: Literal[False] = False

    @model_validator(mode="after")
    def consistent_discovery(self):
        if self.discovery_status == "discovered" and (
            self.observation.status != "verified" or not self.tool_count or self.failure is not None
            or not self.source_bindings_verified or not self.wire_authenticated or not self.wire_call_matches_context
        ):
            raise ValueError("Discovery requires verified scope, sources and authenticated call context.")
        if self.discovery_status == "blocked" and (self.observation.status != "verified" or self.failure is None):
            raise ValueError("A blocked discovery requires a verified caller and an explicit failure.")
        if self.discovery_status == "rejected" and self.observation.status != "rejected":
            raise ValueError("A rejected discovery cannot report a verified caller.")
        return self


async def discover_delegation(probe: DiscoveryRequest, observation: ProbeObservation, context):
    phase, count, source_verified = "configuration", 0, False
    wire, names, error = {"http": []}, {}, None
    headers = dict(context.platform_headers())
    features = os.environ.get("FOUNDRY_AGENT_TOOLSET_FEATURES", "")
    try:
        if headers != {"x-agent-foundry-call-id": context.call_id}:
            raise DemoError("DIAGNOSTIC_PLATFORM_HEADERS")
        async with ManagedIdentityCredential() as credential, data_client() as http, \
                ProjectClient(credential, http, headers) as project:
            toolbox = await project.toolboxes.get_version(
                probe.toolbox_name, probe.toolbox_version, headers=headers,
            )
            if str(toolbox.version) != probe.toolbox_version or len(toolbox.tools) != 2:
                raise DemoError("DIAGNOSTIC_TOOLBOX_CONFIGURATION")
            roles = set()
            for tool in toolbox.tools:
                role = next((role for role in ("architect", "reviewer") if tool.name == "probe_" + role), None)
                if not isinstance(tool, (A2AToolboxTool, A2APreviewToolboxTool)) or role is None or role in roles:
                    raise DemoError("DIAGNOSTIC_TOOLBOX_SOURCE")
                roles.add(role)
                card_profile_valid = (
                    tool.agent_card_path is None and tool.a2a_version == "1.0"
                    if isinstance(tool, A2AToolboxTool)
                    else tool.agent_card_path == "agentCard/v0.3"
                )
                connection = await project.connections.get(tool.project_connection_id.rsplit("/", 1)[-1], headers=headers)
                target = PROJECT + f"/agents/{AGENTS[role]}/endpoint/protocols/a2a"
                if (
                    tool.project_connection_id not in (connection.id, connection.name)
                    or connection.target != target or tool.base_url not in (None, target)
                    or not card_profile_valid or connection.type != "RemoteA2A"
                    or connection.credentials.type != "UserEntraToken"
                    or connection.metadata.get("ApiType") != "Azure"
                    or tool.send_credentials_for_agent_card is not True
                ):
                    raise DemoError("DIAGNOSTIC_SOURCE_TARGET_CHANGED")
                details = await project.agents.get(AGENTS[role], headers=headers)
                if (details.versions.latest.version != probe.specialist_versions[role]
                        or details.versions.latest.status != "active"):
                    raise DemoError("DIAGNOSTIC_SPECIALIST_VERSION_CHANGED")
                names[connection.name] = names[tool.name] = role
            source_verified = True
            token = await credential.get_token("https://ai.azure.com/.default")
            url = PROJECT + f"/toolboxes/{probe.toolbox_name}/versions/{probe.toolbox_version}/mcp"
            capture = WireCapture({url: "toolbox"}, wire, lambda: None)

            async def observe_request(request):
                await capture.request(request)
                wire["http"][-1]["call_matches_context"] = (
                    request.headers.get("x-agent-foundry-call-id") == context.call_id
                )

            http.event_hooks["request"].append(observe_request)
            http.event_hooks["response"].append(capture.response)
            headers.update(Authorization="Bearer " + token.token)
            headers["Foundry-Features"] = (
                features if any(item.strip().casefold() == "toolboxes=v1preview" for item in features.split(","))
                else "Toolboxes=V1Preview" + ("," + features if features.strip() else "")
            )
            http.headers.update(headers)
            phase = "tool-discovery"
            async with asyncio.timeout(120):
                async with MCPStreamableHTTPTool(
                    name="hosted-delegation-diagnostic", url=url + "?api-version=v1",
                    http_client=http, static_headers=headers, load_prompts=False, request_timeout=120,
                ) as tool:
                    count = len(tool.functions)
                    if not count:
                        raise DemoError("DIAGNOSTIC_NO_DISCOVERED_TOOLS")
            if not wire["http"] or not all(
                row["authorization_present"] and row["call_matches_context"] for row in wire["http"]
            ):
                raise DemoError("DIAGNOSTIC_WIRE_CONTEXT")
    except Exception as caught:
        error = DiscoveryFailure.model_validate(failure(caught, names))
    return DiscoveryResult(
        observation=observation, discovery_status="blocked" if error else "discovered", phase=phase,
        tool_count=count, source_bindings_verified=source_verified,
        wire_authenticated=bool(wire["http"]) and all(row["authorization_present"] for row in wire["http"]),
        wire_call_matches_context=bool(wire["http"]) and all(row["call_matches_context"] for row in wire["http"]),
        wire_request_count=len(wire["http"]),
        platform_toolbox_features_present=bool(features.strip()),
        request_ids=[row.get("request_ids", {}) for row in wire["http"]], failure=error,
    )


async def invoke_probe(http, credential, role, request: ProbeRequest, *, headers, timeout=120):
    token = await credential.get_token("https://ai.azure.com/.default")
    response = await http.post(
        PROJECT + f"/agents/{AGENTS[role]}/endpoint/protocols/invocations",
        params={"api-version": "v1", "agent_session_id": request.session_id},
        json=request.model_dump(mode="json"),
        headers={**headers, "Authorization": "Bearer " + token.token},
        timeout=timeout,
    )
    if response.status_code not in (200, 403) or len(response.content) > 16384:
        raise ArtifactError(f"PROBE_HTTP_{response.status_code}")
    result = ProbeResult.model_validate(decode_document(response.content))
    observation = result.observation
    if (observation.probe_id != request.probe_id or observation.role != role
            or (response.status_code == 200) != (observation.status == "verified")
            or request.action == "inspect" and (result.children or result.child_responses)):
        raise ArtifactError("PROBE_RESPONSE_BINDING")
    return result


async def invoke_discovery_probe(http, credential, request: DiscoveryRequest, *, timeout=180):
    token = await credential.get_token("https://ai.azure.com/.default")
    response = await http.post(
        PROJECT + f"/agents/{AGENTS['coordinator']}/endpoint/protocols/invocations",
        params={"api-version": "v1", "agent_session_id": request.session_id},
        json=request.model_dump(mode="json"), headers={"Authorization": "Bearer " + token.token},
        timeout=timeout,
    )
    if response.status_code not in (200, 403) or len(response.content) > 32768:
        raise ArtifactError(f"PROBE_HTTP_{response.status_code}")
    result = DiscoveryResult.model_validate(decode_document(response.content))
    if (result.observation.probe_id != request.probe_id or result.observation.role != "coordinator"
            or (response.status_code == 200) != (result.observation.status == "verified")):
        raise ArtifactError("PROBE_RESPONSE_BINDING")
    return result


def response_discovery_selected(request):
    marker = (request.request.get("metadata") or {}).get("demo_probe_kind")
    if marker is not None and marker not in ("delegation-discovery-v1", "identity-probe-v1"):
        raise ArtifactError("PROBE_ACTION")
    return marker is not None


async def response_discovery_request(request):
    if (request.request.get("background", False) is not False
            or request.request.get("store") is not True or request.request.get("stream", False) is not False
            or request.request.get("previous_response_id") is not None
            or request.request.get("conversation") is not None):
        raise ArtifactError("PROBE_RESPONSE_OPTIONS")
    text = await request.get_input_text()
    if not isinstance(text, str) or len(text.encode("utf-8")) > 4096:
        raise ArtifactError("PROBE_INPUT_LIMIT")
    model = (ProbeRequest if request.request["metadata"]["demo_probe_kind"] == "identity-probe-v1"
             else DiscoveryRequest)
    return model.model_validate(decode_document(text.encode("utf-8")))


class DiscoveryExecutor(Executor):
    def __init__(self, probe, observation, config, scope):
        super().__init__(id=probe.kind)
        self.probe = probe
        self.observation = observation
        self.config = config
        self.scope = scope

    @handler
    async def discover(self, text: str, context: WorkflowContext[None, str]):
        if text != self.probe.model_dump_json():
            raise ArtifactError("PROBE_INPUT_CHANGED")
        result = (await identity_probe_result(
            self.probe, self.observation, self.config, get_request_context(), self.scope,
        ) if isinstance(self.probe, ProbeRequest)
                  else await discover_delegation(self.probe, self.observation, get_request_context()))
        await context.yield_output(result.model_dump_json())


def probe_action_valid(probe: ProbeRequest, role):
    return (
        probe.action == "delegate" and role == "coordinator" and probe.expected_principal is None
        and [child.role for child in probe.children] == ["architect", "reviewer"]
        and len({probe.session_id, *(child.session_id for child in probe.children)}) == 3
    ) or (
        probe.action == "inspect" and role in ("architect", "reviewer")
        and probe.expected_principal is not None and not probe.children
    )


async def create_host_workflow(request):
    from .workflow import create_workflow

    if not response_discovery_selected(request):
        return create_workflow(request)
    probe = await response_discovery_request(request)
    config, context = AgentConfig.from_env(), get_request_context()
    role = next((role for role, name in AGENTS.items() if config.agent_name == name), None)
    identity = isinstance(probe, ProbeRequest)
    for valid, code in (
        ((identity and probe_action_valid(probe, role))
         or (not identity and role == "coordinator"), "PROBE_ACTION"),
        (config.is_hosted and request.scope.is_hosted and config.project_endpoint == PROJECT, "NATIVE_HOST_PLATFORM"),
        (bool(context.user_id) and request.scope.user_id == context.user_id, "NATIVE_HOST_PRINCIPAL"),
        (bool(context.call_id) and request.scope.call_id == context.call_id, "NATIVE_HOST_CALL"),
        (request.scope.session_id == context.session_id == config.session_id == probe.session_id, "NATIVE_HOST_SESSION"),
        (not identity or probe.action == "delegate" or probe.expected_principal == context.user_id, "PROBE_PRINCIPAL"),
    ):
        if not valid:
            raise ArtifactError(code)
    scope = ScopeBinding.from_platform(config, context, project=PROJECT, tenant=required("EXPECTED_AZURE_TENANT_ID"))
    observation = ProbeObservation(
        probe_id=probe.probe_id, role=role, version=config.agent_version,
        status="verified", has_principal=True, has_call_id=True,
        session_matches=True, principal_matches=True if identity and probe.action == "inspect" else None,
    )
    return WorkflowBuilder(
        name=probe.kind, start_executor=DiscoveryExecutor(probe, observation, config, scope),
    ).build()


async def parse_host_turn(request):
    from .workflow import parse_turn

    if not response_discovery_selected(request):
        return await parse_turn(request)
    return WorkflowTurn(input=(await response_discovery_request(request)).model_dump_json())


async def post_response_probe(client, request, *, on_response_id, headers, timeout):
    async with client.responses.with_streaming_response.create(
        input=request.model_dump_json(), store=True, background=False, stream=False,
        extra_body={"agent_session_id": request.session_id},
        metadata={"demo_probe_kind": request.kind},
        extra_headers=headers, timeout=timeout,
    ) as response:
        chunks, size = [], 0
        async for chunk in response.iter_bytes():
            size += len(chunk)
            if size > 65536:
                raise ArtifactError("PROBE_RESPONSE_LIMIT")
            chunks.append(chunk)
    document = decode_document(b"".join(chunks))
    if not isinstance(document, dict):
        raise ArtifactError("PROBE_RESPONSE_SCHEMA")
    response_id = document.get("id")
    if not isinstance(response_id, str) or not 1 <= len(response_id) <= 128:
        raise ArtifactError("PROBE_RESPONSE_ID")
    await on_response_id(response_id)
    if document.get("agent_session_id") != request.session_id:
        raise ArtifactError("PROBE_SESSION_CHANGED")
    return document


def response_probe_result(document, request, role, model):
    if document.get("status") != "completed":
        raise ArtifactError("PROBE_RESPONSE_INCOMPLETE")
    output = document.get("output")
    if (not isinstance(output, list) or len(output) != 1 or not isinstance(output[0], dict)
            or output[0].get("type") != "message" or output[0].get("role") != "assistant"):
        raise ArtifactError("PROBE_RESPONSE_SCHEMA")
    content = output[0].get("content")
    if (not isinstance(content, list) or len(content) != 1 or not isinstance(content[0], dict)
            or content[0].get("type") != "output_text" or not isinstance(content[0].get("text"), str)):
        raise ArtifactError("PROBE_RESPONSE_SCHEMA")
    result = model.model_validate(decode_document(content[0]["text"].encode("utf-8")))
    if (result.observation.probe_id != request.probe_id or result.observation.role != role
            or result.observation.status != "verified"):
        raise ArtifactError("PROBE_RESPONSE_BINDING")
    return result


async def invoke_coordinator_response_probe(
    http, credential, request: DiscoveryRequest | ProbeRequest, *, on_response_id, timeout=180,
):
    async with ProjectClient(credential, http, {}) as project:
        document = await post_response_probe(
            project.get_openai_client(agent_name=AGENTS["coordinator"]), request,
            on_response_id=on_response_id, headers={}, timeout=timeout,
        )
    model = ProbeResult if isinstance(request, ProbeRequest) else DiscoveryResult
    return response_probe_result(document, request, "coordinator", model)


async def identity_probe_result(probe, observation, config, context, scope):
    children = []
    child_responses = []
    if probe.action == "delegate":
        headers = specialist_identity_headers(config=config, context=context, scope=scope)
        if probe.identity_forwarding == "user-only":
            headers.pop("x-agent-foundry-call-id")
        async with ManagedIdentityCredential() as credential, data_client() as http, \
                ProjectClient(credential, http, headers) as project:
            for child in probe.children:
                details = await project.agents.get(AGENTS[child.role], headers=headers)
                if details.versions.latest.version != child.version or details.versions.latest.status != "active":
                    raise ArtifactError("PROBE_VERSION_CHANGED")
                # The caller records all IDs before dispatch and never
                # repeats an uncertain probe. No create retry or adoption.
                if probe.session_creation == "explicit":
                    created = await project.agents.create_session(
                        AGENTS[child.role], agent_session_id=child.session_id,
                        version_indicator=VersionRefIndicator(agent_version=child.version),
                        headers=headers,
                    )
                    if created.agent_session_id != child.session_id:
                        raise ArtifactError("PROBE_SESSION_CHANGED")
                child_request = ProbeRequest(
                    probe_id=probe.probe_id, action="inspect", session_id=child.session_id,
                    expected_principal=scope.principal,
                )
                if probe.specialist_protocol == "responses":
                    async def remember_response(response_id):
                        child_responses.append(ProbeResponseReceipt(
                            role=child.role, requested_version=child.version,
                            response_id=response_id, status="in_progress",
                        ))
                    document = await post_response_probe(
                        project.get_openai_client(agent_name=AGENTS[child.role]), child_request,
                        on_response_id=remember_response, headers=headers, timeout=180,
                    )
                    child_responses[-1] = ProbeResponseReceipt(
                        role=child.role, requested_version=child.version,
                        response_id=document["id"], status=document.get("status"),
                    )
                    if probe.session_creation == "first-response":
                        created = await project.agents.get_session(
                            AGENTS[child.role], child.session_id, headers=headers,
                        )
                        if (created.agent_session_id != child.session_id
                                or created.version_indicator.agent_version != child.version):
                            raise ArtifactError("PROBE_CHILD_BINDING")
                    if document["status"] != "completed":
                        continue
                    result = response_probe_result(document, child_request, child.role, ProbeResult)
                    if result.children or result.child_responses or result.observation.principal_matches is not True:
                        raise ArtifactError("PROBE_RESPONSE_BINDING")
                else:
                    result = await invoke_probe(
                        http, credential, child.role, child_request, headers=headers,
                    )
                if result.observation.version != child.version:
                    raise ArtifactError("PROBE_VERSION_CHANGED")
                children.append(result.observation)
    return ProbeResult(observation=observation, children=children, child_responses=child_responses)


def register_identity_probe(server):
    @server.invoke_handler
    async def inspect_identity(request):
        size = 0
        chunks = []
        async for chunk in request.stream():
            size += len(chunk)
            if size > 4096:
                return JSONResponse({"error": "PROBE_INPUT_LIMIT"}, status_code=413)
            chunks.append(chunk)
        try:
            document = decode_document(b"".join(chunks))
            probe = (DiscoveryRequest if isinstance(document, dict)
                     and document.get("kind") == "delegation-discovery-v1" else ProbeRequest).model_validate(document)
        except (ArtifactError, ValidationError):
            return JSONResponse({"error": "PROBE_SCHEMA"}, status_code=400)
        config, context = server.config, get_request_context()
        role = next((role for role, name in AGENTS.items() if config.agent_name == name), None)
        if role is None:
            return JSONResponse({"error": "PROBE_ROLE"}, status_code=403)
        expected_principal = probe.expected_principal if isinstance(probe, ProbeRequest) else None
        observation = ProbeObservation(
            probe_id=probe.probe_id, role=role, version=config.agent_version,
            status="rejected", has_principal=bool(context.user_id),
            has_call_id=bool(context.call_id),
            session_matches=(request.query_params.getlist("agent_session_id") in ([], [probe.session_id])
                             and context.session_id == config.session_id == probe.session_id),
            principal_matches=(context.user_id == expected_principal if expected_principal is not None else None),
        )
        action_valid = role == "coordinator" if isinstance(probe, DiscoveryRequest) else probe_action_valid(probe, role)
        check = next((code for valid, code in (
            (config.is_hosted and config.project_endpoint == PROJECT, "NATIVE_HOST_PLATFORM"),
            (observation.has_principal, "NATIVE_HOST_PRINCIPAL"),
            (observation.has_call_id, "NATIVE_HOST_CALL"),
            (observation.session_matches, "NATIVE_HOST_SESSION"),
            (expected_principal is None or observation.principal_matches, "PROBE_PRINCIPAL"),
            (action_valid, "PROBE_ACTION"),
        ) if not valid), None)
        if check is not None:
            if isinstance(probe, DiscoveryRequest):
                return JSONResponse(DiscoveryResult(
                    observation=observation.model_copy(update={"check": check}),
                    discovery_status="rejected", phase="preparation",
                ).model_dump(mode="json"), status_code=403)
            return JSONResponse(ProbeResult(observation=observation.model_copy(
                update={"check": check},
            )).model_dump(mode="json"), status_code=403)
        scope = ScopeBinding.from_platform(
            config, context, project=PROJECT, tenant=required("EXPECTED_AZURE_TENANT_ID"),
        )
        observation = observation.model_copy(update={"status": "verified"})
        if isinstance(probe, DiscoveryRequest):
            return JSONResponse((await discover_delegation(probe, observation, context)).model_dump(mode="json"))
        return JSONResponse((await identity_probe_result(
            probe, observation, config, context, scope,
        )).model_dump(mode="json"))
