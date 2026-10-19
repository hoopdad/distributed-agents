# RP-S1 sprint architecture: prove continuity without changing the runtime model

## Scope, accepted baseline and cumulative design

This is the `SprintArchitecture` handoff for **RP-S1**, not an implementation,
SprintPlan, deployment or live acceptance result. The customer outcome remains
a hosted coordinator repeatedly calling remote architect and reviewer agents,
preserving each specialist's session within the same parent conversation.
Exactly three hosted deployments remain.

Accepted inputs are retained, not reopened:

- [Release architecture](customer-prototype-architecture.md), `1f690f5011bef61494b8181fd14e779fa55d858e`.
- [UX](customer-prototype-ux.md), `0f2a2b22a23fdb614e666274eec29c612da0a92f`.
- [Release plan](customer-prototype-release-plan.md), `a2d0f9a06bfa9fd6df7fd932c94491eccb87035d`.
- [Sprint design](customer-prototype-sprint-design.md), `4c8511d374c16219fccb93a722d10e9fb1245f50`.

No completed prior sprints, assigned task IDs, prior dispositions or reconciled
feedback were supplied. The cumulative design is the accepted release
architecture plus this RP-S1 refinement; there is no prior sprint implementation
to certify. The existing [design](design.md), [migration boundary](migration-plan.md),
[implementation workflow](implementation-workflow.md) and
[recovery plan](identity-recovery-plan.md) remain applicable.

The tier documents below are derived architecture contracts, not a replacement
requirements source or new services. `docs/requirements` did not exist at this
handoff's baseline. These logical tier names describe existing ownership:

| Logical tier | Architecture file | Existing code responsibility |
|---|---|---|
| Coordinator | [coordinator](requirements/coordinator/architecture.md) | Parent-scoped bindings, workflow, artifacts and fenced acceptance |
| Specialists | [specialists](requirements/specialists/architecture.md) | Both remote roles' own model history and immutable proposals |
| Client and release boundary | [client-release](requirements/client-release/architecture.md) | Terminal projection and retained exact-release/live verification |

The supplied October 19 customer specification remains authoritative. Do not
copy private delivery inputs, evidence or settings into these directories.
Older accepted documents' statements that this directory did not exist describe
their baseline, not a prohibition on the tier-specific output required here.

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

The current follow-up regression in `tests/test_workflow.py` invalidates
candidate/review refs, checks turn 2, compares children before the follow-up,
and checks two creates and the architect hosted ID after it. It does not yet
assert every final role/framework/version binding or every invocation response.
RP-S1 closes those specific observation gaps through the actual workflow.
This is source inspection, not a failing execution or completed test change.

`RemoteAgents.invoke()` already restores `AgentSession.from_dict(child.framework)`;
`recover()` advances its service continuation from the exact retrieved response.
Both real specialist files already load `specialist_history_v2` / `"history"`
and pass the restored session to their model stage. Architecture does not infer
that these source paths prove hosted or model continuation: RP-S1 must observe
their actual arguments and persistence with controlled offline boundaries.

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

RP-S1 has independent offline proof, clarity, and fresh-inventory/remedy-assessment
boundaries. Neither tests nor README work waits for a provider answer.
DevOps freshly inventories target versions/packages/identities through retained
tools after sole-target private-settings/context validation. Architect/Developer
assess public supported contracts against installed pins and the exact observed
boundary. A research handoff records source/date/version applicability, supported
correction plus reproducer if established, or the precise absent finding.
Repeating old negative research without new evidence is not progress.

If server-side resolution is still the missing evidence, the actionable exit is
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

Only original DevOps owns packaging/publication/live testing. Serialize actual
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
| AC6 | Implement accepted first-screen README and opt-in terminal contract, then real demonstration later |
| AC7 | Integrated targeted/application/repository checks now; exact Linux/amd64/hosting-Python package gate remains DevOps |
| AC8 | Review/integrate intended source, preserve unrelated dirt, commit then reviewed scoped push; no private artifacts in Git |
| AC9 / G8 | Later report actual demo/setup, sanitized proof, final/rollback bindings, cleanup and limitations; no success from this document |

Required source checks use existing validated Python by absolute path:
`Test-Demo.ps1 -Python <absolute-path> -LabRepositoryRoot <explicit-root>` and
`scripts/Test-Repository.ps1 -Python <absolute-path>`. Retained suite follows lab
tool changes. Revalidate final changed source/package, not historical counts.
No dependency install without manifest change or missing-tool failure.

Architect handoff is this cumulative sprint design, navigable tier contracts
and concrete unresolved-blocker disposition, committed for original Product
Owner, Critic and Red Team review. Reviewer agreement is collected by the
existing loop, not asserted here. No runtime repair or live certification is
part of this handoff. Five consecutive rounds without reviewer-verified new
progress stop blocked; productive rounds remain uncapped.
