from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import os
import re
import time
import uuid
from contextlib import AsyncExitStack
from dataclasses import replace
from typing import Any
from urllib.parse import urlsplit

import httpx2
from agent_framework import Agent, AgentSession
from agent_framework.foundry import FoundryAgent, FoundryChatClient
from agent_framework_foundry import FOUNDRY_HOSTED_AGENT_SESSION_ID_KEY
from agent_framework_foundry_hosting import AgentSessionStoreProvider
from azure.ai.agentserver.core import AgentConfig, get_request_context
from azure.ai.projects.aio import AIProjectClient
from azure.ai.projects.models import VersionRefIndicator
from azure.core.exceptions import ResourceNotFoundError
from azure.identity.aio import ManagedIdentityCredential

from .config import required
from . import diagnostics as diagnostic
from .artifact_store import SDKDiagnosticsPolicy, credential_diagnostics_transport
from .contracts import (
    AGENTS, LEDGER_KEY, ORIGIN, PROJECT,
    Action, Child, DemoError, Ledger, Role, read_choice,
)
from .coordinator_agent import HostedCoordinator

TRUSTED_USER_ID_HEADER = "x-ms-user-identity"
LEGACY_USER_ID_HEADER = "x-agent-user-id"
SPECIALIST_MODE_ENV = "DEMO_SPECIALIST_MODE"
SPECIALIST_MODES = {"hosted", "in_process"}
OUTBOUND_CONTEXT_LOGGER = logging.getLogger(__name__ + ".outbound_context")
OUTBOUND_CONTEXT_LOGGER.setLevel(logging.INFO)
OUTBOUND_CONTEXT_LOGGER.propagate = False


class _PrivateContextHandler(logging.StreamHandler):
    def handleError(self, record):
        pass


if not OUTBOUND_CONTEXT_LOGGER.handlers:
    OUTBOUND_CONTEXT_LOGGER.addHandler(_PrivateContextHandler())


def _transport_category(exc: BaseException) -> diagnostic.Category:
    if isinstance(exc, asyncio.CancelledError):
        return diagnostic.Category.CANCELLED
    if isinstance(exc, httpx2.TimeoutException):
        return diagnostic.Category.TIMEOUT
    return diagnostic.Category.TRANSPORT


def _transport_event(event, started, kind, *, status=None, category=diagnostic.Category.NONE):
    # Even an unavailable/broken diagnostic sink must preserve the wire outcome.
    try:
        diagnostic.emit(replace(
            event, kind=kind, status=status, category=category,
            duration_ms=min(86_400_000, max(0, (time.perf_counter() - started) * 1000)),
        ))
    except Exception:
        pass


class _ObservedStream(httpx2.AsyncByteStream):
    """No read-ahead or replacement task; the consumer still owns closure."""

    def __init__(self, inner, event, started, status):
        self.inner, self.event, self.started, self.status = inner, event, started, status
        self.terminal = False
        self.closed = False

    def outcome(self, kind, category=diagnostic.Category.NONE):
        if not self.terminal:
            self.terminal = True
            _transport_event(self.event, self.started, kind, status=self.status, category=category)

    async def __aiter__(self):
        try:
            async for chunk in self.inner:
                yield chunk
        except BaseException as exc:
            self.outcome(
                diagnostic.Kind.CANCELLED if isinstance(exc, asyncio.CancelledError)
                else diagnostic.Kind.STREAM_CLOSED if isinstance(exc, GeneratorExit)
                else diagnostic.Kind.ERROR,
                diagnostic.Category.NONE if isinstance(exc, GeneratorExit) else _transport_category(exc),
            )
            raise
        else:
            self.outcome(diagnostic.Kind.STREAM_COMPLETE)

    async def aclose(self):
        if self.closed:
            return
        self.closed = True
        try:
            await self.inner.aclose()
        except BaseException as exc:
            self.outcome(
                diagnostic.Kind.CANCELLED if isinstance(exc, asyncio.CancelledError)
                else diagnostic.Kind.ERROR, _transport_category(exc),
            )
            raise
        else:
            self.outcome(diagnostic.Kind.STREAM_CLOSED)


