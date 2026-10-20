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
| Cross-scenario evidence assertions | `live_acceptance.py:validate_scenario_evidence`, `tests\test_scenario_evidence.py`, `docs\design.md` | Offline private observation joins for actual parent/both-role bindings, cumulative effects and request counts, once-only confirmed stop/checkpoint retention and separate-parent isolation; no new CLI/public event fields, collector, ledger or live claim |
| Tests/package | `tests`, `Test-Demo.ps1`, `package_guard.py`, requirements and Dockerfile | Offline acceptance and preserved package controls |
| Specialist continuation proof | `tests\test_specialist_continuity.py`, `demo\architect_agent.py`, `demo\reviewer_agent.py` | Both real role load/model/store paths and framework execution with controlled external boundaries; serialized-history value snapshots, identical-brief fresh-history controls, exact-response no-send recovery and held-effect regressions (offline only) |
| Design/handoff | `docs\design.md`, `docs\NEXT-SESSION-PROMPT.md`, migration plan/map, workflow | Blob/MAF workflow design, exhaustive copy-first boundary |
| Customer prototype architecture | `docs\customer-prototype-architecture.md` | Full-scope release design; current recovery-entry evidence and executed canonical/sibling resolver matrix, matched operational-wrapper boundary; installed B candidate versus live selection, source/package join, original-owner handoffs and AC1-AC9 evidence map |
| Customer prototype UX | `docs\customer-prototype-ux.md` | Terminal/README journeys and wireframes, safe continuity/evidence labels, current recovery-entry matched-root/trust interpretations, unchanged machine contract and bounded implementation checks |
| Customer prototype release plan | `docs\customer-prototype-release-plan.md` | Current recovery-entry overlay and three retained sprint goals/acceptance contracts; historical receipts/resolver evidence versus writing/current trust, matched operational-wrapper integration, minimal original-owner dependencies and unchanged live final gates |
| Customer prototype release notes | `docs\customer-prototype-release-notes.md`, `README.md` | Blocked release decision, per-criterion AC1-AC9/G1-G8 ledger, accepted offline source versus unreached live proof, existing closing owners, setup/demo reference and unknown final/rollback bindings |
| Sprint design (RP-S1/RP-S2/RP-S3) | `docs\customer-prototype-sprint-design.md` | Current RP-S1 recovery-entry journey and report-state mapping for historical evidence versus current ownership/trust and matched operational roots; retained screens/fixtures, RP-S3 continuity/recovery/isolation reports, unchanged machine contracts and original execution owners |
| Cumulative sprint architecture (RP-S1/RP-S2/RP-S3) | `docs\customer-prototype-sprint-architecture.md`, `docs\requirements\coordinator\architecture.md`, `docs\requirements\specialists\architecture.md`, `docs\requirements\client-release\architecture.md` | Current RP-S1 recovery-entry/tier overlay: historical evidence versus current writer/trust/inventory, matched operational wrapper/source joins and original-owner closing actions; retained fixtures/candidate, G1-G8 continuity/recovery/isolation and exact-source truthful delivery; unchanged runtime/public contracts |
| Current RP-S1 recovery-entry assignments | `docs\customer-prototype-recovery-sprint-plan.json` | Stopped original ownership evidence reconciliation in parallel with independent current-source drift/check handoff; retained runner and matched operational integration; deferred original DevOps trust/inventory/status/trial. Accepted candidate, application preparation, presentation and assertions are consumed, not redispatched |
| Historical RP-S1 sprint assignments | `docs\customer-prototype-sprint-plan.json` | Retained prior phase-compatible dispatch contract and audit history; current recovery-entry plan supersedes its dispatch list without resetting originating stops |
| RP-S2 sprint assignments | `docs\customer-prototype-rp-s2-sprint-plan.json` | Stopped evidence-only ownership carryover and independent application integration preparation; runner/source join, later strict-trust inventory, exact publication/finite trial and explicit actual G1-G4 handoff; accepted candidate/UX and RP-S1 audit contract retained |
| RP-S3 sprint assignments | `docs\customer-prototype-rp-s3-sprint-plan.json` | Evidence-only stopped carryover alongside independent missing scripted-comparison work; reviewed runner/source integration consumes accepted application preparation; original DevOps gates actual G1-G4, two-turn continuity, once-only supported recovery, independent isolation and truthful exact-source delivery |
| RP-S1 retrospective | `docs\customer-prototype-release-plan.md`, `docs\customer-prototype-architecture.md`, `docs\customer-prototype-ux.md` | Supplied review/process observations, metric limits, bounded evidence-handoff improvements and existing-owner actions; no reset of stopped ownership or live acceptance waiver |
| RP-S3 retrospective | `docs\customer-prototype-release-plan.md`, `docs\customer-prototype-architecture.md`, `docs\customer-prototype-ux.md` | Accepted offline assertion/repair lessons, meaningful negative controls and separate observation provenance; unreached live demonstration, current originating votes, preserved stopped lanes and existing integration/release ownership |
| Identity recovery plan | `docs\identity-recovery-plan.md`, `docs\NEXT-SESSION-PROMPT.md` | G1-G8 objective, consumed diagnostic exception retaining original UNKNOWN, executed outbound/ingress result, cited supported-remedy assessment and provider-dependent execution gate |
| Local context/checks | `scripts\Use-Settings.ps1`, `Initialize-LabSettings.ps1`, `migration.py`, `Test-Repository.ps1` | Validated private linkage, deterministic preservation/public checks |
| Identity triage | `scripts\diagnose_identity.py`, `tests\test_diagnose_identity.py` | Lock-pin audit, synthetic SDK/HTTP probes and sanitized exact-response evidence analysis; no cloud calls or retry authority |
| Identity candidate handoff | `scripts\identity_handoff.py`, `tests\test_identity_handoff.py`, `docs\identity-candidate-handoff.md` | Offline-only A/B candidate, lifecycle header plumbing and receiver namespace negative controls; no installed runtime change or live selection |
| Isolated runtime candidate | `demo\foundry.py:specialist_identity_headers`, `demo\workflow.py:WorkflowRuntime.resources`, `tests\test_isolated_client.py`, `docs\design.md` | B specialist-only project/header/cache; original resource tuple and opaque-only non-specialist authority retained; actual resource lifecycle/cleanup regressions, no live selection |
| Copilot context | `.github\copilot-instructions.md`, agents and skills | Bounded implementation/review and deployment gates |

