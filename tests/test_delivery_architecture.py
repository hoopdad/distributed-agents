"""Architecture contract checks, not live application acceptance."""

import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "docs/requirements/delivery-architecture.json"
MISSION = ROOT / "docs/requirements/delivery-mission.md"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def fields(value, required, optional=()):
    require(isinstance(value, dict), "object required")
    require(set(required) <= value.keys() <= set(required) | set(optional), "object fields")


def strings(value, nonempty=True):
    require(isinstance(value, list), "array required")
    require(not nonempty or bool(value), "nonempty array required")
    require(all(isinstance(item, str) and item.strip() for item in value), "strings required")
    require(len(set(value)) == len(value), "duplicate strings")


def public_file(value):
    require(isinstance(value, str), "path string required")
    path = PurePosixPath(value)
    require(not path.is_absolute() and ".." not in path.parts and "\\" not in value, "relative path")
    require(path.parts and path.parts[0] in {
        "docs", "tests", "demo", "config", "requirements.txt", "requirements.lock.txt",
        "azure.yaml", "package_guard.py", ".dockerignore", ".agentignore",
        "live_acceptance.py", "native_proxy.py",
    }, "public source path")
    require((ROOT / path).is_file(), "source/test file missing: " + value)


def validate_architecture(value):
    """Bounded schema plus mission joins; no claims about deployed behavior."""
    fields(value, (
        "schemaVersion", "authority", "design", "observedSource", "principles", "toolsets",
        "solutionModel", "contracts", "deliveryHandoff", "verification",
    ))
    require(type(value["schemaVersion"]) is int and value["schemaVersion"] == 1, "schema version")
    require(value["authority"] == "docs/requirements/delivery-mission.md", "mission authority")
    public_file(value["design"])
    require(re.fullmatch(r"[a-f0-9]{40}", value["observedSource"]) is not None, "source revision")
    strings(value["principles"])
    require(isinstance(value["toolsets"], list) and value["toolsets"], "toolsets")
    for tool in value["toolsets"]:
        fields(tool, ("name", "source", "purpose"))
        require(all(isinstance(item, str) and item.strip() for item in tool.values()), "tool text")
        public_file(tool["source"])

    canonical = dict(re.findall(
        r"^\| (D[1-7]) \| `([^`]+)` \|", MISSION.read_text(encoding="utf-8"), re.MULTILINE,
    ))
    require(len(canonical) == 7, "mission D1-D7")
    fields(value["solutionModel"], ("components", "flows"))
    components = value["solutionModel"]["components"]
    require(isinstance(components, list), "components array")
    ids = [component["id"] for component in components]
    require(len(ids) == len(set(ids)) and set(ids) == set(canonical.values()), "canonical components")
    requirements = set(canonical)
    for component in components:
        fields(component, ("id", "name", "supports", "requirements", "source", "localTests", "state", "remaining"))
        for key in ("id", "name", "remaining"):
            require(isinstance(component[key], str) and component[key].strip(), "component text")
        strings(component["supports"], nonempty=False)
        require(set(component["supports"]) <= set(ids) - {component["id"]}, "support reference")
        strings(component["requirements"])
        require(set(component["requirements"]) <= requirements, "component requirement")
        for key in ("source", "localTests"):
            strings(component[key])
            for path in component[key]:
                public_file(path)
                if key == "localTests":
                    require(path.startswith("tests/test_"), "test path")
        require(component["state"] in {"change-required", "source-present-live-unverified"}, "no invented live pass")

    flows = value["solutionModel"]["flows"]
    require(isinstance(flows, list) and flows, "flows")
    flow_ids, step_ids, covered = set(), set(), set()
    for flow in flows:
        fields(flow, ("id", "name", "trigger", "steps"), ("persona",))
        for key in ("id", "name", "trigger"):
            require(isinstance(flow[key], str) and flow[key].strip(), "flow text")
        require(flow["id"] not in flow_ids, "duplicate flow")
        flow_ids.add(flow["id"])
        require(isinstance(flow["steps"], list) and flow["steps"], "steps")
        for step in flow["steps"]:
            fields(step, ("id", "description", "components", "requirements"))
            require(isinstance(step["id"], str) and step["id"] and step["id"] not in step_ids, "unique step")
            step_ids.add(step["id"])
            require(isinstance(step["description"], str) and step["description"].strip(), "step description")
            strings(step["components"])
            require(set(step["components"]) <= set(ids), "step component reference")
            strings(step["requirements"])
            require(set(step["requirements"]) <= requirements, "step requirement")
            covered.update(step["requirements"])
    require(covered == requirements, "flow coverage")

    contracts = value["contracts"]
    fixed_contracts = {
        "roles": ["coordinator", "architect", "reviewer"],
        "productionSpecialists": "remote-only",
        "scopeAuthority": "trusted-hosting-context-with-genuine-end-user",
        "manifestWriter": "coordinator",
        "manifestConcurrency": "lease-etag-fenced",
        "outputs": "per-role-immutable",
        "finish": "exact-current-approving-review-without-blockers",
        "unknownEffects": "hold-no-replay",
        "storageIsolation": "application-enforced-not-per-role-rbac",
    }
    fields(contracts, (*fixed_contracts, "statePlanes", "containers", "identityAndNetwork", "compatibility"))
    for key, expected in fixed_contracts.items():
        require(contracts[key] == expected, "mission invariant: " + key)
    for key in ("identityAndNetwork", "compatibility"):
        require(isinstance(contracts[key], str) and contracts[key].strip(), "contract text")
    planes = contracts["statePlanes"]
    require(isinstance(planes, list) and len(planes) == 3, "three state planes")
    require(len({plane["name"] for plane in planes}) == 3, "distinct state planes")
    for plane in planes:
        fields(plane, ("name", "source", "contract"))
        public_file(plane["source"])
        require(isinstance(plane["contract"], str) and plane["contract"].strip(), "state plane contract")
    containers = contracts["containers"]
    require(isinstance(containers, list) and len(containers) == 3, "three containers")
    require({item["logicalName"]: item["writer"] for item in containers} == {
        "control": "coordinator", "candidates": "architect", "reviews": "reviewer",
    }, "per-role container ownership")
    for container in containers:
        fields(container, ("logicalName", "writer", "purpose"))
        require(isinstance(container["purpose"], str) and container["purpose"].strip(), "container purpose")

    handoff = value["deliveryHandoff"]
    fields(handoff, ("planningOwner", "firstSprint", "deploymentCommand", "exclusiveResources",
                     "candidate", "acceptance", "continuation", "exclusions"))
    require(handoff["planningOwner"] == "Scrum Master", "planning ownership")
    require(handoff["firstSprint"] == {
        "walkingSkeleton": True, "kind": "devops", "owner": "DevOps Engineer",
        "dependsOn": [], "otherTasksTransitivelyDependOnSkeleton": True,
    }, "skeleton prerequisites")
    require(handoff["deploymentCommand"] == "azd deploy", "existing infrastructure only")
    strings(handoff["exclusiveResources"])
    strings(handoff["exclusions"])
    require(set(handoff["exclusions"]) >= {
        "infrastructure-provisioning", "rbac-network-dns-quota-mutation", "vm-power",
        "secret-retrieval", "vpn-operations", "private-lab-edits", "fourth-role",
        "production-local-fallback", "unknown-effect-replay", "git-push",
    }, "authority exclusions")
    for key in ("candidate", "acceptance", "continuation"):
        require(isinstance(handoff[key], str) and handoff[key].strip(), "handoff text")

    verification = value["verification"]
    require(isinstance(verification, list) and len(verification) == 7, "verification coverage")
    require({check["requirement"] for check in verification} == requirements, "D1-D7 checks")
    for check in verification:
        fields(check, ("requirement", "component", "localTests", "deployedProof", "status"))
        require(canonical[check["requirement"]] == check["component"], "canonical verification binding")
        strings(check["localTests"])
        for path in check["localTests"]:
            public_file(path)
            require(path.startswith("tests/test_"), "verification test path")
        require(isinstance(check["deployedProof"], str) and check["deployedProof"].strip(), "deployed criterion")
        require(check["status"] == "not-executed", "no unobserved deployed success")


