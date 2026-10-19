# Customer hosted-session prototype: release architecture

## Scope and authority

This is the Architecture Loop handoff for the October 19, 2026 customer prototype.
The outcome is a hosted coordinator repeatedly invoking the same two remote
specialists within one parent conversation, not a new orchestration system.
It complements [design.md](design.md) and the measured history in
[identity-recovery-plan.md](identity-recovery-plan.md). It does not assert
deployment, live acceptance, or reviewer agreement.

The run's supplied customer specification is the release acceptance source.
There is currently no `docs/requirements` directory. Do not invent requirements
or copy private delivery control-plane inputs into this repository.
The October 19 invocation authorizes scoped application/release-tool changes,
reviewed feature-branch delivery, guarded publications to the existing three
roles, synthetic tests, supported hosted compute stop/resume, the existing
read-only SSH mount, and starting the existing registered command VM if needed.
Older documents' consumed single-diagnostic authorization describes history,
not the entirety of this run's authority. Conversely, this run does not reconcile
the old UNKNOWN publication, authorize a held-parent resend, or permit speculative
identity changes. No infrastructure, permissions, quota, network, DNS, VPN,
provider submission, new service, or alternate project is in scope.

## Principles, framework and tools

- Retain the existing explicit execution order and role-local five-stage flows.
  No architecture rewrite, generic session manager, framework replacement, browser
  UI, fourth hosted service, or line-count-driven splitting.
- Use Python, Microsoft Agent Framework, Microsoft Foundry hosted Responses,
  Pydantic contracts and Azure managed-identity Blob adapters already in this
  repository. Keep `requirements.txt` / `requirements.lock.txt` pins; change them
  only for an evidenced compatible remedy with held-state implications reviewed.
  Current direct pins include MAF core 1.21.0, Foundry integration 1.14.0,
  hosting 1.0.0b261002, agentserver Core 2.2.0 and Responses 2.3.0.
- Keep Microsoft-Decision-1 for bounded semantic coordinator choices after
  deterministic gates. It is a model deployment, not another hosted agent.
- Use retained PowerShell/Python/WSL build, Linux package, preview, publication
  and connectivity tools from the linked lab with explicit application/lab roots.
  No direct mutation shortcut or runtime/control-plane replacement.
- Test behavior and provenance, not success-shaped text. Offline fixtures,
  Linux package validation, deployed metadata and live acceptance are distinct
  evidence categories and must remain distinguishable in every report.

## End-to-end call and state design

```text
terminal user turn -> Foundry coordinator parent P
                       MAF begin -> route -> execute -> publish -> route ...
                                             |
                         +-------------------+-------------------+
                         v                                       v
                  remote architect A(P)                  remote reviewer R(P)
                  own model history                      own model history
                         |                                       |
                  immutable candidate                  immutable exact review
                         +----------> coordinator acceptance <---+

second user turn -> same P -> same A(P), R(P); new response IDs and revisions
separate parent Q         -> different A(Q), R(Q) and artifact namespace
```

These are exactly three deployments, not three conversations globally.
Every parent has its own two child bindings. Architect/reviewer calls are causal:
the reviewer needs the accepted current candidate; it cannot run speculatively
in parallel with its producer.

### Source trace and continuity contract

1. `demo/host.py` configures the request-aware `create_workflow` / `parse_turn`
   entry points, `CheckpointStoreProvider` and resilient background hosting.
   The descriptor's `DEMO_RUNTIME=native` and remote specialist configuration
   remain technical configuration names; presentation cleanup must not silently
   rename runtime options or diagnostic codes.
2. `WorkflowRuntime.begin()` in `demo/workflow.py` binds trusted parent scope,
   persists the new requirements revision, invalidates candidate/review approval,
   and retains the parent's manifest children. It must preserve earlier user
   requirements when appending the asynchronous-queue follow-up.
3. `route()` enforces readiness, pending-effect, deadline and budget gates,
   then records a genuine validated Decision-1 choice where needed.
4. `execute()` looks up `manifest.children[role]`. Only a missing role prepares
   a new `ChildBinding`. `RemoteAgents.prepare()` in `demo/foundry.py` prepares a
   framework `AgentSession`, hosted session ID and pinned deployed version.
   The manifest journals creation before `create_session`. Ambiguous creation
   recovers that exact ID; it must not generate another child.
5. Every invocation validates the stored hosted binding and version.
   `RemoteAgents.invoke()` restores `AgentSession.from_dict(child.framework)`
   and passes that session to the remote client's `run`. It records the new
   response ID immediately and retains the updated framework representation.
   Recovering a known response retrieves it for the same hosted session and
   advances the continuation without another send.