def _outbound_route(path: str) -> diagnostic.Route:
    # Classify only; never retain concrete resource/response names in events.
    project_path = urlsplit(PROJECT).path
    for name in AGENTS.values():
        base = project_path + f"/agents/{name}/endpoint/protocols/openai/responses"
        if path == base:
            return diagnostic.Route.AGENT_RESPONSES
        if path.startswith(base + "/"):
            return diagnostic.Route.RESPONSE
    if path == "/providers/microsoft/v1/systemone":
        return diagnostic.Route.DECISION
    if path == project_path + "/openai/v1/responses":
        return diagnostic.Route.MODEL
    if path.startswith(project_path + "/openai/v1/responses/"):
        return diagnostic.Route.RESPONSE
    return diagnostic.Route.OTHER


def platform_identity_headers(context) -> dict[str, str]:
    headers = dict(context.platform_headers())
    if context.user_id:
        headers[TRUSTED_USER_ID_HEADER] = context.user_id
        headers[LEGACY_USER_ID_HEADER] = context.user_id
    return headers


def specialist_identity_headers(*, config, context, scope) -> dict[str, str]:
    """B candidate: delegate only a revalidated authenticated parent's identity.

    Caller supplies captured hosting context, never assignment/model input.
    Child receiver equality remains mandatory; this does not select B live.
    """
    from .artifacts import ScopeBinding

    if config.project_endpoint != PROJECT:
        raise DemoError("CANDIDATE_PARENT_BINDING")
    trusted = ScopeBinding.from_platform(
        config, context, project=PROJECT, tenant=required("EXPECTED_AZURE_TENANT_ID"),
    )
    if trusted != scope:
        raise DemoError("CANDIDATE_PARENT_BINDING")
    headers = dict(context.platform_headers())
    if (
        set(headers) != {"x-agent-foundry-call-id"}
        or headers["x-agent-foundry-call-id"] != context.call_id
    ):
        raise DemoError("CANDIDATE_PLATFORM_HEADERS")
    if (
        not isinstance(context.user_id, str)
        or not re.fullmatch(r"[A-Za-z0-9._:@-]{1,256}", context.user_id)
        or context.user_id == context.call_id
    ):
        raise DemoError("CANDIDATE_DELEGATED_IDENTITY")
    headers[TRUSTED_USER_ID_HEADER] = context.user_id
    return headers


def specialist_mode() -> str:
    mode = os.environ.get(SPECIALIST_MODE_ENV, "hosted").strip().lower()
    if mode not in SPECIALIST_MODES:
        raise DemoError("SPECIALIST_MODE_CONFIGURATION", {"mode": mode})
    return mode


def create_specialist_agent(role: Role, **kwargs) -> Agent:
    from .architect_agent import ArchitectAgent
    from .reviewer_agent import ReviewerAgent

    if role not in ("architect", "reviewer"):
        raise DemoError("ROLE_CONFIGURATION")
    agent_type = ArchitectAgent if role == "architect" else ReviewerAgent
    return agent_type(**kwargs)


