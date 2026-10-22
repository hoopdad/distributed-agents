# Identity evidence handoff: prospective profiling and retained candidate history

## IP-S3 prospective acceptance companion — October 22, 2026

**Comparison preparation only; no new live receipt, invocation, stop or cleanup.**
This additive `IP-S3-ACCEPTANCE-COMPANION` overlay consumes the accepted
[IP-S3 architecture](customer-prototype-sprint-architecture.md#current-ip-s3-continuity-once-only-recovery-and-independent-isolation)
and [IP-S3 design](customer-prototype-sprint-design.md#current-ip-s3-continuity-supported-recovery-and-independent-isolation-october-22-2026).
The IP-S2 overlay and RP-S1 historical body below remain unchanged. Their dated
missing-prerequisite statements are not new instructions. Exactly three hosted
roles, remote specialists, deterministic gates before Decision-1, immutable
role outputs, exact prerequisites, ETag fencing, MAF checkpoints and unknown
effect holds remain required; this companion changes no runtime or parser.

### Source boundary and original votes

Comparison source is runtime/tests `c52786b7dd1595f3048a78061f893dc79635069f`
on `feature/customer-hosted-session-prototype`, with selected-lab
`9b4919d8bcdbf07203f32657936c27328ea6ccc1`. The current sprint architecture
document is `8f5da03931e4ad13fe1bd1166a8b7f6bb3c7c7ac`, design
`c544588b570a2e5ae9f6d5a88f2e96a32cc3ec77`, and accepted IP-S2 companion
`13aecc39fba90d1475de057db07566c69b4ffc27`. These are source references,
not deployed bindings. Independently opened original audits under
`gh-dynamic-workflows/.delivery-runs/eef04e5c-c5ab-4b88-90f6-4a99dd4692ed/context/`
(each filename ends in `.json`):

- `6c19a86535b0b0b133a52e31ee77f89fdb90370742805ac6eeac25811bd499ee`:
  IP-S3 architecture; Product Owner/Critic/Red Team agree and task-complete.
- `cb73116068dae88e649376c587fa360cd2f56a6b5b3b09a06e73065be7d14602`:
  IP-S3 design; Product Owner/Critic agree and task-complete.
- `9bc452275610e015f8ec3f0ad3af80a637966fcbe0c98d9b4a9e1bb541673794`:
  IP-S2 diagnostic overlay; Architect/Critic agree and task-complete.

All inspected votes have empty unmet criteria; none accepts this new companion
or proves a cloud turn. Retain the accepted changed-join boundary for
`["yaml-loops-v1:sprint/1/IP-S1/DevOpsWorkLoop","RELEASE-CHANGED-JOIN-HANDOFF"]`;
do not reassess that source ledger here. At that same origin,
`RELEASE-COMMON-PACKAGE-PUBLICATION` and `RELEASE-LIVE-ACCEPTANCE` remain
required. Both SDK timeout dispositions at
`yaml-loops-v1:sprint/1/IP-S1/task/IP-S1-SDK-POLICIES/AssignedWorkDeveloperLoop`
remain accepted in their unchanged source/test boundary, not new work here.
Historical COMMON rollback ZIP/build provenance is **WAIVED, never PASS**.
Current automated source/package/version/trusted-host/effect checks remain.
Planning serialization/dispatch dispositions belong to the originating Scrum
loop, not to comparison acceptance; this task launches no substitute agents.

### Comparison contract — keep actual values private

Use the existing [scenario validator](../live_acceptance.py)
`_evidence_turn`, `_evidence_continuation`, `validate_scenario_evidence` and
`SCENARIOS`, not aliases, whole-session equality or a new public evidence API.
Each scenario snapshot contains `proof`, `manifest`, cumulative `operations`,
independently observed boundary `creations` and `sends`; followup/restart also
need `checkpoints`. Restart adds `stops` and `proof.hosting_restart`; the final
join additionally consumes `stopped_session`. `proof` carries scenario,
framework, version, metadata, child-session readbacks, delegations and result.
Journal intentions are not observed sends. Keep complete values, receipt
bodies and authentication provenance outside public Git.

| Criterion / canonical steps | Exact comparison and receiving original owner | Retained offline fixtures (not live captures) |
| --- | --- | --- |
| AC2/G5; `continuity-revise`, `continuity-invoke`, `continuity-verify` | Original DevOps hands E2E completed **non-held** initial/followup snapshots. `_evidence_turn` requires `ACCEPTED_ADVISORY`, current artifact refs, active response, accepted/reconciled effects and both bound children. `_evidence_continuation` compares identical `scope_binding` (project/tenant/principal/parent), parent `proof.framework.session_id`, both child tuples `(hosted_id, framework.session_id, version)` and coordinator version. Child framework state must name its actual hosted ID; producer and service readbacks must agree. Compare these identity fields, not complete mutable serialized sessions. | `ScenarioEvidenceTests.test_actual_parent_and_both_child_identities_and_versions_are_required`; `test_actual_offline_graph_captures_pass_including_four_call_revision` in [scenario tests](../tests/test_scenario_evidence.py). |
| AC2/G5; `continuity-verify` | Across initial/followup, retain exactly two cumulative child creations (one per role), with unchanged creation set. Every actual new specialist call has a unique accepted `response_id`; parent active responses differ. `turn` increments once, `generation` increases; old operation transitions remain equal, and new `sends` exactly match current call operations with no duplicates. New responses for invocations do not mean retrieval creates an invocation. | `test_extra_creations_duplicate_sends_and_unreconciled_effects_fail`, `test_stale_approval_and_journal_drift_fail` in [scenario tests](../tests/test_scenario_evidence.py); `test_reject_revise_review_reuses_both_children_with_fresh_responses` in [workflow tests](../tests/test_workflow.py). Four calls in the reject/revise fixture are valid, not a requirement of exactly two calls. |
| AC2/G5; `continuity-revise`, `continuity-verify` | Earlier requirements `content.chunks` remain an exact prefix with new chunks appended, including the canonical private-ingress initial and queue followup briefs. Candidate/review refs must change; current requirements/candidate/review revisions equal the current turn. Compare every `ArtifactRef` field: container, name, sha256, artifact_type, schema_version, requirements_revision, candidate_revision. Validate artifact content hash, scope, producer role/name/session/version/response and ordered `input_refs`. Current call prerequisites start with current requirements; final reviewer inputs equal the current review artifact inputs, including the exact current candidate, never an earlier same-turn candidate. | `test_missing_queue_requirement_is_rejected_even_with_current_valid_artifacts`, `test_final_reviewer_cannot_omit_candidate_in_consistent_journal`, `test_final_reviewer_cannot_use_earlier_same_turn_candidate`; workflow `test_followup_invalidates_old_approval_and_preserves_children`. |
| AC4/G6; `recovery-stop`, `recovery-resume`, `recovery-verify` | Original DevOps consumes completed two-turn proof, exact active parent/version and reconciled effect readiness before any supported stop. Persist once-only intent first; retain observed POST accounting, response and independently observed stopped/idle state. Resume the same parent/both children/pins; compare followup/restart with `_evidence_continuation`, cumulative journals and sends as above, not a new child or replay. E2E compares checkpoint scope, unique checkpoint_id, workflow_name `distributed-agents-v1`, nonempty graph_signature_hash, nonnegative integer iteration_count and dictionary state: all old records unchanged, additional records present, one graph signature. | Scenario `test_stop_confirmation_once_only_and_checkpoint_retention_fail_closed`; workflow `test_hosting_restart_stops_exact_active_parent_and_proves_idle_compute`, `test_native_checkpoint_resumes_fresh_graph_without_duplicate_effects`, `test_known_response_reconciles_after_crash_without_new_remote_call`, `test_unknown_effect_is_held_and_never_redispatched`. |
| AC4/G7; `isolation-bind`, `isolation-execute`, `isolation-verify` | With final deployed bindings and a safe completed comparison scope, original DevOps may independently execute the distinct Cedar parent. E2E compares same project/tenant/principal but different parent hosted/framework IDs, scope prefix and both child hosted/framework IDs; isolated turn is 1, requirements exactly the canonical isolated brief. No overlapping sends, creations or accepted call response IDs; isolated candidate/review content must contain neither Harbor nor asynchronous queue. All scenario metadata equals initial metadata; independently verify actual package/version provenance rather than treating metadata equality as authentication. | Scenario `test_isolation_content_scope_and_release_drift_fail`, `test_valid_hashed_but_leaked_isolated_content_is_rejected`; workflow `test_two_parents_remain_isolated_on_the_same_backend`. [ArtifactRef.assert_scope / Assignment.validate_receiver](../demo/artifacts.py) and [BlobArtifacts.read_artifact](../demo/artifact_store.py) retain trusted-scope rejection and hash verification. |
| AC7-AC9/G8; `release-join`, `release-package`, `release-discriminate`, `release-close` | IP-S3-DELIVERY-JOIN receives reviewed document commits/votes, unchanged-runtime assessment and explicit-root application/repository checks. Original DevOps supplies final common package and three-role source/version/readback/effect bindings, actual live outcomes and attributable cleanup. Existing Scrum review/retro and closeout retain exact reviewed non-force feature delivery/readback, reproducible setup/commands, sanitized evidence and every missing/held/UNKNOWN condition. No fixture or validator PASS closes publication, live criteria or historical cleanup. | Retain scenario `test_documented_private_json_invocation_passes_and_fails_nonzero`, `test_missing_inputs_fail_closed_without_echoing_private_values`; documented `Test-Demo.ps1` and `scripts/Test-Repository.ps1`. No selected-lab tooling changes are assigned here. |

Runtime links: [Terminal client](../demo/terminal.py) `chat` restores the
private parent, pins version, rejects pending ambiguous turns and permits
`recover_only` only for a known response. [RemoteAgents](../demo/foundry.py)
`create`, `_check`, `invoke`, `recover` retain hosted/framework/version checks
and response-only recovery. [Workflow](../demo/workflow.py) `WorkflowRuntime`,
`EffectExecutor` and publication reconcile immutable role artifacts and
write-ahead effects with fenced manifest publication. These paths are distinct
from specialist model history and MAF checkpoint state.

Both roles' [SpecialistContinuityTests](../tests/test_specialist_continuity.py)
`test_architect_persists_and_restores_model_continuation_with_fresh_history_control`
and reviewer counterpart prove, offline, restored framework session identity,
prior `service_session_id` forwarded as model `conversation_id`, then advancing
service response and exact artifact prerequisites. The fresh-history negative
control lacks that continuation despite the same brief. The paired
`test_architect_known_response_recovery_persists_continuation_without_send` /
reviewer counterpart and `*_unknown_and_mismatched_pending_effects_remain_held`
distinguish retrieval from a new model call. Aggregate scenario snapshots
do not independently prove that model-history link in a deployed specialist;
original DevOps/E2E must attribute available private history evidence or report
that observation unavailable, not substitute remembered prose.

### Once-only stop and final-join limitations

`stop_hosting_for_acceptance` writes `stop_pending` before the POST; an existing
matching pending journal permits observation only, never another stop POST.
The aggregate validator requires `phase=stop_confirmed`, matching parent/version,
`stop_http_status=204`, idle readback, matching finite positive `stopped_at`
newer than `previous_stopped_at` (if present), and `restart.stops == [parent]`
from actual boundary capture. Workflow
`test_unknown_host_stop_is_observed_not_sent_again` demonstrates that an
uncertain POST can later be observed idle **without** a recorded HTTP status.
That safe reconciliation is not aggregate G6 acceptance: the missing 204
receipt remains missing; never repeat stop to manufacture it. Unknown effects
remain held unless supported evidence reconciles them. No hard-crash or
universal exactly-once guarantee follows from this supported-stop test.

`validate_scenario_evidence(initial, followup, restart, isolated,
stopped_session)` needs all five inputs for the **final join**, including
restart-versus-isolated effect comparisons. This is not a scheduling
dependency on successful recovery for isolation. Preserve independently
collected isolation observations until final joining is possible; do not
fabricate restart data or change the validator. Its syntactic content exclusions
are bounded synthetic checks, not a proof of all possible information leakage.
Account-wide Blob permission still relies on application enforcement, not
storage-RBAC or malicious-host isolation. Validator acceptance authenticates
neither source/package/version receipts nor log provenance, outbound principal,
platform identity resolution or process ownership. Raw-ingress/response and
cross-container association gaps from IP-S2 remain explicit.

`live_acceptance.py:run` emits a per-turn proof and service readbacks; it does
not export the full aggregate snapshot's manifest, cumulative operation
documents, independently counted sends/creations/stops or checkpoint records.
`ScenarioEvidenceTests.capture` obtains those from synthetic MemoryBackend,
CapturedRemote and InMemoryCheckpointStorage, not a deployed evidence collector.
Original DevOps/E2E must identify supported authorized private collection
seams for the missing records, or return the exact unavailable comparison to
Architect/Scrum. This companion promises no new collector or SDK-internal
access. Aggregate comparisons also do not fetch historical Blob versions or
prove ETag fencing: retain independently attributable immutable artifact-byte
and publication/effect evidence where needed, rather than infer it from a
matching ref or a correctly hashed supplied snapshot.

### Missing receipts and smallest receiving handoffs

All following live evidence is **missing for this correction**, not fabricated
by the fixtures or by this document:

1. **Original DevOps -> continuity:** final common-package/source and three-role
   active-version readbacks, current-effect readiness and completed non-held
   initial parent; both child hosted/framework identities/pins, actual responses,
   immutable artifacts/prerequisites and independently observed creations/sends.
   Private pre-send purpose/intent and ownership are required for new traffic.
   The historical held parent must never be reused to fill this gap.
2. **Original DevOps -> recovery:** completed initial/followup pair and accepted
   comparison; exact active parent/version; durable once-only stop intent,
   actual stop boundary/204/idle receipts, followup/restart checkpoints,
   cumulative journal/output/send reconciliation. Known-response retrieval alone
   cannot supply those receipts. A missing stop receipt or unknown effect is a
   concrete unresolved comparison, not authorization for another operation.
3. **Original DevOps -> independent isolation:** final bindings and safe
   completed comparison parent/scope, distinct synthetic intent/state and
   isolated parent/both-child/artifact/effect/content observations. No
   recovery-success handoff is required to schedule it.
4. **Original E2E -> existing review/closeout:** attribute and compare actual
   private snapshots, retain partial independent observations and identify
   unavailable model-history/stop/checkpoint/request-accounting evidence.
   Route a demonstrated source defect or essential unsupported comparison to
   original Architect/Scrum scoped replanning; do not guess a remedy, relax the
   trust gate or add runtime work to this documentation assignment.
5. **IP-S3-DELIVERY-JOIN -> original Scrum/E2E/DevOps/closeout:** this companion's
   exact reviewed commit/anchor and votes plus the separately reviewed measured
   status handoff; then original delivery, all AC1-AC9/G1-G8 receipts,
   newly owned process/listener cleanup and honest historical UNKNOWN/unproven
   cleanup accounting. Local preparation can complete while these remain open.

The existing native-preflight denial remains localized to original DevOps/
operator supported interactive approval; its exact missing permission and
native tool/authentication readiness remain unproven. This task does not retry
it, request routine authority again, or block independent comparison/status
preparation. No new live identity root cause or supported remedy is established.

### Local preparation verification

The documented `Test-Demo.ps1` with existing absolute Python and explicit
selected-lab root passed dependency checking, **278 tests in 47.334 seconds**
and compilation. `scripts/Test-Repository.ps1` passed current index, 113-file
public boundary, JSON, PowerShell, frontmatter and whitespace checks.
Direct assertions verified the complete preexisting IP-S2/historical suffix
unchanged, new links/anchors/named fixtures and owning-repository commit refs,
and unchanged runtime/test source relative to `c52786b7`. No dependency install,
retained-tooling change, package, live effect or cleanup operation occurred.
These checks verify preparation only; original Architect/Critic review of this
new companion remains pending.

## IP-S2 prospective diagnostic evidence overlay — October 22, 2026

**Preparation only: NOT SENT, NOT LIVE-READY, no identity remedy selected.**
Developer task `IP-S2-DIAGNOSTIC-EVIDENCE` owns this overlay, not publication,
live diagnosis or formal E2E. The RP-S1 content below is unchanged history;
its A/B trial suggestions, historical permissions and finite sequence are
not the current execution plan. Current authority prohibits new RBAC or
infrastructure changes and replay of held/UNKNOWN operations.
This checklist introduces no extra publication approval gate.

### Applicable source and original decisions

Read against application runtime/test baseline
`c52786b7dd1595f3048a78061f893dc79635069f`, SprintArchitecture
`833b4ad90a8429cc6b1453abf5ece22eb54c51d1` and SprintDesign
`6aaf96018ab5c5f2b7ab8a74eceaf1fc09638ab5`, on
`feature/customer-hosted-session-prototype`. The changed release pair names
selected-lab `9b4919d8bcdbf07203f32657936c27328ea6ccc1`; this is not a
deployed package/version claim. The separate JOIN-HANDOFF task and original
same-sprint E2E own its exact-byte/loaded-root reconciliation.

Opened current architecture/design audits
`26adb308b85ae4732ca698f4dcdd8985c3c1096516154c481dad23e63ee9282f.json` and
`12edb53e8280ea614239d71ecd83c7e33a4a0d6628981387dc54014cb181cc6f.json`
under `gh-dynamic-workflows/.delivery-runs/eef04e5c-c5ab-4b88-90f6-4a99dd4692ed/context/`:
both record `agreed`, all original
reviewers `agree:true`, `taskComplete:true`, no unmet criteria. These votes
accept those bounded documents, not this overlay or cloud execution.
Use the [current sprint architecture](customer-prototype-sprint-architecture.md#current-ip-s2-exact-changed-join-guarded-publication-and-live-localization),
[Screen F/G design](customer-prototype-sprint-design.md#screen-fg-reading-order-and-state-layout)
and [finalized coverage](identity-profiling-coverage.md#ip-s1-integration-join).

Apply the provenance-qualified decisions at
`yaml-loops-v1:sprint/1/IP-S1/DevOpsWorkLoop`:
`RELEASE-CHANGED-JOIN-HANDOFF` retains original E2E before DevOps;
`RELEASE-COMMON-PACKAGE-PUBLICATION` requires the new common package and all
three role bindings; `RELEASE-LIVE-ACCEPTANCE` retains real cloud acceptance.
At `yaml-loops-v1:sprint/1/IP-S1/task/IP-S1-SDK-POLICIES/AssignedWorkDeveloperLoop`,
`SDK-CREDENTIAL-TIMEOUT-PRESERVATION` and `SDK-TIMEOUT-REGRESSION-EVIDENCE`
remain within their accepted SDK source/test boundary. No task is reopened
and no criterion is waived here. Historical COMMON rollback ZIP/build
provenance remains **WAIVED, never PASS**.

### Private pre-send checklist — original DevOps must populate, not this task

Keep actual values and receipts exclusively in new private execution evidence,
outside public Git. Every field below is prospective/unpopulated here:

1. **Intent before effect:** record a distinct new diagnostic operation identity,
   timestamp, synthetic purpose, intended parent creation and remote specialist
   collaboration, expected writes/sends, owning run and execution owner.
   Distinguish this intent identity from the application's subsequently derived
   `operation_id(scope, response_id, step)` and each write-ahead effect.
   Do not reserve or reuse the historical held parent's identity/session file.
   List protected held/UNKNOWN operations privately, without resending them.
2. **Exact release bindings:** actual reviewed application/lab source pair and
   accepted changed-join E2E reference; common package content hash/identity,
   dependency/hosting gates, and separate coordinator/architect/reviewer active
   version and package readbacks. All three must bind the same new package.
   Planning commits, local hashes and declared versions are not publication.
3. **Current-effect readiness:** retained authorized release/connectivity route,
   trusted-host evidence, dedicated nonproduction authentication/context and
   current operation/effect reconciliation receipts. Preserve existing safety
   budgets. Verify no unresolved effect is being retried; do not treat the
   rollback waiver as current source/package/trust/effect readiness.
   Missing accepted changed-join evidence blocks dependent effects only.
4. **Capture plan:** source/version-labeled private streams, exact new parent and
   both child response/session associations when available, bounded diagnostic
   events and existing acceptance captures. Mark historical/local/new-live
   evidence separately. Record log time/byte truncation and unavailable joins;
   `emit()` success is not durable delivery. Do not enable raw SDK debug logging
   to obtain complete headers, token/credential responses, bodies or settings.
5. **Owned effects and cleanup:** before launch record baseline listener/process
   ownership and any newly created process PID, start identity, parent/run,
   command purpose and listener endpoint privately. Track handles/resources
   created by this operation, including retained tooling's temporary resources.
   On exit use supported scoped cleanup of attributable newly owned resources;
   confirm the exact process/listener is gone and preserve receipts. Never kill
   by name or remove another owner's listener. Classify cleanup as confirmed,
   incomplete or not applicable; stop invoking if ownership/effects are uncertain.
   A preexisting tunnel is not newly owned merely because this diagnostic used it.

Only original DevOps, after accepted gates and actual readiness, records intent
and sends necessary new synthetic traffic. This document creates no operation,
readiness receipt, process or listener.

### Screen F: observable intervals and association limits

`demo/diagnostics.py` defines schema version 1 and bounded `Event`,
`Observation`, `Binding`, `Coverage`, `Presence`, `Match` and `event_fields`.
Record coverage independently from presence: `observed` can be `absent`,
`empty`, `nonempty` or `malformed/duplicate`. `unavailable` and `not reached`
have no presence value; an omitted slot is not an absent identity.
Missing logs alone cannot prove a checkpoint was not reached: distinguish
supported control-flow evidence from capture loss/unavailable coverage.
`compare_values(..., same_representation=True)` reports true/false only for
nonempty valid exact builtins of the same type; otherwise `not-comparable`.
Never compare public delegation with platform identity as interchangeable values.

| Interval / source hook | Actual observable evidence | Association and unavailable observations |
| --- | --- | --- |
| Coordinator trusted preparation/resources: `demo/workflow.py:create_workflow`, `parse_turn`, `WorkflowRuntime.resources`; `demo/host.py:context_checkpoint`, `execution_checkpoint` | Scope and `get_request_context()` user presence, call presence and safe scope/request equality at preparation, request/background and executor/resource entry. | Hooks observe, never populate identity or authorize a request. Recovery can skip parser; executor/resource hooks still observe. No request object means scope user unavailable. Missing/empty trusted context may reject before public hooks. |
| Actual outbound: `demo/foundry.py:OriginTransport.handle_async_request`, `_observation`, `_ObservedStream` | Final HTTP header presence for delegation, platform user and call; bounded role/method/route/status/timing/category, send/headers/error/cancel/stream-complete/stream-closed. | One local observation alias pairs a send with its response/stream events. Role is the emitting process role, not necessarily the specialist destination. Exact endpoint is intentionally reduced to a route template. Neither header presence nor response status identifies the bearer principal. |
| Platform interval between actual outbound and container ingress | No application-controlled platform identity resolver checkpoint. | **Unavailable** authenticated outbound principal, effective impersonation resolution and platform mapping. Missing `x-ms-user-identity` at ingress alone proves neither translation nor loss; platform-delivered `x-agent-user-id` is a separate observation. |
| Raw receiving host: `demo/host.py:IngressDiagnostics`, public `add_middleware()` before `run()` | Case-insensitive raw multivalue header presence before SDK parsing; ingress send/response-headers/final-body/disconnect/error/cancel. Receive/send bodies and authorization are unchanged. | New request-local observation alias is not a wire trace or response ID. Inherited context can pair reachable in-process checkpoints with this alias; it does not itself connect caller and callee. ASGI final body can precede resilient background work. |
| Pinned SDK preparation/options/parser/execution: `prepare_diagnostic_options`, `WorkflowPreparationDiagnostics`, workflow hooks above | `background` stage means the request's background option at the hook, not proof that HTTP already exited. Exact pinned preparation rejection yields `execution_rejected` with request-context presence; scope may remain unavailable. | `NATIVE_HOST_PRINCIPAL` identifies a missing resolved trusted context at that boundary, not its upstream cause. Pinned endpoint normalizes empty user to absent in ambient context. Background tasks inherit immutable local aliases in tested paths; crash reconstruction may have no original alias or raw ingress. |
| Other SDK HTTP: `demo/artifact_store.py:SDKDiagnosticsPolicy`, supported Blob transport and credential options; `demo/foundry.py:ProjectClient` | Bounded session/storage/credential events through the accepted supported seams, separately from httpx2. | Credential raw hooks do not observe transport errors/cancellation/cache hits; untested branches stay unverified. SDK-owned history/session/checkpoint/workflow-binding/response-store HTTP and CLI internals remain outside coverage. See coverage matrix, not a universal interceptor claim. |

**Private association procedure and hard limit:** retain the outbound fixed
`Diagnostic response_alias=... Native outbound context response_binding=...`
record with its local lifecycle events. `WorkflowRuntime.resources` supplies
its current **parent execution response** to the transport; the retained
response binding is a digest of that response ID, not an identity hash.
`live_acceptance.py:outbound_identity` verifies that exact response digest and
role/presence booleans. Its parser does not expose the new local alias.
This binds caller observations to an execution response, not automatically
to an individual specialist operation or the specialist response.

On the receiver, `ingress_identity` recognizes only the pinned SDK's
`Creating response <exact response ID>` flags. Those are SDK context flags,
not raw-ASGI header presence. Pair an inherited raw-ingress alias with
reachable context events only where actually present; use private known
response/child/journal records for the separate response association.
The current code supplies **no guaranteed exact raw-ASGI-alias to SDK-response
or cross-container wire join**. Operation/response aliases are optional local
UUID aliases, not actual journal IDs; their type alone establishes no join.
Do not fill gaps using timestamps, role order, formatted IDs, identity values
or hashes. Any allowlisted external request/trace metadata must have observed,
supported provenance; this event schema does not promise a gateway trace ID.

`observe_host_failure` extracts only the retained fixed failure, storage-code,
ingress and outbound records. It does **not** collect/project the new structured
event schema into an acceptance report. Original DevOps may retain available
bounded private log records using the authorized route, without changing
machine stdout or inventing an aggregator. Unsupported associations remain
explicitly unavailable. If a stronger association becomes essential, return
the concrete missing criterion to existing Architect/Scrum coordination,
not speculative runtime instrumentation in this documentation task.

### Screen G: milestones are not execution acceptance

| Milestone | Existing source/assertions to consume | What it cannot establish |
| --- | --- | --- |
| Request send | OriginTransport `send`; private write-ahead prepared/dispatched effect plus independently observed boundary sends/creations | Intent is not an observed send; a send is not a response or accepted effect. |
| HTTP headers | `response_headers`, HTTP status and exact source/version capture | HTTP 2xx is not a completed specialist or successful turn. |
| Stream/ASGI outcome | `_ObservedStream` outcomes, ASGI final body/disconnect/cancel; retained host and transport tests | Exhaustion/close/final-body is not accepted collaboration, even if an SDK envelope says completed. Enumerated `execution_complete` is not a guaranteed emitted completion hook. |
| Actual non-held initial outcome | `live_acceptance.py:events`, `validate_artifact_evidence`, `validate_exercised_versions`, `_evidence_turn`, and `run` | Validators check supplied records, not their live origin, transport authentication, private Blob network provenance or cleanup. Independently attributable captures remain necessary. |

For G1-G4, original DevOps must provide final-package proof for all three roles,
genuine Decision-1 choices after deterministic gates, remote architect then
reviewer, and managed-identity/private Blob provenance. Existing assertions
require matching parent scope/hosted and framework session, coordinator version,
active response and manifest `ACCEPTED_ADVISORY`, no pending/unreconciled effect,
and both distinct bound specialist sessions/framework IDs/versions.
Requirements/candidate/review must match current manifest refs, accepted
producer role/name/session/version/response and content. Reviewer inputs must
be the exact current requirements and candidate refs, not an earlier candidate.
Decision refs/content/producers and prerequisite scopes must also agree.

`_evidence_turn` additionally checks immutable operation transitions, prepared
intent, dispatched create/call, accepted effects, exactly two child creations,
unique responses, independently captured send/create counts and delegation to
operation/output-response association. A held parent, `SPECIALIST_INCOMPLETE`,
unknown effect or merely plausible useful prose is not this handoff.
Retain private capture provenance and attribution; do not paste real bindings
or private logs into this document.

### Supported-remedy decision and private external handoff

State the last attributable successful boundary, first failed/missing boundary,
coverage gaps and alternative explanations separately. Evidence of outbound
presence plus missing resolved scope only localizes the **observable interval**;
it proves neither missing RBAC nor a platform defect or caller principal.
Do not substitute a header, call ID or arbitrary inbound identity, remove
`Assignment.validate_receiver` equality, or suppress an existing rejection.

A supported source/configuration remedy needs actual attributable observations,
matching pinned SDK/public contract, exact affected factory/configuration owner
and a regression that reproduces the demonstrated defect. Existing
Architect/Scrum roles route any material contract/scope decision with
Architect-advised Product Owner; scoped supported corrections receive original
review, affected checks and a new exact common package before live reassessment.
No live defect or remedy is established by this preparation.

If the unresolved interval genuinely needs platform tracing, prepare privately:
new diagnostic intent/effect and package/three-version receipt references;
minimal exact caller/receiver response associations and available allowlisted
request IDs; last/first observable boundaries with coverage/truncation labels;
the pinned SDK/header contract and precise unresolved question (authenticated
caller principal and platform delegation resolution for that new request).
Exclude bearer tokens, identity values/hashes, credential responses, bodies,
complete headers and private settings. Keep source records private, do not
submit/upload logs or open a provider case. External tracing/access requiring
new authority is a bounded external handoff, not permission to replay.
Continue independent approved construction through existing planning.

### Smallest IP-S3 handoffs and retained offline evidence

- **Follow-up:** needs a completed non-held initial parent, both child bindings,
  final package/versions and accepted artifacts. `_evidence_continuation`
  checks same scope/parent/framework/both children/pinned versions, fresh parent
  response and child calls, advanced turn/generation, unchanged prior journal,
  no extra creations and updated requirements/current approvals.
- **Once-only supported stop/resume:** execution consumes that completed chain
  (the retained full scenario uses initial then follow-up), idle/no-pending
  effect and exact coordinator target. `stop_hosting_for_acceptance` plus
  `validate_scenario_evidence` require confirmed 204/idle/new stopped timestamp,
  exactly one observed stop POST and scoped retained/advancing MAF checkpoints.
  Restarted terminal alone is not stopped/recovered hosting. Prepare comparisons
  offline now; do not execute stop or resume in this task.
- **Separate-parent isolation:** independent of recovery success; can prepare
  and schedule against final deployment and an actual comparison parent scope,
  both-child/version/artifact/effect evidence. `_evidence_turn` validates its
  standalone accepted turn; the full `validate_scenario_evidence` additionally
  compares the completed chain for distinct parent/child/framework/prefix/effect
  identities, no leaked requirements/content and no release drift. Its combined
  signature requires all four captures; do not call that a standalone live
  isolation pass or fabricate missing recovery captures to satisfy it.
- **Known-response recovery:** exact retrieval only; it is neither a new
  invocation nor another POST/create. Preserve all historical held operations
  and uncertain sends. Never clear pending state to manufacture a new send.

Source-bound retained fixtures include
`tests/test_host_diagnostics.py` (actual pinned resilient nonstream after HTTP
exit, missing/empty principal rejection before hooks, stream disconnect,
cancellation and failed sink);
`tests/test_transport_diagnostics.py` (final-header, stream and recovery);
`tests/test_scenario_evidence.py` (actual offline graph, identities/versions,
extra creations/duplicate sends/unreconciled effects, exact reviewer inputs,
stale approval, once-only stop/checkpoints, isolation/content/release drift).
These are synthetic regression evidence, never deployed observations.

Original Architect/Critic review this overlay. Original DevOps receives only
this prospective checklist after its actual release prerequisites; original
IP-S3 planning receives only the completed-parent/final-binding dependencies
above. No UI/schema/CLI/service, settings, dependencies, live invocation,
publication, stop/resume or cleanup action is added here. Machine stdout and
private stderr evidence boundaries remain unchanged. Original AC1-AC9/G1-G8,
live attribution, cleanup, review/retro and release closeout stay incomplete.

### Developer verification for this overlay

Executed from the application root using the existing absolute Python
`<linked-lab-root>/.venv/Scripts/python.exe` and explicit
`-LabRepositoryRoot <selected-feature-lab-root>`:

- `./Test-Demo.ps1 -Python <absolute-python> -LabRepositoryRoot <explicit-root>`:
  exit 0, **278 tests PASS in 41.222 seconds**, dependency check and compilation
  passed. These rerun synthetic application checks support source references,
  not formal changed-join E2E or a new Linux/cloud result.
- `./scripts/Test-Repository.ps1 -Python <absolute-python>`: exit 0,
  current index, **113 public files**, public/private boundary, JSON, PowerShell,
  frontmatter and whitespace passed. The pre-existing unowned specification
  inventory overlay was present; this is not clean-checkout certification.
- Direct assertions passed: the retained historical body is unchanged, overlay
  local links/anchors resolve, and cited application runtime/tests still match
  `c52786b7`. During final checking one repository run stopped at
  `REPOSITORY_INDEX_STALE` while the shared checkout advanced to concurrent
  JOIN-HANDOFF commit `8b6092a5b6dc228e51245990043f2382b4f26984`. A subsequent
  read-only comparison found actual/expected index identical; rerunning the
  normal repository entry point passed without editing the index. The transient
  mismatch's exact cause was not established; no failure is converted to PASS.

No runtime/test/lab paths were edited. No new path or architecture change
requires an index refresh; preserve the unrelated index/specification overlay.
No dependency installation, authentication, settings import or network/cloud
execution was needed. Original reviewers still assess this deliverable.

## Retained RP-S1-ID-HANDOFF: offline identity candidates, live selection unresolved

## Boundary and result

Developer assignment `RP-S1-ID-HANDOFF` starts from application
`0c43d599760b5213a5b5bd82cfd4e40aede895fa` on
`feature/customer-hosted-session-prototype`. This handoff adds an executable
**offline-only** discriminator and a non-installed delegation candidate. It
does not change hosted runtime behavior, dependencies, lab files, permissions,
deployment or machine-readable acceptance output.

**Selection: `unresolved`.** A tests the existing opaque-call plumbing; it does
not establish an authentication/configuration mismatch or correction. B adds
the documented delegated header to an isolated specialist client in synthetic
tests. The real child principal/namespace, effective permissions, and platform
handling of simultaneous call/delegated headers remain unmeasured. Neither path
is live-selected. HTTP serialization success is not trusted specialist ingress.

The five upstream completion dispositions remain closed within their original
boundaries, including
`["yaml-loops-v1:ArchitectureLoop","architecture-loop-status-reconciliation"]`,
`["yaml-loops-v1:UserExperienceLoop","ux-loop-status-reconciliation"]`,
`["yaml-loops-v1:ReleasePlanLoop","release-plan-loop-status-reconciliation"]`,
`["yaml-loops-v1:sprint/1/RP-S1/SprintDesignLoop","sprint-design-loop-status-reconciliation"]`
and
`["yaml-loops-v1:sprint/1/RP-S1/SprintArchitectureLoop","sprint-architecture-loop-status-reconciliation"]`.
No accepted continuity, terminal or documentation implementation is redispatched.
These dispositions do not supply this assignment's Architect/Critic votes.

## Source and version applicability

Public contracts re-read on October 20, 2026 UTC:

| Source | Applicable finding |
|---|---|
| [User isolation](https://learn.microsoft.com/azure/foundry/agents/how-to/isolate-sessions-per-user), revision `f5104405dfd0231d706f8198fb841f45826595b9`, October 13 | `x-ms-user-identity` accepts 1-256 ASCII letters/digits or `._:-@`; derive it from authenticated server-side identity. The explicit `Microsoft.CognitiveServices/accounts/AIServices/agents/endpoints/UserIdentityImpersonation/action` is required; built-in role names or wildcard coverage do not prove it. |
| Same user-isolation contract | Delegated identities are **not fenced from each other** by the platform. Delegation requires application-owned user/session routing. Header presence alone cannot establish parent isolation or equality with the original platform-derived principal. |
| [Hosted runtime contract](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agent-contract), revision `69a226754528e8d4d032ec652eba7d82e584f648`, September 28 | Retain opaque-call forwarding; do not forward the container-only user header. The public contract does not demonstrate which principal a nested call plus explicit delegation produces. |

Inspected installed Windows AMD64 Python **3.12.10**:
Core **2.2.0**, Responses **2.3.0**, Foundry integration **1.14.0**,
AI Projects **2.7.0**. The command audits the complete lock against the installed
environment. These are not fresh container observations.

Relevant current source boundaries:

- `demo/workflow.py`, `WorkflowRuntime.resources()`, shares its project/header
  resources with model/routing/state paths. Do **not** simply replace its shared
  headers with B; the offline candidate is not wired there.
- `demo/foundry.py`, `RemoteAgents.prepare/create/_check/recover_creation`,
  passes explicit headers to raw Azure SDK operations.
- `RemoteAgents._client/invoke/recover` and `ProjectClient.get_openai_client`
  use a separate OpenAI/Responses default-header path. Recovery retrieves the
  exact response with its child session query; it is not another send.
- `demo/artifacts.py`, `Assignment.validate_receiver()`, compares the actual
  trusted child principal to the parent binding, and validates child version,
  parent manifest and exact prerequisites. Do not remove equality to select B.

## Executable offline handoff

Use the existing pinned Python by **absolute path**. No installation is needed.
Run from the application root:

```powershell
$python = '<absolute-validated-python>'
& $python .\scripts\identity_handoff.py `
  --application-root '<absolute-application-root>' `
  --lab-repository-root '<absolute-lab-root>' `
  --scenario offline-A-B `
  --coordinator-version '<inventory-coordinator-version>' `
  --architect-version '<inventory-architect-version>' `
  --reviewer-version '<inventory-reviewer-version>'
```

All three versions are required positive decimal strings, explicitly reported
as **operator-declared, not cloud-observed**. They are not silently used to
claim tested/deployed versions: synthetic remote fixtures use version `7`.
The runner verifies absolute repository roots, audits lock pins, fingerprints
the candidate/tests and relevant runtime source, then runs nine named probes
in one captured child process with a 120-second local watchdog. That watchdog
is not a live traffic budget or a new delivery limit.

Output is sanitized JSON on stdout: no header values, full session IDs,
transcripts, tokens or root paths. Exit **2** means offline candidate verified
but live selection **unresolved**; **1** means an input/runtime/probe failure.
There is deliberately no live option and no exit-0 live PASS.

`candidate_headers()` lives only in the script. Its arguments must come from
the authenticated host, not assignment/client/model JSON. It checks the complete
parent scope, copies rather than mutates SDK context headers, rejects unexpected
platform header keys and invalid delegation syntax, and refuses a user equal
to the opaque call ID. Python object equality cannot independently attest that
its caller supplied trusted context; production wiring must preserve that trust
boundary. A remains the unchanged SDK opaque context; B adds only
`x-ms-user-identity`, never `x-agent-user-id`.

### What the new tests actually establish

`tests/test_identity_handoff.py` exercises:

1. Both A/B candidates and both roles through real `RemoteAgents` lifecycle
   methods. `prepare/create/_check/recover_creation` headers are observed at
   **mocked raw SDK operation arguments**, not a real Azure wire or server.
2. Real `ProjectClient`/`FoundryAgent` Responses serialization reaches a captured
   `httpx2.MockTransport`: one intentional failed POST then exact known-response
   GET, carrying the candidate headers on both paths. No application specialist
   executes. Each recovery adds zero POSTs and no creates.
3. Failed exact retrieval stays `SPECIALIST_INCOMPLETE`, without creating,
   sending, or advancing framework state.
4. Actual `Assignment.validate_receiver()` for both roles accepts a matching
   synthetic fixture but rejects absent/changed-namespace/forged principals and
   another parent's manifest. These are controlled receiver inputs, not an
   observed platform namespace mapping.
5. Missing/invalid user, opaque-call substitution, forged/cross-parent scope,
   changed hosting session, container-header injection and shared-header
   mutation controls fail closed.
6. Invalid CLI roots/versions do not run probes or print supplied private paths;
   even verified offline results retain unresolved selection and exit 2.

These checks are additional offline evidence, not AC1/AC2 or G1-G8 live proof.
Raw SDK serialization and effective authorization still require the downstream
bounded test; the mocked arguments must not be cited as measured ingress.

## Exact unresolved execution boundary and next owner

No cause-specific A mismatch is currently measured. The B header mechanism is
documented, but nested opaque/delegated coexistence and principal compatibility
are not established by that documentation or the local tests. The current
runtime shares resources with non-specialist operations; this script is not
installed in a hosted bundle and cannot make existing versions execute B.
This assignment excludes publication, inference, permission writes and lab
edits. Therefore there is **no executable live discriminator in this change**.
This is an actionable unresolved handoff, not a claim that B is unsupported
or that provider action is the only remaining route.

Scrum Master with Architect advice should reconcile the concrete next delta
under the existing Product Owner scope process:

1. Join the separate fresh-inventory handoff: exact active versions/packages,
   actual outbound coordinator principal, both targets, explicit effective
   impersonation data action and held-operation locators. Do not reuse this
   document's declared versions as inventory.
2. Assign an isolated specialist-only project/header resource candidate and its
   lifecycle wiring, without changing routing/model/history/checkpoint authority.
   Any runtime/package or lab-runner work goes through the existing internal
   replanning handoff; no new user approval is requested for already-authorized
   ordinary scoped work.
3. Assign a deterministic lab-owned bounded decision runner. It must journal
   the source/package/exact target versions and **fresh synthetic scope before
   each intended effect**, retain unknown outcomes and stop on held work. Keep
   private IDs/evidence outside both repositories.
4. Proposed finite B sequence: architect metadata/create/read, one invocation,
   exact response retrieval if known, trusted entry/receiver comparison; only
   on success repeat for reviewer. Stop on namespace mismatch, absent principal,
   held/unknown effect or changed binding. Never retry a failed/uncertain send
   to obtain a successful-looking trace. A requires an observed supported
   configuration correction before a new trial, not unchanged republication.
5. If a permission delta is demonstrated, use reviewed lab scripts for the exact
   existing agent scope (or smallest documented supported project scope), record
   before/after/readback privately and reconcile uncertain writes before retry.
   No permission delta has been measured or executed here.
6. Required new bundle publication remains with DevOps after source/review/
   Linux/package gates; formal integration acceptance remains with E2E. A
   principal namespace mismatch requiring binding-contract change returns to
   Architect-advised PO/Scrum, not a receiver bypass.

Preserve original UNKNOWN publication, held parents, rollback bindings and
historical cleanup uncertainty. No effects were replayed; no live resources,
listeners or mounts were created here. No support case or private evidence was
submitted. The lab's existing unrelated dirty work remains untouched.

## Verification

Using the existing pinned lab Python 3.12.10 executable by absolute path:

- Final `Test-Demo.ps1 -Python <absolute-path> -LabRepositoryRoot <explicit-root>`
  passed dependency checking, **186 offline tests in 40.019 seconds**, and
  compilation. An initial new receiver fixture omitted its candidate revision;
  that fixture was corrected before these passing final checks.
- `scripts/Test-Repository.ps1` passed index, public/private boundary
  (**73 public files**), JSON, PowerShell, context and whitespace checks.
- The executable command verified **109 installed lock pins** and **nine
  offline probes**, returning intentional exit **2** and selection `unresolved`.
  The example execution supplied historical `23/17/15` only as declared version
  labels; it did not inventory or validate those deployments.
- Private settings were loaded solely through `Use-Settings.ps1`; local
  project syntax and lab/registry tenant/subscription linkage passed without
  printing values. Cloud authentication/context was not queried.

No dependencies were installed. The full retained lab release suite was not
rerun because no lab tooling changed. Final common-bundle/Linux checks, fresh
cloud inventory, permission readback, actual child ingress and release
acceptance remain downstream obligations. This artifact is ready for the
original Architect and Critic review; their agreement is not asserted here.

## RP-S1-ID-INTEGRATE: reviewed source reconciliation

The integration assignment inspected clean application HEAD
`13203ac6f902c6c573a34aed6e04cf09bb4a94b7` on
`feature/customer-hosted-session-prototype`. The supplied original Architect
and Critic reviews accept that identity-handoff commit. It is already on the
authorized branch: no cherry-pick, merge, branch switch or runtime edit is
needed. The reviewed source set is:

- `scripts/identity_handoff.py`
- `tests/test_identity_handoff.py`
- this document and `.github/repo-index.md`

Fresh ancestry checks also confirm the prior integration
`24b883f910dedbc8dc524177f29f59e061be265e` and all its recorded task commits:
`66144401bb9713922ef27c0418c793c3edb570f9` (coordinator),
`c454e500b8a43edb4dc79ab4d7d2360a823d63dd` (specialist continuation),
`56b762e6b67e96169eb216a4b0ebf9486beb3907` (terminal),
`e24fcb96de7ecdc9bb334d033aa067d6b7564aee` (documentation) and
`39c3b4e67fa01120c059e6dbd6115752d19d0376` (remedy research).
`git branch --no-merged HEAD` returned no local branches. No task source was
abandoned, no retained unmerged task branch needs an abandonment reason, and
no branch was deleted. Existing implementation is retained, not new progress.

The exact prior disposition
`["yaml-loops-v1:sprint/1/RP-S1/task/RP-S1-ID-HANDOFF/AssignedWorkDeveloperLoop","identity-handoff-status-reconciliation"]`
keeps the handoff complete within its offline boundary. It is not authority
to install candidate B or to claim either path works live. The five upstream
dispositions listed above likewise stay confined to their original outputs.

### Exact-source checks and reproducible downstream handoff

Using the existing absolute pinned Python 3.12.10 and explicit lab root,
integration reran `Test-Demo.ps1`: dependency check, **186 offline tests in
25.580 seconds**, and compilation passed. No dependencies were installed.
The executable command above was also rerun with **7/7/7 as synthetic declared
version labels**, not inventory: **109 installed pins** matched and all
**nine probes** passed. Intentional exit **2** and `selection: unresolved`
were preserved. The runner fingerprints the exact runtime/candidate/test/lock
source; downstream checks must regenerate and compare those fingerprints,
not substitute historical deployment labels.

The integration commit changes only this handoff and index freshness.
Candidate, tests, runtime, dependency pins, CLI and acceptance contracts are
byte-unchanged from the reviewed source. Its commit message records the exact
integrated commit set and repository-check result. Source checks receive that
commit together with `13203ac6f902c6c573a34aed6e04cf09bb4a94b7`.
These existing public commands reproduce the checks; the lab root and Python
are supplied by the operator, not embedded private settings.

Bounded decision receives the executable **offline** contract and the precise
unresolved execution boundary above. Join fresh inventory separately; this
assignment did not obtain it. Isolated runtime/package wiring and a deterministic
lab decision runner still require the existing Architect-advised Product Owner
and Scrum Master replanning handoff. This is internal scope coordination, not
a request for new user permission. No such architecture or contract decision
is made by integration.

No lab files, migration seals, settings, private evidence or held state were
changed. No cloud call, permission mutation, publication, live inference,
Linux hosting-package test or push was performed by this assignment.
Historical UNKNOWN effects, held parents, rollback bindings and historical
cleanup uncertainty remain preserved, not independently reconciled.
Formal integration acceptance remains with E2E and publication/cloud-pass
with DevOps. This reconciliation does not prove live AC1-AC9/G1-G8 or supply
new Architect/Critic votes for the integration deliverable.
