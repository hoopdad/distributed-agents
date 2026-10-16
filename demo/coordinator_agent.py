from __future__ import annotations

import asyncio
import json
import time
import uuid
from collections.abc import AsyncIterator, Awaitable, Callable
from typing import Any, Protocol

from agent_framework import (
    AgentResponse,
    AgentResponseUpdate,
    AgentSession,
    Content,
    Message,
    ResponseStream,
)
from pydantic import ValidationError

from .contracts import (
    AGENTS,
    LEDGER_KEY,
    Action,
    Candidate,
    Child,
    DemoError,
    Ledger,
    Operation,
    Review,
    Role,
    alias,
)

MAX_CANDIDATE_DESIGN_CHARS = 12000
MAX_REVIEW_RECOMMENDATION_CHARS = 2000


class Journal(Protocol):
    async def load(self, parent: AgentSession) -> Ledger: ...
    async def save(self, parent: AgentSession, ledger: Ledger) -> None: ...


class Remote(Protocol):
    async def prepare(self, role: Role) -> Child: ...
    async def create(self, child: Child) -> None: ...
    async def recover_creation(self, child: Child) -> None: ...
    async def invoke(
        self,
        child: Child,
        brief: dict[str, Any],
        on_response: Callable[[str], Awaitable[None]],
    ) -> str: ...
    async def recover(self, child: Child, response_id: str) -> str: ...


class Router(Protocol):
    async def choose(self, ledger: Ledger, allowed: tuple[Action, ...]) -> tuple[Action, float]: ...