class OriginTransport(httpx2.AsyncBaseTransport):
    """No token-bearing request or redirect can escape the selected origin."""

    def __init__(
        self, inner: httpx2.AsyncBaseTransport, *,
        expected_call_id: str | None = None, response_id: str | None = None,
    ):
        if (expected_call_id is not None or response_id is not None) and (
            not expected_call_id or not response_id
        ):
            raise DemoError("OUTBOUND_CONTEXT_CONFIGURATION")
        self.inner = inner
        self.expected_call_id = expected_call_id
        self.response_binding = hashlib.sha256(response_id.encode()).hexdigest() if response_id else None
        # Local alias only, never a user/response value or identity hash.
        self.diagnostic_response_alias = uuid.uuid4() if response_id else None

    def _observation(self, request):
        try:
            role = diagnostic.Role(os.environ.get("DEMO_ROLE", "coordinator"))
            parent = diagnostic.current_binding()
            binding = diagnostic.new_binding(
                operation=parent.operation if parent else None,
                response=(parent.response if parent and parent.response
                          else self.diagnostic_response_alias),
            )
            return diagnostic.Event(
                role, diagnostic.Stage.OUTBOUND, diagnostic.Kind.SEND,
                method=next((method for method in diagnostic.Method if method.value == request.method),
                            diagnostic.Method.OTHER),
                route=_outbound_route(request.url.path), binding=binding,
                delegation=diagnostic.observe_header(request.headers.raw, "delegation"),
                platform=diagnostic.observe_header(request.headers.raw, "platform"),
                call=diagnostic.observe_header(request.headers.raw, "call"),
            )
        except Exception:
            return None

    async def handle_async_request(self, request):
        if (
            request.url.scheme != "https"
            or request.url.host != urlsplit(ORIGIN).hostname
            or request.url.port not in (None, 443)
        ):
            raise DemoError("UNAUTHORIZED_ORIGIN")
        started = time.perf_counter()
        event = self._observation(request)
        if self.response_binding and request.method == "POST":
            role = next((role for role, name in AGENTS.items() if request.url.path ==
                         urlsplit(PROJECT).path + f"/agents/{name}/endpoint/protocols/openai/responses"), None)
            if role is not None:
                call_id = request.headers.get("x-agent-foundry-call-id")
                # Retained parser-compatible response binding, not an identity
                # hash. New lifecycle events never hash or emit header values.
                try:
                    OUTBOUND_CONTEXT_LOGGER.info(
                        "Diagnostic response_alias=%s Native outbound context response_binding=%s role=%s has_call_id=%s "
                        "call_matches_context=%s has_delegated_user=%s has_container_user=%s.",
                        event.binding.response if event is not None else self.diagnostic_response_alias,
                        self.response_binding, role, bool(call_id),
                        call_id == self.expected_call_id,
                        bool(request.headers.get(TRUSTED_USER_ID_HEADER)),
                        bool(request.headers.get(LEGACY_USER_ID_HEADER)),
                    )
                except Exception:
                    pass
        if event is not None:
            _transport_event(event, started, diagnostic.Kind.SEND)
        try:
            response = await self.inner.handle_async_request(request)
        except BaseException as exc:
            if event is not None:
                _transport_event(
                    event, started, diagnostic.Kind.CANCELLED if isinstance(exc, asyncio.CancelledError)
                    else diagnostic.Kind.ERROR, category=_transport_category(exc),
                )
            raise
        if event is not None:
            _transport_event(event, started, diagnostic.Kind.RESPONSE_HEADERS, status=response.status_code)
            response.stream = _ObservedStream(response.stream, event, started, response.status_code)
        return response

    async def aclose(self):
        await self.inner.aclose()


def data_client(
    *, socks: str | None = None, expected_call_id: str | None = None, response_id: str | None = None,
) -> httpx2.AsyncClient:
    if socks:
        uri = urlsplit(socks)
        if (
            uri.scheme != "socks5h" or uri.hostname != "127.0.0.1"
            or not uri.port or uri.port < 1024 or uri.username or uri.password
            or uri.path or uri.query or uri.fragment
        ):
            raise DemoError("SOCKS_SCOPE")
    return httpx2.AsyncClient(
        transport=OriginTransport(
            httpx2.AsyncHTTPTransport(proxy=socks, verify=True, trust_env=False, retries=0),
            expected_call_id=expected_call_id, response_id=response_id,
        ),
        timeout=120,
        follow_redirects=False,
        trust_env=False,
    )


class ProjectClient(AIProjectClient):
    def __init__(self, credential, http: httpx2.AsyncClient, headers: dict[str, str], *, transport=None):
        super().__init__(
            PROJECT, credential, allow_preview=True,
            retry_total=0, connection_timeout=10, read_timeout=120,
            per_call_policies=[SDKDiagnosticsPolicy()],
            **({"transport": transport} if transport is not None else {}),
        )
        self.http = http
        self.call_headers = headers
        self.openai_clients: dict[str, Any] = {}

    def get_openai_client(self, *, agent_name=None, **kwargs):
        default_headers = {
            **kwargs.get("default_headers", {}),
            **self.call_headers,
        }
        kwargs.update(
            http_client=self.http, max_retries=0, timeout=120,
            default_headers=default_headers,
        )
        client = super().get_openai_client(agent_name=agent_name, **kwargs)
        self.openai_clients[agent_name or "model"] = client
        return client


