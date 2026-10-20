# Customer hosted-session prototype: release plan

## Current ownership-designation release plan (October 20, 2026)

This is the current Product Owner planning overlay. It consumes agreed
[Architecture](customer-prototype-architecture.md) commit
`f72b0f3c1206418f08fc62a149e80f7c12c55e81` and agreed
[UserExperience](customer-prototype-ux.md) commit
`87253d3f5003d1d6f34724401b33c3b5ced2e64a`, the clean application baseline
inspected for this turn on `feature/customer-hosted-session-prototype`.
Requirements remain the supplied customer specification and the derived
[coordinator](requirements/coordinator/architecture.md),
[specialist](requirements/specialists/architecture.md) and
[client/release](requirements/client-release/architecture.md) contracts.

Apply exact prior references
`["yaml-loops-v1:ArchitectureLoop","architecture-close-agreed-deliverable"]`
and `["yaml-loops-v1:UserExperienceLoop","ux-close-agreed-deliverable"]`
only to their originating accepted deliverables. Do not reopen them, rerun
their experiments or borrow their votes for ReleasePlan agreement.
The retained three sprint IDs, detailed acceptance criteria, exclusions and
handoffs below remain binding. Older status snapshots and missing-locator
statements are historical where the accepted recovery-entry architecture now
supplies evidence and explicit coordination designations; neither that evidence
nor this plan closes stopped tasks. Current coordination below supersedes older
missing-designation requests only, not their substantive acceptance criteria.
No runtime, identity, schema, UX or release-acceptance change is made here.

### Recovery delta and bounded closing work

The accepted architecture supplies historical recovery-summary/trust receipt
locators, the dated canonical/sibling resolver matrix and the current user's
explicit writer/integration-owner designations. This planning
turn consumes that handoff without independently authenticating private
receipts or repeating resolver tests. Historical receipt availability is
progress in recovery preparation, not current SSH trust, exclusive writing
ownership, authenticated inventory, successful ingress or final deployment.
Identity selection remains unresolved; installed B is only a candidate.
Fresh application Git inspection here found clean HEAD at the accepted UX
commit on the authorized feature branch. Architecture reports the canonical
lab's six modified and two untracked paths and a tool-denied direct sibling
inspection; these are supplied observations, not fresh verification here.
No lab Git/sibling ownership inspection or mutation is repeated for this
planning deliverable.

The user's `ownershipRecoveryDefaults` is explicit in-run coordination
evidence, not a missing human decision. Consume it together with the supplied
recovery evidence for `RP-S2-LAB-OWNERSHIP`:

