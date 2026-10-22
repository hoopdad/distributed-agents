from __future__ import annotations

import asyncio
from contextlib import redirect_stderr, redirect_stdout
from dataclasses import FrozenInstanceError, replace
import hashlib
import io
import json
import logging
import unittest
from unittest.mock import patch
from uuid import uuid4

from demo import diagnostics as d


def fixture(kind=d.Kind.SEND, **kwargs):
    """Synthetic shared fixture: no endpoint, credential or user values."""
    return d.Event(d.Role.COORDINATOR, d.Stage.OUTBOUND, kind,
                   method=d.Method.POST, route=d.Route.AGENT_RESPONSES, **kwargs)


class DiagnosticContractTests(unittest.TestCase):
    def test_header_states_case_duplicates_and_no_mutation(self):
        cases = [
            ([], d.Presence.ABSENT),
            ([(b"X-MS-USER-IDENTITY", b"")], d.Presence.EMPTY),
            ([("X-Ms-User-Identity", "synthetic")], d.Presence.NONEMPTY),
            ([(b"x-ms-user-identity", b" ")], d.Presence.NONEMPTY),
            ([(b"x-ms-user-identity", b"a"), (b"X-MS-USER-IDENTITY", b"a")],
             d.Presence.MALFORMED_DUPLICATE),
            ([(b"x-ms-user-identity", b"\r\ninjected")], d.Presence.MALFORMED_DUPLICATE),
            ([(b"x-ms-user-identity", None)], d.Presence.MALFORMED_DUPLICATE),
            ([(b"x-ms-user-identity", "x" * 8193)], d.Presence.MALFORMED_DUPLICATE),
        ]
        for headers, expected in cases:
            with self.subTest(expected=expected, headers_count=len(headers)):
                original = list(headers)
                self.assertEqual(d.observe_header(headers, "delegation"),
                                 d.Observation(d.Coverage.OBSERVED, expected))
                self.assertEqual(headers, original)
        self.assertEqual(d.observe_header([(b"x-agent-user-id", b"x")], "platform").presence,
                         d.Presence.NONEMPTY)
        self.assertEqual(d.observe_header([(b"x-agent-foundry-call-id", b"x")], "call").presence,
                         d.Presence.NONEMPTY)

    def test_missing_coverage_never_means_absent(self):
        for invalid in (None, iter([]), [(b"broken",)], [("", b"value")], [("é", b"x")],
                        [(b"bad\r\nname", b"x")],
                        [(b"a", b"")] * 513):
            self.assertEqual(d.observe_header(invalid, "platform"), d.unobserved())
        self.assertEqual(d.observe_header([], "Authorization"), d.unobserved())
        for coverage in (d.Coverage.UNAVAILABLE, d.Coverage.NOT_REACHED):
            fields = d.event_fields(fixture(platform=d.unobserved(coverage)))
            self.assertEqual(fields["platform"], {"coverage": coverage.value})
        with self.assertRaises(ValueError):
            d.unobserved(d.Coverage.OBSERVED)

    def test_scope_values_and_explicit_comparability(self):
        self.assertEqual(d.observe_value(None).presence, d.Presence.ABSENT)
        self.assertEqual(d.observe_value("").presence, d.Presence.EMPTY)
        self.assertEqual(d.observe_value("x").presence, d.Presence.NONEMPTY)
        self.assertEqual(d.compare_values("x", "x"), d.Match.NOT_COMPARABLE)
        for left, right in ((None, None), ("", ""), (b"x", "x"), ("\n", "\n"), (1, 1)):
            self.assertEqual(d.compare_values(left, right, same_representation=True),
                             d.Match.NOT_COMPARABLE)
        self.assertEqual(d.compare_values("x", "x", same_representation=True), d.Match.TRUE)
        self.assertEqual(d.compare_values(b"x", b"y", same_representation=True), d.Match.FALSE)

    def test_closed_schema_rejects_raw_text_objects_and_nonfinite_numbers(self):
        secret = "Bearer PRIVATE_SENTINEL?private=query"
        mutations = [
            {"role": secret}, {"stage": secret}, {"kind": secret}, {"method": secret},
            {"route": "https://private.invalid/" + secret}, {"category": RuntimeError(secret)},
            {"scope_request_match": secret}, {"binding": secret},
            {"binding": d.Binding(uuid4(), response=secret)},
            {"platform": {"presence": secret}},
            {"platform": d.Observation(d.Coverage.UNAVAILABLE, d.Presence.ABSENT)},
            {"platform": d.Observation(d.Coverage.OBSERVED, secret)},
            {"status": True}, {"status": 600}, {"duration_ms": float("nan")},
            {"duration_ms": float("inf")}, {"duration_ms": -1}, {"duration_ms": True},
            {"duration_ms": 86_400_001},
        ]
        with patch.object(d._logger, "info") as sink:
            for changes in mutations:
                with self.subTest(fields=list(changes)):
                    self.assertFalse(d.emit(replace(fixture(), **changes)))
            self.assertFalse(d.emit(object()))
        sink.assert_not_called()
        with self.assertRaises(TypeError):
            d.Event(d.Role.COORDINATOR, d.Stage.OUTBOUND, d.Kind.SEND, body=secret)

    def test_redaction_sentinels_never_reach_event_or_hash(self):
        sentinels = ["PRIVATE_USER_SENTINEL", "Bearer PRIVATE_TOKEN_SENTINEL",
                     "https://private.invalid/path?secret=QUERY_SENTINEL", "BODY_SENTINEL"]
        headers = [(b"x-agent-user-id", sentinels[0]),
                   (b"authorization", sentinels[1]), (b"x-other", sentinels[2])]
        event = fixture(platform=d.observe_header(headers, "platform"),
                        delegation=d.observe_value(sentinels[3]),
                        scope_user=d.observe_value(sentinels[0]),
                        request_user=d.observe_value(sentinels[0]),
                        scope_request_match=d.compare_values(
                            sentinels[0], sentinels[0], same_representation=True))
        with patch.object(d._logger, "info") as sink:
            self.assertTrue(d.emit(event))
        payload = sink.call_args.args[0]
        for secret in sentinels:
            self.assertNotIn(secret, payload)
            self.assertNotIn(hashlib.sha256(secret.encode()).hexdigest(), payload)
        self.assertEqual(json.loads(payload)["scope_request_match"], "true")
        self.assertLess(len(payload), 4096)

    def test_no_arbitrary_object_stringification_or_equality(self):
        class Hostile:
            def __str__(self):
                raise AssertionError("must not stringify")

            def __eq__(self, other):
                raise AssertionError("must not compare")

        value = Hostile()
        self.assertEqual(d.observe_value(value).presence, d.Presence.MALFORMED_DUPLICATE)
        self.assertEqual(d.compare_values(value, value, same_representation=True),
                         d.Match.NOT_COMPARABLE)
        self.assertEqual(d.observe_header([(b"x-agent-user-id", value)], "platform").presence,
                         d.Presence.MALFORMED_DUPLICATE)
        with patch.object(d._logger, "info") as sink:
            self.assertFalse(d.emit(replace(fixture(), route=value)))
        sink.assert_not_called()

    def test_logger_and_serialization_failure_preserve_original_rejection(self):
        class Rejected(Exception):
            pass

        rejection = Rejected("PRIVATE_REJECTION_SENTINEL")
        for target in (patch.object(d._logger, "info", side_effect=RuntimeError("PRIVATE_LOG")),
                       patch.object(d.json, "dumps", side_effect=ValueError("PRIVATE_JSON"))):
            with target:
                with self.assertRaises(Rejected) as caught:
                    try:
                        raise rejection
                    finally:
                        self.assertFalse(d.emit(fixture(d.Kind.EXECUTION_REJECTED)))
                self.assertIs(caught.exception, rejection)

    def test_stderr_only_no_root_stdout_and_fixed_json(self):
        stream, stdout = io.StringIO(), io.StringIO()
        private = logging.StreamHandler(stream)
        root_stdout = logging.StreamHandler(stdout)
        root = logging.getLogger()
        root.addHandler(root_stdout)
        try:
            with patch.object(d._logger, "handlers", [private]), redirect_stdout(stdout):
                self.assertTrue(d.emit(fixture(status=200, duration_ms=1.23456)))
        finally:
            root.removeHandler(root_stdout)
        self.assertEqual(stdout.getvalue(), "")
        fields = json.loads(stream.getvalue())
        self.assertEqual(fields["schema_version"], 1)
        self.assertEqual(fields["duration_ms"], 1.235)
        self.assertNotIn("success", fields)
        self.assertNotIn("binding", fields)

    def test_actual_stderr_sink_failure_does_not_print_logging_traceback(self):
        class BrokenStream:
            def write(self, text):
                raise OSError("PRIVATE_SINK_EXCEPTION")

        stderr, stdout = io.StringIO(), io.StringIO()
        handler = d._PrivateHandler(BrokenStream())
        with (patch.object(d._logger, "handlers", [handler]),
              patch.object(logging, "raiseExceptions", True),
              redirect_stderr(stderr), redirect_stdout(stdout)):
            d.emit(fixture())
        self.assertEqual(stderr.getvalue(), "")
        self.assertEqual(stdout.getvalue(), "")

    def test_milestones_do_not_infer_execution_success(self):
        kinds = [d.Kind.SEND, d.Kind.RESPONSE_HEADERS, d.Kind.STREAM_COMPLETE,
                 d.Kind.ASGI_FINAL_BODY, d.Kind.EXECUTION_REJECTED]
        binding = d.new_binding(operation=uuid4(), response=uuid4())
        events = [d.event_fields(fixture(kind, binding=binding)) for kind in kinds]
        self.assertEqual([event["kind"] for event in events], [kind.value for kind in kinds])
        self.assertTrue(all("success" not in event for event in events))
        self.assertTrue(all(event["binding"] == events[0]["binding"] for event in events))

    def test_binding_nested_reset_validation_and_immutability(self):
        outer, inner = d.new_binding(), d.new_binding()
        self.assertIsNone(d.current_binding())
        with d.bind(outer):
            self.assertEqual(d.event_fields(fixture())["binding"]["observation"],
                             str(outer.observation))
            with self.assertRaises(RuntimeError):
                with d.bind(inner):
                    self.assertIs(d.current_binding(), inner)
                    raise RuntimeError("synthetic")
            self.assertIs(d.current_binding(), outer)
        self.assertIsNone(d.current_binding())
        with self.assertRaises(FrozenInstanceError):
            outer.observation = uuid4()
        with self.assertRaises(ValueError):
            d.new_binding(operation="arbitrary")
        with self.assertRaises(ValueError):
            with d.bind(d.Binding("arbitrary")):
                self.fail("invalid binding entered context")


