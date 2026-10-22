"""Private, bounded observations; never an identity source or an authorizer.

Consumers select route templates/stages, not URLs or exception text. Binding
UUIDs are *local observation aliases*, not user IDs, hashes or proof of a join.
The caller must associate aliases with operation/response evidence privately.
No helper reads a body, changes SDK context, or infers execution success.
"""
from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from enum import Enum
import json
import logging
import math
from uuid import UUID, uuid4


class Role(str, Enum):
    COORDINATOR = "coordinator"
    ARCHITECT = "architect"
    REVIEWER = "reviewer"


class Stage(str, Enum):
    OUTBOUND = "outbound"
    INGRESS = "ingress"
    PREPARATION = "preparation"
    REQUEST = "request"
    BACKGROUND = "background"
    EXECUTION = "execution"
    SESSION = "session"
    STORAGE = "storage"
    CREDENTIAL = "credential"


class Kind(str, Enum):
    SEND = "send"
    RESPONSE_HEADERS = "response_headers"
    ERROR = "error"
    STREAM_COMPLETE = "stream_complete"
    STREAM_CLOSED = "stream_closed"
    CANCELLED = "cancelled"
    ASGI_FINAL_BODY = "asgi_final_body"
    DISCONNECT = "disconnect"
    CONTEXT = "context"
    EXECUTION_COMPLETE = "execution_complete"
    EXECUTION_REJECTED = "execution_rejected"
    EXECUTION_FAILED = "execution_failed"


