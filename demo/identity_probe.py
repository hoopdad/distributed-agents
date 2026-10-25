from __future__ import annotations

from typing import Literal

from azure.ai.agentserver.core import get_request_context
from azure.ai.projects.models import VersionRefIndicator
from azure.identity.aio import ManagedIdentityCredential
from pydantic import Field, ValidationError
from starlette.responses import JSONResponse

from .artifacts import (
    ArtifactError, BoundedId, Identifier, ImmutableModel, Role, ScopeBinding, decode_document,
)
from .config import required
from .contracts import AGENTS, PROJECT
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


class ProbeResult(ImmutableModel):
    kind: Literal["identity-probe-v1"] = "identity-probe-v1"
    diagnostic_only: Literal[True] = True
    observation: ProbeObservation
    children: list[ProbeObservation] = Field(default_factory=list, max_length=2)


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
            or request.action == "inspect" and result.children):
        raise ArtifactError("PROBE_RESPONSE_BINDING")
    return result


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
            probe = ProbeRequest.model_validate(decode_document(b"".join(chunks)))
        except (ArtifactError, ValidationError):
            return JSONResponse({"error": "PROBE_SCHEMA"}, status_code=400)
        config, context = server.config, get_request_context()
        role = next((role for role, name in AGENTS.items() if config.agent_name == name), None)
        if role is None:
            return JSONResponse({"error": "PROBE_ROLE"}, status_code=403)
        observation = ProbeObservation(
            probe_id=probe.probe_id, role=role, version=config.agent_version,
            status="rejected", has_principal=bool(context.user_id),
            has_call_id=bool(context.call_id),
            session_matches=(request.query_params.getlist("agent_session_id") in ([], [probe.session_id])
                             and context.session_id == config.session_id == probe.session_id),
            principal_matches=(context.user_id == probe.expected_principal
                               if probe.expected_principal is not None else None),
        )
        check = next((code for valid, code in (
            (config.is_hosted and config.project_endpoint == PROJECT, "NATIVE_HOST_PLATFORM"),
            (observation.has_principal, "NATIVE_HOST_PRINCIPAL"),
            (observation.has_call_id, "NATIVE_HOST_CALL"),
            (observation.session_matches, "NATIVE_HOST_SESSION"),
            (probe.expected_principal is None or observation.principal_matches, "PROBE_PRINCIPAL"),
            ((probe.action == "delegate" and role == "coordinator"
              and probe.expected_principal is None
              and [child.role for child in probe.children] == ["architect", "reviewer"]
              and len({probe.session_id, *(child.session_id for child in probe.children)}) == 3)
             or (probe.action == "inspect" and role != "coordinator"
                 and probe.expected_principal is not None and not probe.children), "PROBE_ACTION"),
        ) if not valid), None)
        if check is not None:
            return JSONResponse(ProbeResult(observation=observation.model_copy(
                update={"check": check},
            )).model_dump(mode="json"), status_code=403)
        scope = ScopeBinding.from_platform(
            config, context, project=PROJECT, tenant=required("EXPECTED_AZURE_TENANT_ID"),
        )
        observation = observation.model_copy(update={"status": "verified"})
        children = []
        if probe.action == "delegate":
            headers = specialist_identity_headers(config=config, context=context, scope=scope)
            async with ManagedIdentityCredential() as credential, data_client() as http, \
                    ProjectClient(credential, http, headers) as project:
                for child in probe.children:
                    details = await project.agents.get(AGENTS[child.role], headers=headers)
                    if details.versions.latest.version != child.version or details.versions.latest.status != "active":
                        raise ArtifactError("PROBE_VERSION_CHANGED")
                    # The caller records all IDs before dispatch and never
                    # repeats an uncertain probe. No create retry or adoption.
                    created = await project.agents.create_session(
                        AGENTS[child.role], agent_session_id=child.session_id,
                        version_indicator=VersionRefIndicator(agent_version=child.version),
                        headers=headers,
                    )
                    if created.agent_session_id != child.session_id:
                        raise ArtifactError("PROBE_SESSION_CHANGED")
                    result = await invoke_probe(
                        http, credential, child.role, ProbeRequest(
                            probe_id=probe.probe_id, action="inspect", session_id=child.session_id,
                            expected_principal=scope.principal,
                        ), headers=headers,
                    )
                    if result.observation.version != child.version:
                        raise ArtifactError("PROBE_VERSION_CHANGED")
                    children.append(result.observation)
        return JSONResponse(ProbeResult(
            observation=observation, children=children,
        ).model_dump(mode="json"))
