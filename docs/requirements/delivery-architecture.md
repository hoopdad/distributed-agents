# Three-role delivery architecture

## Authority and bounded output

This design implements D1–D7 and F1–F4 in
[delivery-mission.md](delivery-mission.md); it adds no product requirement,
permission or release ceremony. The machine-readable Architecture artifact is
[delivery-architecture.json](delivery-architecture.json), including the stable
`solutionModel`, source/test mappings, state-plane contracts and delivery handoff.
The latest sprint source inspection was `87ad50c0405ceb5384eb71da1cc153123b16f69b` on
`feature/azd-demo-delivery`, with a clean initial worktree. This is an
architecture/schema handoff, not deployed application acceptance.
The [sprint refinement](delivery-sprint-architecture.md) joins this unchanged
solution model to the approved six-task sprint, tier-specific designs and
exact-candidate verification handoffs. There are no completed prior sprints.

## End-to-end technical design

```text
Synthetic terminal -- authenticated stored/background turn --> coordinator
                         MAF: begin -> route -> execute -> publish -> route
                                            |                |
                 gated Decision-1 model <---+                |
                         remote architect <------------------+
                         remote reviewer  <------------------+
                         independent child/model conversations
                                    |
                 private managed-identity Blob shared artifact plane
                 control / candidates / reviews; coordinator fenced manifest
```

The three hosted roles remain `multi-agent-coordinator`,
`multi-agent-architect` and `multi-agent-reviewer`. Decision-1 is a model, not a
fourth hosted service. There is no new web UI or local specialist fallback.
The existing terminal is the user surface. The existing validated private
connectivity, project, aliases and dedicated authentication remain configuration,
not public literals or inferred authority.

### Design, review, revision

The coordinator derives tenant/project/principal/parent from trusted hosting
context, writes immutable requirements, then routes only over permitted actions.
Current `WorkflowRuntime.route()` chooses the prerequisite specialist
deterministically, and asks Decision-1 to choose between that action and
`request_input`; it does **not** delegate authorization or choose an arbitrary
specialist. Calibration confidence/margin can hold a choice. Current approval
finishes deterministically; budgets/deadlines do not constitute success.

Before a remote effect, the coordinator journals intent and binds the child,
assignment and exact accepted refs. The architect reads requirements and, for a
revision, the actual prior design/review. It writes an immutable candidate.
The reviewer reads exact requirements/candidate and writes immutable findings.
Real findings drive an actual changed candidate and a new exact-candidate review.
Only a current approving review without blockers/unresolved requirements permits
accepted advisory output. Coordinator publication validates hashes, revisions,
producer session/version/response and active assignment, then uses lease/ETag
fencing. Specialist output alone is never accepted state.

### Continuity, isolation and recovery

Conversations retain history; MAF checkpoints retain graph position; Blob
artifacts and write-ahead effects retain provenance and accepted work. They are
not interchangeable. A completed same-parent follow-up appends requirements and
invalidates old candidate/review refs while preserving both child bindings and
model histories. A new parent derives a separate namespace and child pair.
Model-supplied IDs or documents do not grant scope.

Known responses are retrieved without resend. Native checkpoints resume only
with compatible pinned versions/state. Ambiguous dispatch/create/stop remains an
explicit hold until supported reconciliation establishes an outcome. Supported
hosted-session compute stop/resume preserves the volume; it proves neither
infrastructure VM recovery nor hard-crash exactly-once behavior.

Managed identity and private-path verification remain mandatory. The existing
account-wide Blob Contributor exception makes ownership application-enforced,
not storage-enforced per-role isolation. No RBAC or network remediation is
selected. If a fresh operation fails genuine end-user propagation, diagnose that
actual boundary first; neither principal substitution nor disabling receiver
checks is an option. A major hosting/transport change needs a deliberate scoped
requirements decision, compatibility checks and deliberate dependency pins.

## Delivery and construction handoff

