# Identity profiling: pinned SDK coverage inventory

The original inventory below retains its research baseline and negative probes.
The [SDK-POLICIES implementation delta](#sdk-policies-implementation-delta)
records the subsequent bounded application attachments and remaining call-site
handoffs. Neither section is a universal coverage or live acceptance claim.

## Scope and evidence

Developer inventory for IP-S1-SDK-INVENTORY, against application baseline
`ddd376d9af37661e1126258896c72c1efdf73dc6` on
`feature/customer-hosted-session-prototype`. This is a source/constructor
inventory, **not installed profiling, a successful live hook or release acceptance**.
It consumes the October 21 IP-S1 overlay in
[SprintArchitecture](customer-prototype-sprint-architecture.md) at `9367939`
and its supplied agreement audit
`0ce2eb36318f8583f59e58ce5afac4b1b6edd92b02df6ff1d3db9af2211c17db`.
No prior dispositions or reconciled corrections were supplied for this task.
The existing trusted-identity, streaming, background, recovery and effect gates
remain mandatory. Historical rollback provenance is WAIVED, never PASS.

Installed distribution metadata was read using the existing linked lab Python:
Foundry hosting `1.0.0b261002`, AgentServer core `2.2.0`, Responses `2.3.0`,
AI Projects `2.7.0`, Blob `12.31.0`, Identity `1.25.3`, Azure Core `1.41.0`
and httpx2 `2.13.1`. These match the application manifest/lock pins.
SDK references below are paths **relative to that interpreter's site-packages**,
not suggestions to edit SDK files. Private settings, token caches and credential
values were not read. No dependency installation, network request or token
acquisition was used for this inventory.

## Source reference key

| Key | Exact pinned source seam |
| --- | --- |
| P | `azure/ai/projects/aio/_client.py:77-102`: default Azure Core policies and `AsyncPipelineClient(..., **kwargs)`; `_patch.py:155-224`: public OpenAI factory forwards kwargs to `AsyncOpenAI`. |
| C | `azure/core/_pipeline_client_async.py:130-141,185-264`: documented `per_call_policies`, `per_retry_policies`, `transport`; policy insertion retains the supplied default chain. |
| B | `azure/storage/blob/_shared/base_client_async.py:95-155`: constructs its own policy list and `AsyncPipeline(transport, policies=policies)`; `_shared/policies.py:328-338`: request hook consumes `raw_request_hook`; `_shared/policies_async.py:100-149`: async response hook consumes `raw_response_hook`. |
| I | `azure/identity/aio/_credentials/managed_identity.py:46-122`: environment-selected credential receives kwargs; `aio/_credentials/imds.py:45-60`, `aio/_internal/managed_identity_client.py:25-40`, `_internal/pipeline.py:39-96`: separate Identity pipeline builder. |
| H | `agent_framework_foundry_hosting/_responses.py:665-689,850-888`: host constructor exposes workflow factory, parser, `prepare_options`, checkpoint/session/response providers; `azure/ai/agentserver/core/_base.py:450-466`: public `add_middleware`. |
| W | `agent_framework_foundry_hosting/_workflow_responses.py:408-487`: request context -> trusted scope -> hosted request -> options hook -> workflow factory -> continuation stores -> input parser -> claim/execution. |
| S | `agent_framework_foundry_hosting/_scope.py:23-58`: hosted scope rejects missing trusted user/call or mismatched session before returning a scope. |
| Q | `azure/ai/agentserver/responses/hosting/_endpoint_handler.py:174-190,856-921,1071`: raw-header extraction and endpoint/stream request-context bind/reset; `core/_request_context.py:41-145`: public context accessor and opaque-call forwarding contract. |
| R | `azure/ai/agentserver/responses/hosting/_resilient_orchestrator.py:239-345,785-895,1111-1163`: reconstruction, task dispatch, durable input capture; `_resilient_input.py:54-83,194-264`: identity serialization/derivation; `_orchestrator.py:99-140`: per-iteration handler context bind/reset. |
| T | `agent_framework_foundry_hosting/_state_store.py:99-138,243-315,395-501`: checkpoint and session providers/stores; `_workflow_state.py:206-219`: SDK-owned workflow binding store. |
| U | `azure/ai/agentserver/core/storage/_state.py:86-186,242-298`: public `FoundryStateStore` construction/get-or-create accepts credential and kwargs, defaults to an owned `DefaultAzureCredential`; `storage/_client.py:55-88`: Azure Core transport/policy chain. |
| V | `azure/ai/agentserver/responses/store/_foundry_provider.py:139-205`: response provider creates its own Azure Core client with fixed policies; constructor accepts credential/settings/version callback, not pipeline kwargs. `responses/hosting/_routing.py:367-405`: hosted default creates this provider with its own `DefaultAzureCredential`; local fallback uses a file store. |

## Factory / transport / attachment matrix

Every proposed attachment below is **not yet implemented or behavior-tested by
this task**. A source-supported seam is not a coverage PASS. Send/headers/error
events do not establish stream or agent-execution completion.

| Path and application owner | Actual transport and supported observation choice | Observable events and safe binding | Explicit gaps and retained/proposed checks |
| --- | --- | --- | --- |
| Agent metadata and specialist session create/lookup: `demo/foundry.py:157-179` `ProjectClient`; `RemoteAgents.prepare/create/_check/recover_creation` at `253-301` | Azure Core `AIProjectClient`, default async transport (AioHttpTransport), **not** `data_client`. P/C support additive `per_call_policies` or `per_retry_policies` in the application's `super().__init__`. Prefer per-call observation of one logical SDK operation; use per-retry only if actual attempts are explicitly distinguished. Retain retry/auth/timeouts. | Bounded session-create, session-lookup and metadata route templates; timing/status/error category, role and allowlisted correlation only. Record header presence, not values; a per-call send checkpoint is before authentication, not proof of final bearer principal. | A Project policy cannot see OpenAI calls. Constructor insertion probe passed (below); SDK-POLICIES must prove actual session operations emit events through a fake transport, including failure and redaction. Preserve ambiguous-create lookup-only behavior. |
| Remote specialist Responses invoke/retrieve: `demo/foundry.py` `RemoteAgents`; `demo/workflow.py` `WorkflowRemoteAgents`; terminal `ProjectClient` | P factory passes application's `http_client` into OpenAI. `demo/foundry.py:95-179` `OriginTransport` / `data_client` is the actual httpx2 seam. TRANSPORT owns final-header send, headers, error and unbuffered stream wrapper. | Exact role endpoint -> fixed Responses route template. Correlate using reviewed event-contract bindings, not raw endpoint IDs, user hashes or bodies. Actual final-header presence is observable here, bearer identity is not. | Azure Core policy installation cannot cover this path. Test exact origin, no redirect/retry, stream chunks/close/cancel and known-response-only recovery. Preserve `WorkflowRemoteAgents.invoke/recover` rather than resend a failed held effect. |
| Specialist model/history calls: `demo/architect_agent.py:191-201`, `demo/reviewer_agent.py:192-202`; `FoundryChatClient(project_client=project)` | `agent_framework_foundry/_chat_client.py:248-258` obtains `project_client.get_openai_client`; thus the same application httpx2 transport for model requests and `responses.retrieve` recovery. | Model Responses template and send/headers/stream/error milestones, safe role/binding supplied by the application. | Model history in MAF `AgentSession` is not an HTTP request. Its persistence uses the session provider row below. Retain pending-model-response retrieval and immutable output tests; do not label model HTTP 200 an accepted candidate. |
| Decision-1: `demo/routing.py:249-280` `DecisionClient.score`; legacy `demo/foundry.py` `DecisionRouter.choose` | Shared httpx2 `data_client`; directly posts to `/providers/microsoft/v1/systemone`. Instrument at OriginTransport for both application clients, not a separate Azure Core policy. | Fixed Decision route, HTTP method/status/timing/category; only allowlisted request IDs/trace metadata. | Token acquisition is separate. Preserve deterministic gates/admission before the call, body/schema validation and machine stdout. Retain `tests/test_routing.py` and Decision adapter tests. |
| Native artifact/effect/manifest Blob access: `demo/workflow.py:142-151,521-550` -> `demo/artifact_store.py:85-104` `BlobArtifacts` | Explicit `AioHttpTransport(use_env_settings=False)` with Blob SDK's own pipeline B. **Generic `per_call_policies` does not insert a policy here** (negative probe below). Public raw request/response hooks can invoke safe policy callbacks at their supported positions. Public custom `transport` is a viable separate boundary for send exceptions, if required; preserve its ownership and existing options. | Fixed Blob operation classes (read/write/lease), status/timing; safe role/operation binding only. Raw hooks do not prove final wire headers or exception coverage; response hooks must not inspect payloads. | Do not use private `_additional_pipeline_policies` / `_pipeline` or replace the policy list to manufacture coverage. SDK-POLICIES must choose supported hooks/transport with tests, or explicitly record uncovered exception intervals. Preserve ETag/fencing, leases, immutable writes and retry_total=0. |
| Specialist injected Blob services: `demo/architect_agent.py:101-115`, `demo/reviewer_agent.py:104-118` | Each constructs its own `BlobServiceClient` and injects `service=` into `BlobArtifacts`. Same B transport/hooks, **bypassing the BlobArtifacts constructor factory**. | Same bounded Blob events; attributable role set by the owning application factory. | Editing only `artifact_store.py` does not cover these two services. SDK-POLICIES reports attachment choice to INTEGRATE; INTEGRATE/Scrum must coordinate these call sites if needed (outside SDK-POLICIES' current owned paths). They must remain explicitly uncovered until fixtures prove coverage. No silently expanded ownership. |
| Application credential acquisition: `demo/workflow.py:525`, `demo/foundry.py:447`, specialist resource factories | Async `ManagedIdentityCredential` uses its own Azure Core pipeline, selected by environment I. Standard `per_call_policies` is **not consumed** by its Identity pipeline builder (negative IMDS probe below). Public `transport` and raw hooks reach pipeline-based implementations; custom `policies` replaces defaults and is unsuitable here. | Fixed credential-acquisition route category, elapsed/status/error category only. Never log request headers, query, token response, principal, environment or exception text. Token cache hits have no HTTP send. | Do not use `_per_retry_policies` or select/patch private credential implementations. SDK-POLICIES must test the chosen public hook/transport with synthetic branches and keep untested environment branches/cache hits explicit. Preserve credential auth, IMDS probing/retries and transport ownership; no credential call was made by this inventory. |
| Terminal credential: `demo/terminal.py:268-272` | `AzureCliCredential` invokes the CLI subprocess (`azure/identity/aio/_credentials/azure_cli.py`), not the ProjectClient/httpx2 transport. | At most an application acquisition boundary; this inventory attaches nothing. | Azure Core/httpx2 policies cannot see CLI internals or cached token handling. No CLI execution, authentication or cache inspection is needed for this research. Keep uncovered rather than inventing pipeline coverage. |
| SDK agent-session/history persistence: `demo/foundry.py:181-209` `HostedJournal`; specialists' `AgentSessionStoreProvider(store_name="specialist_history_v2")`; host defaults | T uses `FoundryAgentSessionStore._get_store` -> `FoundryStateStore.get_or_create(..., user_isolation=True)` with no pipeline kwargs. U uses its own Azure Core client/default credential. Provider constructor accepts only `store_name`. | Application call-boundary checkpoints are reachable; SDK-internal HTTP send/status/errors remain uncovered by application Project/Blob policies. | H exposes provider replacement as a public abstraction, but the stock provider does not expose policy forwarding. Replacing persistence to add logging is not the minimal profiling attachment. Preserve user scope, ETags, serialization and call-ID forwarding. Retain session-history continuity tests; do not claim a Project policy profiles these stores. |
| MAF checkpoints and native workflow bindings: `demo/host.py:44` `CheckpointStoreProvider()`; W continuation preparation | T checkpoint provider exposes allowed types/get_store, not transport/policy kwargs. Both checkpoint and `_workflow_state.FoundryWorkflowBindingStore` construct U independently; the latter is SDK-owned, not the replaceable checkpoint provider. | Application workflow checkpoints/executor boundaries only; internal storage HTTP currently uncovered. | Public U supports constructor kwargs **when the application constructs U**, but these callers do not forward them. A custom checkpoint provider alone cannot cover native binding storage. No monkeypatch or storage rewrite; preserve MAF checkpoints and write-ahead unknown-effect holds. |
| SDK stored Responses / server-managed history | H has `store`/`response_store` provider injection; default hosting routing creates the provider separately. V uses Azure Core, owned credential and fixed policies, not Project or Blob client. Server-managed history may read stored Responses depending on the selected host history mode. | Response-provider call boundary could be decorated through public provider protocol in a separately scoped change; no generic HTTP policy injection in V's constructor. | Distinguish provider injection from policy injection. Stock internal requests remain uncovered. No provider replacement is required to complete this inventory; never claim coverage of all response/history stores or streamed replay because ProjectClient is profiled. |

## Host/context checkpoint reachability

| Boundary | Supported seam and pinned ordering | Meaning / retained gap / proposed fixture |
| --- | --- | --- |
| Raw ingress and ASGI response | H `server.add_middleware(PureASGIMiddleware)` before `run()`; inspect raw `scope["headers"]` without changing it. | Observe case-insensitive absent/empty/nonempty/duplicate/malformed presence for public delegation and platform user headers separately. Pass receive/send/messages/cancellation unchanged. ASGI final body means delivery milestone, not successful background execution. No context is guaranteed before endpoint parsing. |
| Endpoint context | Q extracts `x-agent-user-id` into `PlatformContext.user_id_key`; absent is None, empty is empty. Endpoint ambient `FoundryAgentRequestContext` uses `ctx.user_id or None` and `ctx.call_id or None`, collapsing empty into absent at this particular checkpoint. | Do not infer that all SDK layers preserve empty strings, or that a delegation header must survive. Record independently observed presence/coverage; never recover missing trusted identity from raw headers. |
| Preparation BEFORE application factory | W first reads ambient context and S validates hosted scope; only then builds `HostedResponseRequest` and runs public `prepare_options`. | Missing trusted user/call can reject before **both** options and factory hooks. Existing `demo/host.py` `WorkflowPreparationDiagnostics` filter observes the specific SDK preparation/RuntimeError log while its context is available. This is an exact pinned log event, not a universal exception hook. Keep existing rejection and allowlisted code; absent matching log/context is unavailable, not success. |
| Reachable preparation/options/factory | W calls `prepare_response_options` then resolver. Public `prepare_options` receives `HostedResponseRequest`; `create_workflow(request)` and `WorkflowRuntime.__init__` inspect request scope and ambient accessor. | Compare scope/request-context user or call equality only when representations match; report not-comparable otherwise. Do not compare public delegation to platform user values as if identical. Keep request-local immutable snapshots, no host/transport identity cache. |
| Parser and executors | W parser runs after continuation preparation, except recovery uses `run.recovery_turn()` and can skip parser. Application `parse_turn`, executor handlers and `WorkflowRuntime.resources` are reachable application hooks. | Instrument an actual executor/resource boundary as well as parser; parser alone cannot cover recovery. Execution completion must come from actual workflow outcome, not handler return or SDK-completed envelope. |
| Resilient background AFTER HTTP request exit | R persists user/call/session in durable input; reconstructs response context; `_iter_handler_with_request_context` binds ambient context for each `__anext__` and resets it in `finally`. Both resilient stream and nonstream dispatch are separate paths. | Observe inside the public request-aware factory/executor, not by replacing the private wrapper. Crash recovery has no new raw ingress and cannot retrospectively observe the original request. Test actual pinned host dispatch after endpoint exit, both success/rejection and concurrent reset/cancel. |

The existing
`tests/test_workflow.py::LiveObservationTests.test_pinned_sdk_resilient_identity_survives_serialization_and_handler_entry`
round-trips the pinned serializer and directly invokes its private handler
wrapper. It is useful retained evidence, **not** an actual full-host resilient
background test. INGRESS-CONTEXT still owes that acceptance fixture.
`test_sdk_preparation_filter_reports_only_missing_trusted_scope` is the retained
filter/redaction fixture; it does not establish raw ingress coverage.

## Minimal implementation handoff and verification

1. SDK-POLICIES: use additive Azure Core policy insertion for ProjectClient;
   do not copy that constructor option to Blob or credentials. B/I show why.
   Choose public raw hooks/custom transport where appropriate, preserving
   existing defaults; a missing send-exception hook must remain a named gap.
   Prove covered clients with actual fake-transport requests, not constructor
   presence alone. No private insertion knobs or new credential retrieval.
2. INGRESS-CONTEXT: use H plus public options/factory/parser/executors, retaining
   the preparation log filter. Test the early S failure separately from reachable
   hooks. Explicitly account for empty-value normalization and parser-skipped
   recovery. R is source evidence, not permission to patch SDK internals.
3. INTEGRATE: reconcile the two injected specialist Blob factories with the
   selected attachment, or retain their uncovered status; coordinate call-site
   ownership rather than silently expanding SDK-POLICIES. Refresh the shared
   repository index after incorporating this new document; this task owns only
   this document and preserves the pre-existing dirty index/specification.
4. TRANSPORT can proceed from its event-contract handoff independently. This
   inventory does not gate its httpx2 work or require full SDK coverage first.

Offline constructor probe, run with the existing explicit linked-lab Python:
`AIProjectClient(..., per_call_policies=[marker])` retained one marker;
`BlobServiceClient(..., per_call_policies=[marker])` retained zero;
`ManagedIdentityCredential(per_call_policies=[marker])` with an empty synthetic
environment (IMDS branch) retained zero. Assertions passed, clients were closed,
and the fake credential's `get_token` would raise if called. Read-only inspection
of constructed policy chains was used only for research assertions, not a runtime
private attachment. The two zero counts are actionable negative findings, not
working diagnostics or claims about every credential branch.

Validation executed in the shared checkout:

| Command / check | Actual result and scope |
| --- | --- |
| `./Test-Demo.ps1 -Python <linked-lab-root>/.venv/Scripts/python.exe -LabRepositoryRoot <selected-feature-lab-root>` | Exit 0. `pip check`: no broken requirements. 223 offline application tests passed in 57.198 seconds, including retained wrapper regressions; compilation succeeded. Existing explicit Python and selected-feature lab roots were supplied, with no installation. This was a concurrently changing checkout, not the later INTEGRATE exact-source E2E join. |
| `./scripts/Test-Repository.ps1 -Python <linked-lab-root>/.venv/Scripts/python.exe` | Exit 1 at `REPOSITORY_INDEX_STALE`. Later boundary/parser stages did not run. This is an executed stale-index failure, not the historical permission denial or a repository PASS. INTEGRATE owns index refresh and rerun; no unrelated index changes were absorbed here. |
| Installed metadata + manifest/lock comparison | The eight named versions above matched; no SDK version extrapolation was used. |
| Constructor insertion probes | Three assertions passed (Project insertion; Blob and IMDS non-insertion). No send/token calls. Downstream retained pipeline fixtures still required. |

The initial application source baseline above remains the inventory binding.
While checks ran, the independent event-contract owner committed `20c315e`;
its source is not adopted as a reviewed dependency by this inventory.
No runtime source was changed in this task. The new coverage document and
pre-existing untracked specification require an eventual shared-index refresh;
that concrete repository-check gap is retained for the integration owner.

Safe event bindings must consume the reviewed EVENT-CONTRACT API, not invent
raw identity hashes. Coverage (`observed`/`unavailable`/`not reached`) remains
independent of value presence. Redaction/failure-isolation tests must use sentinel
identities, headers, URLs/query, bodies, credential responses and exception text;
none may escape to private logs or machine stdout. No diagnostic authorizes a
request, suppresses rejection, repairs identity or proves platform translation.
The authenticated outbound principal and platform resolution interval remain
unobserved. No RBAC/platform defect or header substitution is justified here.

Original Architect/Critic review remains downstream of this inventory commit.
Exact-source E2E, newly identified common-package publication, synthetic intent
recording, live AC1-AC9/G1-G8 and attributable cleanup remain their original
owners' work. The held parent and unknown effects are untouched.

## SDK-POLICIES implementation delta

Consumes accepted EVENT-CONTRACT `20c315e`, SDK-INVENTORY `b7b4e0e` and
TRANSPORT `9c8dfdf` on the established feature branch. Their original
Architect/Critic agreement audits are respectively `49fb735d`, `8224c1af` and
`b5e33586` in the current IP-S1 run context. The original implementation was
`87de392`; the timeout-preservation correction below applies the reconciled
required dispositions from the same SDK-POLICIES loop. This delta changes only `demo/foundry.py`,
`demo/artifact_store.py`, this matrix and `tests/test_sdk_diagnostics.py`.
Previously reviewed transport code is preserved.

### Public attachments and exact coverage

| Application path | Implemented public seam / retained behavior | Proven offline coverage and explicit limits |
| --- | --- | --- |
| All application `ProjectClient` instances, including specialist session create/lookup and metadata calls | `SDKDiagnosticsPolicy` is an additive **per-call** `AsyncHTTPPolicy`. `ProjectClient` retains its default pipeline/auth, zero retries and original timeouts; optional keyword-only `transport` forwards the public test/transport seam without changing the default. | Actual pinned `agents.create_session`, `get_session` and `get` operations pass through a synthetic Azure Core transport, with default authentication still acquiring a synthetic bearer. Session routes are closed templates; metadata remains `other`. Logical send/response/error are observed; send is before downstream authentication/retry, and response is when the downstream policy chain returns, **not the instant wire headers arrive**. It is not a final-header principal observation. |
| `BlobArtifacts`' application-owned default service factory | `blob_diagnostics_transport(role=...)` wraps the existing explicit `AioHttpTransport(use_env_settings=False)` using the public `transport` option. No custom policy list or private insertion. Existing `retry_total=0`, size/timeouts, auth, ETag, leases and application scope checks remain unchanged. | Actual pinned Blob `get_blob_properties` and `upload_blob` traverse the default factory and emit per-attempt send/response; failed sends emit error and rethrow. Tests preserve request/response identity and original send options, without body reads or stream wrappers. A successful status is only HTTP evidence. |
| `foundry.create_hosted_agent` application credential factory | `ManagedIdentityCredential(**credential_diagnostics_options(role=...))` uses public raw request/response hooks, leaving transport construction, environment selection, branch defaults and retries entirely with Identity. The original eagerly supplied transport was incorrect and has been removed. | Synthetic IMDS and App Service branches execute the actual pinned credential pipeline with no network or real token acquisition. Paired request/response hooks emit per-attempt events without inspecting credential headers or payloads. IMDS retains its two-second connection default; App Service retains 300 seconds. Baseline/instrumented retry-budget fixtures verify equal configurations and a one-second budget clamped to 1 then 0.75 seconds. Cache hits emit no send. **No transport-error/cancellation hook is available through these callbacks**: a send without response is incomplete, not an inferred error or success. Other environment-selected implementations remain unverified. |
| Reusable public decorator `SDKDiagnosticsTransport` in `artifact_store.py` | Delegates `open`, `close`, `__aenter__`, `__aexit__`, `send(**kwargs)`, `sleep` and the inner optional `connection_config` to the original transport. Exceptions and cancellation propagate; diagnostic sink/schema failure cannot replace outcomes. | Blob transport-send failures remain covered, not failures in subsequent SDK decoding, body iteration, authentication outside this pipeline, or execution. Retry deadline fixtures prove the decorator exposes the original configuration and preserves connection-timeout clamping. It neither buffers nor replaces the response and emits no stream/execution-completion event. Project/Blob header presence comes from the SDK mapping, not raw duplicate-preserving wire headers. Credential factories no longer use this decorator. |

Each request/attempt takes an immutable local observation alias and inherits
only existing safe operation/response aliases. Policy state is local to its
`send` coroutine; credential-hook state uses the public per-request pipeline
context, not a shared client/global identity. Synthetic overlapping requests verify
separate bindings. An alias does not establish a private join or identity.
Only method, fixed route/stage/role, presence, status, elapsed milliseconds and
fixed category reach the closed event projection. No exception text, concrete
URL/query/resource name, bearer/credential payload, user identity or hash is
logged. HTTP errors still reject normally; neither policy nor transport
authorizes anything or changes trusted context.

### Explicit integration handoffs and uncovered intervals

INTEGRATE/Scrum coordinates the remaining **application call-site wiring**
through the original Developer ownership. The accepted inventory already
identified these out-of-task factories; this is not a new diagnostic
architecture or permission to silently expand any task's owned paths:

* `architect_agent.py` and `reviewer_agent.py` create and inject separate Blob
  services. They still bypass the `BlobArtifacts` default factory. Select the
  public `blob_diagnostics_transport(role=...)` for each existing explicit
  transport, preserving that factory's exact options, and retain constructor/
  pipeline regressions. Until that handoff is implemented and tested these
  two injected services are **uncovered**, not PASS.
* `WorkflowRuntime._resources` in `workflow.py`, plus the specialist resource
  factories, still construct their own `ManagedIdentityCredential()`. Wire the
  reviewed `credential_diagnostics_options(role=...)` as public credential
  keyword options, **not a preconstructed transport**; preserve the existing factory
  ownership/lifecycle. Only `foundry.create_hosted_agent` is wired by this
  assignment. Do not label all application token acquisition covered.
* The SDK-owned session/history/checkpoint/workflow-binding/response stores
  in T/U/V remain uncovered at internal HTTP boundaries: their stock callers
  do not forward the application policies/transports. The original pinned
  source evidence above remains applicable. No private SDK edit/provider
  replacement has been introduced. Azure CLI subprocess internals, credential
  cache hits/unverified branches and Foundry platform resolution remain outside
  coverage. The authenticated outbound principal remains unproven.
* Refresh the shared repository index after integrating the new tests/module
  paths, preserving its pre-existing notes/edits. Original E2E still owns the
  final exact-join full checks; original DevOps owns Linux/package/publication,
  synthetic intent, live acceptance and attributable cleanup. No lab release
  tooling changed here. Historical rollback provenance remains WAIVED.

The retained `tests/test_sdk_diagnostics.py` fixtures exercise constructor
attachments through real pinned public SDK pipelines, not merely private
policy-list inspection. They include HTTP rejection, send failures, default
Identity retries, cache non-observation, concurrent policy/transport isolation,
context reset, cancellation, response/body ownership, private redaction,
machine-stdout isolation and diagnostic-failure containment. All credentials,
responses, identities and endpoints in these fixtures are synthetic.

### Executed SDK-POLICIES checks

Commands used the existing absolute linked-lab Python and, for the documented
application entry point, the explicit selected-feature lab root. No dependency
installation, live call, secret acquisition or lab tooling edit occurred.

| Check | Observed result |
| --- | --- |
| `python -m unittest discover -s tests -p test_sdk_diagnostics.py -v` (`OTEL_SDK_DISABLED=true`) | Final **16 tests PASS in 0.464 seconds**. The initial 13-test iteration had one fixture error: the synthetic Project session used `id`, while the pinned model exposes `agent_session_id`. The fixture was corrected to the actual model and public `VersionRefIndicator` contract. No runtime contract was weakened. |
| `./Test-Demo.ps1 -Python <linked-lab-root>/.venv/Scripts/python.exe -LabRepositoryRoot <selected-feature-lab-root>` | Final exit 0: **270 tests PASS in 60.749 seconds**, dependency check and compilation passed. An earlier run before three additional test cases passed 267 tests in 64.323 seconds. These are shared-checkout observations including concurrent host work, not final exact-source integration certification. |
| `./scripts/Test-Repository.ps1 -Python <linked-lab-root>/.venv/Scripts/python.exe` | **FAIL**, exit 1 at `REPOSITORY_INDEX_STALE`; later parser/public-boundary stages did not run. The already dirty shared index is outside this task's owned paths. INTEGRATE retains refresh/preservation and rerun, not a waived gate. |
| Owned `py_compile` and `git diff --check` | PASS for the SDK source/tests and owned documentation (compilation applies to Python only). |

Original Architect/Critic review of this implementation remains pending.
All remaining application call-site gaps above are explicit construction
handoffs; the original live identity interval and release conditions remain
unproven. No HTTP or SDK envelope result closes AC1-AC9/G1-G8.

### Timeout-preservation correction

Applies the exact originating required references
`["yaml-loops-v1:sprint/1/IP-S1/task/IP-S1-SDK-POLICIES/AssignedWorkDeveloperLoop","SDK-CREDENTIAL-TIMEOUT-PRESERVATION"]`
and
`["yaml-loops-v1:sprint/1/IP-S1/task/IP-S1-SDK-POLICIES/AssignedWorkDeveloperLoop","SDK-TIMEOUT-REGRESSION-EVIDENCE"]`.
The original tests above remain historical results, not proof of preserved
timeouts. Critic's source finding confirmed that supplying an eagerly constructed
transport skipped Identity's branch-specific construction. The decorator also
hid `connection_config` from Azure Core's retry deadline calculation.

The correction uses the already inventoried public raw hooks rather than
replicating environment selection or applying IMDS settings to all credentials.
Pinned references: Identity `aio/_credentials/imds.py:45-60` and
`_internal/pipeline.py:69-96`; Azure Core
`pipeline/policies/_custom_hook.py` (`CustomHookPolicy`) and
`pipeline/policies/_retry.py:359-390` (`_configure_timeout`).
No SDK/private patch, branch-selection replacement or dependency change is used.
Raw hooks have no send-error/cancellation callback. This explicit uncovered
credential interval replaces the former decorator's error coverage; the Blob
decorator and Project policy still observe their respective errors.
An incomplete credential pair must never authorize, retry, or infer an outcome.

Offline regressions compare uninstrumented/instrumented IMDS and App Service
factory configuration and actual synthetic retry attempts, including remaining
budget clamping. They retain synthetic cache, redaction, failure containment and
concurrent binding cases, plus propagation of cancellation with no invented
completion/error event. Test fixtures replace only network I/O and use no real
credential acquisition. Integration must consume the corrected options API.

Correction checks (existing absolute linked-lab Python; explicit selected-feature
lab root for `Test-Demo.ps1`):

| Check | Observed correction result |
| --- | --- |
| `python -m unittest discover -s tests -p test_sdk_diagnostics.py -v` with `OTEL_SDK_DISABLED=true` | **20 tests PASS in 0.459 seconds**. Initial 19-test iteration failed because the fixture passed the operation budget via `get_token`, which IMDS does not forward. The fixture now supplies the supported credential constructor timeout to both baseline and instrumented cases; both prove 1 then 0.75-second clamping. No runtime contract was relaxed. |
| `./Test-Demo.ps1 -Python <linked-lab-root>/.venv/Scripts/python.exe -LabRepositoryRoot <selected-feature-lab-root>` | Exit 0: **274 tests PASS in 46.620 seconds**, dependency check and compilation passed. Shared-checkout result, not final integration/E2E certification. |
| `./scripts/Test-Repository.ps1 -Python <linked-lab-root>/.venv/Scripts/python.exe` | **FAIL** at `REPOSITORY_INDEX_STALE`; subsequent stages did not run. Existing shared index edits remain untouched; INTEGRATE owns refresh and exact-join rerun. |
| Owned whitespace check | PASS. |

Return this correction to the original Architect/Critic reviewers. Their prior
votes on `87de392` are not collective acceptance of the new correction.
