# Customer hosted-session prototype: release plan

## Product outcome and planning authority

Deliver a customer-shareable prototype in which a hosted coordinator repeatedly
calls a remote architect and reviewer, preserving each specialist's session
within the same parent conversation. Exactly three hosted roles remain.
Acceptance requires working remote collaboration, not a plan, mock, HTTP 200,
package upload or completed SDK response.

This Product Owner deliverable implements the Release Plan Loop. The supplied
October 19, 2026 customer specification is the requirements source.
`docs/requirements/{coordinator,specialists,client-release}/architecture.md`
contains derived RP-S1 tier contracts, not replacement requirements.
Do not copy private delivery inputs into Git.
The accepted [architecture](customer-prototype-architecture.md) at
`2a736d94cb99c01aca0c516aeaf920e61ddb8fbd` and
[UX contract](customer-prototype-ux.md) at
`3ee9798afa4a419be87bcb68fdfc3540875d171a` are inputs, not work to reopen.
Apply prior dispositions
`["yaml-loops-v1:ArchitectureLoop","architecture-loop-status-reconciliation"]`
and `["yaml-loops-v1:UserExperienceLoop","ux-loop-status-reconciliation"]`
only to their accepted architecture and UX handoffs. Neither supplies release-plan
reviewer votes nor waives unresolved identity or final release gates.
Stakeholder, Architect, Designer and Critic review this release-plan commit in
the existing loop; this document does not assert their votes.

Current authority permits scoped implementation, reviewed feature-branch
commit/push, retained guarded releases for the existing three roles, synthetic
live checks, supported hosted compute stop/resume, the established temporary
read-only SSH mount and starting the exact registered command VM if necessary.
The additional October 19 approval permits either supported authentication/
configuration correction (A) or `x-ms-user-identity` delegation (B), including
necessary narrowly scoped lab RBAC/permission changes. Architect/Scrum may use
bounded local repository decision scripts during design/planning. This is not
permission for identity replacement, new infrastructure, quota,
network/DNS/VPN/registry/monitoring changes, alternate projects/regions/profiles,
provider submission or private evidence transfer. Formal integration validation
remains in the End-to-End Test Loop; publication and cloud-pass remain in the
DevOps Work Loop. Both execute local in-repo scripts developed, run and
troubleshot by agents, not GitHub Actions or ad hoc nondeterministic sequences.
No routine extra approval stage is added for ordinary authorized work.

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

This revision freshly inspected clean application HEAD
`3ee9798afa4a419be87bcb68fdfc3540875d171a` on
`feature/customer-hosted-session-prototype`. Related RP-S1 source and clarity
work was already integrated by `24b883f910dedbc8dc524177f29f59e061be265e`;
workflow fixtures `6614440`, specialist continuation fixtures `c454e50` and
terminal view `56b762e` are retained implementation history, not new progress
or fresh live evidence. The original 17-path dirty baseline is historical,
not the current application worktree. The lab still has unrelated dirty/
untracked work; this loop changes neither lab source nor application runtime.
Do not redispatch accepted work simply because a new planning loop begins.
Scrum Master reconciles the existing RP-S1 SprintPlan's historical input hashes
and narrowly scoped research exclusions against this new authority before
assigning new delta work; do not rewrite its completed-task acceptance.

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
toy implementation, speculative header/grant or local fallback. Necessary
evidence-backed permissions for the chosen path are authorized, not speculative
grants. A stable hosted/framework session identity is not an immutable entire
framework dictionary: response continuation advances. Account-wide Blob Contributor means
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

**Carry-forward:** preserve the integrated fixtures, README and opt-in view.
Criteria 1-5 below remain their verification contract, not instructions to
repeat accepted implementation. Rerun checks for changed source and close only
concrete gaps. The new planning delta is criterion 6's identity-selection
handoff and its local script/fixture contract. Unresolved selection must not
block remaining release/sprint artifacts, fixtures or documentation.

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
  Assess both authorized paths using the selection contract below rather than
  treating old opaque-context research as a provider-only verdict. Actionable
  unresolved findings are a valid bounded research handoff, not release
  success. No submission/contact or speculative publication.

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
6. Fresh inventory and a supported-remedy assessment hand off `selected-A`,
   `selected-B` or `unresolved`, with the exact observations, principal-namespace
   compatibility, supported correction or next closing action, permission
   scope/rationale if applicable, held effects and private evidence locators.
   Offline probes alone cannot select a path. A bounded live discriminator
   must reach trusted specialist ingress under the contract below; an
   unresolved finding must say which path/boundary remains untested and why.
   Existing UNKNOWN publications/held parents remain preserved and disclosed.

**Exclusions:** no claim that fixtures repair identity or pass live AC1/AC2;
no inference solely to repeat historical failure; no acceptance of dirty work
without review; no package/live certification from Windows checks.

**Handoff:** retain reviewed scoped source/fixture commits and UX evidence;
provide fresh private baseline locators, scripted decision-test contract and
supported repair or actionable unresolved finding to RP-S2. A discriminator
requiring changed hosted source hands its minimal reviewed fix to original
DevOps; planning does not publish to force selection. Offline deliverables and
remaining planning artifacts can complete even if selection/live work stops.

### Identity-selection contract across RP-S1 and RP-S2

