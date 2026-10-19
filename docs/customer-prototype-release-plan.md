# Customer hosted-session prototype: release plan

## Product outcome and planning authority

Deliver a customer-shareable prototype in which a hosted coordinator repeatedly
calls a remote architect and reviewer, preserving each specialist's session
within the same parent conversation. Exactly three hosted roles remain.
Acceptance requires working remote collaboration, not a plan, mock, HTTP 200,
package upload or completed SDK response.

This Product Owner deliverable implements the Release Plan Loop. The supplied
October 19, 2026 customer specification is the requirements source; there is no
`docs/requirements` directory. Do not copy private delivery inputs into Git.
The accepted [architecture](customer-prototype-architecture.md) at
`1f690f5011bef61494b8181fd14e779fa55d858e` and
[UX contract](customer-prototype-ux.md) at
`0f2a2b22a23fdb614e666274eec29c612da0a92f` are inputs, not work to reopen.
No prior dispositions or reconciled corrections were supplied for this round.
Stakeholder, Architect, Designer and Critic review this release-plan commit in
the existing loop; this document does not assert their votes.

Current authority permits scoped implementation, reviewed feature-branch
commit/push, retained guarded releases for the existing three roles, synthetic
live checks, supported hosted compute stop/resume, the established temporary
read-only SSH mount and starting the exact registered command VM if necessary.
It does not permit infrastructure/permission/identity replacement, quota,
network/DNS/VPN/registry/monitoring changes, alternate projects/regions/profiles,
provider submission or private evidence transfer. No routine extra approval
stage is added for ordinary authorized work.

Older diagnostic restrictions in the
[recovery plan](identity-recovery-plan.md) and
[implementation workflow](implementation-workflow.md) record historical scope.
They do not cancel this invocation's corrective-work authority. Conversely,
current authority does not reconcile the original publication UNKNOWN, certify
historical cleanup or authorize replay of held parents/uncertain effects.
Do not rerun the consumed diagnostic sequence merely to fill a checklist.

## Baseline, priorities and invariant contracts

Historical execution failed before architect application entry at
`NATIVE_HOST_PRINCIPAL`: actual outbound opaque call context matched, but the
child had no trusted user. Reviewer, continuity, restart and isolation were not
reached. No supported cause-specific remedy, platform defect or missing grant
is established by this planning work. Fresh versions/packages/context must be
inventoried downstream; historical architect17/reviewer15/coordinator23 are
not current-release assertions.

The application starts on `feature/customer-hosted-session-prototype` with
17 pre-existing dirty paths and no staged paths. They include related readability
work, runtime/test edits and documentation. Preserve them for deliberate review
and integration; this plan does not accept or commit them. The lab also has
pre-existing dirty/untracked work, including unrelated infrastructure material.
This loop changes neither lab source nor application runtime.

Priority order:

1. Preserve trusted parent/child identity, exact immutable prerequisites,
   versions, fenced/ETag acceptance, checkpoints and write-ahead effects.
2. Complete useful offline continuity/continuation proof and customer clarity
   while investigating the supported live remedy independently.
3. Repair only evidenced runtime defects; validate and release the exact source
   through retained tools, then prove initial real collaboration.
4. Prove two turns, supported recovery and isolation; deliver truthful evidence
   and reviewed generic source.

Retain Python, MAF, Foundry Responses and existing dependency pins and explicit
execution order unless an observed defect justifies a focused correction.
No generic SessionManager, fourth service, replacement framework, browser UI,
toy implementation, speculative header/grant or local fallback. A stable
hosted/framework session identity is not an immutable entire framework
dictionary: response continuation advances. Account-wide Blob Contributor means
role ownership/parent isolation is application-enforced, not storage-RBAC or
malicious-host isolation.

## Sprint sequence

These three uniquely identified sprints are initial delivery increments, not a
maximum sprint count or fixed calendar promise. Additional productive repair
sprints may be planned through the existing review/retro. Goals are ordered,
but ready independent work need not wait for a global sprint barrier. No
duration, spend, concurrency ceiling or total productive-round cap is imposed.
Scrum Master owns contract-first task decomposition and actual assignment in
SprintPlan, with task IDs, kind, owner, dependsOn, doneWhen, exclusions, handoff
and actual shared-resource names. The work boundaries below are release
contracts, not a competing task graph.

### RP-S1 — Evidence-ready source and understandable continuity

**Goal:** make the customer invariant easy to understand and independently
testable offline, preserve existing work, and establish the next supported live
action without waiting on provider resolution to finish local improvements.

