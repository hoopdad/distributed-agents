# Distributed agents: MAF/Foundry workflow and shared artifacts

The current [delivery mission](requirements/delivery-mission.md) and actual
source/deployment observations govern status. Prior source joins and failure
reports are opt-in [historical context](../.github/repo-history-index.md),
not active blockers or additional release gates.

## How the same specialist session is reused

The customer invariant is one hosted coordinator conversation repeatedly
invoking the same remote architect and reviewer sessions. The three hosted
roles are not three in-process objects. Read the following path in order:

1. [`demo/terminal.py`](../demo/terminal.py) restores the parent's framework
   `AgentSession` from its private session file, verifies the hosted session's
   pinned coordinator version and sends the next user turn with that session.
   A pending or held turn is not permission to send a follow-up.
2. [`demo/workflow.py`](../demo/workflow.py) derives the artifact scope from
   trusted hosting context. In `WorkflowRuntime.execute()`, the locked
   parent-scoped manifest's `children.get(role)` is the create-or-reuse lookup.
   Only a missing role calls `RemoteAgents.prepare()`; the resulting hosted ID,
   framework representation and pinned version are persisted before creation.
   `remote.create()` binds that exact child to its version. An uncertain create
   is inspected through `recover_creation()`, not blindly repeated.
3. [`demo/foundry.py`](../demo/foundry.py), `RemoteAgents.invoke()`, verifies the
   child still exists at its pinned version, restores
   `AgentSession.from_dict(child.framework)` and calls the remote
   `FoundryAgent.run(..., session=session, stream=True)`. The completed session
   representation is saved back to the child; coordinator publication persists
   the binding with the accepted effect. The same lookup and restored session
   apply on a within-turn revision and on a later completed user turn.
4. Inside each remote specialist, `load_or_create_llm_session()` loads
   `"history"` through `AgentSessionStoreProvider`'s `specialist_history_v2`
   store scoped by the hosting context. A new model `AgentSession` is created
   only if history is absent. The architect's `design_solution()` and reviewer's
   `review_solution()` pass that session to their model call; `store_design()`
   and `store_review()` persist it after validating/writing the immutable
   output. Follow these stages in
   [`architect_agent.py`](../demo/architect_agent.py) and
   [`reviewer_agent.py`](../demo/reviewer_agent.py).

The coordinator-to-specialist framework session and the specialist's internal
model-history session are distinct. Hosted/framework **identity fields** and
pinned versions remain stable within a parent; response IDs and service
continuations advance. Do not compare entire serialized sessions as if every
field should stay constant. Known model-response recovery retrieves the exact
journaled response and updates continuation without another model send; unknown
effects remain held.

The requirements artifact also carries earlier requirements, but replaying that
brief or producing plausible memory text does not prove model continuation.
Proof needs actual binding comparisons plus direct restored-history tests and
fresh-history controls for both specialists. Offline fixtures are not live
proof. A separate parent must have separate children and artifact scope; a
model-provided ID cannot establish trusted scope.

### Isolated specialist client candidate (RP-S2-ISOLATED-CLIENT)