External lab tooling is mapped in `docs\migration-map.json`; resolve its root
from private settings. There is no Terraform root or SSH launcher here.
Recovery-entry SprintPlan freshness: inspected clean agreed-sprint-architecture
baseline `095ced1cbb8258eaed6e1bf11beeb19a8b36f08d`; added only the current
recovery-entry assignment JSON and updated navigation/inventory. Preserves the
originating ownership stop and accepted source handoffs; no pending candidate
review or new UX implementation is invented. Current-source checks and ownership
evidence are independent; exact operational wrapper integration and current
trust/inventory join only at original execution gates. Supplied private evidence
presence is not writer exclusivity, current trust or live acceptance. No actual
dispatch, reviewer agreement, lab mutation or cloud operation is inferred.
Recovery-entry sprint-architecture freshness: inspected clean agreed-sprint-design
baseline `160b38d202bd239ecd409b8f7de485b1d7f7e10e`; updated cumulative and
three tier architecture slices plus this navigation, with no added/deleted
paths. Consumes accepted release architecture, UX, planning and sprint screens
without reopening them or repeating private receipt/resolver experiments.
Historical evidence is not current ownership/trust, installed operational
source, identity selection or live acceptance. No runtime, lab, assignment,
public schema, release gate or execution-owner change is inferred.
Recovery-entry RP-S1 design freshness: inspected clean agreed-release-plan
baseline `68c5bd8d8b2835b0f329b4bac5821ddb78809b36`; updated only sprint
design and this navigation, with no added/deleted paths. Retains accepted
screens/fixtures; maps historical evidence availability and matched operational
roots to existing report states and original owners. No new UI, public schema,
task dispatch, private receipt inspection or live capability is inferred.
Recovery-entry release-plan freshness: inspected clean agreed-UX baseline
`8d6d6e05469e6a180db5cba0f77e07f7ff21a3af`; updated only the release plan
and this navigation, with no added/deleted paths. Consumes accepted architecture
and UX without rerunning their experiments; retains RP-S1/RP-S2/RP-S3 contracts,
stopped ownership review, original execution owners and final AC1-AC9/G1-G8.
Historical evidence availability is not current trust, writer ownership or
live acceptance. No task dispatch, lab mutation or cloud operation is inferred.
Recovery-entry UX freshness: inspected clean agreed-architecture baseline
`2f62e3ca5353fdbc3433e1f49fdf9133f95dacbc`; updated only UX handoff and
this navigation, with no added/deleted paths. Retains existing screens, tools,
machine/parser contracts and original owners; historical receipt availability
and local root compatibility are not current trust, writer ownership or live
acceptance. No private evidence was inspected by this UX revision.
Recovery-entry architecture freshness: inspected clean application baseline
`3d731c00e8373774bf8254a8f060eac621d0e928`; updated only release architecture
and this navigation, with no added/deleted paths. Bounded approved inspection
ran both actual canonical/sibling resolvers with matching/mismatching roots
and checked local settings/registry/receipt linkage. Keep runtime, package,
identity, prior accepted handoffs and original execution owners unchanged;
local resolver success is not writing ownership, current trust or live selection.
Release-closeout freshness: inspected clean baseline
`44177bce27d5d4e0f76dcfb5993f9cf0ae51c3a7`; added only blocked release
notes, updated README first-screen status and this index. No runtime, lab
tooling, public event, architecture or sprint contract change; no fresh
deployment, private receipt inspection, integration/push or live claim.
RP-S3 retrospective freshness: inspected clean baseline
`12e2a2a5b3c97268d3b9ba8c631ed483c35762df`; updated only the three
retrospective document slices and navigation, with no added/deleted paths,
runtime changes, new evidence collector or live capability.
RP-S3 design freshness: inspected clean baseline
`585601f4ad3e8d87c029a6fdca2d0326a403e142`; updated only the sprint-design
navigation and its RP-S3 section, with no added/deleted paths or runtime changes.
RP-S3 architecture freshness: inspected clean baseline
`7f7376b85e7b5f4e216dd382480cf6678d07eadf`; updated cumulative and three tier
architecture slices and this navigation. Considered no added/deleted paths;
retained runtime, acceptance parser and package boundaries. Per-scenario
acceptance output does not itself establish the full cross-scenario proof.
RP-S3 planning freshness: inspected clean baseline
`77454900c853e5787eda21f5139cc969976e332a`; added only the RP-S3 assignment
JSON and updated this index. Prior plans remain unchanged. Preserve originating
ownership stop and separate accepted transport-trust handoff; consume accepted
application preparation without redispatch. Missing comparison implementation
is independent of lab ownership and inventory. Reviewed integration owns Git
accounting/push, original E2E owns formal joined validation, and original DevOps
owns all cloud effects and live gates. Recovery and isolation share serialized
resources without an invented dependency; an agreed blocked report enables no
missing prerequisite effects. No dispatch or live capability is inferred here.
RP-S3 evidence-assertion freshness: inspected clean baseline
`2ccef16d055295d036ed176b0b3ba428b8061041`; added
`tests/test_scenario_evidence.py` and extended existing acceptance tooling with
private-input deterministic comparisons documented in `docs/design.md`.
Existing machine events, presentation, runtime and release ownership remain
unchanged. No lab ownership probe, lab writing or cloud effect is involved.
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

