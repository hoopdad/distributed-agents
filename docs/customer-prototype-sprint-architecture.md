# RP-S1 sprint architecture: prove continuity without changing the runtime model

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