class DeliveryArchitectureTests(unittest.TestCase):
    def setUp(self):
        self.architecture = json.loads(ARTIFACT.read_text(encoding="utf-8"))

    def test_full_architecture_contract_and_mission_coverage(self):
        validate_architecture(self.architecture)

    def reject(self, mutate):
        candidate = deepcopy(self.architecture)
        mutate(candidate)
        with self.assertRaises((ValueError, KeyError, TypeError)):
            validate_architecture(candidate)

    def test_rejects_missing_duplicate_or_invented_components(self):
        self.reject(lambda value: value["solutionModel"]["components"].pop())
        self.reject(lambda value: value["solutionModel"]["components"].append(
            deepcopy(value["solutionModel"]["components"][0])))
        self.reject(lambda value: value["solutionModel"]["components"][0].update(id="fourth-service"))

    def test_rejects_dangling_support_and_flow_references(self):
        self.reject(lambda value: value["solutionModel"]["components"][0]["supports"].append("missing"))
        self.reject(lambda value: value["solutionModel"]["flows"][0]["steps"][0]["components"].append("missing"))
        self.reject(lambda value: value["solutionModel"]["flows"][0]["steps"][0].update(requirements=["D8"]))
        self.reject(lambda value: value["solutionModel"]["flows"].append(
            deepcopy(value["solutionModel"]["flows"][0])))

    def test_rejects_missing_sources_and_private_or_traversal_paths(self):
        for path in ("demo/not-present.py", "../outside.py", ".local/settings.json", "/tmp/file"):
            self.reject(lambda value, path=path: value["solutionModel"]["components"][0].update(source=[path]))

    def test_rejects_waived_identity_ownership_recovery_or_finish_contracts(self):
        for key in ("roles", "productionSpecialists", "scopeAuthority", "manifestWriter",
                    "manifestConcurrency", "outputs", "finish", "unknownEffects", "storageIsolation"):
            self.reject(lambda value, key=key: value["contracts"].update({key: "waived"}))
        self.reject(lambda value: value["contracts"]["containers"][1].update(writer="reviewer"))

    def test_rejects_provisioning_missing_lock_and_broken_skeleton_handoff(self):
        self.reject(lambda value: value["deliveryHandoff"].update(deploymentCommand="azd up"))
        self.reject(lambda value: value["deliveryHandoff"].update(exclusiveResources=[]))
        self.reject(lambda value: value["deliveryHandoff"]["firstSprint"].update(dependsOn=["later-task"]))
        self.reject(lambda value: value["deliveryHandoff"]["firstSprint"].update(
            otherTasksTransitivelyDependOnSkeleton=False))
        self.reject(lambda value: value["deliveryHandoff"]["exclusions"].remove("unknown-effect-replay"))

    def test_rejects_missing_checks_wrong_requirement_bindings_and_invented_live_pass(self):
        self.reject(lambda value: value["verification"].pop())
        self.reject(lambda value: value["verification"][0].update(component="architect"))
        self.reject(lambda value: value["verification"][0].update(status="passed"))
        self.reject(lambda value: value["solutionModel"]["components"][1].update(state="live-verified"))

    def test_rejects_unknown_schema_fields(self):
        self.reject(lambda value: value.update(runtimeDisposition="approved"))

    def test_narrative_links_model_and_preserves_acceptance_limitations(self):
        text = (ROOT / self.architecture["design"]).read_text(encoding="utf-8")
        for required in ("delivery-architecture.json", "delivery-mission.md",
                         "not deployed application acceptance", "account-wide Blob Contributor",
                         "DevOps deploys that exact candidate", "No added exhaustion/disposition gates"):
            self.assertIn(required, text)
        for component in self.architecture["solutionModel"]["components"]:
            self.assertIn("| " + component["id"] + " |", text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path)
    args = parser.parse_args()
    output = io.StringIO()
    result = unittest.TextTestRunner(stream=output, verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(DeliveryArchitectureTests)
    )
    report = (
        "Architecture contract checks only; no cloud operations or live acceptance.\n"
        + "UTC: " + datetime.now(timezone.utc).isoformat() + "\n"
        + "Artifact normalized UTF-8 (LF) SHA256: "
        + hashlib.sha256(ARTIFACT.read_text(encoding="utf-8").encode("utf-8")).hexdigest() + "\n"
        + output.getvalue()
        + "exitCode: " + str(0 if result.wasSuccessful() else 1) + "\n"
    )
    print(report)
    if args.evidence:
        destination = args.evidence.resolve()
        require(destination.is_relative_to(ROOT / "docs/requirements/checks"), "public check evidence path")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(report, encoding="utf-8")
    sys.exit(0 if result.wasSuccessful() else 1)
