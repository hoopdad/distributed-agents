# Client and release boundary: RP-S1 projection and evidence architecture

Derived from [RP-S1 sprint architecture](../../customer-prototype-sprint-architecture.md)
and the accepted [SprintDesign](../../customer-prototype-sprint-design.md).
This logical tier adds neither a service nor a release owner.

## Presentation contract

[`demo/terminal.py`](../../../demo/terminal.py) remains the Windows terminal.
`--native --view human` is implemented (`56b762e`, integrated by `24b883f`).
Retain the opt-in, finalization-evaluated view on stderr; identical input keeps identical stdout,
existing default behavior, delegation/result schemas and
[`live_acceptance.py`](../../../live_acceptance.py) parsing unchanged.

This is one finalized summary, not streaming or invented intermediate findings.
Use complete parsed records, preserve repeated calls in order, and finalize
before an accepted summary. Fragmented/recovered prefixes cannot become duplicate
invocations; missing/multiple/malformed results or pending effects cannot become
success. Known-response retrieval is not a new send. Human content includes
current useful design and review findings, not only session labels.

Existing public events expose aliases, not enough exact evidence for a VERIFIED
continuity or creation-count assertion. With those events alone display
unverified/not observed. Do not add raw IDs, external reads or another comparison
ledger just to strengthen the display. Private acceptance compares exact actual
bindings separately. Neutralize terminal controls and prefix every generated
line; support narrow widths and non-color status labels.

[`README.md`](../../../README.md) opens with customer goal, three-role diagram,
two-turn example, stable bindings versus advancing responses, source path and
truthful historical live status. Keep chronology in the recovery plan.
Shareable commands use synthetic input, private state, safe aliases and only
implemented syntax. Follow-up requires a completed, non-held first turn.

Retained Developer doneWhen: implemented view/README plus fixtures for stdout/parser
compatibility, missing evidence, fragmented/recovered streams, finalization,
holds and hostile/multiline content. Designer reviews against accepted screens.
Do not redispatch that integrated implementation. No browser UI, parser
replacement, live success from aliases or CLI stop command.

## Fresh inventory and supported-remedy research

DevOps validates sole-target settings/linkage and authenticated lab context
without displaying private values, then records fresh versions, identities,
packages, rollback and unresolved operations through retained tools.
Architect/Developer research source/date/version-specific supported remedies;
historical matching call context/missing trusted user is unresolved, not proof
of missing RBAC or a provider defect.