class Method(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    OTHER = "other"


class Route(str, Enum):
    # These are categories/templates, never concrete paths or resource names.
    AGENT_RESPONSES = "agents/{agent}/responses"
    RESPONSE = "responses/{response}"
    RESPONSES = "responses"
    SESSIONS = "sessions"
    SESSION = "sessions/{session}"
    MODEL = "model/responses"
    DECISION = "model/decision"
    BLOB = "blob/{container}/{blob}"
    TOKEN = "credential/token"
    OTHER = "other"


class Category(str, Enum):
    NONE = "none"
    TRANSPORT = "transport"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"
    REJECTED = "rejected"
    SDK = "sdk"
    APPLICATION = "application"
    UNKNOWN = "unknown"


class Coverage(str, Enum):
    OBSERVED = "observed"
    UNAVAILABLE = "unavailable"
    NOT_REACHED = "not reached"


class Presence(str, Enum):
    ABSENT = "absent"
    EMPTY = "empty"
    NONEMPTY = "nonempty"
    MALFORMED_DUPLICATE = "malformed/duplicate"


class Match(str, Enum):
    TRUE = "true"
    FALSE = "false"
    NOT_COMPARABLE = "not-comparable"


@dataclass(frozen=True)
class Observation:
    coverage: Coverage
    presence: Presence | None = None


def _valid_value(value: object) -> bool:
    # Exact builtins only: no user-defined __str__, equality, decode or repr.
    if type(value) is str:
        return len(value) <= 8192 and all(32 <= ord(c) <= 126 for c in value)
    if type(value) is bytes:
        return len(value) <= 8192 and all(32 <= c <= 126 for c in value)
    return False


def observe_value(value: object) -> Observation:
    """None is absent, not unavailable. Whitespace is nonempty, not trimmed."""
    if value is None:
        state = Presence.ABSENT
    elif not _valid_value(value):
        state = Presence.MALFORMED_DUPLICATE
    else:
        state = Presence.EMPTY if len(value) == 0 else Presence.NONEMPTY
    return Observation(Coverage.OBSERVED, state)


def unobserved(coverage: Coverage = Coverage.UNAVAILABLE) -> Observation:
    if type(coverage) is not Coverage or coverage is Coverage.OBSERVED:
        raise ValueError("INVALID_DIAGNOSTIC_COVERAGE")
    return Observation(coverage)


_HEADER_NAMES = {
    "delegation": b"x-ms-user-identity",
    "platform": b"x-agent-user-id",
    "call": b"x-agent-foundry-call-id",
}
_HEADER_TOKEN = frozenset(b"!#$%&'*+-.^_`|~0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")


def observe_header(headers: object, slot: str) -> Observation:
    """Inspect raw ASGI/httpx multi-items without merging duplicate values.

    Input is a materialized list/tuple of pairs (bytes or ASCII strings).
    Unknown/malformed structure is unavailable, not an absent identity.
    No arbitrary iterable or SDK object is traversed. Values never survive.
    """
    if type(slot) is not str or slot not in _HEADER_NAMES:
        return unobserved()
    if type(headers) not in (list, tuple) or len(headers) > 512:
        return unobserved()
    found = []
    for item in headers:
        if type(item) not in (tuple, list) or len(item) != 2:
            return unobserved()
        name, value = item
        if type(name) is str:
            if not name.isascii():
                return unobserved()
            name = name.encode("ascii")
        if (type(name) is not bytes or not name or len(name) > 256
                or any(char not in _HEADER_TOKEN for char in name)):
            return unobserved()
        if name.lower() == _HEADER_NAMES[slot]:
            found.append(value)
    if len(found) > 1:
        return Observation(Coverage.OBSERVED, Presence.MALFORMED_DUPLICATE)
    if not found:
        return observe_value(None)
    # A present header with a non-string value (including None) is malformed.
    if type(found[0]) not in (str, bytes):
        return Observation(Coverage.OBSERVED, Presence.MALFORMED_DUPLICATE)
    return observe_value(found[0])


def compare_values(left: object, right: object, *, same_representation: bool = False) -> Match:
    """Compare only explicitly comparable nonempty exact builtin values.

    Callers must not opt in for public delegation vs platform-delivered IDs.
    Absence, empty values, malformed values and bytes-vs-str are not matches.
    Neither operand is retained or hashed.
    """
    if (same_representation is not True or type(left) is not type(right)
            or not _valid_value(left) or not _valid_value(right) or not left or not right):
        return Match.NOT_COMPARABLE
    return Match.TRUE if left == right else Match.FALSE


@dataclass(frozen=True)
class Binding:
    observation: UUID
    operation: UUID | None = None
    response: UUID | None = None


_binding: ContextVar[Binding | None] = ContextVar("diagnostic_binding", default=None)


def new_binding(*, operation: UUID | None = None, response: UUID | None = None) -> Binding:
    """Supply only local aliases, never UUID-shaped identities or trace headers."""
    if any(value is not None and type(value) is not UUID for value in (operation, response)):
        raise ValueError("INVALID_DIAGNOSTIC_BINDING")
    return Binding(uuid4(), operation, response)


def current_binding() -> Binding | None:
    return _binding.get()


@contextmanager
def bind(binding: Binding):
    """Reset even after failure; inherited background copies remain immutable."""
    _binding_fields(binding)
    token = _binding.set(binding)
    try:
        yield binding
    finally:
        _binding.reset(token)


@dataclass(frozen=True)
class Event:
    role: Role
    stage: Stage
    kind: Kind
    method: Method = Method.OTHER
    route: Route = Route.OTHER
    category: Category = Category.NONE
    status: int | None = None
    duration_ms: float | None = None
    binding: Binding | None = None
    delegation: Observation | None = None
    platform: Observation | None = None
    call: Observation | None = None
    scope_user: Observation | None = None
    request_user: Observation | None = None
    scope_request_match: Match = Match.NOT_COMPARABLE


def _binding_fields(binding: Binding) -> dict:
    if type(binding) is not Binding or type(binding.observation) is not UUID:
        raise ValueError("INVALID_DIAGNOSTIC_BINDING")
    result = {"observation": str(binding.observation)}
    for name in ("operation", "response"):
        value = getattr(binding, name)
        if value is not None:
            if type(value) is not UUID:
                raise ValueError("INVALID_DIAGNOSTIC_BINDING")
            result[name] = str(value)
    return result


def _observation_fields(value: Observation) -> dict:
    if type(value) is not Observation or type(value.coverage) is not Coverage:
        raise ValueError("INVALID_DIAGNOSTIC_OBSERVATION")
    if value.coverage is Coverage.OBSERVED:
        if type(value.presence) is not Presence:
            raise ValueError("INVALID_DIAGNOSTIC_PRESENCE")
        return {"coverage": value.coverage.value, "presence": value.presence.value}
    if value.presence is not None:
        raise ValueError("INVALID_DIAGNOSTIC_PRESENCE")
    return {"coverage": value.coverage.value}


def event_fields(event: Event) -> dict:
    """Project an exact closed schema; reject runtime type-hint violations.

    Consumers should call emit(), which contains validation/logger failures.
    This strict projection is exposed for deterministic synthetic fixtures.
    Omitted slots mean no checkpoint supplied, never 'absent'.
    """
    if type(event) is not Event:
        raise ValueError("INVALID_DIAGNOSTIC_EVENT")
    result = {"schema_version": 1}
    for name, cls in (("role", Role), ("stage", Stage), ("kind", Kind),
                      ("method", Method), ("route", Route), ("category", Category),
                      ("scope_request_match", Match)):
        value = getattr(event, name)
        if type(value) is not cls:
            raise ValueError("INVALID_DIAGNOSTIC_FIELD")
        result[name] = value.value
    if event.status is not None:
        if type(event.status) is not int or not 100 <= event.status <= 599:
            raise ValueError("INVALID_DIAGNOSTIC_STATUS")
        result["status"] = event.status
    if event.duration_ms is not None:
        if (type(event.duration_ms) not in (float, int)
                or not math.isfinite(event.duration_ms)
                or not 0 <= event.duration_ms <= 86_400_000):
            raise ValueError("INVALID_DIAGNOSTIC_DURATION")
        result["duration_ms"] = round(event.duration_ms, 3)
    binding = event.binding if event.binding is not None else current_binding()
    if binding is not None:
        result["binding"] = _binding_fields(binding)
    for name in ("delegation", "platform", "call", "scope_user", "request_user"):
        value = getattr(event, name)
        if value is not None:
            result[name] = _observation_fields(value)
    return result


# A dedicated non-propagating stderr sink avoids root/machine-stdout handlers.
# It is intentionally not an SDK logger and never logs a caught exception.
class _PrivateHandler(logging.StreamHandler):
    def handleError(self, record):
        # StreamHandler otherwise prints a traceback (including sink exception
        # text) when logging.raiseExceptions is true. Never fall back to that.
        pass


_logger = logging.getLogger(__name__ + ".private")
_logger.propagate = False
_logger.setLevel(logging.INFO)
if not _logger.handlers:
    _handler = _PrivateHandler()
    _handler.setFormatter(logging.Formatter("%(message)s"))
    _logger.addHandler(_handler)


def emit(event: Event) -> bool:
    """Best-effort private JSON event. Failure never replaces caller rejection.

    True means validation and the logging call returned, not durable delivery.
    A failed stderr sink is silently dropped, never retried or sent elsewhere.
    """
    try:
        payload = json.dumps(event_fields(event), separators=(",", ":"), allow_nan=False)
        if len(payload) > 4096:
            return False
        _logger.info(payload)
        return True
    except Exception:
        return False
