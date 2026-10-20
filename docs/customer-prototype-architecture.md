# Customer hosted-session prototype: release architecture

## Scope and authority

This is the Architecture Loop handoff for the October 19, 2026 customer prototype.
The outcome is a hosted coordinator repeatedly invoking the same two remote
specialists within one parent conversation, not a new orchestration system.
It complements [design.md](design.md) and the measured history in
[identity-recovery-plan.md](identity-recovery-plan.md). It does not assert
deployment, live acceptance, or reviewer agreement.

The run's supplied customer specification is the release acceptance source.
`docs/requirements/{coordinator,specialists,client-release}/architecture.md`
now contains derived logical-tier contracts, not replacement requirements.
Do not invent requirements or copy private delivery control-plane inputs into
this repository.
The October 19 invocation authorizes scoped application/release-tool changes,
reviewed feature-branch delivery, guarded publications to the existing three
roles, synthetic tests, supported hosted compute stop/resume, the existing
read-only SSH mount, and starting the existing registered command VM if needed.
Older documents' consumed single-diagnostic authorization describes history,
not the entirety of this run's authority. Conversely, this run does not reconcile
the old UNKNOWN publication, authorize a held-parent resend, or permit speculative
identity changes. The additional October 19 path-selection and permission
approval permits either supported authentication-configuration correction or
`x-ms-user-identity` delegation, including necessary scoped RBAC/permission
changes in this lab. This narrow exception replaces this document's earlier
blanket permission prohibition, not its identity checks or release gates.
No new infrastructure, quota, network, DNS, VPN, provider submission, new
service, or alternate project is in scope. Do not replace existing identities
merely to obtain a different caller.

## Current source-to-trial decision (October 20, 2026)

This owner inspected clean application HEAD
`3aca5dc236695c5ec7eac98d0cd03bced40da7b8` on
`feature/customer-hosted-session-prototype`. The isolated runtime candidate is
now implemented there; the earlier baseline sections below are historical.
`WorkflowRuntime.resources()` unconditionally builds B's specialist-only
headers/client for this source. The original six-resource tuple still exposes
opaque-only authority to non-specialist callers. No runtime A/B selector exists.
Installed source is **not** live selection: principal compatibility, effective
permission and both specialist receivers remain unmeasured in this turn.

### Source identity is part of the scenario contract

The required runner's scenario label must describe the actual reviewed source,
not configure behavior that this runtime cannot select:

| Trial | Required source/package join | Fail-closed result |
|---|---|---|
| `B-candidate` | Reviewed `3aca5dc` candidate or its reviewed descendant, integrated with the lab runner, then exact-source Linux/common-package/version closure | A pre-candidate package is not B even if the runner labels it B |
| `A-correction` | A separate reviewed source revision containing a concrete supported opaque-path correction, with its own regression and package/version closure | Current unconditional B source cannot be relabeled A; unchanged historical A is not a correction |
| Existing held parent or unknown operation | Retain its original exact source/version/session binding and inspect only known effects | Neither scenario adopts it, changes its identity namespace or sends again |

This is an input-consistency rule for retained local runner/preflight tooling, not a
new receipt protocol, runtime selector, acceptance ledger or approval stage.
Reject mismatched scenario/source/package/actual-version joins before creating
a trial parent. Record the mismatch without dispatch. If A becomes the smallest
evidenced repair, implement it as ordinary reviewed source through the existing
Developer/DevOps loops; do not silently toggle a private environment variable,
edit a sealed stage or switch the shared checkout to an old revision.

The candidate's guards run while resources are constructed, before remote
dispatch. A missing/invalid captured user, full-scope mismatch or forbidden
header is therefore a **local preparation rejection**, not evidence of remote
ingress absence or a denied permission. Only an observed child result can
classify child receiver failure. An absent observation remains unknown.
Keep these distinctions in existing sanitized decision outcomes; no raw identity
or header values belong in the public report.

### Current ownership and readiness join

The existing SprintPlan at `4f2e02d` assigns
`RP-S2-DECISION-RUNNER` to **Developer**, after
`RP-S2-LAB-OWNERSHIP`; DevOps retains inventory, package/publication and the
live trial. This supersedes only the earlier architecture's suggested coding
owner, not the runner contract or DevOps execution ownership.
`RP-S2-ISOLATED-CLIENT` has implementation commit `3aca5dc`; retain it for
original review/integration, without redispatching candidate or RP-S1 UX/
continuity work. This turn does not assert that its task reviews are accepted.

