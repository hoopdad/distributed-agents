"""Bounded UX contract validation; no remote execution or product acceptance."""

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
ARTIFACT = ROOT / "docs/requirements/delivery-user-experience.json"


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def fields(value, names):
    require(isinstance(value, dict) and set(value) == set(names.split()), "object fields")


def text(value):
    require(isinstance(value, str) and bool(value.strip()), "nonempty text")


def strings(value):
    require(isinstance(value, list) and bool(value), "nonempty array")
    for item in value:
        text(item)
    require(len(value) == len(set(value)), "unique strings")


def public_file(value):
    text(value)
    path = PurePosixPath(value)
    require(not path.is_absolute() and ".." not in path.parts and "\\" not in value, "relative file")
    require(path.parts[0] in {"docs", "demo", "tests", "live_acceptance.py"}, "public file")
    require((ROOT / path).is_file(), "existing file")


def validate_ux(value):
    fields(value, "schemaVersion authority architecture design observedSource scope principles "
           "toolsets presentation flows states handoff")
    require(type(value["schemaVersion"]) is int and value["schemaVersion"] == 1, "schema version")
    require(value["authority"] == "docs/requirements/delivery-mission.md", "mission authority")
    require(value["architecture"] == "docs/requirements/delivery-architecture.json", "architecture join")
    require(value["design"] == "docs/requirements/delivery-user-experience.md", "UX narrative")
    for key in ("authority", "architecture", "design"):
        public_file(value[key])
    require(re.fullmatch(r"[a-f0-9]{40}", value["observedSource"]) is not None, "source revision")
    require(value["scope"] == "terminal-direction-only-not-deployed-acceptance", "bounded scope")
    mission = (ROOT / value["authority"]).read_text(encoding="utf-8")
    canonical = dict(re.findall(r"^\| (D[1-7]) \| `([^`]+)` \|", mission, re.MULTILINE))
    require(len(canonical) == 7, "canonical mission coverage")
    architecture = json.loads((ROOT / value["architecture"]).read_text(encoding="utf-8"))

    def requirements(items):
        strings(items)
        require(set(items) <= set(canonical), "original requirement references")

    require(isinstance(value["principles"], list) and bool(value["principles"]), "principles")
    for principle in value["principles"]:
        fields(principle, "name requirements direction")
        text(principle["name"])
        text(principle["direction"])
        requirements(principle["requirements"])
    require(isinstance(value["toolsets"], list) and bool(value["toolsets"]), "toolsets")
    for tool in value["toolsets"]:
        fields(tool, "name source purpose")
        text(tool["name"])
        text(tool["purpose"])
        public_file(tool["source"])

    presentation = value["presentation"]
    fixed = {
        "framework": "existing-terminal-progressive-disclosure",
        "stdout": "unchanged-machine-records",
        "human": "opt-in-stderr",
        "theme": "inherit-terminal-no-forced-colors",
        "generatedContent": "prefixed-control-neutralized-width-wrapped-data",
        "privacy": "aliases-in-human-view-exact-refs-in-authorized-private-evidence",
        "releaseClaim": "none-without-fresh-D1-D7",
        "rag": {
            "green": "fresh-component-end-to-end-pass-exact-candidate-intended-environment",
            "amber": "partial-not-executed-not-verified-or-stale",
            "red": "current-evidenced-failure-or-blocking-criterion",
        },
        "reportColumns": ["Component", "RAG", "Evidence (revision/run/environment + freshness)",
                          "Remaining work/next action"],
    }
    fields(presentation, " ".join(fixed) + " reportComponents screens")
    for key, expected in fixed.items():
        require(presentation[key] == expected, "presentation invariant: " + key)
    strings(presentation["reportComponents"])
    require(set(presentation["reportComponents"]) == set(canonical.values()), "seven component rows")
    screens = presentation["screens"]
    require(isinstance(screens, list) and len(screens) == 3, "three existing surface directions")
    require({item["id"] for item in screens} == {
        "terminal-turn", "terminal-exception", "component-report",
    }, "screen scope")
    screen_coverage = set()
    for screen in screens:
        fields(screen, "id requirements regions")
        strings(screen["regions"])
        requirements(screen["requirements"])
        screen_coverage.update(screen["requirements"])
    require(screen_coverage == set(canonical), "screen requirement coverage")

    flows = value["flows"]
    expected = {flow["id"]: flow for flow in architecture["solutionModel"]["flows"]}
    require(isinstance(flows, list) and len(flows) == len(expected), "all architecture flows")
    require({flow["id"] for flow in flows} == set(expected), "flow identity")
    for flow in flows:
        fields(flow, "id persona trigger steps requirements direction return")
        for key in ("persona", "trigger", "direction", "return"):
            text(flow[key])
        strings(flow["steps"])
        require(flow["steps"] == [step["id"] for step in expected[flow["id"]]["steps"]],
                "exact ordered architecture steps")
        requirements(flow["requirements"])
        require(set(flow["requirements"]) == {
            requirement for step in expected[flow["id"]]["steps"]
            for requirement in step["requirements"]
        }, "architecture requirement coverage")

    gates = {
        "ready": ("submit", "authenticated-new-or-completed-nonheld-parent"),
        "streaming": ("observe", "pending-no-additional-send"),
        "accepted-advisory": ("followup", "completed-nonheld-current-parent"),
        "request-input": ("clarify", "completed-nonheld-current-parent"),
        "routing-hold": ("inspect", "preserve-state-no-automatic-retry"),
        "limit-reached": ("inspect", "preserve-state-no-automatic-retry"),
        "known-pending-response": ("retrieve-known", "persisted-known-response-no-resend"),
        "unknown-effect": ("reconcile", "hold-no-replay"),
        "failed-or-invalid": ("inspect", "preserve-state-no-automatic-retry"),
    }
    states = value["states"]
    require(isinstance(states, list) and len(states) == len(gates), "state coverage")
    require({state["id"] for state in states} == set(gates), "state identity")
    for state in states:
        fields(state, "id requirements display action gate")
        requirements(state["requirements"])
        text(state["display"])
        require((state["action"], state["gate"]) == gates[state["id"]], "safe state action gate")

    handoff = value["handoff"]
    expected_handoff = {
        "scope": "design-artifacts-and-local-contract-checks-only",
        "implementationOwner": "Developer",
        "planningOwner": "Scrum Master",
        "verificationOwners": ["DevOps Engineer", "End-to-End Tester"],
        "candidate": "exact-committed-feature-revision",
        "deployment": "existing-DevOps-then-E2E-under-environment-lock",
        "acceptance": "schema-pass-completes-UX-direction-not-product-acceptance",
        "exclusions": ["new-web-ui", "new-service", "theme-toggle", "stdout-protocol-change",
                       "auth-weakening", "unknown-effect-replay", "infrastructure-mutation",
                       "new-approval-stage"],
    }
    require(handoff == expected_handoff, "existing handoff and authority boundaries")


