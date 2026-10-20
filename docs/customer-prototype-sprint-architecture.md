# Cumulative sprint architecture: evidence-ready source through live delivery

## Sprint architecture entry: RP-S1 canonical continuity contracts (October 20, 2026)

The current packet selects **RP-S1**, not the older RP-S3 overlay below.
Inspected application baseline `59a6a63c523ea3a42e89e04d751c5c063af72987`
on `feature/customer-hosted-session-prototype`; only untracked workflow context
was present. Consume Architecture `35d526ae3a9e722ebe633ba60e2ca572182a5d1e`,
UX `c70571186564cf293a63b00f08511a560b7deb11`, ReleasePlan
`8343d48b310e4d79b7d1de7b133f483475c054f7` and SprintDesign
`59a6a63c523ea3a42e89e04d751c5c063af72987`. Their supplied outcome JSON files
record original reviewer agreement for those bounded artifacts. Those votes
do not transfer to this SprintArchitecture or establish live execution.
The packet supplies no completed sprints, assignments, separate blocked-decision
list, reconciled feedback or prior dispositions. Historical overlays retain
their originating boundaries; they are not newly imposed acceptance demands.

### solutionModel and cumulative scope

The authoritative `solutionModel` is the existing
[Architecture model](customer-prototype-architecture.md#solutionmodel):
ten components, five triggered flows and eighteen uniquely identified steps.
This sprint references that model rather than duplicating or renaming it.
No components, services, public contracts, dependencies or model IDs change.

| Tier | Canonical components and implementation boundary |
|---|---|
| [Coordinator](requirements/coordinator/architecture.md#rp-s1-canonical-coordinator-contract) | `coordinator` (**Hosted coordinator**), `decision-routing` (**Decision-1 routing and admission**) and `workflow-checkpoints` (**MAF workflow checkpoints**). Retain explicit begin/route/execute/publish in `demo/workflow.py`, checkpoint wiring in `demo/host.py`, routing after deterministic gates and fenced current-output acceptance. |
| [Specialists](requirements/specialists/architecture.md#rp-s1-canonical-specialist-contract) | `architect` (**Hosted architect**), `reviewer` (**Hosted reviewer**) and shared `conversation-state` (**Parent and specialist conversation state**). Retain remote session restoration in `demo/foundry.py` and five-stage model-history paths in both role modules. |
| [Client/release](requirements/client-release/architecture.md#rp-s1-canonical-client-release-contract) | `terminal-client` (**Terminal client**) and `release-toolchain` (**Guarded lab release toolchain**). Retain opt-in finalized human stderr, unchanged stdout/parser and external guarded tooling; source ownership is not operational installation. |
| Shared support, defined once | `artifact-plane` (**Private Blob artifacts and effect journal**) supports all three hosted roles; `identity-boundary` (**Trusted identity and private transport**) supports the terminal, roles and artifact plane. Keep their canonical support links, trusted scope, exact immutable refs, private MI path, ETag/fencing and unknown-effect holds. Tier references do not create separate stores or identities. |

| Canonical flow | Trigger, current refinement and cumulative boundary |
|---|---|
| `remote-collaboration` — **Remote design and review** | A fresh synthetic initial requirement triggers `collaboration-bind`, `collaboration-route`, `collaboration-design`, `collaboration-review`, `collaboration-return`. RP-S1 retains directly testable repeated-call contracts and Screens A-D. Actual trusted architect then reviewer ingress, common-bundle provenance and live coordinator acceptance remain RP-S2. |
| `two-turn-continuity` — **Same-parent specialist continuation** | A queue follow-up to a completed non-held parent triggers `continuity-revise`, `continuity-invoke`, `continuity-verify`. RP-S1 fixes the offline comparison boundary below; actual same-parent live proof remains RP-S3 after RP-S2's initial-parent gate. |
| `supported-recovery` — **Supported compute stop and resume** | One retained-script stop request triggers `recovery-stop`, `recovery-resume`, `recovery-verify`. Preserve durable once-only marker, independently confirmed stopped/idle state, original bindings, checkpoints and reconciled effects; no hard-crash or exactly-once claim. Execution remains RP-S3, not an RP-S1 exit condition. |
| `parent-isolation` — **Separate-parent isolation** | A separate synthetic parent on a verified release triggers `isolation-bind`, `isolation-execute`, `isolation-verify`. Require distinct child/history/artifact scope and first-parent requirement exclusion. Its release prerequisites and initial-parent comparison do not depend on successful follow-up/recovery. |
| `guarded-release` — **Exact-source guarded release** | Reviewed owned commits trigger `release-join`, `release-package`, `release-discriminate`, `release-close`. Retain actual loaded-root integration, formal local-script E2E, serialized original DevOps and all exact-source/package/live closure gates. Preparation/inventory is independent of runner coding; no second publisher. |

### RP-S1 contract-first handoff

The actual source chain is parent-scoped `manifest.children.get(role)` in
`WorkflowRuntime.execute()` -> `RemoteAgents.invoke()` restoring
`AgentSession.from_dict(child.framework)` at the pinned version -> each
specialist's `load_or_create_llm_session()` loading `specialist_history_v2`
-> model call -> validated immutable output and stored model continuation.
The remote child framework session and specialist internal model history are
different. Compare stable identity fields and pins, not whole serialized state:
response IDs and continuation state must advance. Conversation history, MAF
checkpoints, artifacts and write-ahead effects remain four distinct concerns.

| RP-S1 criterion | Retained implementation/check interface and receiving owner |
|---|---|
| Two-turn continuity | `tests/test_workflow.py` binding assertions compare parent scope, both hosted/framework child identities and pins, exactly two child creations, both roles on both turns, fresh invocation responses, exact current prerequisite refs and stale-approval invalidation. Integration/E2E checks relevant joined source; alias equality and recalled requirements are insufficient. |
| Controlled repeated calls | Retain `test_reject_revise_review_reuses_both_children_with_fresh_responses`: architect -> blocked reviewer -> same architect -> same reviewer, four new responses and accepted current revisions. This controlled graph uses synthetic boundaries, never live specialist evidence. |
| Direct specialist history | Retain both roles' load/model/store and serialized-value assertions in `tests/test_specialist_continuity.py`, identical-brief fresh-history controls, exact-response zero-send recovery and held/mismatched-effect negatives. Replayed full briefs do not replace these controls. |
| Clarity without parser drift | Consume accepted SprintDesign Screens A-D and `HumanView` / `finalize_workflow_turn` in `demo/terminal.py`; retain `HumanTerminalTests` in `tests/test_demo.py`. Useful current candidate/review and chronological calls appear in opt-in human stderr after finalization. Machine stdout/parser and privacy/control neutralization remain unchanged; the human view is observational, not a continuity verifier. |
| Attributable checks and supported identity assessment | Original source-check/integration owners retain exact changed-source checks and the explicit repository-index closing action. Existing recovery assessment and finite A/B contract provide an actionable unresolved handoff. No new research, renderer or fixture assignment is justified merely by a blocked release. |

### Prior blockers and downstream decisions

Neither identity path is live-selected. The specialist-only B source candidate
is not a measured A correction, automatic fallback or proven ingress remedy.
Historical `NATIVE_HOST_PRINCIPAL` occurred before architect application
execution; it does not prove the current candidate fails, a provider defect or
a missing grant. Preparation rejection leaves receivers unreached. Original
DevOps must discriminate with actual trusted receiver evidence, architect before
reviewer, under the retained finite scripted contract. Necessary demonstrated
chosen-path permissions are pre-approved with exact scope/rationale and
readback; no speculative grant, opaque-call-ID user identity or receiver
equality relaxation is authorized. A material namespace/contract change uses
existing Scrum reconciliation and Architect-advised Product Owner decisions.

For exact originating ownership reference
`["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-LAB-OWNERSHIP/AssignedWorkDeveloperLoop","lab-ownership-review-evidence-access"]`,
consume supplied `ownershipRecoveryDefaults` as acknowledgement/designation,
not substantive ownership acceptance. Existing Developer completes attributable
owned-path/resolver/root evidence for original Architect/Critic review before
eight-path sibling runner writes. This turn does not retry earlier denied
inspection, certify current sibling state or reopen that task's acceptance.
Use approved mirrored evidence and accepted fingerprint references first;
no renewed user authority is missing for that bounded read-only work.

Designated integration Developer then joins reviewed commits with actual
loaded operational roots/bytes/hashes, preserves `LAB_TOOL_OWNER_MISMATCH`
and records task/branch/commit accounting, including reasons for any retained
abandoned code branches. A registered sibling or clean Git does not install
the operational wrapper. Original E2E validates the exact join through local
scripts. In parallel, existing transport/DevOps owners prepare current
containment-source/resource, strict trust, inventory/rollback and unresolved
effect evidence. Original DevOps alone serializes guarded publication and live
G1-G8 after exact-source, retained-suite, Linux hosting-package and preview gates.
Scrum owns minimal dependencies, path ownership, real shared exclusive resources
and Git reconciliation; this architecture assigns no competing task graph.

Preserved untracked workflow context currently causes repository-index drift.
Scrum/integration coordinates its preservation and exclusion from customer Git
then reruns the unchanged `scripts/Test-Repository.ps1`; do not index private
workflow control-plane output, remove unowned files or waive AC7. This does
not require changing the portable application or extending RP-S1 to all live
criteria. All AC1-AC9/G1-G8 remain required for release. Preserve UNKNOWNs,
held parents, rollback assets, unrelated work and historical cleanup uncertainty.
Blob Contributor remains account-wide: isolation is application-enforced,
not storage-RBAC or malicious-host isolation.

### Validation of this sprint refinement

An in-memory document check verified all ten canonical components, five flows,
eighteen steps, three tier entries and seven resolving local/anchor links.
The existing absolute validated Python 3.12.10 executable ran `Test-Demo.ps1`
with an explicit canonical lab root: dependency checks, **204 offline tests
in 53.413 seconds** and compilation passed (exit 0). No dependencies were
installed. Standalone `scripts/migration.py public-check` passed across
**83 Git-visible files**; owned Git whitespace checks passed.

The unchanged `scripts/Test-Repository.ps1` failed its first gate with
`REPOSITORY_INDEX_STALE` (exit 1); its later gates did not execute. Read-only
comparison found four added untracked workflow-audit JSON inventory entries
and zero removals, not added customer source. Those unowned files remain
preserved/excluded from this commit and the public inventory. The closing
action above remains required. No lab source changed; the full retained lab
suite and actual Linux/amd64/hosting-Python package checks were not run.
These local checks validate the documented source boundary, not live progress.

Architect accepts this bounded current-sprint/cumulative/tier design for
original Product Owner, Critic and Red Team review; their votes for this loop
are not yet supplied.
No settings import, fresh cloud inventory, permission mutation, publication,
inference, stop/resume, operational integration, final push or live success is
claimed. Documentation completion is not new runtime progress.

<a id="current-rp-s3-gated-continuation-recovery-isolation-and-delivery-october-20-2026"></a>

## Historical RP-S3: gated continuation, recovery, isolation and delivery (October 20, 2026)

Current sprint is **RP-S3: live continuity, recovery, isolation and customer
delivery**. Inspected clean authorized feature baseline
`23a4d9a950a73a57c13f6b29a9ca6da685e5c987`, containing accepted current RP-S3
SprintDesign. Consume accepted RP-S2 architecture
`1bce6e1c4fe9e8deb8382fa02c44392bc2d25aea`, SprintReview
`1e5eb2adc7714875e07ed69ffd2e2db0ab8c7877` and retrospective
`afe6d4dba937102e12821d770c1f7da4788f1c2c`. Completed RP-S1/RP-S2 workflow
history does not establish their live release goals. Earlier overlays retain
their original attribution; this section governs the current sprint mapping.

### Cumulative design and entry boundary

Retain exactly three remote hosted roles and explicit coordinator
begin/route/execute/publish. The trusted parent manifest's `children.get(role)`
creates or reuses each specialist binding; `RemoteAgents.invoke()` restores
its framework `AgentSession` and pinned version. Each specialist separately
restores `specialist_history_v2` before its model call and persists history
after validated immutable output. Conversation/model history, MAF checkpoints,
immutable artifacts and fenced write-ahead effects are distinct responsibilities.
Keep trusted receiver equality, exact prerequisite/producer/version/revision/hash
checks, coordinator ETag/fencing, Decision-1 after deterministic gates and
unknown-effect holds. No runtime rewrite, new service, generic session manager,
schema, collector, ledger, flag, dependency or duplicate fixture work is needed.

**Entry is BLOCKED:** verified common-bundle G1-G4 and a completed non-held
initial parent are not established. Neither identity path is live-selected.
The latest ownership outcome remains substantively incomplete; runner writes
remain blocked. Supplied coordination and accepted host-trust references are
available, not missing authority. The reported prerequisite PASS remains
owner-attributed: inspected script scope is not independently inspected execution
or current deployment/rollback proof. This task does not refresh private evidence,
earlier access denials, operational installation or cloud state.

### RP-S3 evidence joins and execution dependencies

| Boundary | Required evidence and existing owner |
|---|---|
| Initial-parent readiness | Existing ownership Developer supplies actual nonsecret resolver/Git/path/hash/root-matrix evidence or restores already-authorized bounded read access; originating Architect/Critic substantive acceptance precedes eight-path sibling runner writes. Designated integration Developer reconciles reviewed commits and actual loaded roots/bytes/hashes with durable Git accounting. Original E2E validates that exact join. DevOps independently completes current trust/inventory/rollback/effect preparation, exact-source/retained-suite/Linux hosting-package gates and serialized guarded release; G1-G4 must establish one final common bundle, both remote artifacts, private managed-identity Blob provenance, genuine Decision-1 and the completed non-held initial parent. Accepted blocked reports do not supply readiness. |
| Queue follow-up / AC2, G5 | Original DevOps uses the same private session file and completed parent, not a replacement or held parent. Both roles execute on both turns: compare actual parent and both children's hosted/framework identity fields and pinned versions; continuation fields may advance. Exactly two child creations across the pair, fresh invocation response IDs, current queue-plus-private-ingress requirements and stale-approval invalidation are required. Useful output and safe aliases are presentation, not proof. |
| Repeated calls / AC3 | Consume accepted offline architect -> blocked reviewer -> same architect revision -> same reviewer controls and both-role restored-history/fresh-history tests. Direct model continuation is separate from replayed briefs; do not relabel mocked calls live or reimplement accepted tests. Live AC1/AC2 remain independent obligations. |
| Supported recovery / AC4, G6 | Once the original parent is completed and non-held, use the retained local stop/resume script path and durable once-only marker. Independently observe the same pinned parent stopped/idle with advanced stop metadata before continuation. Verify original parent/both-child bindings, retained checkpoints and reconciled cumulative effects with no duplicate creates/sends. A known-response GET is not a new invocation. Missing confirmation or unknown effects hold execution; no repeated stop, blind resend, hard kill or hard-crash claim. |
| Separate parent / AC4, G7 | DevOps creates a separate synthetic parent on the verified release only when its own source, trust, effect and resource prerequisites pass. Compare distinct child/history/artifact scope and exclusion of the first parent's requirements. This does not depend on successful recovery; serialize shared mutation without inventing a recovery dependency. Account-wide Blob Contributor means application-enforced isolation, not storage-RBAC or malicious-host isolation. |
| Delivery / AC6-AC9, G8 | Keep Screens H-K, README source path, useful current output and opt-in human stderr with unchanged stdout/parser. Private machine observations back a separate sanitized companion; no full identifiers, private roots, transcripts or evidence locators enter customer output/Git. Final exact-source/common-package checks, reviewed scoped feature push and durable integration or retained-branch accounting remain required. Record all AC/G outcomes, reproducible setup/command, exact final/rollback bindings, limitations and positively identified new owned cleanup separately from historical cleanup uncertainty. Missing proof yields BLOCKED, never customer-ready. |

### Observation contract, not a new acceptance implementation

Consume `live_acceptance.validate_scenario_evidence()` and
`tests/test_scenario_evidence.py`, documented in
[design.md](design.md#offline-cross-scenario-evidence-assertions). The existing
private inputs `initial`, `followup`, `restart`, `isolated` and `stopped_session`
join per-scenario proof, scoped manifests, complete cumulative operations,
independent create/send captures, checkpoints and confirmed stop observations.
Capture completeness and association with actual scoped stores remain execution
owner obligations. Do not synthesize requests from journal intentions, deduplicate
duplicate sends, omit unresolved transitions or infer measured zeroes from
missing observations. Caller-supplied JSON passing assertions proves internal
consistency, not independent provenance or live capability.

Original E2E validates the reviewed operational join through local scripts;
original DevOps owns actual collection, serialized release and live acceptance.
Scrum retains contract-first decomposition, minimal dependencies, named exclusive
resources for shared CLI/transport/mount/publication mutation and assignment of
Git reconciliation. Inventory remains independent of runner coding. No substitute
agents, extra approval stage, GitHub Actions or deployment occurs here.

### Dispositions and bounded architecture handoff

Preserve `["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-LAB-OWNERSHIP/AssignedWorkDeveloperLoop","lab-ownership-review-evidence-access"]`:
actual evidence and substantive originating acceptance remain required; do not
repeat denied probes or substitute summaries/trust receipts. Preserve accepted
source checks under
`["yaml-loops-v1:sprint/1/RP-S1/task/RP-S1-CURRENT-SOURCE-CHECKS/AssignedWorkDeveloperLoop","current-source-checks-completion-status"]`
and accepted FAIL reporting under
`["yaml-loops-v1:sprint/1/RP-S1/EndToEndTestLoop","e2e-report-completion-status"]`.
Keep bounded DevOps reports closed under
`["yaml-loops-v1:sprint/1/RP-S1/DevOpsWorkLoop","devops-bounded-assessment-completion-status"]`
while actual cloud-pass obligations remain under
`["yaml-loops-v1:sprint/1/RP-S1/DevOpsWorkLoop","devops-exact-release-cloud-pass"]`.
Upstream Architecture/UX/ReleasePlan and prior sprint design/architecture,
review and retrospective agreements remain closed within their originating
boundaries; no votes transfer to this RP-S3 architecture loop. No disposition
is superseded or actual acceptance failure waived.

The cumulative design and current [coordinator](requirements/coordinator/architecture.md),
[specialists](requirements/specialists/architecture.md) and
[client/release](requirements/client-release/architecture.md) slices are complete
for original Product Owner, Critic and Red Team assessment. Their current RP-S3
votes are not yet supplied. AC1-AC9/G1-G8 remain unestablished as a release;
preserve UNKNOWNs, held parents, rollback assets, unrelated work, originating
stops and no-progress history. Documentation changes are not runtime progress.

<a id="current-rp-s2-ownership-evidence-exact-execution-join-and-initial-collaboration-october-20-2026"></a>

## Historical RP-S2: ownership evidence, exact execution join and initial collaboration (October 20, 2026)

Current sprint is **RP-S2: supported repair and exact three-role remote
collaboration**. Inspected clean authorized feature baseline
`76c797b509f0e8ee53d11ce1fbc275d4ad8ccd59`, containing current RP-S2
SprintDesign. Consume accepted RP-S1 cumulative/tier architecture
`302d8866d3c4f4c4d61b7c63c7f4d24196da664d`, source-check handoff
`b74b84edb6c05fb4dc7f58ba7f88925e2402ddc9`, SprintReview
`350352282f6defafc777dff5c6748d7fb2da3b59` and retrospective
`30c4a534bad1aa38b6b8f46a246c9b84262ecf18`. RP-S1 is completed workflow
history, not a successful live release. Earlier overlays below retain their
original attribution; this section governs the current sprint mapping.

### Retained holistic design

Keep exactly three hosted roles and the existing coordinator's explicit
begin/route/execute/publish sequence. Parent-scoped manifest child lookup,
restored remote `AgentSession` and pinned versions preserve each specialist's
binding; each role separately restores `specialist_history_v2` for model
continuation. Conversation history, workflow checkpoints, immutable artifacts
and fenced write-ahead effects remain separate state concerns. Retain exact
prerequisite/producer/version/revision/hash acceptance, trusted receiver
equality, coordinator ETag/fencing, calibrated Decision-1 after deterministic
gates and unknown-effect holds. No framework rewrite, generic session manager,
fourth service, public schema, CLI flag or duplicate fixture implementation.

### Current blocker and contract-first execution joins

| Boundary | Required handoff and existing closing owner |
|---|---|
| Ownership evidence before runner writes | Under `["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-LAB-OWNERSHIP/AssignedWorkDeveloperLoop","lab-ownership-review-evidence-access"]`, the existing Developer recovers actual nonsecret sibling resolver contents, attributable branch/HEAD/base, eight-path statuses, owner-specific hashes with line-ending explanation and source-bound matched/crossed-root results through the approved external handoff, or restores already-authorized read access. Original Architect/Critic substantive acceptance remains required. Supplied writer/integration designations resolve coordination only; qualified report agreement does not enable writing. Do not repeat denied inspection or substitute reconstructed source, historical trust receipts or another summary. |
| Bounded retained runner | After substantive acceptance, Developer implements only the existing eight-path sibling assignment. Preserve `LAB_TOOL_OWNER_MISMATCH`, competing-owner rejection, scenario/source/package/version checks before parent creation, architect-before-reviewer order, exact-response recovery and unknown-effect holds. Negative fixtures measure zero create/send at rejected preparation boundaries; absent observations do not imply zero effects. No live path selection is claimed by offline tests. |
| Reviewed source to actual loaded source | Designated integration Developer reconciles reviewed application, runner and necessary operational-wrapper commits on authorized feature branches, preserving unrelated dirty/staged canonical work. Record actual loaded roots, bytes/hashes, matched-root success and crossed-root rejection tied to those bytes. Sibling registration, clean Git or a runner commit does not install the operational wrapper. Keep root guards; unresolved installation is not execution-ready. Record task/branch/commit/reason for retained abandoned work durably on the feature branch; preserve those branches. |
| Original E2E readiness | Validate the exact subsequent reviewed join through local repository scripts. Accepted application-only checks and the completed accurate predeployment FAIL report remain closed; neither establishes operational integration. Consume accepted tests rather than reimplementing them. |
| Independent DevOps preparation and release join | Current strict trust, validated sole-target context, deployed/rollback inventory and effect reconciliation are independent of offline coding. After the implementation/E2E join and actual preparation, original DevOps passes exact-source application/repository/retained-tooling, Linux/amd64/hosting-Python and exact-package gates, then uses the serialized guarded publisher for exactly three existing roles. A metadata receipt or mixed diagnostic bundle is not final G1. |

Accepted fingerprint/reference inputs are supplied; use them through retained
strict tooling rather than seeking renewed trust authority. Current transport
and rollback availability still require actual verification. No private
ownership evidence, resolver access, cloud state or receipt authentication was
refreshed in this architecture task. The supplied latest ownership outcome
remains incomplete and runner writing remains blocked. This is the existing
evidence-access closing condition, not a newly invented approval stage or a
request for expanded user authority.

### Supported identity decision and RP-S2 exit

Neither A2A/authentication correction nor specialist-only `x-ms-user-identity`
delegation is live-selected. Choose the smallest supported path only through
the retained finite scripted decision contract. Necessary chosen-path
permissions are already authorized at documented exact scope/rationale, with
retained deterministic execution and readback; speculative grants, opaque
call-ID-as-user substitution, receiver-equality weakening and automatic
fallback remain excluded. Preparation failure leaves receivers unreached;
observed rejection identifies the reached receiver boundary; uncertain effects
remain held and are not retried to produce a decisive-looking result.

Observe trusted architect ingress before reviewer dispatch, then independently
prove reviewer ingress using exact current immutable prerequisites. Selection
alone is not the sprint exit. G1-G4 additionally requires three healthy exact
versions on one verified common bundle, actual coordinator acceptance of both
roles' artifacts, private managed-identity Blob provenance and genuine
Decision-1 with deterministic final gates. Original DevOps owns those live
observations. Unresolved identity selection does not stop remaining artifacts,
but an actionable unresolved report cannot satisfy this live sprint goal.

Only an actual completed, non-held initial parent on that verified bundle
enables RP-S3's queue follow-up and supported once-only confirmed compute
stop/resume. Preserve parent/both-child hosted/framework bindings and pins,
fresh responses, exactly two child creations across the initial/follow-up
pair, current requirements and stale-approval invalidation. Retain accepted
four-call revision and direct-history/fresh-history controls as offline proof.
Separate-parent isolation remains independent of successful recovery and needs
distinct real child/history/artifact scope. Account-wide Blob Contributor
policy provides application-enforced, not storage-RBAC or malicious-host,
isolation. Preserve historical UNKNOWNs, held parents, rollback assets,
unrelated work and historical cleanup uncertainty; AC1-AC9/G1-G8 remain intact.

### Tier handoff and agreement scope

Current slices are [coordinator](requirements/coordinator/architecture.md),
[specialists](requirements/specialists/architecture.md) and
[client/release](requirements/client-release/architecture.md).
Scrum retains decomposition, minimal dependency edges, named exclusive resources
for actual shared mutation and Git reconciliation assignment. No task is
redispatched here. Original E2E and serialized DevOps retain their original
execution gates, using local scripts rather than GitHub Actions.

The five prior completion dispositions for Architecture, UX, ReleasePlan,
RP-S1 SprintDesign and RP-S1 SprintArchitecture remain confined to their exact
originating accepted handoffs. In particular,
`["yaml-loops-v1:sprint/1/RP-S1/SprintArchitectureLoop","sprint-architecture-completion-status"]`
closes RP-S1 only; its votes do not transfer to this RP-S2 loop.
Preserve accepted source checks and E2E FAIL reporting under their originating
completion references. Preserve the two distinct DevOps references
`["yaml-loops-v1:sprint/1/RP-S1/DevOpsWorkLoop","devops-bounded-assessment-completion-status"]`
and `["yaml-loops-v1:sprint/1/RP-S1/DevOpsWorkLoop","devops-exact-release-cloud-pass"]`:
bounded reports remain complete while enclosing cloud-pass remains unmet.
No disposition is superseded or acceptance criterion waived.

Architect considers this documentation handoff complete for original Product
Owner, Critic and Red Team review. Current RP-S2 reviewer votes are not supplied.
This task changes only architecture/navigation documentation; it claims no new
runtime, test-fixture, ownership, integration, identity-selection or live
capability progress. Documentation validation is reported in the owner handoff,
not inferred from earlier overlays' test results.

<a id="current-rp-s1-accepted-recovery-inputs-and-continuity-handoff-october-20-2026"></a>

## Historical RP-S1: accepted recovery inputs and continuity handoff (October 20, 2026)

This invocation selects **RP-S1: evidence-ready source and understandable
continuity**. No assignments, completed sprints or separate blocked-decision
list were supplied. Inspected clean feature-branch baseline
`a1e85442a90a2333bedd6e4beed1d8d849a68ad9`. Consume accepted Architecture
`25d182245a1bb40b842f5787196bd8f8244c4a7d`, UX
`c5e7189252886a653daa42cbf9021f0cf59691b2`, ReleasePlan
`0d0f17b928ba99517551ba20a0c0201801148d9d` and SprintDesign at that baseline.
Earlier overlays below are retained history; their sprint selection, votes,
execution counts and stops are not current observations.

### Holistic design and current criterion joins

Keep exactly three hosted roles, pinned MAF/Foundry and the existing explicit
coordinator begin/route/execute/publish sequence. Parent-scoped manifest
`children.get(role)` creates or reuses hosted/framework bindings and immutable
version pins. `RemoteAgents.invoke()` restores the child's `AgentSession`;
each specialist separately restores `specialist_history_v2` before its model
call. Conversation/model history, workflow checkpoints, immutable artifacts
and fenced write-ahead effects are distinct state responsibilities.

| RP-S1 obligation | Retained contract and evidence handoff |
|---|---|
| Two user turns | Compare actual parent and both roles' hosted/framework identity fields and pinned versions, not entire evolving serialized sessions. Both roles execute on both turns; exactly two children are created across the pair. New invocations have fresh responses, queue follow-up preserves private ingress, and current revisions invalidate stale approval. |
| Repeated orchestration | Preserve controlled architect -> blocked reviewer -> same architect revision -> same reviewer fixtures, both-role binding checks and fresh responses. Existing specialist load/model/store tests and identical-brief fresh-history controls prove continuation separately from replayed requirements. These remain offline controls. |
| Customer clarity | Consume accepted SprintDesign Screens A-D, README goal/diagram/source path and useful `--native --view human` stderr. Default stdout, delegation/result records and acceptance parsing stay unchanged; safe aliases alone prove nothing about bindings. |
| Exact-source checks and supported-remedy handoff | Existing Developer checks cover retained source/fixtures; original E2E owns formal joined-source validation. An actionable unresolved identity finding can satisfy bounded research, never live ingress or release acceptance. Report the reached boundary, missing evidence and existing closing action. |

No rewrite, generic session manager, fourth service, framework/dependency,
public schema, CLI flag or duplicate fixture/presentation implementation is
needed. Preserve trusted receiver equality, exact immutable prerequisites,
producer/version/revision/hash checks, coordinator ETag/fencing, calibrated
Decision-1 after deterministic gates and explicit unknown-effect holds.

### Blocker resolution boundaries and downstream closing actions

Accepted Architecture reports matching supplied host-trust references and
successful direct sibling Git inspection, but incomplete resolver inspection
after denied reads. These are attributed inputs, not refreshed here.
**Accepted trust input is supplied; current strict transport is unverified.**
DevOps must use that accepted fingerprint and evidence reference through the
retained strict wrapper, not request them again or replace them with a newly
observed key. Supplied ownershipRecoveryDefaults resolve missing writer
acknowledgement/integration designation only. Existing Developer completes
point-in-time eight-path sibling ownership/resolver evidence and original
ownership review before runner writes; never write the dirty canonical lab.

The designated Developer joins reviewed application, runner and actually
loaded operational wrapper bytes with matched roots, exact hashes and durable
task/branch/commit accounting. Preserve `LAB_TOOL_OWNER_MISMATCH`: a clean
sibling or committed runner is not operational installation. No guard bypass,
shared branch switch, uncertain resend or adoption of held parents is allowed.
Independent application checks and offline runner coding do not depend on live
inventory; DevOps trust/context/inventory can proceed independently of coding.

Neither A nor specialist-only B is live-selected. Evaluate the smallest
supported candidate through the retained finite scripted decision contract.
Reject source/root/scenario/package/version mismatches before creating a
parent; preparation failure is not receiver failure. Prove architect ingress
and trusted equality before reviewer dispatch, then prove reviewer ingress
independently. Necessary chosen-path permissions are already authorized at
documented exact scope/rationale through retained mechanisms/readback; no
speculative grant, call-ID-as-user substitution or equality relaxation.
Unresolved selection must not halt remaining artifacts.

Scrum retains decomposition, minimal dependencies, exclusive-resource planning
and integration assignment. Original E2E uses local repository scripts.
Original DevOps serializes publication/transport/profile/mount/stage mutation
and owns exact-source application/repository/retained-tooling and actual
Linux/amd64/hosting-Python package gates, guarded publication and live acceptance.
RP-S2 needs common-bundle G1-G4 and a completed non-held initial parent; only
then does RP-S3 continue that parent's queue turn and once-only confirmed
supported stop/resume. Separate-parent isolation needs the final release, not
successful recovery first. Preserve AC1-AC9/G1-G8, rollback assets, historical
UNKNOWNs, held parents and historical cleanup uncertainty. Account-wide Blob
Contributor isolation is application-enforced, not storage-RBAC or malicious-host
isolation. This design creates no new approval stage or release waiver.

### Tier outputs and bounded agreement

Current RP-S1 slices in [coordinator](requirements/coordinator/architecture.md),
[specialists](requirements/specialists/architecture.md) and
[client/release](requirements/client-release/architecture.md) implement this
mapping. Apply only the supplied originating completion dispositions:
`["yaml-loops-v1:ArchitectureLoop","architecture-completion-status"]`,
`["yaml-loops-v1:UserExperienceLoop","ux-completion-status"]`,
`["yaml-loops-v1:ReleasePlanLoop","release-plan-completion-status"]` and
`["yaml-loops-v1:sprint/1/RP-S1/SprintDesignLoop","sprint-design-completion-status"]`.
Those accepted handoffs stay closed; their votes do not transfer to this
SprintArchitecture Loop or originating ownership review.
Architect agrees with this cumulative/tier design for original Product Owner,
Critic and Red Team review. Current-loop reviewer agreement is not yet supplied.
No fresh private evidence, sibling resolver, cloud, deployed binding, identity
selection, push or release acceptance is claimed by this mapping.

### Verification of this handoff

Existing absolute lab Python 3.12.10 ran `Test-Demo.ps1` with explicit lab
root: dependency checks, **204 offline tests in 45.916 seconds**, compilation
and script exit 0. `scripts/Test-Repository.ps1` passed current index,
79-public-file boundary, JSON/PowerShell/context and whitespace checks.
No dependencies were installed. No runtime or retained lab source changed;
full retained lab suite, Linux hosting-package checks, formal E2E and cloud
operations were not run. These repeated local checks are not new live progress.

<a id="current-rp-s3-live-continuity-recovery-isolation-and-truthful-delivery-october-20-2026"></a>

## Historical RP-S3: live continuity, recovery, isolation and truthful delivery (October 20, 2026)

Current sprint is **RP-S3**. Inspected clean application HEAD
`1f24c9a07277d2f5b111f83b186db3ad6a5257aa` on
`feature/customer-hosted-session-prototype`. Consume accepted RP-S2 cumulative
and tier architecture at `74130a8bbda12c32ac8e84523b93b8f5e09794c0`,
retrospective at `dd7728cb80b503883d96d3317a3dd5dee28f1c6e`, and RP-S3
SprintDesign at inspected HEAD. RP-S1/RP-S2 are completed workflow history,
not completed live release gates. This section is the current mapping; earlier
overlays retain their attributed observations and technical history.

### Retained system and actual entry handoff

Retain exactly three hosted roles: terminal -> coordinator MAF
begin/route/execute/publish -> remote architect and reviewer -> deterministic,
fenced acceptance. Parent-owned manifest child lookup, restored remote
`AgentSession`, pinned versions and each specialist's `specialist_history_v2`
remain distinct continuation links. Conversations/model history, graph
checkpoints, immutable artifacts and write-ahead effects are separate state
concerns. No rewrite, fourth service, session manager, history migration,
framework, public schema, CLI flag or comparison ledger is introduced.

Live follow-up requires an actual completed, non-held initial parent with
G1-G4 evidence for the exact final common bundle: three healthy pinned roles,
remote accepted artifacts, private managed-identity provenance and genuine
Decision-1 after deterministic gates. An agreed failure report or selected
identity path does not establish that handoff. Supplied RP-S2 outcomes establish
neither it nor a live-selected identity path; current continuation remains
**BLOCKED**, not an instruction to send into absent or held state.

The existing Developer completes substantive recovery-record reconciliation,
current eight-path sibling status and no-write Python/PowerShell matched-root
acceptance and mismatched-root rejection for originating Architect/Critic
ownership acceptance before runner writes. Supplied designations suffice for
coordination, not proof. Reviewed runner implementation and actual loaded
operational/source integration follow under their existing assignments.
Independently, established transport-owner/user coordination supplies the
previously accepted fingerprint/reference or exact private evidence locator;
original DevOps compares through retained strict tooling before current private
inventory. No renewed designation, trust replacement, repeated unattended denied
probe or dependency from offline coding to live inventory is introduced.

### RP-S3 cross-tier evidence joins

| Obligation | Required comparison and existing execution boundary |
|---|---|
| AC2 / G5: two user turns | Reuse the completed parent's private session file. Compare actual parent and both roles' hosted/framework identity fields and pinned versions; both roles run on initial and queue follow-up turns, with exactly two child creations across that pair and fresh response IDs for new invocations. Preserve private ingress and earlier requirements, add the queue, invalidate stale approval and accept only current immutable prerequisites, revisions, hashes and producers. |
| AC3: repeated orchestration | Retain controlled architect -> blocked reviewer -> same architect -> same reviewer fixtures, both-role binding assertions and direct load/model/store continuation with identical-brief fresh-history controls. These are accepted offline controls, not live success or a new fixture implementation assignment. |
| AC4 / G6: supported compute recovery | Use the existing durable once-only stop marker, supported stop and confirmed stopped/idle state before same-conversation continuation. Compare original parent/both children, pins, checkpoint/effect retention and actual sends. Known-response retrieval is not a new invocation. Unconfirmed/unknown effects stay held; never delete markers, resend or infer no duplicates from resumed output alone. This is not hard-crash recovery or exactly-once deployment. |
| AC4 / G7: separate-parent isolation | Use a separate synthetic parent and private session file; verify distinct actual parent/both-child bindings and artifact scope, exclusion of first-parent requirements and passing cross-scope rejection regressions. Filenames or aliases are insufficient. Isolation and recovery have no invented dependency on each other; their actual shared mutations remain serialized. |
| AC6-AC9 / G8: understandable truthful delivery | Retain README and Screens H-K, useful opt-in human stderr and unchanged machine stdout/parser. Supply sanitized comparison outcomes separately from private exact evidence. Require final exact-source/package checks, reviewed scoped feature push/accounting, actual final/rollback bindings, reproducible setup/demo command, newly owned cleanup and explicit historical uncertainty. Customer-ready requires every AC1-AC9/G1-G8, not report agreement. |

Compare stable identity fields, not entire serialized sessions: continuation
state advances. Replayed briefs, plausible memory prose, display aliases and
HTTP success cannot prove hosted/framework continuity or model history.
Trusted receiver equality, specialist-only candidate delegation, immutable
prerequisites, coordinator ETag/fencing and unknown-effect holds remain intact.
Do not rekey specialist history, adopt held parents or substitute call IDs for
delegated identity. Account-wide Blob Contributor isolation remains
application-enforced, not storage-RBAC or malicious-host isolation.

### Exact-source execution and original-owner handoff

Consume the existing `live_acceptance.validate_scenario_evidence()` and
`tests/test_scenario_evidence.py` assertions for private scenario snapshots,
cumulative operation transitions and independently observed create/send counts.
They perform offline comparisons, not collection or cloud execution. Accepted
source checks and the revision-bound outgoing audit remain attributed accepted
inputs; no duplicate implementation or status-only rerun is requested.
Designated Developer integration supplies reviewed joined commits, actual loaded
roots/bytes/hashes and joined checks to subsequent formal E2E. Any concrete
missing execution join belongs to existing Developer/Scrum decomposition.

Original DevOps retains current strict trust/inventory, exact-source application,
repository and affected retained-tooling checks, Linux/amd64/hosting-Python
package validation, immutable source/package joins, fresh previews and guarded
publication before live gates. Use deterministic local repository scripts,
not GitHub Actions. Serialize publication, transport, CLI, mount and package
mutation; architecture dispatches no work. Preserve rollback assets, historical
UNKNOWN publications, held parents, unrelated dirty/staged work and historical
cleanup uncertainty. New owned cleanup cannot certify historical cleanup.

The supplied latest DevOps boundary is shellId 389, outer exit 2,
`HOST_TRUST_EVIDENCE_REQUIRED`; accepted RP-S2 E2E remains predeployment FAIL.
These are attributed reports, not fresh observations here. Structural recovery
JSON checks, historical trust strings and authenticated ARM prerequisites do not
prove substantive ownership, independent host trust, actual operational
installation or live specialist ingress. Bounded blocked reports can complete
their reporting contracts without satisfying DevOps cloud-pass.

Apply exact prior references
`["yaml-loops-v1:sprint/2/RP-S2/SprintArchitectureLoop","rp-s2-architecture-close-completed-deliverable"]`,
`["yaml-loops-v1:sprint/3/RP-S3/SprintDesignLoop","rp-s3-design-close-completed-deliverable"]`
and
`["yaml-loops-v1:sprint/2/RP-S2/SprintRetroLoop","rp-s2-retro-close-agreed-deliverable"]`
only within their accepted boundaries. They supply no current RP-S3 architecture
votes, ownership acceptance or release waiver; other accepted handoffs stay
closed. Material changed contracts return to existing Architect-advised
Product Owner/Scrum reconciliation, not weakened acceptance.

Architect doneWhen is this current cumulative mapping and the three linked
tier updates committed for original Product Owner/Critic/Red Team review.
Current RP-S3 architecture votes are not yet supplied. Scrum retains
contract-first decomposition, minimal dependencies, resource coordination and
Git-reconciliation assignment. Designated integration reconciles task commits
to authorized feature branches or retains named branches with task IDs, commit
IDs and abandonment reasons in a feature-branch commit message. This design
does not assert successful deployment, runtime progress or customer readiness.

<a id="current-rp-s2-supported-repair-and-exact-remote-collaboration-october-20-2026"></a>

## Historical RP-S2: supported repair and exact remote collaboration (October 20, 2026)

Current sprint is **RP-S2**; RP-S1 is supplied as completed workflow history,
not a successful deployment. Inspected clean application HEAD
`cf017c969720eda2dce6f2cec09f4fa142cbab2d` on
`feature/customer-hosted-session-prototype`. Consume the accepted RP-S1
cumulative/tier architecture at `c888336b1741dd5cbf77f0209749620949301adb`,
retrospective at `006574e6d664ec21d38a86c8e1f1cf15e162f89e`, and RP-S2
SprintDesign at inspected HEAD. Older overlays below retain technical/audit
history; this section selects the current sprint without reopening those
accepted handoffs or claiming fresh private observations.

### Retained holistic design and current acceptance joins

Exactly three hosted roles remain: terminal -> coordinator MAF
begin/route/execute/publish -> remote architect and reviewer -> fenced
acceptance. Parent-scoped manifest lookup, restored remote `AgentSession`,
pinned role versions and both specialists' `specialist_history_v2` remain
distinct continuation links. Conversations, checkpoints, immutable artifacts
and write-ahead effects retain their separate responsibilities. Preserve
both-role two-turn/four-call/history controls and parser-safe human stderr;
no rewrite, additional service, schema, framework or duplicate implementation.

| RP-S2 obligation | Closing owner and evidence boundary |
|---|---|
| Ownership and loaded roots | Existing Developer substantiates named recovery evidence, current eight-path sibling status and matched/mismatched resolver behavior; originating Architect/Critic acceptance precedes runner writes. Supplied writer/integration designations suffice for coordination, not acceptance. |
| Reviewed finite runner | Existing Developer implements the retained interface and offline rejection/unknown/root controls after ownership acceptance. Offline coding consumes agreed fixtures, not live inventory. Preserve `LAB_TOOL_OWNER_MISMATCH`; a sibling commit is not operational installation. |
| Operational/source join | Designated Developer integrates reviewed application, runner and required wrapper bytes at actual loaded roots, records exact commits/hashes/root mapping, reruns joined checks and records scoped push outcomes. Original formal E2E validates that join. |
| Strict trust and current inventory | Original DevOps independently compares the existing accepted host fingerprint via retained tooling, validates sole-target context and observes current three-role versions/packages/identities, rollback and held effects. ARM readiness and another task's historical receipt inspection do not establish this gate. |
| Exact release and actual G1-G4 | Original DevOps runs retained application/repository/tooling and Linux/amd64/hosting-Python checks for exact source/package, fresh previews and guarded publication. Actual common bundle, remote acceptance, private managed-identity provenance and genuine Decision-1 remain separate required proofs. |

The supplied RP-S1 source-check and E2E reports attribute 204 offline passes
to their executions; E2E remains **FAIL**. Supplied DevOps reporting attributes
an exit-2 `HOST_TRUST_EVIDENCE_REQUIRED` stop after partial authenticated ARM
inventory, without transport startup or current private deployment bindings.
Its recovery-file inspection is historical evidence, not transferable ownership
acceptance or a fresh observation here. The originating ownership report still
requires permission-capable bounded sibling/resolver/evidence reads and its
original review. Use the already-sufficient designations; do not request them
again, reset stopped history or treat session-specific access as blanket denial.

### Identity decision and effect boundary

Neither A nor B is live-selected. A requires an evidenced supported
authentication/configuration correction and matching reviewed source. Retained
specialist-only B is candidate code, not proof of delegated ingress. The finite
runner rejects source/root/scenario/package/actual-version mismatches before
parent creation. Preparation rejection is not receiver failure and supplies no
invented zero-send counts. Verify architect trusted ingress and receiver
principal equality before reviewer dispatch; reviewer needs independent evidence.
An unknown effect is held and observed, never automatically resent or retried
under the other identity path. No call-ID-as-user substitution, receiver-equality
relaxation, held-parent adoption or model-history rekey is allowed.

Necessary chosen-path lab permissions remain pre-approved only at documented
exact scope/rationale through retained scripts and readback; speculative grants
are not a remedy. Identity selection alone cannot pass G1-G4. A bounded
prerequisite-stop or actionable unresolved report may complete its reporting
contract while DevOps cloud-pass and customer readiness remain unmet.

### Handoff, cumulative obligations and disposition boundaries

Scrum retains task decomposition, minimal dependencies, shared-resource
serialization and Git-reconciliation assignment; no tasks are dispatched here.
Developer integration must reconcile task commits to authorized feature
branches or retain named branches with task/commit IDs and abandonment reason
in a feature-branch commit message. Preserve unrelated dirty/staged canonical
work; no branch switching, broad staging or root-guard bypass.
Original E2E and DevOps execute deterministic local scripts, not GitHub Actions.
Actual publication/profile/transport/mount/stage mutation remains serialized.

RP-S3 consumes actual G1-G4 and a completed non-held initial parent for live
two-turn continuity, once-only confirmed supported compute stop/resume with
checkpoint/effect preservation, separate-parent isolation and truthful delivery.
It does not consume an agreed failure report as a successful initial turn.
Preserve every AC1-AC9/G1-G8, historical UNKNOWN, held parent, rollback asset
and historical cleanup uncertainty. Account-wide Blob Contributor isolation
remains application-enforced, not storage-RBAC or malicious-host isolation.

The current RP-S2 sections in the linked
[coordinator](requirements/coordinator/architecture.md),
[specialists](requirements/specialists/architecture.md) and
[client/release](requirements/client-release/architecture.md) carry this join.
Apply exact prior references
`["yaml-loops-v1:sprint/1/RP-S1/SprintArchitectureLoop","sprint-architecture-close-completed-deliverable"]`
and
`["yaml-loops-v1:sprint/2/RP-S2/SprintDesignLoop","rp-s2-design-close-completed-deliverable"]`
only to their accepted RP-S1 architecture and RP-S2 design respectively.
Upstream Architecture/UX/ReleasePlan, RP-S1 source/E2E/review/retro closure
dispositions likewise remain bounded; no votes transfer to this architecture
or originating ownership acceptance. Architect agrees with this committed
design for original Product Owner/Critic/Red Team review; current votes and
checks are reported separately. No private inspection, live identity decision,
cloud operation, deployment or substantive runtime progress is claimed here.

<a id="current-rp-s1-accepted-inputs-and-evidence-ready-continuity-october-20-2026"></a>

## Historical RP-S1: accepted inputs and evidence-ready continuity (October 20, 2026)

The supplied sprint is **RP-S1: evidence-ready source and understandable
continuity**; no assignments, completed sprints or additional blocked-decision
list were supplied. Inspected clean application HEAD
`00b228bb78842df3289008be3c99ad6a88d3efe4` on
`feature/customer-hosted-session-prototype`. Consume accepted Architecture
`45318a50098c44843643ef1a7c5479edb4dfbd38`, UserExperience
`b7aa978584b144c1cb485bec5b54e9c8da989964`, ReleasePlan
`2f22642e6f68d841c7ef40097fe1299ccd366dd8` and SprintDesign at that HEAD.
Older RP-S1/RP-S2/RP-S3 overlays retain technical and audit history, not the
current sprint selection, fresh observations or task dispatch.

### Retained design and RP-S1 criterion map

Exactly three hosted roles use the existing pinned Python, MAF/Foundry,
Pydantic, private managed-identity Blob and PowerShell/Python/WSL tools.
Terminal -> coordinator begin/route/execute/publish -> remote architect and
reviewer -> deterministic, fenced acceptance remains the end-to-end flow.
Parent-owned manifest lookup creates or reuses each role's hosted/framework
binding and pinned version; remote `AgentSession` restoration and each
specialist's `specialist_history_v2` load are distinct continuation links.
Conversations retain history, checkpoints retain graph position, immutable
artifacts retain exact work and the write-ahead effect journal reconciles
sends. Responses and revisions advance without replacing session identities.

| RP-S1 criterion | Existing implementation/fixture boundary and handoff |
|---|---|
| Both-role two-turn proof | Retain parent and both specialists' hosted/framework identities and pins, exactly two child creations, both roles on both turns, fresh invocation responses, updated requirements and stale-approval invalidation. Compare identity fields, not entire serialized continuations. |
| Repeated orchestration and model history | Retain ordered architect -> blocked reviewer -> same architect -> same reviewer fixtures and both roles' actual load/model/store paths, persisted-value snapshots and identical-brief fresh-history controls. Replayed requirements are not model-history proof; fixtures remain offline. |
| Understandable continuity with unchanged parsing | Consume accepted README and SprintDesign Screens A-D, useful opt-in human stderr, safe aliases and unchanged machine stdout/parser. Aliases cannot establish actual binding equality. Required application/repository checks remain downstream source gates. |
| Supported decision or actionable unresolved handoff | Retained specialist-only B is candidate-only, not live selection. A needs an evidenced supported authentication/configuration correction and reviewed source. Report preparation versus receiver boundary, reached/unreached roles, missing evidence/remedy, existing closing owner and exact next action; do not invent live success. |

Trusted parent/receiver equality, exact immutable prerequisites, producer/
version/revision/hash checks, coordinator ETag/fencing, calibrated Decision-1
after deterministic gates and unknown-effect holds remain mandatory. No new
service, framework, schema, public event, session manager, UI, runtime selector
or duplicate fixture/presentation implementation is introduced.

### Blocked decisions and minimal execution joins

The accepted Architecture records successful direct sibling Git inspection,
but incomplete resolver/loaded-root verification after denied reads. This is
attributed upstream evidence, not a fresh sibling observation here; older
blanket claims that all Git inspection was denied are not current status.
Supplied Developer writer/integration designations resolve coordination only.
Use them with the supplied recovery evidence in the existing ownership task,
not as ownership acceptance or a renewed request for user designation.

```text
supplied coordination + current owned-path/resolver verification
  -> originating ownership review -> eight-path sibling runner work
accepted application + reviewed runner + required actual operational bytes
  -> designated Developer integration -> original E2E joined-source validation
established strict trust + verified sole-target context -> current inventory
joined source + inventory + exact Linux/package/version gates
  -> original DevOps guarded publication and finite decision -> live G1-G8
```

The existing Developer closes bounded resolver/loaded-root and owned-path
verification before originating review and runner writes. Keep the exact
eight-path allowlist and registered feature sibling boundary from accepted
Architecture; never write the dirty canonical lab. Preserve
`LAB_TOOL_OWNER_MISMATCH`: sibling commits do not install canonical wrappers.
Integration must join reviewed source to actual loaded roots/hashes, preserve
unrelated dirty/staged work and record task/branch/commit accounting and scoped
push. A necessary root/guard contract change returns to existing
Architect-advised Product Owner/Scrum reconciliation, not a guard bypass.

Ownership does not gate independent application checks; private inventory is
not a runner coding prerequisite. DevOps independently closes established
strict host trust and current sole-target inventory. Another role's receipt
reads, current known-host content or historical metadata cannot supply those
observations. Source/root/scenario/package/version rejection precedes parent
creation and is preparation, not observed receiver failure. Observe architect
trusted ingress/equality before reviewer dispatch; reviewer needs its own
evidence. Necessary chosen-path lab permissions remain pre-approved at exact
documented scope/rationale through retained scripts/readback, not speculative
grants. No call-ID-as-user conversion, equality relaxation, automatic fallback,
held-parent adoption or uncertain resend is permitted.

Scrum retains contract-first decomposition, minimal dependencies, integration
assignment and actual shared-resource coordination. Original E2E owns formal
integration; original DevOps owns exact-source Linux/amd64/hosting-Python
checks, guarded publication and cloud-pass through deterministic local scripts,
not GitHub Actions. Serialize publisher/profile/transport/mount/stage mutation
across runs; scheduler labels alone are not OS exclusion.

### Tier outputs, dispositions and completion boundary

The current RP-S1 sections in [coordinator](requirements/coordinator/architecture.md),
[specialists](requirements/specialists/architecture.md) and
[client/release](requirements/client-release/architecture.md) consume this map.
RP-S2 still requires actual common-bundle G1-G4 and a completed non-held initial
parent. RP-S3 retains live both-role two-turn continuity, once-only confirmed
supported compute stop/resume with checkpoints/effects and no duplicate sends,
distinct-parent child/artifact isolation and truthful exact-source delivery.
Account-wide Blob Contributor provides application-enforced isolation, not
storage-RBAC or malicious-host isolation.

Apply these exact supplied prior references only within their originating
accepted deliverables:
`["yaml-loops-v1:ArchitectureLoop","architecture-close-completed-deliverable"]`,
`["yaml-loops-v1:UserExperienceLoop","ux-close-completed-deliverable"]`,
`["yaml-loops-v1:ReleasePlanLoop","release-plan-close-completed-deliverable"]`,
`["yaml-loops-v1:sprint/1/RP-S1/SprintDesignLoop","sprint-design-close-completed-deliverable"]`.
None supplies this SprintArchitecture's Product Owner/Critic/Red Team votes,
originating ownership acceptance or live readiness. No upstream handoff is
reopened. Architect agrees with this cumulative/tier handoff for original
review; checks and current reviewer outcomes are reported separately.
No private receipt/resolver reinspection, lab change, identity selection,
deployment or cloud observation occurs here. Preserve all AC1-AC9/G1-G8,
UNKNOWN effects, held parents, rollback assets and historical cleanup uncertainty.

### Verification for this RP-S1 overlay

Existing absolute lab Python 3.12.10 ran `Test-Demo.ps1` with the explicit lab
root: dependency checking, **204 offline tests in 42.159 seconds**, compilation
and script exit 0. `scripts/Test-Repository.ps1` passed index,
**79-public-file** boundary, JSON/PowerShell/context and whitespace checks.
No dependency installation, retained lab source change, Linux hosting-package
check, formal E2E, cloud operation or push occurred. These repeated checks are
not new runtime progress or live acceptance evidence.

<a id="current-rp-s2-joined-execution-inputs-and-independent-trust-october-20-2026"></a>

## Historical RP-S2: joined execution inputs and independent trust (October 20, 2026)

This RP-S2 overlay consumes the supplied RP-S1 outcomes, retrospective
Architecture/UX/ReleasePlan updates at `a98410f479104a549fe6933df6eea3d4c6e6d132`
and accepted current SprintDesign at inspected clean application HEAD
`d558a721747ddea92a445b8bc45c786ba5c84664` on
`feature/customer-hosted-session-prototype`. Earlier overlays below are retained
technical and audit history, not fresh status or dispatch. RP-S1 reporting
closure is not RP-S2 execution acceptance.

### Architecture decisions carried forward, not reopened

Retain exactly three hosted roles: terminal -> coordinator's explicit MAF
begin/route/execute/publish flow -> remote architect/reviewer -> fenced acceptance.
The parent manifest creates or reuses each role's hosted/framework session and
pinned version; remote `AgentSession` restoration and each specialist's
`specialist_history_v2` load independently preserve continuation. Responses and
requirements/candidate/review revisions advance, bindings do not. Conversations,
checkpoints and immutable artifacts/write-ahead effects remain distinct.
Retain exact prerequisites, stale-approval invalidation, trusted receiver
principal equality, private managed-identity Blob and genuine Decision-1 after
deterministic gates. No new session abstraction, service, dependency, schema,
public event, UI or identity selector is required.

The retained application candidate is specialist-only B, not selected-B.
A requires an evidenced supported authentication/configuration correction and
its own reviewed source; relabeling the B package cannot select A. The finite
runner must reject source/root/scenario/package/actual-version mismatch before
parent creation. Local preparation rejection is not receiver failure.
Architect trusted ingress/receiver success precedes reviewer dispatch; each
role needs its own evidence. Neither ingress nor identity selection alone
proves accepted artifacts, private MI provenance or complete common-bundle G1-G4.
Necessary chosen-path lab permissions remain pre-approved at exact evidenced
scope/rationale using retained deterministic scripts and readback, not speculative
grants. No opaque call-ID conversion, equality relaxation, automatic fallback,
held-parent adoption or uncertain-effect replay is allowed.

### Two independent preparation lanes and the source-to-live join

```text
supplied designations + exact recovery evidence + current sibling/root proof
  -> original ownership acceptance -> reviewed eight-path runner work
accepted application + reviewed runner + required loaded operational wrappers
  -> designated Developer integration -> original E2E exact joined-input checks
previously accepted fingerprint/reference + verified sole-target context
  -> retained strict-trust checks -> authenticated private inventory
reviewed joined inputs + current inventory + final Linux/package/version gates
  -> original DevOps guarded publication and finite ingress decision
  -> actual common-bundle G1-G4 -> non-held initial-parent handoff to RP-S3
```

| Existing boundary | Supplied outcome, missing proof and closing action |
|---|---|
| Ownership before runner writes | Supplied Developer writer/integration designations resolve coordination only. Originating exact-file/sibling inspections were denied; registration is not current safe-writing proof. Developer resumes already-authorized bounded reads in a permission-capable session, substantiates branch/base/status, eight owned paths and loaded resolver behavior, then returns to original Architect/Critic review. No write probe, checkout recreation or repeated designation request. |
| Strict trust before private inventory | DevOps reports ARM/context/model readiness and exit 1 at `HOST_TRUST_EVIDENCE_REQUIRED`. These do not establish SSH/private ingress or current deployed/rollback/held-effect inventory. DevOps recovers the previously accepted ED25519 comparison value and acceptance reference from an exact private locator, then runs retained strict-trust/read-only inventory scripts. Current known-host content is not independent acceptance; do not replace trust. |
| Reviewed source at actual loaded roots | Developer integrates reviewed task commits and every required operational-wrapper delta against exact loaded paths/hashes, preserves unrelated work and records task/branch/commit accounting and scoped push. Sibling wrapper commits are not canonical installation. Preserve `LAB_TOOL_OWNER_MISMATCH`; the dirty canonical lab remains unwritable. An alternative operational root is not selected without all existing settings/profile/registry/stage/source guards passing; a necessary guard/location contract change returns to existing Architect-advised PO/Scrum reconciliation. |
| Joined validation and guarded execution | Original E2E validates the exact reviewed joined inputs when available. Original DevOps joins current inventory and held-effect reconciliation to exact-source Linux/amd64/hosting-Python, common-package/version checks, guarded publication and actual G1-G4. Only a completed non-held compatible initial parent can enter RP-S3 continuity/recovery. |

These are existing contracts and closing owners, not new tasks or approval
stages. Ownership does not gate independent application checks; inventory is
not a runner coding prerequisite. Another role's successful historical receipt
inspection does not supply originating ownership acceptance. Historical hashes,
offline checks and reported ARM observations remain attributed, not freshly
authenticated by this architecture turn. Private evidence stays outside Git.

Scrum retains contract-first assignment, minimal dependencies, Git reconciliation
and actual shared-resource coordination. Original DevOps serializes publisher,
CLI profile, private transport, mount and package-stage mutations across runs;
scheduler labels do not provide OS/cross-run exclusion. E2E and DevOps execute
through retained local scripts with explicit roots, never GitHub Actions.

### Cumulative tier handoff and completion boundary

| Tier | Current RP-S2 handoff |
|---|---|
| [Coordinator](requirements/coordinator/architecture.md#current-rp-s2-joined-execution-boundary) | Retain accepted two-turn/four-call fixtures, both-role bindings and pinned versions, exactly two children, fresh responses, current prerequisites and stale-approval invalidation. Integrate exact reviewed source; preparation success does not prove remote acceptance. |
| [Specialists](requirements/specialists/architecture.md#current-rp-s2-trusted-ingress-boundary) | Retain both real five-stage history paths, persisted-value/fresh-history controls and known-response zero-send recovery. Observe trusted ingress, receiver equality and private immutable output provenance separately for both roles. |
| [Client/release](requirements/client-release/architecture.md#current-rp-s2-trust-and-release-join) | Retain accepted README, Screens F/G, useful opt-in human stderr, safe aliases and unchanged stdout/parser. Report completed bounded assessments separately from unmet execution gates, then hand actual final/rollback bindings and non-held initial scope to RP-S3. |

Apply `["yaml-loops-v1:sprint/1/RP-S1/SprintArchitectureLoop","sprint-architecture-close-agreed-deliverable"]`
only to the accepted RP-S1 architecture; no duplicate implementation or renewed
RP-S1 review is requested. Apply
`["yaml-loops-v1:sprint/2/RP-S2/SprintDesignLoop","rp-s2-sprint-design-close-agreed-deliverable"]`
only to current design acceptance. The retrospective closure under
`["yaml-loops-v1:sprint/1/RP-S1/SprintRetroLoop","sprint-retro-close-agreed-deliverable"]`
supplies the evidence-attribution lesson, not runtime success.
The accepted E2E failure report remains closed under
`["yaml-loops-v1:sprint/1/RP-S1/EndToEndTestLoop","e2e-close-agreed-failure-report"]`;
future joined-input validation is still required. Preserve originating ownership
reference
`["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-LAB-OWNERSHIP/AssignedWorkDeveloperLoop","lab-ownership-review-evidence-access"]`
and its runner-write prohibition until its own evidence/review gates pass.

RP-S2 execution exit still requires actual G1-G4 on one final common bundle.
RP-S3 retains both-role two-turn continuity, once-only confirmed supported
compute stop/resume with checkpoints/effects and no duplicate sends, distinct
parent/child/artifact isolation and truthful customer delivery. Keep all
AC1-AC9/G1-G8, historical UNKNOWNs, held parents, rollback assets, unrelated work
and historical cleanup uncertainty. Account-wide Blob Contributor remains
application-enforced isolation, not storage-RBAC or malicious-host isolation.
Architect accepts this current cumulative/tier deliverable for original Product
Owner, Critic and Red Team review; RP-S1/upstream votes do not supply RP-S2 votes.
This overlay neither accepts ownership nor selects a remedy, deploys, or
certifies customer readiness.

## Current RP-S1 ownership-designation architecture (October 20, 2026)

This SprintArchitecture consumes agreed Architecture
`f72b0f3c1206418f08fc62a149e80f7c12c55e81`, UserExperience
`87253d3f5003d1d6f34724401b33c3b5ced2e64a`, ReleasePlan
`f9ccb6e85c80ce14f36e44cfb6e690fde0d81e80` and SprintDesign
`3103c14781b4509b2bd73ff1ba763cece0f1adf0`, the inspected clean application
baseline on `feature/customer-hosted-session-prototype`. No completed sprint,
assignments or separate blocked-decision list was supplied for this invocation.
Retain the cumulative RP-S1/RP-S2/RP-S3 technical contracts below; their dated
status and measurements are not current execution evidence.

### Resolved coordination input, unchanged technical contracts

Use the user's supplied Developer writer/integration designations and writer
acknowledgements as explicit coordination evidence with recoveryExceptionV1
for the original ownership review. Missing designation is no longer a human
input blocker. This does not establish accepted ownership, current sibling
exclusivity, transport trust, installed operational source or live readiness.
The exact originating boundary remains
`["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-LAB-OWNERSHIP/AssignedWorkDeveloperLoop","lab-ownership-review-evidence-access"]`.
Do not reset its stop or infer permission to write from this design.

Developer for `RP-S2-DECISION-RUNNER` owns only the eight lab paths listed in
[accepted release architecture](customer-prototype-architecture.md#current-ownership-designation-architecture-october-20-2026),
in the registered feature sibling only, never the dirty canonical lab.
Developer for `RP-S2-SOURCE-INTEGRATE` owns reviewed application/lab integration,
durable task/branch/commit accounting and scoped push. Preserve unrelated
dirty/staged work, explicit path ownership and `git commit --only`; no shared
branch switch, write probe, force-push or registration-as-ownership inference.
Scrum retains contract-first decomposition, minimal dependencies, actual shared
resource coordination and assignment of Git reconciliation; this is no dispatch.

Keep exactly three hosted roles and the explicit MAF begin/route/execute/publish
flow. The parent manifest's create-or-reuse lookup retains both specialists'
hosted/framework identities and pinned versions; remote `AgentSession`
restoration and each role's model-history load provide distinct continuation
links. New responses and current revisions advance without replacing children.
Conversations, checkpoints, immutable artifacts and fenced write-ahead effects
remain distinct. Retain exact prerequisites, stale-approval invalidation,
trusted principal equality, private managed-identity Blob, Decision-1 after
deterministic gates and UNKNOWN holds. No runtime/schema/dependency change,
generic session manager, extra service or identity selector is introduced.

### Cross-tier handoff and minimal execution joins

| Tier | RP-S1 retained contract and current coordination delta |
|---|---|
| [Coordinator](requirements/coordinator/architecture.md#current-rp-s1-ownership-designation-boundary) | Retain both-role two-turn/four-call binding, version, creation-count, fresh-response and current-artifact fixtures. Ownership acceptance gates runner writes; source/root/scenario/package/version rejection is preparation, not receiver evidence. |
| [Specialists](requirements/specialists/architecture.md#current-rp-s1-ownership-designation-boundary) | Retain both real five-stage history paths, value snapshots, identical-brief fresh-history negatives and exact-response zero-send recovery. Supplied designations do not establish ingress, receiver equality or live history for either role. |
| [Client/release](requirements/client-release/architecture.md#current-rp-s1-ownership-designation-boundary) | Retain accepted README, useful opt-in human stderr, safe aliases and unchanged stdout/parser. Separate coordination, original ownership acceptance, matched source, current trust/inventory and actual live evidence. |

```text
supplied designation + recovery evidence + current path verification
  -> original ownership acceptance -> bounded runner work
accepted application + reviewed runner + required operational source
  -> designated Developer integration -> original E2E scripted validation
existing strict trust + verified sole-target context -> fresh inventory
joined source + inventory + exact Linux/package gates
  -> original DevOps guarded publication/discriminator -> actual live gates
```

Ownership does not gate independent application checks; inventory is not a
coding prerequisite. Use the supplied recovery locator first when original
owners need evidence. Bounded read-only Git/sibling resolver inspection is
already authorized; any unavailable current observation needs its exact
existing-owner closing action, not another designation request. Architecture's
reported denied sibling inspection and historical receipts are consumed as
supplied observations, not independently reauthenticated here.

Preserve `LAB_TOOL_OWNER_MISMATCH` and explicit operational roots. Canonical
wrappers execute only with their canonical context and verified loaded bytes;
sibling fixes are not canonical installation. Integration must reconcile every
required operational-wrapper revision at its actual loaded path without writing
the dirty canonical lab or altering private settings. An alternative operational
root needs proof of existing settings/profile/registry/stage/source guards;
no unproven move is selected. Missing required source blocks execution. A new
writable location or changed root/guard contract returns to existing
Architect-advised PO/Scrum reconciliation, not a bypass or new approval stage.

Installed specialist-only B remains a candidate, not live selection. A requires
its own supported correction and reviewed source. The finite decision records
preparation rejection versus observed receiver failure and reached/unreached
roles; architect success does not establish reviewer entry. Necessary chosen-path
lab permissions remain pre-approved only at exact evidenced scope through
retained deterministic scripts and readback. No speculative grant, call-ID-as-user,
principal-equality relaxation, held-parent adoption or uncertain resend.
Original DevOps serializes actual publisher/profile/transport/mount mutations;
resource labels alone provide no cross-run exclusion. Local scripts, not GitHub
Actions, remain the execution mechanism.

### Sprint exit and acceptance boundaries

RP-S1 exits with retained source/fixtures/presentation, applicable source checks
and a supported decision baseline or actionable unresolved finding naming the
exact reached boundary, missing observation/remedy, closing owner and next action.
No duplicate fixture or presentation implementation is requested. RP-S2 still
requires actual common-bundle G1-G4 and a completed non-held initial parent;
RP-S3 requires actual both-role two-turn continuity, once-only confirmed supported
stop/resume without duplicates, distinct-parent isolation and truthful delivery.
Retained private-observation assertions collect/authenticate nothing by themselves.
AC1-AC9/G1-G8, rollback assets, historical UNKNOWNs, held parents and historical
cleanup uncertainty remain unchanged. Account-wide Blob Contributor means
application-enforced isolation, not malicious-host or storage-RBAC isolation.

Apply exact prior references
`["yaml-loops-v1:ArchitectureLoop","architecture-close-agreed-deliverable"]`,
`["yaml-loops-v1:UserExperienceLoop","ux-close-agreed-deliverable"]`,
`["yaml-loops-v1:ReleasePlanLoop","release-plan-close-agreed-deliverable"]` and
`["yaml-loops-v1:sprint/1/RP-S1/SprintDesignLoop","sprint-design-close-agreed-deliverable"]`
only to their originating accepted handoffs. None supplies this loop's reviewer
votes or release success. Architect agrees to this bounded cumulative/tier
handoff; current Product Owner, Critic and Red Team agreement is still required.
This documentation-only revision does not repeat private receipt/resolver
experiments, select a remedy, change lab source or execute cloud effects.
Current local checks are reported separately from historical measurements below.

### Local verification for this ownership-designation overlay

Existing absolute lab Python 3.12.10 and the explicit lab root were used:
`Test-Demo.ps1` passed dependency checking, **204 offline tests in 45.825 seconds**
and compilation. `scripts/Test-Repository.ps1` passed index,
**79-public-file** boundary, JSON/PowerShell/context and whitespace checks.
Structural validation passed **62 local links/anchors** and balanced fences
across all four architecture files. No dependencies were installed. These are
documentation/source compatibility checks, not new runtime or live progress.
No lab source changed; full retained lab and Linux hosting-package suites were
not run. No cloud operation, private receipt authentication or push occurred.

## Current RP-S1 recovery-entry architecture (October 20, 2026)

Historical recovery-entry overlay: use the ownership-designation section above
for current coordination inputs; retain the dated technical contracts below.

This is the current **RP-S1 SprintArchitecture** overlay, based on clean
application HEAD `160b38d202bd239ecd409b8f7de485b1d7f7e10e` on
`feature/customer-hosted-session-prototype`. It consumes agreed
[release architecture](customer-prototype-architecture.md) at `2f62e3c`,
[UX](customer-prototype-ux.md) at `8d6d6e0`,
[release plan](customer-prototype-release-plan.md) at `68c5bd8` and
[sprint design](customer-prototype-sprint-design.md) at `160b38d`.
No completed prior sprint or separate blocked-decision list was supplied for
this invocation. Earlier RP-S1/RP-S2/RP-S3 slices below remain cumulative
technical contracts and historical observations, not the current sprint,
new assignments, pending original reviews or fresh live evidence.

### Sprint decision and cross-tier invariants

Retain the three-role end-to-end design: terminal -> hosted MAF coordinator ->
remote architect -> remote reviewer -> fenced current-artifact acceptance.
The same parent manifest reuses both children and their pinned versions on a
revision or follow-up; `RemoteAgents.invoke()` restores their framework
`AgentSession`, and each specialist independently restores model history.
Fresh invocations advance response IDs and current outputs, not child identity.
Conversations, checkpoints and immutable artifacts/effect journals remain
distinct state planes. Keep the explicit lifecycle order, pinned dependencies,
trusted principal equality, private managed-identity Blob path, Decision-1
after deterministic gates, write-ahead effects and UNKNOWN holds.

The architecture delta is **recovery-entry interpretation and matched
operational source integration**, not a runtime rewrite or another identity
mechanism. The installed specialist-only B client remains a candidate.
A requires its own supported, evidenced authentication/configuration correction;
a scenario label cannot switch the installed B source to A. Neither is selected
live. No new service, history schema, public event, CLI flag, comparison ledger,
SessionManager, infrastructure or permission change is introduced here.

| Logical tier | Current RP-S1 boundary and retained handoff |
|---|---|
| [Coordinator](requirements/coordinator/architecture.md#current-rp-s1-recovery-entry-boundary) | Retain both-role two-turn/four-call fixtures, immutable snapshot comparisons, stale-approval invalidation and exact accepted refs. Candidate resource setup failure is preparation rejection, not a remote receiver observation. |
| [Specialists](requirements/specialists/architecture.md#current-rp-s1-recovery-entry-boundary) | Retain both real load/model/store paths, identical-brief fresh-history controls and exact-response zero-send recovery. Neither historical trust nor candidate source proves either role's trusted ingress or restored history live. |
| [Client/release](requirements/client-release/architecture.md#current-rp-s1-recovery-entry-boundary) | Retain accepted README/opt-in human stderr and unchanged machine parser. Join reviewed runner to matched operational wrappers/roots before execution; maintain separate current-trust/inventory and coding lanes. |

### Recovery evidence, source roots and actual closing actions

Consume the accepted release architecture's historical recovery-summary/receipt
locators and executed canonical/sibling resolver matrix without rerunning those
experiments. Those observations do not establish current writer exclusivity,
SSH trust, authenticated inventory, installed wrapper revisions or ingress.
The supplied recovery-exception locator is the first read-only evidence source
when original owners need that evidence; bounded Git/sibling-resolver inspection
is already authorized. Do not request new product permission for that inspection
or silently restart the historically stopped ownership task.

Preserve `LAB_TOOL_OWNER_MISMATCH`: load each retained wrapper with its own
operational lab root. A runner in a separately verified writable checkout may
invoke canonical wrappers explicitly in their canonical context. Reviewed
sibling wrapper changes are not installed canonical changes. Before effects,
integration must join runner, application and every required operational wrapper
revision/hash to the actual loaded paths. A missing required operational delta
is an integration failure, not permission to weaken the guard, copy credentials
or substitute a profile. This is the accepted composition boundary, not a new
third root abstraction.

| Existing owner | Bounded closing condition / downstream handoff |
|---|---|
| Developer / Scrum | Reconcile point-in-time writer/path ownership with supplied branch/status/resolver evidence and originating review before runner writes. Registration alone is insufficient; no write probe or shared branch switch. |
| Transport owner / DevOps | Substantiate the already approved module/source/fingerprint, verify current exact hashes and strict trust, then fresh sole-target authenticated inventory. Historical receipts are locators, not present trust or original-UNKNOWN cleanup. |
| Developer / integration | Retain accepted application fixtures, candidate, presentation and `validate_scenario_evidence()` assertions without redispatch. Complete concrete runner deltas with root/source/scenario/version, partial-role, preparation/receiver, unknown-effect and zero-send negative controls; integrate reviewed operational source. |
| Original E2E | Validate the exact joined implementation through local repository scripts. An agreed predeployment FAIL is not release readiness; architecture observations are not formal integration PASS. |
| Original DevOps | Join fresh inventory to exact-source/Linux/amd64/hosting-Python/common-package gates, retained preview/publication and finite trusted-ingress trial. Architect receiver success precedes reviewer; each reached/unreached role is recorded. Selection alone does not pass G1-G4. |

Writing ownership gates runner coding, not independent application checks.
Current trust and verified context gate inventory, not coding. Reviewed source
and fresh inventory join before release/trial. Only a demonstrated necessary
permission delta adds exact-scope scripted plan/write/readback; the user's lab
approval is retained, not speculative grant authority. Scrum owns task IDs,
minimal dependencies, actual shared-resource serialization and Git reconciliation
in existing planning/execution stages. Keep publication/profile/transport/mount
mutation serialized; scheduler resource names alone give no cross-run isolation.
No assignments or additional approval stage are created by this document.

### Sprint exit, later live gates and disposition boundaries

RP-S1 hands off retained source/fixtures/presentation, applicable current checks
and a supported identity baseline **or actionable unresolved finding**. Preserve
the historical `NATIVE_HOST_PRINCIPAL` result as history, not a fresh diagnosis.
The unresolved decision closes with the exact reached boundary, missing
observation/supported remedy, existing closing owner and next action. A material
principal-namespace or held-state finding goes to existing Architect-advised
PO/Scrum reconciliation, not equality relaxation or invented human approval.
Only genuinely unavailable human/provider information merits needs-input.
Continue the remaining artifacts while selection is unresolved.

RP-S2 still requires actual final common-bundle G1-G4 and a completed non-held
initial parent. RP-S3 still requires both-role two-turn exact continuity,
once-only confirmed supported stop/resume without duplicate effects, independent
separate-parent isolation and truthful exact-source delivery. Retained
`live_acceptance.validate_scenario_evidence()` asserts supplied observations;
it neither collects/authenticates them nor proves live acceptance by itself.
No alias, brief replay, HTTP 200, model memory text or agreed blocked assessment
substitutes for these gates. Account-wide Blob Contributor gives application-
enforced ownership/isolation, not storage-RBAC or malicious-host isolation.
Preserve historical UNKNOWN effects, held parents, rollback assets, unrelated
work and historical cleanup uncertainty.

Apply exactly
`["yaml-loops-v1:ArchitectureLoop","architecture-close-agreed-deliverable"]`,
`["yaml-loops-v1:UserExperienceLoop","ux-close-agreed-deliverable"]`,
`["yaml-loops-v1:ReleasePlanLoop","release-plan-close-agreed-deliverable"]` and
`["yaml-loops-v1:sprint/1/RP-S1/SprintDesignLoop","sprint-design-close-agreed-deliverable"]`
only within their originating acceptance. They preserve accepted handoffs,
not this loop's reviewer votes or release success. The stopped historical
ownership reference remains
`["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-LAB-OWNERSHIP/AssignedWorkDeveloperLoop","lab-ownership-review-evidence-access"]`;
new locatable evidence does not retrospectively accept it or reset its stop.
Architect accepts this bounded design; current Product Owner, Critic and
Red Team agreement remains required for this SprintArchitectureLoop.

### Checks for this recovery-entry overlay

Using the existing absolute canonical-lab Python 3.12.10 executable and
explicit lab root, `Test-Demo.ps1` passed dependency checking, **204 offline
tests in 46.940 seconds**, and compilation. No dependencies were installed.
After index refresh, `scripts/Test-Repository.ps1` passed index,
**78-public-file** boundary, JSON/PowerShell/context and whitespace checks.
Structural checks passed **55 relative links/anchors**, balanced fences in
all four architecture files and current RP-S1 source/root/exit/review boundaries.
These repeated checks validate source/document compatibility, not new runtime
capability or reviewer-verified experimental progress.

Only cumulative architecture, three tier files and navigation changed.
No lab source, runtime, dependency, assignment or machine contract changed;
retained lab release and Linux hosting-package suites were not run.
No private receipt inspection, resolver experiment, authenticated inventory,
cloud operation, identity trial, deployment, stop/resume or push occurred.
Historical measurements below remain historical.

## RP-S3 current sprint: continuity, recovery and isolation evidence joins

This slice retains the accepted RP-S2 architecture at
`8fc296f65589af88706396ecf50e27b0f75deaef`, application preparation at
`990467afd3e03efdf55aa236ee56ecc1bd04de66` and retrospective at
`585601f4ad3e8d87c029a6fdca2d0326a403e142`. The inspected clean baseline is
`7f7376b85e7b5f4e216dd382480cf6678d07eadf` on
`feature/customer-hosted-session-prototype`, containing the accepted
[RP-S3 screens H-K](customer-prototype-sprint-design.md#rp-s3-continuity-supported-recovery-and-truthful-delivery).
RP-S1/RP-S2 process completion is not delivery of their unmet live gates.
Earlier sections below are retained historical slices, not current pending
reviews or claims that no prior sprint has completed.

Exactly three hosted roles, explicit MAF execution order, existing dependency
pins, trusted parent binding and specialist-only B client isolation remain.
No session manager, history migration, fourth service, runtime selector, new
public event/schema, CLI option or comparison ledger is introduced.
The following joins refine existing AC1-AC9/G1-G8, not their requirements.

### Entry handoff and blocked execution

RP-S3 live continuation consumes an actual completed, non-held initial parent
with G1-G4 evidence: final common bundle and exact three-role versions, remote
accepted artifacts, private managed-identity Blob provenance and genuine
Decision-1/deterministic acceptance. Neither identity selection nor an
`ACCEPTED_ADVISORY` string alone establishes this handoff. Preserve its private
source/package/version and parent/child bindings; the queue follow-up uses that
same conversation, not another fresh parent manufactured for the report.

The supplied RP-S2 outcomes do not establish this entry handoff or either
successfully selected live identity path. Architecture can complete while those
effects remain blocked. Keep independent ownership/root and established-trust
lanes, reviewed runner/source integration, formal joined-source E2E and original
DevOps exact-package/publication/finite-trial execution from the RP-S2 joins.
Existing Developer/Scrum coordination delivers bounded existing setup evidence;
existing transport-owner coordination delivers the private accepted fingerprint,
approved module path and module/source SHA256 receipt locator. Failed evidence
lookup is not evidence absence. Do not restart stopped probes, derive replacement
trust, bypass blocked runner writing or repeat missing-trust checks as progress.

### Stable identity, advancing work and independent state

| Concern | Required comparison / owner boundary |
|---|---|
| Parent conversation | Actual hosted ID, framework identity and pinned coordinator version stay stable across initial, queue follow-up and supported continuation; retain the same private terminal session file |
| Both specialist children | Compare each role's actual hosted ID, framework identity, pinned name/version and parent scope in independent before/after snapshots; two total child creations for the initial/follow-up pair |
| New invocation | Both roles run on both user turns; each new call has a fresh response ID and current exact prerequisites; known-response retrieval is not another invocation |
| Requirements and acceptance | Follow-up preserves private ingress and adds the queue; prior approval is invalidated before new work; exact current candidate/review hashes, producers, revisions and fenced acceptance match |
| Specialist model history | Each real role restores its own model session/history; retained direct continuation and identical-brief fresh-history controls prove the offline boundary, not live capability from repeated brief text |
| Graph and effects | MAF checkpoints retain executor position; immutable artifacts, manifest ETag/fencing and write-ahead journals reconcile effects independently of conversation/history |

Do not compare complete serialized sessions as constant: framework service
continuation advances. Keep the retained four-call reject/revise/review fixture
as offline AC3 evidence; live two-turn AC1/AC2 remains separate. No fake/local
specialist or alias/memory-text comparison can fill a missing live observation.

### Supported recovery and separate-parent isolation

[`live_acceptance.py`](../live_acceptance.py) retains the native `restart`
scenario and `stop_hosting_for_acceptance()`: completed bound non-pending parent,
exact parent/version readback, exclusive durable `.hosting-restart.json` intent,
one supported stop request, then confirmed `idle` with a new finite positive
`stopped_at`. Existing `stop_pending` is observed without resending; another
phase rejects a repeated stop. HTTP 204, terminal restart or disconnect alone
does not satisfy G6. Missing confirmation stays unresolved, not permission to
delete the marker or issue another stop.

Original DevOps continues the same parent after confirmation and compares both
children, pinned versions, checkpoint/effect reconciliation and actual sends.
Verify no duplicate effects from journal/response/artifact evidence; do not infer
that from a resumed process or matching output text. Known responses are retrieved
exactly without send. Uncertain creation/send, binding drift and held effects
stop further effects; retain private evidence and the existing repair owner.
This tests supported compute deprovision/rehydration, not hard-crash recovery or
exactly-once platform/deployment effects.

A separate synthetic parent uses a distinct private session file, distinct
actual parent and both child bindings, separate artifact scope and an independent
brief excluding the first conversation's requirements. Verify content exclusion
and retained cross-scope rejection regressions as separate observations.
Different filenames, aliases or version numbers alone prove no isolation.
Account-wide Blob Contributor permits application-enforced role/parent checks,
not storage-RBAC or malicious-host isolation. Isolation and recovery have no
invented dependency on each other; Scrum assigns only their real shared resources.

### Exact-source evidence and delivery handoff

The retained acceptance utility emits per-scenario evidence and checks bindings,
versions and artifact envelopes; that output is not by itself the complete
cross-turn, creation-count, no-duplicate or separate-parent comparison.
Existing Developer/integration work must join actual snapshots and assertions
through deterministic local repository scripts and repair only concrete missing
checks. Original E2E validates joined implementation; original DevOps runs
hosting checks, release and live scenarios. No unimplemented comparison command
is promised here and no GitHub Actions execution is substituted.

| Gate / handoff | Closing evidence, without weakening preceding gates |
|---|---|
| G5 / AC2 | Initial and queue follow-up exact binding/creation/response/current-output comparisons for both roles, with stale approval invalidation |
| G6 / AC4 | Once-only durable stop intent and confirmed stop state joined to same-conversation continuation and no-duplicate-effect assertions |
| G7 / AC4 | Separate-parent bindings/scope, excluded first-parent content and passing cross-scope regressions |
| AC6 | Existing README commands and useful opt-in human stderr output; unchanged stdout/parser; sanitized comparison outcomes supplied separately from private exact proof |
| AC7-AC8 | Final exact-source application/repository and affected retained checks, actual Linux/amd64/hosting-Python package validation, reviewed feature-branch integration and scoped push outcomes |
| G8 / AC9 | Dated per-criterion evidence attribution, actual final/rollback bindings privately, generic setup and reproducible implemented demonstration command, owned cleanup and explicit limitations |

Keep Screens H-K illustrative reporting guidance. Existing aliases cannot
become VERIFIED continuity badges or new machine fields. Exact private bindings,
transcripts, hashes and evidence locators stay out of shareable source/output.
Original DevOps records positively identified newly owned processes, listeners
and mounts and their cleanup; new cleanup never certifies historical cleanup.
Preserve all historical UNKNOWN publications, held parents, rollback assets and
unrelated work. Report each AC/G gate verified, failed or unreached from actual
evidence, distinguishing local/mocked, Linux/package and hosted observations.
Customer-ready requires every mandatory gate; otherwise give the precise last
boundary, missing criterion, existing owner and supported closing action.

Applicable exact prior references remain bounded:

- `["yaml-loops-v1:sprint/2/RP-S2/SprintArchitectureLoop","rp-s2-sprint-architecture-close-agreed-deliverable"]`:
  retained RP-S2 architecture is closed, not current RP-S3 approval.
- `["yaml-loops-v1:sprint/3/RP-S3/SprintDesignLoop","rp-s3-sprint-design-close-agreed-deliverable"]`:
  accepted reporting screens remain closed without duplicate UI implementation.
- `["yaml-loops-v1:sprint/2/RP-S2/SprintRetroLoop","rp-s2-sprint-retro-close-agreed-deliverable"]`:
  retain independent evidence lanes and existing-owner closing actions.
- `["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-LAB-OWNERSHIP/AssignedWorkDeveloperLoop","lab-ownership-review-evidence-access"]`:
  remains unresolved with taskComplete=false, originating five-round stop and
  runner-writing block until substantiated and accepted by original reviewers.
- `["yaml-loops-v1:sprint/2/RP-S2/EndToEndTestLoop","rp-s2-e2e-close-agreed-failure-assessment"]`:
  closed prerequisite FAIL is neither joined-source PASS nor publication readiness.
- `["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-ISOLATED-CLIENT/AssignedWorkDeveloperLoop","isolated-client-close-agreed-handoff"]`:
  retain accepted candidate without renewed review or inferred live compatibility.

Scrum Master retains contract-first decomposition, minimal dependencies, exclusive
publication/transport/CLI ownership and Git reconciliation; architecture does not
dispatch new competing assignments. Material identity namespace, held-state or
source-contract changes return to existing Architect-advised Product Owner/Scrum
reconciliation, never equality relaxation or a release waiver.

## RP-S2 current sprint: evidence joins without a runtime rewrite

This cumulative `SprintArchitecture` carries forward accepted RP-S1 architecture
`4b3d0a4ecfda090f4721008de7c301e3fdf34cbc` and the retrospective
`b43f5569b97c37427cf7f1b47d103846dd350dca`. The RP-S1 sections below retain
their historical scope and observations; their earlier pending-review and
no-completed-sprint statements do not describe this RP-S2 handoff.
The current [RP-S2 design](customer-prototype-sprint-design.md#rp-s2-gated-identity-trial-and-truthful-collaboration-handoff)
is accepted at `9dfb73d5477994128b3d3136eee1a4bf9441314d`, the clean
application baseline inspected for this revision on the authorized feature
branch. RP-S1 process completion is not successful product delivery.

The technical design remains exactly three remote hosted roles, parent-scoped
children with pinned versions, restored framework sessions and specialist model
history. Immutable prerequisites/outputs, trusted receiver equality, coordinator
ETag/fencing, checkpoints, write-ahead effects and explicit unknown holds remain
unchanged. No new runtime selector, public field, CLI, history schema or service
is introduced. The tier contracts below carry the current sprint joins.

### Accepted work and unresolved prerequisite lanes

Apply the following exact prior references within their originating boundaries:

- `["yaml-loops-v1:sprint/1/RP-S1/SprintArchitectureLoop","sprint-architecture-close-agreed-deliverable"]`:
  retain accepted RP-S1 architecture; its votes are not RP-S2 approval.
- `["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-ISOLATED-CLIENT/AssignedWorkDeveloperLoop","isolated-client-close-agreed-handoff"]`:
  candidate `3aca5dc236695c5ec7eac98d0cd03bced40da7b8` and original
  both-role resource-factory review are accepted; do not duplicate them.
- `["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-LAB-OWNERSHIP/AssignedWorkDeveloperLoop","lab-ownership-review-evidence-access"]`:
  ownership/root setup remains incomplete despite agreement with its blocked
  report. Preserve the five-round stop and runner-writing block. Existing
  Developer/Scrum coordination supplies registration, branch/HEAD/status,
  canonical-work preservation, point-in-time writing ownership and positive/
  negative resolver evidence for permitted original-reviewer inspection.
  Do not restart unattended denied probes or recreate the checkout here.
- `["yaml-loops-v1:sprint/1/RP-S1/EndToEndTestLoop","e2e-close-agreed-failure-assessment"]`:
  retain the closed predeployment FAIL assessment, not integration PASS.
- `["yaml-loops-v1:sprint/1/RP-S1/SprintRetroLoop","sprint-retro-close-agreed-deliverable"]`
  and `["yaml-loops-v1:sprint/2/RP-S2/SprintDesignLoop","rp-s2-sprint-design-close-agreed-deliverable"]`:
  retain accepted evidence-boundary guidance and screens without duplicate work.

The independent transport lane needs the **existing independently accepted**
private fingerprint/transport-owner receipt locator before strict-trust
Metadata inventory. The supplied DevOps report stopped at
`HOST_TRUST_EVIDENCE_REQUIRED`; no invocation receipt was independently inspected
here. ARM readiness is not authenticated SSH readiness, and neither establishes
hosted version inventory or specialist ingress. Do not derive trust from a newly
observed key, retrieve key material or put private locators in shareable output.
Missing evidence delivery is not a newly established provider defect.

### Preparation, execution and acceptance joins

| Boundary / existing owner | Required handoff | Failure meaning |
|---|---|---|
| Checkout/root evidence / Developer and Scrum | Substantiated ownership plus canonical operational-root versus writable tooling-root contract, accepted by original setup reviewers | Setup remains unmet; runner writing blocked, not a remote runtime rejection |
| Runner / Developer | Reviewed retained executable and offline root, ownership, mismatch, redaction, partial-role, unknown-effect and zero-create/send fixtures | Coding failure; no inference or publication is authorized by a fixture |
| Joined source / assigned integration owner | Candidate ancestry, reviewed application/lab commits, exact joined checks, durable Git accounting and scoped push outcomes | Predeployment integration prerequisite failure |
| Inventory / DevOps, independent of coding | Strict-trust private current/rollback, package, identity, caller/effective-action and held-effect observations | Explicit missing observation, not evidence of absent permission |
| Formal integration / original E2E | Validate the reviewed joined source through local repository scripts | Accurate FAIL is actionable assessment, not cloud-pass |
| Exact release / original DevOps | Actual Linux/amd64/hosting-Python checks, final source/settings/package hashes, retained preview and guarded publication | Do not create a trial parent from an unjoined or drifted release |
| Finite trial / original DevOps | Rejoin scenario, reviewed source, final common package and actual three-role versions before parent creation; architect trusted ingress/receiver success before reviewer | Preparation rejection, observed receiver rejection, partial ingress and unknown outcomes remain distinct |
| RP-S2 acceptance / original E2E and DevOps | Three healthy common-bundle roles, accepted remote artifacts, private MI Blob provenance and genuine Decision-1 plus deterministic gates G1-G4 | Identity selection alone is insufficient |

The installed source is unconditional B, not a scenario switch. An A trial
requires its own supported corrected source/regression; relabeling B as A or
retrying unchanged A must fail before create/send. A permission write is a
conditional join only when fresh effective-action evidence establishes the
necessary authorized delta; document exact scope/rationale and deterministic
plan/write/readback. No speculative grants or new permission approval stage.

A selected path requires both roles' observed ingress and receiver validation.
Accepted remote collaboration additionally requires the exact candidate/review
prerequisites and coordinator acceptance, private managed-identity artifact
operations and genuine routing records. Preserve historical UNKNOWN publications,
held parents, rollback assets and cleanup uncertainty regardless of the result.
Known-response inspection retrieves the exact response without another send.
No automatic fallback, replacement parent or adoption of held histories.

RP-S3 still owns live two-turn continuity, once-only supported compute stop/resume,
separate-parent isolation and final AC1-AC9/G1-G8 closure. Account-wide Blob
Contributor provides application-enforced scope, not malicious-host/storage-RBAC
isolation. Material namespace/held-state changes return to the existing
Architect-advised PO/Scrum process; ordinary implementation stays with the
retained owners. This architecture revision neither resolves the stopped setup
task nor certifies live selection, transport, deployment or release acceptance.

## Scope, accepted baseline and cumulative design

This is the `SprintArchitecture` handoff for **RP-S1**, not an implementation,
SprintPlan, deployment or live acceptance result. The customer outcome remains
a hosted coordinator repeatedly calling remote architect and reviewer agents,
preserving each specialist's session within the same parent conversation.
Exactly three hosted deployments remain.

Accepted inputs are retained, not reopened:

- [Release architecture](customer-prototype-architecture.md), `cde76380c9c41201f19aedf4b290958c95472689`.
- [UX](customer-prototype-ux.md), `c17813567e7d3db09abe1d2403b948c98131c24f`.
- [Release plan](customer-prototype-release-plan.md), `f20ac1ee1cdbc561198d51fba53f14c90348de8d`.
- [Sprint design](customer-prototype-sprint-design.md), `6a24eaf3110bd964f992a87e01e6916f505e0dda`.

This revision inspected clean application baseline `6a24eaf3110bd964f992a87e01e6916f505e0dda` on
`feature/customer-hosted-session-prototype`. No completed prior sprint was
supplied. Retain the integrated RP-S1 work: coordinator fixtures `6614440`,
direct model-continuation fixtures `c454e50`, human view `56b762e`, documentation
`e24fcb9`, research `39c3b4e` and source reconciliation `24b883f`. These are
existing implementation history, not new progress or live acceptance here.
The cumulative design is the accepted release architecture plus this RP-S1
refinement. The existing [design](design.md), [migration boundary](migration-plan.md),
[implementation workflow](implementation-workflow.md) and
[recovery plan](identity-recovery-plan.md) remain applicable.

The tier documents below are derived architecture contracts, not a replacement
requirements source or new services. These logical tier names describe existing ownership:

| Logical tier | Architecture file | Existing code responsibility |
|---|---|---|
| Coordinator | [coordinator](requirements/coordinator/architecture.md) | Parent-scoped bindings, workflow, artifacts and fenced acceptance |
| Specialists | [specialists](requirements/specialists/architecture.md) | Both remote roles' own model history and immutable proposals |
| Client and release boundary | [client-release](requirements/client-release/architecture.md) | Terminal projection and retained exact-release/live verification |

The supplied October 19 customer specification remains authoritative. Do not
copy private delivery inputs, evidence or settings into these directories.
Older accepted documents' statements that this directory did not exist describe
their baseline, not a prohibition on the tier-specific output required here.

### Prior dispositions and bounded acceptance

Apply these exact provenance-qualified references only to their original outputs:

- `["yaml-loops-v1:ArchitectureLoop","architecture-close-agreed-deliverable"]`
  retains accepted full-release architecture and unresolved identity handoff.
- `["yaml-loops-v1:UserExperienceLoop","ux-close-agreed-deliverable"]`
  retains accepted UX; no redispatch of integrated presentation work.
- `["yaml-loops-v1:ReleasePlanLoop","release-plan-close-agreed-deliverable"]`
  retains accepted release planning and original downstream owners.
- `["yaml-loops-v1:sprint/1/RP-S1/SprintDesignLoop","sprint-design-close-agreed-deliverable"]`
  retains accepted RP-S1 screens and fixture-to-display handoff.

None supplies SprintArchitecture reviewer votes, selects an identity path,
waives live/package gates or reopens an accepted handoff. Scrum Master owns
delta decomposition and Git reconciliation, not a redispatch of accepted work.

## Data flow and sprint delta

```text
user turn -> trusted hosted parent -> begin / route / execute / publish
                                        |
                           manifest.children[role]
                                        |
                     restore bound framework AgentSession
                                        |
                   remote specialist hosted session/version
                                        |
                   role-local stored model history/continuation
                                        |
                immutable proposal -> exact-input validation -> acceptance

complete existing events/result -> optional human stderr projection
                               -> unchanged default stdout / acceptance parser
```

Retain Python, MAF, Foundry Responses, dependency pins and explicit execution
order. Conversations, checkpoints and artifact/effect state remain independent.
Do not add a generic SessionManager, new ledger, framework, fourth service,
browser UI, storage broker or toy orchestration loop.

The integrated `test_followup_invalidates_old_approval_and_preserves_children`
in `tests/test_workflow.py` now records both roles before/after each call and
in the final manifest via `assert_recorded_bindings`. It verifies stable scope,
hosted/framework identities, pinned names/versions, exactly two creations, four
distinct responses, current requirements and invalidation at the follow-up send.
`test_reject_revise_review_reuses_both_children_with_fresh_responses` records
the four-call reject/revise/review path and exact c2 acceptance. Retain these
fixtures and their value snapshots; do not assign their implementation again.
Source inspection is not a fresh execution or live acceptance result.

`RemoteAgents.invoke()` already restores `AgentSession.from_dict(child.framework)`;
`recover()` advances its service continuation from the exact retrieved response.
Both real specialist files already load `specialist_history_v2` / `"history"`
and pass the restored session to their model stage. Architecture does not infer
that these source paths prove hosted or model continuation: RP-S1 must observe
their actual arguments and persistence with controlled offline boundaries.
`tests/test_specialist_continuity.py` already supplies both roles' real
load/model/store execution, identical-brief fresh-history controls, exact-response
no-send recovery and failed-retrieval/existing-output cases. Preserve that
handoff; only a concrete uncovered defect justifies a new fixture task.

## October 20 cross-sprint executable handoff

The accepted release architecture now distinguishes the integrated offline
identity handoff (`13203ac`, reconciled by `bb1743d`) from a hosted candidate.
`scripts/identity_handoff.py` has no live mode; its unresolved exit is not a
runtime fix. The specialist-only client is implemented in
`3aca5dc236695c5ec7eac98d0cd03bced40da7b8` and present on this branch.
Retain it for its original review/integration, without declaring its task
accepted here. The retained decision runner remains a Developer implementation
handoff, not unfinished RP-S1 continuity/UX work.
No completed prior sprint was supplied; this section carries the cumulative
design forward without declaring RP-S1 or RP-S2 accepted.

### Runtime boundary carried into RP-S2

The following client contract is now installed source, not live-selected B.
`WorkflowRuntime.resources()` unconditionally constructs specialist-only B;
it cannot select an A path from a scenario label. Preserve the accepted
[source-to-trial contract](customer-prototype-architecture.md#source-identity-is-part-of-the-scenario-contract):
before trial-parent creation, join the explicit scenario to reviewed source,
the exact common package and actual deployed role versions. `B-candidate`
requires the installed candidate or reviewed descendant; `A-correction`
requires its own evidenced supported correction and regression. Relabeling
B as A or retrying unchanged historical A fails preflight without dispatch.
There is no new runtime selector, configuration knob or approval stage.

Within the existing request-owned `WorkflowRuntime.resources()` stack, keep
the original opaque-only project/header resources and yielded tuple semantics
for routing, parent/model/history/checkpoint operations. B receives a distinct
specialist-only `ProjectClient`, copied headers and independent OpenAI-client
cache, passed only to `WorkflowRemoteAgents`. Do not mutate shared headers,
ambient hosting context or the non-specialist project. A shared credential/
transport is allowed only with regression coverage for safe close ordering
and cleanup on setup failure, cancellation and normal exit.

Before deriving B delegation, reconstruct the full trusted
`ScopeBinding.from_platform(...)` from captured authenticated hosting context
and compare it to runtime scope. Move only necessary pure candidate logic to
runtime-owned source; hosted code cannot import the offline runner. Preserve
opaque-call forwarding and reject container-user headers, absent/forged users
and call-ID-as-user substitution. Receiver principal equality is unchanged.
The coordinator and specialist tier files specify the corresponding tests.

There is no new runtime path selector. DevOps binds a named candidate trial
to reviewed source, one common bundle and exact three-role versions in private
evidence. Existing deployed A remains until deliberate guarded publication;
no automatic switch after an error. A later required selector/settings change
is an explicit Architect/Scrum delta, not an undeclared environment option.
Old pinned/held conversations keep their versions, histories and journals.
Only a fresh synthetic parent may enter this candidate; no implicit migration.

### Contract-first lanes and true joins

These are handoff contracts, not task IDs or new assignments. Scrum Master
owns decomposition, actual dependencies, exclusive resources and integration.

| Lane / original owner | Bounded doneWhen | Join or exclusion |
|---|---|---|
| RP-S1 retained source / Developer | Preserve integrated binding, revision, history and presentation fixtures; repair only affected concrete failures; hand off current checks | Do not redispatch accepted implementation or claim live proof |
| RP-S1 fresh inventory / DevOps | Privately bind sole-target current/rollback versions, packages, protocol, identities, caller/effective action and unresolved owners/effects | Independent of candidate/runner coding; no assumed missing grant |
| RP-S2 isolated runtime / Developer | Retain installed `3aca5dc` and its real resource-factory regressions for original review/integration; repair only concrete failures and check joined source | No duplicate implementation, deployment, namespace relaxation, schema/dependency/history migration or UX rewrite |
| RP-S2 local decision tooling / Developer | After safe lab writing ownership, retained runner satisfies the client-release tier contract with offline ownership, failure, redaction and unknown-effect regressions plus affected retained suite | Coding does not wait for cloud inventory; original DevOps exclusively owns guarded publication and live execution |
| Git/source integration / Scrum-assigned owner | Reviewed task commits joined on the authorized feature branch, exact joined source checked; named retained branches/task/commit/reason recorded for any abandoned code | Establish lab writing ownership safely; never switch its shared dirty checkout under writers |
| Bounded decision / DevOps | Joined runtime/tooling, fresh inventory and exact-source/Linux/package gates precede retained publication and finite trusted-ingress trial | Conditional permission plan/write/readback joins only if a required delta is evidenced; no formal E2E/cloud-pass credit |

The prior lab observation was `feature/swc-think-fast-aca-dns` with eight dirty/
untracked paths; this revision does not refresh that status. None is adopted here.
Scrum must assign safe lab feature-
branch/worktree reconciliation before any lab writing; no new human approval
is required for that internal ownership action.

The decision handoff names each reached/unreached role and returns `selected-A`,
`selected-B` or actionable `unresolved`. Architect-only entry is not both-role
selection or remote collaboration. A resource-construction guard failure is a
local preparation rejection, not observed receiver failure or proof of missing
permission. Classify receiver failure only from an observed child result;
missing observation remains unknown. Missing/changed principal, receiver rejection,
version drift or an unknown effect stops that candidate without another send.
A namespace or held-state contract change returns to existing Architect-advised
PO/Scrum reconciliation; an unavailable supported provider finding is an exact
external stop, not a reason to repeat old research or block remaining artifacts.

## Cross-tier fixture contract

Use test-owned recording adapters around existing interfaces, not a production
protocol or customer-visible evidence database. Capture before/after snapshots
by value: a reused mutable object must not make a comparison pass accidentally.

| Observation | Assert in offline tests | Do not infer |
|---|---|---|
| Parent | Same trusted scope/parent across initial and follow-up | Local filename or alias proves hosted ownership |
| Child, per role | Stable hosted ID, framework `session_id`, agent name and pinned version at each call and final manifest; stored hosted key matches binding | Entire framework dictionary must remain equal |
| Invocation | Ordered role, operation, turn/revisions, exact input refs, response ID and continuation passed/returned | Recovered known response counts as another send |
| Creation | Exactly architect and reviewer once across two turns or the four-call revision fixture | Two visible aliases prove two creations |
| Model, per role | Store key/context, restored identity/state/service continuation actually passed to model call; persistence after output | Same full brief or plausible memory proves history |
| Acceptance | Current requirement/candidate refs and hashes; old approval invalidated before calls; final exact revised review | Blob existence or SDK completion is acceptance |

Initial/follow-up fixture: synthetic private-ingress application, then queue
addition retaining earlier requirements; architect/reviewer each called on both
turns, four distinct invocation responses and two child creations.
Revision fixture: architect c1 -> reviewer blocked c1 -> architect c2 ->
reviewer approves c2. Both repeated calls use the original binding/version;
review c2 consumes exact c2 plus current requirements, not stale c1 approval.
Use controlled routing responses with existing deterministic gates, budgets and
Decision-1 contracts; never force success by bypassing publication.

For model-history tests, hold the input brief constant in a negative-control
comparison so input replay cannot explain the observation. Run each real role's
load/model/store path with a persisted first-session continuation and then a
fresh/absent history store. Assert the model boundary differs as expected.
Known pending model response retrieves that exact ID with zero model sends;
unknown/mismatched pending state remains held. Existing crash, parsing,
cross-scope, transport, checkpoint and fencing cases remain intact.

## Blocker disposition and conditional repair

Historical `NATIVE_HOST_PRINCIPAL` occurs before architect application entry:
the captured outgoing opaque call context matched, but trusted child user was
absent. It is unresolved; no cause-specific remedy, missing grant or platform
defect is established here. No fresh cloud inventory or public-remedy research
is claimed by this architecture refinement.

RP-S1 retains independent offline proof, clarity, and fresh-inventory/remedy-assessment
boundaries. Neither remaining artifacts nor validation waits for a provider answer.
DevOps freshly inventories target versions/packages/identities through retained
tools after sole-target private-settings/context validation. Architect/Developer
assess public supported contracts against installed pins and the exact observed
boundary. A research handoff records source/date/version applicability, supported
correction plus reproducer if established, or the precise absent finding.
Repeating old negative research without new evidence is not progress.

The prior bounded negative research remains valid within its originating scope,
but does not reject the additionally authorized delegation alternative.
If server-side resolution is still the missing evidence after both alternatives
are assessed, the actionable exit is
an exact-pair caller-resolution trace and documented supported platform/SDK
remedy. The operator must separately arrange provider contact/disclosure;
this invocation does not authorize submission or private evidence transfer.
This bounded negative finding may complete research, not RP-S2's live goal.

October 19 authority permits ordinary scoped corrections and guarded releases
for only the existing three roles; the old consumed diagnostic exception is not
a blanket ban on this new work. It never permits uncertain-effect replay,
identity substitution, speculative headers/grants, infrastructure/network/quota
changes or another target. Preserve held parents and original publication UNKNOWN.
Material contract, held-state migration or architecture changes use existing
Scrum Master reconciliation and Architect-advised PO decisions, not an invented
human approval or endless research loop.

### Identity-path decision contract for this sprint

Use the accepted release architecture's
[supported alternatives and selection contract](customer-prototype-architecture.md#supported-identity-alternatives-and-selection-contract).
The October 19 additional approval permits necessary narrowly scoped lab
RBAC/permission changes for either supported path; earlier blanket permission
exclusions are not a new approval prerequisite. No permission mutation or
live discriminator is performed by this document.

| Outcome | Required discriminator | Failing condition / closing action |
|---|---|---|
| `selected-A` | A measured authentication/configuration or effective-caller mismatch, supported correction and fresh trusted specialist ingress passing receiver checks | No mismatch or the same opaque-header failure: do not republish unchanged; evaluate B |
| `selected-B` | Stable authenticated end-user delegation across create/read/send/retrieve; actual child principal compatible with the parent's trusted binding; specialist entry and receiver validation pass | Missing/changed principal, namespace mismatch or held effect: retain evidence, reject that candidate; never weaken equality |
| `unresolved` | Actual attempted checks, why neither path is selected, exact missing fact/remedy and an actionable next owner/step | Continue remaining artifacts; live acceptance stays unmet, not implicitly waived |

For B, `Assignment.validate_receiver()` compares platform-derived child principal
to `scope_binding.principal`. A nonempty user header alone is insufficient:
delegating a platform-derived identity may resolve a different namespace.
Do not use opaque call IDs, assignment JSON, model text or client identity
headers as authenticated user authority. Keep required opaque-call forwarding
unchanged; do not forward container-only `x-agent-user-id`. The legacy
`platform_identity_headers()` helper is not a drop-in delegation fix.
Verify supported header coexistence rather than guessing.

Cover `RemoteAgents.prepare`, `create`, `_check` / `recover_creation`, `invoke`
and `recover`, including the distinct raw SDK and Responses header paths.
`WorkflowRuntime.resources()` now isolates specialist delegation from the original
project/header/cache used by routing and other non-specialist callers; retain
that boundary so parent/model/history/checkpoint authority cannot change
accidentally. If trusted namespace compatibility requires a new
binding contract, bring the exact mismatch to this existing Architect/PO/Scrum
process. Do not migrate held histories or remove receiver equality to select B.

Before any permission write, resolve the actual outbound coordinator principal,
both existing specialist targets and effective explicit data actions. Historical
impersonation permission presence is not fresh readback or proof it is missing.
If needed, scope only the required action to each supported existing agent scope;
an unsupported scope requires a documented smallest supported project scope,
not account/resource-group/subscription escalation. Record exact private
principal/role/resource IDs, before/after state, rationale, ownership and readback.
Use deterministic reviewed lab-owned scripts with unknown-outcome reconciliation;
never create duplicate grants or replace identities for convenience.

The bounded local repository script contract requires explicit application/lab
roots, scenario/path, exact versions and fresh synthetic scope, a finite intended
call sequence and pre-send journal. Offline negative controls cover omitted/
invalid identity, forged assignment principal, cross-parent scope, both roles,
all lifecycle header paths and exact-response no-resend. Observe architect
before reviewer; stop on held/unknown effect. Record presence/match classifications,
entry/receiver result and exact private evidence locators without public raw IDs.
Selection requires actual trusted ingress; offline tests or HTTP 200 do not select.
Both roles must pass before claiming remote collaboration. A required new package
goes through original DevOps source/Linux/package/publication gates; architecture
does not deploy to force selection. Permission readback is not runtime success.

The handoff records `selected-A`, `selected-B` or `unresolved`, hypothesis and
supported source/version applicability, actual tests, principal compatibility,
permission delta/scope/rationale, held effects and closing action. Neither path
is currently live-proven. Bounded decision tests are permitted here; formal E2E
and cloud-pass remain in their original loops through local scripts, not GitHub
Actions. No provider submission/private evidence transfer is authorized.

## Integration, verification and downstream handoff

Scrum Master owns actual task decomposition, minimal dependency edges and Git
reconciliation. These tier contracts are not assignments or another approval
stage. Shared `tests/test_workflow.py` changes need one assigned writer or
serialized fixture handoff. Terminal and README work can use existing schemas
without waiting for new runtime event fields.

Integrate only reviewed related readability changes; preserve originals and
unrelated dirt. Owners commit explicit intended paths on
`feature/customer-hosted-session-prototype` before original review. Integration
uses that branch; retained unmerged code requires named branch, task/commit IDs
and abandonment reason in a feature-branch commit message. Keep abandoned
branches. No broad staging, branch switch beneath writers, force push or reset.

Original E2E owns formal integration validation; original DevOps owns packaging,
publication and cloud-pass. Bounded architecture/planning decision tests do not
replace either gate. Serialize actual
`lab-hosted-release` and `lab-private-transport`; use `application-git-integration`
and, if needed, `lab-git-integration`. Scheduler names are not OS/cross-run locks.
Never race publication against acceptance. The live chain remains supported
correction + reviewed integration -> exact source/Linux/package gates -> guarded
publication -> initial acceptance -> follow-up -> supported stop/resume.
Separate-parent comparison needs initial evidence, not restart.

| Acceptance boundary | RP-S1 output versus later obligation |
|---|---|
| AC1 / G2 | Preserve remote-only architecture; actual accepted remote collaboration remains RP-S2 |
| AC2 / G5 | Exact offline binding/response assertions now; live two-turn comparison remains RP-S3 |
| AC3 | Controlled four-call workflow plus direct model-history fixtures now, labeled offline |
| AC4 / G6-G7 | Retain recovery/isolation regressions; actual once-only supported stop/resume and separate-parent evidence remain RP-S3 |
| AC5 / G1-G8 | G1 final common bundle, G2 collaboration, G3 MI/private Blob, G4 genuine Decision-1, G5 continuity, G6 recovery, G7 isolation, G8 truthful closure remain live gates, not architectural PASS |
| AC6 | Retain integrated first-screen README and opt-in terminal contract, then real demonstration later |
| AC7 | Integrated targeted/application/repository checks now; exact Linux/amd64/hosting-Python package gate remains DevOps |
| AC8 | Review/integrate intended source, preserve unrelated dirt, commit then reviewed scoped push; no private artifacts in Git |
| AC9 / G8 | Later report actual demo/setup, sanitized proof, final/rollback bindings, cleanup and limitations; no success from this document |

Required source checks use existing validated Python by absolute path:
`Test-Demo.ps1 -Python <absolute-path> -LabRepositoryRoot <explicit-root>` and
`scripts/Test-Repository.ps1 -Python <absolute-path>`. Retained suite follows lab
tool changes. Revalidate final changed source/package, not historical counts.
No dependency install without manifest change or missing-tool failure.

### Historical verification of the preceding documentation revision

Using the existing validated absolute Python 3.12.10 executable, without
dependency installation, `Test-Demo.ps1` with explicit lab root passed dependency
checking, **177 offline tests in 19.520 seconds**, and compilation.
`Test-Repository.ps1` passed index, public-boundary (**70 public files**), JSON,
PowerShell, context and whitespace checks. Local documentation checks verified
**32 relative links/anchors across four architecture documents**, AC1-AC9 and
the identity-selection handoff fields.

These are local/offline results, not hosted proof. No lab files changed; its
full retained release suite was not rerun. No fresh cloud inventory, live path
discrimination, permission write, publication, Linux hosting-package validation,
formal E2E acceptance, stop/resume or live continuity/isolation occurred.
The pre-existing unrelated lab worktree remains untouched. Final exact-source/
common-bundle and AC1-AC9/G1-G8 live gates remain downstream obligations.

### Verification of the October 20 cross-sprint refinement

The current source-to-trial reconciliation starts at `6a24eaf` and supersedes
the earlier ownership/readiness description, not its retained test contracts.
Using the existing absolute Python executable with explicit lab root,
`Test-Demo.ps1` passed dependency checking, **192 offline tests in 25.671
seconds**, and compilation. `scripts/Test-Repository.ps1` passed index,
public-boundary (**74 public files**), JSON, PowerShell, context and whitespace
checks. A read-only documentation check verified **36 relative links/anchors**
and balanced fences across all four architecture documents. No dependencies
were installed. These fresh offline results do not retroactively execute the
denied checks recorded by SprintDesign or certify its earlier exact source.
No settings import, cloud inventory, permission change, publication, inference,
Linux-package check or formal acceptance was performed. Lab sources were not
changed; its full retained suite was not rerun. Live path selection remains
unresolved and historical unknowns/held parents remain preserved.

The following results describe the preceding refinement, not this exact source:

Using the existing absolute validated Python 3.12.10 executable with the
explicit lab root, `Test-Demo.ps1` passed dependency checking, **186 offline
tests in 18.803 seconds**, and compilation. `scripts/Test-Repository.ps1`
passed index, public-boundary (**73 public files**), JSON, PowerShell, context
frontmatter and whitespace checks. A local read-only documentation check passed
**34 relative links/anchors across all four architecture documents**, the four
accepted input commit references, lane/join fields and AC1-AC9/G1-G8 coverage.
The index was refreshed using `scripts/repo_index.py`; no paths were added or
deleted. No dependencies were installed.

These source/document results do not select A or B or close AC7's final Linux/
hosting-package requirement. No runtime, lab tooling or permission changed;
the full retained lab suite was therefore not rerun. No settings import, cloud
inventory, permission readback/write, inference, deployment, Linux package
check, formal E2E or live continuity/recovery/isolation test occurred.
The original UNKNOWN and held state are preserved; existing accepted upstream
votes do not supply votes for this sprint architecture refinement.

Architect handoff is this cumulative sprint design, navigable tier contracts
and concrete unresolved-blocker disposition, committed for original Product
Owner, Critic and Red Team review. Reviewer agreement is collected by the
existing loop, not asserted here. No runtime repair or live certification is
part of this handoff. Five consecutive rounds without reviewer-verified new
progress stop blocked; productive rounds remain uncapped.