The current minimal join is:

```text
lab writing ownership -> Developer runner ------------------+
implemented B source -> original review -------------------+-> source integration
fresh inventory (DevOps, independent) --------------------------+
source integration -> final-source/Linux/package gates --------+-> DevOps trial
```

Source integration must cover the reviewed application commit and reviewed
lab-tool commit on their authorized feature branches. Existing lab checkout
`feature/swc-think-fast-aca-dns` and its unrelated dirty files remain untouched
here. Establish safe lab writing ownership rather than switching it underneath
another writer. An evidenced permission delta adds only its own scripted
plan/write/readback edge. Scheduler resource names do not provide OS exclusion.

The lab file inventory inspected here contains retained App/Observe and
publisher tooling but no new decision-runner entry point. That does not prove
no task exists on another worktree; require the actual named commit/entry point
at integration, not a guessed command. Before the finite live trial, DevOps
must demonstrate scenario/source mismatch rejection, pre-dispatch preparation
failure, competing owner, unknown effect hold, exact-response zero-send
recovery, redaction and partial-role outcomes in the retained runner tests.
Architect success alone leaves reviewer unverified. All original AC1-AC9 and
G1-G8 remain downstream and unchanged; this architecture makes no cloud claim.

### Local verification of this source-to-trial update

Using the existing absolute validated Python 3.12.10 executable and explicit
lab root, `Test-Demo.ps1` passed dependency checking, **192 offline tests in
23.678 seconds** and compilation. `scripts/Test-Repository.ps1` passed index,
public-boundary (**74 public files**), JSON, PowerShell, context and whitespace
checks. No dependency installation or runtime change was needed. These repeat
local checks are not new live progress or selection of B.

No settings import, authenticated cloud query, permission change, deployment,
inference, Linux hosting-package gate or release acceptance was performed in
this architecture turn. Lab sources were not changed; the retained full lab
suite was not rerun. Original Product Owner, Red Team and Critic review of this
delta remains required; owner documentation does not assert their agreement.

## Previous architecture decision and inspected baseline

The preceding architecture revision started from application commit
`24b883f910dedbc8dc524177f29f59e061be265e` on
`feature/customer-hosted-session-prototype`, with a clean application worktree.
The previous RP-S1 source/clarity integration is retained, not reopened:
`6614440` added workflow continuity fixtures, `c454e50` added direct specialist
continuation fixtures, `56b762e` added the opt-in terminal view, and `24b883f`
integrated the reviewed source and runnable README. These are implementation
history, not freshly verified live capability or new work credited to this loop.
The lab remained on its existing unrelated feature branch with pre-existing
dirty work. This architecture turn makes no lab edits or branch changes.

No prior dispositions or reconciled feedback were supplied for this invocation.
The new user approval, rather than a newly inferred permission or an older
research task's exclusions, governs identity-path evaluation below.

**Decision:** retain the complete three-role architecture and its current
contracts. Evaluate the smallest supported correction first; permit explicit
delegation as a real alternative, not an already-proven repair. Neither path
has demonstrated successful specialist ingress in this turn. Continue release
and sprint artifact generation while selection is unresolved. Do not declare
a provider-only stop solely because the previous opaque-context research was
unresolved: the newly authorized delegation alternative must be assessed too.
Formal E2E validation stays in the End-to-End Test Loop; deployment and
cloud-pass stay in the DevOps Work Loop. Architecture/planning can run bounded
decision tests, but cannot promote their results to those acceptance gates.

### Verification of the preceding architecture revision

Using the existing validated absolute Python 3.12.10 executable, without
installing dependencies:

- `Test-Demo.ps1 -Python <absolute-validated-python> -LabRepositoryRoot
  <explicit-lab-root>` passed dependency checking, **177 offline tests in
  23.705 seconds**, and compilation.
- `scripts/Test-Repository.ps1 -Python <absolute-validated-python>` passed
  index, public-boundary (**70 public files**), parser and whitespace checks.
- Local documentation checks verified 11 relative links/anchors and the
  presence of AC1-AC9 and the identity-selection handoff fields.

No retained lab source changed, so its full release suite was not rerun.
Linux hosting-package checks, live identity-path selection, deployed/rollback
inventory and formal release acceptance were not executed. Original Product
Owner, Red Team and Critic agreement is not asserted by this owner handoff.

