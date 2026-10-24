"""Deterministically resolve the approved six-task sprint into dispatch-ready cards.

Planning only: no implementation dispatch, cloud operations or acceptance.
"""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / "docs/requirements/delivery-sprint-plan.json"
ESTIMATES = [
    (60, 15, 30),
    (60, 15, 30),
    (60, 15, 30),
    (40, 10, 30),
    (60, 15, 45),
    (20, 15, 45),
]
GOALS = [
    "Enable ordinary azd delivery and prove the early existing three-role skeleton.",
    "Verify trusted routing and private shared-artifact provenance; fix only demonstrated D2/D5 defects.",
    "Verify independent remote design and real findings-driven revision with exact-candidate review.",
    "Verify the existing terminal evidence surface against the accepted sprint design without changing stdout.",
    "Prove same-parent continuity, no-resend recovery and independent-parent isolation.",
    "Integrate the accepted candidates and demonstrate fresh deployed D1-D7 on the exact final revision.",
]


def load(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def resolve_plan():
    release = load("docs/requirements/delivery-release-plan.json")
    architecture = load("docs/requirements/delivery-sprint-architecture.json")
    design = load("docs/requirements/delivery-sprint-design.json")
    bindings = {binding["task"]: binding for binding in architecture["taskBindings"]}
    screens = {item["task"]: item for item in design["taskDesign"]}
    tasks = []
    for index, seed in enumerate(release["sprints"][0]["tasks"]):
        task = dict(seed)
        binding = bindings[task["id"]]
        task.update(
            estimatedMinutes=dict(zip(("implementation", "review", "integration"), ESTIMATES[index])),
            source=binding["source"],
            localTests=binding["localTests"],
            screens=screens[task["id"]]["screens"],
            construction=binding["construction"],
        )
        task["workCard"] = {
            "role": task["owner"],
            "action": task["title"],
            "goal": GOALS[index],
            "components": task["components"],
            "flows": task["flows"],
            "flowSteps": binding["flowSteps"],
            "doneWhen": task["doneWhen"],
            "failureCategories": [],
            "mustAct": task["owner"],
            "locations": binding["source"],
            "evidence": "",
            "cause": "",
            "verification": {"status": "not-yet-verified", "evidence": ""},
            "humanAction": "",
            "humanActionEvidence": "",
        }
        tasks.append(task)
    return {
        "schemaVersion": 1,
        "authority": release["authority"],
        "releasePlan": "docs/requirements/delivery-release-plan.json",
        "sprintArchitecture": "docs/requirements/delivery-sprint-architecture.json",
        "sprintDesign": "docs/requirements/delivery-sprint-design.json",
        "design": "docs/requirements/delivery-sprint-plan.md",
        "observedSource": "3df446cd4468822c32dfe755451a3c4f7155caf4",
        "featureBranch": release["featureBranch"],
        "sprint": architecture["sprint"],
        "scope": "dispatch-ready-planning-not-implementation-or-deployed-acceptance",
        "environment": release["environment"],
        "exclusiveResources": release["exclusiveResources"],
        "deliveryContract": release["deliveryContract"],
        "exclusions": release["exclusions"],
        "estimates": {
            "units": "minutes",
            "meaning": "rough-effort-not-limits-or-timeouts",
            "criticalPath": ["azd-walking-skeleton", "coordinator-blob-contract",
                             "continuity-recovery-isolation", "integrated-terminal-acceptance"],
            "tiedCriticalPath": ["azd-walking-skeleton", "remote-specialist-revision",
                                "continuity-recovery-isolation", "integrated-terminal-acceptance"],
            "dependencyLowerBoundMinutes": 410,
            "sharedVerificationContention": "additional-queue-time-not-in-DAG-lower-bound",
        },
        "dispatch": {
            "executor": "existing-SprintPlanLoop-dispatch-callback",
            "initialReady": ["azd-walking-skeleton"],
            "parallelAfterSkeleton": ["coordinator-blob-contract", "remote-specialist-revision",
                                      "terminal-evidence-surface"],
            "releaseGate": "deployed-pass-and-original-assignment-review",
            "constructionResources": [],
            "verificationResources": release["exclusiveResources"],
            "noNestedWorkflowOrDuplicateDispatch": True,
        },
        "assignments": {
            "AssignedWorkUIDeveloper": [],
            "AssignedWorkDeveloper": [task["id"] for task in tasks if task["kind"] == "developer"],
            "AssignedWorkDevOpsEngineer": [task["id"] for task in tasks if task["kind"] == "devops"],
            "AssignedWorkDesigner": [],
        },
        "tasks": tasks,
    }


if __name__ == "__main__":
    DESTINATION.write_text(json.dumps(resolve_plan(), indent=2, ensure_ascii=False) + "\n",
                           encoding="utf-8")
    print("Generated docs/requirements/delivery-sprint-plan.json; no assignments executed.")