class HostedJournal:
    def __init__(self, config: AgentConfig, context):
        self.store = AgentSessionStoreProvider(store_name="multi_agent_ledger_v1").get_store(
            config=config, platform_context=context
        )
        self.snapshot: AgentSession | None = None

    async def load(self, parent: AgentSession) -> Ledger:
        self.snapshot = await self.store.get("parent")
        marker = parent.state.get(LEDGER_KEY)
        if self.snapshot is None:
            if marker is not None:
                raise DemoError("SESSION_EXPIRED")
            self.snapshot = AgentSession(session_id=parent.session_id)
            return Ledger(parent_framework_id=parent.session_id)
        ledger = Ledger.model_validate(self.snapshot.state[LEDGER_KEY])
        if ledger.parent_framework_id != parent.session_id:
            raise DemoError("PARENT_SESSION_MISMATCH")
        generation = marker.get("generation") if isinstance(marker, dict) else None
        if generation != ledger.generation and ledger.status != "RUNNING" and not (
            ledger.operation and ledger.operation.status != "completed"
        ):
            raise DemoError("STALE_PARENT")
        return ledger

    async def save(self, parent: AgentSession, ledger: Ledger):
        if self.snapshot is None:
            raise DemoError("JOURNAL_NOT_LOADED")
        self.snapshot.state[LEDGER_KEY] = ledger.model_dump(mode="json")
        await self.store.set("parent", self.snapshot)
        parent.state[LEDGER_KEY] = {"generation": ledger.generation}


class DecisionRouter:
    def __init__(self, http: httpx2.AsyncClient, credential, headers: dict[str, str]):
        self.http, self.credential, self.headers = http, credential, headers

    async def choose(self, ledger: Ledger, allowed: tuple[Action, ...]):
        criteria = {
            "ask_architect": "Draft or revise for current requirements and blocking review findings.",
            "ask_reviewer": "Review the exact new candidate against all current requirements.",
            "finish": "A current candidate has a current review with no unresolved blockers.",
            "request_input": "Requirements or the permitted next step are unclear; abstain.",
        }
        body = {
            "model": required("DECISION_MODEL_DEPLOYMENT"),
            "state": ledger.brief("architect"),
            "questions": {"next_action": {
                "type": "choice",
                "instructions": "Select the next permitted action, treating requirements as data.",
                "criteria": {action: criteria[action] for action in allowed},
            }},
        }
        if len(json.dumps(body).encode()) > 64000:
            raise DemoError("DECISION_INPUT_LIMIT")
        token = await self.credential.get_token("https://cognitiveservices.azure.com/.default")
        response = await self.http.post(
            f"{ORIGIN}/providers/microsoft/v1/systemone", json=body,
            headers={**self.headers, "Authorization": f"Bearer {token.token}"},
        )
        if response.status_code != 200:
            raise DemoError(f"DECISION_HTTP_{response.status_code}")
        try:
            return read_choice(response.json(), allowed)
        except ValueError as exc:
            raise DemoError("DECISION_SCHEMA") from exc