**Bounded work and handoff**

- Scrum Master inventories dirty/staged work and named branches, assigns Git
  reconciliation, and establishes disjoint contracts/fixtures before writing.
  Review related readability changes, preserve originals and exclude unrelated
  work. Developer integrates only reviewed related source on the feature branch.
- Developer strengthens the existing two-turn regression for both roles;
  adds a controlled reject/revise/review fixture and direct specialist
  model-history continuation checks using the real stage/session path.
- Developer implements the accepted terminal/README design; Designer reviews
  it against the existing UX contract, not a new web experience.
- DevOps freshly validates the sole-target linkage/context and exact deployed
  versions/packages/identities through retained tools. Architect/Developer
  assess current supported public contracts and concrete runtime defects.
  Provider-dependent negative findings are a valid bounded research handoff,
  not release success. No submission/contact or speculative publication.

**Sprint acceptance / doneWhen**

1. The follow-up test asserts the actual stable parent, both hosted/framework
   child IDs and pinned versions; exactly two child creations total; both
   roles invoked on both turns; fresh invocation response IDs; private ingress
   retained plus queue added; stale candidate/review approval invalidated.
2. A controlled offline architect -> blocked reviewer -> same architect ->
   same reviewer loop records reused bindings, fresh responses, revised exact
   candidate/review references and final current acceptance.
3. Both specialists' second model calls use restored stored history/
   continuation, not merely the replayed brief. Fresh/absent-history negative
   controls and known-response retrieval with no resend are covered.
4. README first screen gives goal, diagram, two-turn example, stable versus
   advancing identities, short accurate source path and truthful live notice.
   Opt-in human terminal output includes useful design/review content without
   changing existing default stdout, delegation/result schemas or parser.
   Tests cover partial/malformed/missing results, holds, recovery, absent
   verification evidence and terminal-control sanitization. Alias equality
   alone never becomes verified continuity or a creation-count claim.
5. Targeted checks, `Test-Demo.ps1` and `scripts/Test-Repository.ps1` pass for
   the integrated source; retained lab regressions pass if tooling changed.
   Evidence distinguishes offline tests from deployment/live results.
6. Fresh inventory and a supported-remedy assessment identify a concrete
   correction to attempt, or the exact missing provider finding/action.
   Existing UNKNOWN publications/held parents remain preserved and disclosed.

**Exclusions:** no claim that fixtures repair identity or pass live AC1/AC2;
no inference solely to repeat historical failure; no acceptance of dirty work
without review; no package/live certification from Windows checks.

**Handoff:** reviewed scoped source/fixture commits, UX implementation evidence,
private exact baseline locators, and supported repair or actionable negative
finding to RP-S2. Offline deliverables can be accepted even if live work stops.

### RP-S2 — Supported repair and exact three-role remote collaboration

**Goal:** correct the evidenced runtime boundary within authority, produce one
verified common bundle, and accept a real current architect/reviewer result.

**Bounded work and handoff**

- Developer implements the smallest supported correction with a
  failing-before/passing-after regression. Architect advises on compatibility
  and held state; material architecture/contract/feasibility changes return to
  existing Architect-advised PO scope decisions via needs-replan.
- DevOps owns testing, build, preview, guarded publication, live diagnosis and
  repair iteration in the original DevOps work loop. No separate deployer or
  new approval stage. Directly coupled retained lab fixes require their suite.
- Scrum Master reconciles owner commits/review feedback and integration.
  Required source review and exact-package gates precede publication.

**Sprint acceptance / doneWhen**

1. Supported evidence explains why the correction addresses the observed
   gate. Identity/scope, immutable outputs, exact references, ETag/fencing,
   checkpoints, bounded calls, genuine calibrated Decision-1 and unknown holds
   remain enforced. Dependency changes, if necessary, have compatible
   provenance/lock updates and an explicit held-state compatibility strategy.
2. Final intended source passes affected tests, the full application runner
   with absolute existing validated Python and explicit lab root, repository
   checks, affected retained regressions and actual Linux/amd64/hosting-Python
   package checks. No dependency install without manifest change/missing tool.
3. Retained source/allowlist/dependency/trust gates, immutable stage, settings/
   source/ZIP hashes and fresh version preview bind the exact package. Explicit
   ApplicationRoot/LabRepositoryRoot are used; packages/stages/evidence stay
   outside both repositories. No historical migration hash resealing.
4. Guarded publication outcomes are reconciled before another operation.
   Exactly three healthy roles use one final verified common bundle with
   unchanged identities and rollback versions/packages retained (G1).
   A mixed diagnostic deployment cannot pass this criterion.
