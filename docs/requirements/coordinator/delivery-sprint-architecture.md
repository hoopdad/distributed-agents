# Coordinator tier: current delivery sprint

Authority: [mission D2/F2-F3 and D6/F4](../delivery-mission.md).
Model and task joins: [SprintArchitecture](../delivery-sprint-architecture.json).
Main components: `coordinator-routing` and
`session-continuity-recovery-isolation`.

## Routing and dispatch

`demo/host.py` constructs the graph in `demo/workflow.py`.
`WorkflowRuntime.begin/route/execute/publish` binds trusted context, appends
requirements, invalidates stale refs, validates deterministic prerequisites and
finish gates, journals effects and accepts exact outputs. `demo/routing.py`
and the calibrated corpus constrain genuine Decision-1 choices to the permitted
specialist action versus `request_input`; the model grants no authority.
Approval finishes deterministically; budget/deadline exhaustion is not success.

`design-review-revision` crosses the shared-artifact plane and independent
specialists: persist intent and exact assignment before dispatch, then validate
scope, producer/session/version/response, hashes, revisions and exact inputs
before coordinator lease/ETag publication. Real findings require a revised
design and current exact-candidate review without blockers.

## Continuity and recovery

`demo/foundry.py` restores each pinned child `AgentSession`; specialists retain
their separate model histories. `followup-and-recovery` changes requirements and
invalidates candidate/review, not child identity. Known responses are retrieved
without resend. Native checkpoints resume graph state; write-ahead records
reconcile effects; neither conversation nor checkpoint proves exactly-once.
Unknown effects remain held.

`independent-parent-isolation` derives a different trusted namespace and child
pair. No supplied ID authorizes another parent's refs. `live_acceptance.py`
joins real initial/followup/restart/isolated and stopped-session observations
with independent create/send captures. Only supported hosted-session compute
stop/resume is authorized, not VM power or forced state/version migration.

Local targets: `tests/test_workflow.py`, `tests/test_routing.py`,
`tests/test_specialist_continuity.py`, `tests/test_isolated_client.py`,
`tests/test_scenario_evidence.py`. These are mapped runtime targets, not live
results. DevOps/E2E must prove current trusted-user propagation, genuine choices,
stable bindings/history and recovery/isolation on the exact candidate.
No current evidence selects an identity remedy or major transport change.