The source candidate implements the
[accepted B client contract](customer-prototype-architecture.md#request-local-client-ownership-and-unchanged-trust)
in `WorkflowRuntime.resources()`. The original six-element tuple keeps its
meaning: store, remote specialists, original project, credential, HTTP, original
headers. Only the remote specialists receive a separate `ProjectClient`,
header copy and OpenAI-client cache. Routing, parent and model callers retain
opaque-only authority. Both project clients share the request-owned credential
and exact-origin, zero-retry HTTP transport; the exit stack closes project
pipelines before HTTP and credential.

`demo/foundry.py:specialist_identity_headers()` re-derives the full scope from
captured hosting context and the configured tenant/project, then compares it to
the runtime scope. It rejects unexpected platform headers, invalid delegation
syntax and call-ID-as-user substitution. The specialist copy carries the
unchanged opaque call header plus `x-ms-user-identity`, never `x-agent-user-id`.
It does not use the legacy `platform_identity_headers()` helper. Receiver
principal equality, pinned versions, child/history lookup, effect journals and
unknown-effect holds are unchanged.

`tests/test_isolated_client.py` exercises the actual resource factory and
SDK/Responses clients with controlled network/storage boundaries. Both roles
cover prepare, create, check, ambiguous-create inspection, attempted send and
exact-response recovery; restored hosted/framework/version bindings remain
intact. Negative tests cover changed/forged scope, invalid identity, failed
retrieval without send/create, and cleanup after success, setup failure,
binding failure and cancellation. Closing the specialist project does not
invalidate the original model client's shared HTTP transport. The existing
wire-log test now verifies candidate-only delegation and unchanged original
resources; diagnostic values remain redacted.

Local verification: the existing validated Python 3.12.10 environment passed
dependency checks, **192 offline tests in 23.865 seconds**, and compilation via
`Test-Demo.ps1 -Python <absolute-python> -LabRepositoryRoot <explicit-lab-root>`.
No dependencies were installed. These results do not prove principal namespace
compatibility, permission effectiveness, live specialist entry or release
acceptance. The candidate has no automatic path selector. Existing deployed
versions remain unchanged until the original DevOps loop deliberately publishes
the reviewed exact-source/common package. Source integration must join this
commit with the independently implemented lab runner, then run final-source
and Linux/package gates. Use only a fresh synthetic parent; never adopt held
historical parents or replay uncertain effects.

### Conversations, checkpoints and artifacts are different state

| Concern | Responsible source | Purpose |
|---|---|---|
| Parent and child conversations | `demo/terminal.py`, `demo/foundry.py`, each specialist's history stages | Keep hosted/framework identities and model continuation for the appropriate conversation |
| MAF checkpoints | `demo/host.py`, `create_workflow()` in `demo/workflow.py` | Resume graph/executor position at supported boundaries |
| Blob artifacts, manifest and effects | `demo/artifact_store.py`, `demo/artifacts.py`, `WorkflowRuntime` | Preserve exact requirements/outputs, accepted revisions, provenance, fenced publication and write-ahead effect reconciliation |

None substitutes for the others. New requirements invalidate the prior
candidate/review approval, not the parent/child session bindings. Checkpoints
alone cannot make a remote send exactly once. Application ownership/scope
checks are not storage-RBAC isolation under the linked lab's account-wide
Blob Contributor policy. See [the current mission](requirements/delivery-mission.md)
and [the terminal example](../README.md#two-turn-terminal-demonstration)
for acceptance and baseline syntax, not a live-success transcript.

### Offline cross-scenario evidence assertions

`live_acceptance.validate_scenario_evidence()` joins existing per-scenario
acceptance proofs with private source observations. It performs no collection,
network call, inference, stop or retry. Existing `live_acceptance.py` arguments,
stdout events/parser and opt-in human presentation are unchanged. This callable
is an assertion entry point for retained local execution, not another persistent
comparison ledger or a new release gate.

Run from the application root with the existing absolute validated Python.
`$EvidenceInput` is an absolute private JSON path outside both repositories,
assembled by the execution owner from actual observations:

```powershell
& $Python -c 'import json,sys; from demo.terminal import private_state_path; from live_acceptance import validate_scenario_evidence; validate_scenario_evidence(**json.loads(private_state_path(sys.argv[1]).read_text(encoding="utf-8"))); print("Supplied scenario observations passed offline assertions.")' $EvidenceInput
```

Input keyword keys are `initial`, `followup`, `restart`, `isolated` and
`stopped_session`. Each scenario snapshot contains:

- `proof`: the existing full JSON proof emitted by `live_acceptance.run()`,
  including actual parent framework state, version, child-session metadata,
  delegations and result/artifact envelopes. Aliases alone are insufficient.
- `manifest`: the corresponding completed parent-scoped `Manifest` document,
  including both children's actual hosted/framework identities, pinned versions,
  current accepted references and parent response ID.
- `operations`: the complete cumulative immutable documents from that parent's
  existing `operations/<operation>/<transition>.json` namespace, each retaining
  its original `scope_binding` and `effect`. Include all transitions, not only
  accepted records; missing intent/dispatch, unresolved effects and changed old
  transitions fail closed.
- `creations` and `sends`: cumulative lists of operation IDs, **one entry per
  actually observed specialist create/request send**, from independent boundary
  captures, not lists deduplicated or reconstructed from journal intentions.
  Known-response GETs are not sends. Duplicate entries, missing operations,
  additional creations and response reuse fail. Collection completeness and
  source attribution remain execution-owner obligations.
- For `followup` and `restart`, `checkpoints`: a private capture association with
  `scope_binding` and `records` containing serialized MAF checkpoint documents
  from that parent's existing checkpoint store. Preserve all document fields
  (SDK message enums serialized to their values). The collector must bind the
  association to the actual scoped store; the SDK graph state alone contains
  no parent identity. Assertions require same scope, retained unchanged prior
  checkpoints, new checkpoints and unchanged graph signature after continuation.
- For `restart`, `stops`: one parent ID per actually observed stop POST. Supply
  the existing confirmed durable marker as `proof.hosting_restart`, not an
  invented success flag. `stopped_session` is the actual GET observation of the
  same pinned parent in idle state with matching newly advanced `stopped_at`.

Successful assertions mean the supplied observations are internally consistent:
stable actual parent/both-child identities and versions, new responses on each
turn, exactly two child creations, both-role invocation/effect/output joins,
current hashed requirements/artifacts and invalidated stale approval; confirmed
once-only supported stop plus retained checkpoints/effects without duplicate
sends; and separate-parent child/artifact scope with synthetic requirement
exclusion. The helper checks the fixed Harbor/Cedar synthetic scenarios, not
arbitrary customer transcripts. It rejects Harbor/queue leakage in isolated
candidate/review content (the isolated input deliberately mentions Harbor only
to exclude it). This is application-enforced isolation, not malicious-host or
storage-RBAC isolation.

No self-authenticating provenance or live capability follows from caller-supplied
JSON. DevOps must supply complete, source-bound private observations; original
E2E validates the joined implementation and the existing release gates still
apply. Missing captures are an unmet evidence condition, not authority to
recreate parents, repeat stops or resend unknown effects. Diagnostics from the
new helper are fixed codes without private values.

`tests/test_scenario_evidence.py` executes the real offline graph with controlled
remote/storage/router boundaries and real MAF checkpoints. Its initial fixture
forces four architect/reviewer revision calls. Positive JSON round-trip and
negative binding, version, missing-input, stale/current-output, queue-omission,
extra-create, duplicate-send/response, held-effect, stop/checkpoint, scope,
content-leak and release-drift controls are synthetic only. They do not perform
hosted compute stop/resume or replace live G1–G8 evidence.

> **Current delivery objective:** [requirements/delivery-mission.md](requirements/delivery-mission.md)
> records the current user amendments, source integration, normal-azd work and
> component acceptance/RAG rules. [NEXT-SESSION-PROMPT.md](NEXT-SESSION-PROMPT.md)
> supplies authority only when submitted. Actual current observations determine
> blockers; history is opt-in, not an active gate. The CLI delivery workflow is
> not this application's MAF workflow.

## Following a request through the source

For Foundry hosting, `demo\host.py` hands request parsing and graph construction
to the top-level `parse_turn()` and `create_workflow()` functions
in `demo\workflow.py`. The coordinator graph reads in order:

1. **Begin:** append the user requirement to the shared artifact history.
2. **Route:** load accepted prerequisites, apply deterministic gates, and
   record a validated Decision-1 choice.
3. **Effect:** prepare and dispatch the selected remote specialist operation.
4. **Publish:** validate its assigned output, update the coordinator manifest,
   then return to routing or finish with a result.

For a teaching-oriented reading path, follow `WorkflowRuntime.begin()`, `route()`,
`execute()`, and `publish()` in `demo\workflow.py`. These lifecycle methods are
consecutive, in execution order; shared resource, provenance, journal and result
helpers follow them. Numbered stage comments keep each event's sequence visible
inline. `begin()` names the requirements content, immutable artifact and accepted
reference separately, then resets each turn field explicitly. `execute()` spells
out each role's output type/path and whether the candidate revision advances.
In particular, `route()` reads top to bottom:
resume the turn, validate prerequisites and deterministic finish/budget gates,
recover or prepare the journaled decision, request a model choice only if needed,
then validate and accept that choice. There is no private routing pipeline to
trace through. Shared helpers retain the storage, provenance and journal rules;
this readability refactor does not remove recovery or authorization checks.

Coordinator events open `BlobArtifacts` via `WorkflowRuntime.resources()`;
specialist classes construct their Azure SDK clients in their role-local code. The
`control` container holds requirements, decisions, operation records, and the
coordinator manifest; architect outputs go to `candidates`, and reviewer
outputs go to `reviews`. The coordinator owns manifest publication. These Blob
documents are distinct from MAF workflow checkpoints and Foundry agent-session
history; neither checkpoint nor conversation state replaces the write-ahead
effect record.

`demo\architect_agent.py` and `demo\reviewer_agent.py` define the two
specialist agent classes and contain their complete assignment lifecycles:

- **Architect:** `ArchitectAgent.run_assignment()` validates the assignment, reads
  requirements and any assigned prior design/review from Blob Storage, generates
  a `Candidate` design, validates its revisions, and writes an immutable candidate
  JSON artifact before returning its reference.
- **Reviewer:** `ReviewerAgent.run_assignment()` validates the assignment, reads the
  exact requirements and candidate from Blob Storage, generates a `Review`,
  validates its revisions/approval, and writes an immutable review JSON artifact
  before returning its reference.

The architect's `run_assignment()` is a five-stage recipe. The five methods sit
directly beneath it in execution order:

1. `connect_and_load_assignment()` registers Azure clients on the caller's
   `AsyncExitStack`, verifies the private storage path and assignment, and returns
   the Blob store, Foundry project, headers, assignment and any existing design.
2. `read_requirements_and_prior_work()` returns the model's input brief.
3. `load_or_create_llm_session()` returns the LLM conversation session store,
   session and model deployment, reconciling any completed design or pending call.
4. `design_solution()` generates design text or recovers a known model response.
5. `store_design()` validates and writes the candidate, saves the session, and
   returns its artifact reference.

The reviewer's `run_assignment()` uses the same five-stage pattern, with its
methods also directly beneath it:

1. `connect_and_load_assignment()` returns the Blob store, Foundry project,
   headers, validated assignment and any existing review, registering clients on
   the caller's `AsyncExitStack`.
2. `read_requirements_and_design()` returns a brief containing the exact
   requirements and candidate design.
3. `load_or_create_llm_session()` returns the reviewer's LLM conversation session
   store, session and deployment, reconciling any completed review or pending call.
4. `review_solution()` generates review text or recovers a known model response.
5. `store_review()` validates the review/revisions, writes the immutable review,
   saves the session, and returns its artifact reference.

Only each role's `run_assignment()` invokes its stage methods; stages do not call
each other. Completed-design/review early returns remain visible after session
reconciliation, without repeating inference or storage. Each orchestrator owns its
`AsyncExitStack`, including cleanup when connection setup fails partway through.
No pipeline framework or shared runtime wrapper is involved.

Both roles keep their own
pending-model journal, known-response recovery and existing-output reconciliation;
the read/generate/write sequence remains understandable within each role's file.
Both roles' first stages explicitly construct
Azure SDK `ManagedIdentityCredential`, `BlobServiceClient`, and the Foundry
`ProjectClient` (an `AIProjectClient` subclass). The stack closes these clients
on success, failure, or cancellation.
Private-path verification precedes artifact reads. The existing exact-origin,
no-retry Foundry transport is retained, as are Blob timeouts, private-network
checks and disabled proxy inheritance. There is no specialist dependency on
`WorkflowRuntime`, resource tuple, or new service abstraction.
The model itself receives input content and returns JSON; it has no storage tools.
Shared scoped access, serialization and immutable writes remain in
`demo\artifact_store.py`. `demo\specialist.py` shares only model instruction
formatting and agent resource cleanup; it is not another deployed agent.
`WorkflowRuntime.specialize()` passes explicit trusted hosting values to the appropriate class method.
MAF graph execution, trusted hosting checks, coordinator resource setup and coordinator
publication remain in `demo\workflow.py`. Locator contracts live with the
artifact/assignment schemas in `demo\artifacts.py`. Routing helpers remain in
`demo\routing.py`; Decision-1 is not a fourth hosted service.
Assignment/output locators require integer schema version 1 in their Pydantic
contracts, so agent/coordinator flows do not repeat version branches. Unsupported
versions fail as `ValidationError`; the coordinator retains an uncertain effect
without accepting the output. Deployment checks can validate fixed configuration,
but cannot replace request-time identity/scope, revision, deadline, artifact
integrity or model-response recovery checks. Those gates remain in the live path.
The migration map retains the original source filenames and hashes as history,
not as a current application-file inventory.
This source map describes code paths; it is not evidence that live
managed-identity Blob access or hosted acceptance has passed.

## Implementation status

This describes implemented source, not live acceptance or a fresh deployment
inventory. The workflow/artifact/routing code and offline tests exist; the
descriptor configures MAF hosting and remote specialists. Determine current
deployed status from current observations; this source document supplies no
live pass or active failure. Historical versions, failures and delivery
ownership remain opt-in context through the historical index.

The submitted invocation authorizes scoped implementation, azd delivery and
synthetic acceptance in the existing nonproduction project. Preserve actual
held operations and unknown effects without importing old diagnoses as
blanket blockers. See [the implementation workflow](implementation-workflow.md)
and [the mission](requirements/delivery-mission.md) for current acceptance.
The solution uses a Microsoft Agent Framework workflow, Foundry parent/child
sessions, strict specialist contracts, a durable operation journal and remote
Responses transport.

Exactly three hosted agent deployments are intended:

| Deployment | Responsibility | State/output ownership |
|---|---|---|
| Coordinator | Host the MAF workflow, authenticate the request, enforce gates, use Microsoft-Decision-1 for semantic choices, invoke remote specialists | Parent conversation, workflow checkpoint, operation journal, requirements and authoritative manifest |
| Architect | Read assigned requirements/review revisions and propose a candidate | Own child conversation and immutable candidate outputs |
| Reviewer | Read the exact assigned candidate and requirements and evaluate them | Own child conversation and immutable review outputs |

Do not instantiate specialists inside the coordinator in production or add a
fourth orchestration deployment. A local fake/in-process implementation remains
useful only as an explicit offline test adapter.

## State planes and identity

Three independent state planes have different purposes:

1. **Foundry conversation history:** the parent and each child have their own
   hosted session IDs and framework session representations. Pin each deployed
   version. Never use another agent's conversation object as shared storage.
2. **MAF workflow checkpoints:** resume stable workflow/executor IDs at supported
   superstep boundaries using the hosting SDK's supported checkpoint provider.
   Store through the supported Foundry-backed state integration, not in mutable
   conversation messages. Confirm APIs against the pinned SDK before coding.
3. **Blob artifact plane:** prerequisite documents, immutable specialist
   deliverables, validated decision records, a write-ahead operation record,
   and the authoritative manifest connecting accepted revisions.

Use a request-aware workflow factory and the supported
`CheckpointStoreProvider` integration if supported by the pinned hosting SDK.
Do not base the host on deprecated `workflow.as_agent()` APIs. If the pins cannot
support Foundry workflow hosting, document the exact incompatibility and make the smallest
coherent dependency update with compatibility tests and a regenerated lock.

The artifact conversation key is the **coordinator's trusted parent Foundry
hosted session ID**. A caller-supplied string or model-produced `session_id` is
not authorization. Derive the binding from validated request/platform identity.
Namespace it by canonical project, tenant and authenticated principal:

```text
v1/<project-scope-digest>/<tenant-principal-digest>/<parent-session-digest>/
    requirements/<requirements-revision>/<operation-id>.json
    decisions/<requirements-revision>/<operation-id>.json
    assignments/<operation-id>.json
    operations/<operation-id>/<transition>.json
    manifest.json
```

Candidates and reviews use the same trusted scope in their respective
containers. Digests produce safe bounded path components; persist the canonical
binding privately so digest equality is not mistaken for authorization.
Specialist child sessions differ from the parent. Issue a server-validated
assignment binding child role/session/version to that parent scope, operation,
exact inputs, permitted output type, and deadline. Verify the assignment on
every call, including resume. Do not let the model choose container names,
accounts, blob paths, tenant IDs, or parent IDs.

Existing hosted identities were observed and their exact container-scoped
grants applied. Actual runtime managed-identity Blob access and its private
network path have **not** been proven; verify them during live acceptance.
The subsequently approved trusted-lab policy adds account-wide Blob Contributor
for project agents, superseding effective per-role storage isolation.
Missing trusted principal context is a fail-closed condition, not permission to
use a default user. A terminal's UUID alone is not proof of ownership.

The baseline host's offline construction reports SDK response resilience
disabled: `store=true` alone does not recover an in-flight response after an
ungraceful crash. In the next iteration configure supported resilient hosting,
verify its storage integration, and test hard-kill/restart behavior. Where a
remote response remains unrecoverable, retain the explicit uncertain hold.
Neither a workflow checkpoint nor a stored conversation fixes this by itself.
The explicit acceptance restart uses the pinned hosted-session `:stop` API,
requires HTTP 204 and a new provider `stopped_at` in idle state, then continues
the same parent. Its durable write-ahead marker prevents resending an uncertain
stop. This tests supported compute deprovision/rehydration with persistent
volume, not an ungraceful hard kill or in-flight crash recovery.

## Blob access and network boundaries

Default to three containers in one private storage account: `control`,
`candidates`, and `reviews`. The names are generic configuration, not fixed
resource identities. Use separate managed identities for the three deployments.

| Identity | Control | Candidates | Reviews |
|---|---|---|---|
| Coordinator | Read/write | Read | Read |
| Architect | Read prerequisites | Read/write own outputs | Read assigned prior findings |
| Reviewer | Read prerequisites | Read assigned candidate | Read/write own outputs |

**Approved trusted-lab exception:** project agents now have account-wide Blob
Contributor access in the linked lab. The above matrix remains the application
adapter's ownership contract, not the effective Azure permission matrix.
Container-scoped grants are retained but cannot restrict an additional broader
grant. Immutable writes, assignment/parent checks and coordinator-only manifest
publication depend on trusted application code; an agent identity used outside
those adapters can read, overwrite or delete other roles' blobs. Do not claim
storage-enforced single-writer isolation or malicious-host isolation for this
lab. Live acceptance must report this limitation rather than expect RBAC
denials for cross-role access. This exception does not weaken schema, hash,
ETag, fencing, prerequisite or unknown-effect gates.

Use the least-privilege container-scoped data roles available; writer identities
may have delete permissions under built-in contributor roles. Enforce
append-only output semantics in application adapters, enable appropriate
soft-delete/versioning/retention, and assess custom roles or a broker if strict
storage-level immutability is required. The above matrix is a workload boundary,
not per-user isolation: Blob RBAC does not authorize arbitrary path prefixes.
Authenticate and authorize each artifact request in deterministic application
code. Do not expose general-purpose Blob read/write tools to the language model.
If directly invoked specialists cannot validate assignments with trusted
context, introduce a narrowly scoped broker capability or stronger service
authorization; do not pass storage account keys or trust JSON claims.

Use managed identity + HTTPS, disable public network and shared-key access,
avoid connection strings/account keys/SAS in prompts or evidence, and give the
runtime private DNS/network reachability to the Blob endpoint. Add DFS endpoints
and the corresponding DNS only if the selected storage mode actually uses DFS.
Verify checkpoint/history storage needs independently of this artifact account.
Do not assume creating a private endpoint makes hosted compute reach it.

Terraform, network/DNS configuration, registry allocations, and private
connectivity live in the lab repository. When adding a private zone there, also
add the private and public-equivalent VPN conditional forwarding entries in
the same change. Installation on the VPN server remains a user action.

## Artifact contracts

Use strict, versioned schemas with unknown fields rejected and bounded payloads.
An artifact envelope contains:

| Field | Requirement |
|---|---|
| `schema_version`, `artifact_type` | Supported version and typed document kind |
| `scope_binding` | Trusted project/tenant/principal/parent binding or its verified digest |
| `operation_id` | Application-issued idempotency key, not a model-generated ID |
| `producer` | Agent role, deployed name/version, child session and response IDs when applicable |
| `input_refs` | Exact immutable object names, hashes, schema and requirements/candidate revisions |
| `requirements_revision`, `candidate_revision` | Explicit causal relationship; review refers to the exact candidate |
| `content`, `content_sha256` | Canonical UTF-8 payload and deterministic verified digest |
| `publication_state` | Output is a proposal until coordinator acceptance |

Hash canonical serialization with nonfinite numbers rejected. Separate service
metadata from model-produced content. Define maximum bytes, nesting depth,
artifact count, and allowed media types before implementation. Treat text in
artifacts as untrusted data, not authority or executable instructions.
Do not substitute an alias, a mutable "latest" link, or a newly generated
requirements summary for the exact referenced source. Keep source provenance
and explicit ordered chunks when bounded routing context is constructed.

Specialists read only the assigned immutable inputs through typed adapters.
Architect emits a candidate whose revisions match the assignment; reviewer
emits an approval or blockers whose requirements and candidate revisions both
match. A review cannot approve while containing blockers. Malformed,
truncated, oversize, contradictory or stale outputs do not become ready
artifacts. Preserve existing baseline parsing/normalization regression tests,
but document intentional tightening instead of silently repairing content.

## Manifest publication and concurrency

The coordinator is the **sole authoritative manifest writer**. Specialists
write immutable operation-specific proposals, never the shared manifest.
Create outputs with `If-None-Match: *`; verify an existing object's hash and
provenance before treating it as an idempotent duplicate. A name collision with
different content is an integrity error.

Publish in this order:

1. Load and verify the session binding and current manifest generation/ETag.
2. Persist a pending operation with exact prerequisite references and reserved
   output name before any remote effect.
3. Invoke the pinned child session/version; record its response ID as soon as
   observable, without waiting for a final answer.
4. Specialist reads assigned inputs and writes its immutable proposed output.
5. Coordinator validates completion, ownership, input hashes, strict schema,
   revisions, producer version, and output hash; then conditionally updates
   the manifest with `If-Match: <observed-etag>`.
6. Mark the operation accepted and record the resumable workflow checkpoint.

On an ETag conflict, reread and reconcile the recorded operation and revisions.
Do not issue another specialist call as a conflict retry. One active writer
lease or equivalent fenced claim per parent must protect cross-instance turns;
ETag checks still protect publication if a lease expires. Define lease renewal,
fencing and crash recovery explicitly. A Windows local file lock is not
distributed coordination.

Downstream prerequisites are ready only when listed as accepted by the
manifest. Blob existence or a child completion event alone is insufficient.
New user requirements create a new revision and invalidate the current
candidate/review chain. No previous approval carries over automatically.

## Recovery and exactly-once limits

MAF superstep checkpoints are not a distributed transaction with Foundry
Responses or Blob publication. **Keep an application write-ahead journal** and
stable operation IDs to reconcile uncertain remote side effects.

| Observed recovery state | Safe action |
|---|---|
| Child creation pending, ID persisted | Query that exact session and reconcile its version/binding |
| Call pending, response ID persisted | Recover that response; do not create another response |
| Output exists, manifest not published | Verify exact provenance/hash and publish conditionally |
| Manifest accepted, checkpoint older | Reconcile the accepted operation without replaying the effect |
| Call may have happened, no recoverable response ID | Hold as uncertain; surface the condition for reconciliation |
| Expired/deleted session, changed deployment version, incompatible state | Stop or use an explicit reviewed migration; never silently start over |

Retries are bounded and permitted only where idempotency/recovery is established.
Record retry budgets and reconcile before resending. Resume restores child IDs,
deployed versions, requirements revision, artifact refs, pending effect,
manifest generation, and MAF workflow position. A new process must not
clear pending state or switch from remote to in-process to appear successful.

Define retention, user deletion/export, and encryption policies across all
three state planes. Ordinary cleanup must not delete pending operations or
prerequisites needed by resumable sessions. Deletion requires explicit scope
and authorization; do not write an automatic destructive migration.

## Microsoft-Decision-1 routing

Use Microsoft-Decision-1 for the coordinator's semantic choices, not to generate
designs or authorize actions. Reuse the **contract pattern**, not environment
secrets or the whole application, from the sibling think-fast project:
`.contracts/decision-provider.yml`, `.contracts/decision-runtime.yml`, and
`docs/shared-routing-policy-design.md`. The shared-routing design is a proposal;
verify implemented provider behavior against the pinned API/SDK.

Deterministic code first computes allowed actions:

| Choice | Deterministic prerequisites |
|---|---|
| Ask architect | Bound session, accepted requirements, remaining budget, no unresolved effect |
| Ask reviewer | Accepted current candidate and exact requirements refs |
| Finish | Current review approves the current candidate with no blockers |
| Request input | Safe clarification/hold path; cannot conceal transport or integrity errors |

Do not call a model when a deterministic next action suffices or no safe action
is available. Where a semantic choice remains, send bounded application-owned
state, explicit alternatives, decision criteria, exact revision/provenance
references, and relevant findings. Do not share mutable agent conversations.
The criteria should distinguish missing user information, needed design
revision, review readiness, and final readiness.

Validate the provider response against its actual decision wire contract:
typed action/probability associations, unique allowed choices, finite values
in range, valid distribution where required by that contract, and bounded
usage metadata. Do not invent a probability format or treat a generative
response as a Decision-1 result. Pin the deployment alias through configuration.
Persist the input schema/policy/model versions, state hash, candidate choices,
provider outcome, probability information, measured usage, and final gated
action in an immutable decision record.

Probability is a selection signal, **not** permission. Calibrate confidence
threshold and margin/abstention policy using a checked-in evaluation corpus;
do not copy a hardcoded threshold just to avoid clarification. Invalid,
unavailable, or low-confidence routing is explicit; it never falls back to
an unapproved model or bypasses prerequisites. A deterministic safe hold may
be used with its reason, distinct from user-information clarification.

The earlier lab context recorded a 17 RPM Decision-1 deployment limit; that is
historical context, not a new quota check or a portable default. Verify live
capacity before deployment. Use configured bounded admission control and
shared enforcement across coordinator instances, cancellation, deadlines, and
bounded 429 handling. Do not create a scaling/benchmark loop or alter quota
under this task.

## Compatibility, evidence, and acceptance

The current [mission](requirements/delivery-mission.md) defines acceptance and
safe delivery. Establish any identity-propagation failure from current evidence,
not an inherited plan or historical diagnosis. Preserve this architecture
rather than replacing user identity with a session ID or an assignment field.

Preserve the Responses streaming/final aggregation contract, role routing,
alias-versus-real-ID distinction, terminal pending-turn holds, strict revision
checks, stored remote response recovery, and credential-free artifact contents.
Version new manifest/workflow schemas independently of the baseline ledger.
Document whether old sessions remain on their old version or migrate through
an explicit adapter; do not reinterpret old state as new schema.

Offline acceptance covers role access, trusted scope isolation, exact-input
revision checks, malformed artifacts, duplicate/conflicting publication,
cross-instance ETag/fencing conflicts, Decision-1 contracts, budgets, transport
errors, cancellation, and crashes at each publication boundary. It must prove
no duplicate remote effect after process restart where recovery is possible,
and an explicit hold where it is not.

Live acceptance must prove all three intended deployments/versions, remote
specialist calls rather than in-process calls, actual managed identity Blob
access over the private path, parent continuity across turns/restart,
isolated parents, prerequisite consumption, accepted candidate/review hashes,
and Decision-1 routing evidence. Inspect synthetic outputs and sanitized
metadata, not secret-bearing transcripts. A passing offline test, copied azd
environment, successful upload, or healthy host alone is not this acceptance.
