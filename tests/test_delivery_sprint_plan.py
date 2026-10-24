"""Executable sprint planning checks; never product/deployed acceptance."""

import argparse
from copy import deepcopy
from contextlib import redirect_stdout
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import time
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_sprint_plan import resolve_plan  # noqa: E402

ARTIFACT = ROOT / "docs/requirements/delivery-sprint-plan.json"


def require(value, reason):
    if not value:
        raise ValueError(reason)


def validate(plan):
    # Exact inheritance prevents a generated plan silently expanding approved scope.
    require(plan == resolve_plan(), "approved inputs, dispatch contract and work cards must match")
    tasks = plan["tasks"]
    by_id = {task["id"]: task for task in tasks}
    require(len(by_id) == len(tasks) == 6, "unique assigned tasks")
    release = json.loads((ROOT / plan["releasePlan"]).read_text(encoding="utf-8"))
    architecture = json.loads((ROOT / plan["sprintArchitecture"]).read_text(encoding="utf-8"))
    bindings = {item["task"]: item for item in architecture["taskBindings"]}
    visited = set()

    def ancestors(key, active=frozenset()):
        require(key in by_id and key not in active, "known acyclic dependencies")
        result = set()
        for dep in by_id[key]["dependsOn"]:
            result.add(dep)
            result.update(ancestors(dep, active | {key}))
        return result

    fields = set("role action goal components flows flowSteps doneWhen failureCategories mustAct "
                 "locations evidence cause verification humanAction humanActionEvidence".split())
    for task, seed in zip(tasks, release["sprints"][0]["tasks"]):
        require(all(task[key] == value for key, value in seed.items()), "preserve approved task")
        card = task["workCard"]
        require(set(card) == fields, "workCard schema")
        require(card["role"] == task["owner"] and card["action"] == task["title"]
                and card["doneWhen"] == task["doneWhen"], "owner/title/doneWhen identity")
        require(card["components"] == task["components"] and card["flows"] == task["flows"]
                and card["flowSteps"] == bindings[task["id"]]["flowSteps"], "architecture scope")
        require(card["failureCategories"] == [] and card["evidence"] == card["cause"]
                == card["humanAction"] == card["humanActionEvidence"] == "", "unperformed card")
        require(card["verification"] == {"status": "not-yet-verified", "evidence": ""},
                "no invented verification")
        require("passes in the deployed environment" in task["doneWhen"], "deployed doneWhen")
        require("DevOpsWorkLoop then EndToEndTestLoop" in task["handoff"], "continuous verification")
        require(all((ROOT / path).is_file() for path in task["source"] + task["localTests"]),
                "inspectable module/test joins")
        require(all(type(n) is int and n >= 0 for n in task["estimatedMinutes"].values()), "estimates")
        deps = ancestors(task["id"])
        if task is not tasks[0]:
            require(tasks[0]["id"] in deps, "deployed-first dependency")
        visited.add(task["id"])
    require(tasks[0]["walkingSkeleton"] and tasks[0]["dependsOn"] == []
            and tasks[0]["owner"] == "DevOps Engineer", "first walking skeleton")
    assignment_ids = [key for group in plan["assignments"].values() for key in group]
    require(len(assignment_ids) == len(set(assignment_ids)) and set(assignment_ids) == visited,
            "all tasks assigned once")
    for output, kind in (("AssignedWorkUIDeveloper", "ui"), ("AssignedWorkDeveloper", "developer"),
                         ("AssignedWorkDevOpsEngineer", "devops"), ("AssignedWorkDesigner", "designer")):
        require(plan["assignments"][output] == [t["id"] for t in tasks if t["kind"] == kind],
                "assignment output ownership")
    for path in (plan["estimates"]["criticalPath"], plan["estimates"]["tiedCriticalPath"]):
        require(sum(sum(by_id[key]["estimatedMinutes"].values()) for key in path) == 410,
                "critical path arithmetic")
        require(all(left in by_id[right]["dependsOn"] for left, right in zip(path, path[1:])),
                "critical path edges")
    ready = [t["id"] for t in tasks if not t["dependsOn"]]
    require(ready == plan["dispatch"]["initialReady"], "actual initial readiness")
    after = [t["id"] for t in tasks if t["dependsOn"] == ready]
    require(after == plan["dispatch"]["parallelAfterSkeleton"], "independent fanout")
    require(sum(sum(t["estimatedMinutes"].values()) for t in tasks) == 595, "effort arithmetic")