## October 20 architecture delta: executable candidate boundary

This Architecture Loop inspected clean application HEAD
`bb1743d85cb10e6520c92efaa42df0702178f57a` on
`feature/customer-hosted-session-prototype`. The lab remains on
`feature/swc-think-fast-aca-dns` with unrelated dirty work; this turn neither
changes that branch nor edits lab files. The integrated
[`identity-candidate-handoff.md`](identity-candidate-handoff.md) adds nine
offline probes in `13203ac`, reconciled by `bb1743d`. Its current executable
has **no live mode** and intentionally returns exit 2 with unresolved selection.
Neither that command nor this architecture executes a hosted B candidate.

At that inspected baseline, the handoff identified a concrete implementation gap:
`WorkflowRuntime.resources()` supplied one `ProjectClient`/header set
to both `WorkflowRemoteAgents` and non-specialist operations. Runtime candidate
installation and a journaled live decision runner are absent. Resolve that
internal design gap here rather than sending the same unresolved research
back to Scrum without an implementation contract.

**Architecture decision:** retain A as the existing opaque-call baseline.
Prepare B as a reviewed, exact-source candidate with a separate specialist-only
project/header client. This is permission to design/assign the candidate, not
selection of B, a claim that parent-derived delegation preserves namespace, or
authority to weaken the receiver. No new framework, schema, deployed role,
user approval stage or infrastructure is introduced. The existing public
delegation references and caveats below still apply.

### Request-local client ownership and unchanged trust

Within the existing `WorkflowRuntime.resources()` `AsyncExitStack`:

1. Keep the original managed-identity credential, exact-origin/no-retry HTTP
   transport and opaque-only project/header resources for routing, model,
   parent/history/checkpoint and other non-specialist uses. Keep the yielded
   resource tuple's meaning/order so callers need no orchestration rewrite.
2. For the B candidate, construct a distinct `ProjectClient` with a **copied**
   specialist header dictionary and a separate OpenAI-client cache. Sharing
   the request-owned credential/HTTP transport is permitted; client lifecycle
   tests must prove cleanup does not invalidate another client while in use.
   Do not mutate `project.call_headers`, SDK ambient context or a shared dict.
3. Derive B's user exclusively from captured authenticated hosting context.
   Revalidate the full `ScopeBinding.from_platform(...)` against the runtime's
   scope before constructing delegated headers. Apply the offline candidate's
   syntax, missing-user, unexpected-header and call-ID-substitution guards.
   Move only the needed pure logic into runtime-owned source; hosted code must
   not import a script/test runner. Never forward `x-agent-user-id`.
4. Give only `WorkflowRemoteAgents` the specialist project/header pair.
   Preserve unchanged opaque-call forwarding alongside B's delegated header.
   Cover metadata/prepare, create, check, ambiguous-create inspection, send
   and exact-response retrieval. Raw Azure SDK explicit headers and Responses
   default headers are separate paths and both require assertions.
5. Do not change `Assignment.validate_receiver()` or specialist history/storage
   construction. The actual child principal must still match the parent's
   trusted principal and all existing scope/version/prerequisite checks.
   Principal absence or namespace change fails the candidate, even if hosting
   returns HTTP 200 or a response can be retrieved.

No new runtime selector is required by this design. Bind an explicitly named
B trial to its reviewed source commit/common package/three target versions in
the private decision record; do not infer a path from errors or switch paths
automatically. The existing bundle retains A until a candidate is deliberately
published by DevOps. If downstream work instead needs a configuration selector,
its source/settings/package closure is an explicit Architect/Scrum delta,
not an undeclared environment variable outside retained settings validation.

Old pinned sessions remain on their old bindings/versions. Do not adopt any
existing held parent, translate its principal/history or attach old children
to the candidate. The candidate starts a fresh synthetic parent. A failed
trial is retained as failed/held evidence; rollback versions and immutable
packages remain available. A later final release may use B only after trusted
ingress selection and full release gates; no old-state migration is implied.

### Deterministic decision runner contract

The assigned Developer supplies the local, lab-owned runner using retained
wrappers; original DevOps executes it. This section defines required behavior,
**not an existing command**. Formal E2E and deployment/cloud-pass ownership
do not move. The current source/scenario join above also applies.