SprintArchitecture reconciliation freshness: inspected clean base
`6a24eaf3110bd964f992a87e01e6916f505e0dda`. Updated the cumulative sprint
document and all three tier contracts; no additions/deletions. Retain installed
`3aca5dc` for original review/integration, Developer runner ownership and
pre-parent scenario/source/package/actual-version checks. Preparation rejection,
observed receiver failure and unknown observation are separate outcomes;
no live path selection or upstream handoff reopening is implied.

RP-S2-ISOLATED-CLIENT freshness: inspected clean application base
`4f2e02d9b08bc1c5258d6f799e9a9f0809705a81`. Added
`tests/test_isolated_client.py`; no deletions. Runtime now constructs the
accepted specialist-only B candidate, leaving original project/header/cache
authority unchanged. The older offline handoff remains non-installed diagnostic
logic, not a selector. No deployment, inference, permission or lab source change.
Existing README/terminal/continuity implementations are preserved.

RP-S2 SprintPlanLoop freshness: inspected clean application base
`8fc296f65589af88706396ecf50e27b0f75deaef`. Added only
`docs/customer-prototype-rp-s2-sprint-plan.json`; retained the RP-S1 plan unchanged.
Evidence-delivery-only carryover preserves the ownership task's five-round stop
and runner-writing block. Application integration preparation is independent;
the joined source task retains reconciliation, exact checks and reviewed scoped
push. Original E2E/DevOps retain formal integration, strict-trust inventory,
exact package/publication, finite ingress and actual G1-G4 acceptance. No fresh
lab ownership/trust, dispatch or live outcome is inferred by planning.

