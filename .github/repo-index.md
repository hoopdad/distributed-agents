# Repository index

Read this index before searching. Refresh the inventory with
`scripts\repo_index.py`; `--check` fails on drift. Only public Git-visible files
are indexed; ignored state, dependencies and external lab files are excluded.

## Architecture and search entry points

| Area | Entry points | Responsibility |
|---|---|---|
| Orchestration | `main.py`, `demo\host.py`, `demo\workflow.py`, `demo\coordinator_agent.py` | Checkpointed MAF/Foundry graph; consecutive begin/route/execute/publish lifecycle methods precede shared correctness helpers, with numbered inline stages and explicit handoffs |
| Specialist agents | `demo\architect_agent.py`, `demo\reviewer_agent.py`, `demo\specialist.py` | Each role's run_assignment orchestrates five typed stage methods directly below it; explicit role-local Azure SDK setup, input reads, LLM session/recovery and immutable writes without WorkflowRuntime dependency |
| Contracts/configuration | `demo\artifacts.py`, `demo\contracts.py`, `demo\config.py`, `config\settings.example.json` | Strict artifacts/assignments and atomic artifact/routing settings |
| Blob/routing | `demo\artifact_store.py`, `demo\routing.py`, `config\routing-corpus.json`, `scripts\calibrate_routing.py` | Role-owned immutable outputs, fenced journal/manifest, typed calibrated Decision-1 and shared admission |
| Foundry integration | `demo\foundry.py`, `agent_metadata.py`, `azure.yaml` | Trusted host/state/provider adapters; three MAF/Foundry remote-mode services deployed, not live-accepted |
| Local client/transport | `demo\terminal.py`, `native_proxy.py`, `live_acceptance.py` | Private terminal with opt-in `--native --view human` stderr projection, unchanged stdout/parser, exact-origin proxy, bounded diagnostics, artifact-envelope audit and guarded compute stop/resume acceptance |
| Tests/package | `tests`, `Test-Demo.ps1`, `package_guard.py`, requirements and Dockerfile | Offline acceptance and preserved package controls |
| Specialist continuation proof | `tests\test_specialist_continuity.py`, `demo\architect_agent.py`, `demo\reviewer_agent.py` | Both real role load/model/store paths and framework execution with controlled external boundaries; serialized-history value snapshots, identical-brief fresh-history controls, exact-response no-send recovery and held-effect regressions (offline only) |
| Design/handoff | `docs\design.md`, `docs\NEXT-SESSION-PROMPT.md`, migration plan/map, workflow | Blob/MAF workflow design, exhaustive copy-first boundary |
| Customer prototype architecture | `docs\customer-prototype-architecture.md` | October 19 full-scope release design, authorized authentication/delegation alternatives, principal-namespace discriminator, least-privilege exception, continuation contracts and AC1-AC9 evidence map |
| Customer prototype UX | `docs\customer-prototype-ux.md` | Terminal/README journeys and wireframes, safe continuity/evidence labels, unchanged machine contract and bounded implementation checks |
| Customer prototype release plan | `docs\customer-prototype-release-plan.md` | Three initial sprint goals/acceptance contracts, retained RP-S1 integration, authorized A/B identity discriminator/permission handoff, unresolved-path artifact continuation, exact release/live gates and original-owner closeout |
| RP-S1 sprint design | `docs\customer-prototype-sprint-design.md` | Sprint-specific README/terminal screens, ordered revision trace, incomplete/recovered-event behavior and fixture-to-display implementation handoff |
| RP-S1 sprint architecture | `docs\customer-prototype-sprint-architecture.md`, `docs\requirements\coordinator\architecture.md`, `docs\requirements\specialists\architecture.md`, `docs\requirements\client-release\architecture.md` | Cumulative design and logical-tier contracts for exact binding fixtures, direct model continuation, unchanged terminal projection and independent supported-remedy assessment |
| RP-S1 sprint assignments | `docs\customer-prototype-sprint-plan.json` | Dispatch-ready original-role tasks, minimal handoff dependencies, parallel file ownership, shared release resources and explicit Git/source integration |
| Identity recovery plan | `docs\identity-recovery-plan.md`, `docs\NEXT-SESSION-PROMPT.md` | G1-G8 objective, consumed diagnostic exception retaining original UNKNOWN, executed outbound/ingress result, cited supported-remedy assessment and provider-dependent execution gate |
| Local context/checks | `scripts\Use-Settings.ps1`, `Initialize-LabSettings.ps1`, `migration.py`, `Test-Repository.ps1` | Validated private linkage, deterministic preservation/public checks |
| Identity triage | `scripts\diagnose_identity.py`, `tests\test_diagnose_identity.py` | Lock-pin audit, synthetic SDK/HTTP probes and sanitized exact-response evidence analysis; no cloud calls or retry authority |
| Copilot context | `.github\copilot-instructions.md`, agents and skills | Bounded implementation/review and deployment gates |