6. Each specialist's `load_or_create_llm_session()` restores `"history"` from
   `AgentSessionStoreProvider(store_name="specialist_history_v2")` in its
   hosting context. Its model-generation stage receives that restored session;
   model pending-operation state records input digest, deployment and response.
   `store_design()` / `store_review()` writes the immutable artifact, clears the
   completed pending operation and persists history. The hosting response ID
   and the internal model-response continuation are different identities.
7. `publish()` validates exact input references, schema, scope, producer
   role/session/version/response, content hash and current revisions before
   fenced/ETag manifest acceptance. An old approval cannot approve new requirements.

The stable contract is parent hosted identity, both children hosted identities,
both framework session identities and pinned versions. Serialized framework
state is not wholly immutable: response continuation must advance. Compare stable
identity fields separately from evolving service-response IDs/state. New
invocations require new response IDs; retrieval of the same known response does
not. Never equate safe display aliases, repeated full requirements or plausible
memory text with actual session continuation.

### Three independent state concerns

| Concern | Durable owner and purpose | Not a substitute for |
|---|---|---|
| Conversations | Parent hosting state, child binding framework dictionaries and specialist model history | Artifact provenance or authorization |
| Workflow position | MAF hosting checkpoints with stable executor IDs | Remote-effect outcome reconciliation |
| Artifacts and effects | Private Blob scope, immutable prerequisites/outputs, manifest and write-ahead journal | Framework/model conversation history |

Use existing `demo/artifacts.py` and `demo/contracts.py` schemas, not a second
protocol. Assignment/output locators are version 1. Typed assignments bind
trusted scope, exact prerequisite refs, operation, expected producer, revisions,
permitted output and deadline. The model cannot select scope or write authority.
Specialists write only their immutable proposals; the coordinator alone accepts.
Creation uses immutable writes; acceptance uses ETag/fencing. A publication
conflict causes reconciliation, not another specialist call.

## Identity and recovery boundaries

Foundry trusted project/tenant/principal/parent binding is mandatory.
The pinned `context.platform_headers()` forwards the opaque call context; it
does not authorize copying the container user header or deriving authority from
an assignment body. Keep exact-origin transport, no automatic effect retry,
private-path checks, bounded calls, managed identity and sanitized diagnostics.

Historical evidence, not a fresh observation in this architecture loop, shows
matching outbound opaque call context and missing trusted user at the architect,
failing `NATIVE_HOST_PRINCIPAL` before specialist application execution.
The older public supported-remedy assessment found no cause-specific correction;
neither a platform defect nor missing grant is established. Downstream work may
research current public supported contracts and reproduce a concrete SDK defect.
It may implement a supported scoped correction with a failing-before regression.
Do not republish the same speculative change or label identity repair verified
without actual successful remote execution.

If only provider-side caller resolution can supply the remedy, preserve exact
private evidence and report the required human/provider action; provider contact
or evidence transfer is not authorized. A bounded research task can close with
actionable negative findings without closing the release. A material proposed
contract/architecture change returns through Architect/PO scope decisions.

Keep write-ahead operation IDs and explicit unknown-effect holds at every
external boundary. Known response -> retrieve; verified immutable output ->
reconcile acceptance; unknown send without recoverable identity -> hold.
Old held parents and publication UNKNOWNs remain retained. New guarded operations
require their own exact source/package/version/owner records and reconciled
outcomes; a new run, package or version is not a replay permission.

Recovery acceptance is one supported hosted compute stop with its durable
marker, confirmed stopped/idle state and same-parent continuation. Preserve
checkpoints, children and effect journals; prove no duplicate sends. It is not
hard-kill testing, exactly-once infrastructure, or a general crash guarantee.
Never repeat an uncertain stop or clear its marker to retry.

The lab's account-wide Blob Contributor policy means role/parent restrictions
are application-enforced. They do not protect against a malicious hosted process
using its identity outside these adapters. Do not request RBAC changes or claim
storage-enforced tenant isolation to satisfy the prototype.

## Downstream implementation and fixture handoffs

The Scrum Master owns task decomposition, actual assignments, minimal dependency
edges and Git reconciliation. The following are architecture contracts, not
additional approval stages or a replacement sprint plan.

