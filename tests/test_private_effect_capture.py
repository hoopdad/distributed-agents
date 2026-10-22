"""Synthetic private local files/public transports only; never live receipts."""
from __future__ import annotations

import asyncio
from contextlib import ExitStack, redirect_stdout, redirect_stderr
from dataclasses import replace
import hashlib
import io
import json
import os
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock, patch

import test_host_diagnostics as host_fixtures
from test_effect_observation import (
    Bytes, ProjectWire, RawBytes, binding, child, credential, response_path,
)
from demo import effect_observation as e
from demo.private_effect_capture import CaptureError, PrivateEffectCapture
from demo.foundry import OriginTransport, ProjectClient, RemoteAgents

import httpx2


def receipt(b, phase, occurrence=None, status=None, category=None):
    return e.Receipt(b, occurrence, "dispatch" if phase.startswith("window_") else
                     "project" if b.action == "create" else "responses",
                     phase, status, category)


def completed(capture, b, *, occurrence="a" * 32, status=None):
    status = status if status is not None else 201 if b.action == "create" else 204 if b.action == "stop" else 200
    capture(receipt(b, "window_open"))
    capture(receipt(b, "request", occurrence))
    capture(receipt(b, "headers", occurrence, status))
    if b.action != "create":
        capture(receipt(b, "stream_complete", occurrence, status))
    capture(receipt(b, "window_closed"))