Use the accepted architecture's
[selection contract](customer-prototype-architecture.md#supported-identity-alternatives-and-selection-contract),
not a new protocol or a permission wizard. This work may cross the sprint
handoff without creating a global barrier:

| Boundary | Done when / closing action | Original owner and exclusions |
|---|---|---|
| Fresh context and fixture contract | Validate sole-target linkage through `Use-Settings.ps1` and the existing private native settings; record exact role/version/package/protocol/caller/grant/rollback bindings without printing values. Define both-role, two-parent, missing/invalid identity, forged assignment and known-response no-resend cases. | Scrum Master decomposes; Developer owns fixtures; DevOps owns retained cloud inventory. No production profile, inferred missing grant or held-parent replay. |
| A: authentication/configuration correction | A measured supported mismatch has a failing-before/passing-after regression and a minimal correction; a finite scripted synthetic call reaches specialist application entry with trusted principal and receiver checks passing. | Architect advises, Developer repairs, DevOps executes release prerequisites. Unchanged opaque-header republishing, metadata or HTTP 200 cannot select A. |
| B: delegated user identity | A server-authenticated stable identifier uses the supported delegation contract on prepare/create/read, Responses send and known-response retrieve. Both SDK client paths and principal equality/namespace are tested; specialist-only headers do not alter routing, model, history or parent authorization. | Developer implements the narrow boundary; Architect advises compatibility. Never use opaque call IDs, assignment JSON, client-supplied/default identities or outbound container user headers as authority. |
| Required permission delta | Freshly identify actual caller, effective data action and existing assignment; deterministic reviewed lab scripts compare/plan/write/read back only a demonstrated necessary delta, with durable ownership and exact scope/rationale. Unknown effects hold. | DevOps in the original work loop; approval is already supplied. Prefer existing specialist agent scope, or document the smallest supported project scope before mutation. No broad Owner/Contributor, convenience account/subscription grant, duplicate assignment or identity replacement. |
| Decision record | Explicit scenario and finite intended sequence, journal-before-send, fresh synthetic scope, architect before reviewer; exact private bindings and sanitized presence/match/entry flags; `selected-A`, `selected-B` or `unresolved` with closing action and cleanup. | Architect/Scrum may run bounded planning decision scripts. Stop a candidate on held/unknown effects; inspect known responses, never resend for a missing receipt. Both roles must pass before claiming collaboration. No formal release acceptance from a discriminator. |

For B, verify the actual platform-resolved principal matches the trusted
parent/assignment binding; merely making the user header nonempty is not
success. Establish supported coexistence/precedence with unchanged opaque call
forwarding rather than guessing. Do not apply a specialist header globally
through the shared workflow project client. Namespace mismatch or a required
schema/held-state migration returns to this existing Architect-advised PO
scope decision via Scrum reconciliation; preserve equality checks and old
histories, not silent rebinding. No further user permission request is needed
for the already-authorized scoped path.

Planning tests cannot bypass final source/Linux/package/review gates or the
retained publisher: DevOps owns any required publication. If neither supported
alternative can be exercised safely, return an actionable unresolved record
and continue artifact generation. A provider-only stop needs the precise
unavailable finding/remedy after accounting for both paths, not the old
opaque-context result alone.

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
- The original End-to-End Test Loop owns formal integration validation through
  local repository scripts. It may accurately agree on predeployment FAIL;
  this never supplies DevOps cloud-pass or release acceptance.
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
   unchanged hosted identities, documented necessary permission deltas for
   the selected path, and rollback versions/packages retained (G1).
   A mixed diagnostic deployment cannot pass this criterion.
5. A fresh synthetic private-ingress initial parent executes architect and
   reviewer remotely, with current exact input/output hashes, producers,
   versions, revisions and fenced coordinator acceptance (AC1/G2). Actual MI
   private-path Blob provenance and genuine Decision-1/final gates pass
   (G3/G4). HTTP 200 or SDK completion alone is insufficient.

**Exclusions:** no blind upgrade/header/grant experiment; necessary supported
permission changes are included only under the selection contract. No replay of
uncertain publication/inference; no provider-case submission; no infrastructure
workaround.
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
writers or remove Git locks. Only the original DevOps loop deploys. Formal
integration validation remains with the original End-to-End Test Loop; scripted
decision observations during planning are neither that gate nor cloud-pass.
Before any coupled lab change,
Scrum Master assigns Git reconciliation and establishes the authorized feature
branch only when safe for existing writers; do not switch the currently dirty
lab checkout underneath them.

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
provider information or out-of-scope authority can stop earlier. Unresolved
path selection alone must not halt remaining artifact generation or be
misreported as a missing user approval. A provider-only
exit must account for both authorized paths and specify the exact-pair
caller-resolution trace/documented remedy
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

## Verification of this release-plan revision

Documentation/index only; no runtime, dependency, deployment, permission or lab
source changes. Using the existing pinned lab Python 3.12.10 environment by
absolute path, without installing dependencies:

- `Test-Demo.ps1 -Python <absolute-validated-python> -LabRepositoryRoot
  <explicit-lab-root>` passed dependency checking, **177 offline tests in
  19.140 seconds**, and compilation.
- `scripts/Test-Repository.ps1 -Python <absolute-validated-python>` passed
  index, public-boundary (**70 public files**), JSON/PowerShell/frontmatter
  parsing and whitespace checks.

An initial invocation mistakenly selected the installed system Python 3.12.10
instead of the pinned lab environment. Its dependency check passed, but unittest
discovery ran 44 tests with six import/dependency errors (7.582 seconds);
compilation was not reached. Existing pinned lab Python was then located and
its relevant SDK versions checked before the successful full run above. No
source fix or dependency installation was used to hide that failed invocation.

No retained lab source changed, so its full release suite was not rerun.
No Linux hosting-package check, fresh cloud/rollback inventory, identity
discriminator, permission change, publication or live acceptance was performed.
The Product Owner accepts this plan for original review; Stakeholder,
Architect, Designer and Critic agreement on this commit remains to be recorded.
Accepted upstream architecture/UX votes are not substituted for these votes.
