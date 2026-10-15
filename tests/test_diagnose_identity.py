from __future__ import annotations

import importlib.metadata
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
from contextlib import redirect_stdout

from scripts import diagnose_identity as diagnostic


class IdentityDiagnosticTests(unittest.TestCase):
    def test_pins_report_missing_and_mismatch_without_installing(self):
        with tempfile.TemporaryDirectory() as directory:
            lock = Path(directory) / "requirements.lock.txt"
            lock.write_text("--index-url https://example.invalid/simple\nexample==1.0\nmissing==2.0\n", encoding="utf-8")
            with patch.object(importlib.metadata, "version", side_effect=[
                "0.9", importlib.metadata.PackageNotFoundError("missing"),
            ]):
                pins = diagnostic.check_pins(lock)
        self.assertEqual([pin["matches"] for pin in pins], [False, False])
        self.assertIsNone(pins[1]["installed"])

    def test_duplicate_or_unpinned_lock_is_rejected(self):
        for content in ("example>=1.0\n", "example==1.*\n", "example==1\nExample==1\n", ""):
            with self.subTest(content=content), tempfile.TemporaryDirectory() as directory:
                lock = Path(directory) / "lock.txt"
                lock.write_text(content, encoding="utf-8")
                with self.assertRaises(diagnostic.DiagnosticError):
                    diagnostic.check_pins(lock)

    def test_inapplicable_platform_pin_is_not_a_missing_dependency(self):
        with tempfile.TemporaryDirectory() as directory:
            lock = Path(directory) / "lock.txt"
            lock.write_text('example==1.0; sys_platform == "never-platform"\n', encoding="utf-8")
            with patch.object(importlib.metadata, "version") as version:
                pins = diagnostic.check_pins(lock)
            version.assert_not_called()
        self.assertFalse(pins[0]["applies"])
        self.assertTrue(pins[0]["matches"])

    def test_trace_sanitizes_unknown_values(self):
        raw = {
            "schema_version": 1, "private": "synthetic-private",
            "observations": [{
                "role": "architect", "has_user_id": False, "has_call_id": True,
                "exact_response_bound": True, "private": "synthetic-private",
            }],
        }
        with tempfile.TemporaryDirectory() as directory:
            trace = Path(directory) / "trace.json"
            trace.write_text(json.dumps(raw), encoding="utf-8")
            report = diagnostic.read_trace(trace)
        self.assertNotIn("synthetic-private", json.dumps(report))

    def test_exact_deployment_metadata_is_sanitized_and_analyzed(self):
        trace = {
            "schema_version": 1, "parent_project_endpoint_captured": False,
            "deployment_metadata": [{
                "role": role, "version": "1", "source": "exact_version_metadata",
                "responses_protocol": "2.0.0", "status": "active", "http_status": 200,
                "package_matches_expected": True, "identity_matches_baseline": True,
                "closure_proven": True, "private": "synthetic-private",
            } for role in sorted(diagnostic.ROLES)],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "trace.json"
            path.write_text(json.dumps(trace), encoding="utf-8")
            clean = diagnostic.read_trace(path)
            self.assertNotIn("synthetic-private", json.dumps(clean))
            report = diagnostic.analyze([{"matches": True}], {"passed": True}, clean)
            self.assertIn("DEPLOYED_VERSIONS_ACTIVE_PROTOCOL_2", report["findings"])
            self.assertIn("PARENT_PROJECT_ENDPOINT_NOT_CAPTURED", report["findings"])
            trace["deployment_metadata"][0]["closure_proven"] = "true"
            path.write_text(json.dumps(trace), encoding="utf-8")
            with self.assertRaises(diagnostic.DiagnosticError):
                diagnostic.read_trace(path)

    def test_protocol_mismatch_is_not_masked_by_other_healthy_roles(self):
        trace = self.trace()
        trace["deployment_metadata"] = [{"role": "architect", "responses_protocol": "1.0.0"}]
        report = diagnostic.analyze([{"matches": True}], {"passed": True}, trace)
        self.assertIn("DEPLOYED_RESPONSES_PROTOCOL_MISMATCH", report["findings"])
        self.assertNotIn("DEPLOYED_VERSIONS_ACTIVE_PROTOCOL_2", report["findings"])

    def test_trace_rejects_duplicates_oversize_and_truthy_nonbooleans(self):
        cases = [
            '{"schema_version":1,"schema_version":1}',
            '{"schema_version":1,"error":"synthetic-private"}',
            " " * 131073,
            json.dumps({"schema_version": 1, "observations": [{
                "role": "architect", "has_user_id": "false", "has_call_id": True,
                "exact_response_bound": True,
            }]}),
            json.dumps({"schema_version": 1, "observations": [{
                "role": [], "has_user_id": False, "has_call_id": True,
                "exact_response_bound": True,
            }]}),
        ]
        with tempfile.TemporaryDirectory() as directory:
            trace = Path(directory) / "trace.json"
            for raw in cases:
                with self.subTest(size=len(raw)):
                    trace.write_text(raw, encoding="utf-8")
                    with self.assertRaises(diagnostic.DiagnosticError):
                        diagnostic.read_trace(trace)

    def trace(self, bound=True, outbound=False):
        return {
            "correlation_verified": True,
            "observations": [
                {"role": "coordinator", "has_user_id": True, "has_call_id": True, "exact_response_bound": bound},
                {"role": "architect", "has_user_id": False, "has_call_id": True, "exact_response_bound": bound},
            ],
            "outbound": [{
                "role": "architect", "has_call_id": True, "call_matches_context": True,
                "has_delegated_user": False, "has_container_user": False, "exact_response_bound": True,
            }] if outbound else [],
        }

    def test_ingress_evidence_does_not_prove_outbound_or_platform_bug(self):
        report = diagnostic.analyze([{"matches": True}], {"passed": True}, self.trace())
        self.assertIn("TRUSTED_USER_MISSING_AT_CHILD_INGRESS", report["findings"])
        self.assertIn("LIVE_MATCHING_CALL_ID_NOT_CAPTURED", report["findings"])
        self.assertEqual(report["live_root_cause"], "NOT_ESTABLISHED")
        self.assertFalse(any(report["authorization"].values()))

    def test_unbound_observations_are_not_accepted_as_live_proof(self):
        report = diagnostic.analyze([{"matches": True}], {"passed": True}, self.trace(bound=False))
        self.assertNotIn("TRUSTED_USER_MISSING_AT_CHILD_INGRESS", report["findings"])

    def test_unrelated_exact_observations_cannot_establish_a_call_chain(self):
        trace = self.trace(outbound=True)
        trace["correlation_verified"] = False
        report = diagnostic.analyze([{"matches": True}], {"passed": True}, trace)
        self.assertIn("TRUSTED_USER_MISSING_AT_CHILD_INGRESS", report["findings"])
        self.assertNotIn("PARENT_IDENTITY_PRESENT_CHILD_IDENTITY_ABSENT", report["findings"])
        self.assertEqual(report["next_discriminator"], "OBSERVE_EXACT_PRESERVED_PARENT_AND_CHILD_INGRESS")
        self.assertIn("PARENT_CHILD_CORRELATION_NOT_VERIFIED", report["findings"])
        self.assertNotIn("SUPPORTED_CALL_ID_OBSERVED_BEFORE_MISSING_CHILD_USER", report["findings"])

    def test_matching_wire_changes_discriminator_but_not_retry_authority(self):
        report = diagnostic.analyze([{"matches": True}], {"passed": True}, self.trace(outbound=True))
        self.assertEqual(report["next_discriminator"], "CORRELATE_PLATFORM_CALL_RESOLUTION_FOR_EXACT_PARENT_AND_CHILD")
        self.assertEqual(report["live_root_cause"], "NOT_ESTABLISHED")
        self.assertFalse(any(report["authorization"].values()))

    def test_conflicting_ingress_is_not_misreported_as_a_platform_boundary(self):
        trace = self.trace(outbound=True)
        trace["observations"].append({
            "role": "architect", "has_user_id": True, "has_call_id": True, "exact_response_bound": True,
        })
        report = diagnostic.analyze([{"matches": True}], {"passed": True}, trace)
        self.assertIn("CONFLICTING_INGRESS_OBSERVATIONS", report["findings"])
        self.assertNotIn("SUPPORTED_CALL_ID_OBSERVED_BEFORE_MISSING_CHILD_USER", report["findings"])
        self.assertEqual(report["next_discriminator"], "CORRELATE_INGRESS_WITH_DURABLE_TASK_REENTRY")

    def test_child_ingress_is_reported_without_inventing_parent_observation(self):
        trace = self.trace()
        trace["observations"] = trace["observations"][1:]
        report = diagnostic.analyze([{"matches": True}], {"passed": True}, trace)
        self.assertIn("TRUSTED_USER_MISSING_AT_CHILD_INGRESS", report["findings"])
        self.assertNotIn("PARENT_IDENTITY_PRESENT_CHILD_IDENTITY_ABSENT", report["findings"])
        self.assertEqual(report["next_discriminator"], "CAPTURE_EXACT_PARENT_INGRESS_AND_OUTBOUND_CONTEXT")

    def test_probe_process_never_echoes_failure_payload(self):
        private = b"synthetic-private-error"
        with patch.object(subprocess, "run", return_value=subprocess.CompletedProcess([], 1, private, private)):
            result = diagnostic.offline_probes()
        self.assertEqual(result, {"passed": False, "classification": "OFFLINE_PROBE_PROCESS_FAILED"})
        self.assertNotIn("synthetic-private", json.dumps(result))

    def test_probe_process_timeout_and_malformed_result_are_explicit(self):
        with patch.object(subprocess, "run", side_effect=subprocess.TimeoutExpired("probe", 120)):
            self.assertEqual(diagnostic.offline_probes()["classification"], "OFFLINE_PROBE_TIMEOUT")
        for output in (b"not-json", b'{"passed":true,"tests_run":0,"probes":{}}'):
            with self.subTest(output=output), patch.object(
                subprocess, "run", return_value=subprocess.CompletedProcess([], 0, output, b""),
            ):
                self.assertEqual(diagnostic.offline_probes()["classification"], "OFFLINE_PROBE_REPORT_INVALID")

    def test_offline_success_does_not_return_live_success(self):
        output = io.StringIO()
        with patch("sys.argv", ["diagnose_identity.py"]), \
                patch.object(diagnostic, "check_pins", return_value=[{"matches": True}]), \
                patch.object(diagnostic, "offline_probes", return_value={"passed": True}), \
                redirect_stdout(output):
            code = diagnostic.main()
        self.assertEqual(code, 2)
        report = json.loads(output.getvalue())
        self.assertEqual(report["status"], "OFFLINE_VERIFIED_LIVE_UNRESOLVED")
        self.assertEqual(report["analysis"]["live_root_cause"], "NOT_ESTABLISHED")


if __name__ == "__main__":
    unittest.main()