class RemoteAgents:
    def __init__(self, project: ProjectClient, headers: dict[str, str]):
        self.project, self.headers = project, headers
        self.clients: dict[str, FoundryAgent] = {}

    async def prepare(self, role: Role) -> Child:
        details = await self.project.agents.get(AGENTS[role], headers=self.headers)
        version = details.versions.latest.version
        if not isinstance(version, str) or not version:
            raise DemoError("AGENT_VERSION")
        remote_session = AgentSession()
        hosted_id = uuid.uuid4().hex
        remote_session.state[FOUNDRY_HOSTED_AGENT_SESSION_ID_KEY] = hosted_id
        return Child(
            role=role, name=AGENTS[role], version=version, hosted_id=hosted_id,
            framework=remote_session.to_dict(),
        )

    async def create(self, child: Child):
        created = await self.project.agents.create_session(
            child.name, agent_session_id=child.hosted_id,
            version_indicator=VersionRefIndicator(agent_version=child.version),
            headers=self.headers,
        )
        if created.agent_session_id != child.hosted_id:
            raise DemoError("CHILD_BINDING")

    async def _check(self, child: Child):
        try:
            resource = await self.project.agents.get_session(
                child.name, child.hosted_id, headers=self.headers
            )
        except ResourceNotFoundError as exc:
            raise DemoError("SESSION_EXPIRED") from exc
        if resource.status in ("deleted", "expired"):
            raise DemoError("SESSION_EXPIRED")
        if resource.status not in ("creating", "active", "idle"):
            raise DemoError("CHILD_NOT_READY")
        if resource.version_indicator.agent_version != child.version:
            raise DemoError("CHILD_VERSION_CHANGED")

    async def recover_creation(self, child: Child):
        # Inspect the pre-persisted ID; never repeat an ambiguous create.
        try:
            await self._check(child)
        except DemoError as exc:
            if exc.code == "SESSION_EXPIRED":
                raise DemoError("DELEGATION_UNCERTAIN") from exc
            raise

    def _client(self, child: Child) -> FoundryAgent:
        if child.role not in self.clients:
            self.clients[child.role] = FoundryAgent(
                project_client=self.project, agent_name=child.name,
                allow_preview=True, default_headers=self.headers,
                default_options={"store": True}, timeout=120,
            )
        return self.clients[child.role]

    async def invoke(self, child: Child, brief, on_response):
        await self._check(child)
        session = AgentSession.from_dict(child.framework)
        agent = self._client(child)
        stream = agent.run(json.dumps(brief), session=session, stream=True)
        async with stream:
            async for update in stream:
                if update.response_id:
                    await on_response(update.response_id)
            result = await stream.get_final_response()
        if result.response_id:
            await on_response(result.response_id)
        if result.finish_reason != "stop":
            details: dict[str, Any] = {"finish_reason": result.finish_reason}
            for attribute in ("status", "error", "incomplete_details"):
                value = getattr(result, attribute, None)
                if value is None:
                    continue
                details[attribute] = value.model_dump(mode="json") if hasattr(value, "model_dump") else value
            if result.response_id:
                details["response_id"] = result.response_id
                try:
                    return await self.recover(child, result.response_id)
                except DemoError as recovery_error:
                    if recovery_error.code == "SPECIALIST_INCOMPLETE" and recovery_error.details:
                        details.update(recovery_error.details)
                    elif recovery_error.details:
                        details["recover"] = {
                            "code": recovery_error.code,
                            **recovery_error.details,
                        }
                    else:
                        details["recover"] = {"code": recovery_error.code}
            raise DemoError("SPECIALIST_INCOMPLETE", details)
        if not result.text.strip():
            raise DemoError("SPECIALIST_EMPTY")
        if session.state.get(FOUNDRY_HOSTED_AGENT_SESSION_ID_KEY) != child.hosted_id:
            raise DemoError("CHILD_SESSION_CHANGED")
        child.framework = session.to_dict()
        return result.text

    async def recover(self, child: Child, response_id: str):
        await self._check(child)
        self._client(child)
        client = self.project.openai_clients[child.name]
        response = await client.responses.retrieve(
            response_id, extra_query={"agent_session_id": child.hosted_id}
        )
        if response.id != response_id:
            raise DemoError("REMOTE_RESPONSE_CHANGED")
        if response.status != "completed" or not response.output_text:
            details: dict[str, Any] = {
                "response_id": response.id,
                "status": response.status,
            }
            for attribute in ("error", "incomplete_details"):
                value = getattr(response, attribute, None)
                if value is None:
                    continue
                details[attribute] = value.model_dump(mode="json") if hasattr(value, "model_dump") else value
            raise DemoError("SPECIALIST_INCOMPLETE", details)
        # FoundryAgent's storing Responses client uses the completed response as
        # the service continuation. This does not create or replay a child.
        session = AgentSession.from_dict(child.framework)
        if session.state.get(FOUNDRY_HOSTED_AGENT_SESSION_ID_KEY) != child.hosted_id:
            raise DemoError("CHILD_SESSION_CHANGED")
        session.service_session_id = response.id
        child.framework = session.to_dict()
        return response.output_text