class DurabilityTests(unittest.TestCase):
    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)

    def new(self, expected=None, wrapper=None):
        handle = self.stack.enter_context(tempfile.TemporaryFile("w+b"))
        capture = PrivateEffectCapture(wrapper(handle) if wrapper else handle,
                                       expected=[binding()] if expected is None else expected, new_exclusive=True)
        return handle, capture

    def test_strict_order_durable_roundtrip_opaque_objects_and_caller_ownership(self):
        handle, capture = self.new()
        completed(capture, binding())
        anchor = capture.checkpoint(quiescence_receipt="owned-quiescence")
        result = capture.readback(anchor)
        self.assertTrue(result.complete, result.issues)
        self.assertEqual([r.phase for r in result.receipts],
                         ["window_open", "request", "headers", "stream_complete", "window_closed"])
        self.assertEqual(anchor.length, len(result.raw))
        self.assertEqual(anchor.sha256, hashlib.sha256(result.raw).hexdigest())
        for private in (capture, anchor, result):
            self.assertNotIn("synthetic", repr(private))
        self.assertFalse(handle.closed)

    def test_handle_binding_and_receipt_rejections_are_constant_and_no_discovery(self):
        for expected in ([], [binding(), binding()], [replace(binding(), role="rogue")],
                         [replace(binding(), operation="private\ninvalid")]):
            with self.assertRaises(CaptureError):
                self.new(expected=expected)
        handle = self.stack.enter_context(tempfile.TemporaryFile("w+b"))
        for exclusive in (False, None):
            with self.assertRaisesRegex(CaptureError, "^CAPTURE_HANDLE$"):
                PrivateEffectCapture(handle, expected=[binding()], new_exclusive=exclusive)
        handle.write(b"existing-private-bytes")
        handle.flush()
        with self.assertRaisesRegex(CaptureError, "^CAPTURE_HANDLE$"):
            PrivateEffectCapture(handle, expected=[binding()], new_exclusive=True)
        for invalid in (
            object(), replace(receipt(binding(), "request", "a" * 32), phase="arbitrary"),
            receipt(binding(), "request", "not-an-occurrence"),
            receipt(binding(), "headers", "a" * 32, True),
            receipt(binding(), "window_closed", category="private-secret"),
            receipt(replace(binding(), target="foreign"), "window_open"),
        ):
            _, capture = self.new()
            with self.assertRaisesRegex(CaptureError, "^CAPTURE_WRITE$"):
                capture(invalid)

    def test_partial_write_fsync_failure_and_cancelled_sink_latch_unhealthy_keep_bytes(self):
        class Partial:
            def __init__(self, handle):
                self.handle = handle
            def __getattr__(self, name):
                return getattr(self.handle, name)
            def write(self, raw):
                return self.handle.write(raw[:7])

        handle, capture = self.new(wrapper=Partial)
        with self.assertRaises(CaptureError):
            capture(receipt(binding(), "window_open"))
        handle.seek(0)
        self.assertEqual(len(handle.read()), 7)
        self.assertFalse(capture.readback(None).complete)
        for failure in (OSError("PRIVATE_FSYNC"), asyncio.CancelledError()):
            handle, capture = self.new()
            with patch("demo.private_effect_capture.os.fsync", side_effect=failure):
                with self.assertRaisesRegex(CaptureError, "^CAPTURE_WRITE$"):
                    capture(receipt(binding(), "window_open"))
            self.assertFalse(capture.readback(None).complete)
            self.assertGreater(os.fstat(handle.fileno()).st_size, 0)
            with self.assertRaises(CaptureError):
                capture.checkpoint(quiescence_receipt="owned")

    def test_readback_corruption_truncation_extra_fields_gaps_and_anchor_changes(self):
        for mutation in (
            lambda raw: raw[:-1],
            lambda raw: raw.replace(b'"seq":1', b'"seq":9'),
            lambda raw: raw.replace(b'"phase":"request"', b'"phase":"unknown"'),
            lambda raw: raw.replace(b'"seq":0', b'"extra":1,"seq":0'),
            lambda raw: raw.replace(b"synthetic-child", b"different-child"),
            lambda raw: raw + raw.splitlines(keepends=True)[0],
        ):
            handle, capture = self.new()
            completed(capture, binding())
            anchor = capture.checkpoint(quiescence_receipt="owned")
            original = capture.readback(anchor).raw
            changed = mutation(original)
            handle.seek(0)
            handle.write(changed)
            handle.truncate()
            handle.flush()
            result = capture.readback(anchor)
            self.assertFalse(result.complete)
            self.assertEqual(result.raw, changed)
        _, capture = self.new()
        completed(capture, binding())
        anchor = capture.checkpoint(quiescence_receipt="owned")
        for forged in (replace(anchor, records=2), replace(anchor, bindings_sha256="0" * 64),
                       replace(anchor, quiescence_receipt=""), replace(anchor, length=True)):
            self.assertFalse(capture.readback(forged).complete)

    def test_reject_semantic_order_pending_error_late_and_duplicate_without_dedup(self):
        b = binding()
        cases = [
            [receipt(b, "window_open")],
            [receipt(b, "window_open"), receipt(b, "headers", "a" * 32, 200)],
            [receipt(b, "window_open"), receipt(b, "request", "a" * 32),
             receipt(b, "error", "a" * 32, category="cancelled"),
             receipt(b, "window_closed")],
            [receipt(b, "window_open"), receipt(b, "request", "a" * 32),
             receipt(b, "headers", "a" * 32, 200), receipt(b, "stream_closed", "a" * 32, 200),
             receipt(b, "window_closed")],
        ]
        for rows in cases:
            _, capture = self.new()
            for row in rows:
                capture(row)
            result = capture.readback(capture.checkpoint(quiescence_receipt="owned"))
            self.assertFalse(result.complete)
            self.assertEqual(result.receipts, tuple(rows))
        _, capture = self.new()
        completed(capture, b)
        # Same binding, second dispatch/attempt is retained, never collapsed.
        completed(capture, b, occurrence="b" * 32)
        result = capture.readback(capture.checkpoint(quiescence_receipt="owned"))
        self.assertFalse(result.complete)
        self.assertEqual(result.raw.count(b'"phase":"request"'), 2)

    def test_stop_needs_actual_204_not_200_or_intent(self):
        b = binding("stop", "coordinator", target="synthetic-parent")
        for status in (200, 204):
            _, capture = self.new([b])
            completed(capture, b, status=status)
            result = capture.readback(capture.checkpoint(quiescence_receipt="owned"))
            self.assertEqual(result.complete, status == 204)

    def test_storage_bounds_fail_closed_without_erasing_prefix(self):
        handle, capture = self.new()
        capture(receipt(binding(), "window_open"))
        handle.seek(0)
        prefix = handle.read()
        with patch("demo.private_effect_capture.MAX_RECORDS", 1):
            with self.assertRaises(CaptureError):
                capture(receipt(binding(), "request", "a" * 32))
        handle.seek(0)
        self.assertEqual(handle.read(), prefix)
        self.assertFalse(capture.readback(None).complete)

    def test_pending_at_close_cannot_be_repaired_by_later_stream_completion(self):
        b = binding()
        _, capture = self.new()
        for r in (
            receipt(b, "window_open"), receipt(b, "request", "a" * 32),
            receipt(b, "headers", "a" * 32, 200),
            receipt(b, "window_closed"),  # even a malformed optimistic close
            receipt(b, "stream_complete", "a" * 32, 200),
        ):
            capture(r)
        result = capture.readback(capture.checkpoint(quiescence_receipt="owned"))
        self.assertFalse(result.complete)
        self.assertIn("CAPTURE_INCOMPLETE", result.issues)
        self.assertEqual(len(result.receipts), 5)

    def test_every_valid_phase_is_retained_even_when_accounting_rejects(self):
        # Separate captures exercise request_late, error and close_error alongside
        # ordinary phases; failure does not delete or rewrite raw receipts.
        b = binding()
        for tail in (
            [receipt(b, "error", "a" * 32, 200, "timeout"),
             receipt(b, "close_error", "a" * 32, 200, "transport")],
            [receipt(b, "stream_complete", "a" * 32, 200),
             receipt(b, "close_error", "a" * 32, 200, "cancelled")],
        ):
            _, capture = self.new()
            rows = [receipt(b, "window_open"), receipt(b, "request", "a" * 32),
                    receipt(b, "headers", "a" * 32, 200), *tail, receipt(b, "window_closed")]
            for r in rows:
                capture(r)
            result = capture.readback(capture.checkpoint(quiescence_receipt="owned"))
            self.assertFalse(result.complete)
            self.assertEqual(result.receipts, tuple(rows))


