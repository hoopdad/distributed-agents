# Cumulative sprint architecture: RP-S1/RP-S2 preparation and RP-S3 delivery

## Current RP-S1 recovery-entry architecture (October 20, 2026)

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
