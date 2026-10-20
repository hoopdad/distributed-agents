# Specialist tier: RP-S1 direct model-history architecture

Derived from [RP-S1 sprint architecture](../../customer-prototype-sprint-architecture.md).
Architect and reviewer remain two separate existing hosted roles, not extra
tiers/services to deploy.

## Existing source and state

[`ArchitectAgent`](../../../demo/architect_agent.py) and
[`ReviewerAgent`](../../../demo/reviewer_agent.py) keep their explicit
five-stage run_assignment flows: connect/validate, read inputs, load history,
generate/recover, write immutable proposal. They do not acquire a dependency
on WorkflowRuntime or a generic session manager.

Each `load_or_create_llm_session()` loads `"history"` from
`AgentSessionStoreProvider(store_name="specialist_history_v2")` with its actual
hosting config/context. `design_solution()` / `review_solution()` pass that
restored session to `agent.run`. The hosted child response, framework service
continuation and internal model response are distinct observations.

The pending-model journal binds operation, input digest, deployment and response.
Known response retrieval advances the internal continuation without sending.
After exact immutable output writes, `store_design()` / `store_review()` clear
pending state and persist history. Existing-output recovery checks provenance
and reconciles history; it is not permission to generate another output.

## Retained RP-S1 proof boundary

[`tests/test_specialist_continuity.py`](../../../tests/test_specialist_continuity.py)
already implements the direct continuation/fresh-history/recovery fixtures
below for both real roles (`c454e50`, integrated by `24b883f`).
Retain these tests and their negative controls; source presence is not fresh
execution or live specialist success.

For each real role, use controlled external model/session-store/Blob adapters
but execute the actual load, model and store stages. Capture store config/context,
loaded framework ID/state/service continuation and the exact session supplied
to the model boundary. Complete a first operation, persist/reload history, and
invoke a second operation with its own pending journal and fresh response.
Check accepted assignment revisions/refs and history persistence, not prose.

Use a fresh/absent-history negative control with the same second brief: it must
not receive the first continuation. Independently compare both roles; success
for architect does not establish reviewer history. Full input replay, object
identity in a fake store, and convincing memory text cannot satisfy this proof.
Snapshot values rather than retaining mutable references.

For a known pending response, assert exact retrieve ID, zero model sends and
persisted continuation after output. Retain mismatch/unknown pending holds,
publication-crash history reconciliation and strict parsing/revision/provenance
cases in [`tests/test_workflow.py`](../../../tests/test_workflow.py).

## Ownership and doneWhen

Retained Developer handoff: both roles have direct continuation, fresh-history control
and no-resend recovery assertions with existing dependency pins. Coordinate
shared test-file ownership with the coordinator fixture work through Scrum Master.
Exclusions: no new history store/schema, model-memory claim from artifacts,
dependency upgrade without supported cause/compatibility, private evidence
in Git or live inference in this fixture task.

Historical missing trusted user fails before these stages execute. Passing
offline history tests does not repair that host gate or prove live MI Blob
operations. Supported-remedy research remains independent; remote accepted
outputs and private provenance must pass live AC1/AC5 G2-G3 downstream.

For either authorized A/B repair, preserve trusted platform identity and
`Assignment.validate_receiver()` principal/version/child/prerequisite checks.
A nonempty child user does not prove it matches the parent namespace.
If delegation changes that namespace, stop the candidate and use the existing
Architect/PO contract decision; do not trust the assignment's claimed identity,
rekey history or adopt held sessions under a different principal. Both roles'
hosted/framework and model-history boundaries require compatible identity
through creation, send and exact-response recovery. No specialist impersonation
grant is needed merely to receive a call. Required coordinator grants are
narrowly authorized and documented under the
[sprint decision contract](../../customer-prototype-sprint-architecture.md#identity-path-decision-contract-for-this-sprint);
permission presence/readback alone cannot prove specialist execution.