class PublicTransportTests(unittest.IsolatedAsyncioTestCase):
    async def test_failed_fsync_does_not_change_real_project_outcome_or_retry(self):
        for failure in (OSError("PRIVATE_ERROR"), asyncio.CancelledError()):
            with tempfile.TemporaryFile("w+b") as handle:
                capture = PrivateEffectCapture(handle, expected=[binding("create")], new_exclusive=True)
                wire = ProjectWire()
                with patch("demo.private_effect_capture.os.fsync", side_effect=failure):
                    async with httpx2.AsyncClient() as http:
                        async with ProjectClient(credential(), http, {}, transport=wire) as project:
                            with e.private_sink(capture), e.dispatch(binding("create")) as window:
                                await RemoteAgents(project, {}).create(child())
                self.assertEqual(len(wire.requests), 1)
                self.assertTrue(window.sink_failed)
                self.assertFalse(window.capture_complete)
                self.assertFalse(capture.readback(None).complete)
                self.assertGreater(os.fstat(handle.fileno()).st_size, 0)

    async def test_concurrent_real_project_composition_and_binding_isolation(self):
        bindings = [binding("create", operation=f"operation-{i}", target=f"child-{i}") for i in range(2)]
        with ExitStack() as stack:
            captures = [PrivateEffectCapture(stack.enter_context(tempfile.TemporaryFile("w+b")),
                                            expected=[b], new_exclusive=True) for b in bindings]
            wire = ProjectWire()
            async with httpx2.AsyncClient() as http:
                async with ProjectClient(credential(), http, {}, transport=wire) as project:
                    async def run(b, capture):
                        selected = child()
                        selected.hosted_id = b.target
                        with e.private_sink(capture), e.dispatch(b):
                            await RemoteAgents(project, {}).create(selected)
                    await asyncio.gather(*(asyncio.create_task(run(b, c)) for b, c in zip(bindings, captures)))
            self.assertEqual(len(wire.requests), 2)
            for b, capture in zip(bindings, captures):
                result = capture.readback(capture.checkpoint(quiescence_receipt="owned"))
                self.assertTrue(result.complete, result.issues)
                self.assertTrue(all(r.binding == b for r in result.receipts))

    async def test_completed_then_late_inherited_traffic_invalidates_old_and_new_anchors(self):
        release = asyncio.Event()
        with tempfile.TemporaryFile("w+b") as handle:
            capture = PrivateEffectCapture(handle, expected=[binding()], new_exclusive=True)
            async with httpx2.AsyncClient(transport=OriginTransport(httpx2.MockTransport(
                    lambda r: httpx2.Response(200, stream=RawBytes(b"PRIVATE_BODY"))))) as http:
                async def send_late():
                    await release.wait()
                    await http.post(response_path())
                with e.private_sink(capture), e.dispatch(binding()):
                    await http.post(response_path())
                    task = asyncio.create_task(send_late())
                anchor = capture.checkpoint(quiescence_receipt="premature")
                self.assertTrue(capture.readback(anchor).complete)
                release.set()
                await task
            self.assertFalse(capture.readback(anchor).complete)
            result = capture.readback(capture.checkpoint(quiescence_receipt="actual-quiescence"))
            self.assertFalse(result.complete)
            self.assertIn("CAPTURE_LATE", result.issues)
            attempts = [r for r in result.receipts if r.phase == "request"]
            self.assertEqual(len(attempts), 2)
            self.assertEqual(len({r.occurrence for r in attempts}), 2)
            self.assertNotIn(b"PRIVATE_BODY", result.raw)

    async def test_stream_cancel_early_close_and_sink_failure_preserve_wire_semantics(self):
        for mode in ("retained", "broken", "cancelled", "absent", "early"):
            with self.subTest(mode=mode), tempfile.TemporaryFile("w+b") as handle:
                capture = PrivateEffectCapture(handle, expected=[binding()], new_exclusive=True)
                stream = Bytes(block=True)
                def broken(r):
                    raise OSError("PRIVATE_ERROR")
                def cancelled(r):
                    raise asyncio.CancelledError()
                sink = {"retained": capture, "early": capture, "broken": broken,
                        "cancelled": cancelled, "absent": None}[mode]
                out, err = io.StringIO(), io.StringIO()
                with redirect_stdout(out), redirect_stderr(err):
                    async with httpx2.AsyncClient(transport=OriginTransport(httpx2.MockTransport(
                            lambda r: httpx2.Response(200, stream=stream)))) as http:
                        with e.private_sink(sink), e.dispatch(binding()):
                            response = await http.send(http.build_request("POST", response_path()), stream=True)
                            self.assertEqual(stream.pulls, 0)
                            if mode != "early":
                                async def consume():
                                    async for _ in response.aiter_bytes():
                                        pass
                                task = asyncio.create_task(consume())
                                await stream.entered.wait()
                                task.cancel()
                                with self.assertRaises(asyncio.CancelledError):
                                    await task
                            await response.aclose()
                            await response.aclose()
                self.assertEqual(stream.closes, 1)
                self.assertEqual(out.getvalue(), "")
                # Under parallel suite load asyncio may emit its own slow-task
                # debug warning to stderr; that is not a consumer log. Check
                # the actual private sentinels rather than suppressing warnings.
                for forbidden in ("PRIVATE_ERROR", "private-body", "synthetic-operation",
                                  "synthetic-child"):
                    self.assertNotIn(forbidden, err.getvalue())
                result = capture.readback(capture.checkpoint(quiescence_receipt="owned"))
                self.assertFalse(result.complete)
                self.assertNotIn(b"private-body", result.raw)

    async def test_known_response_only_recovery_never_creates_send_accounting(self):
        seen = []
        payload = {"id": "resp_synthetic", "object": "response", "created_at": 1,
                   "model": "", "status": "completed", "agent_session_id": "synthetic-child",
                   "output": [{"type": "message", "id": "msg_synthetic", "role": "assistant",
                               "status": "completed", "content": [
                                   {"type": "output_text", "text": "Synthetic output.", "annotations": []}]}]}
        def handle(request):
            seen.append(request.method)
            return httpx2.Response(200, json=payload)
        with tempfile.TemporaryFile("w+b") as file:
            capture = PrivateEffectCapture(file, expected=[binding()], new_exclusive=True)
            async with httpx2.AsyncClient(transport=OriginTransport(httpx2.MockTransport(handle))) as http:
                async with ProjectClient(credential(), http, {}) as project:
                    project.agents.get_session = AsyncMock(return_value=SimpleNamespace(
                        status="active", version_indicator=SimpleNamespace(agent_version="7")))
                    with e.private_sink(capture), e.dispatch(binding()):
                        self.assertEqual(await RemoteAgents(project, {}).recover(child(), "resp_synthetic"),
                                         "Synthetic output.")
            self.assertEqual(seen, ["GET"])
            result = capture.readback(capture.checkpoint(quiescence_receipt="owned"))
            self.assertFalse(result.complete)
            self.assertFalse(any(r.phase == "request" for r in result.receipts))


