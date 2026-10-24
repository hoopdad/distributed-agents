"""Release planning contracts only; no deployment or live acceptance."""

import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "docs/requirements/delivery-release-plan.json"


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def fields(value, names):
    require(isinstance(value, dict) and set(value) == set(names.split()), "object fields")


def text(value):
    require(isinstance(value, str) and bool(value.strip()), "nonempty text")


def strings(value, empty=False):
    require(isinstance(value, list) and (empty or bool(value)), "string array")
    for item in value:
        text(item)
    require(len(value) == len(set(value)), "unique strings")


def validate_plan(plan):
    fields(plan, "schemaVersion authority architecture userExperience design observedSource "
           "featureBranch scope environment planningOwner exclusiveResources deliveryContract exclusions sprints")
    require(type(plan["schemaVersion"]) is int and plan["schemaVersion"] == 1, "version")
    references = {
        "authority": "docs/requirements/delivery-mission.md",
        "architecture": "docs/requirements/delivery-architecture.json",
        "userExperience": "docs/requirements/delivery-user-experience.json",
        "design": "docs/requirements/delivery-release-plan.md",
    }
    for key, value in references.items():
        require(plan[key] == value and (ROOT / value).is_file(), "input reference")
    require(re.fullmatch("[a-f0-9]{40}", plan["observedSource"]) is not None, "source revision")
    require(plan["featureBranch"] == "feature/azd-demo-delivery", "authorized feature branch")
    require(plan["scope"] == "release-planning-not-deployed-acceptance", "planning boundary")
    require(plan["environment"] == "existing-validated-nonproduction-dev-lab-project", "existing environment")
    require(plan["planningOwner"] == "Scrum Master", "task decomposition owner")
    resources = ["existing-nonproduction-project-deployment-and-verification",
                 "existing-nonproduction-project-deployment-configuration"]
    require(plan["exclusiveResources"] == resources, "shared environment/configuration serialization")
    require(plan["deliveryContract"] == {
        "candidate": "exact-committed-revision-or-immutable-artifact",
        "construction": "local-checks-no-shared-environment-mutation",
        "verification": ["DevOpsWorkLoop", "EndToEndTestLoop"],
        "lock": "held-across-exact-candidate-deployment-and-E2E",
        "dependencyRelease": "only-after-deployed-pass-and-original-assignment-review",
        "evidence": ["actual-command", "actual-exitCode", "nonempty-repository-relative-result",
                     "candidate", "run", "observed-environment-and-versions"],
        "blockers": "current-evidenced-criterion-only-continue-independent-approved-work",
        "unknownEffects": "preserve-holds-no-replay",
        "replan": "material-contract-dependency-or-scope-change-through-existing-roles",
        "gitReconciliationOwner": "Scrum Master",
        "gitReconciliation": "SprintReview-SprintRetro-ReleaseCloseout-feature-commit-or-retained-named-branch-with-commit-and-abandonment-reason-in-feature-commit",
    }, "mission delivery contract")
    require(plan["exclusions"] == [
        "azd-up-or-provision-without-separate-exact-authority",
        "infrastructure-RBAC-network-DNS-quota-VM-power",
        "secret-retrieval-VPN-private-lab-edits-production-profiles",
        "fourth-role-hidden-local-specialists-principal-substitution",
        "authorization-weakening-unknown-effect-replay-held-state-clearing",
        "SDK-journal-or-database-edits",
        "Git-push-provider-submission",
        "new-approval-stages-disposition-ledgers-invented-limits",
    ], "authority exclusions")
    mission = (ROOT / plan["authority"]).read_text(encoding="utf-8")
    canonical = dict(re.findall(r"^\| (D[1-7]) \| `([^`]+)` \|", mission, re.MULTILINE))
    require(len(canonical) == 7, "mission IDs")
    architecture = json.loads((ROOT / plan["architecture"]).read_text(encoding="utf-8"))
    flows = {flow["id"] for flow in architecture["solutionModel"]["flows"]}
    ux = json.loads((ROOT / plan["userExperience"]).read_text(encoding="utf-8"))
    require(flows == {flow["id"] for flow in ux["flows"]}, "accepted flow joins")

    def subset(items, allowed):
        strings(items)
        require(set(items) <= set(allowed), "requirement/component/flow authority")

    sprints = plan["sprints"]
    require(isinstance(sprints, list) and bool(sprints), "one or more sprints")
    sprint_ids = [sprint["id"] for sprint in sprints]
    strings(sprint_ids)
    all_tasks = {}
    requirements_seen, components_seen, flows_seen = set(), set(), set()
    sprint_graph = {}
    for sprint in sprints:
        fields(sprint, "id title goal dependsOn requirements flows acceptanceCriteria tasks")
        for key in ("id", "title", "goal"):
            text(sprint[key])
        strings(sprint["dependsOn"], empty=True)
        require(set(sprint["dependsOn"]) <= set(sprint_ids), "known sprint dependencies")
        sprint_graph[sprint["id"]] = sprint["dependsOn"]
        subset(sprint["requirements"], canonical)
        subset(sprint["flows"], flows)
        criteria = sprint["acceptanceCriteria"]
        require(isinstance(criteria, list) and bool(criteria), "sprint acceptance criteria")
        for criterion in criteria:
            fields(criterion, "requirement criterion")
            require(criterion["requirement"] in sprint["requirements"], "criterion trace")
            text(criterion["criterion"])
        require({item["requirement"] for item in criteria} == set(sprint["requirements"]), "criterion coverage")
        require(isinstance(sprint["tasks"], list) and bool(sprint["tasks"]), "task seeds")
        covered = set()
        for task in sprint["tasks"]:
            fields(task, "id title kind owner walkingSkeleton dependsOn requirements components "
                   "flows exclusiveResources doneWhen exclusions handoff")
            for key in ("id", "title", "owner", "doneWhen", "handoff"):
                text(task[key])
            require(task["id"] not in all_tasks, "unique task IDs")
            all_tasks[task["id"]] = task
            require(task["kind"] in {"ui", "developer", "designer", "devops"}, "task kind")
            require(task["owner"] == {
                "ui": "Developer", "developer": "Developer", "designer": "Designer",
                "devops": "DevOps Engineer",
            }[task["kind"]], "concrete owner")
            require(type(task["walkingSkeleton"]) is bool, "skeleton marker")
            strings(task["dependsOn"], empty=True)
            subset(task["requirements"], sprint["requirements"])
            subset(task["components"], canonical.values())
            require(set(task["components"]) == {canonical[r] for r in task["requirements"]}, "component trace")
            subset(task["flows"], sprint["flows"])
            strings(task["exclusions"])
            strings(task["exclusiveResources"], empty=True)
            require(set(task["exclusiveResources"]) <= set(resources), "known resources")
            if task["kind"] == "devops":
                require(task["exclusiveResources"] == resources, "deployment lock ownership")
            else:
                require(task["exclusiveResources"] == [], "construction not serialized behind environment lock")
            require("passes in the deployed environment" in task["doneWhen"], "deployed task acceptance")
            require("DevOpsWorkLoop then EndToEndTestLoop" in task["handoff"], "continuous verification")
            covered.update(task["requirements"])
            components_seen.update(task["components"])
            flows_seen.update(task["flows"])
        require(covered == set(sprint["requirements"]), "sprint task coverage")
        requirements_seen.update(covered)
    require(requirements_seen == set(canonical), "D1-D7 coverage")
    require(components_seen == set(canonical.values()) and flows_seen == flows, "full solution coverage")

    def ancestors(graph, node, visiting=None):
        visiting = set() if visiting is None else visiting
        require(node in graph and node not in visiting, "known acyclic dependencies")
        result = set()
        for dependency in graph[node]:
            result.add(dependency)
            result.update(ancestors(graph, dependency, visiting | {node}))
        return result

    for node in sprint_graph:
        ancestors(sprint_graph, node)
    graph = {key: task["dependsOn"] for key, task in all_tasks.items()}
    for node in graph:
        ancestors(graph, node)
    skeleton = sprints[0]["tasks"][0]
    require(skeleton["walkingSkeleton"] is True and skeleton["kind"] == "devops"
            and skeleton["owner"] == "DevOps Engineer" and skeleton["dependsOn"] == [],
            "first dependency-free DevOps walking skeleton")
    require(sum(task["walkingSkeleton"] for task in all_tasks.values()) == 1, "one early skeleton")
    require("azd deploy" in skeleton["doneWhen"] and
            "separate successful deployed-probe check" in skeleton["handoff"] and
            "actual azd deploy command/exit evidence" in skeleton["handoff"], "actual deployment and probe contract")
    for task in sprints[0]["tasks"][1:]:
        require(skeleton["id"] in ancestors(graph, task["id"]), "skeleton prerequisite")


