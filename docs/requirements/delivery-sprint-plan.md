# Sprint 1 dispatch plan

Scrum Master refinement of the approved release's `three-role-delivery` sprint,
not a scope amendment. Authority: [delivery mission](delivery-mission.md)
D1-D7/F1-F4. Inputs: [release plan](delivery-release-plan.json),
[sprint architecture](delivery-sprint-architecture.json) and
[sprint design](delivery-sprint-design.json). The generated
[dispatch contract](delivery-sprint-plan.json) preserves all six tasks, owners,
dependencies, doneWhen, exclusions and handoffs. Regenerate deterministically with
`python scripts/build_sprint_plan.py`; this does not dispatch or deploy anything.

## Contract-first tasks and ready waves

| Task | Owner | Prerequisites | Implementation / review / integration (minutes) |
|---|---|---|---|
| `azd-walking-skeleton` | DevOps Engineer | None | 60 / 15 / 30 |
| `coordinator-blob-contract` | Developer | Accepted skeleton | 60 / 15 / 30 |
| `remote-specialist-revision` | Developer | Accepted skeleton | 60 / 15 / 30 |
| `terminal-evidence-surface` | Developer | Accepted skeleton | 40 / 10 / 30 |
| `continuity-recovery-isolation` | Developer | Accepted coordinator/Blob and remote specialists | 60 / 15 / 45 |
| `integrated-terminal-acceptance` | DevOps Engineer | All four construction tasks accepted | 20 / 15 / 45 |

The first task is `walkingSkeleton:true`, DevOps-owned and dependency-free.
Only it is initially ready. After its deployed acceptance, the three independent
construction tasks fan out concurrently. Continuity waits for its two real
prerequisites, not for terminal presentation. No task has been executed or
accepted by this planning turn. No UI or Designer construction is added:
the existing terminal design supplies direction; the approved Developer task
implements/verifies that surface. Empty UI/Designer assignment lists are intentional.

Critical path: skeleton -> coordinator/Blob (tied with remote specialists) ->
continuity/recovery/isolation -> integrated terminal acceptance: **410 minutes**
as a rough DAG lower bound. Summed effort is 595 minutes. Estimates include
local work, review and deployment integration; they are not caps, deadlines,
new concurrency limits or acceptance criteria. Shared verification queue time
can lengthen elapsed duration. Critical-path priority must not block another
ready authorized task.

## Dispatch and continuous verification

The existing SprintPlanLoop callback resolves the committed JSON and submits
all six tasks to the existing dependency scheduler, which starts ready work and
fans out independent construction. Return dispatch-ready assignments to that
callback; do not launch a nested workflow or duplicate specialist delivery agents.
The local scheduler test executes this exact graph with synthetic callbacks,
proving actual concurrent dispatch in the test, not implementation execution.
The live workflow callback's dispatch receipt arrives after this owner returns.

Construction hands off local command/exit/result evidence and the **exact
committed revision or immutable artifact**, synthetic inputs and source/test
joins from sprint architecture. Developer construction does not mutate the
shared environment. DevOpsWorkLoop then EndToEndTestLoop hold both
`existing-nonproduction-project-deployment-and-verification` and
`existing-nonproduction-project-deployment-configuration` across deployment
and E2E for each candidate, before original assignment review and dependency
release. These resources serialize mutable cloud state, not source-file overlap.
Keep local construction unblocked while another candidate is verifying.

The skeleton must replace/test incompatible normal-azd predeploy hooks, emit an
actual `azd deploy` command/exit and a **separate deployed probe** for exact
candidate, three bindings, observed versions and operation outcome. No
preapproved ZIP/hash/private approval receipt is required for this path;
unused legacy release safeguards remain untouched. Final integration deploys
the exact combined candidate, not an unrelated mutable checkout.

Failed deployed verification never accepts an assignment or releases dependents.
Localize current blockers; continue independent ready work. Preserve unknown
effects without resend or clearing state. Known-response retrieval is not resend.
No infrastructure/RBAC/network/DNS/quota/VM power, secret retrieval, private lab
edits, principal substitution, fourth role, weakened authorization or push.
Supported hosted-session stop/resume is not hard-crash proof.
The trusted-lab account-wide Blob Contributor limitation remains:
ownership is application-enforced, not storage-enforced per-role isolation.

## Git integration and bounded handoff

Scrum Master owns Git reconciliation through the existing SprintReview,
SprintRetro and ReleaseCloseout, not a new approval stage. Use
`feature/azd-demo-delivery`; construction supplies exact commits. Inspect
concurrent/staged paths, commit only owned paths and never switch a shared
checkout underneath other workers. Every task's code must reach this feature
branch or remain on a named retained branch with task, commit IDs and concrete
abandonment reason recorded in a feature-branch commit message. Do not discard
abandoned code or treat chat as the durable record.

Planning completion means executable plan/dependency/dispatch checks pass and
every task is assigned. It does not mean implementation or deployed acceptance.
Original Product Owner, Architect and Critic reviewers verify this planning
handoff; implementation uses existing DevOps/E2E and original review loops.
No newly invented tests, ledgers or optional suggestions expand user scope.

## Component status at planning

Source inspected: `3df446cd4468822c32dfe755451a3c4f7155caf4`.
Environment: intended existing validated nonproduction dev-lab; not contacted.
No runtime/run version or deployment result is asserted.

| Component | RAG | Evidence (revision/run/environment + freshness) | Remaining work/next action |
|---|---|---|---|
| deployment | 🔴 | Current azure.yaml still calls package_guard.py for all roles; D1/F1 source mismatch, no deployment attempted | DevOps replaces/tests hooks, deploys/probes skeleton |
| coordinator-routing | 🟠 | Planning checks only; deployed routing not executed | Verify trusted gates and genuine Decision-1 |
| architect | 🟠 | Exact-input revision work assigned, remote execution unverified | Verify real findings-driven immutable revision |
| reviewer | 🟠 | Exact-candidate review assigned, remote review unverified | Verify findings and current revised-candidate approval |
| blob-shared-context | 🟠 | Private MI/provenance work assigned, live exchange unverified | Verify exchange and fenced publication |
| session-continuity-recovery-isolation | 🟠 | Follow-up/recovery/isolation scenarios assigned, not executed | Verify retained bindings, supported stop/resume and isolation |
| terminal-demo | 🟠 | Existing terminal UX mapped; live demonstration unverified | Run remote revision and same-parent follow-up |