Use the [sprint A/B/unresolved decision contract](../../customer-prototype-sprint-architecture.md#identity-path-decision-contract-for-this-sprint)
and accepted release architecture, including trusted namespace compatibility at
every SDK lifecycle boundary. Neither path is currently live-proven.
The prior bounded remedy research is retained but does not dispose of the newly
authorized delegation path. Necessary lab RBAC/permission changes for a supported
path are already authorized when exact scope and rationale are documented.
Resolve the actual caller/targets/effective action first; avoid duplicate grants.
Reviewed deterministic lab scripts own plan/write/readback and unknown holds.
No new infrastructure, identities or broad convenience roles are authorized.

Research/decision doneWhen: supported correction with a concrete reproducer and held-state
implications, or actionable negative finding specifying the missing exact-pair
caller-resolution trace/documented remedy after evaluating the supported
alternatives. Record selected-A/selected-B/unresolved, actual tests, exact private
evidence locators, principal compatibility, permission scope/rationale, held
effects and closing action. No provider submission/private transfer,
speculative publication, unrelated permission/network/infra or uncertain-effect replay.
Completed research does not pass the live release goal.

## Release ownership and later gates

### RP-S2 deterministic local runner: implementation contract

The accepted [decision-runner design](../../customer-prototype-architecture.md#deterministic-decision-runner-contract)
is required behavior, not an implemented CLI. `scripts/identity_handoff.py`
remains offline-only. The SprintPlan assigns Developer to implement the runner;
original DevOps retains its live execution and package/publication ownership.
Develop the retained lab runner
independently of runtime coding and fresh inventory, with these joined inputs:
absolute application/lab roots and validated Python, explicit `A-correction`
or `B-candidate` scenario, reviewed source/common package/exact role versions,
fresh context/inventory and private evidence destination outside both repos.
No new deployment owner or acceptance ledger is introduced.

The [current source-to-trial contract](../../customer-prototype-architecture.md#source-identity-is-part-of-the-scenario-contract)
is mandatory at integration: `3aca5dc` installs unconditional B specialist
delegation, not an A/B switch. Reject a scenario that does not match the actual
reviewed source/package/role versions before dispatch. A requires its own
evidenced corrected source, not relabeling B or retrying unchanged opaque A.
Distinguish local resource-preparation rejection from observed remote receiver
failure; missing observation remains unknown. No automatic fallback or held-parent
adoption is introduced.

| Phase | Fail-closed contract |
|---|---|
| Preflight | Use only application settings loader/native settings; verify sole target and dedicated authenticated context; read back actual caller/effective grants and rollback/held records |
| Ownership | Serialize actual publisher/CLI/transport/mount mutation across runs; scheduler names alone are insufficient; journal intended effects and exact bindings before dispatch |
| Finite trial | Predeclare one fresh synthetic parent and architect-then-reviewer sequence using existing assignments/exact prerequisites; reviewer waits for trusted architect entry/receiver success; retain routing/deadline/admission budgets |
| Observation/recovery | Bind private actual role/version/parent/child/framework/response/artifact scope; public presence/match/entry classes only; known exact response retrieval sends nothing; absent observation stays unknown |
| Stop/result | Missing/changed principal, receiver failure, version drift or uncertain create/send holds; return selected-A/selected-B/unresolved, reached/unreached roles, permission delta/readback, private locators, owned cleanup and next action |

Offline runner tests cover competing owner, failure before/after dispatch,
unknown publication/create/send, known-response zero-send inspection, redaction
and partial-role results. Extend retained App/Observe tools if necessary;
never substitute ad hoc commands or an unprotected diagnostic endpoint.
Reviewed runtime and tooling integrate before any trial, followed by exact
source/Linux/package gates and retained preview/publication in DevOps.
Only a demonstrated necessary permission delta adds scripted plan/write/readback
as a dependency. Permission readback is not runtime success. No unchanged A
retry, automatic path fallback or automatic new parent after failure is permitted.

Scrum assigns actual lab file/Git ownership before writing: the observed shared
lab branch has unrelated dirty work and must not be switched under writers.
Keep reviewed task commits or durably record task, retained branch, commits
and abandonment reason on the feature branch. This implementation handoff
does not move formal E2E validation or DevOps cloud-pass into architecture.

Formal integration validation remains in the original E2E loop. Bounded scripted
decision tests during architecture/planning establish selection evidence only.
Use local repository scripts for E2E and DevOps, never GitHub Actions; a needed
deployment still follows DevOps source/Linux/package gates and retained publisher.
Original DevOps exclusively owns retained packaging, preview, WSL publication
and cloud-pass with explicit ApplicationRoot/LabRepositoryRoot. Serialize
publisher/shared CLI/stage and transport/mount resources. Preserve strict SSH,
read-only mount, private evidence outside both repositories, exact source/settings/
ZIP hashes, allowlists, dependency provenance, actual Linux/amd64/hosting-Python
checks, unchanged identities, rollback versions and owned cleanup.

RP-S2 requires one final common three-role bundle, real remote accepted outputs,
private MI artifact provenance and genuine Decision-1 (G1-G4). RP-S3 requires
exact two-turn binding/response proof (G5), once-only supported compute stop/resume
with marker and confirmed stopped/idle state/no duplicate effects (G6), distinct
parent children/artifact scope (G7), and truthful closure (G8). This is not
hard-crash or exactly-once deployment certification.

Final AC1-AC9 reporting distinguishes offline, Linux-package and live evidence,
records exact final/rollback bindings, setup/demo command and unverified limits.
Preserve original publication UNKNOWN, held parents, historical cleanup uncertainty
and account-wide Blob Contributor's application-only isolation limitation.
Reviewed scoped commits/push and source reconciliation remain downstream.
