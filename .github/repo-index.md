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
| Customer prototype architecture | `docs\customer-prototype-architecture.md` | Full-scope release design and canonical `solutionModel` component/flow IDs; supplied trust comparisons versus current execution, sibling registration versus denied direct Git/resolver inspection, existing ownership designations and original review; actual loaded roots, B candidate versus live selection, source/package join and AC1-AC9 evidence map |
| Customer prototype UX | `docs\customer-prototype-ux.md` | Current canonical five-flow/eighteen-step journey-to-screen map from architecture `35d526a`; README/terminal hierarchy, interaction/failure rules, retained wireframes/accessibility and evidence-to-display contract; attributed inspection versus execution, unchanged stdout/parser and no new UI |
| Customer prototype release plan | `docs\customer-prototype-release-plan.md` | Current canonical release-planning entry consumes architecture `35d526a` and UX `c705711`; machine-readable RP-S1/RP-S2/RP-S3 goals, acceptance, exclusions and handoffs map all five flows/eighteen steps. Independent preparation versus ownership/runner/loaded-source/E2E/DevOps critical path; accepted work retained, current separate sibling inspection unavailable, no live acceptance. Older sprint reviews/retrospectives remain attributed history |
| Customer prototype release notes | `docs\customer-prototype-release-notes.md`, `README.md` | Current blocked closeout at `23e7d48`: AC1-AC9/G1-G8 ledger; accepted application/observation/review/retro handoffs versus missing substantive ownership and actual operational join; supplied host trust distinct from containment-source/resource readiness; separately attributed Windows checks, conditional demo, unknown final/rollback bindings and unverified final push |
| Sprint design (RP-S1/RP-S2/RP-S3) | `docs\customer-prototype-sprint-design.md` | Current RP-S1 entry consumes architecture `35d526a`, UX `c705711` and release plan `8343d48`; maps two canonical flows/eight steps to retained A-D screens, with F/G blocked-item handoff. Keeps actual binding/history proof separate from alias-only human stderr, preserves parser and qualified check failure, and assigns no duplicate implementation. Older RP-S2/RP-S3 layouts remain historical |
| Cumulative sprint architecture (RP-S1/RP-S2/RP-S3) | `docs\customer-prototype-sprint-architecture.md`, `docs\requirements\coordinator\architecture.md`, `docs\requirements\specialists\architecture.md`, `docs\requirements\client-release\architecture.md` | Current RP-S1 canonical entry references Architecture `35d526a` model without renaming ten components/five flows/eighteen steps; two-flow/eight-step offline continuity, history and presentation contracts join all three tiers. Historical RP-S2/RP-S3 remain cumulative; originating ownership, actual loaded-source/E2E, independent preparation and serialized exact-package/live gates are not RP-S1 live exit criteria or waived release obligations |
| Current RP-S1 recovery-entry assignments | `docs\customer-prototype-recovery-sprint-plan.json` | Dispatch-ready current five-input handoff at `302d886`: independent original ownership/source-check assignments, accepted fixture/clarity reuse, supplied trust/designations, gated runner and explicit loaded-root/Git integration; original E2E and serialized DevOps retained, early RP-S2 work is not an RP-S1 live exit criterion |
| Historical RP-S1 sprint assignments | `docs\customer-prototype-sprint-plan.json` | Retained prior phase-compatible dispatch contract and audit history; current recovery-entry plan supersedes its dispatch list without resetting originating stops |
| Current RP-S2 sprint assignments | `docs\customer-prototype-rp-s2-sprint-plan.json` | Current `1bce6e1` architecture/`76c797b` design and accepted `b74b84e` source-check handoff; existing ownership evidence recovery and read-only outgoing-drift preparation run independently, then eight-path sibling runner and explicit loaded-root/Git integration; original E2E and serialized DevOps inventory/trial/G1-G4 retain actual live gates; accepted reports are not redispatched |
| Current RP-S3 sprint assignments | `docs\customer-prototype-rp-s3-sprint-plan.json` | Current `c22d809` architecture/`23a4d9a` design and `afe6d4d` retrospective; originating ownership evidence recovery parallel with read-only validator/observation handoff; accepted `0e9add5` application audit consumed without redispatch; eight-path runner and explicit loaded-root/Git integration precede original E2E and serialized DevOps G1-G8. Supplied trust used first, attributed execution distinguished from inspected capture |
| RP-S1 retrospective | `docs\customer-prototype-release-plan.md`, `docs\customer-prototype-architecture.md`, `docs\customer-prototype-ux.md` | Current recovery-entry review `3503522`: eight two-round accepted boundaries versus single-round planning; qualified report agreement versus substantive ownership and actual loaded-source proof, attributed offline checks and mixed metadata versus live gates; existing-owner decisions and measurement limits, no ownership reset or live waiver; older overlays retain history |
| Current RP-S2 retrospective | `docs\customer-prototype-release-plan.md`, `docs\customer-prototype-architecture.md`, `docs\customer-prototype-ux.md` | Accepted review `1e5eb2a`: six single-round accepted boundaries versus unchanged live block; incremental application handoff consumed once, prerequisite execution owner-attributed versus inspected script scope, existing ownership/access and independent inventory closing actions; no new schema, duplicate implementation or live waiver; older overlays retained |
| Current RP-S3 retrospective | `docs\customer-prototype-release-plan.md`, `docs\customer-prototype-architecture.md`, `docs\customer-prototype-ux.md` | Accepted review `be996f8`: retained observation map versus actual provenance/installation; independent containment-source/resource preparation and originating ownership acceptance; conditional README instructions do not close DevOps delivery. Six supplied single-round accepted boundaries are not live progress or measured latency; existing-owner actions and three sprint contracts retained |
| Identity recovery plan | `docs\identity-recovery-plan.md`, `docs\NEXT-SESSION-PROMPT.md` | G1-G8 objective, consumed diagnostic exception retaining original UNKNOWN, executed outbound/ingress result, cited supported-remedy assessment and provider-dependent execution gate |
| Local context/checks | `scripts\Use-Settings.ps1`, `Initialize-LabSettings.ps1`, `migration.py`, `Test-Repository.ps1` | Validated private linkage, deterministic preservation/public checks |
| Identity triage | `scripts\diagnose_identity.py`, `tests\test_diagnose_identity.py` | Lock-pin audit, synthetic SDK/HTTP probes and sanitized exact-response evidence analysis; no cloud calls or retry authority |
| Identity candidate handoff | `scripts\identity_handoff.py`, `tests\test_identity_handoff.py`, `docs\identity-candidate-handoff.md` | Offline-only A/B candidate, lifecycle header plumbing and receiver namespace negative controls; no installed runtime change or live selection |
| Isolated runtime candidate | `demo\foundry.py:specialist_identity_headers`, `demo\workflow.py:WorkflowRuntime.resources`, `tests\test_isolated_client.py`, `docs\design.md` | B specialist-only project/header/cache; original resource tuple and opaque-only non-specialist authority retained; actual resource lifecycle/cleanup regressions, no live selection |
| Copilot context | `.github\copilot-instructions.md`, agents and skills | Bounded implementation/review and deployment gates |