class SprintPlanTests(unittest.TestCase):
    def setUp(self):
        self.plan = json.loads(ARTIFACT.read_text(encoding="utf-8"))

    def reject(self, change):
        candidate = deepcopy(self.plan)
        change(candidate)
        with self.assertRaises((ValueError, KeyError, TypeError)):
            validate(candidate)

    def test_schema_approved_scope_assignment_and_dependency_contract(self):
        validate(self.plan)

    def test_negative_skeleton_bypass_cycle_and_unknown_dependency(self):
        self.reject(lambda p: p["tasks"][0].update(walkingSkeleton=False))
        self.reject(lambda p: p["tasks"][1].update(dependsOn=[]))
        self.reject(lambda p: p["tasks"][1].update(dependsOn=["missing"]))
        self.reject(lambda p: p["tasks"][1].update(dependsOn=[p["tasks"][1]["id"]]))

    def test_negative_unassigned_wrong_owner_and_duplicate_assignment(self):
        self.reject(lambda p: p["assignments"]["AssignedWorkDeveloper"].pop())
        self.reject(lambda p: p["assignments"]["AssignedWorkDesigner"].append(p["tasks"][1]["id"]))
        self.reject(lambda p: p["tasks"][1]["workCard"].update(role="Designer"))

    def test_negative_card_drift_fabricated_observation_or_scope(self):
        for field, value in (("action", "Generic work"), ("doneWhen", "Offline pass"),
                             ("evidence", "Passed"), ("humanAction", "Approve"),
                             ("components", ["fourth-role"]),
                             ("verification", {"status": "passed", "evidence": "none"})):
            self.reject(lambda p, field=field, value=value: p["tasks"][1]["workCard"].update({field: value}))

    def test_negative_lock_candidate_and_dependency_release_bypass(self):
        self.reject(lambda p: p["deliveryContract"].update(candidate="mutable-checkout"))
        self.reject(lambda p: p["deliveryContract"].update(dependencyRelease="offline-only"))
        self.reject(lambda p: p["tasks"][0].update(exclusiveResources=[]))
        self.reject(lambda p: p["tasks"][1].update(exclusiveResources=p["exclusiveResources"]))
        self.reject(lambda p: p["dispatch"].update(releaseGate="local-pass"))

    def test_negative_estimates_are_not_limits(self):
        self.reject(lambda p: p.update(maxSprints=1))
        self.reject(lambda p: p["estimates"].update(dependencyLowerBoundMinutes=1))
        self.reject(lambda p: p["tasks"][0]["estimatedMinutes"].update(implementation=-1))

    def test_narrative_scope_and_status_coverage(self):
        text = (ROOT / self.plan["design"]).read_text(encoding="utf-8")
        for task in self.plan["tasks"]:
            self.assertIn("`" + task["id"] + "`", text)
        for component in self.plan["tasks"][-1]["components"]:
            self.assertIn("| " + component + " |", text)
        for phrase in ("410 minutes", "595 minutes", "Scrum Master owns Git reconciliation",
                       "separate deployed probe", "DevOpsWorkLoop then EndToEndTestLoop",
                       "not implementation execution"):
            self.assertIn(phrase, text)

    def test_actual_runtime_schema_and_synthetic_parallel_dispatch(self):
        result = subprocess.run(["node", "tests/test_delivery_sprint_dispatch.mjs"],
                                cwd=ROOT, capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        print(result.stdout)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, required=True)
    args = parser.parse_args()
    started = time.monotonic()
    output = io.StringIO()
    with redirect_stdout(output):
        result = unittest.TextTestRunner(stream=output, verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(SprintPlanTests))
    code = 0 if result.wasSuccessful() else 1
    report = (
        "Planning/schema and synthetic dispatch only; no cloud or implementation acceptance.\n"
        "Command: python tests/test_delivery_sprint_plan.py --evidence "
        + args.evidence.as_posix() + "\nUTC: " + datetime.now(timezone.utc).isoformat()
        + "\nArtifact normalized UTF-8 SHA256: "
        + hashlib.sha256(ARTIFACT.read_text(encoding="utf-8").encode("utf-8")).hexdigest()
        + "\n" + output.getvalue() + "elapsedSeconds: " + str(round(time.monotonic() - started, 3))
        + "\nexitCode: " + str(code) + "\n")
    destination = args.evidence.resolve()
    require(destination.is_relative_to(ROOT / "docs/requirements/checks"), "public evidence path")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(report, encoding="utf-8")
    print(report)
    sys.exit(code)