5. A fresh synthetic private-ingress initial parent executes architect and
   reviewer remotely, with current exact input/output hashes, producers,
   versions, revisions and fenced coordinator acceptance (AC1/G2). Actual MI
   private-path Blob provenance and genuine Decision-1/final gates pass
   (G3/G4). HTTP 200 or SDK completion alone is insufficient.

**Exclusions:** no blind upgrade/header/grant experiment; no replay of uncertain
publication/inference; no provider-case submission; no infrastructure workaround.
If no supported remedy is available, this sprint remains blocked against its
live goal even when its research task is complete.

**Handoff:** reviewed exact source/package/version/identity/rollback bindings,
known publication outcomes/owned cleanup, and completed initial-parent private
evidence/state for RP-S3. Keep unsuccessful/held parents separate and retained.

### RP-S3 — Live continuity, recovery, isolation and customer delivery

**Goal:** demonstrate the original two-turn promise on the final release and
close AC1-AC9 truthfully, preserving historical unknowns and unrelated work.

**Bounded work and handoff**

- DevOps uses RP-S2's completed, non-held synthetic parent for follow-up, then
  one supported compute stop/resume. It owns separate-parent live testing and
  exact evidence through retained acceptance/connectivity tooling.
- Developer updates measured README/demo status and delivery documentation;
  Designer checks customer clarity. Scrum Master owns final Git reconciliation.
  Product Owner evaluates AC1-AC9 in existing sprint review/release closeout.

**Sprint acceptance / doneWhen**

1. Add an asynchronous queue while preserving private ingress/earlier
   requirements. Actual parent and both specialists' hosted/framework bindings
   and pinned versions remain stable; each role runs on both turns with new
   invocation responses and current revised output; no follow-up child creation
   occurs (AC2/G5). Preserve the exact private comparison, not memory prose.
2. Once-only supported hosted compute stop has a durable marker and confirmed
   stopped/idle state. Continue the same parent/children/checkpoints/effect
   journal without duplicate sends (AC4/G6); do not claim hard-crash recovery.
3. A separate synthetic parent has distinct children/artifact scope and excludes
   the first parent's requirements. Existing cross-scope rejection regressions
   pass (AC4/G7); account-wide permissions remain accurately disclosed.
4. Actual two-turn terminal view and useful design/review output agree with
   private machine evidence. The final command uses implemented syntax,
   synthetic input, safe aliases, private state and retained trusted transport.
   Detailed JSON remains separately available (AC6).
5. Required checks cover the exact delivered source and common bundle (AC7);
   changed runtime/package inputs invalidate earlier certification and require
   fresh gates/publication and affected live evidence. Documentation-only
   closeout changes still receive repository checks and source-closure audit;
   do not invent a new bundle just to change a report.
6. Reviewed intended application changes and affected retained tooling are
   committed and pushed on `feature/customer-hosted-session-prototype` in the
   affected repositories. All task code is integrated there or retained on a
   named branch with task, commit IDs and abandonment reason recorded in a
   feature-branch commit message. Keep abandoned branches and unrelated dirty
   work; disclose remaining dirt instead of resetting it (AC8).
7. Delivery report lists reproducible setup/terminal command, sanitized
   continuity proof, checks actually run, exact final/rollback bindings, newly
   owned cleanup, remaining limitations and every AC1-AC9/G1-G8 result (AC9/G8).
   Private exact locators stay private; generic customer documentation contains
   no secrets, private lab literals, evidence, packages or workflow runtime.

**Exclusions:** no hard kill, historical cleanup certification, destructive
deletion/pruning, automatic retry of uncertain stop/send, real customer input
or storage-enforced isolation claim.

**Handoff:** customer-ready only if every release criterion passes live where
required; otherwise precise blocked/needs-input report with unmet criteria and
next supported action, never a customer-ready success label.

## Critical path, minimal edges and shared ownership

Baseline/contract inventory enables three independent boundaries: offline
fixtures, terminal/README implementation, and supported-remedy assessment/fresh
release inventory. Terminal fixtures may use the existing event contract;
they need not wait for identity repair. Final integration waits for each
owned source change it includes, not unrelated research or unavailable provider
responses. No new diagnostic task is mandatory when existing bound evidence
already identifies the unsupported boundary.

The live critical chain is:

