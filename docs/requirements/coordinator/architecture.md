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

## RP-S1 implementation contract

Extend the existing follow-up regression in
[`tests/test_workflow.py`](../../../tests/test_workflow.py), using the real MAF
graph and controlled remote/routing/storage boundaries. Before follow-up sends,
assert stale candidate/review refs are invalidated. Compare independent snapshots
of both role bindings before/after every invocation and final manifest:
hosted ID, framework `session_id`, stored hosted key, pinned name/version and
stable parent scope. Record creates separately; exactly two total.

Assert architect and reviewer both run on each turn, new response IDs for new
invocations, updated current requirements retaining private ingress plus queue,
and exact current final review acceptance. Do not freeze evolving framework
service-response state.

Add a controlled architect -> blocked reviewer -> same architect revision ->
same reviewer fixture through those same runtime/publication gates. Assert
four causal calls, two bindings, four fresh responses and c2's exact prerequisites.
Do not replace this with an in-process specialist implementation or a toy loop.
Fakes are explicitly offline; live AC1/AC2 remain independently required.

## Recovery and handoff

Known hosted response recovery retrieves the exact response for the pinned
child, advances its framework continuation and sends nothing. Unknown effect,
expired/mismatched binding, uncertain creation and provenance failure stay held.
ETag conflict reconciles publication; it never triggers another model call.
Preserve existing crash/checkpoint/revision/isolation/transport cases.

Developer doneWhen: strengthened two-turn and four-call fixtures establish
AC2/AC3's offline evidence and preserve existing regressions. Handoff includes
call-order snapshots, assertions and committed source/tests for integration.
Scrum Master assigns the shared test-file writer and Git reconciliation.
Exclusions: no new schema, generic session manager, identity bypass, live
acceptance claim or replay of historical held parents.
