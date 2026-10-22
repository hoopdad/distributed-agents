# Private scenario collection: pinned public-seam qualification

## Decision and boundary

Developer task **IP-C1-COLLECTION-SEAMS**, originating in IP-S3 criteria
0/1/2/5 and specification Required acceptance 7. This is offline qualification,
not a collector implementation, permission resolution, live observation or
release acceptance. The smallest usable result is **partially feasible with
specific unqualified joins**, not a claim that the aggregate can now be collected.

Source inspected on `feature/customer-hosted-session-prototype` at
`ef6cbc4d87d3408f9d08b9f8e712205a0e5d8841`. Runtime remains the accepted
`c52786b7dd1595f3048a78061f893dc79635069f`; the accepted
[companion](identity-candidate-handoff.md#ip-s3-prospective-acceptance-companion--october-22-2026)
is `1d6f88308cadeb120bef0f19eac7101a2859caa4`. Opened original companion audit
`840944fb5b24b2469ada0c3d4f50b88871e28a2ceea99150fec5b36ccc00be23.json`
under the bound run's project-relative context directory: Architect/Critic
each agree and mark that documentation task complete. Its missing live
collection handoff is not reopened or silently satisfied here.

New files are this matrix and `tests/test_scenario_collection_seams.py`;
the index is refreshed. No runtime, validator, companion, schema, package or
selected-lab source changes. Existing native-preflight denial is not retried.
Historical COMMON rollback provenance remains **WAIVED, never PASS**.

## Pins and evidence vocabulary

The existing explicit Python was used without installing dependencies.
Observed installed versions match `requirements.txt`:
`agent-framework-core==1.21.0`,
`agent-framework-foundry-hosting==1.0.0b261002`,
`azure-ai-agentserver-core==2.2.0`,
`azure-ai-agentserver-responses==2.3.0`,
`azure-ai-projects==2.7.0`, `azure-storage-blob==12.31.0`,
`agent-framework-foundry==1.14.0`, `openai==3.24.0`, `httpx2==2.13.1`.
Paths below are relative to that interpreter's `site-packages`, not private
environment data. Public classes are imported from documented package exports;
underscored implementation files are **read-only source references**, not hooks.

- **Fixture-qualified:** public API executed with synthetic input/local SDK
  persistence or a synthetic transport; not a hosted behavior attestation.
- **Source-only candidate:** inspected public option, but this task does not
  claim an executed collector or complete service enumeration through it.
- **Unavailable now:** current runtime/capture cannot supply an attributable
  aggregate association. A proposed adapter does not change this status.

| Pinned source | Relevant public API / lines |
| --- | --- |
| `agent_framework/_sessions.py` | `AgentSession.to_dict/from_dict`, 1883-1922 |
| `agent_framework/_workflows/_checkpoint.py` | `WorkflowCheckpoint` and shallow `to_dict/from_dict`, 34-131 |
| `agent_framework_foundry_hosting/_state_store.py` | `FoundryCheckpointStore.save/load/load_with_hash/list_checkpoints`, 138-218; `CheckpointStoreProvider.validate_checkpoint_value/get_store/get_store_for_scope`, 259-314; `FoundryAgentSessionStore.get/set`, 427-458; `AgentSessionStoreProvider.get_store`, 492-494 |
| `agent_framework_foundry_hosting/_scope.py` | `FoundryRequestScope.from_context`, 23-58 |
| `agent_framework_foundry_hosting/_request.py` | `HostedResponseRequest.__init__`, 153-166: copied request, scope, exact response ID |
| `agent_framework_foundry_hosting/_responses.py` | `ResponsesHostServer.__init__`, 665-909: public `prepare_options`, `checkpoint_store_provider`, `response_store` |
| `azure/ai/agentserver/core/storage/_state.py` | `FoundryStateStore.get_or_create`, 242-317; `get_item`, 476-500; `list_keys`, 549-611 |
| `azure/ai/projects/aio/operations/_operations.py` | `AgentsOperations.create_session`, 1769-1866; `get_session`, 1868-1936; `list_sessions`, 2054-2148 |
| `azure/storage/blob/aio/_container_client_async.py` | `ContainerClient.list_blobs`, 811-902; source-only candidate |
| `azure/storage/blob/aio/_blob_client_async.py` | `BlobClient.download_blob`, 680-815; source-only collection candidate, distinct from application `read_manifest` fixture |

Exact inspected source SHA256 anchors (not release/package seals):

| Source | SHA256 |
| --- | --- |
| `agent_framework_foundry_hosting/_state_store.py` | `8b7dcc45484f2a10f2b460bf51e40c1d6c4bea174bc4728c77d667a4294754ac` |
| `agent_framework_foundry_hosting/_request.py` | `f892ca11971329a3ce69d1ea0fdc5546282548cd54e7632ee5abb4296504fc83` |
| `agent_framework_foundry_hosting/_workflow_state.py` | `faa88ee4f082aa70fc203db82f23b12e6ac3c2d661dbd62de6a1cb76dd9280e3` |
| `agent_framework_foundry_hosting/_workflow_responses.py` | `ee9b5000d8a7194831dbef866c8fa863a3a5831a44ab02d61e450524747fbffd` |
| `azure/ai/agentserver/core/storage/_state.py` | `d1db57c626c58ed9b9628e68edf435c3f171e30f2f66bcc0e330e910ef040dbf` |
| `azure/ai/projects/aio/operations/_operations.py` | `5a6a569f2700c0146b20e3a1a8a5992f2c9a351050a5025d2023f4f7bf84340b` |

## Feasibility matrix against existing aggregate fields

The contract remains `live_acceptance.validate_scenario_evidence`, especially
`_evidence_turn`, `_evidence_continuation` and its checkpoint/stop comparisons
(`live_acceptance.py:357-629`). Validation checks supplied observations, **not
their origin**. No new field or validator copy is introduced.

| Existing field / owner | Public seam and actual qualification | Scope, completeness, consistency and remaining gap |
| --- | --- | --- |
| `manifest`; artifact refs in `proof` | `demo/artifact_store.py:BlobArtifacts(service=...)`, `read_manifest`, `read_artifact`, `lock_manifest`; fixture-qualified with the existing `MemoryBackend` service injection. | Scope originates in `ScopeBinding.from_platform`, not a collector input or model text. Manifest is a mutable ETag-fenced current head, not a history listing. Capture the exact turn/generation/active response and immutable refs, retain the bytes privately, and reject changed head/ref/scope. Separate reads are not a transaction. Fixtures reject cross-scope and missing manifest. They do not verify private Blob DNS, real ETags or cloud access. |
| Cumulative `operations` | `WorkflowRuntime.transition` (`demo/workflow.py:577-586`) writes `{scope_binding,effect}` via `BlobArtifacts.write_operation`; fixture-qualified immutable transition retention, same-byte idempotence and changed-byte collision rejection. | `BlobArtifacts` has **no public operation enumeration/read collection API**. Source-only lower SDK candidate: existing authenticated `BlobServiceClient.get_container_client(...).list_blobs(name_starts_with=scope.prefix+"operations/")`, then named `get_blob_client(...).download_blob()`. An external reader needs the actual trusted scope and approved existing client/auth route, not discovery by principal hashes. Exhaust every page/continuation, preserve raw named transitions including UNKNOWN/failed, reject duplicate/cross-scope/missing records. Neither manifest.effect nor accepted refs identify every prior operation. Blob listing is not a multi-object snapshot; quiesce the owned turn and recheck head/read bindings. No live or synthetic paginated Blob enumerator is claimed here. |
| `checkpoints.scope_binding`, `checkpoints.records` | Public `ResponsesHostServer(prepare_options=...,checkpoint_store_provider=...)`; a fixture-only `CheckpointStoreProvider` subclass delegates `get_store_for_scope`, retaining actual context ID and public scope beside `HostedResponseRequest.response_id`. The real pinned local resilient host executes two independent synthetic background responses and exports stored specialist checkpoints. | Positive local association: response -> trusted SDK scope -> actual provider context -> loaded records. Request-local ContextVar is reset by fixture ASGI middleware; background ownership and concurrent scope stay separate. This is **not** a deployed collector, coordinator execution proof or crash-context guarantee. The SDK's `get_store` rejects absent user/call and mismatched hosted session before creation; fixtures test that without claiming local backend authorization. |
| Checkpoint persistence and JSON attachment | `FoundryCheckpointStore.save/load/load_with_hash/list_checkpoints` are fixture-qualified via temporary local SDK persistence. Plain-JSON records attach to the retained aggregate validator and its missing/duplicate/cross-scope rejection unchanged. | **Actual native checkpoint export is not directly JSON serializable.** `to_dict` is shallow and actual local native state contains `WorkflowInvocationKwargs`; direct JSON raises `TypeError`. The fixture retains this negative result; no `default=str`, type stripping or private checkpoint codec is used. Typed checkpoints can load and return their exact persisted encoding hash, but the current aggregate records need an explicitly justified public serialization/projection contract. Successful plain-JSON attachment does not solve this gap. |
| Checkpoint enumeration/immutability | `FoundryCheckpointStore.list_checkpoints(workflow_name=...)` source loops `list_keys(after=...)` and `get_item` through pages. Lower `FoundryStateStore.list_keys(limit=1,after=...,order="asc")` pagination/missing item is fixture-qualified locally for an explicit fixture-owned name. | Public store needs **actual context ID**, not just parent/workflow/graph. SDK read-only evidence `_workflow_state.py:541-551` derives it from scope and lineage; `_workflow_responses.py:409-447` prepares the run after the public options hook. No public offline workflow-binding-store export supplies that response/lineage pair. Do not derive/reproduce private naming hashes. `list_checkpoints` can skip items removed between list/get; no atomic snapshot/completeness attestation. Duplicate or changing pages must remain failures; do not deduplicate receipts. `save` can overwrite an existing checkpoint ID (fixture demonstrates changed hash); iteration count is not unique. Freeze retained before/after receipts and compare IDs, graph and state, never latest-only. |
| `creations` | Public `ProjectClient(...,transport=synthetic_transport)` and `agents.create_session` fixture executes the pinned pipeline with synthetic credentials/HTTP 201. Actual wire body contains reserved hosted session ID and version, **not journal operation ID**. | SDK boundary can expose target/version; current app diagnostics reduce route/presence and cannot attribute each attempt to a trusted operation. `RemoteAgents.create(child)` and workflow create write-ahead operation require an explicit source-owned association at dispatch plus independent final transport observation. Parent creation is separate from these exactly-two specialist creations. `list_sessions` is a paged current resource listing, not once-only creation evidence; neither it nor GET status reconstructs missed boundary sends. |
| `sends` | Application `WorkflowRuntime` dispatches a typed `AssignmentLocator` to `WorkflowRemoteAgents.invoke` / `RemoteAgents.invoke`; actual Responses uses `ProjectClient.get_openai_client` and `OriginTransport`, not Azure Core. | **Unavailable exact live boundary-to-operation accounting.** Locator carries operation ID to invocation, but neither existing diagnostics nor timing/role/local aliases form an authoritative bridge to each actual POST. A journal intent/dispatched/accepted transition is not an independent HTTP count. Retain repeated attempts as repeated entries (aggregate rejects duplicates), known-response retrieval as GET only, and distinguish specialist Responses POSTs from downstream model/Decision requests. No fixture here claims to have installed a wire collector. |
| `stops`; `restart.proof.hosting_restart`; `stopped_session` | `live_acceptance.stop_hosting_for_acceptance` writes private pre-stop intent, calls `http.request("POST", ...+":stop")`, requires 204 and reads session status/stopped_at; source reference `live_acceptance.py:183-233`. | **Unavailable independent stop boundary capture in current aggregate runner.** Need exact parent/version, one actual POST occurrence, original 204 receipt and monotonic stopped_at readback. Durable `stop_pending` or later idle cannot supply missing HTTP receipt or another allowed stop. Keep an uncertain stop held; never replay to fill evidence. No send/stop was executed by this task. |
| Model-history provenance (supporting companion obligation, **not a new aggregate field**) | `ArchitectAgent.load_or_create_llm_session/design_solution`, reviewer equivalents; named public `AgentSessionStoreProvider(store_name="specialist_history_v2").get_store(...).get("history")`. Public `AgentSession.to_dict/from_dict` and store get/set are fixture-qualified locally. | Captures service_session_id, framework ID and actual pending-operation state at the seam, not an input-history attestation. Application stores pending `id`, input_sha256, deployment and response_id; store snapshot alone does not prove what a model consumed. Need before/after snapshots associated with exact specialist operation and actual model boundary previous response/messages provenance, without raw bodies in diagnostics. `responses.retrieve(known_id)` does not send again or prove original model input history. SDK-internal outer history/response stores are not specialist model history. Current aggregate validator does not independently assert that history; retain it as missing evidence rather than inventing schema/PASS. |
| `proof` metadata, child readbacks and final scenario join | Existing `live_acceptance.run`, `events`, `validate_artifact_evidence`, `validate_exercised_versions`; accepted companion. | Current runner emits only part of the aggregate. Final all-scenario validation is a join, not a scheduling dependency that makes successful recovery necessary for independent isolation. Current package/three-role version bindings, actual effects, completed non-held initial turn and owned cleanup remain original DevOps/E2E obligations. |

**Read effects and page termination:** the pinned Foundry checkpoint/session
helpers obtain their lower store through `FoundryStateStore.get_or_create`;
even a load/list can therefore resolve or create a missing store. Do not call
that a guaranteed read-only remote export. The fixtures use only temporary
local stores. A receiving adapter must use the already-owned authorized
runtime store and its actual association, or an explicitly qualified existing
store reader; arbitrary context/name probing is not allowed. The checkpoint
page loop stops on `not has_more` **or a missing last_id**. A missing cursor,
truncation or disappearance during traversal cannot attest completeness.

## Smallest justified next adapter contract (not implemented)

Retain the existing private aggregate keys and current terminal/stdout contract.
No generic event ledger, diagnostic identity fields, new hosting role or private
SDK method is required or authorized by this qualification.

1. **Read-only immutable/current-state reader:** consume an explicitly
   attributed current manifest/head and exact typed artifact refs through the
   existing authorized client. For operations, qualify the source-only paged Blob
   candidate above before claiming completeness. Retain every distinct named
   transition and its source receipt, not intentions masquerading as sends.
   Take a quiescent owned-turn capture, verify the head/generation did not move
   during reads and keep earlier immutable snapshots; fail closed on gaps.
2. **Checkpoint attachment:** public options hook can establish a private
   request-local `(response_id, SDK scope)` tuple; delegated provider
   `get_store_for_scope` can retain the real opaque context ID and scoped store.
   This exact association is now fixture-qualified in the real local host.
   Compose with existing hooks and ASGI reset; preserve retry/stream/background
   behavior. Do not reconstruct identity/scope from headers or infer lineage
   from clock/iteration/parent. Persist only allowlisted private receipt values,
   never SDK objects, settings or raw identity in public diagnostics. Cold-process
   recovery requires a captured authoritative association or stays unavailable.
3. **Resolve typed checkpoint export before adapter construction:** actual
   loaded state is richer than JSON. Original Architect/Scrum should decide the
   smallest supported serialization/projection preserving state equality for
   the existing comparison, or request a bounded SDK public export handoff.
   Do not import private encoders, read guessed SDK store names, silently drop
   typed state or add fields to the acceptance contract under this task.
4. **Independent boundary adapter:** a separately scoped application correction
   must attach trusted exact operation/role/target at actual dispatch to
   application-owned Project/httpx2 transports and the retained stop client.
   Capture each actual matching POST and its response/error without retries,
   body consumption, deduplication or authorization change. Retain duplicates
   and incomplete observation windows as failures; compare the captured list
   against journal operations only afterward. Session IDs, diagnostic aliases
   and journal states alone are insufficient. Qualify this bridge with negative,
   duplicate, concurrency and known-response-only fixtures before live use.
5. **Model history:** use the application-owned specialist store's actual
   before/after pending-operation and service continuation snapshots together
   with an independently attributable model request boundary. If a supported
   public observation cannot establish consumed history, return that exact
   missing comparison; do not use final prose or a stored ID as substitute.

Items 1/3/4/5 are **not working collection capabilities**. The bounded
qualification can complete with these actionable negatives; implementing them
would be new scoped work routed by existing Architect/Scrum, not a hidden runtime
change here. Qualification does not re-authorize a denied operation.

### Minimal receiving handoffs

- **Original Architect/Scrum Master:** exact qualification commit and fixtures;
  choose only necessary serialization and independently attributable-boundary
  follow-on work. No re-review of the accepted companion or source inventory.
  To close typed-state export uncertainty, supply a supported public round-trip
  for one real typed native checkpoint and demonstrate preserved comparison
  state. To close offline lineage discovery, supply an authoritative previously
  captured response/scope/context association, not a guessed hash.
- **Original E2E/DevOps evidence owners:** after native readiness and current
  automated package/source/version/trusted-host/effect gates, collect private
  receipts for the specific missing operations/windows, actual scoped
  checkpoint pages, immutable transitions, model continuity and owned cleanup.
  Preserve missing 204/UNKNOWN receipts and held parents. No external upload,
  credential retrieval or provider tracing is needed for this qualification.
  A required unsupported external comparison must be handed off with its exact
  missing record and smallest authorized action; no live origin is asserted.
- Exact prior references
  `["yaml-loops-v1:sprint/1/IP-S1/DevOpsWorkLoop","RELEASE-COMMON-PACKAGE-PUBLICATION"]`
  and `["yaml-loops-v1:sprint/1/IP-S1/DevOpsWorkLoop","RELEASE-LIVE-ACCEPTANCE"]`
  remain unmet original release duties, not prerequisites to offline research.
  Accepted credential-timeout/changed-join/planning dispositions retain their
  originating task boundaries; none is superseded here.

## Executable qualification and verification

`tests/test_scenario_collection_seams.py` uses temporary
`AGENTSERVER_STATE_ROOT` and the SDK local backend (never the user's default
state root). Existing synthetic workflow/transport fixtures are reused;
no SDK internals are patched. The pinned actual host uses ASGI in-process
traffic only. Public store construction validates synthetic hosted scope while
its persistence backend remains local: this distinction is intentional.
Local hashing/partitioning never proves real authentication or service isolation.

The 13 focused fixtures cover pins, immutable operation retention/collision,
manifest missing/cross-scope rejection, duplicate JSON keys, scoped checkpoint
partition/rejection, shallow snapshots, changed-ID overwrite, local lower-store
pagination, session persistence limits, actual Project constructor/pipeline,
public host options/provider association, actual typed-JSON failure, and
unchanged aggregate rejection of missing/duplicate/cross-scope inputs.
The aggregate attachment uses existing offline graph captures, not a copied
validator or freshly invented successful live receipts.

Commands (substitute the private invocation's explicit existing absolute roots):

```powershell
& <absolute-python> -m unittest discover -s tests -p test_scenario_collection_seams.py -v
.\Test-Demo.ps1 -Python <absolute-python> -LabRepositoryRoot <explicit-selected-lab-root>
& <absolute-python> scripts/repo_index.py
.\scripts\Test-Repository.ps1 -Python <absolute-python>
```

Final observed check results and exact resulting commit are returned in the
DeveloperWork handoff/commit message. Initial fixture probes incorrectly used
HTTP 200 for a create API requiring 201, then an incorrect ResponseStore import
and the coordinator workflow name for a specialist graph; corrected those test
assumptions, not production behavior. The subsequent actual typed-checkpoint
JSON failure is retained as a negative finding, not hidden behind a serializer.
The first full run also exposed test-only resource leakage: invoking cleanup
on an unstarted helper `IsolatedAsyncioTestCase` did not close its resource
stack. The new fixture now registers that stack directly on the running test,
with explicit environment/logger/clock restoration assertions. No baseline
test or runtime rejection was weakened to repair the two logger failures and
host-backend error caused by that leak. After correction, focused fixtures
passed (13 tests in 3.390 seconds); documented application checks passed
dependency validation, 291 tests in 54.196 seconds and compilation. Repository
checks passed a refreshed 117-file inventory, public boundary, JSON, PowerShell,
frontmatter and whitespace. These counts include the preserved unowned public
specification/index overlay; they are not clean-checkout certification.
No lab source changed, so affected retained release-tool checks are not required.
No package, live invocation, stop, permission-denial retry or push occurred.
