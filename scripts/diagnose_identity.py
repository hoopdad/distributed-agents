from __future__ import annotations

import argparse
import importlib.metadata
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
ROLES = frozenset({"coordinator", "architect", "reviewer"})
PROBES = {
    "native_http_boundary": "NativeWorkflowTests.test_native_resources_forward_sdk_context_without_redelegating_platform_user",
    "durable_identity": "LiveObservationTests.test_pinned_sdk_resilient_identity_survives_serialization_and_handler_entry",
    "missing_principal_gate": "LiveObservationTests.test_sdk_preparation_filter_reports_only_missing_trusted_scope",
    "wire_diagnostic_redaction": "NativeOutboundTransportTests.test_outbound_context_reports_wire_presence_and_matches_without_values",
    "exact_origin": "NativeOutboundTransportTests.test_outbound_diagnostics_exclude_unrelated_requests_and_reject_other_origins",
}
CHILD_PROBE = """
import contextlib, io, json, sys, unittest
names = json.loads(sys.argv[1])
captured = io.StringIO()
with contextlib.redirect_stdout(captured), contextlib.redirect_stderr(captured):
    suite = unittest.defaultTestLoader.loadTestsFromNames(list(names.values()))
    result = unittest.TextTestRunner(stream=captured).run(suite)
failed = {test.id() for test, _ in result.errors + result.failures}
skipped = {test.id() for test, _ in result.skipped}
valid = result.testsRun == len(names)
print(json.dumps({
    "passed": valid and result.wasSuccessful() and not skipped,
    "tests_run": result.testsRun,
    "probes": {key: ("failed" if name in failed else "skipped" if name in skipped
                     else "passed" if valid and not failed else "inconclusive")
               for key, name in names.items()},
}))
"""


class DiagnosticError(ValueError):
    pass


def check_pins(path: Path) -> list[dict]:
    try:
        from packaging.requirements import InvalidRequirement, Requirement
    except ImportError as exc:
        raise DiagnosticError("LOCK_PARSER_UNAVAILABLE") from exc
    pins = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith(("#", "--index-url ")):
            continue
        try:
            requirement = Requirement(line)
        except InvalidRequirement as exc:
            raise DiagnosticError("LOCK_FORMAT_INVALID") from exc
        specifiers = list(requirement.specifier)
        if (
            requirement.url or requirement.extras or len(specifiers) != 1
            or specifiers[0].operator != "==" or "*" in specifiers[0].version
        ):
            raise DiagnosticError("LOCK_FORMAT_INVALID")
        name, expected = requirement.name, specifiers[0].version
        normalized = re.sub(r"[-_.]+", "-", name).lower()
        if normalized in pins:
            raise DiagnosticError("LOCK_DUPLICATE_PIN")
        pins[normalized] = (expected, requirement.marker is None or requirement.marker.evaluate())
    if not pins:
        raise DiagnosticError("LOCK_EMPTY")
    results = []
    for name, (expected, applies) in sorted(pins.items()):
        if not applies:
            results.append({
                "distribution": name, "expected": expected, "installed": None,
                "applies": False, "matches": True,
            })
            continue
        try:
            installed = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            installed = None
        results.append({
            "distribution": name, "expected": expected, "installed": installed,
            "applies": True, "matches": installed == expected,
        })
    return results


def offline_probes() -> dict:
    environment = dict(os.environ)
    environment.update({
        "FOUNDRY_PROJECT_ENDPOINT": "https://example.services.ai.azure.com/api/projects/example-project",
        "SPECIALIST_MODEL_DEPLOYMENT": "synthetic-worker",
        "DECISION_MODEL_DEPLOYMENT": "synthetic-decision",
        "OTEL_SDK_DISABLED": "true", "PYTHONWARNINGS": "ignore",
    })
    environment["PYTHONPATH"] = os.pathsep.join((str(ROOT), str(ROOT / "tests")))
    names = {key: "test_workflow." + name for key, name in PROBES.items()}
    try:
        result = subprocess.run(
            [sys.executable, "-B", "-c", CHILD_PROBE, json.dumps(names)],
            cwd=ROOT, env=environment, capture_output=True, timeout=120,
        )
    except subprocess.TimeoutExpired:
        return {"passed": False, "classification": "OFFLINE_PROBE_TIMEOUT"}
    if result.returncode:
        return {"passed": False, "classification": "OFFLINE_PROBE_PROCESS_FAILED"}
    try:
        value = json.loads(result.stdout)
    except (ValueError, UnicodeError):
        return {"passed": False, "classification": "OFFLINE_PROBE_REPORT_INVALID"}
    if (
        not isinstance(value, dict) or type(value.get("passed")) is not bool
        or type(value.get("tests_run")) is not int or value["tests_run"] != len(PROBES)
        or not isinstance(value.get("probes"), dict) or set(value["probes"]) != set(PROBES)
        or any(status not in ("passed", "failed", "skipped", "inconclusive")
               for status in value["probes"].values())
        or value["passed"] != all(status == "passed" for status in value["probes"].values())
    ):
        return {"passed": False, "classification": "OFFLINE_PROBE_REPORT_INVALID"}
    return value