The CLI delivery workflow is not the application's MAF graph. Scrum Master
decomposes this design; DevOps owns Sprint 1's dependency-free
`walkingSkeleton:true` assignment. All other first-sprint tasks transitively
depend on its deployed pass. This document does not assign a sprint schedule.

Current inspection confirms all three `azure.yaml` hooks invoke
`package_guard.py`; its `main()` requires `DEMO_APPROVED_PACKAGE_SHA256`,
`TMPDIR` and `DEMO_PACKAGE_RECEIPT`. This is a current source-level D1/F1
contract mismatch, not a fresh attempted deployment failure. The smallest planned
change replaces these hooks with ordinary source exclusions, dependency and
build validation for normal `azd deploy`, preserving unused legacy package tools.
The hosted target stays Linux/amd64/Python 3.13, Responses 2.0.0 with
`remote_build`; requirements and the lock remain the compatibility authority.
The exact supported packaging behavior must be tested, not guessed from YAML.

Construction supplies local checks and an exact committed candidate, without
deploying. DevOps deploys that exact candidate and E2E probes it while holding
`existing-nonproduction-project-deployment-and-verification` and
`existing-nonproduction-project-deployment-configuration`; then original
reviewers assess acceptance. The skeleton requires both actual azd command
evidence and a separate successful deployed probe. Later candidate acceptance
requires the applicable fresh deployed criteria, not offline test results.
Continue independent approved construction around localized failures without
releasing genuine blocked prerequisites. No added exhaustion/disposition gates.

Normal deployment uses only existing services. No `azd up/provision`,
infrastructure, RBAC/network/DNS/quota, VM power, secrets, VPN, private lab edits,
fourth role or Git push is authorized here. Before any later delivery launch,
the execution owner performs the mission's current framework/registration checks;
this ArchitectureLoop neither launches nor upgrades the running delivery engine.

## Verification and current evidence

Run the architecture contract suite from the repository root:

```powershell
python tests/test_delivery_architecture.py --evidence docs/requirements/checks/delivery-architecture.txt
python -m unittest discover -s tests -p test_delivery_input.py -v
python scripts/repo_index.py --check
```

These checks validate the artifact's structure, canonical coverage, source/test
joins, reference integrity, authority boundaries and negative mutations. They
are not execution tests of MAF, Blob, private connectivity or remote inference.
Existing application regression targets are mapped in the artifact, not claimed
as newly run here. The existing `live_acceptance.validate_scenario_evidence()`
can join independently collected private observations; caller-supplied JSON
alone is not live provenance. Preserve raw private context outside public Git;
retain only sanitized commands/outcomes and repository-relative evidence refs.

| Component | RAG | Evidence/freshness | Remaining work/next action |
|---|---|---|---|
| deployment | 🔴 | Source inspected at `87ad50c`: three legacy predeploy hooks and required approval environment | DevOps replace/test normal-azd path, then actual skeleton/candidate deployment and probes |
| coordinator-routing | 🟠 | Current graph/routing source inspected; no fresh live result | Verify genuine gated Decision-1 and exact finish/provenance |
| architect | 🟠 | Current remote assignment lifecycle inspected; no fresh live result | Real first design and findings-driven revision |
| reviewer | 🟠 | Current remote assignment lifecycle inspected; no fresh live result | Actual first findings and exact revised-candidate approval |
| blob-shared-context | 🟠 | Current immutable store/scope/lease source inspected; no fresh live result | Private MI exchange and publication probes |
| session-continuity-recovery-isolation | 🟠 | Current binding/state source inspected; no fresh live result | Follow-up, known recovery/checkpoints, supported stop/resume and independent parent |
| terminal-demo | 🟠 | Existing terminal/acceptance source, unexecuted here | Fresh synthetic full flow and same-parent follow-up |

Schema completion only completes this bounded architecture output. Deployed
versions, environment authentication and product acceptance remain unverified.
