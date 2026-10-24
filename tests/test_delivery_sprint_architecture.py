"""Sprint architecture and inherited planning contracts; never live acceptance."""

import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import time
import unittest

import test_delivery_architecture
import test_delivery_release_plan
import test_delivery_sprint_design
import test_delivery_user_experience
from test_delivery_architecture import fields, public_file, require, strings, validate_architecture


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "docs/requirements/delivery-sprint-architecture.json"


def load(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def text(value):
    require(isinstance(value, str) and bool(value.strip()), "nonempty text")


def validate_sprint_architecture(value):
    fields(value, (
        "schemaVersion", "authority", "architecture", "solutionModelRef", "design",
        "releasePlan", "sprintDesign", "observedSource", "sprint", "priorSprints",
        "scope", "tiers", "taskBindings", "evidenceState",
        "blockedArchitectureDecisions", "handoff",
    ))
    require(type(value["schemaVersion"]) is int and value["schemaVersion"] == 1, "schema version")
    expected = {
        "authority": "docs/requirements/delivery-mission.md",
        "architecture": "docs/requirements/delivery-architecture.json",
        "design": "docs/requirements/delivery-sprint-architecture.md",
        "releasePlan": "docs/requirements/delivery-release-plan.json",
        "sprintDesign": "docs/requirements/delivery-sprint-design.json",
    }
    for key, path in expected.items():
        require(value[key] == path, "approved input reference")
        public_file(path)
    require(value["solutionModelRef"] == value["architecture"] + "#/solutionModel", "reuse holistic model")
    require(re.fullmatch(r"[a-f0-9]{40}", value["observedSource"]) is not None, "observed revision")
    require(value["scope"] == "sprint-architecture-only-no-runtime-or-transport-change", "bounded scope")
    require(value["priorSprints"] == [], "no invented completed sprints")
    require(value["blockedArchitectureDecisions"] == [], "no historical or speculative blockers")

    architecture = load(value["architecture"])
    validate_architecture(architecture)
    require(architecture["observedSource"] == value["observedSource"], "current holistic source join")
    require(architecture["sprintRefinement"] == {
        "sprint": value["sprint"], "design": value["design"],
        "contract": ARTIFACT.relative_to(ROOT).as_posix(),
    }, "holistic refinement backlink")
    plan = load(value["releasePlan"])
    design = load(value["sprintDesign"])
    sprints = [s for s in plan["sprints"] if s["id"] == value["sprint"]]
    require(len(sprints) == 1 and design["sprint"] == value["sprint"], "approved sprint")
    sprint = sprints[0]
    components = {c["id"]: c for c in architecture["solutionModel"]["components"]}
    flows = {f["id"]: f for f in architecture["solutionModel"]["flows"]}
    steps = {s["id"]: s for f in flows.values() for s in f["steps"]}

    tier_components = {
        "client-release": ["deployment", "terminal-demo"],
        "coordinator": ["coordinator-routing", "session-continuity-recovery-isolation"],
        "specialists": ["architect", "reviewer"],
        "shared-artifacts": ["blob-shared-context"],
    }
    require(isinstance(value["tiers"], list) and len(value["tiers"]) == 4, "four technical tiers")
    require({t["id"] for t in value["tiers"]} == set(tier_components), "tier identities")
    covered = []
    for tier in value["tiers"]:
        fields(tier, ("id", "design", "components", "requirements"))
        require(tier["components"] == tier_components[tier["id"]], "single shared support ownership")
        require(tier["design"] == "docs/requirements/" + tier["id"] + "/delivery-sprint-architecture.md",
                "tier design location")
        public_file(tier["design"])
        covered.extend(tier["components"])
        strings(tier["requirements"])
        required = {r for c in tier["components"] for r in components[c]["requirements"]}
        require(set(tier["requirements"]) == required, "tier mission join")
        narrative = (ROOT / tier["design"]).read_text(encoding="utf-8")
        for reference in (*tier["components"], "delivery-mission.md", "delivery-sprint-architecture.json"):
            require(reference in narrative, "tier narrative join")
    require(len(covered) == len(set(covered)) and set(covered) == set(components), "complete tier partition")

    tasks = {t["id"]: t for t in sprint["tasks"]}
    bindings = value["taskBindings"]
    require(isinstance(bindings, list) and len(bindings) == len(tasks), "all existing tasks")
    require({b["task"] for b in bindings} == set(tasks), "no new or missing tasks")
    require({d["task"] for d in design["taskDesign"]} == set(tasks), "sprint design join")
    all_steps = set()
    for binding in bindings:
        fields(binding, ("task", "requirements", "components", "flows", "flowSteps",
                         "source", "localTests", "construction", "handoff"))
        task = tasks[binding["task"]]
        for key in ("requirements", "components", "flows"):
            require(binding[key] == task[key], "preserve approved task " + key)
        strings(binding["flowSteps"])
        permitted_steps = {s["id"] for f in binding["flows"] for s in flows[f]["steps"]}
        require(set(binding["flowSteps"]) <= permitted_steps, "task flow-step join")
        require(all(set(steps[s]["components"]) & set(binding["components"])
                    for s in binding["flowSteps"]), "step touches assigned components")
        all_steps.update(binding["flowSteps"])
        for key in ("source", "localTests"):
            strings(binding[key])
            mapped = {p for c in binding["components"] for p in components[c][key]}
            for path in binding[key]:
                public_file(path)
                require(path in mapped, "actual architecture source/test join")
        text(binding["construction"])
        text(binding["handoff"])
    require(all_steps == set(steps), "holistic flow-step coverage")

    state = value["evidenceState"]
    fields(state, ("implementation", "localVerification", "deployment",
                   "independentLiveVerification", "acceptedAssignments", "currentBlocker"))
    require(state["implementation"] == "source-present-except-D1-predeploy-contract-change-required",
            "source versus missing construction")
    require(state["localVerification"] == "architecture-contract-checks-only-runtime-tests-mapped-not-executed",
            "no invented runtime verification")
    require(state["deployment"] == state["independentLiveVerification"] == "not-executed",
            "no invented live pass")
    require(state["acceptedAssignments"] == [], "no assignment released by architecture")
    blocker = state["currentBlocker"]
    fields(blocker, ("requirement", "component", "flow", "step", "evidence",
                     "failure", "remedyOwner", "unblock"))
    require((blocker["requirement"], blocker["component"], blocker["flow"], blocker["step"])
            == ("D1/F1", "deployment", "exact-candidate-delivery", "select-and-check"),
            "localized original-criterion blocker")
    require(blocker["evidence"] == ["azure.yaml", "package_guard.py"], "inspectable current source")
    require(blocker["remedyOwner"] == "DevOps Engineer", "existing owner")
    text(blocker["failure"])
    text(blocker["unblock"])

    handoff = value["handoff"]
    fields(handoff, ("planningOwner", "verificationLoops", "exclusiveResources", "candidate",
                     "construction", "dependencyRelease", "unknownEffects", "replan"))
    require(handoff["planningOwner"] == plan["planningOwner"], "planning ownership")
    require(handoff["verificationLoops"] == plan["deliveryContract"]["verification"],
            "existing DevOps then E2E")
    require(handoff["exclusiveResources"] == plan["exclusiveResources"]
            == architecture["deliveryHandoff"]["exclusiveResources"], "both shared resources")
    for key in ("candidate", "construction", "dependencyRelease", "unknownEffects", "replan"):
        require(handoff[key] == plan["deliveryContract"][key], "approved handoff " + key)


class SprintArchitectureTests(unittest.TestCase):
    def setUp(self):
        self.value = json.loads(ARTIFACT.read_text(encoding="utf-8"))

    def reject(self, mutate):
        candidate = deepcopy(self.value)
        mutate(candidate)
        with self.assertRaises((ValueError, TypeError, KeyError)):
            validate_sprint_architecture(candidate)

    def test_full_sprint_contract_tier_and_task_joins(self):
        validate_sprint_architecture(self.value)

    def test_rejects_model_fork_scope_expansion_and_historical_blockers(self):
        self.reject(lambda v: v.update(solutionModelRef="invented-model"))
        self.reject(lambda v: v.update(scope="new-transport"))
        self.reject(lambda v: v.update(priorSprints=["invented-accepted-sprint"]))
        self.reject(lambda v: v["blockedArchitectureDecisions"].append("old-header-diagnosis"))

    def test_rejects_missing_duplicate_or_reassigned_tiers(self):
        self.reject(lambda v: v["tiers"].pop())
        self.reject(lambda v: v["tiers"][0].update(id="coordinator"))
        self.reject(lambda v: v["tiers"][0]["components"].append("blob-shared-context"))
        self.reject(lambda v: v["tiers"][0].update(requirements=["D2"]))

    def test_rejects_missing_invented_or_changed_tasks(self):
        self.reject(lambda v: v["taskBindings"].pop())
        self.reject(lambda v: v["taskBindings"][0].update(task="new-task"))
        self.reject(lambda v: v["taskBindings"][1].update(components=["architect"]))
        self.reject(lambda v: v["taskBindings"][1].update(requirements=["D8"]))
        self.reject(lambda v: v["taskBindings"][0].update(flows=["design-review-revision"]))

    def test_rejects_dangling_steps_private_paths_and_unmapped_tests(self):
        self.reject(lambda v: v["taskBindings"][0]["flowSteps"].append("missing"))
        self.reject(lambda v: v["taskBindings"][0].update(flowSteps=["review-and-revise"]))
        self.reject(lambda v: v["taskBindings"][0].update(source=[".local/settings.json"]))
        self.reject(lambda v: v["taskBindings"][0].update(localTests=["tests/test_artifacts.py"]))
        self.reject(lambda v: v["tiers"][0].update(design="../outside.md"))

    def test_rejects_invented_execution_and_assignment_acceptance(self):
        for key in ("localVerification", "deployment", "independentLiveVerification"):
            self.reject(lambda v, key=key: v["evidenceState"].update({key: "passed"}))
        self.reject(lambda v: v["evidenceState"]["acceptedAssignments"].append("azd-walking-skeleton"))
        self.reject(lambda v: v["evidenceState"]["currentBlocker"].update(requirement="invented-gate"))

    def test_rejects_missing_locks_mutable_candidates_replay_and_premature_release(self):
        self.reject(lambda v: v["handoff"]["exclusiveResources"].pop())
        self.reject(lambda v: v["handoff"].update(candidate="mutable-working-tree"))
        self.reject(lambda v: v["handoff"].update(unknownEffects="retry"))
        self.reject(lambda v: v["handoff"].update(dependencyRelease="local-pass"))
        self.reject(lambda v: v["handoff"]["verificationLoops"].reverse())

    def test_rejects_new_contract_fields(self):
        self.reject(lambda v: v.update(dispositionLedger=[]))

    def test_narrative_keeps_source_live_and_architecture_acceptance_distinct(self):
        narrative = (ROOT / self.value["design"]).read_text(encoding="utf-8")
        for item in (
            "not deployed acceptance", "No product scope", "not newly",
            "No major host change", "unknown effects stay held",
            "application-enforced ownership", "not storage-enforced per-role isolation",
            "separate deployed", "No local result substitutes",
        ):
            self.assertIn(item, narrative)
        for component in load(self.value["architecture"])["solutionModel"]["components"]:
            self.assertIn("| " + component["id"] + " |", narrative)
        for tier in self.value["tiers"]:
            self.assertIn(tier["design"].removeprefix("docs/requirements/"), narrative)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, required=True)
    args = parser.parse_args()
    destination = args.evidence.resolve()
    require(destination.is_relative_to(ROOT / "docs/requirements/checks"), "public check evidence path")
    modules = [
        sys.modules[__name__], test_delivery_architecture, test_delivery_user_experience,
        test_delivery_release_plan, test_delivery_sprint_design,
    ]
    suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromModule(m) for m in modules)
    output = io.StringIO()
    started = time.monotonic()
    result = unittest.TextTestRunner(stream=output, verbosity=2).run(suite)
    elapsed = time.monotonic() - started
    exit_code = 0 if result.wasSuccessful() else 1
    source = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True,
    ).strip()
    refs = [
        "docs/requirements/delivery-sprint-architecture.json",
        "docs/requirements/delivery-architecture.json",
        "docs/requirements/delivery-user-experience.json",
        "docs/requirements/delivery-release-plan.json",
        "docs/requirements/delivery-sprint-design.json",
    ]
    hashes = "".join(
        relative + " normalized UTF-8 LF SHA256: "
        + hashlib.sha256((ROOT / relative).read_text(encoding="utf-8").encode("utf-8")).hexdigest()
        + "\n" for relative in refs
    )
    report = (
        "Architecture/planning contract checks only; no runtime tests or cloud operations.\n"
        + "UTC: " + datetime.now(timezone.utc).isoformat() + "\n"
        + "Precommit source HEAD: " + source + "\nPython: " + sys.version.split()[0]
        + "\nCommand: " + subprocess.list2cmdline([sys.executable, *sys.argv]) + "\n"
        + hashes + output.getvalue()
        + f"Elapsed: {elapsed:.3f} s (combined local test suite)\nexitCode: {exit_code}\n"
    )
    print(report)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(report, encoding="utf-8")
    sys.exit(exit_code)