def unique_pairs(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise DiagnosticError("TRACE_DUPLICATE_KEY")
        value[key] = item
    return value


def read_trace(path: Path) -> dict:
    with path.open("rb") as stream:
        raw = stream.read(131073)
    if len(raw) > 131072:
        raise DiagnosticError("TRACE_BYTE_LIMIT")
    try:
        value = json.loads(raw, object_pairs_hook=unique_pairs)
    except DiagnosticError:
        raise
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise DiagnosticError("TRACE_JSON_INVALID") from exc
    if not isinstance(value, dict) or type(value.get("schema_version")) is not int or value["schema_version"] != 1:
        raise DiagnosticError("TRACE_SCHEMA_INVALID")
    if "error" in value:
        raise DiagnosticError("TRACE_SOURCE_REJECTED")
    if type(value.get("correlation_verified", False)) is not bool:
        raise DiagnosticError("TRACE_CORRELATION_INVALID")
    sanitized = {"schema_version": 1, "correlation_verified": value.get("correlation_verified", False)}
    fields = {
        "observations": ("has_user_id", "has_call_id"),
        "outbound": ("has_call_id", "call_matches_context", "has_delegated_user", "has_container_user"),
    }
    for section, flags in fields.items():
        items = value.get(section, [])
        if not isinstance(items, list) or len(items) > 32:
            raise DiagnosticError("TRACE_ROWS_INVALID")
        sanitized[section] = []
        for item in items:
            if (
                not isinstance(item, dict) or not isinstance(item.get("role"), str) or item["role"] not in ROLES
                or type(item.get("exact_response_bound")) is not bool
                or any(type(item.get(flag)) is not bool for flag in flags)
            ):
                raise DiagnosticError("TRACE_FLAGS_INVALID")
            if section == "outbound" and item["call_matches_context"] and not item["has_call_id"]:
                raise DiagnosticError("TRACE_FLAGS_INCONSISTENT")
            sanitized[section].append({
                "role": item["role"], "exact_response_bound": item["exact_response_bound"],
                **{flag: item[flag] for flag in flags},
            })
    metadata = value.get("deployment_metadata", [])
    if not isinstance(metadata, list) or len(metadata) > len(ROLES):
        raise DiagnosticError("TRACE_METADATA_INVALID")
    sanitized["deployment_metadata"] = []
    seen = set()
    for row in metadata:
        flags = ("package_matches_expected", "identity_matches_baseline", "closure_proven")
        if (
            not isinstance(row, dict) or not isinstance(row.get("role"), str)
            or row["role"] not in ROLES or row["role"] in seen
            or row.get("source") != "exact_version_metadata"
            or not isinstance(row.get("version"), str)
            or not re.fullmatch(r"[1-9][0-9]{0,8}", row["version"])
            or not isinstance(row.get("responses_protocol"), str)
            or not re.fullmatch(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", row["responses_protocol"])
            or row.get("status") not in ("active", "failed", "inactive", "creating")
            or type(row.get("http_status")) is not int or not 100 <= row["http_status"] <= 599
            or any(type(row.get(flag)) is not bool for flag in flags)
        ):
            raise DiagnosticError("TRACE_METADATA_INVALID")
        seen.add(row["role"])
        sanitized["deployment_metadata"].append({
            key: row[key] for key in ("role", "version", "responses_protocol", "status", "http_status", *flags)
        })
    if "parent_project_endpoint_captured" in value:
        if type(value["parent_project_endpoint_captured"]) is not bool:
            raise DiagnosticError("TRACE_PROJECT_BINDING_INVALID")
        sanitized["parent_project_endpoint_captured"] = value["parent_project_endpoint_captured"]
    return sanitized


def analyze(pins: list[dict], probes: dict, trace: dict | None) -> dict:
    findings = []
    if not all(pin["matches"] for pin in pins):
        findings.append("INSTALLED_RUNTIME_DIFFERS_FROM_LOCK")
    if not probes.get("passed"):
        findings.append("OFFLINE_IDENTITY_CONTRACT_NOT_VERIFIED")
    metadata = trace.get("deployment_metadata", []) if trace else []
    if any(row["responses_protocol"] != "2.0.0" for row in metadata):
        findings.append("DEPLOYED_RESPONSES_PROTOCOL_MISMATCH")
    elif {row["role"] for row in metadata} == ROLES and all(
        row["http_status"] == 200 and row["status"] == "active"
        and row["package_matches_expected"] and row["identity_matches_baseline"] and row["closure_proven"]
        for row in metadata
    ):
        findings.append("DEPLOYED_VERSIONS_ACTIVE_PROTOCOL_2")
    else:
        findings.append("DEPLOYED_PROTOCOL_METADATA_INCOMPLETE_OR_UNHEALTHY")
    if trace and trace.get("parent_project_endpoint_captured") is False:
        findings.append("PARENT_PROJECT_ENDPOINT_NOT_CAPTURED")
    observations = trace["observations"] if trace else []
    conflicts = {
        role for role in ROLES
        if len({(row["has_user_id"], row["has_call_id"]) for row in observations
                if row["role"] == role and row["exact_response_bound"]}) > 1
    }
    if conflicts:
        findings.append("CONFLICTING_INGRESS_OBSERVATIONS")
    parent = any(
        row["role"] == "coordinator" and row["role"] not in conflicts and row["exact_response_bound"]
        and row["has_user_id"] and row["has_call_id"] for row in observations
    )
    children = [
        row for row in observations
        if row["role"] in ("architect", "reviewer") and row["role"] not in conflicts and row["exact_response_bound"]
        and row["has_call_id"] and not row["has_user_id"]
    ]
    correlated = trace is not None and trace.get("correlation_verified") is True
    if children:
        findings.append("TRUSTED_USER_MISSING_AT_CHILD_INGRESS")
        if probes.get("passed"):
            findings.append("OFFLINE_DURABLE_CONTEXT_PRESERVES_SUPPLIED_IDENTITY")
    if parent and children and correlated:
        findings.append("PARENT_IDENTITY_PRESENT_CHILD_IDENTITY_ABSENT")
    if not any(row["exact_response_bound"] for row in observations):
        findings.append("EXACT_RESPONSE_INGRESS_NOT_CAPTURED")
    if observations and not correlated:
        findings.append("PARENT_CHILD_CORRELATION_NOT_VERIFIED")
    outbound = trace["outbound"] if trace else []
    matching_wire = correlated and any(
        wire["role"] == child["role"] and wire["exact_response_bound"]
        and wire["has_call_id"] and wire["call_matches_context"]
        and not wire["has_delegated_user"] and not wire["has_container_user"]
        for wire in outbound for child in children
    )
    if not matching_wire:
        findings.append("LIVE_MATCHING_CALL_ID_NOT_CAPTURED")
    if parent and children and matching_wire:
        findings.append("SUPPORTED_CALL_ID_OBSERVED_BEFORE_MISSING_CHILD_USER")
    if conflicts:
        next_discriminator = "CORRELATE_INGRESS_WITH_DURABLE_TASK_REENTRY"
    elif parent and children and matching_wire:
        next_discriminator = "CORRELATE_PLATFORM_CALL_RESOLUTION_FOR_EXACT_PARENT_AND_CHILD"
    elif parent and children and correlated:
        next_discriminator = "CAPTURE_EXACT_PARENT_OUTBOUND_CALL_PRESENCE_AND_CONTEXT_MATCH"
    elif children and correlated:
        next_discriminator = "CAPTURE_EXACT_PARENT_INGRESS_AND_OUTBOUND_CONTEXT"
    else:
        next_discriminator = "OBSERVE_EXACT_PRESERVED_PARENT_AND_CHILD_INGRESS"
    return {
        "findings": findings,
        "live_root_cause": "NOT_ESTABLISHED",
        "next_discriminator": next_discriminator,
        "authorization": {
            "publication_retry": False, "inference_retry": False,
            "principal_substitution": False, "permission_change": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Offline identity probes and sanitized evidence analysis; no cloud calls.")
    parser.add_argument("--trace", type=Path, help="Explicit sanitized exact-response trace JSON; never raw logs or state.")
    args = parser.parse_args()
    try:
        pins = check_pins(ROOT / "requirements.lock.txt")
        probes = offline_probes()
        trace = read_trace(args.trace) if args.trace else None
        offline_verified = all(pin["matches"] for pin in pins) and probes.get("passed") is True
        report = {
            "schema_version": 1, "mode": "READ_ONLY_OFFLINE",
            "status": "OFFLINE_VERIFIED_LIVE_UNRESOLVED" if offline_verified else "OFFLINE_VERIFICATION_FAILED",
            "pins": pins, "offline": probes, "trace": trace,
            "analysis": analyze(pins, probes, trace),
        }
        print(json.dumps(report, sort_keys=True))
        return 2 if offline_verified else 1
    except DiagnosticError as exc:
        print(json.dumps({"schema_version": 1, "error": str(exc)}))
        return 2
    except OSError:
        print(json.dumps({"schema_version": 1, "error": "DIAGNOSTIC_IO_FAILED"}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