```text
supported correction + integrated reviewed source
  -> final source/Linux/package gates -> exact preview -> guarded publication
  -> accepted initial parent -> same-parent follow-up -> supported stop/resume
  -> evidence closeout
final publication -> separate-parent run
initial-parent evidence + separate-parent evidence -> isolation comparison
recovery + isolation comparison + source/Git reconciliation -> final closeout
```

Separate-parent comparison needs initial-parent evidence, not its follow-up or
restart. Independent parents may logically overlap only if retained transport,
admission and ownership permit; default to serialization for actual shared
tools. Architect output precedes exact reviewer consumption and coordinator
acceptance; same-parent turns are serial. No publisher races live acceptance.

Scrum Master assigns actual `exclusiveResources`, including
`application-git-integration`, `lab-hosted-release` (publisher/project/shared CLI
and stage), and `lab-private-transport` (mount/ports/connection owner); use
`lab-git-integration` if lab files change. Shared files also require exclusive
ownership or an explicit fixture handoff. Scheduler names are not OS or
cross-run locks: check existing owners, never switch a shared branch under
writers or remove Git locks. Only the original DevOps loop deploys.

## Evidence coverage and release decision

| Criterion | Planned evidence owner and increment |
|---|---|
| AC1 / G2 | DevOps RP-S2: actual remote current artifact acceptance, exactly three roles |
| AC2 / G5 | Developer RP-S1 fixtures; DevOps RP-S3 exact live two-turn comparison |
| AC3 | Developer RP-S1 controlled repeated binding/response and specialist model-history fixtures, explicitly offline |
| AC4 / G6-G7 | DevOps RP-S3 supported stop/resume and separate-parent comparisons; Developer retained rejection tests |
| AC5 / G1-G8 | DevOps RP-S2 G1-G4; RP-S3 G5-G8; PO closeout checks every gate |
| AC6 | Developer RP-S1 README/terminal; Designer review; DevOps RP-S3 real demonstration |
| AC7 | Developer targeted/source checks; DevOps RP-S2 exact Linux/package gates and RP-S3 freshness audit |
| AC8 | Scrum Master Git reconciliation; owners explicit-path commits; reviewed scoped push before closeout |
| AC9 / G8 | DevOps exact bindings/cleanup/evidence; Developer generic docs; PO truthful release decision |

Use the existing pinned validated Python by absolute path:
`Test-Demo.ps1 -Python <absolute-path> -LabRepositoryRoot <explicit-root>` and
`scripts/Test-Repository.ps1 -Python <absolute-path>`. Retained lab suite runs
after release/connectivity changes; retained Linux checks must bind the final
source/hosting package. Historical test counts and packages do not certify new
source. Known response retrieval is not a new invocation; do not demand a new
response ID from retrieval itself.

Owners commit useful intended partial work before original reviewers inspect
it, using explicit owned paths and shared-checkout `git commit --only`. Include
the required Copilot trailer and observed usage metadata only when available.
Never sweep staged/dirty work, force-push, amend reviewed history or remove
another owner's lock. Integration and push use the authorized feature branch;
do not introduce a separate acceptance board.

## Repair iteration and stop semantics

For each repair: observe exact failure/current bindings -> supported hypothesis
-> focused regression/fix -> targeted and required exact-release checks ->
reviewed exact package/preview -> guarded publication -> synthetic live
comparison -> reconcile outcome and newly owned cleanup before another effect.
Do not treat repeated speculative publications, repeated tests, reworded
findings or file churn as new progress.

Scrum Master reconciles unresolved review feedback in the existing loop;
Architect advises PO on ambiguous scope. Raw suggestions remain audit evidence.
Apply required/approved and deferred/declined dispositions only within their
originating task/acceptance boundaries; cite the exact reference if reconsidered.
Never rewrite requirements to waive a failure or reopen accepted handoffs.

Five consecutive rounds without reviewer-verified new progress stop blocked;
productive rounds/sprints have no total cap. Genuine missing authentication,
provider information or out-of-scope authority can stop earlier. A provider-only
exit must specify the exact-pair caller-resolution trace/documented remedy
needed and the operator's next action; do not submit or transfer private evidence.
Fresh public supported-contract research remains allowed, but absence of a
supported remedy cannot be solved by inventing one. Internal material scope
changes use needs-replan, not manufactured human approval.

If blocked, retain completed offline work, known response IDs, held parents,
UNKNOWN publication history, rollback packages and private evidence. Clean only
positively identified newly owned processes/listeners/mounts. Report each
criterion as verified, failed, not reached or otherwise unverified with its
actual evidence scope; an actionable research result completes only that bounded
task. Release acceptance still requires AC1-AC9, not agreement on a failure report.
