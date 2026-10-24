# Shared-artifact tier: current delivery sprint

Authority: [mission D5/F3 and D6/F4](../delivery-mission.md).
Model and task joins: [SprintArchitecture](../delivery-sprint-architecture.json).
Main component: `blob-shared-context`, one shared support plane, not another
hosted role. It supports coordinator, specialists and continuity.

## Immutable documents and publication

`demo/artifacts.py` defines trusted `ScopeBinding`, typed artifact/assignment
refs, revisions, hashes and producer bindings. `demo/artifact_store.py` verifies
configured private DNS/IP bindings, accesses Blob with managed identity, writes
role outputs immutably and protects coordinator manifest publication with
lease/ETag fencing. `demo/config.py` validates the allowlisted settings.

The `control` container holds coordinator requirements, decisions, assignments,
child refs, operation records and manifest. Only architect writes `candidates`;
only reviewer writes `reviews`. Exact requirement/candidate/prior-review refs
travel in assignments; specialists return exact output refs for coordinator
validation, not arbitrary text to be accepted.

`design-review-revision`, `followup-and-recovery` and
`independent-parent-isolation` share this support. The parent-scoped manifest
retains child bindings; each new requirements revision invalidates stale
candidate/review approval. Write-ahead prepared/dispatched/response/accepted
transitions reconcile side effects separately from MAF checkpoints. Unknown
effects remain explicit holds, never erased or replayed.

Existing account-wide Blob Contributor means role ownership is
application-enforced, not storage-enforced per-role isolation. No new RBAC,
network, DNS, container provisioning or secret retrieval is authorized.

Local targets: `tests/test_artifacts.py`, `tests/test_config.py`,
`tests/test_workflow.py`, `tests/test_scenario_evidence.py`. DevOps/E2E must
capture actual private-path MI reads/writes and immutable provenance/fencing for
the same deployed candidate. Caller-supplied snapshot consistency alone proves
neither capture completeness nor live access. Keep raw refs/identities private;
public evidence records sanitized outcomes only.