Historical RP-S1 SprintPlanLoop freshness: inspected clean application base
`4b3d0a4ecfda090f4721008de7c301e3fdf34cbc`; no paths added/deleted.
Retain installed `3aca5dc` for original review/check handoff, not duplicate coding.
The lab registers a sibling feature checkout at `bdd6b2a`, but its direct
inspection was execution-permission denied; checkout safety and canonical-root
compatibility remain assigned, not assumed. Preserve all eight canonical dirty/
untracked paths. Runner coding and integration do not wait for cloud inventory.
Assign pre-parent scenario/source/package/actual-version mismatch fixtures and
preparation/receiver/unknown classifications to runner, integration and trial.
Keep original E2E and later DevOps gates, minimal joins and exclusive resources.
Existing orchestrator dispatches ready original work loops before planning
review; eligibility is not observed dispatch or reviewer agreement.
No runtime, lab, cloud or workflow-runtime mutation by this planning turn.

Historical ReleasePlanLoop revision freshness: inspected clean application base
`3ee9798afa4a419be87bcb68fdfc3540875d171a`. No added/deleted paths,
runtime, dependency or deployment boundary changes. Release planning retains
the integrated RP-S1 source and accepted architecture/UX handoffs; it adds the
new authorized A/B selection and scoped permission work to the sprint handoff.
Formal E2E validation and DevOps publication/cloud-pass remain separate;
unresolved selection does not block remaining artifacts or waive live gates.

Current ArchitectureLoop revision freshness: inspected integrated base
`bb1743d85cb10e6520c92efaa42df0702178f57a`, with a clean application worktree.
No paths added/deleted, runtime or dependency changes. The release architecture
now resolves the integrated offline handoff's missing runtime/runner design:
request-local specialist-only B client, unchanged non-specialist authority,
exact-source candidate activation and finite journaled decision execution.
It provides bounded downstream ownership/dependencies without reopening RP-S1
fixtures/UX. Neither path is live-selected; E2E/DevOps gates remain unchanged.