| Input / stage | Required behavior |
|---|---|
| Invocation | Explicit absolute application/lab roots, existing validated Python, scenario (`A-correction` or `B-candidate`), exact reviewed source/package/role-version bindings and private evidence destination outside both repositories |
| Preflight | Load only `Use-Settings.ps1` with the existing native settings; verify sole-target linkage and dedicated authenticated tenant/subscription; join fresh inventory, actual caller/effective action and rollback records. Declared versions from the offline runner are not inventory. |
| Mutation ownership | One owner for `lab-hosted-release` and `lab-private-transport`; journal exact intended effect/bindings before dispatch. Serialize actual publisher/CLI/mount use, including across workflow runs; scheduler labels alone provide no OS exclusion. |
| Publication | If a new candidate bundle is needed, use reviewed source checks, actual Linux/amd64/hosting-Python gate, immutable stage, fresh preview and retained publisher. This is original DevOps work, not an architecture deployment shortcut. |
| Finite trial | One fresh parent; attempt architect first, then reviewer only after trusted architect entry/receiver success. Record the finite intended role calls before starting. Routing/model calls retain existing admission/deadline budgets. A needs a measured supported correction; do not trial unchanged A again. |
| Observation | Privately bind exact actual role/version/parent/child/framework/response and artifact scope; publicly expose presence/match/entry classifications only. Verify the receiver passed, not only nonempty ingress identity. Coexistence of opaque and delegated headers remains a measured question. |
| Failure/recovery | Stop on missing/changed principal, version drift, receiver rejection, unknown create/send or held effect. Retrieve a known exact response only; never create/send again to obtain a missing receipt. Preserve absent evidence as unknown rather than negative proof. |
| Result | `selected-A`, `selected-B` or `unresolved`; actual tests and evidence kind, principal compatibility for each reached role, private locators, permission delta/readback, holds, cleanup and next closing action. Report unreached reviewer explicitly. A successful architect discriminator alone is not three-role collaboration. |

Reuse existing assignments and exact immutable prerequisites for the trial.
Do not invent an unprotected diagnostic endpoint, ask the model to assert its
identity, bypass Blob validation or add a second acceptance ledger. If retained
App/Observe modes cannot express the finite decision sequence safely, extend
them with targeted lab regressions rather than improvising external commands.
Unknown effect records must be inspectable without dispatch. Missing permission
is a conditional delta, not an assumed prerequisite: read back the existing
explicit grant before planning any scoped write.

### Minimal downstream delta and stop conditions

Scrum Master owns actual task IDs, assignments and Git reconciliation. The
following bounded contracts refine the existing release plan, not replace it:

| Delta / original owner | Done when | Hard handoff / exclusions |
|---|---|---|
| Isolated B runtime / Developer | Exact-source candidate wires specialist-only clients; real resource-factory tests prove both-role lifecycle headers, unmodified non-specialist context, cleanup, trusted binding negatives and known-response zero-send recovery; complete application/repository checks pass | Uses integrated offline handoff; excludes deployment, namespace relaxation, dependency migration and duplicate continuity/UX implementation |
| Fresh inventory / DevOps | Sole-target active/rollback package/version/identity/protocol, actual caller/effective explicit action and unresolved operation records are current and privately bound | Independent of runtime coding; no assumed missing grant or mutation from metadata alone |
| Decision tooling / assigned Developer | Retained local runner implements the table above; offline failure/unknown/ownership/redaction fixtures and affected retained suite pass | Runner coding can parallel runtime coding against this contract; live execution remains DevOps and waits for inventory plus reviewed candidate/source/Linux/package gates |
| Bounded ingress decision / DevOps | Execute the finite trial under existing authority and record selected/unresolved with receiver evidence for each reached role | No formal acceptance credit; stop on held/unknown work. Unsupported namespace requires an explicit end-to-end authenticated design through Architect-advised PO/Scrum, never an equality bypass. |
| Integration / Scrum-assigned owner | All reviewed task commits are on the authorized feature branch, or named retained branches/commit IDs/reasons are recorded in a feature-branch commit; exact integrated source rechecked | Do not switch a shared lab checkout underneath other work; establish its feature branch safely before writing, or use a separate branch/worktree with explicit integration ownership |

