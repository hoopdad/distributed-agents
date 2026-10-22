"""Optional PRIVATE dispatch-to-transport receipts, not authorization or a ledger.

Install ``private_sink(callable)`` in the owning execution context (before
background task creation), then let trusted source dispatches bind operations.
The callable must synchronously retain immutable Receipt objects in private
storage; this module has no logger, file writer, credentials or remote exporter.
Missing window closure, zero requests, sink failure or unfinished streams means
incomplete evidence. A receipt/HTTP status never establishes execution success.

Only application-owned Project, Responses and stop transports are covered.
No bodies, queries, headers, identity values/hashes or exception messages are
examined. In particular, consumed specialist/model history is NOT observable:
pending history and previous_response_id do not prove consumed input. Platform,
SDK-internal clients, terminal parent creation/send and pre-install traffic are
uncovered. No aggregate schema or validation requirement is changed.
"""
from __future__ import annotations

import asyncio
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Callable, Literal
from urllib.parse import quote, urlsplit
from uuid import uuid4

import httpx2
from azure.core.pipeline.transport import AsyncHttpTransport

from .contracts import AGENTS, PROJECT


@dataclass(frozen=True)
class Binding:
    """Trusted source association; values confer no permissions."""

    operation: str
    role: str
    target: str
    version: str
    action: Literal["create", "send", "stop"]


@dataclass(frozen=True)
class Receipt:
    binding: Binding
    occurrence: str | None
    transport: str
    phase: str
    status: int | None = None
    category: str | None = None


_sink: ContextVar[Callable[[Receipt], None] | None] = ContextVar("private_effect_sink", default=None)
_dispatch: ContextVar[CaptureWindow | None] = ContextVar("private_effect_dispatch", default=None)


@contextmanager
def private_sink(sink: Callable[[Receipt], None]):
    """Not a diagnostic logger. Caller owns private durability and completeness."""
    token = _sink.set(sink)
    try:
        yield
    finally:
        _sink.reset(token)


class CaptureWindow:
    def __init__(self, binding, sink):
        self.binding, self.sink = binding, sink
        self.active = True
        self.requests = 0
        self.pending = 0
        self.sink_failed = False
        self.truncated = False

    @property
    def capture_complete(self):
        # This is capture coverage only, never an effect/turn success assertion.
        return (not self.active and self.requests > 0 and self.pending == 0
                and not self.sink_failed and not self.truncated)

    def emit(self, occurrence, transport, phase, status=None, category=None):
        try:
            self.sink(Receipt(self.binding, occurrence, transport, phase, status, category))
        except Exception:
            self.sink_failed = True

    def matches(self, method, url, transport):
        if not self.active or method != "POST":
            return False
        base, actual = urlsplit(PROJECT), urlsplit(str(url))
        if actual.scheme != "https" or actual.netloc != base.netloc:
            return False
        agent = quote(AGENTS[self.binding.role], safe="")
        path = base.path + f"/agents/{agent}/endpoint/"
        if self.binding.action == "create":
            return transport == "project" and actual.path == path + "sessions"
        if self.binding.action == "send":
            return transport == "responses" and actual.path == path + "protocols/openai/responses"
        return (transport == "responses" and actual.path ==
                path + "sessions/" + quote(self.binding.target, safe="") + ":stop")


@contextmanager
def dispatch(binding: Binding):
    """Call only after existing trusted binding/write-ahead gates.

    Creation has no wire operation field: this source-owned context associates
    it without reading its body. ContextVar inheritance covers awaited SDK and
    background tasks. A task outliving this window cannot acquire a new binding;
    an already-started occurrence retains its original window.
    """
    sink = _sink.get()
    window = CaptureWindow(binding, sink) if sink is not None else None
    token = _dispatch.set(window)
    if window:
        window.emit(None, "dispatch", "window_open")
    try:
        yield window
    finally:
        if window:
            window.active = False
            # A late response cannot retrospectively certify a closed window.
            if window.pending:
                window.truncated = True
            window.emit(None, "dispatch", "window_closed",
                        category=None if window.capture_complete else "incomplete")
        _dispatch.reset(token)


def _category(exc):
    if isinstance(exc, asyncio.CancelledError):
        return "cancelled"
    if isinstance(exc, (TimeoutError, httpx2.TimeoutException)):
        return "timeout"
    return "transport"


class Attempt:
    def __init__(self, window, transport):
        self.window, self.transport = window, transport
        self.id = uuid4().hex
        self.terminal = False
        window.requests += 1
        window.pending += 1
        self.emit("request")

    def emit(self, phase, status=None, category=None):
        self.window.emit(self.id, self.transport, phase, status, category)

    def finish(self, phase, status=None, category=None):
        if not self.terminal:
            self.terminal = True
            self.window.pending -= 1
            if phase == "stream_closed":
                self.window.truncated = True
            self.emit(phase, status, category)


def request_attempt(method, url, transport):
    window = _dispatch.get()
    # Observation failure must not change the original dispatch/rejection.
    try:
        return Attempt(window, transport) if window and window.matches(method, url, transport) else None
    except Exception:
        if window:
            window.sink_failed = True
        return None


class ProjectTransport(AsyncHttpTransport):
    """Public Azure Core transport composition; never applied to credentials."""

    def __init__(self, inner):
        self.inner = inner

    @property
    def connection_config(self):
        return self.inner.connection_config

    async def open(self):
        return await self.inner.open()

    async def close(self):
        return await self.inner.close()

    async def __aenter__(self):
        await self.inner.__aenter__()
        return self

    async def __aexit__(self, *args):
        return await self.inner.__aexit__(*args)

    async def sleep(self, duration):
        return await self.inner.sleep(duration)

    async def send(self, request, **kwargs):
        attempt = request_attempt(request.method, request.url, "project")
        try:
            response = await self.inner.send(request, **kwargs)
        except BaseException as exc:
            if attempt:
                attempt.finish("error", category=_category(exc))
            raise
        if attempt:
            attempt.finish("headers", status=response.status_code)
        return response


class ResponseStream(httpx2.AsyncByteStream):
    """Pass-through bytes, cancellation and consumer-owned close, no read-ahead."""

    def __init__(self, inner, attempt, status):
        self.inner, self.attempt, self.status = inner, attempt, status
        self.closed = False

    async def __aiter__(self):
        try:
            async for chunk in self.inner:
                yield chunk
        except BaseException as exc:
            self.attempt.finish(
                "stream_closed" if isinstance(exc, GeneratorExit) else "error",
                self.status, None if isinstance(exc, GeneratorExit) else _category(exc),
            )
            raise
        else:
            self.attempt.finish("stream_complete", self.status)

    async def aclose(self):
        if self.closed:
            return
        self.closed = True
        try:
            await self.inner.aclose()
        except BaseException as exc:
            if self.attempt.terminal:
                self.attempt.window.truncated = True
                self.attempt.emit("close_error", self.status, _category(exc))
            else:
                self.attempt.finish("error", self.status, _category(exc))
            raise
        else:
            self.attempt.finish("stream_closed", self.status)
