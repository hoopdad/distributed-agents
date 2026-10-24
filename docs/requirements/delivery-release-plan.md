# Three-role release plan

## Authority and planning boundary

This ReleasePlan covers mission D1-D7/F1-F4, not new product scope. Its executable
artifact is [delivery-release-plan.json](delivery-release-plan.json). Inputs are
the accepted Architecture at `5757a3a` and UserExperience at `830fd60`, their
contracts, and the current mission. Initial source is
`830fd60e1578682e154052e0280ea1d1664d8db3` on `feature/azd-demo-delivery`;
the initial worktree was clean. No runtime launch or deployment occurs in this
planning loop. A planning schema pass is not deployed acceptance.

One scope-based sprint, `three-role-delivery`, delivers the authorized journeys.
This is not a sprint/time/spend cap. Partial sprints count against any explicit
user-configured cap; none is invented here. Scrum Master owns contract-first
task decomposition, critical-path scheduling and Git reconciliation. The task
entries are release-level seeds for SprintPlan, not a bypass of that role.
Existing source is verified and only demonstrated gaps are remediated; the plan
does not require rewriting already working code.

## Goal, order and genuine prerequisites

Sprint goal: deploy early, then prove the real remote revision and continuity
journeys on exactly coordinator, architect and reviewer in the existing validated
nonproduction dev-lab project.

1. **`azd-walking-skeleton` — DevOps Engineer, dependency-free, first.**
   Replace the incompatible normal-azd predeploy ZIP/hash/receipt requirement
   with supported source exclusions, dependency/build checks. Preserve unused
   legacy lab safeguards. Deploy the committed skeleton using **`azd deploy`**;
   provide actual command/exit evidence plus a **separate deployed probe** for
   the exact candidate, observed role versions/bindings and operation outcome.
   Configuration/packaging health is an early milestone, not proof of D2-D7.
2. **After skeleton deployed acceptance**, construct independent
   `coordinator-blob-contract` (D2/D5), `remote-specialist-revision` (D3/D4) and
   `terminal-evidence-surface` (D7) candidates concurrently where file ownership
   permits. Their separate construction needs no task-to-task dependency.
   Each still requires exact-candidate deployed verification before acceptance.
3. **`continuity-recovery-isolation` (D6)** follows accepted coordinator/Blob and
   specialist contracts, which supply the real context, child and effect state
   whose retention/isolation it verifies. It does not depend on human rendering.
4. **`integrated-terminal-acceptance` (D1-D7)** joins all accepted candidates and
   fresh synthetic journeys. Existing final review/retro/closeout reconcile Git
   and evidence; no extra approval stage is added.

Critical path is skeleton → the slower of coordinator/Blob and specialist
contracts → continuity/recovery/isolation → integrated acceptance. Terminal
surface work runs beside the middle path. All first-sprint tasks transitively
depend on the skeleton. A failed prerequisite is not waived by local tests.
Localize a failure to its observed operation/criterion and continue genuinely
independent approved work without releasing blocked dependents.

## Acceptance coverage

The JSON acceptance criteria are the release contract:

| Requirement | Required fresh outcome |
|---|---|
| D1 | Early skeleton and final integrated revision deployed via normal azd; exact-candidate command and probe evidence |
| D2 | Trusted deterministic MAF gates/write-ahead effects, then actual validated Decision-1 semantic choices |
| D3 | Remote first design and actual-findings-driven changed immutable candidate |
| D4 | Real first findings and review of the exact revised candidate; current blocker-free approval |
| D5 | Private MI Blob exchange of exact refs, immutable provenance and fenced coordinator publication |
| D6 | Same parent, retained independent children/history, stale-ref invalidation, known-response/checkpoint no-resend recovery, supported stop/resume and isolated second parent |
| D7 | Fresh terminal revision flow and same-parent follow-up exposing genuine artifacts/decisions and truthful component RAG |

Architecture flow IDs remain `exact-candidate-delivery`,
`design-review-revision`, `followup-and-recovery`, and
`independent-parent-isolation`. No new component/flow vocabulary is introduced.
Synthetic scenarios must yield real findings and a changed design, not scripted
model approvals. Follow-up retains earlier private ingress while adding a queue.
Known-response retrieval is not resend; uncertain effects remain holds.
Hosted-session stop/resume preserves volume and is not VM power or hard-crash
proof. The account-wide Blob Contributor exception means application-enforced
ownership, not storage-enforced per-role isolation.

## Exact-candidate verification and handoff

Construction owners supply passing local checks and an exact committed revision
or immutable artifact; they do not mutate the shared environment.
**DevOpsWorkLoop then EndToEndTestLoop run after each candidate**, before its
original assignment review, acceptance or dependent release. They hold
`existing-nonproduction-project-deployment-and-verification` across deployment
and E2E, plus the declared configuration resource when mutating shared settings.
Deploy that exact integrated candidate, never a mutable unrelated checkout.
Report actual command, exit code, candidate/run, observed environment/versions
and nonempty repository-relative sanitized results. Raw private evidence stays
private; public logs must not expose credentials or full private session refs.

All assignment doneWhen conditions require a deployed pass. Planning checks
only prove the plan's contracts. The skeleton owner must actually execute
`azd deploy` and a separate deployed probe; writing those words is not execution.
No `azd up/provision` is authorized under this existing-services invocation.
Before later workflow launches the execution owner follows current framework,
inactive-upgrade and registration checks in the mission; this plan does not
launch or replace the currently active delivery runtime.

Material contract/dependency/scope changes return through existing roles only.
Unchanged denials and uncertain effects are not replayed. No blanket stop from
history, principal substitution, infrastructure/RBAC/network mutation, private
lab edits, invented limits, disposition ledger or new approval ceremony.
Scrum Master assigns Git reconciliation in SprintPlan: intended work lands on
the feature branch, or remains on a named retained branch with task/commit IDs
and abandonment reason recorded in a feature-branch commit at existing
SprintReview/SprintRetro/ReleaseCloseout. No push.

## Current component status (planning source; no live checks)

| Component | RAG | Evidence (revision/run/environment + freshness) | Remaining work/next action |
|---|---|---|---|
| deployment | 🔴 RED | Current `830fd60` azure.yaml invokes package_guard.py on all three roles; guard requires approved hash/receipt; no deployed attempt here | DevOps replace/test hooks, deploy skeleton and exact-candidate probe |
| coordinator-routing | 🟠 AMBER | Plan/architecture only; fresh deployed gates NOT VERIFIED | Verify trusted gates and genuine Decision-1 |
| architect | 🟠 AMBER | Remote first/revised design acceptance planned; not executed | Verify actual findings-driven revision |
| reviewer | 🟠 AMBER | Exact revised-candidate review planned; not executed | Verify initial findings and current approval |
| blob-shared-context | 🟠 AMBER | Private MI/fenced provenance acceptance planned; not executed | Probe real exchange and exact bindings |
| session-continuity-recovery-isolation | 🟠 AMBER | Follow-up/recovery/isolation planned; not executed | Verify known-response/checkpoints, stop/resume and isolated parent |
| terminal-demo | 🟠 AMBER | Existing terminal direction mapped; fresh demo not executed | Run actual remote revision and same-parent follow-up |

Release claim requires fresh D1-D7 on the exact final candidate. Until then,
report accepted work, remaining criteria and the precise next action.