| Work boundary | Done when / handoff | Exclusions |
|---|---|---|
| Developer: continuity regression | Extend `test_followup_invalidates_old_approval_and_preserves_children` to record both roles' hosted/framework IDs, versions, response sequence, exactly two creations, both turn invocations, current requirements and stale approval invalidation | No live claim from fakes; do not compare entire changing framework dictionaries as immutable |
| Developer: controlled revision fixture | Force architect -> blocked reviewer -> same architect -> same reviewer; record exact bindings, new response IDs, revised candidate and review refs and final approval | Do not replace the actual workflow with a toy loop or treat this as live AC3 proof |
| Developer: model continuation | Exercise each real specialist stage with restored history and captured model-session/continuation arguments; prove the second model call uses prior stored history, plus fresh/absent history negative control and known-response no-resend recovery | Replaying a full brief or checking memory text alone is insufficient |
| Developer: supported runtime correction | Evidence-backed failing-before regression and smallest supported fix; preserve identity, artifacts, routing and recovery contracts | No speculative headers/grants, history reset or fourth service |
| Designer: customer clarity | First-screen README goal/diagram/two-turn invariant/source path/status, plus concise terminal continuity display derived from validated real events and useful design/review output | No UI/framework rewrite; diagnostic chronology belongs in the existing recovery document |
| DevOps: exact release and live proof | Required source checks, actual Linux hosting-package gate, guarded exact-package preview/publication, final common bundle and synthetic G1-G8 evidence or precise external stop | No metadata-only PASS, mixed diagnostic final release or repeated unknown effect |

Keep acceptance JSON/envelopes and delegation parser unchanged. Prefer opt-in
or separate terminal presentation if readable lines would disturb the existing
machine stream. Presentation must label stable parent/child aliases versus new
response aliases, and indicate verified checks versus unavailable observations.
Generate aliases from actual validated bindings; no raw private IDs, tokens,
real customer transcripts or private lab configuration. Existing machine
evidence remains the acceptance source; do not introduce a parallel ledger.

## Release verification and evidence matrix

| Criterion | Evidence required by downstream original owner loops |
|---|---|
| AC1 / G2 | Real three-role remote execution and accepted current candidate/review, exact requirements and producer/hash/revision checks; no local specialist |
| AC2 / G5 | Synthetic private-ingress initial turn then asynchronous-queue follow-up; same parent, both hosted/framework children and versions, new role responses, no new children |
| AC3 | Controlled offline reject/revise/review fixture with binding and model-history continuation assertions, explicitly labeled offline; AC1/AC2 independently live |
| AC4 / G6-G7 | Once-only supported stop/resume with no duplicate effects, plus distinct second-parent child bindings/artifact scope and no cross-parent requirement leakage |
| AC5 / G1-G8 | G1: final common bundle, exact healthy deployed versions/unchanged identities; G2: remote collaboration; G3: real MI/private Blob provenance; G4: genuine Decision-1; G5: continuity; G6: recovery; G7: isolation; G8: truthful cleanup/unknowns |
| AC6 | Customer-readable first screen and actual two-turn terminal view with unchanged separately available machine evidence |
| AC7 | Exact-source `Test-Demo.ps1 -Python <absolute-validated-python> -LabRepositoryRoot <explicit-root>`, `scripts/Test-Repository.ps1 -Python <absolute-validated-python>`, targeted tests, retained regressions after lab changes, actual source-bound Linux/amd64/hosting-Python package tests |
| AC8 | Reviewed related readability integration, intended explicit-path commits/push on the feature branch, preserved originals/unrelated dirt/history; no private evidence/settings/packages/runtime in Git |
| AC9 / G8 | Reproducible setup/terminal command, sanitized continuity proof, checks actually run, exact final/rollback bindings, owned cleanup and unverified limitations |

DevOps must freshly inventory actual versions/identities/package hashes through
retained tools after private settings validation, not adopt historical
architect17/reviewer15/coordinator23 as current release identity. Build source and
dependency provenance, immutable stage, approved ZIP/version preview and Linux
gate must bind the exact delivered revision/common bundle; no resealing old
migration hashes or installing dependencies without manifest change/missing tool.

The critical live chain is supported identity remedy -> verified source/package
-> guarded final publication -> initial accepted parent -> follow-up -> supported
stop/resume -> evidence closeout. Offline tests and clarity can proceed independently
of remedy discovery. Separate-parent live execution needs the final release and
initial-parent evidence for comparison, not the first parent's restart.
Only the DevOps work loop publishes and executes live operations. Serialize the
publisher and retained transport/mount/CLI resources; the scheduler is not an OS
lock. Suggested `exclusiveResources` names for Scrum assignment are
`lab-hosted-release`, `lab-private-transport` and `application-git-integration`;
map them to actual shared resources rather than assuming cross-run enforcement.

Architecture work excludes deployment, acceptance execution, support submission,
runtime repair and unreviewed dirty-source integration. Those remain downstream.
Owners commit explicit owned paths before review; reviewed scoped work is pushed
on `feature/customer-hosted-session-prototype`. Preserve unrelated staged/dirty
work; integrate task commits there or durably record named retained branches,
commit IDs and abandonment reasons in feature-branch commit messages.
Use existing sprint review/retro and release closeout, not new approval stages.
Five consecutive rounds without reviewer-verified new progress stop blocked;
productive rounds remain uncapped. This conditional architecture is not a
guarantee that a supported provider remedy exists or that AC1-AC9 will pass.