External lab tooling is mapped in `docs\migration-map.json`; resolve its root
from private settings. There is no Terraform root or SSH launcher here.
`config\routing-calibration.json` records the successful real routing-v3
evaluation (eight ready and four missing-input cases correct, selected threshold
0.5/margin 0) on the unchanged frozen corpus. All four real evaluation journals
and the retired blank-facts calibration are retained. Request hashes bind policy
and explicit nonempty facts; no offline fixture is
release evidence. Application Windows/Linux gates pass; artifact infrastructure
is applied with scoped zero-change convergence. Reproduced hosted publication
originally placed architect 17/reviewer 15/coordinator 22 on
common bundle `51064aa426d28d0cfa6b126eac7fce5ab0e9a5a0667267ef105884c1805adde2`
with unchanged identities and earlier versions retained. The subsequent approved
coordinator-only diagnostic activated version 23 on
`03aa0da34942ca66283a37dae8b6edab04ac053291937eebdc2464cdb8f839d9`;
architect 17/reviewer 15 retain their prior bundle. This mixed deployment is
not final common-bundle acceptance. Coordinator 19 proved
`DECISION_CALIBRATION_PROVENANCE`: absent facts became blank in the Windows
loader but defaulted nonempty in hosting. The local correction truly unsets
missing options, forwards explicit facts to all roles and validates the fresh
genuine calibration before packaging. Live execution now writes requirements and
a routing decision; the architect fails SDK preparation (`RuntimeError`,
`storage_error`) and its known operation is explicitly held. Deployed SDK-scope
diagnostics prove `NATIVE_HOST_PRINCIPAL`: no trusted user reaches the architect.
An actual HTTP-edge test preserves delegation headers; the required explicit
coordinator impersonation permission already exists. A supported platform/SDK
identity-propagation remedy remains blocked, with no principal substitution.
The pinned SDK preserves supplied identity through durable task recovery in an
offline regression. Exact-response read-only ingress-presence observation is
implemented. An earlier Bastion observation could not connect because the lab
command VM was deallocated. Existing
Azure Monitor query access independently confirms user/call present at the
coordinator and user absent/call present at the architect, with correlated
Responses POST HTTP 200. Deployed Foundry calls now forward SDK
`context.platform_headers()` directly, without re-delegating the derived platform
user or forwarding the container-only user header. Strict scope checks
remain unchanged. Explicit operator approval permitted starting
the existing command VM; fresh guarded connectivity and three-service
publication passed with exact hashes, unchanged identities and proven cleanup.
Fresh initial acceptance still holds `SPECIALIST_INCOMPLETE`; exact-response
observation confirms architect 17 again fails `NATIVE_HOST_PRINCIPAL`, with
call identity present and user identity absent. Supported opaque propagation
did not resolve the live failure; its cause remains unresolved. No platform
defect or missing permission has been established. Followup/restart/isolation
were not reached; acceptance/observation jobs and listeners closed.
Deployed HTTP-edge diagnostics report only fixed-role header
presence/context-match flags correlated by a response-ID hash; no header
values, raw IDs, tokens or content are logged. Known-child failure observation
also reads the exact parent's bounded logs. A real workflow resource/client/
transport regression verifies this wiring. These diagnostics do not authorize calls or resolve the
propagation failure.
Before the new approved diagnostic, exact-version reconciliation found
coordinator 23 returned HTTP404 while coordinator 22 remained active. The original publisher's
owner and outcome are unbound; new retained lab observation/inspection tools
do not authorize publication replay or establish original mount closure.
Repeatable identity triage verifies 109 local lock pins and five mocked SDK
probes. Fresh exact-version metadata confirms the three deployed roles use
Responses 2.0.0 with the expected package and identities. The current application suite
has 132 passing Windows/Linux tests (seven expected Linux skips).
A bounded Monitor query now independently confirms the exact coordinator22 /
architect17 ingress discrepancy and a correlated HTTP200 POST to the expected
architect Responses path on the configured project origin.
The one approved prospective attempt is consumed: new durable pre-dispatch
owner/source/package/version evidence, exact active23 and unchanged identity,
separate runner/outer cleanup proven. One fresh MAF/Foundry parent wrote
requirements and genuine Decision-1 routing, then held SPECIALIST_INCOMPLETE.
Exact-response Observe sent zero inference and captured actual architect
outbound call present and equal to the SDK context, with delegated/container
user headers absent. The exact architect child had call identity but no trusted
user and failed NATIVE_HOST_PRINCIPAL. App/Observe owners closed. The original
UNKNOWN and historical cleanup uncertainty remain; no held turn was replayed.
Supported server-side caller-resolution findings and a documented platform/SDK
remedy are required; no platform defect is proven. The provider packet is unsent,
and the consumed exception grants no further publication or inference.
The retained release suite now runs 138 tests on Windows and Linux with expected skips.
Known-response stream recovery is deployed. The known
responses and pending parent are preserved, not resent. Completed remote work, MI private
Blob access, artifact provenance, isolation and actual hosting restart are unverified.
The approved linked-lab policy gives project agents account-wide Blob
Contributor: ownership/publication gates remain application-enforced, not
storage-enforced per-role isolation.
Do not search ignored `.azure`, `.azure-cli`, `.local`, `.migration` or
conversation/credential stores.

