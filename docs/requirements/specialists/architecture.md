# Specialist tier: cumulative RP-S1/RP-S2/RP-S3 history and ingress architecture

## RP-S3 repeated calls and model-history boundary

The [RP-S3 state comparisons](../../customer-prototype-sprint-architecture.md#stable-identity-advancing-work-and-independent-state)
retain each real specialist's five-stage flow and `specialist_history_v2`.
The remote child's hosted/framework binding and pinned version are distinct
from its internal model session and advancing response continuation. Both roles
must execute on initial and queue follow-up turns with their original bindings,
new invocation responses and exact current immutable requirements/candidate
refs; receiver principal equality remains mandatory at every call.

Retain both-role actual load/model/store fixtures, persisted value snapshots,
identical-brief fresh-history negative controls and exact-response zero-send
recovery. Replayed requirements or persuasive memory prose cannot demonstrate
restored model history. These fixtures establish the controlled offline
boundary, not successful live ingress or model continuation.

After supported coordinator compute stop/resume, reuse the original children
and their compatible history; do not rekey, recreate or adopt held sessions.
Reconcile known model responses without another model send and immutable output
with pending history before claiming no duplicates. Missing observations or
unknown effects remain held. A separate parent must have distinct child/history
scope and no first-parent requirements in its accepted output. Application
checks under account-wide Blob access are not malicious-host storage isolation.
No new specialist service, history schema, grant, endpoint or identity repair
is introduced; actual G1-G4 entry remains a separate prerequisite.

## RP-S2 observed ingress is a separate boundary

Use the [current cumulative joins](../../customer-prototype-sprint-architecture.md#preparation-execution-and-acceptance-joins)
without rewriting either specialist's five-stage lifecycle. Retain accepted
history/fresh-history/no-resend fixtures and installed B caller isolation.
Neither candidate review nor an authenticated transport establishes specialist
entry. Record reached and unreached roles separately: architect trusted entry
and receiver success precede reviewer dispatch; reviewer success requires its
own observed result and exact accepted architect prerequisites.

Preparation rejection has no receiver result; unknown observation must remain
unknown. If the actual child principal differs from the trusted parent binding,
stop and retain the exact private evidence for existing Architect/PO/Scrum
reconciliation. Do not relax equality, rekey history, adopt held sessions or
add a diagnostic endpoint. An ingress success is not direct model-history,
private MI Blob or accepted-output proof; those gates remain separately required.

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

### RP-S2 compatibility boundary, not a specialist rewrite

The isolated candidate is coordinator-owned; it does not change either role's
history-store construction, five-stage flow or `Assignment.validate_receiver()`.
The installed `3aca5dc` B client is not successful live selection. Resource
preparation rejection at the coordinator does not show that either receiver
was reached. Record a receiver failure only from an observed child result;
unreached roles and missing observations remain explicitly unverified/unknown.
Retain both roles' existing continuation/fresh-history/no-resend fixtures when
the candidate changes callers. The live discriminator must establish actual
trusted ingress **and** successful receiver validation per reached role before
claiming identity compatibility; a user-presence flag or model-generated
identity assertion cannot do so. Architect success does not imply reviewer
entry. Do not create a diagnostic endpoint, rekey history or import tooling.

A missing/changed child principal rejects the candidate. Record the exact
reached gate and private binding locator; carry an evidenced namespace mismatch
to existing Architect-advised PO/Scrum scope reconciliation. Old pinned sessions
and held operations are not adopted by a new candidate. Application-enforced
scope ownership under account-wide Blob Contributor remains a disclosed
limitation, not a claim of storage-RBAC isolation.

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