Original architecture handoff freshness: inspected base commit
`1dfb7fed6fdeb3cc506b5394927fdfcebe39a4bc` plus the pre-existing readability
worktree changes. Added `docs\customer-prototype-architecture.md`; no runtime,
entry-point, dependency or ownership boundary changed by that document.
Historical deployment/test numbers above are context, not freshly validated
release evidence. Use the October 19 invocation's authority within its exact
scope; the older consumed exception cannot authorize unknown-effect replay.

Current UX handoff freshness: inspected clean architecture baseline
`0a244702c7ccf01f1916c4b3a2580346ffb02fea` for the October 20
candidate-to-customer handoff. Retained integrated screens/fixtures; clarified
offline/unresolved versus partial ingress, selected identity path and full
customer release, plus fresh trial versus held historical conversation.
No new command, public event, runtime boundary or added/deleted path.

Previous UX handoff freshness: inspected clean architecture baseline
`2a736d94cb99c01aca0c516aeaf920e61ddb8fbd`. Reconciled
`docs\customer-prototype-ux.md` with the integrated human-view implementation
and README (`56b762e`, `24b883f`), current derived requirements and authorized
identity-path handoff. No paths added/deleted, runtime, dependency or public
event contract changed. Human-view syntax is implemented; exact continuity
claims and live release acceptance still require separate private evidence.

Current release-plan freshness: inspected clean baseline
`c17813567e7d3db09abe1d2403b948c98131c24f`, accepted architecture `cde7638`
and UX `c178135`, for the source-to-trial release delta. Retain installed
candidate `3aca5dc` for original review/integration, not redispatch. Developer
safe lab ownership precedes runner coding and source integration before E2E;
fresh inventory/status and guarded trial remain later original DevOps work.
Require scenario/source/package/deployed-version consistency before parent
creation and distinguish local preparation rejection from observed receiver
failure. Scrum Master retains task decomposition and lab reconciliation.
No paths added/deleted or runtime/dependency contracts changed by this plan.
Identity selection and live release remain unresolved.

Original release-plan freshness: based on accepted architecture `1f690f5` and UX
`0f2a2b2`, preserving the existing 17 dirty paths. Added
`docs\customer-prototype-release-plan.md`; no runtime, dependency or ownership
boundary changed. Scrum Master retains task decomposition/Git reconciliation;
DevOps retains publication/live acceptance. Sprint acceptance is planned, not
executed or waived by a bounded research exit.

Current SprintDesignLoop freshness: inspected clean release-plan baseline
`5449ff49af6a79dbc9fef75c1314d6689cdba6d3`, accepted architecture `0a24470`
and UX `ef5c79d`. Reconciled `docs\customer-prototype-sprint-design.md` with
the specialist-only candidate/finite-runner handoff: offline-only, fresh trial,
architect-only entry, both-role selection and final release are distinct
screen/report interpretations. Retain integrated `--native --view human`,
fixtures and README without redispatch. No candidate migration screen, identity
selector, permission wizard, new evidence ledger or release-success badge.
No paths added/deleted, runtime/CLI/schema/ownership boundary changes.
Prior-loop completion dispositions remain confined to their originating work;
SprintDesign review and downstream live/package gates remain separate.

Current SprintArchitectureLoop freshness: inspected clean baseline
`6d5df4256cf9239f491528226dd9502c1c185e37`, accepted release architecture
`0a24470`, UX `ef5c79d`, release plan `5449ff4` and sprint design `6d5df42`.
Updated the existing cumulative sprint and three logical-tier contracts with
concrete RP-S2 isolated-client/resource-factory tests, unchanged specialist
receiver/history boundary, deterministic lab-runner implementation and true
integration joins. Retain accepted RP-S1 fixtures/UX; no redispatch or new
runtime selector. Lab dirty branch/files remain untouched; Scrum assigns safe
lab writing/Git reconciliation. No added/deleted paths, runtime, dependency
or schema changes. Identity selection, formal E2E and DevOps cloud-pass remain
unresolved downstream, not claims of this architecture revision.