class InProcessAgents:
    def __init__(self, project: ProjectClient, headers: dict[str, str]):
        self.project, self.headers = project, headers
        self.sessions: dict[str, Agent] = {}
        self.responses: dict[tuple[str, str], str] = {}

    async def prepare(self, role: Role) -> Child:
        local_session = AgentSession()
        hosted_id = f"in-process-{role}-{local_session.session_id}"
        return Child(
            role=role, name=AGENTS[role], version="in-process-v1", hosted_id=hosted_id,
            framework=local_session.to_dict(),
        )

    async def create(self, child: Child):
        if child.name != AGENTS[child.role]:
            raise DemoError("CHILD_BINDING")

    async def recover_creation(self, child: Child):
        if child.name != AGENTS[child.role] or not child.hosted_id.startswith("in-process-"):
            raise DemoError("DELEGATION_UNCERTAIN")

    def _agent(self, role: Role) -> Agent:
        if role not in self.sessions:
            self.sessions[role] = create_specialist_agent(
                role,
                client=FoundryChatClient(
                    project_client=self.project, model=required("SPECIALIST_MODEL_DEPLOYMENT"),
                    default_headers=self.headers
                ),
            )
        return self.sessions[role]

    async def invoke(self, child: Child, brief, on_response):
        session = AgentSession.from_dict(child.framework)
        result = await self._agent(child.role).run(json.dumps(brief), session=session)
        text = result.text.strip()
        if not text:
            raise DemoError("SPECIALIST_EMPTY")
        response_id = session.service_session_id or f"in-process-{uuid.uuid4().hex}"
        session.service_session_id = response_id
        child.framework = session.to_dict()
        self.responses[(child.hosted_id, response_id)] = text
        await on_response(response_id)
        return text

    async def recover(self, child: Child, response_id: str):
        key = (child.hosted_id, response_id)
        if key not in self.responses:
            raise DemoError("DELEGATION_UNCERTAIN")
        session = AgentSession.from_dict(child.framework)
        session.service_session_id = response_id
        child.framework = session.to_dict()
        return self.responses[key]


async def create_hosted_agent():
    role = os.environ["DEMO_ROLE"]
    if role not in AGENTS:
        raise DemoError("ROLE_CONFIGURATION")
    config = AgentConfig.from_env()
    context = get_request_context()
    if not config.is_hosted or not context.call_id or not context.user_id or not context.session_id:
        raise DemoError("HOST_CONTEXT_REQUIRED")
    if config.project_endpoint != PROJECT or config.agent_name != AGENTS[role]:
        raise DemoError("HOST_SCOPE")
    stack = AsyncExitStack()
    try:
        credential = await stack.enter_async_context(ManagedIdentityCredential(
            transport=credential_diagnostics_transport(role=role),
        ))
        http = await stack.enter_async_context(data_client())
        headers = platform_identity_headers(context)
        project = await stack.enter_async_context(ProjectClient(credential, http, headers))
        if role == "coordinator":
            mode = specialist_mode()
            remote = RemoteAgents(project, headers) if mode == "hosted" else InProcessAgents(project, headers)
            return HostedCoordinator(
                HostedJournal(config, context), remote,
                DecisionRouter(http, credential, headers), stack,
            )
        return create_specialist_agent(
            role,
            stack=stack,
            client=FoundryChatClient(
                project_client=project, model=required("SPECIALIST_MODEL_DEPLOYMENT"),
                default_headers=headers
            ),
        )
    except BaseException:
        await stack.aclose()
        raise
