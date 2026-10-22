"""Opt-in PRIVATE local retention of the existing effect-observation contract.

The owning caller opens a NEW exclusive binary regular file (e.g. ``x+b``),
protects its permissions, supplies trusted expected bindings and installs this
callable with ``private_sink`` BEFORE creating background tasks. This module
opens no path, owns no handle/client, logs nothing and activates no host hook.
No arbitrary objects, headers, bodies or identities are serialized.

After ALL inherited tasks/transports have quiesced, retain ``checkpoint``'s
length/digest/binding anchor independently, then ``readback``/``reconcile``.
Quiescence and exclusive ownership are caller attestations, not established by
fsync or window_closed. Keep the handle and raw partial bytes even on failure.
Late writes invalidate previous anchors; unhealthy capture never recovers.
Local fsync is not remote durability, history completeness or turn success.
Results and anchors are private and intentionally have opaque reprs.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import os
import re
import stat
from dataclasses import dataclass
from threading import RLock

from .artifacts import Effect, Manifest, ScopeBinding, decode_document
from .effect_observation import Binding, Receipt

# Storage bounds only, not workflow/attempt/time budgets.
MAX_RECORDS = 4096
MAX_LINE = 4096
MAX_BYTES = 4 * 1024 * 1024
ZERO = "0" * 64
PHASES = {
    "window_open", "window_closed", "request_late", "request", "headers",
    "stream_complete", "stream_closed", "error", "close_error",
}


class CaptureError(ValueError):
    """Only constant codes escape; never include private inputs/OS exceptions."""


def _require(condition, code):
    if not condition:
        raise CaptureError(code)


def _text(value):
    return (type(value) is str and 0 < len(value) <= 512
            and all(32 <= ord(c) < 127 for c in value))


def _binding(value):
    _require(type(value) is Binding, "CAPTURE_BINDING")
    _require(all(_text(v) for v in (value.operation, value.target, value.version))
             and value.role in ("coordinator", "architect", "reviewer")
             and value.action in ("create", "send", "stop"), "CAPTURE_BINDING")
    _require((value.role == "coordinator") == (value.action == "stop"), "CAPTURE_BINDING")
    return [value.operation, value.role, value.target, value.version, value.action]


def _encode(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def _digest(raw):
    return hashlib.sha256(raw).hexdigest()


def _expected(bindings):
    try:
        values = tuple(bindings)
        _require(0 < len(values) <= MAX_RECORDS, "CAPTURE_BINDING")
        rows = [_binding(b) for b in values]
        _require(len({b.operation for b in values}) == len(values), "CAPTURE_BINDING")
        return values, _digest(_encode(sorted(rows)))
    except Exception:
        raise CaptureError("CAPTURE_BINDING") from None


def _receipt(r, expected):
    _require(type(r) is Receipt and r.binding in expected, "CAPTURE_RECEIPT")
    _binding(r.binding)
    _require(r.phase in PHASES, "CAPTURE_PHASE")
    window = r.phase in ("window_open", "window_closed")
    _require((window and r.transport == "dispatch" and r.occurrence is None)
             or (not window and r.transport == (
                 "project" if r.binding.action == "create" else "responses")
                 and type(r.occurrence) is str
                 and re.fullmatch("[a-f0-9]{32}", r.occurrence) is not None),
             "CAPTURE_ASSOCIATION")
    _require(r.status is None or (type(r.status) is int and 100 <= r.status <= 599),
             "CAPTURE_STATUS")
    if r.phase in ("headers", "stream_complete", "stream_closed", "close_error"):
        _require(r.status is not None, "CAPTURE_STATUS")
    elif r.phase != "error":
        _require(r.status is None, "CAPTURE_STATUS")
    categories = {
        "window_closed": (None, "incomplete"), "request_late": ("incomplete",),
        "error": ("cancelled", "timeout", "transport"),
        "close_error": ("cancelled", "timeout", "transport"),
    }
    _require(r.category in categories.get(r.phase, (None,)), "CAPTURE_CATEGORY")
    return {
        "binding": _binding(r.binding), "occurrence": r.occurrence,
        "transport": r.transport, "phase": r.phase, "status": r.status, "category": r.category,
    }


@dataclass(frozen=True, repr=False)
class CaptureAnchor:
    length: int
    sha256: str
    records: int
    bindings_sha256: str
    quiescence_receipt: str


@dataclass(frozen=True, repr=False)
class CaptureReadback:
    complete: bool
    issues: tuple[str, ...]
    raw: bytes
    receipts: tuple[Receipt, ...]


@dataclass(frozen=True, repr=False)
class OperationAnchor:
    """Separately retained scoped operation name/digest, NOT derived from sink."""
    binding: Binding
    name: str
    sha256: str


@dataclass(frozen=True, repr=False)
class StopAnchor:
    """Independent retained stop-intent binding plus attributed state readback.

    This attests the caller reconciled the once-only durable intent. Only an
    actual retained HTTP 204 occurrence AND stopped/idle state can join it.
    """
    binding: Binding
    state: str


@dataclass(frozen=True, repr=False)
class Accounting:
    complete: bool
    issues: tuple[str, ...]
    capture: CaptureReadback
    creations: tuple[str, ...] = ()
    sends: tuple[str, ...] = ()
    stops: tuple[str, ...] = ()


def _coverage(receipts, expected):
    """Strict per-window/occurrence state machine; never deduplicate attempts."""
    windows, occurrences, issues = {}, {}, []
    for r in receipts:
        b, phase, key = r.binding, r.phase, r.occurrence
        if phase == "window_open":
            _require(b not in windows, "CAPTURE_WINDOW")
            windows[b] = [False, 0]
            continue
        _require(b in windows, "CAPTURE_WINDOW")
        closed = windows[b][0]
        if phase == "window_closed":
            _require(not closed, "CAPTURE_WINDOW")
            windows[b][0] = True
            if r.category or any(
                value[0] == b and value[1] not in (
                    ("headers",) if b.action == "create" else ("stream_complete",)
                ) for value in occurrences.values()
            ):
                issues.append("CAPTURE_INCOMPLETE")
            continue
        if phase == "request_late":
            _require(closed and key not in occurrences, "CAPTURE_ORDER")
            occurrences[key] = [b, "late", None]
            issues.append("CAPTURE_LATE")
        elif phase == "request":
            if key in occurrences:
                _require(occurrences[key][:2] == [b, "late"], "CAPTURE_ORDER")
            else:
                _require(not closed, "CAPTURE_ORDER")
            occurrences[key] = [b, "request", None]
            windows[b][1] += 1
        else:
            _require(key in occurrences and occurrences[key][0] == b, "CAPTURE_ORDER")
            previous = occurrences[key][1]
            if closed:
                issues.append("CAPTURE_AFTER_CLOSE")
            if phase == "headers":
                _require(previous == "request", "CAPTURE_ORDER")
            elif phase in ("stream_complete", "stream_closed"):
                _require(r.transport == "responses" and previous == "headers", "CAPTURE_ORDER")
                _require(r.status == occurrences[key][2], "CAPTURE_STATUS")
            elif phase == "error":
                _require(previous in ("request", "headers"), "CAPTURE_ORDER")
                _require(r.status == occurrences[key][2], "CAPTURE_STATUS")
            elif phase == "close_error":
                _require(previous in ("stream_complete", "stream_closed", "error"), "CAPTURE_ORDER")
                _require(r.status == occurrences[key][2], "CAPTURE_STATUS")
            occurrences[key][1:] = [phase, r.status]
            if phase in ("error", "close_error", "stream_closed"):
                issues.append("CAPTURE_EFFECT_INCOMPLETE")
    if set(windows) != set(expected) or any(not v[0] or v[1] != 1 for v in windows.values()):
        issues.append("CAPTURE_WINDOW_INCOMPLETE")
    for b, phase, status in occurrences.values():
        if (phase != ("headers" if b.action == "create" else "stream_complete")
                or status not in ((200, 201) if b.action == "create" else
                                  (204,) if b.action == "stop" else (200,))):
            issues.append("CAPTURE_EFFECT_INCOMPLETE")
    if len(occurrences) != len(expected):
        issues.append("CAPTURE_OCCURRENCE_COUNT")
    return tuple(dict.fromkeys(issues))


class PrivateEffectCapture:
    """Synchronous callback. Caller owns file lifetime, exclusivity and privacy."""

    def __init__(self, handle, *, expected, new_exclusive=False):
        self._lock = RLock()
        self._handle = handle
        self._healthy = True
        self._raw = b""
        self._records = 0
        self._previous = ZERO
        self.expected, self._bindings = _expected(expected)
        try:
            _require(new_exclusive is True and handle.readable() and handle.writable()
                     and handle.seekable() and "b" in handle.mode, "CAPTURE_HANDLE")
            info = os.fstat(handle.fileno())
            _require(stat.S_ISREG(info.st_mode) and info.st_size == 0
                     and handle.tell() == 0, "CAPTURE_HANDLE")
        except Exception:
            raise CaptureError("CAPTURE_HANDLE") from None

    def __repr__(self):
        return "<PrivateEffectCapture>"

    def _read(self):
        self._handle.flush()
        self._handle.seek(0)
        value = self._handle.read(MAX_BYTES + 1)
        _require(type(value) is bytes and len(value) <= MAX_BYTES, "CAPTURE_SIZE")
        return value

    def __call__(self, receipt):
        with self._lock:
            try:
                _require(self._healthy, "CAPTURE_UNHEALTHY")
                row = {"seq": self._records, "previous": self._previous,
                       "receipt": _receipt(receipt, self.expected)}
                line = _encode(row) + b"\n"
                _require(len(line) <= MAX_LINE and self._records < MAX_RECORDS
                         and len(self._raw) + len(line) <= MAX_BYTES, "CAPTURE_SIZE")
                _require(self._read() == self._raw, "CAPTURE_CHANGED")
                self._handle.seek(0, os.SEEK_END)
                _require(self._handle.write(line) == len(line), "CAPTURE_PARTIAL_WRITE")
                self._handle.flush()
                os.fsync(self._handle.fileno())
                _require(self._read() == self._raw + line, "CAPTURE_READBACK")
                self._raw += line
                self._records += 1
                self._previous = _digest(line)
            except (Exception, asyncio.CancelledError):
                self._healthy = False
                raise CaptureError("CAPTURE_WRITE") from None

    def checkpoint(self, *, quiescence_receipt):
        """Caller retains this anchor independently; not a seal against late IO."""
        with self._lock:
            try:
                _require(_text(quiescence_receipt), "CAPTURE_QUIESCENCE")
                _require(self._healthy and self._read() == self._raw, "CAPTURE_UNHEALTHY")
                return CaptureAnchor(len(self._raw), _digest(self._raw), self._records,
                                     self._bindings, quiescence_receipt)
            except Exception:
                self._healthy = False
                raise CaptureError("CAPTURE_ANCHOR") from None

    def readback(self, anchor):
        with self._lock:
            raw, receipts = b"", []
            read_ok, anchor_checked = False, False
            try:
                raw = self._read()
                read_ok = True
                if raw != self._raw:
                    self._healthy = False
                _require(self._healthy, "CAPTURE_UNHEALTHY")
                _require(type(anchor) is CaptureAnchor and _text(anchor.quiescence_receipt)
                         and anchor.bindings_sha256 == self._bindings
                         and type(anchor.length) is int and anchor.length == len(raw)
                         and anchor.sha256 == _digest(raw) and raw == self._raw
                         and type(anchor.records) is int and anchor.records == self._records,
                         "CAPTURE_ANCHOR")
                anchor_checked = True
                previous = ZERO
                lines = raw.splitlines(keepends=True)
                _require(len(lines) == anchor.records, "CAPTURE_RECORDS")
                for index, line in enumerate(lines):
                    _require(line.endswith(b"\n") and len(line) <= MAX_LINE, "CAPTURE_TRUNCATED")
                    row = json.loads(line)
                    _require(type(row) is dict and set(row) == {"seq", "previous", "receipt"}
                             and type(row["seq"]) is int and row["seq"] == index
                             and row["previous"] == previous and _encode(row) + b"\n" == line,
                             "CAPTURE_RECORD")
                    value = row["receipt"]
                    _require(type(value) is dict and set(value) == {
                        "binding", "occurrence", "transport", "phase", "status", "category",
                    }, "CAPTURE_RECEIPT")
                    _require(type(value["binding"]) is list and len(value["binding"]) == 5,
                             "CAPTURE_BINDING")
                    r = Receipt(Binding(*value["binding"]), value["occurrence"], value["transport"],
                                value["phase"], value["status"], value["category"])
                    _receipt(r, self.expected)
                    receipts.append(r)
                    previous = _digest(line)
                issues = _coverage(receipts, self.expected)
            except (Exception, asyncio.CancelledError):
                # Observed integrity/durability failure is permanent. Restoring
                # bytes later cannot turn this interval into complete evidence.
                if not read_ok or anchor_checked:
                    self._healthy = False
                issues = ("CAPTURE_READBACK_INCOMPLETE",)
            return CaptureReadback(not issues, issues, raw, tuple(receipts))

    def reconcile(self, anchor, *, state, manifest_sha256, manifest_etag,
                  operations=(), stops=()):
        """Join independent caller anchors with accepted reader output.

        No import of the non-runtime reader and no aggregate/schema modification.
        Returns conditional list *candidates*, never accepted execution results.
        Missing evidence returns no accounting, while raw capture is preserved.
        """
        with self._lock:
            capture = self.readback(anchor)
            try:
                _require(capture.complete, "CAPTURE_INCOMPLETE")
                _require(state.complete is True and not state.issues
                         and state.quiescence_receipt == anchor.quiescence_receipt,
                         "CAPTURE_STATE")
                for manifest in (state.manifest, state.manifest_recheck):
                    _require(manifest is not None and manifest.sha256 == manifest_sha256
                             and _digest(manifest.raw) == manifest_sha256
                             and manifest.etag == manifest_etag and _text(manifest_etag),
                             "CAPTURE_MANIFEST")
                head = Manifest.model_validate(decode_document(state.manifest.raw))
                ops, stop_refs = tuple(operations), tuple(stops)
                _require(all(type(a) is OperationAnchor for a in ops)
                         and all(type(a) is StopAnchor for a in stop_refs), "CAPTURE_STATE_ANCHOR")
                anchors = [a.binding for a in (*ops, *stop_refs)]
                _require(len(anchors) == len(self.expected) and set(anchors) == set(self.expected),
                         "CAPTURE_STATE_ANCHOR")
                for a in ops:
                    b = a.binding
                    _require(b.action in ("create", "send"), "CAPTURE_STATE_ANCHOR")
                    child = head.children.get(b.role)
                    _require(child is not None and child.bound and child.hosted_id == b.target
                             and child.version == b.version, "CAPTURE_TARGET")
                    records = [r for r in state.operations if r.name == a.name]
                    _require(len(records) == 1, "CAPTURE_OPERATION")
                    record = records[0]
                    _require(record.sha256 == a.sha256 and _digest(record.raw) == a.sha256,
                             "CAPTURE_OPERATION")
                    document = decode_document(record.raw)
                    _require(set(document) == {"scope_binding", "effect"}, "CAPTURE_OPERATION")
                    scope = ScopeBinding.model_validate(document["scope_binding"])
                    effect = Effect.model_validate(document["effect"])
                    _require(scope == head.scope_binding and effect.operation_id == b.operation
                             and effect.role == b.role
                             and effect.kind == ("create" if b.action == "create" else "call")
                             and a.name == f"{scope.prefix}operations/{b.operation}/{effect.status}.json",
                             "CAPTURE_OPERATION")
                for a in stop_refs:
                    b = a.binding
                    _require(b.action == "stop" and a.state in ("stopped", "idle")
                             and b.target == head.scope_binding.parent_session
                             and b.version == head.coordinator_version, "CAPTURE_STOP")
                return Accounting(True, (), capture,
                                  tuple(b.operation for b in self.expected if b.action == "create"),
                                  tuple(b.operation for b in self.expected if b.action == "send"),
                                  tuple(b.target for b in self.expected if b.action == "stop"))
            except (Exception, asyncio.CancelledError):
                return Accounting(False, ("CAPTURE_RECONCILIATION_INCOMPLETE",), capture)
