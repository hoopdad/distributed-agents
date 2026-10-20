# Coordinator tier: RP-S1 continuity and acceptance architecture

Derived from the accepted release architecture and
[RP-S1 sprint architecture](../../customer-prototype-sprint-architecture.md).
This is a logical tier contract, not a new requirements source or deployment.

## Existing boundaries

- [`demo/host.py`](../../../demo/host.py) supplies request-aware workflow entry
  and checkpoint/resilient hosting.
- [`demo/workflow.py`](../../../demo/workflow.py) owns trusted parent begin,
  route, execute and publish, `manifest.children`, write-ahead operations and
  coordinator-only ETag/fencing acceptance.
- [`demo/foundry.py`](../../../demo/foundry.py) owns remote prepare/create/check,
  restored `AgentSession` invocation and exact-response recovery.
- [`demo/artifacts.py`](../../../demo/artifacts.py) and
  [`demo/artifact_store.py`](../../../demo/artifact_store.py) retain strict
  assignments, immutable prerequisites/proposals and scoped manifest adapters.

Never accept a model/session string as identity. Retain exact producer,
hash/revision, parent scope, pinned version, private-path and bounded routing
checks. Account-wide Blob Contributor means these role/parent restrictions
are application-enforced, not malicious-host or storage-RBAC isolation.

## Retained RP-S1 implementation contract

The integrated follow-up regression in
[`tests/test_workflow.py`](../../../tests/test_workflow.py), using the real MAF
graph and controlled remote/routing/storage boundaries, implements this contract.
Retain its stale candidate/review invalidation at the actual follow-up send.
Compare independent snapshots
of both role bindings before/after every invocation and final manifest:
hosted ID, framework `session_id`, stored hosted key, pinned name/version and
stable parent scope. Record creates separately; exactly two total.

Assert architect and reviewer both run on each turn, new response IDs for new
invocations, updated current requirements retaining private ingress plus queue,
and exact current final review acceptance. Do not freeze evolving framework
service-response state.

Retain `test_reject_revise_review_reuses_both_children_with_fresh_responses`:
architect -> blocked reviewer -> same architect revision -> same reviewer
through those same runtime/publication gates. Assert
four causal calls, two bindings, four fresh responses and c2's exact prerequisites.
Do not replace this with an in-process specialist implementation or a toy loop.
Fakes are explicitly offline; live AC1/AC2 remain independently required.

## Conditional identity repair boundary

Follow the [sprint identity discriminator](../../customer-prototype-sprint-architecture.md#identity-path-decision-contract-for-this-sprint).
A corrects only an observed supported authentication/configuration mismatch.
B derives delegation exclusively from authenticated server-side user context.
Neither is live-selected. `Assignment.validate_receiver()` must continue to
compare trusted child principal to parent `scope_binding.principal`; a changed
namespace is an Architect/PO contract decision, not permission to relax equality.
Opaque call IDs and assignment principal fields are never delegated identities.

Cover prepare/create/read/check/invoke/exact-response recovery consistently.
Separate specialist-only delegation from the shared `WorkflowRuntime.resources()`
project/header client if necessary; routing, parent, model and checkpoint context
must not inherit a child delegation by accident. Do not forward container-only
user headers or use the legacy two-header helper as an untested repair.
Negative controls must reject absent/forged identities and cross-parent access.
Required lab grants are authorized only with exact verified caller/target/action,
scoped rationale, deterministic execution and readback; no identity replacement.
Known binding/effect records remain immutable historical authority, not migratable
to a new namespace by inference.

## Recovery and handoff

Known hosted response recovery retrieves the exact response for the pinned
child, advances its framework continuation and sends nothing. Unknown effect,
expired/mismatched binding, uncertain creation and provenance failure stay held.
ETag conflict reconciles publication; it never triggers another model call.
Preserve existing crash/checkpoint/revision/isolation/transport cases.

Retained Developer doneWhen: strengthened two-turn and four-call fixtures establish
AC2/AC3's offline evidence and preserve existing regressions. Handoff includes
call-order snapshots, assertions and committed source/tests for integration.
This work is integrated in `6614440` / `24b883f`; Scrum Master assigns only
concrete deltas and Git reconciliation, not duplicate fixture implementation.
Exclusions: no new schema, generic session manager, identity bypass, live
acceptance claim or replay of historical held parents.
