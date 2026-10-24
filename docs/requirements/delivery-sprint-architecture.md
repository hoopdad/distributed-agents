# Sprint architecture: three-role delivery

## Bounded refinement and authority

This is the SprintArchitecture output for `three-role-delivery`, grounded in
[delivery-mission.md](delivery-mission.md) D1-D7/F1-F4 and the current-state
amendment. It is architecture-contract completion, not deployed acceptance.
No product scope, dependency, permission, API, transport or SDK pin changes.
The [contract](delivery-sprint-architecture.json) joins the approved
[release plan](delivery-release-plan.json) and
[sprint terminal design](delivery-sprint-design.json).
There are no completed prior sprints to merge or prior blocked decisions to
carry forward from the supplied current packet. Historical diagnoses are not
reintroduced as prerequisites.

The holistic [Architecture solutionModel](delivery-architecture.json#/solutionModel)
remains authoritative: seven stable components, four flows and thirteen steps.
The sprint contract references that model rather than copying/renaming it.
All existing components and flows are retained. Tier designs partition ownership
of the technical design, not deployments or new services:

| Tier design | Main components | Approved criteria |
|---|---|---|
| [Client and release](client-release/delivery-sprint-architecture.md) | Existing-project azd delivery; Synthetic terminal acceptance surface | D1, D7 |
| [Coordinator](coordinator/delivery-sprint-architecture.md) | MAF coordinator and gated routing; Parent-bound continuity and safe recovery | D2, D6 |
| [Specialists](specialists/delivery-sprint-architecture.md) | Remote design and revision agent; Remote exact-candidate review agent | D3, D4 |
| [Shared artifacts](shared-artifacts/delivery-sprint-architecture.md) | Private shared artifact plane | D5 |

## Current evidence and decisions

Source inspected: `87ad50c0405ceb5384eb71da1cc153123b16f69b` on
`feature/azd-demo-delivery`, initially clean. Current `azure.yaml` has three
`python3 package_guard.py` predeploy hooks; `package_guard.main()` requires
`DEMO_APPROVED_PACKAGE_SHA256`, `TMPDIR` and `DEMO_PACKAGE_RECEIPT`.
This reproduces a source-contract mismatch with D1/F1, not an attempted cloud
deployment failure. It is localized to `deployment`,
`exact-candidate-delivery/select-and-check`. DevOps owns the already approved
replacement, not an authorization bypass. The extension's actual supported
packaging behavior must be verified during that task; this design does not
invent a hook or exclusion API.

Current source already contains MAF `begin/route/execute/publish`, exact-ref
assignment readers, specialist history recovery, private Blob validation,
immutable outputs and manifest fencing. These are source-present, not newly
runtime-tested or deployed by this architecture turn. No current operation
establishes an end-user propagation failure or a need to change transport.
No major host change is selected. A future demonstrated incompatibility would
be localized and handled through existing scoped requirements/replan roles.

### Cross-tier contract and flow

1. `design-review-revision`: terminal authenticates the parent; coordinator
   derives trusted scope, appends immutable requirements and validates gates.
   Decision-1 chooses only among permitted semantic alternatives. Coordinator
   records intent and pinned child/assignment before a remote effect.
2. Architect reads exact assigned requirements and prior design/review, if
   present. Reviewer reads exact requirements/candidate. Actual findings cause
   a changed immutable design and a new exact-candidate review. Coordinator
   validates producer, hashes, revisions and prerequisites before fenced
   publication; only current approval without blockers permits advisory finish.
3. `followup-and-recovery`: completed same-parent follow-up invalidates stale
   refs but retains independent child bindings and model history. Conversations,
   native checkpoints and write-ahead Blob effects are different state planes.
   Known-response retrieval does not send again; unknown effects stay held.
   Supported hosted-session stop/resume preserves volume, not hard-crash proof.
4. `independent-parent-isolation`: separate trusted parent means separate
   namespace, prerequisites and children. A string ID/model document grants no
   access. Capture evidence must establish no cross-parent context/artifacts.
5. `exact-candidate-delivery`: construct/check an exact committed candidate;
   DevOps deploys it and E2E verifies those same versions before original review,
   assignment acceptance or dependency release. No local result substitutes.

## Sprint joins and handoff

The contract's six `taskBindings` connect every approved task's canonical
components/flows/steps to actual modules, existing test targets, construction
focus and evidence handoff. They do not replace Scrum Master's task contract:
dependencies, doneWhen and exclusions remain in the approved release plan.

The dependency-free DevOps walking skeleton comes first; all other tasks
transitively depend on its deployed pass. Coordinator/Blob, remote revision and
terminal work remain independent branches of that graph after the skeleton.
Continuity retains its coordinator/specialist prerequisites. Final integration
retains all four construction dependencies. Localized failures do not justify
new dependencies or stop independent approved construction, and never release
dependents on offline evidence.

Construction emits local checks and exact commit/artifact only. DevOpsWorkLoop
then EndToEndTestLoop hold both
`existing-nonproduction-project-deployment-and-verification` and
`existing-nonproduction-project-deployment-configuration` across candidate
deployment and verification. Record actual azd command/exit, separate deployed
probe, source/artifact-to-role-version bindings, environment and durable outcome.
Scrum Master retains Git reconciliation at existing sprint review/retro and
release closeout; no extra approval stage.

No provisioning, RBAC/network/DNS/quota, VM power, secret retrieval, VPN/private
lab edits, principal substitution, fourth role, local production specialists,
unknown replay, journal/database editing or Git push. Legacy lab release tools
remain intact. Existing account-wide Blob Contributor grants provide
application-enforced ownership, not storage-enforced per-role isolation.

## Executable completion and product limits

Run `python tests/test_delivery_sprint_architecture.py --evidence
docs/requirements/checks/delivery-sprint-architecture.txt`. The suite validates
schema/reference integrity, original mission/solution model/task joins, all
tiers/flows/criteria, exact-candidate locks and negative mutations. It also runs
the existing architecture, UX, release-plan and sprint-design contract suites.
The runner records normalized input hashes, UTC, source revision, Python,
actual test output, elapsed seconds and exit code. These are architecture-only
checks, not remote execution or proof that mapped application tests passed.

Fresh deployment, authentication, runtime/run outcome and hosted versions were
not observed. Runtime regressions and all deployed assignment criteria remain
with their existing construction and DevOps/E2E owners.

| Component | RAG | Evidence/freshness | Remaining work/next action |
|---|---|---|---|
| deployment | 🔴 | Current `87ad50c` descriptor/guard source mismatch, no deployment attempted | DevOps replace/test hooks, deploy/probe the skeleton |
| coordinator-routing | 🟠 | Current graph/gate source inspected; architecture checks only | Verify genuine gated Decision-1 and exact-current finish |
| architect | 🟠 | Exact-input/history source inspected; no fresh remote run | Real findings-driven changed immutable design |
| reviewer | 🟠 | Exact candidate/requirements reader inspected; no fresh remote run | Initial findings and exact revised-candidate approval |
| blob-shared-context | 🟠 | Private-path/immutable/fenced source mapped; deployed exchange unverified | Verify actual private MI exchange and provenance |
| session-continuity-recovery-isolation | 🟠 | Existing state-plane and scenario paths mapped; no live scenarios | Verify follow-up, known recovery, scoped stop/resume and isolation |
| terminal-demo | 🟠 | Accepted terminal design inherited; no fresh demonstration | Exercise remote revision and same-parent follow-up |