class PinnedBackgroundConsumerTests(unittest.IsolatedAsyncioTestCase):
    # Reuse only local setup/helpers, not duplicate baseline test discovery.
    asyncSetUp = host_fixtures.PinnedHostTests.asyncSetUp
    asyncTearDown = host_fixtures.PinnedHostTests.asyncTearDown
    terminal_snapshot = host_fixtures.PinnedHostTests.terminal_snapshot
    server = host_fixtures.PinnedHostTests.server
    async def test_consumer_installed_before_real_resilient_background_task_creation(self):
        release, entered, finished = asyncio.Event(), asyncio.Event(), asyncio.Event()
        selected = binding("create")
        wire = ProjectWire()
        def factory(request):
            self.owned_response_ids.append(request.response_id)
            async def specialize(text):
                entered.set()
                await release.wait()
                async with httpx2.AsyncClient() as http:
                    async with ProjectClient(credential(), http, {}, transport=wire) as project:
                        with e.dispatch(selected):
                            await RemoteAgents(project, {}).create(child())
                finished.set()
                return "synthetic result"
            runtime = SimpleNamespace(role="architect", request=request, specialize=specialize)
            with patch("demo.workflow.WorkflowRuntime", return_value=runtime):
                return host_fixtures.create_workflow(request)
        server = self.server(factory)
        with tempfile.TemporaryFile("w+b") as file:
            capture = PrivateEffectCapture(file, expected=[selected], new_exclusive=True)
            async with server.router.lifespan_context(server):
                async with httpx2.AsyncClient(
                    transport=httpx2.ASGITransport(app=server), base_url="http://synthetic",
                ) as client:
                    headers = {"x-agent-user-id": "synthetic-user-0",
                               "x-agent-foundry-call-id": "synthetic-call-0"}
                    with e.private_sink(capture):
                        response = await client.post("/responses", json={
                            "input": "synthetic turn", "background": True, "store": True,
                        }, headers=headers)
                    self.assertEqual(response.status_code, 200)
                    await asyncio.wait_for(entered.wait(), 10)
                    self.assertEqual(os.fstat(file.fileno()).st_size, 0)
                    release.set()
                    await asyncio.wait_for(finished.wait(), 10)
                    result = await self.terminal_snapshot(client, response.json()["id"], headers)
                    self.assertEqual(result.json()["status"], "completed")
            readback = capture.readback(capture.checkpoint(quiescence_receipt="owned"))
            self.assertTrue(readback.complete, readback.issues)
            self.assertEqual(len(wire.requests), 1)
            self.assertNotIn(b"synthetic-user", readback.raw)


if __name__ == "__main__":
    unittest.main()