class DeliveryUserExperienceTests(unittest.TestCase):
    def setUp(self):
        self.ux = json.loads(ARTIFACT.read_text(encoding="utf-8"))

    def reject(self, mutate):
        candidate = deepcopy(self.ux)
        mutate(candidate)
        with self.assertRaises((ValueError, KeyError, TypeError)):
            validate_ux(candidate)

    def test_full_ux_schema_and_mission_architecture_joins(self):
        validate_ux(self.ux)

    def test_rejects_missing_invented_or_duplicate_component_rows(self):
        self.reject(lambda x: x["presentation"]["reportComponents"].pop())
        self.reject(lambda x: x["presentation"]["reportComponents"].append("dashboard"))
        self.reject(lambda x: x["presentation"]["reportComponents"].append("architect"))

    def test_rejects_missing_flows_wrong_steps_and_requirement_expansion(self):
        self.reject(lambda x: x["flows"].pop())
        self.reject(lambda x: x["flows"][0]["steps"].reverse())
        self.reject(lambda x: x["flows"][0]["requirements"].append("D8"))
        self.reject(lambda x: x["flows"][0]["requirements"].remove("D4"))
        self.reject(lambda x: x["flows"].__setitem__(1, deepcopy(x["flows"][0])))

    def test_rejects_unfounded_green_historical_red_or_protocol_changes(self):
        self.reject(lambda x: x["presentation"]["rag"].update(green="sdk-completed"))
        self.reject(lambda x: x["presentation"]["rag"].update(red="historical-failure"))
        self.reject(lambda x: x["presentation"].update(stdout="new-human-summary"))
        self.reject(lambda x: x["presentation"].update(releaseClaim="approved-model-text"))
        self.reject(lambda x: x["presentation"].update(privacy="print-private-paths"))

    def test_rejects_resend_uncertain_followup_and_weakened_state_gates(self):
        for index in range(len(self.ux["states"])):
            self.reject(lambda x, index=index: x["states"][index].update(gate="always"))
        for state_id in ("unknown-effect", "known-pending-response", "streaming"):
            self.reject(lambda x, state_id=state_id: next(
                state for state in x["states"] if state["id"] == state_id
            ).update(action="submit"))
        self.reject(lambda x: x["states"].pop())

    def test_rejects_new_screens_private_paths_and_missing_sources(self):
        self.reject(lambda x: x["presentation"]["screens"][0].update(id="web-dashboard"))
        self.reject(lambda x: x["presentation"]["screens"][0].update(regions=[]))
        for path in (".local/settings.json", "../outside.py", "/tmp/file", "demo/not-present.py"):
            self.reject(lambda x, path=path: x["toolsets"][0].update(source=path))

    def test_rejects_scope_changes_or_local_only_product_acceptance(self):
        self.reject(lambda x: x.update(scope="new-web-product"))
        self.reject(lambda x: x["handoff"].update(acceptance="local-tests-release-dependents"))
        self.reject(lambda x: x["handoff"].update(deployment="designer-deploys"))
        self.reject(lambda x: x["handoff"]["exclusions"].remove("auth-weakening"))
        self.reject(lambda x: x.update(runtimeDisposition="approved"))

    def test_narrative_covers_flows_states_and_truthful_existing_surface(self):
        narrative = (ROOT / self.ux["design"]).read_text(encoding="utf-8")
        for phrase in ("not deployed application acceptance", "unchanged machine records",
                       "account-wide Blob Contributor", "Known-response retrieval is not resend",
                       "No forced ANSI colors", "not a live phase dashboard",
                       "schema checks, not remote behavior tests"):
            self.assertIn(phrase.lower(), narrative.lower())
        for flow in self.ux["flows"]:
            self.assertIn("`" + flow["id"] + "`", narrative)
        for component in self.ux["presentation"]["reportComponents"]:
            self.assertIn("| " + component + " |", narrative)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path)
    args = parser.parse_args()
    output = io.StringIO()
    result = unittest.TextTestRunner(stream=output, verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(DeliveryUserExperienceTests)
    )
    exit_code = 0 if result.wasSuccessful() else 1
    report = (
        "UX contract checks only; no cloud operations or deployed acceptance.\n"
        "Command: python tests/test_delivery_user_experience.py --evidence "
        "docs/requirements/checks/delivery-user-experience.txt\n"
        + "UTC: " + datetime.now(timezone.utc).isoformat() + "\n"
        + "Artifact normalized UTF-8 (LF) SHA256: "
        + hashlib.sha256(ARTIFACT.read_text(encoding="utf-8").encode("utf-8")).hexdigest() + "\n"
        + output.getvalue() + "exitCode: " + str(exit_code) + "\n"
    )
    print(report)
    if args.evidence:
        destination = args.evidence.resolve()
        require(destination.is_relative_to(ROOT / "docs/requirements/checks"), "public evidence path")
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(report, encoding="utf-8")
    sys.exit(exit_code)