class DeliveryReleasePlanTests(unittest.TestCase):
    def setUp(self):
        self.plan = json.loads(ARTIFACT.read_text(encoding="utf-8"))

    def reject(self, mutate):
        candidate = deepcopy(self.plan)
        mutate(candidate)
        with self.assertRaises((ValueError, KeyError, TypeError)):
            validate_plan(candidate)

    def test_plan_schema_authority_and_full_coverage(self):
        validate_plan(self.plan)

    def test_requires_first_dependency_free_devops_skeleton(self):
        self.reject(lambda p: p["sprints"][0]["tasks"][0].update(walkingSkeleton=False))
        self.reject(lambda p: p["sprints"][0]["tasks"].reverse())
        self.reject(lambda p: p["sprints"][0]["tasks"][0].update(kind="developer", owner="Developer"))
        self.reject(lambda p: p["sprints"][0]["tasks"][0].update(dependsOn=["terminal-evidence-surface"]))

    def test_rejects_cycles_unknown_dependencies_and_skeleton_bypass(self):
        self.reject(lambda p: p["sprints"][0]["tasks"][1].update(dependsOn=[]))
        self.reject(lambda p: p["sprints"][0]["tasks"][2].update(dependsOn=["missing"]))
        self.reject(lambda p: p["sprints"][0]["tasks"][1].update(dependsOn=["coordinator-blob-contract"]))
        self.reject(lambda p: p["sprints"][0].update(dependsOn=["three-role-delivery"]))
        self.reject(lambda p: p["sprints"].append(deepcopy(p["sprints"][0])))

    def test_rejects_local_acceptance_missing_azd_evidence_or_probe(self):
        self.reject(lambda p: p["sprints"][0]["tasks"][0].update(handoff="Mention azd, no probe"))
        for index in range(len(self.plan["sprints"][0]["tasks"])):
            self.reject(lambda p, index=index: p["sprints"][0]["tasks"][index].update(doneWhen="Offline tests pass"))
            self.reject(lambda p, index=index: p["sprints"][0]["tasks"][index].update(handoff="Review now"))

    def test_rejects_missing_or_invented_requirement_component_flow(self):
        self.reject(lambda p: p["sprints"][0]["acceptanceCriteria"].pop())
        self.reject(lambda p: p["sprints"][0]["tasks"][1]["requirements"].append("D8"))
        self.reject(lambda p: p["sprints"][0]["tasks"][1]["components"].append("fourth-service"))
        self.reject(lambda p: p["sprints"][0]["tasks"][1].update(flows=["invented-flow"]))
        self.reject(lambda p: p["sprints"][0]["tasks"].pop(1))

    def test_rejects_mutable_candidate_lock_bypass_or_sprint_end_only_E2E(self):
        for key in ("candidate", "construction", "verification", "lock", "dependencyRelease",
                    "blockers", "unknownEffects", "gitReconciliation"):
            self.reject(lambda p, key=key: p["deliveryContract"].update({key: "bypass"}))
        self.reject(lambda p: p["sprints"][0]["tasks"][0].update(exclusiveResources=[]))
        self.reject(lambda p: p["sprints"][0]["tasks"][1].update(
            exclusiveResources=p["exclusiveResources"]))

    def test_rejects_scope_and_authority_expansion(self):
        self.reject(lambda p: p.update(environment="new-project"))
        self.reject(lambda p: p.update(planningOwner="Product Owner"))
        self.reject(lambda p: p["exclusions"].pop())
        self.reject(lambda p: p.update(maxSprints=1))
        self.reject(lambda p: p.update(runtimeDispositions=[]))

    def test_narrative_contains_scope_milestones_and_truthful_status(self):
        narrative = (ROOT / self.plan["design"]).read_text(encoding="utf-8")
        for phrase in ("planning schema pass is not deployed acceptance",
                       "separate deployed probe", "DevOpsWorkLoop then EndToEndTestLoop",
                       "Critical path", "Scrum Master", "account-wide Blob Contributor",
                       "Known-response retrieval is not resend"):
            self.assertIn(phrase, narrative)
        for task in self.plan["sprints"][0]["tasks"]:
            self.assertIn("`" + task["id"] + "`", narrative)
        for component in json.loads((ROOT / self.plan["architecture"]).read_text(
                encoding="utf-8"))["solutionModel"]["components"]:
            self.assertIn("| " + component["id"] + " |", narrative)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path)
    args = parser.parse_args()
    output = io.StringIO()
    result = unittest.TextTestRunner(stream=output, verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(DeliveryReleasePlanTests))
    exit_code = 0 if result.wasSuccessful() else 1
    report = (
        "Release planning checks only; no cloud operations or deployed acceptance.\n"
        "Command: python tests/test_delivery_release_plan.py --evidence "
        "docs/requirements/checks/delivery-release-plan.txt\n"
        "UTC: " + datetime.now(timezone.utc).isoformat() + "\n"
        "Artifact normalized UTF-8 (LF) SHA256: "
        + hashlib.sha256(ARTIFACT.read_text(encoding="utf-8").encode("utf-8")).hexdigest() + "\n"
        + output.getvalue() + "exitCode: " + str(exit_code) + "\n")
    print(report)
    if args.evidence:
        destination = args.evidence.resolve()
        require(destination.is_relative_to(ROOT / "docs/requirements/checks"), "public evidence path")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(report, encoding="utf-8")
    sys.exit(exit_code)