class DiagnosticIsolationTests(unittest.IsolatedAsyncioTestCase):
    async def test_concurrent_and_inherited_background_snapshot_after_exit(self):
        release = asyncio.Event()
        aliases = [d.new_binding(), d.new_binding()]

        async def background():
            await release.wait()
            return d.event_fields(fixture(d.Kind.CONTEXT))["binding"]

        async def request(binding):
            with d.bind(binding):
                task = asyncio.create_task(background())
                await asyncio.sleep(0)
                self.assertIs(d.current_binding(), binding)
            self.assertIsNone(d.current_binding())
            return task

        tasks = await asyncio.gather(*(request(binding) for binding in aliases))
        self.assertIsNone(d.current_binding())
        release.set()
        results = await asyncio.gather(*tasks)
        self.assertEqual([result["observation"] for result in results],
                         [str(binding.observation) for binding in aliases])

    async def test_cancelled_request_resets_binding_and_propagates(self):
        entered = asyncio.Event()

        async def request():
            try:
                with d.bind(d.new_binding()):
                    try:
                        entered.set()
                        await asyncio.Future()
                    finally:
                        with patch.object(d._logger, "info", side_effect=RuntimeError("logger")):
                            self.assertFalse(d.emit(fixture(d.Kind.CANCELLED)))
            finally:
                self.assertIsNone(d.current_binding())
            self.fail("cancellation suppressed")

        task = asyncio.create_task(request())
        await entered.wait()
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await task
        self.assertIsNone(d.current_binding())


if __name__ == "__main__":
    unittest.main()
