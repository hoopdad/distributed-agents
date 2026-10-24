# Specialist tier: current delivery sprint

Authority: [mission D3-D4 and F2-F3](../delivery-mission.md).
Model and task joins: [SprintArchitecture](../delivery-sprint-architecture.json).
Main components: `architect` and `reviewer`, exactly two remote deployments
alongside the coordinator; never hidden in-process production substitutes.

## Remote design and review

`demo/architect_agent.py:run_assignment` loads and validates the Blob assignment,
reads exact requirements plus prior design/review where assigned, restores the
architect's own `specialist_history_v2`, generates or recovers a known model
response and writes an immutable candidate before returning its reference.
`demo/reviewer_agent.py:run_assignment` independently reads exact requirements
and candidate, restores its own history and writes immutable findings/review.
`demo/specialist.py`, `demo/foundry.py` and `demo/artifacts.py` provide shared
typed/remote/session contracts; shared code is not a shared conversation.

Receiver validation binds genuine principal/project/tenant, role/name,
pinned version, hosted/framework child, active assignment, deadline and exact
prerequisites. Session IDs, model content and artifact documents grant no access.
Unknown model effects remain held; known response retrieval is not inference.

`design-review-revision` must yield actual first findings, a changed immutable
candidate addressing them, and review of that exact revision. Coordinator
publication validates producer/output/input joins before approval gates finish.
No manufactured finding, no-op revision or fabricated approval demonstrates F2.

Local targets: `tests/test_specialist_continuity.py`, `tests/test_workflow.py`,
`tests/test_artifacts.py`. DevOps/E2E must verify real remote calls, exact hashes
and producers, findings-to-revision joins and current blocker-free review.
Source presence and architecture checks are not remote acceptance. A current
trusted-user failure must be observed before diagnosing its cause; no guard
weakening, principal substitution or speculative transport remedy is selected.