SprintArchitectureLoop canonical RP-S1 freshness: inspected authorized feature
baseline `59a6a63c523ea3a42e89e04d751c5c063af72987`; updated existing cumulative
sprint architecture, three tier slices and this navigation only. No added/deleted
paths, runtime, dependency or public contract change. References the accepted
canonical solutionModel; no duplicate implementation or reviewer votes.
Unowned workflow context remains preserved/excluded; repository-index drift
has an explicit Scrum/integration closing action, not an AC7 waiver. No current
sibling/private recovery inspection, settings import, operational integration,
cloud execution, final push or runtime progress is certified.

SprintDesignLoop canonical RP-S1 freshness: inspected authorized feature
baseline `8343d48b310e4d79b7d1de7b133f483475c054f7`; updated existing
SprintDesign and this navigation only, no added/deleted paths or runtime
changes. Reuses two canonical flows/eight steps and retained A-D layouts;
source inspection confirms finalization-driven opt-in human stderr, not
streaming progress or exact continuity verification. Originating input
agreements do not transfer votes to this design. Unowned workflow context
remains preserved and excluded; its repository-index closing action is not
waived. No sibling/private evidence, cloud operation, operational join,
publication, scoped push or live progress is certified.

ReleasePlanLoop canonical-sprint freshness: inspected authorized feature
baseline `c70571186564cf293a63b00f08511a560b7deb11`; updated existing release
plan and this navigation only, no added/deleted paths or runtime changes.
Consumes supplied original Architecture/UX agreements without transferring
votes. Three unique sprint contracts cover all canonical flows/steps, preserve
independent inventory and actual ownership/source/E2E/cloud gates, and do not
redispatch accepted implementation. No private/sibling/cloud inspection,
operational integration, publication, final push or runtime progress certified.
Preserved untracked workflow context outside owned commits.

