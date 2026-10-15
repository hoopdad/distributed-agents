# Distributed agents: native workflow and shared artifacts

## Status and intended change

This describes the implemented native design, not a claim of live acceptance.
Native workflow/artifact/routing source and focused offline tests now exist;
the deployment descriptor selects native hosting and remote specialists.
Application tests pass on Windows and Linux/amd64. The lab applied the 14
artifact resources and verified scoped zero-change convergence; private
container, identity-grant and retention metadata checks pass. Reproduced bundled
publication is complete: architect 17, reviewer 15 and coordinator 22
are active on SHA256
`51064aa426d28d0cfa6b126eac7fce5ab0e9a5a0667267ef105884c1805adde2`,
with unchanged identities and earlier/diagnostic versions retained.
Coordinator 19's earlier diagnostic release established the original failure:
`DECISION_CALIBRATION_PROVENANCE`: the Windows loader converted an absent fact
sheet into a blank variable during calibration; deployment omitted it and used
the nonempty public default. The correction truly removes absent optional
settings, requires explicit nonempty release facts and forwards them to all roles.
A fresh evaluation exposed a missing-workload ambiguity. Routing-v3 distinguishes
fact-sheet constraints from missing user purpose; its genuine twelve-call
calibration passes all eight ready and four missing-input cases. The unchanged
selection algorithm selects threshold 0.5/margin 0. Historical observations and
the retired calibration remain intact; the frozen corpus/coverage gates are
unchanged. Corrected facts and calibration are deployed. Initial live execution
writes requirements and a routing decision, but the architect fails during SDK
hosting preparation (`RuntimeError`, provider `storage_error`) and the coordinator
preserves the known effect as uncertain after timeout. This is not proof of a
permission problem. Read-only observation retrieves the exact child response and
bounded sanitized logs. Deployed SDK-boundary diagnostics identify
`NATIVE_HOST_PRINCIPAL`: the architect has no trusted user context before the
application factory. The actual pinned-SDK HTTP-edge test preserves delegated
headers, and read-only coordinator RBAC inspection confirms the explicit
`UserIdentityImpersonation/action` grant already exists. Neither observation
authorizes substituting a principal inside the container or weakening
`FoundryRequestScope`. Supported platform/SDK identity propagation remains a
live blocker. Known-response stream recovery is deployed; the fresh coordinator
preserves `SPECIALIST_INCOMPLETE` without resend or concealment.
Read-only existing Azure Monitor telemetry further confirms the known architect
enters the SDK with call identity but no user identity, while its coordinator
enters with both; the correlated architect Responses POST returned HTTP 200.
This rules out loss solely during background recovery, but is not a live wire
capture. The deployed propagation change uses the pinned SDK's
`context.platform_headers()` for native internal calls rather than re-delegating
the already-derived user ID or forwarding a container-only identity header.
The legacy transport is unchanged. Following explicit approval to start the
existing command VM, fresh guarded connectivity and all three publications
passed, with unchanged identities and proven process/mount cleanup.
Fresh initial acceptance on these versions still holds `SPECIALIST_INCOMPLETE`.
Read-only exact-response observation confirms architect 17 fails
`NATIVE_HOST_PRINCIPAL` with call identity present and trusted user absent.
Thus SDK-supported opaque propagation alone did not resolve the live failure.
The unresolved propagation boundary is not proof of a platform defect or a
missing permission. Trusted scope gates remain strict; followup, hosting
stop/resume and isolation were not reached. Owned jobs/listeners closed after
both acceptance and observation.
Local, undeployed HTTP-edge diagnostics compare the actual outbound opaque
call header with the captured request context, exposing only presence/match
booleans and an allowlisted role. A response-ID hash binds the observation
without logging raw IDs, identity/header values, tokens or content; it grants
no authority. Known-child failure observation additionally reads the exact
parent's bounded logs. No trusted-scope or legacy transport behavior changes.
Pending states and response IDs remain preserved; no repeat inference was sent.
Offline construction is not proof of hosted identity/context correctness.
Completed remote specialist work, end-to-end managed-identity artifact
provenance, two-parent isolation and actual hosting restart/resume remain
unverified. Metadata is not managed-identity data-plane proof.
All four real twelve-case calibration journals remain preserved, including both
failed evaluations and the earlier blank-facts success. The public routing-v3
calibration binds full request hashes to the current policy and explicit facts;
the corpus's v1 dataset metadata is not a policy downgrade.
The preserved baseline has a handwritten coordinator, durable operation ledger,
Foundry parent/child session handling, strict specialist contracts, and optional
remote Responses transport. Its explicit legacy adapter still supports
`in_process` specialists for regression coverage. The target replaces orchestration with a native Microsoft Agent
Framework workflow and explicitly deploys remote specialists. Keep the baseline
available until the new implementation passes offline and live acceptance.

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
support native hosting, document the exact incompatibility and make the smallest
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
stable operation IDs; replacing the handwritten coordinator does not eliminate
uncertain remote side effects.

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
manifest generation, and native workflow position. A new process must not
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