Current ReleasePlanLoop revision freshness: inspected clean application base
`3ee9798afa4a419be87bcb68fdfc3540875d171a`. No added/deleted paths,
runtime, dependency or deployment boundary changes. Release planning retains
the integrated RP-S1 source and accepted architecture/UX handoffs; it adds the
new authorized A/B selection and scoped permission work to the sprint handoff.
Formal E2E validation and DevOps publication/cloud-pass remain separate;
unresolved selection does not block remaining artifacts or waive live gates.

Current ArchitectureLoop revision freshness: inspected integrated base
`24b883f910dedbc8dc524177f29f59e061be265e`, with a clean application worktree.
No paths added/deleted, runtime or dependency changes. The release architecture
now covers the additional user-authorized A/B identity paths, scripted bounded
decision-test contract, and unchanged formal E2E/DevOps gates. Existing RP-S1
source/clarity integration is retained; neither path is claimed live-selected.

Original architecture handoff freshness: inspected base commit
`1dfb7fed6fdeb3cc506b5394927fdfcebe39a4bc` plus the pre-existing readability
worktree changes. Added `docs\customer-prototype-architecture.md`; no runtime,
entry-point, dependency or ownership boundary changed by that document.
Historical deployment/test numbers above are context, not freshly validated
release evidence. Use the October 19 invocation's authority within its exact
scope; the older consumed exception cannot authorize unknown-effect replay.

Current UX handoff freshness: inspected clean architecture baseline
`2a736d94cb99c01aca0c516aeaf920e61ddb8fbd`. Reconciled
`docs\customer-prototype-ux.md` with the integrated human-view implementation
and README (`56b762e`, `24b883f`), current derived requirements and authorized
identity-path handoff. No paths added/deleted, runtime, dependency or public
event contract changed. Human-view syntax is implemented; exact continuity
claims and live release acceptance still require separate private evidence.

Release-plan freshness: based on accepted architecture `1f690f5` and UX
`0f2a2b2`, preserving the existing 17 dirty paths. Added
`docs\customer-prototype-release-plan.md`; no runtime, dependency or ownership
boundary changed. Scrum Master retains task decomposition/Git reconciliation;
DevOps retains publication/live acceptance. Sprint acceptance is planned, not
executed or waived by a bounded research exit.

Current SprintDesignLoop freshness: inspected clean release-plan baseline
`b0d73b07247bbadbbab9afa9a1bb85b8fa32d480`, accepted architecture `2a736d9`
and UX `3ee9798`. Reconciled `docs\customer-prototype-sprint-design.md` with
integrated `--native --view human`: one finalization-evaluated stderr summary,
ordered calls and final current content, not invented intermediate findings.
Retain integrated fixtures/README without redispatch. A/B/unresolved identity
selection adds no selector, permission wizard or release-success badge.
No paths added/deleted, runtime/CLI/schema/ownership boundary changes.
Prior-loop completion dispositions remain confined to their originating work;
SprintDesign review and downstream live/package gates remain separate.

Sprint-architecture freshness: based on accepted SprintDesign `4c8511d` and
the accepted release architecture/plan, preserving the same 17 dirty paths.
Added `docs\customer-prototype-sprint-architecture.md` and three derived
logical-tier architecture files under `docs\requirements`; no prior sprint
was supplied. These are not copied delivery requirements or new services.
No runtime, dependency, event schema or deployment ownership changed.