- Developer is the tooling writer for `RP-S2-DECISION-RUNNER`, only in the
  registered feature sibling, never the dirty canonical lab checkout.
  The exact eight-path allowlist is retained in
  [accepted architecture](customer-prototype-architecture.md#current-ownership-designation-architecture-october-20-2026):
  `identity_decision.py`, `Invoke-IdentityDecision.ps1`,
  `tests/test_release_identity_decision.py`, `Test-PrivateConnectivity.ps1`,
  `observe_agent.py`, `release_roots.py`, `Release-Roots.ps1` under
  `foundry-tf/multi-agent/`, plus `.github/repo-index.md`.
- Developer is integration owner for `RP-S2-SOURCE-INTEGRATE` in application
  and lab. Scrum retains decomposition, critical-path planning, reconciliation
  assignment and exclusive-resource coordination; it consumes this designation
  rather than asking the user to designate an owner again.
- Supplied writer acknowledgements preserve canonical dirty/staged paths,
  task-owned writes, explicit path ownership and `git commit --only`; forbid
  shared branch switching, force-push, destructive cleanup and ownership
  inferred from registration/clean status.

Original ownership review still checks actual current checkout/path
coordination and preservation evidence before runner writes. If the supplied
acknowledgements/designations were the only missing input, present them to the
original reviewers now; do not restart a missing-user-approval loop. A remaining
tool-denied observation gets its exact existing-owner closing action, not a
claim of safe writing or an invented need for expanded product authority.
Older work-package wording about another writable arrangement does not expand
this designation: any necessary new writable location or changed root guard
returns to existing Architect-advised PO/Scrum scope reconciliation before use.

Use the provided recovery-exception locator first through the existing bounded
read-only mechanism. Current user approval already covers bounded read-only
Git/sibling-resolver inspection: do not request new product permission for it.
Keep exact private locators in the workflow/private handoff, never customer Git.
Preserve the stopped ownership assignment under exact historical reference
`["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-LAB-OWNERSHIP/AssignedWorkDeveloperLoop","lab-ownership-review-evidence-access"]`.
New evidence is reconciled by its original owners/reviewers, not silently
converted into accepted writing authority or a reset of the five-round stop.

| Existing boundary / priority | Original owner and doneWhen | Exclusions and handoff |
|---|---|---|
| P0: writing ownership | Developer/Scrum presents supplied designations, acknowledgements and recovery evidence to the original ownership reviewers, closes any concrete current checkout/path verification gap, and obtains originating acceptance before runner writes | No repeated designation request, worktree recreation, write probe, shared branch switch or registration-as-exclusivity claim; supply actual owned paths and preservation inventory to runner/integration |
| P0: transport and inventory | Transport owner/DevOps consumes historical receipts, substantiates the already approved module/source and fingerprint, verifies current exact hashes and strict trust, then performs fresh sole-target authenticated Metadata inventory | No replacement trust, credential scan or inferred grant; hand off exact private deployed/rollback/package/identity/caller/action/held-owner observations; inventory is independent of runner coding |
| P1: deterministic runner | Developer implements the retained runner after verified writing ownership, using the accepted matched wrapper/root boundary and existing finite-trial contract; offline root-mismatch, scenario/source mismatch, partial-role, preparation/receiver, unknown and zero-send controls pass | Canonical wrappers run only with their canonical operational root; sibling wrapper changes are not installed canonical changes. No bypass of owner guards, automatic fallback, second ledger or cloud effect |
| P1: reviewed integration | Designated Developer for RP-S2-SOURCE-INTEGRATE joins reviewed application/runner/required operational-wrapper revisions, checks drift and retained regressions, accounts for every task commit, and prepares scoped feature-branch delivery under Scrum reconciliation | Consume accepted candidate, history/continuity, presentation and assertion work without redispatch. A missing required operational-wrapper revision blocks execution; record retained branch/task/commit/reason durably for abandoned code |
| P1: exact execution | Original E2E validates joined source through local repository scripts. Original DevOps joins fresh inventory with exact-source/Linux/package gates, then guarded publication, finite ingress decision and final G1-G4 initial collaboration | An agreed predeployment E2E FAIL is not readiness. Architect trusted ingress/receiver success precedes reviewer. Scoped necessary permission plan/write/readback is included only when evidenced; no uncertain-effect replay |
| P2: customer outcome | Original DevOps proves two-turn continuity, once-only supported recovery and independent separate-parent isolation, then exact-source handoff; PO evaluates all release criteria in existing review/closeout | No hard-crash/exactly-once claim, alias-as-proof, public private identifiers or cleanup claim for historical unknowns |

These are release work boundaries, not replacement task assignments. Scrum
Master owns contract-first decomposition, unique task IDs/kinds/owners,
minimal `dependsOn`, file ownership, actual `exclusiveResources` and Git
reconciliation in the existing SprintPlan. No new approval stage is added.

### Retained sprint goals and acceptance checkpoints

| Sprint ID | Goal and required acceptance | Handoff |
|---|---|---|
| RP-S1 | Evidence-ready source and understandable continuity: retain both-role two-turn bindings/pins, exactly two creations, fresh responses/current requirements and stale-approval invalidation; controlled four-call revision and direct model-history/fresh-history/no-resend fixtures (offline AC3); README/terminal and unchanged machine parser; applicable source checks; supported decision baseline or actionable unresolved record | Consume accepted source/fixtures/UX and recovery evidence; carry only concrete unmet preparation work into RP-S2. Local completion does not establish live AC1/AC2 |
| RP-S2 | Supported repair and exact three-role collaboration: verified writing ownership, reviewed matched-root runner/integration, fresh context/inventory, supported A or B decision, exact reviewed source/settings/stage/ZIP and Linux/amd64/hosting-Python checks; three healthy roles on one final common bundle with rollback retained; live remote current-artifact acceptance, private managed-identity Blob provenance and genuine Decision-1/final gates (AC1, AC5/G1-G4, release portion of AC7) | Completed non-held initial parent plus actual private source/package/version/rollback/identity/effect evidence to RP-S3; held trial parents remain separate |
| RP-S3 | Live continuity, recovery, isolation and customer delivery: same parent/both child hosted/framework bindings and pins across queue follow-up with fresh responses/current outputs/no extra child creation (AC2/G5); once-only confirmed supported stop and same-conversation checkpoint/effect/no-duplicate continuation (AC4/G6); distinct separate parent/children/scope/content exclusion (AC4/G7); truthful readable demonstration (AC6), final exact checks (AC7), reviewed scoped push/task accounting (AC8), reproducible command/final-rollback/new-owned-cleanup/limitations report (AC9/G8) | Customer-ready only with every AC1-AC9/G1-G8 satisfied; otherwise exact unmet criteria and closing owner/action, without relabeling blocked as PASS |

No sprint is newly declared accepted by this table. Detailed sprint contracts
below supply the remaining doneWhen/exclusions. Productive repair sprints and
rounds have no total cap; five consecutive rounds without reviewer-verified
new progress stop as blocked. Continue remaining artifacts when authentication
selection is unresolved. A bounded negative research task can finish without
satisfying RP-S2's live goal or release acceptance.

### Minimal edges, execution ownership and release decision

```text
supplied designations + recovery evidence + current coordination
  -> original ownership acceptance -> Developer runner -> reviewed source integration
accepted application handoffs --------> reviewed source integration
reviewed source integration -> original E2E joined validation
historical trust handoff -> current strict trust -> fresh DevOps inventory
reviewed source + inventory -> DevOps exact Linux/package/preview/publication
publication + necessary permission readback (only if evidenced) -> finite ingress
selected correction + exact common-bundle/source closure -> actual G1-G4 parent
actual G1-G4 -> same-parent queue follow-up -> once-only supported recovery
actual G1-G4 -> independent separate-parent isolation
recovery + isolation + exact checks/reviewed Git delivery -> release closeout
```

Inventory is not a coding/integration prerequisite. Isolation does not depend
on recovery success. This logical graph does not override installed YAML phase
ordering or dispatch work. Selection is not final acceptance; an unchanged
candidate bundle can be final only if all exact final gates pass, without an
unnecessary second publication. Runtime/package drift invalidates affected
checks and live proof. Required operational wrapper deltas must be reviewed
and present where execution loads them before effects.

Keep all deployment/cloud-pass with original DevOps and formal integration
with original E2E, using local repository scripts, not GitHub Actions. Serialize
`lab-hosted-release`, `lab-private-transport` and `lab-cli-context` for actual
shared publication/profile/mount/transport operations; assign
`application-git-integration` and `lab-git-integration` for actual Git mutation.
Resource names do not supply cross-run OS isolation. Preserve unrelated work,
strict trust, old pinned sessions, rollback assets, held parents, original
UNKNOWN effects and historical cleanup uncertainty.

A remains an evidenced supported authentication/configuration correction;
B must preserve actual trusted receiver principal equality through creation,
send and known-response retrieval. Never use opaque call IDs as user identity,
relax receiver checks, rekey histories or infer permission failure from local
preparation rejection. Both roles must pass trusted ingress before selection;
full artifact/provenance/Decision-1 gates remain separate. Material namespace/
contract/architecture findings return to existing Scrum reconciliation and
Architect-advised PO scope decision, not an invented human approval gate.
Only exact genuinely unavailable human/provider information stops as
needs-input. Provider submission/private disclosure remains unauthorized.

Release evidence must label offline assertions, formal integration, Linux
package checks, bounded decision observations and actual live acceptance
separately. Account-wide Blob Contributor still gives application-enforced
role/parent isolation, not storage-RBAC or malicious-host isolation.
Current deployed/rollback bindings, successful A/B selection, push and live
AC1-AC9 are not established by this planning turn.

### Historical checks for the preceding recovery-entry revision

Using the existing absolute validated canonical-lab Python executable and
explicit lab root, `Test-Demo.ps1` passed dependency checking, **204 offline
tests in 47.059 seconds**, and compilation. No dependencies were installed.
After refreshing the index, `scripts/Test-Repository.ps1` passed index,
**78-public-file** boundary, JSON/PowerShell/context and whitespace checks.
A structural check passed all three unique detailed sprint contracts,
goal/acceptance/exclusion/handoff sections, current upstream references,
relative file links, disposition/root boundaries, independent inventory/
isolation edges and AC1-AC9/G1-G8 coverage.

These are local checks only. No settings import, authenticated inventory,
private receipt inspection, resolver experiment, permission mutation,
publication, inference, Linux hosting-package validation or compute stop
was performed here. No lab source changed, so the retained lab suite was
not rerun. Reviewed scoped push remains with the integration handoff.

Those results belong to the preceding revision, not the current source.
Current ownership-designation checks and reviewer handoff are recorded below;
no historical count certifies this revision.

### Current planning verification and original-review handoff

This revision changes only the release plan and repository navigation.
It retains all three sprint goals, doneWhen, exclusions, handoffs and
AC1-AC9/G1-G8 gates; no new task dispatch, approval stage, runner write,
permission change or cloud operation follows from planning acceptance.
Scrum carries the specific designations into existing task contracts and
original ownership review. Developer reconciles reviewed source and actual
operational roots; original E2E owns formal integrated validation; original
DevOps owns exact Linux/package checks, publication and live acceptance.

Using the existing absolute canonical-lab Python 3.12.10 executable and explicit
lab root, `Test-Demo.ps1` passed dependency checking, **204 offline tests in
45.517 seconds**, and compilation. No dependencies were installed. An initial
existence probe found no executable at the nested multi-agent environment path;
the existing lab-root environment was then located and used, without creating
or changing an environment. After deterministic index refresh,
`scripts/Test-Repository.ps1` passed index, **79-public-file** boundary,
JSON/PowerShell/context and whitespace checks. A structural assertion passed
three unique sprint contracts with goals, doneWhen, exclusions and handoffs,
current upstream references, designation/acceptance boundaries, independent
inventory/isolation edges and current-overlay relative file links.

These checks are local/offline only. No settings import, private receipt
authentication, resolver experiment, current lab inventory, permission mutation,
publication, live inference, Linux hosting-package validation or compute stop
was performed. No lab source changed, so the retained full lab suite was not
rerun. No push or deployed/rollback binding is established here.

The Product Owner accepts this release-plan deliverable for the original
Stakeholder, Architect, Designer and Critic to review. Their current ReleasePlan
agreement is not supplied; accepted Architecture/UX votes are not substitutes.
Until those votes arrive, the concrete remaining loop criterion is original
reviewer agreement, not further architecture research or live delivery.

## RP-S3 retrospective — offline proof and unreached live outcomes

Product Owner retrospective, October 20, 2026. Inputs: SprintReview commit
`12e2a2a5b3c97268d3b9ba8c631ed483c35762df` and its four supplied current
original-reviewer agreements; accepted assertion commits `dcdb5e4` and `552e466`
and their current originating Architect/Critic agreements; agreed RP-S3
prerequisite E2E FAIL; supplied RP-S3 ownership and DevOps needs-input reports
and original reviews. Fresh application inspection found clean HEAD at the
SprintReview commit on the authorized feature branch. No lab verification,
private receipt search or cloud execution was performed for this retrospective.

**Outcome: product blocked, not customer-ready.** The substantive application
advance is reviewed offline comparison coverage and its focused prerequisite
repair, not live collaboration. No completed non-held initial parent, actual
G1-G4 entry, live follow-up, supported recovery or separate-parent isolation is
established. All three sprint contracts below remain unchanged.

### Observations, metric limits and decisions

| Supplied input / observation | Process lesson | Decision within existing ownership |
|---|---|---|
| Original assertion delivery needed the ordered operation/artifact prerequisite repair | Separately valid envelopes and journal entries can still contradict each other | Consume accepted `552e466` and its two internally consistent negative controls without duplicate repair. Preserve legitimate revision and JSON round-trip controls; exercise the intended invariant rather than incidental malformed input. |
| Twelve scenario-evidence tests and 204 full offline tests were reported after repair; reviewers inspected source/fixtures but did not rerun them | Assertion correctness and observation provenance are independent evidence boundaries | Integration consumes both accepted commits and the documented executable/private-input contract, revalidates drift and runs joined checks. Original E2E validates exact joined revisions; DevOps supplies actual private observations and final exact-source/Linux/package evidence. No offline result becomes live PASS. |
| Current SprintReview has four accepting votes; current E2E has three accepting votes for prerequisite FAIL | Completion snapshots must consume current originating agreements, not inherit another loop's votes | Preserve those accepted bounded closures. This retrospective has its own six original reviewers; their current agreement is not supplied by SprintReview or RP-S2 retrospective agreement. No closure-only commit or repeated test is required after agreement. |
| Ownership carryover remains unsubstantiated and DevOps remains before authenticated Metadata inventory | Redispatch and unsuccessful evidence lookup do not cure either independent prerequisite | Developer/Scrum supplies existing bounded ownership/root evidence for original Architect/Critic inspection; transport-owner/Scrum separately supplies the existing private accepted-trust receipt locator to DevOps. Preserve the originating five-round stop and runner-writing block; no unattended probes, checkout recreation or replacement trust. |
| No reviewed runner/source integration or completed initial parent is established | An agreed blocked dependency report does not enable effects | Retain existing runner/integration tasks and formal E2E readiness, then original DevOps package/publication/finite-ingress gates. Actual G1-G4 entry gates continuity and isolation independently; supported recovery also requires completed two-turn proof. Serialize shared execution resources without making isolation depend on recovery success. |

Reported round counts are audit context, not error rates or elapsed delays:
the supplied assertion loop has three rounds, E2E and SprintReview each two,
and DevOps one; the originating ownership stop remains five rounds and is not
reset by later carryovers. Complete communication denominators, delivery latency,
end-to-end elapsed timing, usage totals and current cloud invocation receipts
were not supplied. No numerical improvement rate is inferred. The already
accepted implementation advances are not credited again by this retrospective;
changed prose, repeated checks and agreed failure assessments are not new
implementation or live progress.

### Artifact improvements and preserved dispositions

- [Architecture](customer-prototype-architecture.md#rp-s3-retrospective-assertion-correctness-is-not-observation-provenance):
  preserve exact operation/artifact joins and meaningful negative controls while
  distinguishing supplied-evidence consistency from live provenance.
- [UserExperience](customer-prototype-ux.md#rp-s3-retrospective-separate-assertion-results-from-live-demonstration):
  separate accepted offline assertions, joined readiness and unreached measured
  demonstration without changing accepted screens or machine contracts.
- ReleasePlan: retain the RP-S3 review's prioritized existing-owner closing
  actions below. Scrum Master retains decomposition, critical-path/resource
  coordination and Git reconciliation. No duplicate task, acceptance waiver,
  scope change or approval stage is introduced.

Preserve exact unresolved reference
`["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-LAB-OWNERSHIP/AssignedWorkDeveloperLoop","lab-ownership-review-evidence-access"]`,
including `taskComplete=false`, the originating stop and runner-writing block.
If existing evidence cannot be delivered, retain the evidence/access stop and
originating permitted interactive path, not unattended verification.
Retain accepted
`["yaml-loops-v1:sprint/3/RP-S3/task/RP-S3-EVIDENCE-CHECKS/AssignedWorkDeveloperLoop","rp-s3-evidence-checks-close-agreed-deliverable"]`
and satisfied
`["yaml-loops-v1:sprint/3/RP-S3/task/RP-S3-EVIDENCE-CHECKS/AssignedWorkDeveloperLoop","rp-s3-exact-operation-artifact-prerequisites"]`.
Preserve the completed prerequisite FAIL under
`["yaml-loops-v1:sprint/3/RP-S3/EndToEndTestLoop","rp-s3-e2e-close-agreed-failure-assessment"]`
and blocked backlog closure under
`["yaml-loops-v1:sprint/3/RP-S3/SprintReviewLoop","rp-s3-sprint-review-close-agreed-deliverable"]`.
Neither establishes integration PASS, publication readiness or cloud-pass.
Earlier retrospective and upstream closures remain confined to their original
boundaries. The three unchanged sprint objects remain required under
`["yaml-loops-v1:sprint/1/RP-S1/SprintRetroLoop","sprint-retro-preserve-release-plan-payload"]`.

No task code is abandoned here. Accepted application assertions are retained
in feature history; reviewed lab runner integration, cross-repository
reconciliation, remote freshness and scoped push remain unestablished obligations
of the existing integration owner. No fresh lab branch disposition is claimed.
Preserve unrelated work, historical UNKNOWN effects, held parents, rollback
assets and cleanup uncertainty. Account-wide Blob access provides
application-enforced role/parent isolation, not malicious-host storage isolation.
AC1-AC9/G1-G8 remain mandatory; final release readiness is not established.

The Product Owner accepts this bounded retrospective for current Scrum Master,
Critic, Architect, Red Team, Designer and Developer review. Their current RP-S3
retrospective votes are not yet supplied; other-loop and earlier-sprint votes
are not substitutes. No blocked writing, stopped-probe restart, replacement
trust, speculative grant, provider submission or uncertain-effect replay is
authorized by this document.

## RP-S3 sprint review — offline assertions accepted, live demonstration unreached

Product Owner review, October 20, 2026. Inputs: committed RP-S3 SprintPlan
`2ccef16d055295d036ed176b0b3ba428b8061041`; accepted assertion delivery
`dcdb5e436a6a6bd3a75a0d6f616de96fadffaea9` and prerequisite repair
`552e46695a5a1edecb40112f7c04db9e8916a738`; supplied current originating
Architect/Critic acceptance; agreed RP-S3 prerequisite E2E FAIL; and supplied
RP-S3 DevOps needs-input report and its three original reviews. Fresh application
inspection found clean HEAD at the repair on the authorized feature branch.
No lab ownership verification, private evidence lookup or cloud operation was
performed for this review.

**Demonstration: unreached; product blocked and not customer-ready.** The
accepted implementation adds deterministic cross-scenario comparisons and
synthetic controls, including the exact ordered operation/artifact prerequisite
join. Its reported 204-test checks are offline evidence, not actual remote
collaboration, continuity, supported recovery or separate-parent isolation.
The originating reviewers inspected source/fixtures but did not independently
rerun those checks or inspect execution receipts. This review consumes their
accepted handoff without reopening it or claiming its progress again.

The current DevOps report states no settings import, tests, Linux package
validation, cloud checks, transport startup, publication, inference or compute
stop/resume. Reviewers independently inspected the trust guards and application
revision, not live execution. The existing private accepted-trust receipt was
not delivered; unsuccessful lookup does not establish its absence elsewhere.
Neither a provider defect nor a missing permission is proven. A completed
non-held initial parent and actual G1-G4 entry remain unavailable. Agreement
with bounded blocked reports supplies none of those missing prerequisites.

### Prioritized carryover and closing actions

No duplicate task, new approval stage, scope change or acceptance waiver is
introduced. All three sprint contracts below remain unchanged. Scrum Master
retains decomposition, critical-path/resource coordination and Git reconciliation.

| Priority / boundary | Existing assignment and owner | Concrete closing action |
|---|---|---|
| P0 — Originating ownership/root evidence remains unsubstantiated | `RP-S2-LAB-OWNERSHIP`, Developer with existing Scrum Master coordination | Deliver existing registration, sibling branch/HEAD/status, canonical dirty/staged-work preservation, point-in-time writing ownership and positive/negative resolver evidence for permitted original Architect/Critic inspection. Preserve `taskComplete=false`, the originating five-round stop and runner-writing block until substantiated and accepted. If evidence is unavailable, retain the access stop and originating permitted interactive path; this carryover permits no renewed unattended verification, write probes or checkout recreation. |
| P0 — Established transport trust has not been handed off | `RP-S2-FRESH-INVENTORY`, DevOps with existing transport-owner/Scrum coordination | Supply the existing private receipt locator binding the independently accepted command-VM ED25519 fingerprint, approved owner-module path, module SHA256 and source SHA256, without keys or credentials. Resume retained strict-trust Metadata only after substantiation, with explicit roots, settings-loader validation and private invocation evidence. Obtain fresh deployed/rollback/package/identity, caller/effective-action and held-owner observations; do not derive replacement trust. |
| P1 — Reviewed retained runner and exact joined source are unavailable | `RP-S2-DECISION-RUNNER`, then `RP-S2-SOURCE-INTEGRATE`, Developer | After accepted originating ownership evidence, complete the retained runner and its existing offline fixtures. Consume accepted application preparation and both accepted assertion commits, including their documented executable/private-input contract. Inspect subsequent drift; join reviewed source, run joined checks, account every task commit and verify actual remote freshness/outgoing scope before reviewed scoped push. Do not redispatch accepted candidate/assertion work. Cloud inventory is not a coding prerequisite. |
| P1 — Formal integration and exact release gates remain unmet | Original E2E owner; `RP-S2-INGRESS-TRIAL`, DevOps | Formally validate exact joined revisions. With sufficient fresh inventory, complete actual Linux/amd64/hosting-Python and immutable source/settings/stage/ZIP gates, then retained guarded publication and finite ingress. Join scenario/source/common package/actual three-role versions before parent creation; observe architect trusted ingress before reviewer. Preserve preparation, partial-ingress, observed receiver-rejection and unknown classifications. |
| P1 — Initial collaboration/provenance entry proof is missing | `RP-S2-G1-G4`, DevOps | Verify final three-role healthy common-bundle and rollback bindings, remote accepted artifacts, actual private managed-identity Blob provenance and genuine Decision-1/final gates for a completed non-held initial parent. Do not create another parent or resend to fill reporting gaps. |
| P2 — Live follow-up and readable demonstration are unreached | `RP-S3-TWO-TURN`, DevOps | After actual G1-G4 entry, continue the completed initial parent with the queue requirement. Use reviewed assertions and actual private observations for both roles' hosted/framework bindings, pins, exactly two child creations, fresh invocation responses, current requirements/artifacts and stale-approval invalidation. Measure existing human stderr presentation separately from machine evidence; aliases and memory prose are not proof. |
| P2 — Supported recovery and isolation are unreached | `RP-S3-SUPPORTED-RECOVERY` and `RP-S3-ISOLATION`, DevOps | Recovery requires verified two-turn completion, once-only durable stop intent, confirmed stopped state and same-conversation checkpoint/effect/no-duplicate proof. Isolation independently requires G1-G4 entry, distinct parent/children/artifact scope and content exclusion, not recovery success. Serialize shared execution resources; do not resend stops, remove markers, adopt held parents or infer hard-crash/exactly-once guarantees. |
| P2 — Exact delivery and customer handoff remain incomplete | `RP-S3-DELIVERY`, DevOps; Product Owner retains release decision | Join final exact-source/package checks, actual reviewed scoped push, private exact final/rollback bindings, implemented setup/demo commands, sanitized actual proof and newly owned cleanup accounting. Keep historical UNKNOWN effects and cleanup uncertainty visible. Declare customer-ready only when every AC1-AC9/G1-G8 criterion passes. |

### Acceptance boundary and original-review handoff

AC1/AC2/AC4/AC5 and actual G1-G8 remain unverified or unreached, not passing.
AC3's accepted controlled revision/model-history fixtures remain offline.
AC6's README/terminal implementation is retained, but measured live demonstration
is unreached. AC7 final joined-source/Linux/package validation, AC8 reviewed
cross-repository integration/scoped push, and AC9 exact fresh final/rollback
bindings and verified demonstration remain outstanding. The implemented command
shape remains in [README](../README.md#two-turn-terminal-demonstration); do not
execute follow-up until the initial turn completes without a pending/held effect.
The [private-input assertion contract](design.md#offline-cross-scenario-evidence-assertions)
checks supplied observations; it neither collects nor independently authenticates
them. Account-wide Blob access provides application-enforced role/parent
isolation, not malicious-host storage isolation.

Preserve exact prior reference
`["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-LAB-OWNERSHIP/AssignedWorkDeveloperLoop","lab-ownership-review-evidence-access"]`
as unresolved despite historical outcomeStatus labels. Retain accepted
`["yaml-loops-v1:sprint/3/RP-S3/task/RP-S3-EVIDENCE-CHECKS/AssignedWorkDeveloperLoop","rp-s3-evidence-checks-close-agreed-deliverable"]`
and its satisfied
`["yaml-loops-v1:sprint/3/RP-S3/task/RP-S3-EVIDENCE-CHECKS/AssignedWorkDeveloperLoop","rp-s3-exact-operation-artifact-prerequisites"]`.
The closed assessment under
`["yaml-loops-v1:sprint/3/RP-S3/EndToEndTestLoop","rp-s3-e2e-close-agreed-failure-assessment"]`
remains FAIL, not integration PASS or publication readiness. Earlier SprintReview,
retrospective, candidate, architecture/design and release-plan agreements remain
within their originating boundaries; they do not close this RP-S3 review.

No task code is abandoned by this review. Fresh application inspection confirms
the two accepted assertion commits in feature ancestry; no new lab integration
or remote freshness is asserted. Existing integration retains durable task/
branch/commit accounting and scoped push responsibility. Preserve unrelated
work, held parents, historical UNKNOWN publications, rollback assets and cleanup
uncertainty. No cleanup is certified by this document.

The Product Owner accepts this bounded blocked-backlog assessment for current
RP-S3 Scrum Master, Critic, Architect and Red Team review. Their current
SprintReview votes are not supplied; earlier-sprint or other-loop votes are not
substitutes. This documentation claims no new implementation/live progress and
authorizes no blocked writing, stopped-probe restart, replacement trust,
speculative grant or uncertain-effect replay.

## RP-S2 retrospective — stopped prerequisites and evidence delivery

Product Owner retrospective, October 20, 2026. Inputs: SprintReview commit
`34d545db8bb8f9e795f5da35e6207bf347060e7a` and its four supplied current
original-reviewer agreements; accepted application preparation at `990467a`;
the agreed RP-S2 prerequisite E2E FAIL; supplied RP-S2 ownership and DevOps
needs-input reports and original reviews. Fresh application inspection found
the review commit on the authorized feature branch with a clean worktree.
No lab verification, stopped probe, private-state lookup or cloud execution was
performed for this retrospective.

**Outcome: blocked, not customer-ready.** Accepted source preparation and
accurate failure handoffs are retained; no live identity selection, specialist
ingress, common-bundle acceptance or completed initial parent is established.
All three sprint goals, acceptance criteria and handoffs below remain unchanged.

### Observations, metrics and decisions

| Supplied observation | Process finding | Existing-owner improvement |
|---|---|---|
| Current SprintReview has four accepting original votes; RP-S2 E2E has three accepting votes for a prerequisite FAIL | Reconciled completion must follow the current originating votes, not a stale pending-vote snapshot or an earlier sprint's agreement | Existing owner/Scrum coordination consumes those agreements once. No closure-only commit, repeated test or extra approval stage is needed. These votes do not approve this RP-S2 retrospective. |
| The evidence-only ownership carryover remains `taskComplete=false`, with no substantiating locator supplied | Redispatch and empty history searches did not close the originating setup criterion | Developer/Scrum delivers existing bounded registration, sibling branch/HEAD/status, canonical preservation, point-in-time writing ownership and positive/negative resolver evidence to original Architect/Critic reviewers. Preserve the five-round stop and runner-writing block; if evidence is unavailable, retain the access stop and originating permitted interactive path, not unattended probes. |
| DevOps reports no current settings import, tests, cloud checks or transport startup; reviewers inspected trust guards | A missing established trust handoff is not a current remote receiver failure or provider diagnosis | Existing transport-owner/Scrum coordination supplies the private accepted-fingerprint/owner-module-path/module-and-source-SHA256 receipt locator, without keys or credentials. DevOps then resumes retained strict-trust Metadata with explicit roots and private invocation evidence. Do not regenerate trust. |
| Independent application preparation is accepted at `990467a`; the reported outgoing audit uses local refs, with no upstream configured | Source review progressed independently, but does not establish server freshness or reviewed lab integration | Existing integration owner consumes this handoff after reviewed runner completion, checks later drift, verifies remote freshness/outgoing scope and performs the assigned reviewed scoped push. Inventory remains independent of coding. |
| No accepted runner/source integration, exact Linux/package gates or G1-G4 evidence is supplied | Agreement on bounded stop assessments does not satisfy encompassing cloud-pass | Preserve original formal E2E and DevOps ownership. Join exact reviewed source, scenario, common package and actual three-role versions before trial-parent creation; do not create another parent or resend to fill reporting gaps. |

These are supplied observations, not newly measured execution metrics. The
originating ownership stop is five rounds; its RP-S2 evidence-only carryover
does not reset that counter. The supplied RP-S2 review and E2E each show two
rounds; counts alone are not error rates, elapsed delays or additional progress.
No complete communication denominator, delivery latency, end-to-end timing,
usage total or current cloud invocation receipts were supplied. Repeated
offline checks, changed prose and this retrospective earn no substantive
implementation/live progress credit.

### Artifact improvements and exact disposition boundaries

- [Architecture](customer-prototype-architecture.md#rp-s2-retrospective-evidence-joins-remain-independent):
  distinguish accepted independent application preparation, ownership/root
  evidence, established transport trust and the reviewed-source/release joins.
  Keep existing identity, session, provenance and unknown-effect contracts.
- [UserExperience](customer-prototype-ux.md#rp-s2-retrospective-report-the-boundary-not-an-implied-retry):
  report observed/unreached boundaries, evidence attribution and existing
  closing owner/action without implying an authorized retry, exposing private
  locators or adding a public presentation requirement.
- ReleasePlan: retain the prioritized existing-owner actions in the RP-S2
  review above. Scrum Master retains dependencies, shared-resource
  serialization and Git reconciliation; no duplicate task or gate is added.

Apply exact reference
`["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-LAB-OWNERSHIP/AssignedWorkDeveloperLoop","lab-ownership-review-evidence-access"]`
as unresolved within its setup boundary despite historical status labels.
Preserve the closed prerequisite FAIL under
`["yaml-loops-v1:sprint/2/RP-S2/EndToEndTestLoop","rp-s2-e2e-close-agreed-failure-assessment"]`
and closed blocked backlog assessment under
`["yaml-loops-v1:sprint/2/RP-S2/SprintReviewLoop","rp-s2-sprint-review-close-agreed-deliverable"]`.
Accepted candidate, RP-S1 retrospective and upstream architecture/UX/planning
closures remain confined to their originating deliverables; no inherited vote
closes this RP-S2 retrospective. The repaired three-sprint payload required by
`["yaml-loops-v1:sprint/1/RP-S1/SprintRetroLoop","sprint-retro-preserve-release-plan-payload"]`
remains preserved, without reopening that accepted retrospective.

No task code is abandoned here. Existing application source-accounting findings
are supplied evidence; fresh lab integration or branch accounting is not
claimed. Existing integration retains durable reconciliation and scoped-push
responsibility. Preserve historical UNKNOWN publications, held parents, rollback
assets, unrelated work and cleanup uncertainty. Account-wide Blob access means
application-enforced role/parent isolation, not malicious-host storage isolation.
AC1-AC9/G1-G8 remain binding; RP-S3 live continuity, supported recovery, isolation
and final delivery still require their actual upstream initial-parent handoff.

The Product Owner accepts this bounded retrospective for the original Scrum
Master, Critic, Architect, Red Team, Designer and Developer reviews. Current
RP-S2 retrospective votes are not yet supplied. No new scope authority,
deployment, provider submission or stopped-operation resumption is requested.

## RP-S2 sprint review — prerequisites stopped, live gates unmet

Product Owner review, October 20, 2026. Inputs: committed RP-S2 SprintPlan
`990467afd3e03efdf55aa236ee56ecc1bd04de66`, supplied current application
handoff and original reviews, agreed RP-S2 predeployment E2E FAIL, and supplied
RP-S2 DevOps needs-input report and its three original reviews. Fresh application
inspection found that HEAD on `feature/customer-hosted-session-prototype` with
a clean worktree. No lab checkout verification or private-state search was
performed for this review.

**Demonstration: blocked, not customer-ready.** No current workstation-to-cloud
demonstration, publication, specialist ingress or completed non-held initial
parent is established by these inputs. The DevOps owner explicitly reports no
settings import, tests, cloud checks or transport startup this turn. Its
reviewers inspected the retained trust boundary, not a cloud execution receipt.
The earlier RP-S1 ARM execution claim is historical, not new RP-S2 inventory.
Empty history searches do not prove that existing receipts are absent elsewhere.
Neither a provider defect nor a missing permission is established.

### Prioritized backlog disposition within existing assignments

These findings retain existing tasks rather than adding duplicate work or
changing sprint acceptance. Scrum Master retains coordination, dependencies,
shared-resource serialization and Git reconciliation.

| Priority / boundary | Existing assignment and owner | Concrete closing action |
|---|---|---|
| P0 — Originating ownership/root handoff remains unsubstantiated | `RP-S2-LAB-OWNERSHIP`, Developer with Scrum Master coordination | Deliver existing registration, sibling branch/HEAD/status, canonical dirty/staged-work preservation, point-in-time writing ownership and positive/negative root-resolution evidence for permitted original Architect/Critic inspection. Preserve the originating five-round stop and `taskComplete=false`; this evidence-only carryover permits no renewed unattended probes, write probes or checkout recreation. If existing evidence cannot be supplied, retain the access stop and use only the originating permitted interactive verification path when execution access is available. Runner writing remains blocked until substantiated and accepted. |
| P0 — Established transport trust has not been handed off | `RP-S2-FRESH-INVENTORY`, DevOps Engineer with existing transport-owner/Scrum coordination | Supply the exact existing private receipt locator binding the independently accepted command-VM ED25519 fingerprint, approved transport-owner module path, module SHA256 and source SHA256. Do not send keys/credentials or derive replacement trust. DevOps then resumes retained strict-trust Metadata with explicit roots and private invocation evidence, obtaining current/rollback/package/identity, caller/effective-action and held-owner observations. |
| P1 — Runner and reviewed joined source are unavailable | `RP-S2-DECISION-RUNNER`, then `RP-S2-SOURCE-INTEGRATE`, Developer | After accepted ownership evidence, implement the retained runner and its accepted root/ownership/mismatch/partial-role/unknown/redaction/zero-send fixtures. Consume the accepted application preparation at `990467a`, revalidate subsequent drift, join reviewed commits and run affected joined checks. Verify remote freshness and outgoing scope before reviewed scoped push; the application handoff's 27-ahead/21-path audit used local tracking refs and found no configured upstream. Cloud inventory is not a coding prerequisite. |
| P1 — Formal joined-source and release prerequisites remain unmet | Original E2E owner, then `RP-S2-INGRESS-TRIAL`, DevOps Engineer | Formally validate exact joined revisions; complete actual Linux/amd64/hosting-Python and immutable source/settings/stage/ZIP gates. With sufficiently complete inventory, use the retained guarded publisher and finite runner. Join scenario/source/common package/actual three-role versions before parent creation; observe architect trusted ingress before reviewer. Preparation rejection, partial ingress, receiver rejection and unknown outcomes remain distinct. |
| P1 — Actual G1-G4 proof is missing | `RP-S2-G1-G4`, DevOps Engineer | Consume final exact three-role healthy common-bundle/rollback bindings and a completed non-held initial parent; verify remote accepted artifacts, private managed-identity Blob provenance and genuine Decision-1/final gates. Do not create another parent or resend merely to complete reporting. Identity selection alone is not G1-G4 acceptance. |
| P2 — Live continuity and customer delivery remain downstream | Existing RP-S3 E2E/DevOps owners | Only after the required initial-parent handoff, prove two-turn bindings/versions and fresh responses, once-only supported compute stop/resume without duplicate effects, separate-parent isolation, measured terminal clarity and final AC1-AC9/G1-G8 delivery. Do not continue a held parent. |

The current original Architect/Critic reviews accept the bounded application
preparation; its earlier owner snapshot's pending votes are historical. That
handoff does not establish runner integration or fresh remote branch state.
Likewise, the current DevOps reviews agree with the precise bounded inventory,
unexecuted-trial and G1-G4 stop reports but explicitly withhold encompassing
cloud-pass completion. Those assessments need not wait for product success;
their agreement does not supply missing live proof.

Apply these exact prior references without reopening their originating work:

- `["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-LAB-OWNERSHIP/AssignedWorkDeveloperLoop","lab-ownership-review-evidence-access"]`
  remains unresolved despite historical status labels; its stop is not reset.
- `["yaml-loops-v1:sprint/2/RP-S2/EndToEndTestLoop","rp-s2-e2e-close-agreed-failure-assessment"]`
  closes the accurate prerequisite FAIL, not integration PASS or publication readiness.
- `["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-ISOLATED-CLIENT/AssignedWorkDeveloperLoop","isolated-client-close-agreed-handoff"]`
  retains accepted candidate review without duplicate implementation or live selection.
- `["yaml-loops-v1:ReleasePlanLoop","release-plan-close-agreed-deliverable"]`
  preserves all three sprint contracts. Accepted design, architecture and
  retrospective closures remain confined to their own deliverables.

### Acceptance and original-review handoff

AC1/AC2/AC4/AC5 and G1-G8 live proof remain unmet or unreached. AC3 fixtures
and AC6 README/terminal implementation are retained offline/source evidence;
measured live presentation is unverified. AC7 final joined-source/Linux/package
checks, AC8 cross-repository integration/reviewed scoped push, and AC9 exact
final/rollback bindings, successful reproducible demonstration and owned-cleanup
handoff remain outstanding. Account-wide Blob access still means application-
enforced role/parent isolation, not malicious-host storage isolation.

No criterion, contract, architecture or authority is changed. Preserve historical
UNKNOWN publications, held parents, rollback assets, unrelated dirty work and
cleanup uncertainty. No new code branch is abandoned by this review; source
integration and durable task accounting remain assigned to the existing owner.
The Product Owner accepts this blocked backlog assessment for current RP-S2
Scrum Master, Critic, Architect and Red Team review. Those current SprintReview
votes are not yet supplied; RP-S1 votes do not close RP-S2. This documentation
records no implementation/live progress and authorizes no automatic resumption,
cloud operation, speculative grant or uncertain-effect replay.

## RP-S1 retrospective — evidence handoffs and truthful closure

Product Owner retrospective, October 20, 2026. Inputs are the committed sprint
review `db446a7269354474ecb3b83736cfd2f3752cac84`, supplied original-reviewer
reports, agreed predeployment E2E FAIL, DevOps needs-input outcome and stopped
lab-ownership assignment. Fresh application inspection found that review commit
on `feature/customer-hosted-session-prototype` with a clean worktree.
No stopped ownership probe, private evidence search or cloud operation was
restarted for this retrospective.

**Outcome:** retain the customer goal and all AC1-AC9/G1-G8 gates. Working
hosted collaboration has not been delivered. The useful retained outcomes are
reviewed candidate/continuity/presentation source and accurate bounded failure
handoffs, not a live identity-path decision or customer-ready release.

### Observations and metric limitations

| Supplied evidence | Workflow-quality finding | Decision |
|---|---|---|
| Architecture, UX, ReleasePlan, SprintDesign, SprintArchitecture, isolated-client and E2E records each show two rounds and a stale completion report corrected after original votes arrived | Agreement collection and owner status reconciliation caused avoidable closure churn; these rounds are not new implementation progress | Existing owner/Scrum coordination should consume collected votes once, preserving their exact task boundary. Do not create another commit or rerun tests solely to acknowledge agreement. |
| Lab ownership stopped after five rounds with no reviewer-verified new progress; read-only access was denied and coordination delivery failed | An attempted message is not delivered evidence; owner-reported setup is not an accepted writing handoff | Preserve the stop and `taskComplete=false`. Existing Developer/Scrum coordination supplies bounded evidence for permitted original-reviewer inspection; runner writing stays blocked. |
| DevOps reports `HOST_TRUST_EVIDENCE_REQUIRED`, exit 2; reviewers inspected the script but not this invocation's receipt | ARM readiness, authenticated SSH readiness and hosted inference are different observation boundaries | Obtain the existing accepted private trust/transport-owner receipt locator, then resume retained Metadata inventory with strict trust and private execution provenance. Do not regenerate trust or retrieve keys. |
| SprintReview at `db446a7` has four supplied original votes, all `agree=true`, `taskComplete=true`, no unmet review criteria | The bounded blocked-review output is accepted even though the product is not ready | Carry forward that agreement without another review-only commit or reopening the E2E FAIL; DevOps cloud-pass remains unmet. These votes do not approve this retrospective. |
| SprintReview reports 192 offline tests in 18.753 seconds and repository checks | Repeated local checks protect source but do not advance the missing integration/package/live evidence | Keep revision-bound results attributed. Do not count repeated tests, changed prose or this retrospective as new substantive progress. |

The first row's counts describe supplied loop records, not a measured error
rate or elapsed delay. No complete execution/communication event denominator,
token/cost total, cloud invocation receipt or end-to-end timing was supplied.
Do not infer latency, delivery reliability, a provider defect or a permission
failure from these observations. The recorded five-round stop belongs to the
ownership assignment; a new retrospective round does not reset it.

### Improvements within existing artifacts and assignments

These decisions change process guidance, not architecture, contracts, sprint
acceptance, dependencies or execution authority. They add no approval stage,
public evidence ledger, CLI controls or work package.

| Artifact / accountable owner | Improvement and existing closing action | Verification boundary |
|---|---|---|
| [Architecture](customer-prototype-architecture.md#rp-s1-retrospective-evidence-boundary), Architect; Developer/Scrum execute existing ownership and integration tasks | Separate source-contract acceptance from operational readiness. Make the existing ownership/root evidence consumable by the original reviewers before runner writing; retain the scenario/source/package/version join before trial creation. | Original ownership review substantiates registration, exact branch/HEAD/status, canonical preservation, writing ownership and positive/negative resolver evidence. No architecture reapproval or repeated write probe is required. |
| [UserExperience](customer-prototype-ux.md#rp-s1-retrospective-blocked-handoff-language), Designer; DevOps supplies measured results | Keep one truthful blocked status with reached/unreached boundary, evidence attribution, existing owner and closing action. Do not fabricate terminal role rows, publish a nonexistent runner command or require customer identity controls. | Existing human/machine output fixtures remain retained; measured live presentation is still downstream, not established by a wireframe. |
| ReleasePlan, Product Owner; Scrum Master coordinates existing tasks | Preserve two independent P0 handoffs: ownership/root evidence before coding, accepted transport trust before inventory. Then runner -> source integration -> original E2E and DevOps exact-package/live gates. Coding does not wait for cloud inventory. | Original task reviewers accept the respective bounded handoffs. Integration owns scoped source accounting/push; DevOps alone owns guarded publication/cloud-pass. No automatic resumption is authorized by this document. |

Keep what worked: exactly three roles; isolated specialist authority and
unchanged receiver equality; explicit local/remote/unknown classifications;
machine-readable contracts; independent coding/inventory lanes; scoped Git
commits and retained unknown-effect holds. Do not duplicate accepted candidate,
continuity or presentation work.

Apply these exact prior references only within their originating boundaries:

- `["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-LAB-OWNERSHIP/AssignedWorkDeveloperLoop","lab-ownership-review-evidence-access"]`
  remains unresolved; report agreement is not setup completion.
- `["yaml-loops-v1:sprint/1/RP-S1/EndToEndTestLoop","e2e-close-agreed-failure-assessment"]`
  remains closed as an accurate FAIL, not integration PASS.
- `["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-ISOLATED-CLIENT/AssignedWorkDeveloperLoop","isolated-client-close-agreed-handoff"]`
  remains closed; no duplicate implementation.
- `["yaml-loops-v1:ArchitectureLoop","architecture-close-agreed-deliverable"]`,
  `["yaml-loops-v1:UserExperienceLoop","ux-close-agreed-deliverable"]`,
  `["yaml-loops-v1:ReleasePlanLoop","release-plan-close-agreed-deliverable"]`,
  `["yaml-loops-v1:sprint/1/RP-S1/SprintDesignLoop","sprint-design-close-agreed-deliverable"]`
  and `["yaml-loops-v1:sprint/1/RP-S1/SprintArchitectureLoop","sprint-architecture-close-agreed-deliverable"]`
  remain accepted upstream outputs, not waivers of downstream failures.

No material scope decision supersedes those dispositions. Preserve UNKNOWN
publications, held parents, rollback assets, unrelated dirty work and historical
cleanup uncertainty. Nothing here certifies current final/rollback versions,
Linux package validity, effective permissions, specialist ingress or cleanup.
No task branch is abandoned or source integration claimed by this documentation.

The Product Owner accepts this retrospective for original Scrum Master, Critic,
Architect, Red Team, Designer and Developer review in SprintRetroLoop.
Their independent retrospective agreements are not yet supplied; upstream
votes and acceptance of the blocked SprintReview do not satisfy this loop's
own agreement condition. Do not hold the bounded retrospective open awaiting
eventual deployment success once its own original reviewers agree.

Validation of this documentation-only delta: `Test-Demo.ps1` using the existing
absolute validated Python and explicit lab root passed dependency checks,
192 offline tests in 20.471 seconds and compilation.
`scripts/Test-Repository.ps1` passed index, 74-public-file boundary, parser and
whitespace checks. A local link/anchor check passed all four links in the new
retrospective sections and balanced fences in the three documents. No
dependencies were installed, lab source changed or Linux package/live check
performed. These repeated checks are not substantive new progress.

## RP-S1 sprint review — blocked workstation-to-cloud demonstration

Sprint review input: the accepted SprintPlan at
`2f6e6601231b5f80b33abed5ab7b3786804b52c8`, accepted candidate
`3aca5dc236695c5ec7eac98d0cd03bced40da7b8`, agreed predeployment E2E
FAIL assessment and supplied DevOps needs-input report. Application Git
inspection for this review found that same HEAD, a clean worktree and the
authorized `feature/customer-hosted-session-prototype` branch. The reports
below are supplied execution/review evidence, not independently repeated
cloud observations.

**Demonstration outcome: blocked, not customer-ready.** No workstation-to-cloud
two-turn demonstration, current-candidate specialist ingress or final common
bundle was established. The installed B candidate is not a live-selected path;
A has no evidenced corrected source. Neither a provider defect nor a missing
permission has been demonstrated. Historical receiver failures are not fresh
failures of this candidate.

The E2E assessment is complete as an accurate predeployment FAIL under
`["yaml-loops-v1:sprint/1/RP-S1/EndToEndTestLoop","e2e-close-agreed-failure-assessment"]`.
Its reported 192 offline tests and repository checks apply to the stated
source, not a final Linux hosting package or live collaboration. The supplied
DevOps report says settings/linkage and ARM prerequisite checks reached
`HOST_TRUST_EVIDENCE_REQUIRED` (exit 2), before authenticated SSH metadata,
publication or inference. Its reviewers inspected the script boundary but
did not inspect an invocation receipt; fresh ARM execution therefore remains
owner-reported, not independently verified.

### Prioritized findings retained in the release backlog

These are closing actions within existing assignments, not duplicate tasks,
new acceptance stages or changed architecture. Scrum Master retains assignment,
dependency/resource serialization and Git reconciliation ownership.

| Priority / finding | Existing owner and task | Closing action and inspectable handoff |
|---|---|---|
| P0 — Stopped lab ownership/root handoff | Developer with Scrum Master coordination; `RP-S2-LAB-OWNERSHIP` | Deliver existing bounded registration, exact branch/HEAD/status, canonical dirty-work preservation, point-in-time writing ownership and positive/negative resolver evidence for permitted original Architect/Critic inspection; alternatively resume ordinary read-only verification when execution access is available. Preserve the five-round stop and keep runner writing blocked until substantiated and accepted. |
| P0 — Missing established transport-trust handoff | DevOps Engineer; `RP-S1-FRESH-INVENTORY` | Obtain the exact existing private accepted-fingerprint/transport-owner receipt locator through existing coordination. Resume retained Metadata inventory under strict trust, recording a private execution-evidence locator, fresh current/rollback bindings, effective permissions and held effects. Do not retrieve keys, regenerate trust or infer independent trust from a newly observed key. |
| P1 — Reviewed finite runner and joined source missing | Developer; `RP-S2-DECISION-RUNNER`, then `RP-S2-SOURCE-INTEGRATE` | After the ownership handoff, finish the existing runner, mismatch/zero-create-send, ownership, redaction and recovery fixtures; join reviewed application/lab commits, run joined checks and report scoped push outcomes. Do not make coding depend on cloud inventory or reimplement the accepted candidate. |
| P1 — Package/publication/ingress prerequisites unmet | DevOps Engineer; `RP-S2-INGRESS-TRIAL` | After reviewed integration and fresh inventory, validate exact source and actual Linux/amd64/hosting-Python package, use the guarded publication chain and finite trial, and distinguish preparation rejection, observed receiver failure and unknown outcomes. Select neither A nor B without the required actual ingress proof. |
| P2 — Customer demonstration and final acceptance not reached | Existing RP-S2/RP-S3 E2E and DevOps owners | Retain G1-G4 remote collaboration/provenance gates followed by two-turn continuity, once-only supported stop/resume, isolation, final exact release checks and truthful handoff. Do not run recovery against a held parent or substitute offline results for live proof. |

The ownership action applies exact prior reference
`["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-LAB-OWNERSHIP/AssignedWorkDeveloperLoop","lab-ownership-review-evidence-access"]`.
That assignment remains owner-reported complete with review blocked,
`taskComplete=false`; agree-with-report votes do not establish setup completion.
No stopped denied probes, write probes, checkout recreation or settings changes
are requested by this review. This is missing execution access/evidence, not a
request for expanded product authority.

The partial-inventory and unresolved-status reports are actionable bounded
handoffs for `RP-S1-FRESH-INVENTORY` and `RP-S1-STATUS-HANDOFF`; they need not
wait for eventual live success. They do not complete the encompassing DevOps
cloud-pass condition. Neither role was reached by inference in the supplied
DevOps turn. No private current/final/rollback binding locator was supplied to
this review, so none is certified here.

### Acceptance and scope disposition

- AC1, AC2, AC4 and AC5 / G1-G8: live proof remains unmet or not reached.
- AC3: retained controlled revision/continuation fixtures are offline evidence,
  not a new live result or a request to duplicate accepted implementation.
- AC6: accepted README/terminal work is retained; measured live presentation
  remains unverified.
- AC7: historical source checks do not satisfy the final exact Linux/package
  gate; joined tooling checks remain outstanding.
- AC8: local application branch/status was inspected; reviewed cross-repository
  reconciliation and scoped push remain outstanding. Canonical lab dirty work
  was not reinspected or adopted.
- AC9: this is a blocked handoff, not final delivery. Current exact final/
  rollback bindings, reproducible successful live demonstration and final
  owned-cleanup evidence remain outstanding.

The accepted architecture, UX, release plan, SprintDesign and SprintArchitecture
closure dispositions remain confined to their original deliverables. Preserve
the accepted candidate handoff under
`["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-ISOLATED-CLIENT/AssignedWorkDeveloperLoop","isolated-client-close-agreed-handoff"]`.
No criterion is waived, accepted handoff reopened or deferred enhancement
promoted into a blocker. No material contract change is proposed.

This review records the existing stops without restarting them. Preserve all
UNKNOWN publications, held parents, rollback assets, unrelated work and
historical cleanup uncertainty. No cloud operation, publication, inference,
permission change, transport startup, compute stop/resume or cleanup is
performed by this Product Owner review. Its documentation is not substantive
new implementation/live progress. Scrum Master, Critic, Architect and Red Team
agreement for this SprintReviewLoop has not yet been supplied; prior-loop votes
do not close this loop or establish release acceptance.

Local validation of this documentation delta used the existing absolute
validated Python and explicit lab root: `Test-Demo.ps1` passed dependency
checks, 192 offline tests in 18.753 seconds and compilation;
`scripts/Test-Repository.ps1` passed index, 74-public-file boundary, parser and
whitespace checks. No dependency installation or lab source change occurred.
These repeated local checks do not constitute new substantive progress or
final-package/live proof.

## Product outcome and planning authority

Deliver a customer-shareable prototype in which a hosted coordinator repeatedly
calls a remote architect and reviewer, preserving each specialist's session
within the same parent conversation. Exactly three hosted roles remain.
Acceptance requires working remote collaboration, not a plan, mock, HTTP 200,
package upload or completed SDK response.

This Product Owner deliverable implements the Release Plan Loop. The supplied
October 19, 2026 customer specification is the requirements source.
`docs/requirements/{coordinator,specialists,client-release}/architecture.md`
contains derived tier contracts, not replacement requirements.
Do not copy private delivery inputs into Git.
The accepted [architecture](customer-prototype-architecture.md) at
`cde76380c9c41201f19aedf4b290958c95472689` and
[UX contract](customer-prototype-ux.md) at
`c17813567e7d3db09abe1d2403b948c98131c24f` are inputs, not work to reopen.
Apply prior dispositions
`["yaml-loops-v1:ArchitectureLoop","architecture-close-agreed-deliverable"]`
and `["yaml-loops-v1:UserExperienceLoop","ux-close-agreed-deliverable"]`
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
`c17813567e7d3db09abe1d2403b948c98131c24f` on
`feature/customer-hosted-session-prototype`. Related RP-S1 source and clarity
work was already integrated by `24b883f910dedbc8dc524177f29f59e061be265e`;
workflow fixtures `6614440`, specialist continuation fixtures `c454e50` and
terminal view `56b762e` are retained implementation history, not new progress
or fresh live evidence. The original 17-path dirty baseline is historical,
not the current application worktree. The lab still has unrelated dirty/
untracked work; this loop changes neither lab source nor application runtime.
Do not redispatch accepted work simply because a new planning loop begins.
The later identity handoff `13203ac`, reconciled by
`bb1743d85cb10e6520c92efaa42df0702178f57a`, is also retained. Its
`scripts/identity_handoff.py` is offline-only and returns exit 2 / `unresolved`;
it neither installs the runtime candidate nor executes live selection.
The installed isolated B candidate at
`3aca5dc236695c5ec7eac98d0cd03bced40da7b8` is now source history, not a
successfully selected live path. Retain its original review and source-integration
handoff rather than redispatching implementation. The accepted October 20
architecture binds trial labels to actual candidate source and distinguishes
local preparation rejection from observed remote receiver failure.
The phase-compatible SprintPlan at `4f2e02d9b08bc1c5258d6f799e9a9f0809705a81`
assigns safe lab checkout setup, runner coding and source integration to Developer
before E2E; inventory/status and trial execution remain later DevOps work.
Scrum Master reconciles its historical input hashes against these accepted
contracts at the existing planning handoff, without rewriting completed task
acceptance, claiming dispatch or redispatching the offline handoff as a live runner.
No decision-runner implementation commit/entry point has been supplied to this
loop; integration must obtain the actual reviewed handoff rather than invent a command.

Fresh Git inspection found the application clean on the authorized branch.
The lab remains on `feature/swc-think-fast-aca-dns`, with eight pre-existing
dirty/untracked paths. This planning turn edits neither lab files nor branches.
Cloud context, active/rollback bindings and permissions were not inventoried
here; the independent DevOps inventory below remains required.

Priority order:

1. Preserve trusted parent/child identity, exact immutable prerequisites,
   versions, fenced/ETag acceptance, checkpoints and write-ahead effects.
2. Preserve accepted offline continuity/continuation proof and customer clarity;
   retain the installed candidate for review/integration and finish independent
   decision tooling. Inventory has no coding prerequisite, but executes in the
   original later DevOps phase; do not reopen accepted source work.
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
concrete gaps. The integrated offline identity handoff is retained; criterion
6's fresh inventory and live discriminator remain outstanding downstream.
RP-S2 now owns the installed candidate's review/integration and remaining runner
implementation rather than another round of the completed bounded research
assignment. Unresolved selection must not block remaining release/sprint
artifacts, fixtures or documentation.

**Bounded work and handoff**

- Scrum Master inventories dirty/staged work and named branches, assigns Git
  reconciliation, and establishes disjoint contracts/fixtures before writing.
  Review related readability changes, preserve originals and exclude unrelated
  work. Developer integrates only reviewed related source on the feature branch.
- Developer preserves the integrated two-turn, controlled reject/revise/review
  and direct specialist model-history fixtures; repairs only a concrete
  regression exposed by changed source, not duplicate implementation.
- Developer preserves the accepted terminal/README implementation; Designer
  evaluates affected changes against the existing UX contract, not a new web
  experience or redispatched clarity task.
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

**October 20 implementation increment:** retain the installed isolated B
candidate for original review/integration, finish the finite lab-owned decision
runner, then measure trusted ingress in DevOps.
A remains a supported alternative only when a measured cause-specific
authentication/configuration correction exists. Neither path is selected.
This is concrete implementation, not another open-ended remedy investigation.
Do not reopen the accepted architecture or UX handoffs.

The following are bounded release work packages, not assigned SprintPlan tasks.
Scrum Master supplies actual unique task IDs, `kind`, owner, `dependsOn`,
exclusive resources, file ownership and Git reconciliation in the existing
Sprint Planning Loop. In particular, the older SprintPlan's no-runtime/no-lab
exclusions describe that completed assignment, not a ban on these new packages.

| Work package / original owner | doneWhen and inspectable handoff | Exclusions |
|---|---|---|
| Installed isolated candidate / Developer | Retain `3aca5dc` for its original review and integration; close only concrete unmet criteria. Its contract keeps `WorkflowRuntime.resources()`'s original opaque-only tuple for routing/model/parent/history/checkpoints, with a distinct project/copied-header client and separate OpenAI cache only for `WorkflowRemoteAgents`. Full captured `ScopeBinding` revalidation precedes B derivation. Real resource-factory regressions cover both roles, raw SDK and Responses lifecycle paths, non-specialist immutability, cleanup, invalid identities and known-response zero-send recovery. Hand off reviewed runtime/test commits and source checks, not a live selection claim. | No redispatch merely because planning restarts; no production import of the offline script, shared/ambient header mutation, container-user forwarding, opaque-call-ID delegation, dependency/schema/history migration, receiver relaxation, new selector or duplicate UX/continuity implementation. |
| Fresh inventory / DevOps Engineer | In the original later DevOps phase, validate sole-target settings and authenticated dedicated context through retained tools; privately bind exact current/rollback versions, packages, identities, protocol, actual caller/effective explicit action and unresolved effect/owner records. Hand off reached/missing observations and private locators; consume them in the retained RP-S1 status handoff without waiting for trial success. Existing explicit grants are read back before proposing a delta. | Independent of candidate and runner coding; no assumed missing grant, inference, publication, adoption of dirty lab work or historical cleanup claim. |
| Safe lab writing ownership / Developer, assigned by Scrum Master | Establish a verified isolated writable checkout on `feature/customer-hosted-session-prototype`, or another safe ownership arrangement reconciled by Scrum, before runner writes. Hand off actual root/branch/base/owned paths and preserved dirty-path inventory. The existing plan records a branch ref but an execution-denied worktree attempt; do not claim that attempt created a usable checkout. | No switching the shared dirty lab checkout, adopting its eight unrelated paths, removing locks or requesting product permission already granted. An actual setup failure is an execution finding with its exact closing action. |
| Decision tooling / Developer | After safe lab ownership, implement the retained local runner against the accepted architecture table: explicit absolute roots/Python/scenario/reviewed source/package/versions/private destination; joined inventory at execution; finite pre-journaled architect-then-reviewer sequence; trusted receiver observations; exact known-response inspection without resend; held/unknown/version-drift stops; selected/unresolved result, unreached roles, permissions and owned cleanup. Offline fixtures prove scenario/source mismatch rejects before parent creation, preparation rejection is not remote failure, competing ownership/unknown holds, zero-send recovery, partial-role results and redaction. Affected retained suite passes; reviewed tool commits hand off to integration before E2E. | No dependency on later DevOps inventory for coding, invented command, second ledger, unprotected endpoint, automatic path switch, infinite probe, inference from mocks or publication/transport bypass. Original DevOps still executes the runner live. |
| Git/source integration / Developer, assigned by Scrum Master | Reconcile reviewed application and affected lab task commits on `feature/customer-hosted-session-prototype`, or record task/named retained branch/commit IDs/abandonment reason in a feature-branch commit message. Recheck exact joined source and retained regressions. Give DevOps source/package-input closure; DevOps later joins its fresh private inventory. | No dependence on later inventory for source integration; no shared-checkout branch switch under writers, unrelated staged changes, lost originals, migration reseal or chat-only abandonment accounting. Scrum Master assigns the owner before lab writing. |
| Bounded ingress decision / DevOps Engineer | After integrated review/source/Linux/package gates, inventory and any demonstrated necessary permission readback, use retained preview/publication and the finite runner on one fresh synthetic trial parent. Record `selected-A`, `selected-B` or actionable `unresolved`, actual child receiver/principal compatibility per reached role, exact private bindings, holds and cleanup. Architect-only entry explicitly leaves reviewer unreached. | Not formal E2E or cloud-pass; no held-parent adoption, namespace translation, repeat send for missing receipt, automatic new parent after failure, unchanged A retry or metadata/HTTP-200 success claim. |

The runtime candidate has no new runtime path selector: the named `B-candidate`
trial is bound privately to reviewed `3aca5dc` or its reviewed descendant,
common package and exact three actual deployed versions. `A-correction`
requires a separate evidenced supported correction in reviewed source with its
own regression/package/version closure; the installed unconditional B source
cannot be relabeled A, and historical unchanged A is not a correction.
Reject inconsistent scenario/source/package/actual-version joins before creating
a trial parent, without dispatch. No environment toggle, sealed-stage edit or
shared-checkout switch is an identity selection mechanism.
Missing/invalid captured user, scope mismatch or forbidden headers may reject
local resource preparation before dispatch; they do not establish failed remote
ingress or a denied permission. Only actual child observation classifies a
receiver failure; absent observations remain unknown. Architect-only success
leaves reviewer unreached/unverified, not a completed both-role selection.
Preserve the yielded resource tuple semantics and existing receiver equality,
immutable artifacts, bounded model routing, history and recovery behavior.
Old pinned conversations/versions remain untouched. Move only required pure
candidate logic into application-owned runtime source; keep operational
journaling and deployment tooling lab-owned.

Only a demonstrated necessary permission delta adds a work package/dependency:
DevOps implements reviewed deterministic plan/write/readback for the verified
caller/action/target and smallest supported scope, documenting exact scope and
rationale privately. Prior approval covers that bounded change; no routine
human approval stage is added. An uncertain write remains held and blocks
dependent trial execution, not independent artifact work.

The candidate and runner are not assumed feasible merely because their offline
tests pass. If actual child principal is absent or changes namespace, stop
without weakening `Assignment.validate_receiver()`, rekeying histories or
adopting held state. Scrum reconciles the exact finding into an existing
Architect-advised PO contract/scope decision (`needs-replan`). Genuine required
provider information or authentication is reported as the exact external stop,
not invented missing permission approval. Bounded actionable negative findings
can finish a task while this sprint's live acceptance remains unmet.

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

The accepted architecture/UX, installed candidate and integrated offline
identity contract are available now. Safe lab ownership enables Developer
runner coding; the installed candidate follows its original review handoff.
Do not add edges from later inventory to coding or source integration.
Installed YAML phases place offline implementation/integration before E2E and
all DevOps work later; logical independence is not observed concurrent dispatch.
Fresh inventory/status does not depend on a successful trial. Retained
continuity/terminal source needs regression verification for changed source,
not new implementation.
Integration joins only included code/tool commits; it does not wait on cloud
inventory or unrelated research. The finite live decision waits on both fresh
inventory and exact integrated reviewed source/Linux/package gates. A measured
permission delta adds only its actual dependent edge. Final formal validation
and cloud-pass remain their original gates, even if the decision succeeds.

The live critical chain is:

```text
safe lab writing ownership -> Developer decision runner ------+
installed runtime candidate -> original review --------------+-> source/Git integration
source/Git integration
  -> exact source/Linux/package gates -> fresh preview -> guarded publication
source/Git integration -> original formal E2E handoff (predeployment FAIL permitted)
fresh DevOps inventory ----------------------------------> finite ingress decision
candidate publication ------------------------------------> finite ingress decision
necessary permission delta/readback (only if proven) ------> finite ingress decision
selected supported correction + final common-bundle/source closure
  + original E2E handoff -> DevOps cloud-pass/accepted initial parent
  -> same-parent follow-up -> supported stop/resume -> evidence closeout
final publication -> separate-parent run
initial-parent evidence + separate-parent evidence -> isolation comparison
recovery + isolation comparison + source/Git reconciliation -> final closeout
```

This is a logical edge map, not two deployers or a new approval sequence.
Formal E2E may report predeployment FAIL; DevOps then performs guarded
publication and cloud-pass. Selection alone supplies neither acceptance.
A deliberately published candidate common bundle may become the final bundle
only if unchanged exact source/package/settings/versions satisfy every final
gate; do not demand an otherwise unnecessary second publication. If runtime
or packaging inputs change after the trial, rebuild/review/publish and refresh
affected live proof. Never use a failed/held trial parent as the acceptance
parent; use the explicitly planned final acceptance scope, not a retry escape.

Separate-parent comparison needs initial-parent evidence, not its follow-up or
restart. Independent parents may logically overlap only if retained transport,
admission and ownership permit; default to serialization for actual shared
tools. Architect output precedes exact reviewer consumption and coordinator
acceptance; same-parent turns are serial. No publisher races live acceptance.

Scrum Master assigns actual `exclusiveResources`, including
`application-git-integration`, `lab-hosted-release` (publisher/project/shared CLI
and stage), and `lab-private-transport` (mount/ports/connection owner); use
`lab-cli-context` for inventory's shared authenticated profile and
`lab-git-integration` if lab files change. Inventory takes the actual release/
transport/context resources while observing; offline runner coding needs none
of those live resources. Shared files also require exclusive
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

## Historical verification of the preceding release-plan revision

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

## Historical verification and review handoff: earlier October 20 release delta

Inspected baseline `ef5c79d94114f156ab0d03497fafffd1e348aabf` on
`feature/customer-hosted-session-prototype`. Changes are limited to this
release plan and the repository index. No runtime, dependency, SprintPlan,
accepted architecture/UX or lab source was edited.

Using the existing absolute lab Python 3.12.10 AMD64 executable, verified
against installed MAF core 1.21.0, agentserver Core 2.2.0 and Responses 2.3.0:

- `Test-Demo.ps1 -Python <absolute-validated-python> -LabRepositoryRoot
  <explicit-lab-root>` passed dependency checking, **186 offline tests in
  19.039 seconds**, and compilation. These include the retained Windows
  connectivity-wrapper tests; they are not cloud observations.
- Refreshed `scripts/repo_index.py`; no public paths were added/deleted.
  `scripts/Test-Repository.ps1 -Python <absolute-validated-python>` passed
  index, public-boundary (**73 public files**), JSON/PowerShell/context and
  whitespace checks.
- A local structural/link check passed three unique sprint IDs, each sprint's
  goal/acceptance/exclusions/handoff, AC1-AC9/G1-G8 coverage, the five new
  bounded work-package contracts and all five relative links/anchors.
  Its first invocation used an over-specific literal `conditional` assertion
  absent from the plan wording; correcting the check to the actual permission
  delta contract passed. No acceptance criterion was removed or waived.

No dependencies were installed. No settings import, cloud inventory,
permission readback/write, inference, publication, Linux hosting-package gate,
supported stop/resume, push or live acceptance was performed in this planning
turn. No lab source changed, so the full retained lab suite was not rerun.
Historical UNKNOWN/held work and all unrelated dirty lab paths are preserved.

The Product Owner agrees with this release plan and hands its owned commit to
the original Stakeholder, Architect, Designer and Critic in ReleasePlanLoop.
Their release-plan votes are not yet available; upstream architecture/UX
agreement cannot satisfy this loop's agreement condition. The next action is
review of this committed plan, followed by reconciled correction only for a
concrete unmet release-plan criterion. Subsequent Scrum task decomposition
must use the ready parallel lanes and explicit integration contract above.
Identity-path implementation/selection and all final live release gates remain
downstream obligations, not claims made by this plan.

## Current source-to-trial release handoff and verification

This revision uses accepted architecture `cde7638` and UX `c178135`, preserving
their completed agreement under the exact prior references at the top of this
plan. It aligns the three retained sprint contracts with installed candidate
`3aca5dc` and phase-compatible assignment `4f2e02d`: finish Developer-owned safe
lab setup/runner/source integration; perform inventory/status and the guarded
trial in original DevOps. It adds the accepted scenario/source/package/actual
version join and preparation-versus-receiver outcome requirements to those
work packages. It does not change sprint acceptance, runtime, dependency pins,
machine contracts, architecture/UX, task JSON or lab source.

Fresh application status was clean at `c17813567e7d3db09abe1d2403b948c98131c24f`
on `feature/customer-hosted-session-prototype`; only this plan and its index
are intended edits. The canonical lab remains on its existing branch with
eight pre-existing dirty/untracked paths, untouched. No actual runner checkout,
task dispatch, runner commit or current cloud binding is asserted by this plan.

Using the existing absolute canonical lab virtual-environment Python, confirmed
as CPython 3.12.10 AMD64 with MAF core 1.21.0, agentserver Core 2.2.0 and
Responses 2.3.0, without dependency installation:

- `Test-Demo.ps1 -Python <absolute-validated-python> -LabRepositoryRoot
  <explicit-lab-root>` passed dependency checking, **192 offline tests in
  22.276 seconds**, and compilation. This is local regression evidence only.
- Refreshed the repository index; no paths were added/deleted.
  `scripts/Test-Repository.ps1 -Python <absolute-validated-python>` passed
  index, public-boundary (**74 public files**), parser and whitespace checks.
- An inline structural/link check passed all three unique sprint contracts,
  goals/acceptance/exclusions/handoffs, AC1-AC9/G1-G8 coverage, relative links/
  anchors, current accepted references, Developer runner ownership and the
  source/outcome guards. An initial interpreter metadata probe requested an
  uninstalled distribution name; checking the actual pinned distribution names
  resolved that lookup error without installation or source changes.

No settings import, authentication, cloud inventory, permission mutation,
inference, publication, Linux package validation, stop/resume or live acceptance
was performed. The full retained lab suite was not rerun because lab source
was unchanged. Historical unknowns, held parents and rollback assets remain
preserved. Push awaits the reviewed scoped integration handoff.

The Product Owner agrees with this bounded release plan and submits the owned
commit for Stakeholder, Architect, Designer and Critic review in this existing
ReleasePlanLoop. Their current release-plan agreements have not been supplied;
accepted upstream votes are not substitutes. Only those missing original
reviews or a concrete reconciled correction remain for this planning loop.
Identity selection and AC1-AC9/G1-G8 live acceptance remain downstream, not
reasons to redispatch accepted planning or label the release customer-ready.
