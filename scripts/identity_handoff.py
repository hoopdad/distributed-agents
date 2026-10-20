"""Offline-only A/B candidate handoff. Never imported by the hosted runtime.

This exercises client plumbing, not Foundry caller resolution or authorization.
It intentionally has no live mode and cannot select a remediation path.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import diagnose_identity as diagnostic

PROBES = {
    "lifecycle_A_B_both_roles": "CandidateLifecycleTests.test_both_paths_cover_raw_and_responses_lifecycle",
    "omitted_invalid_identity": "CandidateHeaderTests.test_omitted_invalid_or_call_identity_is_rejected",
    "forged_or_cross_parent_binding": "CandidateHeaderTests.test_forged_or_cross_parent_binding_is_rejected",
    "isolated_header_copy": "CandidateHeaderTests.test_candidate_does_not_change_shared_parent_headers",
    "container_header_rejection": "CandidateHeaderTests.test_unexpected_platform_headers_are_rejected",
    "actual_receiver_namespace_and_scope": "CandidateReceiverTests.test_actual_receiver_requires_same_principal_and_parent",
    "failed_retrieval_no_resend": "CandidateLifecycleTests.test_failed_exact_retrieval_does_not_send_or_create",
    "cli_fail_closed": "CandidateCommandTests.test_invalid_roots_or_versions_fail_without_private_output",
    "offline_success_never_selects": "CandidateCommandTests.test_verified_offline_report_stays_unresolved",
}


def candidate_headers(path: str, *, config, context, scope) -> dict[str, str]:
    """Review candidate only: caller must supply authenticated host context.

    Do not call with assignment/client/model-supplied identity. Equality here
    cannot establish that arbitrary Python objects came from a trusted host.
    A live discriminator must additionally measure the child receiver's actual
    principal. No current runtime code calls this function.
    """
    from demo.artifacts import ScopeBinding

    if path not in ("A", "B"):
        raise ValueError("CANDIDATE_PATH")
    trusted = ScopeBinding.from_platform(
        config, context, project=config.project_endpoint, tenant=scope.tenant,
    )
    if trusted != scope:
        raise ValueError("CANDIDATE_PARENT_BINDING")
    headers = dict(context.platform_headers())
    if (
        set(headers) != {"x-agent-foundry-call-id"}
        or headers["x-agent-foundry-call-id"] != context.call_id
    ):
        raise ValueError("CANDIDATE_PLATFORM_HEADERS")
    if path == "B":
        # Documented syntax is necessary but does not prove principal-namespace
        # compatibility. Never derive the user from the opaque call context.
        if (
            not re.fullmatch(r"[A-Za-z0-9._:@-]{1,256}", context.user_id)
            or context.user_id == context.call_id
        ):
            raise ValueError("CANDIDATE_DELEGATED_IDENTITY")
        headers["x-ms-user-identity"] = context.user_id
    return headers


def offline_probes() -> dict:
    # Reuse the bounded/redacted child harness, but keep the new test selection
    # independent from the historical opaque-context diagnostic.
    environment = dict(os.environ)
    environment.update({
        "FOUNDRY_PROJECT_ENDPOINT": "https://example.services.ai.azure.com/api/projects/example-project",
        "SPECIALIST_MODEL_DEPLOYMENT": "synthetic-worker",
        "DECISION_MODEL_DEPLOYMENT": "synthetic-decision",
        "OTEL_SDK_DISABLED": "true", "PYTHONWARNINGS": "ignore",
        "PYTHONPATH": os.pathsep.join((str(ROOT), str(ROOT / "tests"))),
    })
    names = {key: "test_identity_handoff." + value for key, value in PROBES.items()}
    try:
        result = subprocess.run(
            [sys.executable, "-B", "-c", diagnostic.CHILD_PROBE, json.dumps(names)],
            cwd=ROOT, env=environment, capture_output=True, timeout=120,
        )
        value = json.loads(result.stdout) if result.returncode == 0 else None
    except (subprocess.TimeoutExpired, ValueError, UnicodeError):
        value = None
    if (
        not isinstance(value, dict) or type(value.get("passed")) is not bool
        or value.get("tests_run") != len(PROBES)
        or not isinstance(value.get("probes"), dict) or set(value["probes"]) != set(PROBES)
        or any(item not in ("passed", "failed", "skipped", "inconclusive")
               for item in value["probes"].values())
        or value["passed"] != all(item == "passed" for item in value["probes"].values())
    ):
        return {"passed": False, "classification": "OFFLINE_HANDOFF_REPORT_INVALID"}
    return value


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--application-root", type=Path, required=True)
    parser.add_argument("--lab-repository-root", type=Path, required=True)
    parser.add_argument("--scenario", choices=("offline-A-B",), required=True)
    for role in ("coordinator", "architect", "reviewer"):
        parser.add_argument(f"--{role}-version", required=True)
    args = parser.parse_args(argv)
    try:
        if (
            not args.application_root.is_absolute() or args.application_root.resolve() != ROOT
            or not args.lab_repository_root.is_absolute()
            or args.lab_repository_root.resolve() == ROOT
            or not (args.lab_repository_root / ".git").exists()
            or not (args.lab_repository_root / "foundry-tf/multi-agent/Test-PrivateConnectivity.ps1").is_file()
            or any(not re.fullmatch(r"[1-9][0-9]{0,8}", getattr(args, role + "_version"))
                   for role in ("coordinator", "architect", "reviewer"))
        ):
            raise ValueError("HANDOFF_INPUT_INVALID")
        pins = diagnostic.check_pins(ROOT / "requirements.lock.txt")
        probes = offline_probes()
        passed = all(pin["matches"] for pin in pins) and probes["passed"]
        source = {
            name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            for name in (
                "demo/foundry.py", "demo/workflow.py", "demo/artifacts.py",
                "requirements.lock.txt", "scripts/identity_handoff.py", "tests/test_identity_handoff.py",
            )
        }
        report = {
            "schema_version": 1, "selection": "unresolved",
            "classification": "OFFLINE_CANDIDATE_VERIFIED" if passed else "OFFLINE_CANDIDATE_FAILED",
            "evidence_kind": "offline_synthetic", "source_sha256": source,
            "declared_versions_not_cloud_observed": {
                role: getattr(args, role + "_version")
                for role in ("coordinator", "architect", "reviewer")
            },
            "lock_pin_count": len(pins), "pins_match": all(pin["matches"] for pin in pins),
            "probes": probes,
            "live_execution_available": False,
            "permission_delta": "NOT_MEASURED_NO_WRITE",
            "principal_namespace_compatibility": "NOT_MEASURED",
            "next_action": "RECONCILE_LAB_RUNNER_AND_ISOLATED_RUNTIME_CANDIDATE_WITH_ARCHITECT_SCRUM",
            "holds": "PRESERVE_ALL_HISTORICAL_UNKNOWN_AND_HELD_PARENTS",
        }
        print(json.dumps(report, sort_keys=True))
        return 2 if passed else 1
    except (OSError, ValueError):
        # Paths and exceptions may contain private values; return fixed codes.
        print(json.dumps({"selection": "unresolved", "classification": "HANDOFF_INPUT_OR_RUNTIME_INVALID"}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