class Coordinator:
    id = AGENTS["coordinator"]
    name = AGENTS["coordinator"]
    description = "Decision-only, bounded durable remote specialist delegation."

    def __init__(self, journal: Journal, remote: Remote, router: Router):
        self.journal = journal
        self.remote = remote
        self.router = router

    def run(self, messages=None, *, stream=False, session=None, **kwargs):
        """Framework entry point: resolve the parent session and start its response stream."""
        parent = session if session is not None else self.create_session()
        updates = self._stream(messages, parent)
        if stream:
            return ResponseStream(updates, finalizer=AgentResponse.from_updates)
        return self._complete(updates)

    @staticmethod
    async def _complete(updates: AsyncIterator[AgentResponseUpdate]) -> AgentResponse:
        return AgentResponse.from_updates([update async for update in updates])

    def create_session(self, *, session_id: str | None = None) -> AgentSession:
        return AgentSession(session_id=session_id)

    def get_session(self, service_session_id: str, *, session_id: str | None = None) -> AgentSession:
        return AgentSession(session_id=session_id, service_session_id=service_session_id)

    async def _save(self, parent: AgentSession, ledger: Ledger) -> None:
        ledger.generation += 1
        await self.journal.save(parent, ledger)

    @staticmethod
    def _normalize_candidate_payload(payload: Any) -> Any:
        if not isinstance(payload, dict):
            return payload
        design = payload.get("design")
        if isinstance(design, str) and len(design) > MAX_CANDIDATE_DESIGN_CHARS:
            return {**payload, "design": design[:MAX_CANDIDATE_DESIGN_CHARS]}
        return payload

    @staticmethod
    def _normalize_review_payload(payload: Any) -> Any:
        if not isinstance(payload, dict):
            return payload
        normalized = dict(payload)
        recommendation = normalized.get("recommendation")
        if isinstance(recommendation, str) and len(recommendation) > MAX_REVIEW_RECOMMENDATION_CHARS:
            normalized["recommendation"] = recommendation[:MAX_REVIEW_RECOMMENDATION_CHARS]
        for key in ("blocking_findings", "unresolved_requirements"):
            values = normalized.get(key)
            if isinstance(values, list) and len(values) > 20:
                normalized[key] = values[:20]
        return normalized

    @staticmethod
    def _parse_specialist_json(text: str, validate: Callable[[str], Any]):
        stripped = text.strip()
        attempts = [stripped]
        if stripped.startswith("```"):
            lines = stripped.splitlines()
            if len(lines) >= 3 and lines[-1].strip() == "```":
                attempts.append("\n".join(lines[1:-1]).strip())
        start, end = stripped.find("{"), stripped.rfind("}")
        if start >= 0 and end > start:
            attempts.append(stripped[start:end + 1].strip())
        seen: set[str] = set()
        final_error: Exception | None = None
        for payload in attempts:
            if not payload or payload in seen:
                continue
            seen.add(payload)
            try:
                return validate(payload)
            except Exception as exc:
                final_error = exc
        if final_error is not None:
            raise final_error
        raise DemoError("SPECIALIST_EMPTY")

    def _apply(self, ledger: Ledger, role: Role, text: str) -> None:
        try:
            if role == "architect":
                payload = self._parse_specialist_json(text, json.loads)
                candidate = Candidate.model_validate(self._normalize_candidate_payload(payload))
                if (
                    candidate.requirements_revision != ledger.turn
                    or candidate.candidate_revision != ledger.candidate_revision + 1
                ):
                    raise DemoError("SPECIALIST_REVISION")
                ledger.candidate = candidate
                ledger.candidate_revision = candidate.candidate_revision
                ledger.review = None
                ledger.rounds += 1
            else:
                payload = self._normalize_review_payload(
                    self._parse_specialist_json(text, json.loads)
                )
                if (
                    isinstance(payload, dict)
                    and payload.get("approved") is True
                    and (payload.get("blocking_findings") or payload.get("unresolved_requirements"))
                ):
                    payload = {**payload, "approved": False}
                review = Review.model_validate(payload)
                if (
                    review.requirements_revision != ledger.turn
                    or review.candidate_revision != ledger.candidate_revision
                ):
                    raise DemoError("SPECIALIST_REVISION")
                ledger.review = review
        except (ValidationError, ValueError, TypeError) as exc:
            raise DemoError("SPECIALIST_SCHEMA", {
                "role": role,
                "validation": str(exc),
                "snippet": text[:500],
            }) from exc

    async def _recover(self, parent: AgentSession, ledger: Ledger) -> bool:
        operation = ledger.operation
        if operation is None or operation.status == "completed":
            return ledger.status == "RUNNING"
        child = ledger.children[operation.role]
        if operation.kind == "create":
            await self.remote.recover_creation(child)
            child.bound = True
        elif operation.response_id:
            text = await self.remote.recover(child, operation.response_id)
            self._apply(ledger, operation.role, text)
        else:
            raise DemoError("DELEGATION_UNCERTAIN")
        operation.status = "completed"
        ledger.status = "RECOVERED"
        await self._save(parent, ledger)
        return True

    async def _call(self, parent: AgentSession, ledger: Ledger, role: Role) -> dict[str, Any]:
        if role not in ledger.children:
            child = await self.remote.prepare(role)
            if child.name != AGENTS[role] or child.role != role:
                raise DemoError("CHILD_BINDING")
            ledger.children[role] = child
            ledger.operation = Operation(id=uuid.uuid4().hex, role=role, kind="create")
            await self._save(parent, ledger)
            await self.remote.create(child)
            child.bound = True
            ledger.operation.status = "completed"
            await self._save(parent, ledger)
        child = ledger.children[role]
        if not child.bound:
            raise DemoError("DELEGATION_UNCERTAIN")
        ledger.calls += 1
        ledger.operation = Operation(id=uuid.uuid4().hex, role=role, kind="call")
        await self._save(parent, ledger)

        async def remember(response_id: str):
            if ledger.operation.response_id not in (None, response_id):
                raise DemoError("REMOTE_RESPONSE_CHANGED")
            if ledger.operation.response_id is None:
                ledger.operation.response_id = response_id
                await self._save(parent, ledger)

        start = time.monotonic()
        text = await self.remote.invoke(child, ledger.brief(role), remember)
        self._apply(ledger, role, text)
        ledger.operation.status = "completed"
        await self._save(parent, ledger)
        return {
            "event": "delegation",
            "role": role,
            "action": f"ask_{role}",
            "round": ledger.rounds,
            "candidate_revision": ledger.candidate_revision,
            "specialist_mode": (
                "in_process"
                if child.version.startswith("in-process-") or child.hosted_id.startswith("in-process-")
                else "hosted"
            ),
            "hosted_session": alias(child.hosted_id),
            "framework_session": alias(child.framework["session_id"]),
            "response": alias(ledger.operation.response_id),
            "duration_ms": round((time.monotonic() - start) * 1000),
            "status": "completed",
        }

    async def _stream(self, messages, parent: AgentSession) -> AsyncIterator[AgentResponseUpdate]:
        text = self._input_text(messages)
        ledger = await self.journal.load(parent)
        error = None
        try:
            async with asyncio.timeout(360):
                async for update in self._run_turn(parent, ledger, text):
                    yield update
        except (DemoError, TimeoutError) as exc:
            error = self._record_turn_error(ledger, exc)
        # Unexpected SDK/storage errors propagate; no successful-looking fallback.
        await self._save(parent, ledger)
        yield self._result_update(ledger, error)

    @staticmethod
    def _input_text(messages) -> str:
        if isinstance(messages, str):
            text = messages
        elif isinstance(messages, Message):
            text = messages.text
        elif isinstance(messages, list) and all(isinstance(item, Message) for item in messages):
            text = "\n".join(item.text for item in messages if item.role == "user")
        else:
            raise DemoError("INPUT_SCHEMA")
        if not text.strip() or len(text) > 4000:
            raise DemoError("INPUT_LIMIT")
        return text

    async def _run_turn(
        self, parent: AgentSession, ledger: Ledger, text: str
    ) -> AsyncIterator[AgentResponseUpdate]:
        if await self._recover(parent, ledger):
            # Reconciliation is a turn of its own, not permission to dispatch more work.
            ledger.status = "RECOVERED"
            return
        await self._start_turn(parent, ledger, text)
        async for update in self._run_decision_loop(parent, ledger):
            yield update

    async def _start_turn(self, parent: AgentSession, ledger: Ledger, text: str) -> None:
        if (
            len(ledger.requirements) >= 50
            or sum(len(item) for item in ledger.requirements) + len(text) > 24000
        ):
            raise DemoError("CONVERSATION_LIMIT")
        ledger.turn += 1
        ledger.requirements.append(text)
        ledger.calls = ledger.rounds = ledger.decisions = 0
        ledger.status = "RUNNING"
        await self._save(parent, ledger)

    async def _run_decision_loop(
        self, parent: AgentSession, ledger: Ledger
    ) -> AsyncIterator[AgentResponseUpdate]:
        while ledger.status == "RUNNING":
            decision = await self._choose_action(parent, ledger)
            if decision is None:
                break
            action, confidence = decision
            yield self._update({
                "event": "decision",
                "action": action,
                "confidence": confidence,
                "turn": ledger.turn,
            })
            if self._finish_for_decision(ledger, action, confidence):
                break
            role: Role = "architect" if action == "ask_architect" else "reviewer"
            event = await self._call(parent, ledger, role)
            event["confidence"] = confidence
            yield self._update(event)

    async def _choose_action(
        self, parent: AgentSession, ledger: Ledger
    ) -> tuple[Action, float] | None:
        if ledger.decisions >= 10:
            ledger.status = "LIMIT_REACHED"
            return None
        allowed = ledger.allowed()
        ledger.decisions += 1
        await self._save(parent, ledger)
        action, confidence = await self.router.choose(ledger, allowed)
        if action not in allowed or not 0 <= confidence <= 1:
            raise DemoError("DECISION_SCHEMA")
        return action, confidence

    @staticmethod
    def _finish_for_decision(ledger: Ledger, action: Action, confidence: float) -> bool:
        if confidence < 0.8 or action == "request_input":
            ledger.status = "REQUEST_INPUT"
            return True
        if action == "finish":
            ledger.status = "ACCEPTED_ADVISORY"
            return True
        if ledger.calls >= 6 or (action == "ask_architect" and ledger.rounds >= 3):
            ledger.status = "LIMIT_REACHED"
            return True
        return False

    @staticmethod
    def _record_turn_error(ledger: Ledger, exc: DemoError | TimeoutError) -> Any:
        ledger.status = exc.code if isinstance(exc, DemoError) else "TURN_TIMEOUT"
        error = exc.details if isinstance(exc, DemoError) else None
        if ledger.operation and ledger.operation.status != "completed":
            ledger.operation.status = "uncertain"
            if ledger.operation.response_id is None and ledger.status not in (
                "SESSION_EXPIRED", "CHILD_NOT_READY", "CHILD_VERSION_CHANGED",
            ):
                ledger.status = "DELEGATION_UNCERTAIN"
        return error

    @staticmethod
    def _result_update(ledger: Ledger, error: Any) -> AgentResponseUpdate:
        return Coordinator._update({
            "event": "result",
            "status": ledger.status,
            "turn": ledger.turn,
            "calls": ledger.calls,
            "decisions": ledger.decisions,
            "candidate": ledger.candidate.model_dump() if ledger.candidate else None,
            "review": ledger.review.model_dump() if ledger.review else None,
            "clarification": (
                "Please clarify the requirements or routing uncertainty."
                if ledger.status == "REQUEST_INPUT" else None
            ),
            "error": error,
        }, final=True)

    @staticmethod
    def _update(payload: dict[str, Any], *, final: bool = False) -> AgentResponseUpdate:
        return AgentResponseUpdate(
            role="assistant",
            contents=[Content.from_text(json.dumps(payload, allow_nan=False) + "\n")],
            finish_reason="stop" if final else None,
        )


class HostedCoordinator(Coordinator):
    def __init__(self, journal, remote, router, stack):
        super().__init__(journal, remote, router)
        self.stack = stack

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.stack.aclose()