UserExperienceLoop canonical-journey freshness: inspected authorized feature
baseline `35d526ae3a9e722ebe633ba60e2ca572182a5d1e`; updated existing UX
entry and this navigation, no added/deleted paths, runtime or contract change.
Preserved the untracked workflow-context directory outside owned commits.
Mapped all five canonical flows/eighteen steps to existing presentation and
safe next actions; retained full principles, tools, wireframes and handoffs.
Architecture votes are not UX votes; attributed recovery/trust inspection is
not Designer/cloud proof. No new renderer, evidence field, identity selection,
deployment, operational integration or live acceptance is claimed.

ArchitectureLoop solution-model freshness: inspected clean authorized feature
baseline `87f1b35`; added canonical IDs for the existing ten components and five
flows to the existing architecture, plus current evidence limitations and owner
handoff. No added/deleted paths or runtime/contracts/dependencies changed.
Canonical lab dirt is preserved; sibling registration is not direct sibling
inspection, which was denied along with resolver access. Supplied recovery JSON
and fingerprint comparisons are input checks, not ownership or live acceptance.
No settings import, cloud operation, operational installation or push is claimed.

ReleaseCloseoutLoop freshness: inspected clean authorized feature baseline
`23e7d48d4b227638638294072092427942a15e7e`; updated existing release notes,
README status and this navigation, no added/deleted paths. Consumes supplied
original sprint agreements without reopening accepted handoffs or transferring
votes to closeout. Compared application execution inputs remain unchanged
from `b74b84e`; no operational installation, private evidence, lab state,
cloud test or final push is certified. Supplied host trust is not missing
authority; independent containment-source/resource preparation remains open.

SprintRetroLoop current RP-S3 freshness: inspected clean authorized feature
baseline `be996f84694f9c94f163448f8afcc3ddce095223`; updated only existing
Architecture, UX, ReleasePlan and this navigation, no added/deleted paths.
Consumes accepted current review and observation handoff without duplicate
implementation or unchanged runtime tests. Independent preparation remains
separate from runner coding. No private evidence recovery, settings import,
transport, cloud operation, operational integration or push is certified.
Original reviewers assess this retrospective; no inherited votes or live waiver.

SprintReviewLoop current RP-S3 freshness: inspected clean authorized feature
baseline `673d1e9e9913bd636c35c91aa9b013b05b355d69`; updated only existing
ReleasePlan review and index, no added/deleted paths. Consumes supplied original
outcomes without transferring prior votes or reopening accepted handoffs.
Conditional README command is not live-verified. No private/sibling/cloud
inspection, runtime test rerun, operational integration or push certification.
Existing owners retain precise closing actions; no new approval stage or
substantive runtime-progress claim.

External lab tooling is mapped in `docs\migration-map.json`; resolve its root
from private settings. There is no Terraform root or SSH launcher here.
SprintPlanLoop current RP-S3 freshness: inspected clean authorized feature
baseline `c22d80995c3242c954da40f8831593e6fcc4c258`; refreshed only the
existing assignment JSON and this navigation, no added/deleted paths.
Current originating dispositions retain substantive ownership acceptance and
actual integration/E2E/package/live gates. Independent observation handoff
consumes accepted application work; no duplicate source implementation,
denied inspection, cloud operation or runtime-progress claim. Existing YAML
orchestrator owns dispatch and original planning-reviewer collection.
SprintArchitectureLoop current RP-S3 freshness: inspected clean authorized
feature baseline `23a4d9a950a73a57c13f6b29a9ca6da685e5c987`; updated existing
cumulative architecture, three tier slices and this navigation; no added/deleted
paths. Consumes accepted current design and RP-S2 architecture/review/retro,
preserving originating ownership/access stops and source/E2E/DevOps boundaries.
Existing observation consistency assertions are not independent provenance.
No runtime change, private ownership recovery, cloud observation or live progress.
SprintDesignLoop current RP-S3 freshness: clean authorized feature baseline
`afe6d4dba937102e12821d770c1f7da4788f1c2c`; updated only existing SprintDesign
and this navigation, no added/deleted paths or runtime/ownership boundary change.
Current originating outcomes/round counts and historical tests remain attributed.
No private ownership evidence, lab source, cloud state or runtime refreshed.
Retains three sprint contracts, originating stops and existing-owner execution
actions without treating report acceptance or prose changes as runtime progress.
SprintReviewLoop current RP-S2 freshness: clean authorized feature baseline
`0e9add565d22b2cb617485e257875e72984907af`; updated only existing ReleasePlan
review and index navigation, no added/deleted paths. Consumes current original
application/E2E/DevOps reviews without transferring RP-S1 votes, rerunning
unchanged checks or retrying denied ownership inspection. Records live goal
unmet and existing-owner closing actions; no operational integration, final
push, cloud PASS or runtime-progress certification.
SprintPlanLoop current RP-S2 freshness: inspected clean authorized feature
baseline `1bce6e1c4fe9e8deb8382fa02c44392bc2d25aea`; updated only the existing
RP-S2 assignment plan and navigation, no added/deleted paths. Seven retained
tasks consume current agreed inputs and exact originating dispositions.
Ownership evidence recovery remains blocked on its original substantive review;
independent outgoing-drift preparation does not reopen accepted source checks
or repeat a revision-matched audit. Original orchestrator owns parallel dispatch;
original E2E and serialized DevOps own actual operational/package/live proof.
Canonical lab status/registration inspection is preservation context only.

