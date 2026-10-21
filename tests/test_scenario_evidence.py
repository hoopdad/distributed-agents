"""Synthetic boundary captures only: no hosted or compute-recovery claims."""
from __future__ import annotations

import asyncio
import copy
import dataclasses
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
from contextlib import ExitStack
from types import SimpleNamespace
from unittest.mock import patch

from agent_framework import InMemoryCheckpointStorage

from live_acceptance import SCENARIOS, events, validate_artifact_evidence, validate_scenario_evidence
from demo import routing, workflow
from demo.artifacts import decode_document
from test_workflow import (
    FakeRouter, MemoryBackend, RecordingRemote, TestRuntime, graph, make_store,
    synthetic_calibration,
)


class ScenarioClock:
    """Fixture-owned wall time; only admission waits advance it, never the host."""

    epoch = 2_000_000_000.0

    def __init__(self):
        self.now = self.epoch
        self.reads = 0
        self.waits = []

    def time(self):
        self.reads += 1
        if self.reads > 10_000:
            raise AssertionError("SYNTHETIC_CLOCK_READ_LIMIT")
        return self.now

    async def sleep(self, delay):
        if not 0 < delay <= 65 or len(self.waits) >= 20 or self.now + delay > self.epoch + 600:
            raise AssertionError("SYNTHETIC_CLOCK_WAIT_LIMIT")
        self.waits.append(delay)
        self.now += delay
        await asyncio.sleep(0)  # Yield without changing or waiting on the event-loop clock.


def clock_bindings():
    # Include shared clocks to detect accidental stdlib/event-loop clock mutation.
    return (workflow.time, routing.time, routing.asyncio, time.time, time.monotonic, asyncio.sleep)


class CapturedRemote(RecordingRemote):
    def __init__(self, backend):
        super().__init__(backend, reject_first_review=True)
        self.create_requests, self.send_requests = [], []

    async def create(self, child):
        # Capture the actual boundary invocation, independently of intentions.
        manifests = [
            decode_document(raw) for (_, name), raw in self.backend.blobs.items()
            if name.endswith("manifest.json")
        ]
        manifest = next(value for value in manifests
                        if value["children"].get(child.role, {}).get("hosted_id") == child.hosted_id)
        self.create_requests.append(manifest["effect"]["operation_id"])
        await super().create(child)

    async def invoke(self, child, locator, callback):
        self.send_requests.append(locator["operation_id"])
        return await super().invoke(child, locator, callback)


class ScenarioEvidenceTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.fixture_resources = resources = ExitStack()
        # Registered before *any* acquisition/calibration/capture can fail.
        self.addCleanup(resources.close)
        self.clock = ScenarioClock()
        resources.enter_context(patch.object(
            workflow, "time", SimpleNamespace(time=self.clock.time, monotonic=time.monotonic),
        ))
        resources.enter_context(patch.object(routing, "time", SimpleNamespace(time=self.clock.time)))
        resources.enter_context(patch.object(routing, "asyncio", SimpleNamespace(sleep=self.clock.sleep)))
        resources.enter_context(patch.dict(os.environ, {
            "DECISION_REQUESTS_PER_MINUTE": "17",
            "DECISION_MODEL_DEPLOYMENT": "synthetic-decision",
        }))
        self.backend = MemoryBackend()
        self.remote = CapturedRemote(self.backend)
        self.checkpoints = {}
        self.data = {}
        with patch("demo.workflow.DecisionClient", return_value=FakeRouter()), patch(
            "demo.workflow.load_calibration", return_value=synthetic_calibration(),
        ):
            for scenario in ("initial", "followup", "restart"):
                self.data[scenario] = await self.capture(scenario, "parent-one")
            self.data["isolated"] = await self.capture("isolated", "parent-two")
        stop = {
            "schema_version": 1, "parent": "parent-one", "version": "2",
            "phase": "stop_confirmed", "previous_stopped_at": None,
            "stop_http_status": 204, "stopped_at": 1234,
        }
        self.data["restart"]["proof"]["hosting_restart"] = stop
        self.data["restart"]["stops"] = ["parent-one"]
        self.data["stopped_session"] = {
            "agent_session_id": "parent-one", "version_indicator": {"agent_version": "2"},
            "status": "idle", "stopped_at": 1234,
        }

    async def capture(self, scenario, parent):
        runtime = TestRuntime(self.backend, self.remote, parent=parent, response="response-" + scenario)
        storage = self.checkpoints.setdefault(parent, InMemoryCheckpointStorage())
        result = await graph(runtime, storage).run(SCENARIOS[scenario])
        proof = events("\n".join(result.get_outputs()))
        manifest = await make_store(self.backend, runtime.scope, "coordinator").read_manifest()
        operations = [
            decode_document(raw) for (_, name), raw in self.backend.blobs.items()
            if name.startswith(runtime.scope.prefix + "operations/")
        ]
        create_ids = {item["effect"]["operation_id"] for item in operations
                      if item["effect"]["kind"] == "create"}
        call_ids = {item["effect"]["operation_id"] for item in operations
                    if item["effect"]["kind"] == "call"}
        proof.update(
            scenario=scenario, version="2", hosting_restart=None,
            framework={
                "session_id": "framework-" + parent,
                "state": {"foundry_hosted_agent_session_id": parent},
            },
            metadata={role: {"version": "2"} for role in ("coordinator", "architect", "reviewer")},
            child_sessions={
                role: {"agent_session_id": child.hosted_id, "version_indicator": {"agent_version": "2"}}
                for role, child in manifest.children.items()
            },
        )
        return copy.deepcopy({
            "proof": proof, "manifest": manifest.model_dump(mode="json"), "operations": operations,
            "creations": [item for item in self.remote.create_requests if item in create_ids],
            "sends": [item for item in self.remote.send_requests if item in call_ids],
            "checkpoints": {
                "scope_binding": runtime.scope.model_dump(mode="json"),
                "records": json.loads(json.dumps([
                    dataclasses.asdict(item) for item in await storage.list_checkpoints(
                        workflow_name="distributed-agents-v1",
                    )
                ], default=lambda item: item.value)),
            },
        })

    def validate(self, data=None):
        validate_scenario_evidence(**(self.data if data is None else data))

    def reject(self, mutate, code):
        data = copy.deepcopy(self.data)
        mutate(data)
        with self.assertRaisesRegex(RuntimeError, code):
            self.validate(data)

    async def test_actual_offline_graph_captures_pass_including_four_call_revision(self):
        self.assertEqual(len(self.data["initial"]["proof"]["delegations"]), 4)
        self.validate()
        # File contract must round-trip JSON, not depend on live Python objects.
        self.validate(json.loads(json.dumps(self.data)))

    async def test_real_admission_wait_expires_quota_using_only_fixture_time(self):
        backend = MemoryBackend()
        runtime = TestRuntime(backend, None)
        store = make_store(backend, runtime.scope, "coordinator")
        started = self.clock.time()
        waits_before = len(self.clock.waits)
        for operation in ("1" * 32, "2" * 32):
            await routing.reserve_decision(
                store, operation_id=operation, deployment="synthetic",
                limit=1, deadline=self.clock.time() + 65,
            )
        self.assertEqual(self.clock.time() - started, 60)
        self.assertEqual(self.clock.waits[waits_before:], [60])
        state = decode_document(next(iter(backend.blobs.values())))
        self.assertEqual([item["operation_id"] for item in state["reservations"]], ["2" * 32])
        self.assertFalse(backend.leases)

    def change_initial_final_call_prerequisites(self, data, role, input_refs):
        kind = {"architect": "candidate", "reviewer": "review"}[role]
        output_ref = data["initial"]["manifest"][kind]
        operation = next(
            item["effect"]["operation_id"] for item in data["initial"]["operations"]
            if item["effect"]["status"] == "accepted" and item["effect"]["output_ref"] == output_ref
        )
        for scenario in ("initial", "followup", "restart"):
            for item in data[scenario]["operations"]:
                if item["effect"]["operation_id"] == operation:
                    item["effect"]["input_refs"] = copy.deepcopy(input_refs)
            # Keep the final envelopes, hashes and cumulative journal observations
            # internally consistent: only the operation/artifact join contradicts.
            self.assertEqual(data[scenario]["proof"]["result"], self.data[scenario]["proof"]["result"])
            validate_artifact_evidence(data[scenario]["proof"]["result"])

    async def test_final_reviewer_cannot_omit_candidate_in_consistent_journal(self):
        data = copy.deepcopy(self.data)
        self.change_initial_final_call_prerequisites(
            data, "reviewer", [data["initial"]["manifest"]["requirements"]],
        )
        with self.assertRaisesRegex(RuntimeError, "^EVIDENCE_OUTPUT_PREREQUISITES$"):
            self.validate(data)

    async def test_final_reviewer_cannot_use_earlier_same_turn_candidate(self):
        data = copy.deepcopy(self.data)
        manifest = data["initial"]["manifest"]
        earlier = next(
            item["effect"]["output_ref"] for item in data["initial"]["operations"]
            if item["effect"]["status"] == "accepted" and item["effect"]["kind"] == "call"
            and item["effect"]["role"] == "architect"
            and item["effect"]["output_ref"] != manifest["candidate"]
        )
        self.assertIn(earlier, manifest["accepted"])
        self.assertEqual(earlier["requirements_revision"], manifest["turn"])
        self.change_initial_final_call_prerequisites(
            data, "reviewer", [manifest["requirements"], earlier],
        )
        with self.assertRaisesRegex(RuntimeError, "^EVIDENCE_OUTPUT_PREREQUISITES$"):
            self.validate(data)

    async def test_documented_private_json_invocation_passes_and_fails_nonzero(self):
        command = (
            "import json,sys; from demo.terminal import private_state_path; "
            "from live_acceptance import validate_scenario_evidence; "
            "validate_scenario_evidence(**json.loads(private_state_path(sys.argv[1]).read_text(encoding='utf-8'))); "
            "print('Supplied scenario observations passed offline assertions.')"
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "synthetic-evidence.json"
            for valid in (True, False):
                data = copy.deepcopy(self.data)
                if not valid:
                    data["restart"]["sends"].append(data["restart"]["sends"][0])
                path.write_text(json.dumps(data), encoding="utf-8")
                result = subprocess.run(
                    [sys.executable, "-c", command, str(path)],
                    cwd=Path(__file__).resolve().parents[1], capture_output=True, text=True, timeout=60,
                )
                self.assertEqual(result.returncode == 0, valid, result.stderr)
                if valid:
                    self.assertIn("passed offline assertions", result.stdout)
                else:
                    self.assertEqual(result.stdout, "")
                    self.assertIn("EVIDENCE_REQUEST_ACCOUNTING", result.stderr)
                    self.assertNotIn("parent-one", result.stderr)

    async def test_missing_inputs_fail_closed_without_echoing_private_values(self):
        for scenario in ("initial", "followup", "restart", "isolated"):
            for field in ("proof", "manifest", "operations", "sends", "creations"):
                self.reject(lambda data, s=scenario, f=field: data[s].pop(f),
                            "EVIDENCE_MISSING_OR_INVALID")
        for field in ("checkpoints", "stops"):
            self.reject(lambda data, f=field: data["restart"].pop(f), "EVIDENCE_MISSING_OR_INVALID")
        self.reject(lambda data: data.update(stopped_session={}), "EVIDENCE_MISSING_OR_INVALID")
        data = copy.deepcopy(self.data)
        data["initial"]["proof"]["result"].update(status="HELD", private_text="never-echo-this")
        with self.assertRaisesRegex(RuntimeError, "^EVIDENCE_TURN_REJECTED$"):
            self.validate(data)

    async def test_actual_parent_and_both_child_identities_and_versions_are_required(self):
        for role in ("architect", "reviewer"):
            for field in ("hosted_id", "version"):
                self.reject(lambda data, r=role, f=field: data["followup"]["manifest"]["children"][r].update(
                    {f: "drifted-private-value"}
                ), "EVIDENCE_CHILD_BINDING")
            self.reject(lambda data, r=role: data["followup"]["manifest"]["children"][r]["framework"].update(
                session_id="drifted-private-value"
            ), "EVIDENCE_DELEGATION_BINDING")
        self.reject(lambda data: data["followup"]["proof"]["framework"].update(session_id="other-parent"),
                    "EVIDENCE_CONTINUITY")
        self.reject(lambda data: data["followup"]["manifest"].update(active_response_id="response-initial"),
                    "EVIDENCE_CONTINUITY")

    async def test_extra_creations_duplicate_sends_and_unreconciled_effects_fail(self):
        for field in ("creations", "sends"):
            self.reject(lambda data, f=field: data["restart"][f].append(data["restart"][f][0]),
                        "EVIDENCE_REQUEST_ACCOUNTING")
            self.reject(lambda data, f=field: data["restart"][f].pop(), "EVIDENCE_REQUEST_ACCOUNTING")
        def extra_create(data):
            records = data["followup"]["operations"]
            original = next(item for item in records if item["effect"]["kind"] == "create")
            for status in ("prepared", "dispatched", "accepted"):
                item = copy.deepcopy(original)
                item["effect"].update(operation_id="f" * 32, status=status)
                records.append(item)
            data["followup"]["creations"].append("f" * 32)
        self.reject(extra_create, "EVIDENCE_EXACTLY_TWO_CREATIONS")
        self.reject(lambda data: data["restart"]["operations"][0]["effect"].update(status="unknown"),
                    "EVIDENCE_UNRECONCILED_EFFECT|EVIDENCE_INTENT_REQUIRED")

    async def test_stale_approval_and_journal_drift_fail(self):
        self.reject(lambda data: data["followup"]["manifest"].update(
            review=data["initial"]["manifest"]["review"]
        ), "EVIDENCE_MISSING_OR_INVALID")
        self.reject(lambda data: data["followup"]["operations"].pop(), "EVIDENCE_")
        def repeated_response(data):
            calls = [item["effect"] for item in data["followup"]["operations"]
                     if item["effect"]["kind"] == "call" and item["effect"]["status"] == "accepted"]
            changed, previous = calls[-1]["operation_id"], calls[0]["response_id"]
            for item in data["followup"]["operations"]:
                if item["effect"]["operation_id"] == changed and item["effect"]["response_id"]:
                    item["effect"]["response_id"] = previous
        self.reject(repeated_response, "EVIDENCE_FRESH_RESPONSES")
        self.reject(lambda data: data["followup"]["proof"]["delegations"].pop(),
                    "EVIDENCE_TURN_REJECTED")
        self.reject(lambda data: data["restart"]["manifest"].update(
            active_response_id="response-initial"
        ), "EVIDENCE_PARENT_RESPONSE_REUSE")

    async def test_missing_queue_requirement_is_rejected_even_with_current_valid_artifacts(self):
        data = copy.deepcopy(self.data)
        # Produce correctly hashed artifacts/journals for a wrong follow-up brief;
        # do not corrupt hashes merely to make this negative control fail.
        self.backend = MemoryBackend()
        self.remote = CapturedRemote(self.backend)
        self.checkpoints = {}
        with patch("demo.workflow.DecisionClient", return_value=FakeRouter()), patch(
            "demo.workflow.load_calibration", return_value=synthetic_calibration(),
        ), patch.dict(SCENARIOS, {"followup": "Preserve private ingress; omit the queue change."}):
            for scenario in ("initial", "followup", "restart"):
                data[scenario] = await self.capture(scenario, "parent-one")
        data["restart"]["proof"]["hosting_restart"] = self.data["restart"]["proof"]["hosting_restart"]
        data["restart"]["stops"] = ["parent-one"]
        with self.assertRaisesRegex(RuntimeError, "EVIDENCE_SYNTHETIC_REQUIREMENTS"):
            self.validate(data)

    async def test_stop_confirmation_once_only_and_checkpoint_retention_fail_closed(self):
        for change in (
            {"phase": "stop_pending"}, {"parent": "other-parent"}, {"version": "3"},
            {"stop_http_status": 200}, {"stopped_at": float("nan")},
            {"previous_stopped_at": 1234},
        ):
            self.reject(lambda data, c=change: data["restart"]["proof"]["hosting_restart"].update(c),
                        "EVIDENCE_CONFIRMED_STOP")
        self.reject(lambda data: data["stopped_session"].update(status="active"),
                    "EVIDENCE_CONFIRMED_STOP")
        self.reject(lambda data: data["restart"]["stops"].append("parent-one"), "EVIDENCE_ONCE_ONLY_STOP")
        self.reject(lambda data: data["followup"]["checkpoints"].update(records=[]),
                    "EVIDENCE_CHECKPOINT_RECONCILIATION")
        self.reject(lambda data: data["restart"]["checkpoints"]["records"][0].update(state={"corrupted": True}),
                    "EVIDENCE_CHECKPOINT_RECONCILIATION")
        self.reject(lambda data: data["restart"].update(checkpoints=data["followup"]["checkpoints"]),
                    "EVIDENCE_CHECKPOINT_RECONCILIATION")
        self.reject(lambda data: data["restart"]["checkpoints"].update(
            scope_binding=data["isolated"]["manifest"]["scope_binding"]
        ), "EVIDENCE_CHECKPOINT_SCOPE")

    async def test_isolation_content_scope_and_release_drift_fail(self):
        self.reject(lambda data: data["isolated"]["proof"]["framework"].update(session_id="framework-parent-one"),
                    "EVIDENCE_PARENT_ISOLATION")
        self.reject(lambda data: data["isolated"]["operations"][0].update(
            scope_binding=data["initial"]["manifest"]["scope_binding"]
        ), "EVIDENCE_OPERATION_SCOPE")
        self.reject(lambda data: data["isolated"]["proof"]["metadata"]["coordinator"].update(
            diagnostic_only=True
        ), "EVIDENCE_RELEASE_DRIFT")

    async def test_valid_hashed_but_leaked_isolated_content_is_rejected(self):
        original = CapturedRemote.output_content
        for role, field in (("architect", "design"), ("reviewer", "recommendation")):
            def contaminated(remote, child, assignment):
                result = original(remote, child, assignment)
                return result.model_copy(update={field: "Project Harbor asynchronous queue"}) \
                    if child.role == role else result
            with patch("demo.workflow.DecisionClient", return_value=FakeRouter()), patch(
                "demo.workflow.load_calibration", return_value=synthetic_calibration(),
            ), patch.object(CapturedRemote, "output_content", contaminated):
                data = copy.deepcopy(self.data)
                data["isolated"] = await self.capture("isolated", "leaked-" + role)
            with self.assertRaisesRegex(RuntimeError, "EVIDENCE_CONTENT_LEAK"):
                self.validate(data)


class ScenarioSettingsTests(unittest.TestCase):
    def assert_clock_bindings(self, before):
        for actual, expected in zip(clock_bindings(), before):
            self.assertIs(actual, expected)

    def test_all_captures_own_settings_and_restore_ambient_values_and_absence(self):
        for ambient in (None, ("invalid", ""), ("1", "ambient-decision")):
            with self.subTest(ambient=ambient), patch.dict(os.environ):
                names = ("DECISION_REQUESTS_PER_MINUTE", "DECISION_MODEL_DEPLOYMENT")
                for index, name in enumerate(names):
                    if ambient is None:
                        os.environ.pop(name, None)
                    else:
                        os.environ[name] = ambient[index]
                before = dict(os.environ)
                clocks_before = clock_bindings()
                captures = []
                original = ScenarioEvidenceTests.capture

                async def checked_capture(fixture, scenario, parent):
                    self.assertIs(workflow.time.time.__self__, fixture.clock)
                    self.assertIs(routing.time.time.__self__, fixture.clock)
                    self.assertEqual(clock_bindings()[3:], clocks_before[3:])
                    self.assertIs(workflow.time.monotonic, time.monotonic)
                    self.assertEqual(
                        tuple(os.environ[name] for name in names),
                        ("17", "synthetic-decision"),
                    )
                    captures.append(scenario)
                    return await original(fixture, scenario, parent)

                with patch.object(ScenarioEvidenceTests, "capture", checked_capture):
                    result = unittest.TestResult()
                    ScenarioEvidenceTests(
                        "test_actual_offline_graph_captures_pass_including_four_call_revision"
                    ).run(result)
                self.assertTrue(result.wasSuccessful(), result.errors + result.failures)
                self.assertEqual(captures, ["initial", "followup", "restart", "isolated"])
                self.assertEqual(dict(os.environ), before)
                self.assert_clock_bindings(clocks_before)

    def test_setup_failure_restores_settings_before_and_during_capture(self):
        for ambient in (None, ("invalid", "ambient-decision")):
            for failure in ("calibration", "initial", "followup", "restart", "isolated"):
                with self.subTest(ambient=ambient, failure=failure), patch.dict(os.environ):
                    names = ("DECISION_REQUESTS_PER_MINUTE", "DECISION_MODEL_DEPLOYMENT")
                    for index, name in enumerate(names):
                        if ambient is None:
                            os.environ.pop(name, None)
                        else:
                            os.environ[name] = ambient[index]
                    before = dict(os.environ)
                    clocks_before = clock_bindings()
                    original = ScenarioEvidenceTests.capture
                    original_calibration = synthetic_calibration

                    def calibration():
                        self.assertEqual(
                            tuple(os.environ[name] for name in names),
                            ("17", "synthetic-decision"),
                        )
                        if failure == "calibration":
                            raise RuntimeError("SYNTHETIC_SETUP_FAILURE")
                        return original_calibration()

                    async def capture(fixture, scenario, parent):
                        if scenario == failure:
                            raise RuntimeError("SYNTHETIC_SETUP_FAILURE")
                        return await original(fixture, scenario, parent)

                    with patch(__name__ + ".synthetic_calibration", side_effect=calibration), \
                         patch.object(ScenarioEvidenceTests, "capture", capture):
                        result = unittest.TestResult()
                        ScenarioEvidenceTests(
                            "test_actual_offline_graph_captures_pass_including_four_call_revision"
                        ).run(result)
                    self.assertEqual(len(result.errors), 1, result.errors)
                    self.assertIn("SYNTHETIC_SETUP_FAILURE", result.errors[0][1])
                    self.assertFalse(result.failures)
                    self.assertEqual(dict(os.environ), before)
                    self.assert_clock_bindings(clocks_before)

    def test_nested_setup_restores_outer_clock_and_environment_after_success_and_failures(self):
        before, clocks_before = dict(os.environ), clock_bindings()

        async def exercise():
            outer = ScenarioEvidenceTests()
            try:
                await outer.asyncSetUp()
                outer.validate()
                outer_environment, outer_clocks = dict(os.environ), clock_bindings()
                original_capture = ScenarioEvidenceTests.capture
                original_calibration = synthetic_calibration
                for failure in (None, "calibration", "initial", "followup", "restart", "isolated"):
                    with self.subTest(failure=failure):
                        inner = ScenarioEvidenceTests()

                        def calibration():
                            self.assertIs(workflow.time.time.__self__, inner.clock)
                            self.assertIsNot(inner.clock, outer.clock)
                            if failure == "calibration":
                                raise RuntimeError("SYNTHETIC_SETUP_FAILURE")
                            return original_calibration()

                        async def capture(fixture, scenario, parent):
                            if scenario == failure:
                                raise RuntimeError("SYNTHETIC_SETUP_FAILURE")
                            return await original_capture(fixture, scenario, parent)

                        try:
                            with patch(__name__ + ".synthetic_calibration", side_effect=calibration), \
                                 patch.object(ScenarioEvidenceTests, "capture", capture):
                                if failure is None:
                                    await inner.asyncSetUp()
                                    inner.validate()
                                else:
                                    with self.assertRaisesRegex(RuntimeError, "^SYNTHETIC_SETUP_FAILURE$"):
                                        await inner.asyncSetUp()
                        finally:
                            # We directly await setup inside the outer event loop,
                            # not a second IsolatedAsyncioTestCase runner. Close its
                            # registered scope directly; normal-runner failure
                            # cleanup is covered by the tests above.
                            inner.fixture_resources.close()
                        self.assertEqual(dict(os.environ), outer_environment)
                        self.assert_clock_bindings(outer_clocks)
                # Continue a real outer capture after nested clocks have been removed.
                with patch("demo.workflow.DecisionClient", return_value=FakeRouter()), patch(
                    "demo.workflow.load_calibration", return_value=synthetic_calibration(),
                ):
                    await outer.capture("isolated", "outer-after-nesting")
            finally:
                outer.fixture_resources.close()

        asyncio.run(exercise())
        self.assertEqual(dict(os.environ), before)
        self.assert_clock_bindings(clocks_before)

    def test_synthetic_waits_advance_only_owned_time_and_fail_closed_at_bounds(self):
        clock = ScenarioClock()
        before = clock_bindings()
        asyncio.run(clock.sleep(60))
        self.assertEqual(clock.time(), clock.epoch + 60)
        self.assertEqual(clock.waits, [60])
        for delay in (0, -1, 66, float("nan"), float("inf")):
            with self.subTest(delay=delay), self.assertRaisesRegex(AssertionError, "CLOCK_WAIT_LIMIT"):
                asyncio.run(clock.sleep(delay))
        clock.now = clock.epoch + 600
        with self.assertRaisesRegex(AssertionError, "CLOCK_WAIT_LIMIT"):
            asyncio.run(clock.sleep(1))
        clock.reads = 10_000
        with self.assertRaisesRegex(AssertionError, "CLOCK_READ_LIMIT"):
            clock.time()
        self.assert_clock_bindings(before)


if __name__ == "__main__":
    unittest.main()
