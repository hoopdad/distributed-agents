# Client and release tier: current delivery sprint

Authority: [mission D1/F1 and D7](../delivery-mission.md).
Model and task joins: [SprintArchitecture](../delivery-sprint-architecture.json).
Main components: `deployment` and `terminal-demo`. No additional UI or service.

## Deployment contract

`azure.yaml` targets the existing project and exactly three hosted roles, with
Responses 2.0.0, Python 3.13 and `remote_build`. Its current three predeploy
hooks call `package_guard.py`, whose approval ZIP/hash/receipt contract conflicts
with F1. The `azd-walking-skeleton` DevOps task replaces only the normal path
with supported ordinary source/package exclusions, dependency and build checks.
Verify actual azd extension semantics; do not guess a new YAML/wire API.
Preserve `.dockerignore`, `.agentignore`, requirements/lock compatibility and
unused exact-package tools; no provisioning, infrastructure or private lab edits.

`exact-candidate-delivery` selects an exact committed revision/immutable artifact.
Actual azd outcome and a separate deployed probe must join that candidate to all
three actual hosted versions. DevOps then E2E serialize shared environment and
configuration resources through verification. No mutable unrelated checkout,
offline-only acceptance or dependent release before the skeleton deployed pass.

## Terminal contract

`demo/terminal.py`, `native_proxy.py` and `live_acceptance.py` implement
`design-review-revision`, `followup-and-recovery` and acceptance reporting.
Inherit [sprint terminal design](../delivery-sprint-design.json): machine stdout
unchanged, human view opt-in stderr, generated content treated as data,
exact private refs kept out of public summaries. Show advisory acceptance only
after validated current result and persisted finalization. Known-response
recovery retrieves; pending/unknown work never becomes a send permission.

Local targets: `tests/test_demo.py`, `tests/test_scenario_evidence.py`.
Mapped targets are not newly executed application evidence. DevOps/E2E must
exercise the actual terminal revision and same-parent follow-up, with seven
canonical evidence-backed RAG rows; model approval is not release acceptance.