Previous SprintArchitectureLoop freshness: inspected clean baseline `46a1b50`,
accepted release architecture `2a736d9`, UX `3ee9798`, release plan `b0d73b0`
and sprint design `46a1b50`. Reconciled the cumulative sprint and three existing
logical-tier contracts with integrated fixtures (`6614440`, `c454e50`), human
view (`56b762e`) and source reconciliation (`24b883f`); do not redispatch them.
Added the authorized A/B/unresolved scripted selection handoff, lifecycle/
principal-namespace compatibility and exact scoped permission/readback boundary.
Prior completion dispositions remain confined to their originating outputs.
No added/deleted paths, runtime, dependency or event schema changes; E2E and
DevOps retain formal validation and publication/cloud-pass respectively.
Neither identity path nor final package/live gates are proven by this revision.

Current SprintPlanLoop freshness: inspected clean application baseline
`97d8610f2691c7440ba74b40933f500c0af46801` on the authorized feature branch.
Replaced obsolete eight-task redispatch with five concrete delta assignments:
newly authorized identity-path script/contract and fresh target inventory start
in parallel, followed by explicit source reconciliation, bounded decision and
independent exact-source delivery checks. Retain accepted fixture/README/terminal
commits and all five provenance-qualified upstream completion dispositions.
No added/deleted paths, runtime/dependency changes or lab edits. The unrelated
dirty lab branch stays untouched; any required lab permission/tool writing
needs internal ownership/branch replanning, not new permission approval.
Actual parallel dispatch and original planning votes belong to the orchestrator;
this plan neither asserts those events nor proves either identity path live.

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

RP-S1-ID-HANDOFF freshness: based on clean `0c43d599760b5213a5b5bd82cfd4e40aede895fa`.
Added offline-only `scripts\identity_handoff.py`, its test module and
`docs\identity-candidate-handoff.md`. No runtime/dependency/lab changes.
Candidate B is not installed; both paths remain live-unresolved. Tests observe
raw SDK operation arguments and mocked Responses HTTP, not platform ingress.
Original reviewers and downstream runtime/lab integration retain their roles.

RP-S1-ID-INTEGRATE freshness: inspected clean `13203ac6f902c6c573a34aed6e04cf09bb4a94b7`
on the authorized feature branch. Reviewed identity source is already integrated;
prior `24b883f` integration and all five recorded task commits are ancestors.
No unmerged local task branch or abandoned source was found. The integration
section in `docs\identity-candidate-handoff.md` records exact-source checks and
the offline/unresolved downstream contract. No paths added/deleted, runtime,
dependency, lab or contract changes. Fresh inventory, isolated runtime/lab-runner
replanning and formal E2E/DevOps release gates remain separate.

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
- `docs\customer-prototype-recovery-sprint-plan.json`
- `docs\customer-prototype-release-notes.md`
- `docs\customer-prototype-release-plan.md`
- `docs\customer-prototype-rp-s2-sprint-plan.json`
- `docs\customer-prototype-rp-s3-sprint-plan.json`
- `docs\customer-prototype-sprint-architecture.md`
- `docs\customer-prototype-sprint-design.md`
- `docs\customer-prototype-sprint-plan.json`
- `docs\customer-prototype-ux.md`
- `docs\design.md`
- `docs\identity-candidate-handoff.md`
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
- `scripts\identity_handoff.py`
- `scripts\migration.py`
- `scripts\repo_index.py`
- `tests\test_artifacts.py`
- `tests\test_config.py`
- `tests\test_demo.py`
- `tests\test_diagnose_identity.py`
- `tests\test_identity_handoff.py`
- `tests\test_isolated_client.py`
- `tests\test_routing.py`
- `tests\test_scenario_evidence.py`
- `tests\test_specialist_continuity.py`
- `tests\test_workflow.py`

<!-- inventory:end -->
