# RP-S1 sprint architecture: prove continuity without changing the runtime model

## Scope, accepted baseline and cumulative design

This is the `SprintArchitecture` handoff for **RP-S1**, not an implementation,
SprintPlan, deployment or live acceptance result. The customer outcome remains
a hosted coordinator repeatedly calling remote architect and reviewer agents,
preserving each specialist's session within the same parent conversation.
Exactly three hosted deployments remain.

Accepted inputs are retained, not reopened:

- [Release architecture](customer-prototype-architecture.md), `2a736d94cb99c01aca0c516aeaf920e61ddb8fbd`.
- [UX](customer-prototype-ux.md), `3ee9798afa4a419be87bcb68fdfc3540875d171a`.
- [Release plan](customer-prototype-release-plan.md), `b0d73b07247bbadbbab9afa9a1bb85b8fa32d480`.
- [Sprint design](customer-prototype-sprint-design.md), `46a1b50f336bb37dd1109dd062e0e654dc30ff0b`.

This revision inspected clean application baseline `46a1b50` on
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

- `["yaml-loops-v1:ArchitectureLoop","architecture-loop-status-reconciliation"]`
  retains accepted full-release architecture and unresolved identity handoff.
- `["yaml-loops-v1:UserExperienceLoop","ux-loop-status-reconciliation"]`
  retains accepted UX; no redispatch of integrated presentation work.
- `["yaml-loops-v1:ReleasePlanLoop","release-plan-loop-status-reconciliation"]`
  retains accepted release planning and original downstream owners.
- `["yaml-loops-v1:sprint/1/RP-S1/SprintDesignLoop","sprint-design-loop-status-reconciliation"]`
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
`WorkflowRuntime.resources()` shares project/headers with routing; isolate
specialist delegation where needed so parent/model/history/checkpoint authority
cannot change accidentally. If trusted namespace compatibility requires a new
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

### Verification of this documentation revision

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

Architect handoff is this cumulative sprint design, navigable tier contracts
and concrete unresolved-blocker disposition, committed for original Product
Owner, Critic and Red Team review. Reviewer agreement is collected by the
existing loop, not asserted here. No runtime repair or live certification is
part of this handoff. Five consecutive rounds without reviewer-verified new
progress stop blocked; productive rounds remain uncapped.