Only an evidenced required permission delta introduces its corresponding
scripted plan/write/readback dependency. A genuine unavailable platform remedy
can stop execution with an actionable external finding; unresolved candidate
research alone does not stop remaining artifacts. Continue ReleasePlan and
SprintPlan outputs even while selection is unresolved. Original AC1-AC9 and
G1-G8, including final common bundle, two-turn/revision/continuation evidence,
private MI provenance, stop/resume, isolation, truthful terminal and closeout,
remain unchanged. Do not redispatch the already integrated RP-S1 fixtures/UX.

The owner considers this conditional end-to-end design ready for the original
Product Owner, Red Team and Critic review. Their agreement and live feasibility
are not claimed by a documentation change.

### Verification of the October 20 delta

Using the existing absolute validated Python executable and explicit lab root,
`Test-Demo.ps1` passed dependency checking, **186 offline tests in 23.995
seconds**, and compilation. `scripts/Test-Repository.ps1 -Python
<absolute-validated-python>` passed index, public-boundary (**73 public files**),
JSON, PowerShell, context and whitespace checks. A targeted local check passed
the architecture contract fields and all three relative links/anchors.
No dependencies were installed and no runtime source changed.

These are local source/document checks, not newly credited continuity proof.
No cloud inventory, settings import, permission readback/write, inference,
publication, Linux hosting-package check or live acceptance was performed.
No lab tool changed, so the retained full lab release suite was not rerun.
The remaining executable candidate/runner and all live gates are explicitly
downstream; historical unknowns and unrelated dirty work are untouched.

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

### Supported identity alternatives and selection contract

Public sources checked for this revision:

| Source | Observed revision / applicable fact |
|---|---|
| [Hosted runtime contract](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agent-contract#platform-request-headers-container-protocol-200) | Source `69a226754528e8d4d032ec652eba7d82e584f648`, updated September 28, 2026: container protocol 2.0.0 forwards the opaque call ID unchanged to other agents; the injected user header is container-only. |
| [Per-user isolation and delegation](https://learn.microsoft.com/azure/foundry/agents/how-to/isolate-sessions-per-user#isolate-sessions-for-your-own-users) | Source `f5104405dfd0231d706f8198fb841f45826595b9`, updated October 13, 2026: `x-ms-user-identity` is a supported trusted-service contract; value is a stable authenticated end-user identifier, 1-256 permitted characters, not a call ID. Delegated-session access is not fenced between delegated users. |
| [Hosted agent permissions](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agent-permissions#delegate-the-end-user-identity) | Source `bd74da57b5293b70e0538b76b75d983ab2e67d80`, updated September 23, 2026: delegation requires the explicit `Microsoft.CognitiveServices/accounts/AIServices/agents/endpoints/UserIdentityImpersonation/action` data action, not a built-in role or wildcard assumption. |

The installed Core 2.2.0 `platform_headers()` was inspected again: it emits
only `x-agent-foundry-call-id`; it does not send a delegated or container user.
The existing offline diagnostic returned `OFFLINE_VERIFIED_LIVE_UNRESOLVED`
(intentional exit 2). Settings were loaded solely with `Use-Settings.ps1`;
local schema and expected lab linkage passed without displaying values.
These are local observations, not authenticated cloud-context validation.
No cloud version/permission readback, inference, permission mutation or
publication occurred in this architecture turn.

| Path | Smallest admissible change | Selection evidence / rejection condition |
|---|---|---|
| A: agent-to-agent authentication/configuration correction | Preserve existing Responses transport and unchanged opaque-call forwarding. Correct only a measured endpoint, protocol, effective-caller permission or supported authentication configuration mismatch. Here agent-to-agent is the interaction, not a requirement to introduce a new A2A wire protocol. | Fresh exact bindings and relevant effective permissions establish the mismatch, then a bounded synthetic invocation reaches the specialist with trusted context and passes existing receiver checks. HTTP 200, health, permission presence or another identical opaque-header publication do not select A. |
| B: explicit `x-ms-user-identity` delegation | Use the existing authenticated coordinator as the trusted middle tier for the two specialists. Derive the identifier exclusively from authenticated server-side user context; validate its permitted syntax and stability. Never derive it from `call_id`, model output, assignment JSON, a client-supplied identity or a default principal. | Exact SDK/HTTP checks show a consistent delegated namespace on session create/read, Responses send and known-response retrieve. A fresh synthetic parent reaches specialist application entry and passes principal/assignment validation. A changed/missing principal, namespace mismatch, 403 or held effect is a failed discriminator, not permission to relax checks. |

Do not combine call-context forwarding and explicit delegation by guesswork.
For B, establish from the supported contract and a bounded test whether both
headers can coexist and which identity the platform actually resolves. Forward
the opaque call ID unchanged wherever the platform contract requires it; never
recast it as a delegated user or suppress it to escape a failure. Do not forward
`x-agent-user-id` outbound. The legacy `platform_identity_headers()` currently
adds both user headers and is **not** a drop-in B implementation.

#### Binding compatibility is a required discriminator

`Assignment.validate_receiver()` in `demo/artifacts.py` compares the child's
platform-injected principal to the parent's `scope_binding.principal`.
The delegation docs do not promise that delegating an already platform-derived
user ID returns that same principal rather than a newly derived identity.
Therefore a nonempty child user alone cannot select B. Privately compare the
actual trusted identities, exposing only match/presence classifications publicly.

A valid B design must use one stable, authenticated delegation scheme across
the affected lifecycle. Verify all existing boundaries: `RemoteAgents.prepare`,
`create`, `_check` / `recover_creation`, `invoke` and `recover`; raw Azure SDK
session operations and OpenAI Responses clients use different header plumbing.
At the earlier baseline `WorkflowRuntime.resources()` shared a project/header
client with routing and other project operations. Candidate `3aca5dc` now
separates specialist delegation while retaining original model, checkpoint,
history and parent authority. Preserve that explicit separation and execution
order; no generic session manager or second protocol is needed.

If B changes the principal namespace, do not remove the equality assertion,
trust the supplied assignment principal, migrate old histories or silently
reinterpret saved bindings. Return the exact mismatch to this existing
Architect/PO/Scrum process for an authenticated end-to-end namespace/binding
design and focused negative tests. That is an internal bounded contract
decision, not a request for new permission already granted by the user.
An alternative that cannot preserve or securely establish the required binding
is not selected merely because it makes the host gate nonempty.

#### Permission exception: exact scope, not blanket mutation

Before any write, freshly resolve the actual outbound authenticated coordinator
principal, the two existing specialist resources and existing role definitions/
assignments from the validated sole-target lab context. Historical evidence
says an explicit impersonation grant already exists: verify its actual caller,
data action and effective scope rather than create a duplicate or infer it is
missing. Record private exact resource/principal/role IDs, before/after state,
reason and operation outcome; public source contains only generic contracts.

For B, if genuinely missing, grant only the impersonation data action to that
verified coordinator identity, assigned at each existing specialist's supported
agent scope. If that scope is unsupported, document the observed constraint
and smallest supported project scope before mutation; never expand to a
subscription/resource-group/account assignment for convenience. A custom role's
assignable scope is not an instruction to assign it at that broader scope.
For A, any additional interaction permission likewise needs a demonstrated
missing data action at the exact target; no generic Owner/Contributor remedy.
Specialists need no impersonation grant just to serve incoming calls.

Perform necessary changes via deterministic, reviewed lab-owned scripts using
the dedicated verified profile. They must compare installed state, plan the
exact approved delta, record effect ownership before sending, avoid duplicate
assignments, reconcile unknown outcomes and report readback separately from
runtime success. This exception permits required permissions only; it does
not authorize new infrastructure, identity replacement, credentials, model
capacity, network/DNS changes or public ingress. No permission change is made
by this document. Existing account-wide Blob policy is unchanged.

#### Bounded decision procedure and downstream handoff

Scrum Master decomposes these contracts into tasks, not another approval stage:

1. **Read-only inventory and fixture contract:** resolve fresh role/version/
   package/protocol/caller/grant bindings through retained tools; preserve
   rollback and UNKNOWN records. Define a local scripted decision test with
   explicit roots, path, exact versions and a new synthetic scope. Source and
   tests must cover omitted/invalid user, forged assignment identity, two parent
   scopes, both roles, all SDK header boundaries and exact-response no-resend.
2. **Smallest discriminating correction:** A only if a concrete supported
   mismatch is found; otherwise evaluate B against its documented delegation
   contract and binding-compatibility checks. Developer owns application changes,
   DevOps owns any required package/publication or lab permission execution.
   Do not redeploy A unchanged as an experiment. Each candidate must have its
   own hypothesis and failing-before/passing-after local regression.
3. **Bounded ingress observation:** use an in-repo local script, synthetic data
   and a fresh decision-test parent, journaled before sends. Capture exact role/
   version/session/response, header-presence and principal-match flags,
   application-entry/receiver-check outcome and cleanup. Try architect before
   reviewer; stop the candidate on a held/unknown effect. Never resend to get a
   missing receipt. Review existing exact responses instead. Any deployment
   prerequisites still use the original DevOps source/Linux/package gates and
   retained publisher, not an architecture-loop bypass.
4. **Decision output:** `selected-A`, `selected-B`, or `unresolved`, with cause,
   actual tests, binding-compatibility result, exact private evidence locators,
   changed permission scope/rationale (if any), held effects and closing action.
   A selected path needs successful trusted specialist ingress, not merely the
   offline probes. Confirm both roles before claiming release collaboration.
   The decision test is not AC1-AC5 or G1-G8 release acceptance.
5. **Continue artifacts regardless:** unresolved selection does not block
   remaining design, release planning, fixtures or documentation. A true
   provider-only finding needs a specific unavailable supported remedy after
   these alternatives are assessed; external contact/disclosure remains excluded.

The script must require an explicit scenario and record its finite intended
call sequence, not run uncontrolled inference or a benchmark. Diagnostic
inference permission is not automatic authority to repeat an unknown effect.
If the existing environment cannot exercise B without a new package, hand the
minimal reviewed change to original DevOps; do not silently deploy during
architecture to force path selection.

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
using its identity outside these adapters. Do not claim storage-enforced tenant
isolation to satisfy the prototype. The identity-remediation permission exception
above does not require changing this Blob policy.

## Downstream implementation and fixture handoffs

The Scrum Master owns task decomposition, actual assignments, minimal dependency
edges and Git reconciliation. The following are architecture contracts, not
additional approval stages or a replacement sprint plan.

| Work boundary | Done when / handoff | Exclusions |
|---|---|---|
| Developer: continuity regression | Extend `test_followup_invalidates_old_approval_and_preserves_children` to record both roles' hosted/framework IDs, versions, response sequence, exactly two creations, both turn invocations, current requirements and stale approval invalidation | No live claim from fakes; do not compare entire changing framework dictionaries as immutable |
| Developer: controlled revision fixture | Force architect -> blocked reviewer -> same architect -> same reviewer; record exact bindings, new response IDs, revised candidate and review refs and final approval | Do not replace the actual workflow with a toy loop or treat this as live AC3 proof |
| Developer: model continuation | Exercise each real specialist stage with restored history and captured model-session/continuation arguments; prove the second model call uses prior stored history, plus fresh/absent history negative control and known-response no-resend recovery | Replaying a full brief or checking memory text alone is insufficient |
| Developer: supported runtime correction | Evidence-backed failing-before regression and smallest supported path A/B fix under the selection contract above; preserve identity, artifacts, routing and recovery contracts | No speculative headers/grants, history reset or fourth service; authorized necessary permissions are not categorically excluded |
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
Only the DevOps work loop publishes and establishes cloud-pass. Bounded decision
tests are allowed during design/planning as described above, not formal E2E
acceptance; all tests use deterministic local repository scripts, never GitHub
Actions. The E2E loop owns formal integration validation. Serialize the
publisher and retained transport/mount/CLI resources; the scheduler is not an OS
lock. Suggested `exclusiveResources` names for Scrum assignment are
`lab-hosted-release`, `lab-private-transport` and `application-git-integration`;
map them to actual shared resources rather than assuming cross-run enforcement.

This architecture turn excludes deployment, formal acceptance execution, support
submission, runtime repair and unreviewed dirty-source integration. Those remain
downstream. Future bounded decision tests may be assigned within architecture/
planning under the current user authority without moving release gates.
Owners commit explicit owned paths before review; reviewed scoped work is pushed
on `feature/customer-hosted-session-prototype`. Preserve unrelated staged/dirty
work; integrate task commits there or durably record named retained branches,
commit IDs and abandonment reasons in feature-branch commit messages.
Use existing sprint review/retro and release closeout, not new approval stages.
Five consecutive rounds without reviewer-verified new progress stop blocked;
productive rounds remain uncapped. This conditional architecture is not a
guarantee that a supported provider remedy exists or that AC1-AC9 will pass.