SprintArchitectureLoop current RP-S2 freshness: inspected clean authorized
feature baseline `76c797b509f0e8ee53d11ce1fbc275d4ad8ccd59`; refreshed existing
cumulative architecture, three tier slices and this navigation; no paths
added/deleted. Consumes accepted RP-S1/source-check/review/retro and current
RP-S2 design without reopening acceptance or transferring votes. Preserves
actual-evidence access closing action, runner block, loaded-source/E2E join,
independent trust/inventory and original guarded DevOps G1-G4 ownership.
No private ownership/resolver inspection, runtime repair, identity selection,
deployment or live-capability progress is claimed.
SprintDesignLoop current RP-S2 freshness: inspected clean authorized feature
baseline `30c4a534bad1aa38b6b8f46a246c9b84262ecf18`; refreshed only existing
sprint design and this navigation, no paths added/deleted. Consumes accepted
RP-S1 handoffs without reopening them or transferring reviewer votes. Maps
current blocked work and initial collaboration proof to retained screens;
no UI implementation, private evidence inspection, runtime or live claim.
SprintRetroLoop current RP-S1 freshness: inspected clean authorized feature
baseline `350352282f6defafc777dff5c6748d7fb2da3b59`; updated only existing
Architecture, UserExperience, ReleasePlan retrospective sections and this
navigation, no paths added/deleted. Supplied round counts, offline checks and
DevOps metadata remain attributed; no private/sibling/cloud inspection or
runtime repair. Records existing-owner process improvements without reopening
accepted work, supplying ownership acceptance or waiving integration/live gates.
SprintReviewLoop current RP-S1 freshness: inspected clean authorized feature
baseline `b74b84edb6c05fb4dc7f58ba7f88925e2402ddc9`; added the current
review/backlog section to the existing ReleasePlan and refreshed this navigation,
no paths added/deleted. Supplied source/E2E/DevOps results remain attributed;
no private/sibling/cloud inspection, live demo, integration or push is claimed.
Accepted source checks and bounded reports stay closed; originating ownership
evidence/access, actual operational join and exact-package/cloud gates remain
with existing owners. This documentation review is not new runtime progress.
SprintPlanLoop RP-S1 accepted-input freshness: inspected clean authorized feature
baseline `302d8866d3c4f4c4d61b7c63c7f4d24196da664d`; refreshed existing
recovery-entry JSON and this navigation, no paths added/deleted. Consumes all
five supplied accepted inputs and exact originating completion dispositions
without reopening them or borrowing their votes. Original ownership and
current-source checks are resource-disjoint initial Developer work; reviewed
runner/loaded-root integration is explicit, with original E2E and serialized
DevOps thereafter. Canonical lab status/registration was inspected read-only:
dirty unrelated work remains untouched; current canonical HEAD differs from
the older plan. No private evidence authentication, sibling resolver, cloud,
dispatch, new task acceptance, package, push or live progress is claimed.
SprintArchitectureLoop RP-S1 accepted-input freshness: inspected clean feature
baseline `a1e85442a90a2333bedd6e4beed1d8d849a68ad9`; refreshed cumulative
architecture and three tier slices plus this navigation; no paths added/deleted.
Consumes the four supplied accepted upstream handoffs without reopening them
or transferring votes. Accepted trust/reference and coordination are distinct
from current strict transport, originating ownership acceptance and actual
loaded-source integration. No private evidence/resolver/cloud inspection,
identity selection, deployment or runtime progress is claimed.
SprintDesignLoop RP-S1 accepted-input freshness: inspected clean feature
baseline `0d0f17b928ba99517551ba20a0c0201801148d9d`; updated only existing
sprint design/navigation, no added/deleted paths. Retains existing screens
and fixtures without duplicate implementation or transferred upstream votes.
Accepted trust input and coordination are distinguished from current transport,
originating ownership acceptance and loaded-root integration. No private/lab
source inspection, cloud operation or live progress is claimed.
ReleasePlanLoop recovery-handoff freshness: inspected clean feature baseline
`c5e7189252886a653daa42cbf9021f0cf59691b2`; updated only the existing
release plan and this navigation, no added/deleted paths. Consumes accepted
architecture/UX and supplied trust/designation inputs without transferring
votes or reopening their acceptance. No private/sibling/cloud inspection,
task dispatch, operational reconciliation, push or runtime progress is claimed.
Original ownership, integration, E2E and DevOps exact-package/live gates remain.
UserExperienceLoop recovery-handoff freshness: inspected clean feature baseline
`25d182245a1bb40b842f5787196bd8f8244c4a7d`, committed architecture and
existing terminal render/finalization path; refreshed only the existing UX
handoff and this navigation, no added/deleted paths. Consumes accepted
architecture without transferring votes; supplied accepted trust input is not
current SSH validation or receipt authentication. No private/sibling/cloud
inspection, runtime change, deployment or live demonstration is claimed.
ArchitectureLoop recovery-handoff freshness: inspected clean feature baseline
`a1bca5d`; no added/deleted paths. Eight named external recovery files parsed;
value-suppressed comparisons matched the user-accepted fingerprint to both
supplied references and local settings to historical approved project/lab roots.
Current sibling Git inspection succeeded; resolver reads were denied and not
retried through an alternate route. Accepted trust/designation inputs do not
establish current strict SSH, ownership acceptance, loaded-source integration,
identity selection or live readiness. Existing original owners and gates remain.
ReleaseCloseout freshness: inspected clean authorized feature baseline
`b809cb91a9f84114ea8edd5829ccc5759d98a1d8`; updated only existing release
notes, README status and this navigation; no added/deleted paths. Verified
retained source/audit/map/review ancestry and unchanged execution inputs from
`b13670e`. Supplied private observations and historical test execution remain
attributed, not independently refreshed. No operational reconciliation, push,
deployment or customer-ready claim; all AC1-AC9/G1-G8 remain required.
RP-S3 SprintRetro freshness: inspected clean authorized feature HEAD
`0f2e6276bb53f84605d745db24cafd1991133d21`; updated only Architecture,
UserExperience, ReleasePlan retrospective sections and this navigation, no
added/deleted paths. Supplied original
Developer/E2E/DevOps outcomes remain attributed, not fresh private/cloud proof.
Retains substantive originating ownership acceptance, independent strict trust,
actual loaded-root integration, formal E2E and exact-package/live gates.
No completed non-held initial parent, task-code reconciliation, deployment,
push or successful demonstration is established by this documentation review.
RP-S3 SprintPlan freshness: inspected clean authorized feature HEAD
`cb85ce076592454dfc5d2e3ac6b657a06b554cfa`; refreshed only the existing
RP-S3 plan and this navigation; no added/deleted paths. Consumes accepted
scenario assertions/prerequisite repair, source checks and outgoing audit
without duplicate implementation. Two resource-disjoint initial Developer
handoffs converge at reviewed runner/actual loaded-root integration. Exact
eight-path writer and designated integration ownership remain bounded;
canonical dirty work, historical UNKNOWNs and held parents are protected.
Original formal E2E and serialized DevOps package/live gates remain unchanged.
Planning does not substantiate sibling ownership, independent host trust,
operational installation or a completed initial parent. Dispatch and original
planning votes remain for the existing YAML orchestrator.
RP-S3 SprintArchitecture freshness: inspected clean authorized feature HEAD
`1f24c9a07277d2f5b111f83b186db3ad6a5257aa`; refreshed cumulative mapping
and three tier slices plus this navigation, no paths added/deleted.
Consumes accepted RP-S2 architecture/retro and RP-S3 design within their
originating boundaries, without transferred votes. Retains accepted offline
scenario assertions and current missing initial-parent/ownership/root/trust
handoffs with attributed observations, original integration/E2E/DevOps and
exact-source/package/live requirements. No private/lab/cloud inspection,
task dispatch, runtime implementation or live progress is claimed.
RP-S3 SprintDesign freshness: inspected clean authorized feature HEAD
`dd7728cb80b503883d96d3317a3dd5dee28f1c6e`; refreshed only current sprint
design mapping and this navigation, no paths added/deleted. Retains H-K layouts
and accepted prior design/UX without transferred votes or duplicate implementation.
Supplied RP-S2 outcomes remain attributed: no completed non-held initial parent,
ownership acceptance, actual loaded-root join or established strict-trust handoff.
Original formal E2E, exact-package/live gates and scoped Git reconciliation remain.
No sibling/private/cloud inspection, deployment or runtime progress is claimed.
RP-S2 SprintRetro freshness: inspected clean authorized feature HEAD
`16a57b6f6a77d4d2e8fbb58ecd179d115cf4e0b8`; updated only the existing
Architecture, UserExperience and ReleasePlan retrospective sections plus this
navigation, no paths added/deleted. Supplied current RP-S2 outcomes and original
reviews remain attributed; RP-S1 votes do not transfer. Preserve accepted
handoffs, missing ownership/loaded-root/trust proof and original package/live
gates. No sibling/private/cloud inspection, code integration/abandonment or
substantive runtime progress is claimed.
RP-S2 SprintReview freshness: inspected clean authorized feature HEAD
`61a99cba878b62fe5df0d1de361a178d87c273a9`; updated only release-plan review
and this navigation, no paths added/deleted. Consumes accepted outgoing audit
and RP-S2 E2E FAIL without reopening them; private/ARM/exit observations remain
attributed to DevOps, not freshly verified. Original ownership/root acceptance,
strict trust, reviewed operational integration and exact-package/live gates
remain unmet; no completed initial parent is handed to RP-S3. This review
creates or abandons no task code and supplies no runtime progress or cloud-pass.
RP-S2 SprintPlan freshness: inspected clean authorized feature HEAD
`74130a8bbda12c32ac8e84523b93b8f5e09794c0`; refreshed only existing RP-S2
plan and this navigation, no paths added/deleted. Carries seven existing
original-role assignments, two resource-disjoint initial Developer lanes,
exact accepted source/commit provenance and bounded prior dispositions.
Originating ownership acceptance still gates runner writes; matched operational
integration, scoped push/accounting, formal E2E and original DevOps package/live
gates remain separate. Fresh canonical status and feature-sibling registration
do not verify sibling ownership/resolvers. Dispatch is for the existing YAML
orchestrator; no current dispatch, planning votes or live progress is inferred.
RP-S2 SprintArchitecture freshness: inspected clean application HEAD
`cf017c969720eda2dce6f2cec09f4fa142cbab2d`; refreshed cumulative architecture
and three tier slices plus this navigation, no added/deleted paths.
Consumes exact accepted RP-S1 architecture and RP-S2 design dispositions only
within their originating boundaries; no transferred reviewer votes. Supplied
offline/ARM/receipt/trust observations remain attributed, not fresh proof.
Retains original ownership acceptance, independent trust, actual loaded-root
integration, scoped Git accounting and original exact-package/live gates.
No lab/private/cloud inspection, implementation dispatch or runtime progress.
RP-S2 SprintDesign freshness: inspected clean application HEAD
`006574e6d664ec21d38a86c8e1f1cf15e162f89e`; refreshed only existing sprint
design and this navigation, with no added/deleted paths. Consumes accepted
RP-S1 design and retrospective within their originating boundaries, not RP-S2
votes. Retains F/G operator layouts, supplied designations through original
ownership acceptance, independent strict trust, joined-source validation and
actual G1-G4 release proof. Current exit-2 and private observations are attributed
to supplied DevOps reporting, not freshly verified. No new implementation,
private inspection, task dispatch, cloud operation or runtime progress claimed.
RP-S1 SprintRetro freshness: inspected clean recovery-entry SprintReview HEAD
`ca4345d5761d053e201747da4018e29c7720dd25`; refreshed existing retrospective
sections in Architecture, UserExperience and ReleasePlan plus this navigation,
with no added/deleted paths. Current supplied rounds/results are attributed,
not fresh runtime measurements. Original accepted handoffs remain closed;
current retrospective votes are not borrowed. No lab, private-evidence or
cloud inspection, code integration/abandonment or substantive progress claimed.
RP-S1 SprintReview freshness: inspected clean recovery-entry HEAD
`b13670e354102f922994ac1a1e82cf07243b2abe`; updated only release-plan review
and navigation, no added/deleted paths. Supplied source/E2E report closures
remain bounded; reported ARM/recovery observations are not independently
verified, ownership remains unaccepted and DevOps cloud-pass is false.
Retains existing tasks/owners and three sprint contracts; no runtime,
private-evidence, deployment or substantive progress claim.
Current RP-S1 SprintPlan freshness: inspected clean accepted SprintArchitecture
baseline `c888336b1741dd5cbf77f0209749620949301adb`; refreshed only the existing
recovery-entry assignment JSON and this navigation, with no added/deleted paths.
Consumes the five exact supplied completed-deliverable dispositions within their
originating boundaries. Retains seven bounded original-owner assignments, two
resource-disjoint initial Developer lanes, accepted fixture contracts, supplied
coordination through original ownership review, explicit matched-root integration
and phase-separated original E2E/DevOps gates. Fresh canonical Git status and
worktree registration are navigation evidence, not resolver proof or exclusive
writing authority. No current dispatch, reviewer agreement, sibling write, cloud
operation or substantive runtime progress is inferred.
Current RP-S1 SprintArchitecture freshness: inspected clean accepted SprintDesign
baseline `00b228bb78842df3289008be3c99ad6a88d3efe4`; updated only cumulative
architecture, three tier slices and this navigation, with no added/deleted paths.
Consumes exact supplied upstream closure references within originating boundaries,
not current reviewer votes. Retains accepted source/history/presentation contracts,
supplied coordination through original ownership review, independent trust,
matched loaded-source integration and original E2E/DevOps live gates.
No private reinspection, task dispatch, lab mutation or live capability is inferred.
Current RP-S1 SprintDesign freshness: inspected clean accepted ReleasePlan
baseline `2f22642e6f68d841c7ef40097fe1299ccd366dd8`; updated only sprint design
and this navigation, with no added/deleted paths. Consumes exact upstream closure
dispositions within their originating boundaries and retains accepted screens,
fixtures, parser contracts and original ownership/integration/E2E/DevOps gates.
Attributes successful sibling Git separately from incomplete resolver proof;
no private reinspection, runtime change, current reviewer votes or live capability
is inferred.
Current ReleasePlan Loop freshness: inspected clean accepted UX baseline
`b7aa978584b144c1cb485bec5b54e9c8da989964`; updated only release plan and
this navigation, with no added/deleted paths. Consumes exact architecture/UX
closure dispositions within their originating boundaries, not ReleasePlan votes.
Attributes successful sibling Git observation separately from incomplete
resolver/ownership proof; retains supplied designations, independent trust,
matched operational-source integration and three sprint goals/criteria.
No private receipt/sibling reinspection, task dispatch, lab mutation or live
readiness is inferred. Original ownership, E2E and DevOps gates remain unchanged.
Current Architecture Loop freshness: inspected clean application baseline
`6e08b5470f7cd21ba46505e0c8628d8f1185bc34`; updated only release architecture
and this navigation, with no added/deleted paths. Direct registered-sibling Git
status/HEAD/branch inspection succeeded; subsequent complete resolver reads
were tool-denied and no bypass or matrix execution followed. This narrows the
originating evidence gap without accepting ownership, authorizing runner writes,
changing contracts or claiming live progress. Retains original integration,
E2E/DevOps gates, canonical dirty work and all historical holds.
Current UserExperience Loop freshness: inspected clean accepted architecture
baseline `45318a50098c44843643ef1a7c5479edb4dfbd38`; updated only UX and
this navigation, with no added/deleted paths. Retains existing customer screens,
accessibility and parser contracts; distinguishes attributed direct sibling Git
evidence from unresolved resolver verification. No repeated private inspection,
new runtime progress, ownership acceptance or live capability is claimed.
Current RP-S2 SprintPlan freshness: inspected clean architecture baseline
`2fc6498ad2cd694fff76230d89731a0e2263373c`; updated only the existing RP-S2
assignment JSON and this navigation, with no added/deleted paths. Retains seven
existing assignments, supplied designations through originating ownership review,
an independent outgoing-commit audit consuming accepted current-source checks,
the exact eight-path runner allowlist and actual loaded-wrapper integration.
Original E2E/DevOps phase boundaries, strict host trust, all live gates and
historical holds remain unchanged. No substitute dispatcher, direct sibling
proof, private evidence authentication, cloud operation or live claim.
Current RP-S2 SprintArchitecture freshness: inspected clean SprintDesign baseline
`d558a721747ddea92a445b8bc45c786ba5c84664`; updated only cumulative
architecture, three tier slices and this navigation, with no added/deleted paths.
Consumes supplied RP-S1 outcomes, accepted current design and retrospective
evidence-attribution guidance without reopening originating handoffs or borrowing
their reviewer votes. Retains independent ownership/trust recovery, exact loaded
operational roots, original integration/E2E/DevOps owners and all live gates.
No private-evidence authentication, lab mutation or live capability is inferred.
Current RP-S2 SprintDesign freshness: inspected clean retrospective baseline
`a98410f479104a549fe6933df6eea3d4c6e6d132`; updated only sprint design
and this navigation, with no added/deleted paths. Consumes supplied RP-S1
outcomes and retrospective guidance in retained Screens F/G, without reopening
accepted RP-S1 screens, reports or upstream handoffs. Preserves independent
ownership/trust lanes, original reviewers and execution owners. No new UI,
public contract, private evidence authentication or live capability is inferred.
Current RP-S1 retrospective freshness: inspected clean SprintReview baseline
`1ceeb96671c446a9c0770bdbd0141f08c7ae9b77`; updated only Architecture,
UserExperience, ReleasePlan and this navigation, with no added/deleted paths.
Consumes supplied current outcomes and exact prior dispositions without
reopening accepted handoffs, repeating private probes or changing contracts.
Preserves separate ownership/trust lanes and original integration/E2E/DevOps
owners; documentation and repeated checks are not substantive runtime progress.
No current retrospective reviewer agreement, live proof or Git integration of
runner work is inferred.
RP-S1 sprint-review freshness: inspected clean baseline
`f037cd650a5869193f9bfb85453ae3b06aaabf83`; updated only the release
plan and this navigation, with no added/deleted paths. Consumes retained
offline/E2E and partial DevOps reports, not fresh cloud/private-evidence proof.
Preserves original ownership review, strict trust, existing execution owners,
unknown-effect holds and all release criteria; no new task or live claim.
Ownership-designation SprintPlan freshness: inspected clean application baseline
`e4785bbe90fea4348b5645775d976897d969b023`; updated the existing recovery
assignment JSON and this navigation only, with no added/deleted paths.
Carries supplied Developer writer/integration designations and acknowledgements
through original ownership acceptance, not premature runner-write authority.
Retains two independent initial Developer lanes, matched operational roots,
explicit Git reconciliation and phase-compatible original DevOps assignments.
Actual dispatch and current reviewer votes remain with the orchestrator; no
cloud, private-evidence authentication or live capability is asserted.
Ownership-designation SprintArchitecture freshness: inspected clean agreed
sprint-design baseline `3103c14781b4509b2bd73ff1ba763cece0f1adf0`; updated
only cumulative architecture, three tier slices and this navigation, with no
added/deleted paths. Consumes supplied writer/integration designations as original
ownership-review evidence, not accepted ownership or premature runner-write
authority. Retains matched operational-source roots, independent trust/inventory,
accepted source/UX/fixtures and original E2E/DevOps gates. No private evidence
reauthentication, lab mutation, new assignment or live capability is inferred.
Ownership-designation SprintDesign freshness: inspected clean agreed-release-plan
baseline `f9ccb6e85c80ce14f36e44cfb6e690fde0d81e80`; updated only sprint
design and this navigation, with no added/deleted paths. Consumes supplied
writer/integration designations and acknowledgements as original-review evidence,
not accepted ownership or premature runner-write authority. Retains existing
customer screens/fixtures, independent trust/inventory, matched operational roots
and original E2E/DevOps gates. No new implementation assignment, private evidence
authentication, lab/sibling mutation or live capability is inferred.
Ownership-designation release-plan freshness: inspected clean agreed-UX
baseline `87253d3f5003d1d6f34724401b33c3b5ced2e64a`; updated only the
release plan and this navigation, with no added/deleted paths. Consumes current
explicit Developer writer/integration designations and acknowledgements as
evidence for original ownership review, not accepted writing authority.
Retains three sprint contracts, accepted application/UX handoffs, independent
inventory, matched operational-source integration and original E2E/DevOps
gates. No private receipt/resolver reinspection, lab mutation, task dispatch,
identity selection or live capability is inferred.
Ownership-designation UX freshness: inspected clean agreed-architecture
baseline `f72b0f3c1206418f08fc62a149e80f7c12c55e81`; updated only UX
handoff and this navigation, with no added/deleted paths. Supplied writer and
integration-owner designations are coordination evidence for original ownership
review, not new customer input or accepted writing authority. Retains full UX
screens/tools, safe aliases, stdout/parser, matched-source joins and existing
E2E/DevOps owners. No private receipt inspection, runtime/lab mutation, new
implementation assignment or live capability is inferred.
Ownership-designation architecture freshness: inspected clean application
baseline `4212a7b59270a0fe791735385a4359a6ab30cb68`; updated only release
architecture and this navigation, with no added/deleted paths. Consumes the
current user's exact RP-S2 ownership coordination defaults without passing the
originating review or permitting runner writes prematurely. Seven named
private evidence files parsed; allowlisted local linkage/hold checks passed.
Canonical status/worktree registration were observed; direct sibling inspection
was tool-denied, so current sibling status/exclusivity is not asserted.
Retains accepted runtime/UX/assertion handoffs, matched loaded-source roots,
original E2E/DevOps gates and truthful unresolved live status. No lab mutation,
runtime/schema change, new stage or cloud operation is inferred.
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