Sprint-plan freshness: based on accepted SprintArchitecture `202e381` and
SprintDesign `4c8511d`, with the same 17 pre-existing dirty paths preserved.
Added `docs\customer-prototype-sprint-plan.json`: eight bounded assignments,
six initially ready non-overlapping lanes, explicit source/Git integration and
separate original DevOps ownership. Dispatch and planning reviewer agreement
remain the existing orchestrator's next actions; no implementation is claimed.

S1-MODEL freshness: based on assignment baseline `8759b7f` and the two
pre-existing role-local `artifact_mode`/`SessionCandidate`/`SessionReview`
terminology diffs, deliberately reviewed for integration. Added
`tests\test_specialist_continuity.py`; no dependency, history schema, runtime
boundary or live capability changed. `S1-INTEGRATE` must reconcile the matching
pre-existing `demo\specialist.py` terminology change owned by that task.
The new fixtures exercise actual role stages and `Agent.run`; only connection
setup, persisted storage and external model transport are controlled.

S1-INTEGRATE freshness: inspected same-branch S1-COORD `6614440`,
S1-MODEL `c454e50`, S1-TERMINAL `56b762e` and S1-DOCS `e24fcb9`.
Reconciles the remaining seven assigned readability diffs, including host
factory/parser wiring and the shared specialist `artifact_mode` keyword.
README commands now use the implemented opt-in human view; earlier design
documents retain their historical proposal wording. No added/deleted files,
dependency, machine schema, migration seal or deployment boundary changes.
Recovery chronology remains owned by S1-REMEDY (`39c3b4e`), not this task.
Offline integrated-source validation does not establish live acceptance or a
final Linux hosting package. Exact baseline/task path accounting is retained
in the S1-INTEGRATE commit message.

<!-- inventory:start -->

## Public file inventory

- `.agentignore`
- `.dockerignore`
- `.env.example`
- `.gitattributes`
- `.github\agents\distributed-agents-builder.agent.md`
- `.github\agents\distributed-agents-reviewer.agent.md`
- `.github\copilot-instructions.md`
- `.github\repo-index.md`
- `.github\skills\distributed-agent-implementation\SKILL.md`
- `.github\skills\lab-deployment\SKILL.md`
- `.github\skills\repo-index\SKILL.md`
- `.gitignore`
- `Dockerfile`
- `LICENSE`
- `README.md`
- `Test-Demo.ps1`
- `agent_metadata.py`
- `azure.yaml`
- `config\routing-calibration.json`
- `config\routing-corpus.json`
- `config\settings.example.json`
- `demo\__init__.py`
- `demo\architect_agent.py`
- `demo\artifact_store.py`
- `demo\artifacts.py`
- `demo\config.py`
- `demo\contracts.py`
- `demo\coordinator_agent.py`
- `demo\foundry.py`
- `demo\host.py`
- `demo\reviewer_agent.py`
- `demo\routing.py`
- `demo\specialist.py`
- `demo\terminal.py`
- `demo\workflow.py`
- `docs\NEXT-SESSION-PROMPT.md`
- `docs\customer-prototype-architecture.md`
- `docs\customer-prototype-release-plan.md`
- `docs\customer-prototype-sprint-architecture.md`
- `docs\customer-prototype-sprint-design.md`
- `docs\customer-prototype-sprint-plan.json`
- `docs\customer-prototype-ux.md`
- `docs\design.md`
- `docs\identity-recovery-plan.md`
- `docs\implementation-workflow.md`
- `docs\migration-map.json`
- `docs\migration-plan.md`
- `docs\requirements\client-release\architecture.md`
- `docs\requirements\coordinator\architecture.md`
- `docs\requirements\specialists\architecture.md`
- `live_acceptance.py`
- `main.py`
- `native_proxy.py`
- `package_guard.py`
- `requirements.lock.txt`
- `requirements.txt`
- `scripts\Initialize-LabSettings.ps1`
- `scripts\Test-Repository.ps1`
- `scripts\Use-Settings.ps1`
- `scripts\calibrate_routing.py`
- `scripts\diagnose_identity.py`
- `scripts\migration.py`
- `scripts\repo_index.py`
- `tests\test_artifacts.py`
- `tests\test_config.py`
- `tests\test_demo.py`
- `tests\test_diagnose_identity.py`
- `tests\test_routing.py`
- `tests\test_specialist_continuity.py`
- `tests\test_workflow.py`

<!-- inventory:end -->
