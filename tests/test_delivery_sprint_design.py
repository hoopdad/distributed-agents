"""Sprint design contract checks only; no deployed or usability acceptance."""

import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import unittest

from test_delivery_user_experience import fields, public_file, require, strings, text


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "docs/requirements/delivery-sprint-design.json"


def load(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def validate_sprint_design(value):
    fields(value, "schemaVersion authority architecture userExperience releasePlan design "
           "observedSource sprint scope presentation screens journeys taskDesign stateActions "
           "blockedDesignItems handoff")
    require(type(value["schemaVersion"]) is int and value["schemaVersion"] == 1, "schema version")
    refs = {
        "authority": "docs/requirements/delivery-mission.md",
        "architecture": "docs/requirements/delivery-architecture.json",
        "userExperience": "docs/requirements/delivery-user-experience.json",
        "releasePlan": "docs/requirements/delivery-release-plan.json",
        "design": "docs/requirements/delivery-sprint-design.md",
    }
    for key, expected in refs.items():
        require(value[key] == expected, "original input reference")
        public_file(value[key])
    import re
    require(isinstance(value["observedSource"], str)
            and re.fullmatch(r"[a-f0-9]{40}", value["observedSource"]), "source revision")
    require(value["scope"] == "sprint-terminal-design-only-no-runtime-change", "bounded design")
    architecture = load(value["architecture"])
    ux = load(value["userExperience"])
    plan = load(value["releasePlan"])
    sprints = [s for s in plan["sprints"] if s["id"] == value["sprint"]]
    require(len(sprints) == 1, "existing sprint")
    sprint = sprints[0]
    fixed = {key: ux["presentation"][key] for key in (
        "stdout", "human", "theme", "generatedContent", "privacy", "releaseClaim",
    )}
    fixed.update(
        readingOrder="orientation-ordered-observations-result-limitations-next-action",
        ragLabels=["GREEN", "AMBER", "RED"],
        narrowLayout="linear-wrapped-regions-not-wide-TUI",
        fixtures="illustrations-with-placeholders-never-live-evidence",
    )
    require(value["presentation"] == fixed, "inherited presentation and truthful fixtures")
    screens = value["screens"]
    expected = {
        "terminal-turn": (
            "existing-opt-in-human-stderr",
            ["ready", "streaming", "accepted-advisory", "request-input", "routing-hold", "limit-reached"],
            ["orientation", "ordered-calls", "current-result", "confidence-footer"],
            "validated-complete-current-result-and-successful-state-finalization",
            "not-observed-never-inferred", "authorized-private-evidence-not-new-stdout",
        ),
        "terminal-exception": (
            "existing-opt-in-human-stderr",
            ["known-pending-response", "unknown-effect", "failed-or-invalid"],
            ["observed-boundary", "recovery-boundary"],
            "hold-or-invalid-or-unfinalized-output-never-accepted",
            "not-observed-never-inferred", "supported-private-reconciliation-not-reset-or-new-parent",
        ),
        "component-report": (
            "existing-authorized-acceptance-evidence-and-delivery-report", [],
            ["candidate-header", "artifact-trail", "verification-and-action"],
            "fresh-source-bound-deployed-checks-not-advisory-model-approval",
            "not-verified-amber-not-failed", "private-exact-refs-sanitized-public-summary",
        ),
    }
    require(isinstance(screens, list) and len(screens) == len(expected), "three existing screens")
    require({s["id"] for s in screens} == set(expected), "screen identity")
    covered_states = []
    for screen in screens:
        fields(screen, "id surface states regions acceptanceBoundary missingData detailRoute")
        surface, states, regions, boundary, missing, detail = expected[screen["id"]]
        require((screen["surface"], screen["states"], screen["acceptanceBoundary"],
                 screen["missingData"], screen["detailRoute"])
                == (surface, states, boundary, missing, detail), "surface and safe boundaries")
        require([r["id"] for r in screen["regions"]] == regions, "ordered screen regions")
        covered_states.extend(states)
        for region in screen["regions"]:
            fields(region, "id fields source visibility")
            strings(region["fields"])
            public_file(region["source"])
            require(region["visibility"] == (
                "authorized-evidence" if screen["id"] == "component-report" else "default-human"
            ), "privacy boundary")
    require(set(covered_states) == {s["id"] for s in ux["states"]}, "all inherited UX states")
    trail = screens[2]["regions"][1]["fields"]
    require(trail == [
        "exact-requirements-ref", "first-design-ref", "actual-first-findings-ref",
        "changed-design-ref", "exact-revised-review-ref", "gated-decision-refs",
        "child-producer-and-prerequisite-bindings",
    ], "real exact revision and provenance trail")

    flows = {f["id"]: f for f in architecture["solutionModel"]["flows"]}
    journeys = value["journeys"]
    require(len(journeys) == len(flows) and {j["id"] for j in journeys} == set(flows),
            "existing flow coverage")
    for journey in journeys:
        fields(journey, "id screens steps return")
        strings(journey["screens"])
        require(set(journey["screens"]) <= set(expected), "existing journey screens")
        require(journey["steps"] == [s["id"] for s in flows[journey["id"]]["steps"]],
                "ordered architecture flow steps")
        text(journey["return"])
    tasks = {t["id"]: t for t in sprint["tasks"]}
    rows = value["taskDesign"]
    require(len(rows) == len(tasks) and {r["task"] for r in rows} == set(tasks),
            "all sprint task design joins")
    for row in rows:
        fields(row, "task requirements components flows screens direction")
        for key in ("requirements", "components", "flows"):
            require(row[key] == tasks[row["task"]][key], "exact release task scope")
        strings(row["screens"])
        require(set(row["screens"]) <= set(expected), "existing task screens")
        text(row["direction"])
    require(value["stateActions"] == "inherit-exact-delivery-user-experience-state-action-gates",
            "no new state machine")
    require(value["blockedDesignItems"] == [], "no supplied blocked design items")
    require(value["handoff"] == {
        "implementationOwner": "Developer", "planningOwner": "Scrum Master",
        "verificationLoops": plan["deliveryContract"]["verification"],
        "exclusiveResources": plan["exclusiveResources"],
        "candidate": "exact-committed-feature-revision-or-immutable-artifact",
        "construction": "local-checks-no-shared-environment-mutation",
        "dependencyRelease": "only-after-deployed-pass-and-original-assignment-review",
        "assignedDesignImplementation": [],
        "exclusions": ux["handoff"]["exclusions"],
    }, "existing owners, locks and deployed acceptance")


class DeliverySprintDesignTests(unittest.TestCase):
    def setUp(self):
        self.design = load("docs/requirements/delivery-sprint-design.json")

    def reject(self, mutate):
        candidate = deepcopy(self.design)
        mutate(candidate)
        with self.assertRaises((ValueError, KeyError, TypeError)):
            validate_sprint_design(candidate)

    def test_schema_and_exact_sprint_architecture_UX_joins(self):
        validate_sprint_design(self.design)

    def test_rejects_missing_or_expanded_task_scope(self):
        self.reject(lambda x: x["taskDesign"].pop())
        for key, extra in (("requirements", "D8"), ("components", "dashboard"),
                           ("flows", "reset-parent")):
            self.reject(lambda x, key=key, extra=extra: x["taskDesign"][0][key].append(extra))
        self.reject(lambda x: x["taskDesign"].__setitem__(1, deepcopy(x["taskDesign"][0])))

    def test_rejects_changed_flows_order_and_new_screens(self):
        self.reject(lambda x: x["journeys"].pop())
        self.reject(lambda x: x["journeys"][0]["steps"].reverse())
        self.reject(lambda x: x["journeys"][0]["screens"].append("web-dashboard"))
        self.reject(lambda x: x["screens"][0].update(id="new-ui"))

    def test_rejects_stdout_theme_privacy_and_false_acceptance_changes(self):
        for key, bad in (("stdout", "human-on-stdout"), ("theme", "forced-ANSI"),
                         ("privacy", "print-private-refs"), ("releaseClaim", "model-approved"),
                         ("fixtures", "live-success")):
            self.reject(lambda x, key=key, bad=bad: x["presentation"].update({key: bad}))

    def test_rejects_hold_replay_unpersisted_success_or_missing_states(self):
        self.reject(lambda x: x["screens"][1].update(detailRoute="reset-and-resend"))
        self.reject(lambda x: x["screens"][0].update(acceptanceBoundary="partial-stream"))
        self.reject(lambda x: x["screens"][1]["states"].remove("unknown-effect"))
        self.reject(lambda x: x.update(stateActions="retry-all"))

    def test_rejects_fabricated_or_stale_revision_trail(self):
        self.reject(lambda x: x["screens"][2]["regions"][1]["fields"].remove("actual-first-findings-ref"))
        self.reject(lambda x: x["screens"][2]["regions"][1]["fields"].reverse())
        self.reject(lambda x: x["screens"][2].update(missingData="failed-red"))

    def test_rejects_private_paths_and_public_artifact_disclosure(self):
        for path in (".local/settings.json", "../outside.py", "demo/absent.py"):
            self.reject(lambda x, path=path: x["screens"][0]["regions"][0].update(source=path))
        self.reject(lambda x: x["screens"][2]["regions"][1].update(visibility="default-human"))

    def test_rejects_local_only_acceptance_new_assignments_and_scope(self):
        self.reject(lambda x: x["handoff"].update(dependencyRelease="schema-pass"))
        self.reject(lambda x: x["handoff"]["verificationLoops"].reverse())
        self.reject(lambda x: x["handoff"]["exclusiveResources"].pop())
        self.reject(lambda x: x["handoff"]["assignedDesignImplementation"].append("new-task"))
        self.reject(lambda x: x.update(blockedDesignItems=["historical-denial"]))
        self.reject(lambda x: x.update(scope="new-product"))

    def test_narrative_has_layouts_flow_joins_and_honest_limitations(self):
        narrative = (ROOT / self.design["design"]).read_text(encoding="utf-8")
        for phrase in ("Illustrative layout only", "not deployed acceptance",
                       "no assigned design implementation tasks",
                       "not all prior artifact bodies", "Unknown effect",
                       "Account-wide Blob Contributor", "No retry/reset/new-parent",
                       "not deployed behavior", "not a new live phase"):
            self.assertIn(phrase.lower(), narrative.lower())
        for journey in self.design["journeys"]:
            self.assertIn("`" + journey["id"] + "`", narrative)
        for component in load(self.design["userExperience"])["presentation"]["reportComponents"]:
            self.assertIn("| " + component + " |", narrative)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path)
    args = parser.parse_args()
    output = io.StringIO()
    result = unittest.TextTestRunner(stream=output, verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(DeliverySprintDesignTests)
    )
    code = 0 if result.wasSuccessful() else 1
    revision = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True, check=True,
    ).stdout.strip()
    report = (
        "Sprint design contract only; no deployed behavior or usability acceptance.\n"
        + "Command: " + subprocess.list2cmdline([sys.executable, *sys.argv]) + "\n"
        + "UTC: " + datetime.now(timezone.utc).isoformat() + "\n"
        + "Execution base HEAD (may precede committed design): " + revision + "\n"
        + "Artifact normalized UTF-8 LF SHA256: "
        + hashlib.sha256(ARTIFACT.read_text(encoding="utf-8").encode("utf-8")).hexdigest() + "\n"
        + output.getvalue() + "exitCode: " + str(code) + "\n"
    )
    print(report)
    if args.evidence:
        destination = args.evidence.resolve()
        require(destination.is_relative_to(ROOT / "docs/requirements/checks"), "public evidence path")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(report, encoding="utf-8")
    sys.exit(code)
