# Cumulative sprint architecture: evidence-ready source through live delivery

## Current IP-S3: continuity, once-only recovery and independent isolation

October 22, 2026. This current **SprintArchitecture** refines the retained
IP-S3 ReleasePlan and accepted SprintDesign `c544588b570a2e5ae9f6d5a88f2e96a32cc3ec77`.
It applies to the three tier overlays linked below. Earlier IP-S2/IP-S1 text
is retained history; its missing changed-join statements no longer describe
the current prerequisite. No runtime correction, additional role, UI feature,
SDK pin or product-scope change is established or assigned by this document.
Exactly three hosted roles and remote specialists remain required.

### Evidence baseline and changed condition

Opened the following current-run audits in
`gh-dynamic-workflows/.delivery-runs/eef04e5c-c5ab-4b88-90f6-4a99dd4692ed/context/`
(all filenames have `.json` suffix):

- Architecture `4241c18ddb85c123bb3e4d00c3c38658def66dd3fe04d77a6604f1d8056410a3`
  and ReleasePlan `0c2598dcfa07a6e154b8452a4baf4387d8d2dc0f4f6356193eb919c3f8181f67`
  record original agreement/completion for the model and bounded sprint scope.
- IP-S3 design `cb73116068dae88e649376c587fa360cd2f56a6b5b3b09a06e73065be7d14602`
  records Product Owner/Critic agreement and completion, with no unmet criteria.
- Changed-join E2E `4797ab07efa9ab46e5f8882caa9f7b3957910cec20b4c9ed5ec3574bbed1c8d2`
  records Architect/Critic/Product Owner agreement and completion for the
  bounded offline reassessment: application `13aecc39fba90d1475de057db07566c69b4ffc27`,
  runtime/tests `c52786b7dd1595f3048a78061f893dc79635069f`, selected-lab
  `9b4919d8bcdbf07203f32657936c27328ea6ccc1`. Captured Windows/Linux proofs
  retain their exclusions and emulated-host limitations; they are not live proof.
- Latest DevOps `dfd473725551074526ddec41e0dbc23a0ca81a6d7d265e89dbf8a669004f8a3f`
  records agreement on the partial report, but all three original reviewers
  retain `taskComplete:false`. Runtime ZIP/dependency preparation is not a
  final common bundle. Native WSL preflight was denied because no interactive
  response was available; the exact missing permission is unidentified.
  Native pinned-tool/authentication checks, publication and cloud tests remain
  incomplete. This turn does not retry that call or test an alternate route.

Application HEAD at inspection is `c544588b570a2e5ae9f6d5a88f2e96a32cc3ec77`
on `feature/customer-hosted-session-prototype`. Direct Git comparison from
`c52786b7` through that HEAD found no changes in `demo`, `tests`,
`live_acceptance.py`, manifests, package guard or application test entrypoint.
Documentation ancestry is not a newly deployed version. The accepted
source-pair handoff remains applicable to that unchanged runtime boundary;
current automated construction/package bindings still must reflect actual bytes.
Unowned specification/index changes are preserved, not clean-checkout proof.

### solutionModel: retained canonical graph and current step interpretation

This SprintArchitecture incorporates the machine-readable
[solutionModel](customer-prototype-architecture.md#solutionmodel) by reference:
ten components, five triggered flows, eighteen stable steps and unchanged
support links. No IDs, names or implementation relationships change. The
source/criterion matrix and handoffs below refine its affected steps only.
For this invocation, dated `release-package`, `release-discriminate` and
`release-close` descriptions are interpreted with the current authority:
historical COMMON rollback ZIP/build provenance is **WAIVED, never PASS**;
current package/source/version/trusted-host/effect checks remain; localization
is evidence-supported, not a finite A/B selector or guessed header substitution.
No rollback readback or manual checksum approval is recreated as a gate.

| Approved criterion / canonical steps | Components, actual modules and retained checks | Implemented / locally verified / deployed / live-verified distinction |
| --- | --- | --- |
| AC2/G5; `continuity-revise/invoke/verify` | Terminal client; Hosted coordinator/architect/reviewer; Parent and specialist conversation state; Private Blob artifacts and effect journal. `demo/terminal.py`, `demo/foundry.py`, `demo/workflow.py`, `demo/artifacts.py`; `live_acceptance.py::_evidence_continuation`; `tests/test_specialist_continuity.py`, scenario identity/creation/send/stale-approval/queue tests, workflow reject/revise tests. | Implemented and covered by accepted offline evidence; no new construction defect found. Final-package completed initial parent and actual follow-up observations are missing. Aliases, remembered text and SDK completion alone cannot pass G5. |
| AC4/G6; `recovery-stop/resume/verify` | Guarded lab release toolchain; MAF workflow checkpoints; conversation/artifact components and remote roles. Retained selected-lab wrapper; `demo/terminal.py`, `demo/foundry.py`, `demo/workflow.py`; `live_acceptance.py::validate_scenario_evidence`; scenario stop/checkpoint test and workflow stop/unknown-stop/known-response/checkpoint regressions. | Implemented and offline tested, not newly stopped/resumed or live-verified. Requires completed two-turn proof, exact active parent/version and reconciled durable intent. A supported compute stop is not hard-crash or exactly-once certification. |
| AC4/G7; `isolation-bind/execute/verify` | Terminal client; remote hosted roles; shared conversation, identity and artifact components. `demo/artifacts.py`, `demo/artifact_store.py`, `demo/workflow.py`, `live_acceptance.py`; scenario content/scope/release-drift tests and workflow two-parent rejection/isolation tests. | Implemented and offline tested. Final deployment/comparison scope and separate-parent live evidence are missing; recovery success is not a prerequisite. Application enforcement under account-wide Blob access is not storage-RBAC or malicious-host isolation. |
| AC3/AC6; `collaboration-review/return`, `continuity-verify` | Hosted specialists, Terminal client and artifact plane. `tests/test_workflow.py`, `tests/test_specialist_continuity.py`, `tests/test_demo.py`; unchanged machine stdout/parser and opt-in human stderr in `demo/terminal.py`. | Retain controlled reject/revise/history and presentation fixtures as offline proof; no new renderer or parser field. Useful live output still requires accepted artifacts/finalization. HELD/UNKNOWN overrides success-looking prose. |
| AC7-AC9/G8; `release-join/package/discriminate/close` | Guarded lab release toolchain, Terminal client, artifact plane and Trusted identity and private transport. `package_guard.py`, `Test-Demo.ps1`, `scripts/Test-Repository.ps1`, `live_acceptance.py`, README/release notes, retained selected-lab tooling; accepted coverage and diagnostic handoffs. | Changed-join E2E accepted and preparation partially executed. Final common bundle, three-role readbacks, actual cloud criteria, exact reviewed feature delivery/readback, attributable cleanup and original review/retro/closeout remain unproven. No publication or live pass is inferred from local checks. |

### Minimal handoffs and execution ordering

1. **Existing original DevOps release continuation:** consume the accepted
   changed-join audit, not another source-ledger task. Operator resolution of
   the exact denied native-preflight approval through supported interactive
   controls is the local unblock, not a new deployment authorization. Original
   DevOps then verifies native pinned tools/dedicated authentication and
   continues the existing prepared stage through its supported package interface,
   validating freshness rather than rebuilding unchanged preparation for credit.
   Complete automated current bindings/effect checks and serialize the existing
   publisher for one new common package across coordinator, architect, reviewer.
2. **Completed-parent handoff to continuity:** original DevOps supplies private
   final package/source/three-role readbacks, completed non-held initial result,
   trusted parent and both child hosted/framework identities, pins, actual
   response IDs, creation/send observations, current immutable artifacts and
   exact prerequisites. Record distinct new synthetic intent before necessary
   traffic. Only then send the queue follow-up on that same parent. Compare
   identity fields, not entire serialized sessions; retain earlier requirements,
   invalidate stale approval, prove exactly two child creations across the
   pair and fresh responses for new invocations. Known-response retrieval
   neither creates a new turn nor resolves an unknown specialist effect.
3. **Completed-two-turn handoff to recovery:** require that proof, current
   operation readiness and durable once-only stop intent bound to the exact
   parent/version. Confirm stop receipt and independently observed idle state;
   an uncertain stop remains held, never another stop request. Resume through
   supported existing state/checkpoints and reconcile prior journal records,
   retained checkpoint entries and new sends/outputs with no duplicates.
4. **Independent isolation handoff:** final deployed bindings plus a safe
   completed comparison parent/scope permit a distinct synthetic parent and
   its own children/artifact namespace. Do not require recovery success or a
   whole-sprint acceptance. Compare both parents' real hosted/framework child
   identities, pins, namespaces, content and effects; retain cross-scope
   rejection evidence. A new parent is not a workaround for replaying a held
   effect. If final package/version bindings change, do not silently migrate
   saved parents or combine incompatible observations into continuity proof.
5. **Evidence join and original closeout:** the existing
   `validate_scenario_evidence` interface takes initial/followup/restart/isolated
   captures and stopped-session evidence together. This final all-scenario
   join does not impose a recovery-success dependency on isolation execution.
   Preserve partial independent isolation observations for original review
   while final aggregate acceptance remains incomplete; do not fabricate a
   restart fixture as live input or add a replacement public parser API.
   Snapshot validation checks supplied observations, not their authenticity:
   original evidence owners independently bind private receipts to actual
   source, common package, active versions and effects.

### Work-conserving planning and bounded prior decisions

Scrum Master owns task decomposition, critical-path scheduling, shared-path
ownership and Git reconciliation in the existing SprintPlan. Ready independent
IP-S3 work is a concise acceptance/closeout companion mapping retained
comparison fields and fixture references to still-missing live receipts, plus
measured status and reviewed exact-ref delivery preparation. Reuse accepted
tests and Screen H/I/J/K contracts; do not redispatch already accepted fixture,
terminal or SDK implementation. If an actual comparison/source gap is found,
assign only its demonstrated criterion and regression through original roles.
No live parent or native-preflight retry is needed for that preparation.
The denied native operation gates dependent package/publication/live effects,
not these document/fixture-contract checks or approved delivery construction.

Apply exact prior reference
`["yaml-loops-v1:sprint/1/IP-S1/DevOpsWorkLoop","RELEASE-CHANGED-JOIN-HANDOFF"]`
as satisfied for the accepted unchanged runtime/selected-lab pair by the opened
changed-join audit, not as a release waiver. At that same origin,
`RELEASE-COMMON-PACKAGE-PUBLICATION` and `RELEASE-LIVE-ACCEPTANCE` remain
required. At
`yaml-loops-v1:sprint/1/IP-S1/task/IP-S1-SDK-POLICIES/AssignedWorkDeveloperLoop`,
`SDK-CREDENTIAL-TIMEOUT-PRESERVATION` and `SDK-TIMEOUT-REGRESSION-EVIDENCE`
remain satisfied inside their accepted unchanged SDK boundary. No disposition
is superseded and no additional approval stage or whole-sprint dependency
is added. IP-S1/IP-S2 remain partial; this architecture is not IP-S3 acceptance.

No new attributable observation establishes the authenticated outbound
principal, platform identity resolution or a supported identity remedy.
The [prospective diagnostic handoff](identity-candidate-handoff.md#ip-s2-prospective-diagnostic-evidence-overlay--october-22-2026)
still limits association: raw-ASGI-to-response and cross-container joins are
not guaranteed; timing or public-header absence alone is not identity loss.
Diagnostics cannot populate trusted context or suppress rejection. Any actual
supported remedy returns through affected original source/review/E2E/package
steps. Preserve trusted parent binding, deterministic gates before Decision-1,
immutable role outputs, exact prerequisite refs, ETag/fencing, MAF checkpoints
and write-ahead unknown-effect holds throughout.

Original closeout separately records implemented, locally verified, deployed
and independently live-accepted states; exact reviewed commits/readbacks and
attributable newly owned process/listener cleanup remain required. Preserve
historical held/UNKNOWN operations and historical cleanup uncertainty. No
secret/private settings access, external upload, infrastructure/RBAC/network/
DNS/quota/registry/VPN mutation, production profile or uncertain-effect replay
is authorized. Waiting requires the existing work-exhaustion audit; this
bounded architecture handoff is not that audit or unattended-readiness proof.

Architect accepts this cumulative/tier refinement for original Product Owner,
Critic and Red Team review; current reviewer votes are not claimed. Local
checks and the actual documentation commit are reported in the owner response,
not substituted for original DevOps cloud-pass or release closeout.

## Current IP-S2: exact changed join, guarded publication and live localization

October 22, 2026. This is the current **SprintArchitecture** overlay and
applies to all three tier documents. The IP-S1 sections below are retained
history, including their then-missing construction and permission observations,
not directions to repeat accepted work. Consume current SprintDesign
`6aaf96018ab5c5f2b7ab8a74eceaf1fc09638ab5` and retained Architecture,
UX and ReleasePlan references below. No new role, infrastructure, SDK pin,
identity authority, UI contract or product acceptance is introduced.

### Exact-source reconciliation and original evidence

The reviewed runtime/test baseline is application
`c52786b7dd1595f3048a78061f893dc79635069f`; its accepted original E2E audit is
`da4425177dd7b48116a3b6eb9aa04742eb2f0cb3d4d4196494c5a4416c2e34a0.json`.
The changed selected-lab source is
`9b4919d8bcdbf07203f32657936c27328ea6ccc1`, replacing
`1e9ddb8560a5637d639f4657111f3bca49d38d78` in the release join. Both use
`feature/customer-hosted-session-prototype`. Later application planning commits
are not new runtime bytes or an excuse to replay application construction.
Original E2E must explicitly bind the actual candidate source and loaded roots,
account for documentation-only ancestry and preserve unowned working overlays;
do not silently equate moving HEAD with the accepted runtime baseline.

Opened original DevOps audit
`f7b942e94652c10a41c6e32a96cef0d447c00995ec1fbcd2a35cb65a28677dec.json`
in the same current-run context directory named below. Architect, Critic and
Developer each record `agree:true`, `taskComplete:false`. Their agreement
accepts the bounded correction/report, not publication or cloud tests.
Original E2E reviewers Architect/Critic/Product Owner recorded agreement and
completion for the earlier join. IP-S2 SprintDesign audit
`12edb53e8280ea614239d71ecd83c7e33a4a0d6628981387dc54014cb181cc6f.json`
records Product Owner/Critic agreement and completion for design only.

Inspected the lab correction diff: `foundry-tf/multi-agent/Build-Demo.ps1`
adds individual read-only `.agentignore`, `.dockerignore`, `Dockerfile`
mounts only to the application test invocation; retained regressions assert
exact mount count, no broad/writable overlay and failure propagation.
The missing `/app/.agentignore` failure is a confirmed test-input closure
defect, not an identity defect. No runtime image construction, auth, network
isolation or accepted application fixture was changed.

Opened the referenced private DevOps `verification.json`. It attributes
278 Windows application passes and 236/240 retained passes (four exclusions);
Linux has 270/278 application and 197/240 retained passes (eight and 43
exclusions). Both corrected wrappers exited zero; exclusions are not passes.
The Linux selected-lab closure case was excluded without an explicit linked
checkout and passed in the linked Windows wrapper. The image was linux/amd64
on an arm64 host; no native-amd64-host claim follows. Captured streams are
combined tool output, not independently separated OS streams. These are
inspected prior execution results, not new Architect-run tests. Original E2E
assesses applicability and performs only necessary changed-join verification.
No final bundled package, current publication or new live pass is evidenced.

### solutionModel and criterion-to-source readiness

The machine-readable `solutionModel` remains incorporated from
[Architecture](customer-prototype-architecture.md#solutionmodel): ten components,
five triggered flows, eighteen stable steps and unchanged support links.
All IDs/names persist; no implementation child or additional flow is needed.
For this invocation, `release-package` excludes the historical rollback
prerequisite (WAIVED, never PASS), and `release-discriminate` means
evidence-supported localization, not a finite A/B trial or guessed identity
selection. Those dated canonical descriptions cannot override current authority.

| Approved criterion / canonical steps and components | Actual source and accepted contract | Current state / smallest missing handoff |
| --- | --- | --- |
| Profiling acceptance 1-3; `collaboration-bind/design/review`, `continuity-invoke`, `recovery-resume`, `isolation-execute`; Trusted identity and private transport and hosted roles | `demo/diagnostics.py`, `demo/foundry.py`, `demo/host.py`, `demo/workflow.py`, `demo/routing.py`, `demo/artifact_store.py`, specialist agent factories; `docs/identity-profiling-coverage.md` and focused tests | Implemented and locally verified at application baseline; retain accepted event API, public hooks, timeout preservation and gaps. No new source fix assigned. Deployment and independently live-verified identity behavior remain unproven. |
| Profiling acceptance 2-4; `release-join`, `release-package`; Guarded lab release toolchain | `package_guard.py`, `Test-Demo.ps1`, `scripts/Test-Repository.ps1`, selected-lab Build-Demo and `tests/test_release_native_settings.py` | Closure correction implemented with attributed Windows/Linux evidence. Original same-sprint E2E must issue updated exact-pair handoff; then original DevOps completes package/hosting gates and one serialized publication. |
| Profiling acceptance 5-6; `release-discriminate`, `collaboration-design/review`; Trusted identity and private transport, Hosted coordinator/architect/reviewer | OriginTransport final send, pure-ASGI ingress and reachable SDK/background events; coverage matrix; `live_acceptance.py` and retained guarded release tooling | New diagnostic only after current-effect readiness and privately recorded distinct intent/identity. Associate observations by safe supported bindings, not timing; localize interval, not an assumed principal/platform cause. Any supported remedy goes through affected original construction/review/E2E and new common package. |
| IP-S2 G1-G4 and retained AC1-AC9/G1-G8; `collaboration-return`, `continuity-*`, `recovery-*`, `isolation-*`, `release-close`; state, artifact and checkpoint components plus Terminal client | `demo/artifacts.py`, workflow/effect journal, remote specialist history, `live_acceptance.py`, retained scenario checks; accepted Screen F/G and B/C/H-K contracts | No new completed non-held parent or both-child final-package binding supplied. IP-S3 can prepare fixtures/evidence comparisons independently; actual follow-up and stop/resume consume completed non-held parent, while isolation needs final deployment/comparison evidence, not recovery success. Original review/retro/closeout and cleanup stay required. |

### Bounded dispositions and continuation routing

Apply exact reference
`["yaml-loops-v1:sprint/1/IP-S1/DevOpsWorkLoop","RELEASE-CHANGED-JOIN-HANDOFF"]`:
this amendment records the pair and original reviews. Scrum Master owns the
existing continuation amendment and Git reconciliation assignment; use the
supported same-sprint prerequisite recheck for
`sprint/1/IP-S1/EndToEndTestLoop` before the original blocked
`sprint/1/IP-S1/DevOpsWorkLoop`, when exposed in `continuation.recheckable`.
Do not edit runtime state or launch duplicate loops. Original E2E consumes
captured evidence, verifies changed bindings/exclusions as necessary, and issues
the updated handoff through Architect/Critic/Product Owner review. This is the
existing prerequisite, not another approval stage or blanket rerun.

Apply exact references at that same DevOps origin:
`RELEASE-COMMON-PACKAGE-PUBLICATION` and `RELEASE-LIVE-ACCEPTANCE`.
After accepted changed-join E2E, the single original DevOps owner continues
native common-package creation, automated current source/package/version/
trusted-host/effect checks and guarded all-three-role publication. Preserve
exact package and individual role/version receipts privately. A successful
publication, HTTP status, exhausted stream or SDK envelope is not G1-G4.
Do not consume this still-missing handoff merely because this architecture
is accepted, or relabel unfinished IP-S1 DevOps as completed IP-S2 work.

The exact references at
`yaml-loops-v1:sprint/1/IP-S1/task/IP-S1-SDK-POLICIES/AssignedWorkDeveloperLoop`,
`SDK-CREDENTIAL-TIMEOUT-PRESERVATION` and `SDK-TIMEOUT-REGRESSION-EVIDENCE`,
remain satisfied within their accepted implementation/test boundary as
recorded in original E2E/coverage. Preserve the raw-hook limitation (credential
transport failures, cancellation and cache hits are not covered); SDK-owned
stores and Foundry platform resolution remain outside documented coverage.
Do not reopen those accepted tasks or claim universal transport interception.

### Diagnostic decision and localized downstream boundaries

Record a new synthetic diagnostic's purpose, unique operation identity, exact
bindings, effect intent and attributable process/listener ownership privately
before send. Preserve the held original parent, known responses and UNKNOWN
effects; retrieval is not a new invocation. Observe actual final outbound
presence -> raw ingress presence -> SDK/request context -> reachable resilient
background/preparation checkpoints, distinguishing unavailable/not-reached
coverage from absent/empty/nonempty values. Diagnostics never supply trusted
identity or suppress a rejection. Missing public delegation header at ingress
alone establishes neither loss nor translation; formats need not match.

Only attributable evidence plus supported pinned contracts justify a remedy.
No call-ID substitution, guessed header mapping, private SDK patch, new RBAC,
infrastructure/network/DNS/quota/registry/VPN mutation, production profile,
secret retrieval, external upload or uncertain-effect replay is authorized.
If observations leave the platform interval unresolved, prepare a private
bounded external-tracing handoff without sending it; continue independent
approved construction. Report authenticated principal and platform resolution
as unproven until observed. Actual tool denial remains binding.

The missing changed-join handoff blocks dependent publication/live effects,
not accepted source, current design, independent IP-S3 preparation or bounded
evidence review. Scrum Master can schedule those through existing planning
without a whole-sprint dependency; shared files require explicit ownership.
No sprint/attempt/time/credit cap or new release gate is added. Waiting requires
the existing work-exhaustion audit, not merely this local prerequisite gap.
IP-S1 stays partial; no IP-S2 or release completion is asserted here.

Architect owns this bounded cumulative design; original Product Owner, Critic
and Red Team reviews are pending. Documentation/model checks for this turn
are reported in the owner handoff, separately from prior runtime evidence.
No new package, deployment, live request or cleanup action is performed by
this architecture amendment.

## IP-S1: paired transport, ingress and SDK-context construction (October 21, 2026)

This is the current **SprintArchitecture** for the identity-profiling increment.
It refines, rather than reopens, Architecture `e247969942a343c9b1662a59a54ef47c3c714386`,
UserExperience `56076795b4524e82ab4beb2b1f1ff958c26c7eac`, ReleasePlan
`4999ce5817a1714c6c2dc65ebbecb933bf49ecb4` and SprintDesign
`84bacadf163a5f8a0397078961bf4fd16401810e`. Opened their supplied JSON audits
in `gh-dynamic-workflows/.delivery-runs/eef04e5c-c5ab-4b88-90f6-4a99dd4692ed/context/`:
`4241c18ddb85c123bb3e4d00c3c38658def66dd3fe04d77a6604f1d8056410a3`,
`33b776afca6daafd69eee5bcf54a17ffd50ddda99fe1ab479ef0c10d3e4d1b32`,
`0c2598dcfa07a6e154b8452a4baf4387d8d2dc0f4f6356193eb919c3f8181f67`,
and `38e57ebfe79756be28cddd9e1ed30056ab753777175ff5c1d85af5dd90211f22`
(each with `.json` suffix). Each records agreement and taskComplete from all
its original reviewers, with no unmet criteria. These are document handoffs,
not acceptance of newly implemented diagnostics or new live capability.
Both supplied priorDispositions arrays are empty; no reconciled feedback or
additional blocked architecture decision is supplied.

This overlay and the current identity-profiling Architecture/ReleasePlan govern
this invocation. Earlier sections below remain dated history, not executable
directions. Historical COMMON rollback ZIP/build-provenance is **WAIVED**, not
PASS or a new prerequisite. Routine authorized checks do not require a new
manual sign-off; an actual current tool denial remains binding. No new RBAC,
infrastructure, secret access, external upload or uncertain-effect replay is
authorized. Current automated package/source/version/trusted-host and operation
effect checks remain required.

### solutionModel: retained model and sprint source bindings

The complete machine-readable `solutionModel` is incorporated by reference from
[Architecture](customer-prototype-architecture.md#solutionmodel): ten components,
five triggered flows, eighteen uniquely identified steps and unchanged support
links. This sprint introduces no new component, flow, hosted role or persona.
Diagnostics implement **Trusted identity and private transport**
(`identity-boundary`), shared once across the three hosted roles. The canonical
release-step descriptions are interpreted under this current overlay: historical
rollback inventory and finite A/B-trial wording do not reinstate waived gates,
invent a cap, authorize permission mutation or select an identity alternative.

| Approved criterion / canonical components and flow steps | Source seam and missing construction | Smallest contract and evidence handoff |
| --- | --- | --- |
| IP-S1 transport semantics; profiling implementation 1, 5 / Trusted identity and private transport; Hosted coordinator / `collaboration-design`, `collaboration-review`, `continuity-invoke`, `recovery-resume` | `demo/foundry.py`: `OriginTransport.handle_async_request`, `data_client`, `ProjectClient.get_openai_client`, remote invoke/recover; `demo/routing.py`: Decision HTTP client. Current OriginTransport checks origin and emits presence booleans on selected POSTs only; paired events and stream outcomes are missing. | Developer supplies shared event contract, actual final-header send/headers/error/stream fixtures, exact-origin and no-second-send recovery regressions. No live input is required. |
| IP-S1 host semantics/context; implementation 2, 3 / Trusted identity and private transport; Hosted architect; Hosted reviewer / `collaboration-bind`, `collaboration-design`, `collaboration-review`, `isolation-execute` | `demo/host.py`: retain `WorkflowPreparationDiagnostics`, replace chained native server construction/run only as needed to call public `add_middleware` before `run`; `demo/workflow.py`: `create_workflow`, `parse_turn`, request-aware executor/resource boundaries. Raw ingress and preparation/background checkpoints are missing. | Developer supplies pure-ASGI message parity, actual pinned resilient-background context and early-rejection fixtures; report unreachable hooks separately. Never populate trusted context from headers. |
| IP-S1 coverage/redaction; implementation 4 / Private Blob artifacts and effect journal; Parent and specialist conversation state; MAF workflow checkpoints / `collaboration-route`, `collaboration-return`, `recovery-resume` | `demo/artifact_store.py`: `BlobArtifacts` service factory; `demo/workflow.py`: `WorkflowRuntime._resources`; `demo/foundry.py`: ProjectClient, HostedJournal and credential factories. SDK-owned session/checkpoint stores are separate paths. | Developer supplies factory/transport/hook coverage matrix and supported Azure Core policy attachment where available, or explicit uncovered-path evidence. Installing one policy is not universal coverage. |
| IP-S1 construction join; acceptance 1-3 / Guarded lab release toolchain / `release-join` | Focused tests beside retained `tests/test_workflow.py` and transport/host regressions; `package_guard.py`, `Test-Demo.ps1`, `scripts/Test-Repository.ps1`. A new shared `demo/diagnostics.py` is permitted only if useful and included in actual package closure. | Reviewed exact source, event contract, coverage matrix and actual test commands/results to original Developer E2E, then original DevOps. No package allowlist/tooling change is presumed. |

These bindings cover all affected tiers; unaffected deterministic routing,
specialist history, immutable artifacts, ETag/fencing, MAF checkpoints,
write-ahead holds, accepted fixtures and terminal presentation remain retained.
The tier refinements are [coordinator](requirements/coordinator/architecture.md),
[specialists](requirements/specialists/architecture.md) and
[client/release](requirements/client-release/architecture.md).

### Shared event and lifecycle contract for construction

Use the accepted Architecture safe-event schema as the common interface before
parallel edits. A shared helper, if introduced, accepts only bounded explicit
fields, never arbitrary SDK objects. Include schema version, role, stage,
event kind, allowlisted method/route template, duration in milliseconds,
HTTP status, fixed error category and safe attributable binding where available.
Do not create a logging secret, new logging service or public diagnostic API.
Private structured logging must not leak into terminal machine stdout.

Presence states are `absent`, `empty`, `nonempty`, or `malformed/duplicate`
where actually observable. Coverage states are independently `observed`,
`unavailable`, or `not reached`; missing coverage must not become absent.
Scope/request-context equality is true/false/not-comparable only for equal
representations. Public `x-ms-user-identity` and platform `x-agent-user-id`
need not share representation or survive the platform unchanged. Case-insensitive
raw header inspection preserves duplicate information; it never selects a user.
Never log identity values/hashes, tokens, credential responses, full headers,
bodies, raw URLs/path IDs, queries, private settings or exception messages.

Distinguish send, HTTP response headers, stream outcome and execution outcome.
An exhausted stream, ASGI final body, handler return or SDK-completed envelope
does not establish successful workflow execution. Preserve exact-origin HTTPS,
TLS, no redirects, zero automatic retries, original chunks, receive/send messages,
disconnect, close ownership and exception/cancellation propagation. Diagnostics
must not read ahead, buffer a body, start a background replacement task or retry
an effect. Expected logger/serialization failure must not change authorization
or suppress the original rejection.

Use request-local immutable data or reset ContextVars; never cache a current
identity on middleware, transport or process globals. The pinned host can reject
trusted scope before the workflow factory/options hooks are reached. Retain its
existing preparation failure filter and diagnostic codes; observe safe context
there only if the expected pinned event occurs. Unavailable event/context is a
documented gap. Use public `prepare_options` and reachable request-aware workflow
hooks without patching SDK private methods or site-packages. Resilient-background
tests must exercise the actual pinned host path, including context after request
exit, not just a directly called fake factory.

Application ProjectClient session calls, Blob calls and credential acquisition
require individual factory/pipeline inspection; OpenAI Responses/model and
Decision HTTP paths use httpx2, not Azure Core. Before attaching policies,
verify the supported pinned constructor/policy option and preserve auth/retries.
Inventory SDK-created AgentSessionStoreProvider, CheckpointStoreProvider,
history/response stores and credential internals separately. If no supported
injection exists, record it as uncovered without claiming gateway visibility
or authenticated bearer-principal observation.

### Work graph, evidence states and downstream boundary

Scrum Master assigns concrete owners, shared-file coordination and Git
reconciliation in the existing SprintPlan. This architecture does not dispatch
new tasks or create another approval stage. After the event interface handoff,
transport/stream work and pure-ASGI/context fixtures can progress independently.
SDK inventory, redaction/concurrency tests, known-response recovery, packaging
closure and later approved offline acceptance preparation need no new live call.
Shared paths require coordination, not full-sprint serialization.

Developer's bounded handoff requires exact reviewed commits; event contract;
coverage rows with factory, transport, supported hook, events, gaps, test/source
references; missing/empty/case/duplicate and redaction sentinels; outbound
failures; stream/disconnect/cancellation/close parity; request/background
isolation; pre-factory and existing authorization rejection; and known-response
retrieval without another send. Preserve retained cases and stdout/parser.
Original E2E then executes documented application/repository checks with an
explicit existing Python and selected lab root. Changed release tooling also
requires affected retained lab regressions. Do not install dependencies without
a manifest change or observed missing tool. Actual Linux/hosting/package gates
remain original DevOps work.

| Evidence level at this Architect turn | State and next owner |
| --- | --- |
| Architecture/design contracts | Accepted incoming document handoffs inspected; this sprint refinement awaits Product Owner, Critic and Red Team review. |
| Profiling implementation and local verification | Inspected host/transport source lacks the new paired instrumentation; construction and focused/whole-suite runtime checks remain Developer/E2E work. This document does not assert those tests ran. |
| Deployed state | Accepted Architecture attributes historical successful three-role publication followed by `NATIVE_HOST_PRINCIPAL` and `SPECIALIST_INCOMPLETE`; no new publication/readback was performed here. |
| Independent live acceptance | Not established. Authenticated outbound principal, platform delegation and original ingress remain unproven; no RBAC/platform cause is diagnosed. Historical held/UNKNOWN effects remain untouched. |

The walking skeleton is final outbound -> raw ingress -> SDK/request ->
reachable background observation for a newly identified, intent-recorded
synthetic operation after reviewed source/E2E and current-effect readiness.
It exposes integration but cannot gate unrelated construction. Only attributable
paired evidence can localize an interval and justify supported remediation.
Unproven association is a gap, not loss inferred by timing. Preserve the held
original parent; no retrospective capture or resend.

Original DevOps consumes reviewed passing prerequisites, builds a newly
identified common package for all three roles and owns guarded serialized
publication and attributable cleanup. A supported correction, if justified,
returns through affected original construction/review/check/package stages.
An external tracing need blocks only that observation/remedy; continue independent
authorized work and prepare the smallest private handoff without external upload.

IP-S2/IP-S3 remain separate approved increments without whole-sprint dependencies.
Final common-package G1-G4 must prove completed non-held remote collaboration;
that parent gates same-parent follow-up and supported once-only recovery.
Isolation needs final bindings/comparison evidence, not recovery success.
AC1-AC9/G1-G8, original reviews/retro/closeout and owned cleanup remain actual
release conditions; historical rollback alone is WAIVED. Account-wide Blob access
still provides application-enforced, not malicious-host/storage-RBAC isolation.
Do not claim release acceptance from an accurate report, local fixture or
agreement on this design.

### Architecture verification and handoff

This turn's direct Python contract check passed: the parsed canonical model
equals accepted Architecture `e2479699`, with ten components, five flows,
eighteen steps, valid support/step references, existing current-overlay file
links and explicit waiver markers. Owned-path `git diff --check` passed.
The requested inventory refresh plus documented `scripts/Test-Repository.ps1`
command did not execute: tool permission was denied because no interactive
user response was available. No missing project authority or underlying
repository defect was identified; no alternate-path retry or constituent
substitute was used. The Python model check is architecture evidence only,
not that repository suite. Preserve the pre-existing index/specification edits;
no new file inventory entry is introduced by these four document refinements.
No runtime suite, deployment or live operation was performed by this turn.

Architect accepts this bounded cumulative design and tier handoff for original
Product Owner, Critic and Red Team review. Scrum Master next decomposes the
reviewed construction contracts. Full documented repository validation remains
unexecuted and must be recorded/resolved through supported interactive tool
permission before dependent execution; this is not a new manual checksum or
scope approval gate and does not block independent approved construction.

## Continuation 2: deliver the newly accepted customer-status handoff

Apply the [separate second amendment](customer-prototype-repaired-join-continuation-2-architecture.json).
Original agreements `266ca3fe` and `e94141c6` close the status correction and
prior pinned delivery respectively. The latter delivered only `b42ab2f8`;
fresh remote inspection still returns that ref. The newly reviewed correction
at `9ae328c8`, with reviewed architecture/plan ancestry, remains undelivered.
Existing closeout Developer can deliver exactly that ref without editing status,
repeating accepted construction or adopting this new planning ancestry.
Canonical components and runtime tiers remain unchanged; only `release-close`
for Terminal client / Guarded lab release toolchain is affected (AC8/AC9).

This is not an unchanged DevOps resume or an exhaustion finding. Required
repository approval and dependent execution remain blocked; independent exact
common-package/effect record coordination stays with original DevOps/Scrum.
No new locator or execution approval was obtained. Planning is not new progress;
later planning-only commits alone must not manufacture another delivery loop.
All actual Linux/package, common-byte/effect, live and cleanup gates remain.

## Remaining-execution continuation: actual stage entry, independent closeout

The separate [first-continuation architecture amendment](customer-prototype-repaired-join-continuation-architecture.json)
consumes original current E2E `bc39274e` and DevOps `15229112`, including their
original reviews. E2E is no longer unscheduled: permitted repaired-join suites
actually passed offline, while its overall FAIL retains the denied repository
check. Original DevOps also actually entered; its diagnostic-only provenance
finding closes a bounded reporting slice, not common rollback/effect readiness.
Do not replay either stage merely to update historical scheduling statements.

The amendment preserves the canonical solutionModel and runtime tiers. It
identifies two independent existing closeout-owner slices under `release-close`:
correct materially stale README/release status for original review, and deliver
already-reviewed documentation pinned to `b42ab2f8`, excluding this amendment
and the new status commit. Fresh application remote inspection
returned `8b50f343`; current local documentation extends through `b42ab2f8`.
This is a newly measured unfinished documentation slice, not redispatch of the
accepted delivery through `8b50f343`, new clarity construction or a live claim.
Scrum consumes the bounded tasks and original resource/owner contracts through
its existing loop. This architecture amendment itself is not execution progress.

Required repository approval and dependent Linux/package/publication stay
blocked. Existing original DevOps/Scrum coordination still needs exact common
package and unresolved-effect record locators; no new locator was obtained here.
Do not retry denied proof access, duplicate diagnostic investigation, infer
global exhaustion or resume unchanged DevOps from unrelated closeout work.
Both readiness exits, no engine-startup/uncertain-effect replay, actual live
acceptance and partial-sprint accounting remain unchanged.

## REPAIRED-JOIN-REMAINING-EXECUTION: original execution of the accepted repair

This current sprint consumes the agreed
[Architecture applicability](customer-prototype-architecture.md#current-repaired-join-traversal-source-acceptance-is-not-execution-acceptance-october-21-2026),
[remaining release plan](customer-prototype-repaired-join-remaining-release-plan.json)
and retained [sprint screens](customer-prototype-sprint-design.md). It supersedes
dated source-selection and continuation-routing statements below, not historical
outcomes, accepted construction or actual release criteria. Both supplied
priorDispositions arrays are empty; no accepted task is reopened.

At inspection, application HEAD was `1800e116c5ef352368959afa56f9069e9e225f36`
on `feature/customer-hosted-session-prototype` with a clean working tree.
Its ancestry after accepted integration `8b50f343` changes eight
documentation/index paths only. The selected repaired lab remains the accepted
`885801565ae11878a7c4f33c29f6b45b0eb19af7` handoff, not a fresh lab observation
in this turn. Use [the reviewed source join](design.md#reviewed-discovery-repair-source-join).
Original E2E must inventory its actual execution HEAD and account for this
documentation overlay; non-documentation drift needs original source review.

The canonical [solutionModel](customer-prototype-architecture.md#solutionmodel)
is incorporated unchanged: ten stable components, five triggered flows,
eighteen steps and their support links. The following table refines evidence
and operation dependencies, not implementation or public contracts.

| Canonical components / steps / criteria | Actual source and retained handoff | Missing verification and receiving owner |
| --- | --- | --- |
| Guarded lab release toolchain / `release-join`, `release-package` / AC7 | `Test-Demo.ps1`, accepted retained discovery bootstrap and seven fresh-process regressions, reviewed source join above. Repair/integration/ref-delivery acceptance is retained. | Original Developer EndToEndTestLoop runs permitted application/retained suites with pinned absolute Python and explicit roots, then original Architect/Critic/Product Owner review. No duplicate implementation tasks or assigned-work E2E substitute. |
| Guarded lab release toolchain; Trusted identity and private transport / `release-package`, `release-discriminate` / AC7, G1, G8 | Retained packaging/transport wrappers and [existing owner investigation contract](customer-prototype-post-delivery-exhaustion-architecture.json#existingOwnerInvestigationHandoff). | Original DevOps independently follows genuinely new permitted nonsecret common rollback ZIP-byte/provenance and next-operation effect locators. No E2E PASS or Linux-success dependency for that investigation. Return actual findings or an exact observed boundary, not mirror absence as global absence. |
| Hosted coordinator; Decision-1 routing and admission; MAF workflow checkpoints; Private Blob artifacts and effect journal / `collaboration-bind` through `collaboration-return` / AC1, AC5 | `demo/workflow.py`, `demo/foundry.py`, `demo/contracts.py`, `demo/artifacts.py`, `demo/routing.py`, `live_acceptance.py`; accepted fixtures and source contracts. | Actual trusted architect-before-reviewer ingress, genuine Decision-1/private Blob provenance, final common bundle and completed NON-HELD G1-G4 initial parent remain unverified. Source acceptance does not select a live identity path. |
| Hosted architect; Hosted reviewer; Parent and specialist conversation state / `continuity-revise/invoke/verify`, `recovery-stop/resume/verify`, `isolation-bind/execute/verify` / AC2-AC4 | `demo/architect_agent.py`, `demo/reviewer_agent.py`, `demo/specialist.py`, `demo/foundry.py`, `demo/artifact_store.py`, `tests/test_workflow.py`, `live_acceptance.py`; accepted continuation/revision/recovery/isolation fixtures remain offline. | Actual two-turn binding/pin comparisons, new responses and current requirements; once-only supported stop/resume with no duplicate effects; separate-parent scope evidence. Completed non-held initial parent gates follow-up and stop/resume. Isolation needs final bindings/comparison evidence, not recovery success. |
| Terminal client; Guarded lab release toolchain / `collaboration-return`, `release-close` / AC6, AC8, AC9 | `README.md`, `main.py`, `demo/terminal.py`, retained UX/screens and existing closeout ownership. | Existing closeout Developer refreshes measured customer status and delivers only reviewed intended ancestry. Actual demo, exact final/rollback bindings and attributable cleanup remain obligations; no duplicate clarity construction. |

### Source denial, independent lane and dependent execution

The recovered originating `scripts/Test-Repository.ps1` requests were denied
by interactive tool approval when no user response was available. This is an
unmet required AC7 check, not an executed test failure or diagnosed Azure
permission defect. No affirmative approval exists. Do not retry it, invoke an
alternate path or run constituent checks as substitutes. Affirmative approval
of that exact bounded interactive execution/tool prompt is the unblock condition.
No new architecture decision or broader permission is required here.

Scrum hands zero construction assignments directly to original E2E, followed
by original DevOps. An accurate reviewed predeployment FAIL can close E2E
reporting, never AC7 readiness. The fresh original traversal offers the normal
stage route; this document does not assert successful E2E/DevOps scheduling.
Historical continuation-validator limits below do not prohibit the current
normal route, nor authorize another unchanged resume or runtime/journal edit.

Within original DevOps, independent rollback/effect investigation stays useful
while required source readiness is blocked. Dependent changed-tool execution
waits for original E2E/reviews and all required source checks actually passing.
Then revalidate the SAME selected engine read-only, without replaying
Ensure-LinuxEngine startup or restarting Docker, and run BOTH complete corrected
actual Linux suites plus hosting/package gates. Actual package readiness AND
actual common rollback-byte/reconciled-effect readiness precede ONE serialized
guarded publisher. A bounded negative investigation report is not readiness.

Preserve existing Git/engine/stage/publication/context/transport/mount and parent
exclusive-resource contracts; Scrum names their actual assignment use without
creating whole-sprint dependencies or a second publisher/investigator. Settings
remain exclusively `scripts/Use-Settings.ps1`; no secret/private-state access,
canonical dirty-lab adoption, infrastructure/permission change, local specialist,
identity bypass or uncertain-effect replay. Account-wide Blob Contributor
still means application-enforced, not storage-RBAC or malicious-host isolation.

Opened current original agreement records `59abdb6c`, `89791f90` and `eefeb59d`
under delivery run `490ad8fa-3d48-4905-a216-d2159f43d446`: their original
reviewers agreed to Architecture, ReleasePlan and SprintDesign respectively.
Those votes justify bounded reuse, not this refinement's pending reviewer votes
or live success. This is documentation applicability only, no new execution
progress. No tests, repository-check constituents, settings, engine/cloud
operations, publication, inference, stop/resume or push were performed.
All three historical sprints and this remaining-execution sprint stay partial;
AC1-AC9/G1-G8, historical UNKNOWNs, held parents and rollback assets remain.

## RE-EXEC-1 continuation: accepted ref delivery, independent-work dispatch boundary

The [post-delivery assessment](customer-prototype-post-delivery-exhaustion-architecture.json)
consumes original delivery agreement `b8980bc5`. Previously verified remote refs
are application `8b50f343` and lab `88580156`; the ref-only queue below is historical,
not an unfinished assignment. No duplicate construction or resume is supplied.
Original changed-source E2E dispatch and repository-check execution remain
unresolved. Existing DevOps rollback/effect investigation is independently
authorized and incomplete, **not certified exhausted** by this bounded audit.
Scrum/orchestrator retains original-stage scheduling and originating rejection
record coordination. No new module/fixture gap or unused approved backlog slice
is evidenced. Retain partial delivery and every actual source/package/live gate;
this checkpoint is neither release success nor new execution progress.

Correction of `d964941d`, per exact disposition
`["yaml-loops-v1:sprint/1/RE-EXEC-1/continuation/4/SprintArchitectureLoop","RE-EXEC-1-EXHAUSTION-HANDOFF"]`:
the four work-exhaustion checks **do not establish exhaustion**. The existing
DevOps owner's common rollback-byte locator/effect questions remain useful
independent work; the mirror finding is not absence elsewhere. Original DevOps
invocations are completed in the visible registry, not messageable running/idle
owners. Installed continuation validation rejects new DevOps tasks and permits
only supplied blocked keys; the sole key addresses the entire unchanged DevOps
stage, not its investigation lane. The original-stage scheduler cannot separately
dispatch that lane from this packet. This is a precise internal **needs-replan**
boundary, not an empty continue queue, a claim of exhausted investigation or a
missing human permission.

Existing Scrum/orchestrator coordination must route the existing owner's bounded
nonsecret locator/effect investigation through original DevOps placement without
repeating mirror inspection or dependent operations. Require an inspectable
locator/effect finding or precise record/access boundary, not completed rollback
readiness, to close this bounded handoff. Do not create a duplicate investigator,
fabricate a resume key, relabel DevOps as construction or edit runtime/journals.
The amendment records the exact owner report, scheduling sources and four-check
assessment. Coordinator/specialist contracts and canonical model remain unchanged.

## RE-EXEC-1 continuation: accepted join, newly eligible ref closeout

The [exact-ref closeout amendment](customer-prototype-reviewed-ref-closeout-architecture.json)
consumes original integration agreement `cc7f2e82` for application `8b50f343`
and original parent-plan agreement `c0843a7e`. The repaired source join now
exists and is accepted; the missing-join statement in the historical section
below no longer describes current source. Do not repeat integration or repair.
Fresh application remote readback remains `55cf0216`. Queue only the existing
closeout Developer's now-review-eligible **ref-only** delivery of `8b50f343`,
with lab `88580156` readback, excluding this amendment and moving HEAD.
Actual delivery needs original review; no artificial ledger commit is required.

This changes only **Guarded lab release toolchain** / `release-close` /
AC8 and AC9 readiness. It does not resolve original changed-source E2E dispatch.
The current continuation cannot express that stage: do not invent a resume
key, repeat DevOps continuation or reopen accepted negative research. Scrum/
orchestrator retains the precise internal limitation and originating-owner
rejection-record recovery. Existing independent rollback/effect ownership,
both readiness exits, all E2E/Linux/package/live criteria and historical
uncertainty remain. The canonical model and runtime tiers are unchanged.
This bounded planning work earns no new execution-progress credit.

## RE-EXEC-1 continuation: consume accepted repair, retain original-stage limits

The [reviewed-join amendment](customer-prototype-reviewed-join-continuation-architecture.json)
consumes original repair agreement `4334061a` for lab `88580156` and the
accepted negative repository-check investigation `26415128`. Do not redispatch
either task. Original resumed DevOps audit `4e6d08bb` confirms that the current
continuation retains/skips agreed E2E `0a08120c`, which covers lab `651a2290`,
not the repair. No supported dispatch correction has been established here.
Do not invent an E2E resume key, substitute assigned-work E2E, modify runtime
or journals, or repeat an unchanged DevOps resume.

The last source-join record in `docs/design.md` still binds lab `651a2290`.
Scrum can queue the **existing integration/final-closeout Developer's**
unfinished repaired-join and reviewed Git-delivery slice, once, using its
existing Git resources. This is useful approved `release-join`/`release-close`
work, not new construction or a scheduler repair. Deliver only exact
already-reviewed ancestry; new documentation and this amendment need their
own original reviews before push. The amendment supplies the bounded card.
No new owner or whole-sprint barrier is introduced.

Original changed-source Developer E2E and Architect/Critic/Product Owner
reviews remain mandatory before dependent changed-tool DevOps. The denied
repository suite remains unmet; originating-owner rejection-record recovery
is coordination, not a repeat of accepted negative research. Existing DevOps
rollback-byte/effect investigation remains independent. BOTH readiness exits,
all actual Linux/package and cloud gates, historical unknowns and no-startup
replay remain binding. This continuation is not exhausted: the retained
integration slice is ready. It creates no execution-progress credit.

## RE-EXEC-1 continuation: retained discovery ownership

The separate [discovery continuation amendment](customer-prototype-discovery-continuation-architecture.json)
localizes the newly observed original E2E failure at application `66224a3d` /
selected feature lab `651a2290`. Opened original E2E audit `0a08120c` and
DevOps audit `78728c47` with their original review decisions. E2E agreement
accepts an actionable FAIL; DevOps remains incomplete. The retained runner
does not bind application modules before discovery, while the Windows identity
trace test prepends lab tools. This affects **Guarded lab release toolchain** /
`release-join`, `release-package` / AC7, not hosted identity or the accepted
cold-import fixture correction.

This overlay supersedes only the earlier zero-new-construction statement:
there is now one bounded Developer entrypoint repair/regression and a separate
read-only investigation of the exact repository-check denial/changed condition.
The amendment supplies their source criteria, ownership, doneWhen, exclusions
and original-review handoffs for Scrum's queue. The two tasks are independent.
Missing `scripts/Test-Repository.ps1` execution remains unmet, not a waiver,
new user-permission request or license to retry/bypass the denial.

Consume the four exact originating dispositions under
`["yaml-loops-v1:sprint/1/RE-EXEC-1/DevOpsWorkLoop", ...]`:
`RE-EXEC-1-DISCOVERY-OWNERSHIP`, `RE-EXEC-1-REPOSITORY-CHECK`,
`RE-EXEC-1-RELEASE-READINESS`, `RE-EXEC-1-REVIEWED-GIT-DELIVERY`.
Do not reopen accepted fixture source or UX accounting. The canonical
solutionModel, coordinator/specialist tiers, five flows and eighteen step IDs
are unchanged.

New reviewed source returns through existing integration ownership to actual
original changed-join E2E and Architect/Critic/Product Owner reviews before
dependent DevOps. Historical agreed FAIL is not a cached passing prerequisite.
If original changed-source E2E cannot dispatch, report the precise internal
scheduling limitation; do not replace that stage or loop unchanged continuations.
Existing rollback ZIP-byte/effect investigation and reviewed Git delivery remain
independent under their existing owners. BOTH actual readiness exits still
precede one serialized guarded publisher. Preserve all live gates, historical
plans, UNKNOWNs, held parents and the no-startup-replay restriction. This
architecture amendment is not execution progress or release acceptance.

## RE-EXEC-1: accepted corrected join, original integration gate first

This sprint consumes the accepted [holistic recovery architecture](customer-prototype-architecture.md#current-recovery-traversal-validate-the-accepted-corrected-join-first-october-21-2026),
[remaining-execution ReleasePlan](customer-prototype-remaining-execution-release-plan.json)
and [SprintDesign](customer-prototype-ux.md#current-recovery-traversal-source-acceptance-is-not-execution-october-21-2026).
Their current original outcome audits `7d8e8f2a`, `909cb570` and `05ea4d14`
under delivery run `563841c9-c44a-4a83-87e5-63600eaaea58` were opened:
all original reviewers recorded agreement, task complete and no unmet bounded
criteria. Those votes accept their documents, not execution or live capability.

Selected application baseline is `7322ed7a06954e8006843cb466ba76bc6bf16146`,
selected feature lab is `651a22908984174d3947b9d04ed68f6cd13ea90c`, and accepted
integration is `28636214a870a3a635222015fa67527ddba320fc`.
Observed application HEAD before this documentation change is
`a9cecf1076c6861220b955a37ff668ae42f94d85` on
`feature/customer-hosted-session-prototype`, clean. Its subsequent integration
ancestry changes documentation/index only. Include this sprint/tier refinement
in exact-source and later reviewed delivery accounting; do not silently replace
the selected lab with canonical dirty source.

The canonical [solutionModel](customer-prototype-architecture.md#solutionmodel)
is incorporated unchanged: ten components, five flows, eighteen steps and shared
support links. The three [tier contracts](requirements/client-release/architecture.md)
retain their implementation boundaries. This opening supersedes only stale
pending-construction and continuation-resume routing in dated sections below.
No accepted source task, settled review/retro or historical capped invocation
is restarted. There are **zero new construction assignments**.

| Canonical scope / criteria | Actual source and consumed handoff | Missing evidence and smallest original-owner exit |
| --- | --- | --- |
| Guarded lab release toolchain / `release-join`, `release-package` / AC7 | `Test-Demo.ps1`, `scripts/Test-Repository.ps1`, [reviewed fixture join](design.md#reviewed-cold-import-fixture-source-join); lab `Build-Demo.ps1`, `tests/test_release_identity_decision.py` | Original Developer **EndToEndTestLoop** validates actual loaded roots, committed inputs and exact corrected join with pinned absolute Python/local scripts. Original Architect/Critic/Product Owner reviews precede changed-tool DevOps. Preserve the prior exact test denial; missing required checks remain unmet, with no unchanged retry or bypass. |
| Toolchain and Trusted identity and private transport / `release-package` / AC7, G1, G8 | Accepted mounts/helper/selectors and separate cold-import test provenance; retained release/connectivity tooling | Original DevOps revalidates the SAME selected engine read-only, then BOTH complete corrected actual Linux suites and hosting/package gates. Independently, existing inventory ownership investigates actual common rollback ZIP bytes and next-operation effects. BOTH readiness exits precede one serialized publisher; metadata alone is insufficient. |
| Hosted coordinator, Hosted architect, Hosted reviewer; conversation state, checkpoints, artifacts and Decision-1 / collaboration / AC1, AC5 | `demo/workflow.py`, `demo/foundry.py`, `demo/specialist.py`, `demo/contracts.py`, `demo/artifacts.py`, `demo/routing.py`, `live_acceptance.py`; accepted runtime/fixtures | Original DevOps proves trusted architect ingress before reviewer, final common bundle and actual G1-G4 with a completed non-held initial parent. Neither identity-remediation path is established live. |
| Same hosted roles and shared state; Terminal client / continuity, recovery, isolation / AC2-AC6 | `demo/terminal.py`, `demo/architect_agent.py`, `demo/reviewer_agent.py`, `demo/artifact_store.py`, the modules above and accepted UX | That completed parent unlocks queue follow-up and once-only supported stop/resume. Final deployed bindings unlock separate-parent isolation independently of recovery success. Compare actual bindings/pins, new responses, histories, exact artifacts and effects; aliases or recalled text are not proof. |
| Terminal client and toolchain / `release-close` / AC6, AC8, AC9 | `README.md`, `docs/customer-prototype-ux.md`, `docs/identity-recovery-plan.md`; existing integration/final-closeout ownership | Reviewed Git delivery can proceed independently of live success, without concurrent unreviewed ancestry. Final sanitized demo, exact final/rollback bindings, per-criterion ledger and attributable owned cleanup still require real evidence. |

Scrum Master's bounded SprintPlan therefore has empty new task/assignment
arrays and hands directly to the original E2E stage, not an assigned-work E2E
substitute. Formal E2E may accurately report predeployment FAIL; that is not
passing missing source prerequisites or release acceptance. Original DevOps
remains the later deployment/cloud-pass stage. Keep minimal dependencies and
existing exclusive resources for engine/stage, publisher/context/transport/mount,
primary-parent mutations and Git reconciliation; no full-sprint dependency is
introduced and scheduler names provide no cross-run isolation.

Opened original fixture/integration source audits `bb19091a` and `81d6d269`
from predecessor run `0159ec9f-a89c-47f9-986f-80d9dfe6740a`.
Apply exact reference
`["yaml-loops-v1:sprint/3/RP-S3/DevOpsWorkLoop","retained-live-preparation-fixture-initialization"]`
only to its accepted source boundary, retaining missing actual execution.
Current original UX audit `883721e3` accepts the reconciliation for
`["yaml-loops-v1:UserExperienceLoop","UX-DELIVERY-RUN-ACCOUNTING"]`;
do not reopen that bounded handoff or replace its historical run association.
The current packet has no additional prior dispositions or reconciled rework.

Never replay the once-attempted engine startup, uncertain publications or held
parents. Preserve UNKNOWNs, rollback assets and historical cleanup uncertainty.
No infrastructure/permission change, settings import, runtime change or new
scope is introduced. Blob isolation remains application-enforced under
account-wide Contributor, not storage-RBAC or malicious-host isolation.
Historical RP-S1/RP-S2/RP-S3 remain partial; AC1-AC9/G1-G8 remain required.
This documentation alignment is not new construction or execution progress.

## Work-conserving continuation: cold-import fixture boundary

This continuation amendment consumes application `7fef48b7` and registered
feature lab `1526012`. Original RP-S1/RP-S2/RP-S3 DevOps boundaries remain
partial. The latest authoritative execution is audit `0413fdfc` under current-run
`gh-dynamic-workflows/.delivery-runs/0159ec9f-a89c-47f9-986f-80d9dfe6740a/context`;
its reconciled governance, not individual reviewer suggestions, drives this
amendment. Opened accepted architecture `e568cf6a`, plan `3009f694` and exact-join
E2E `2f339393`, plus earlier blocked audits `d29bb042` and `7e74a2ea`.
Their bounded agreements are not deployment acceptance.

The separate [continuation architecture and task contract](customer-prototype-fixture-continuation-architecture.json)
preserves the original plans and ReleasePlan unchanged. Its solutionModel
incorporates the canonical ten components, five flows and eighteen steps
[by reference](customer-prototype-architecture.md#solutionmodel); no new runtime,
service, model, operation, permission or acceptance gate is introduced.

### Verified failure, source boundary and missing construction

Independently hashed the approved mirrored `linux-final-7fef48b7-1526012.log`
(`af9c4422b6f970d84b42ab87fb83e4f5c6396ea11d2c6f9a26fddf90a8fcaeb0`)
and `linux-inspection-7fef48b7-1526012.json`
(`083556f41e382fa4b436635701f4f0560627fc8eefff04b9395ee480c1b4933e`).
The log records 206 application tests (199 passed, seven skips) and 224 retained
tests (178 passed, 43 platform skips, three configuration errors). All seven
native-observation cases now execute. Inspected sibling source:
`LivePreparationTests.check_rejection` imports `demo.contracts` at line 360
before establishing synthetic configuration; `demo/config.py` validates the
project at import. All three errors terminate at missing
`FOUNDRY_PROJECT_ENDPOINT`, before the intended rejection assertions.

Apply exactly
`["yaml-loops-v1:sprint/3/RP-S3/DevOpsWorkLoop","retained-live-preparation-fixture-initialization"]`.
The existing Developer owns only lab
`foundry-tf/multi-agent/tests/test_release_identity_decision.py` and necessary
lab index updates for the correction. Establish fixture-owned synthetic
configuration before configuration-dependent imports; register reliable
restoration including setup/error paths. Add fresh-process coverage that removes
ambient operational configuration and starts without warmed application imports,
executes all three rejection cases and verifies the expected guards were reached.
Preserve UNKNOWN's no-inventory assertion, version/identity drift rejection and
no-parent-creation behavior, alongside strict runtime configuration validation.
Do not weaken assertions to accept a configuration exception as the desired
rejection. Use the existing validated dependencies, pinned absolute Python,
explicit roots and mocks; no credentials or real service calls.

This is a **Guarded lab release toolchain** test-only correction at
`release-package` (AC7), not an identity/runtime failure or a mount redesign.
Accepted mount/provenance/native-observation work under
`["yaml-loops-v1:sprint/2/RP-S2/DevOpsWorkLoop","retained-linux-test-input-closure"]`
remains consumed. No edits to Build-Demo, runtime, helper, context, selector,
application fixtures or package allowlists are needed by the new source task.
The existing integration Developer then verifies actual loaded owners and
committed bytes, records changed test-only provenance separately from the
unchanged runtime/Decision closure, delivers reviewed refs and refreshes only
stale measured documentation. Original reviews and changed-join E2E precede
changed-tool execution. Source-task completion does not require deployment.

### Blast radius, independent work and exact resume

| Scope / criterion | What can proceed | What remains blocked and receiving owner |
| --- | --- | --- |
| Toolchain / `release-join`, `release-package` / AC7 | Two bounded source/integration tasks in the separate amendment, then original E2E | Original DevOps reruns BOTH actual complete Linux suites and hosting/package gates for the new exact join; no startup replay or fixture PASS substitution. |
| Toolchain and **Trusted identity and private transport** / `release-package` / AC9, G1/G8 | Existing DevOps continues provenance-backed common rollback ZIP locator/byte hashing and next-operation effect accounting independently of fixture repair | Neither of the two located ZIPs matches the expected common rollback hash per `0413fdfc`; those byte/journal findings remain owner-attributed here. No exhaustive private-tree search, reseal, regeneration or inferred availability. |
| Three hosted roles, Decision-1, artifacts / `release-discriminate`, collaboration steps / AC1, AC5 | Existing reviewed scripts/fixtures are usable contracts, not new construction | BOTH real readiness exits gate one original serialized publisher, architect-before-reviewer ingress, final common bundle, genuine G1-G4 and completed non-held initial parent. |
| Conversation state, checkpoints, terminal, artifacts / continuity/recovery/isolation / AC2-AC6 | Accepted implementation and offline fixtures remain available; no duplicate preparation task | Continuity/recovery need that completed parent; isolation needs final bindings/safe effects but not recovery success. No full-sprint dependency is introduced. |
| Terminal and toolchain / `release-close` / AC8-AC9 | Existing integration/closeout can push/read back already reviewed documentation and refresh measured status on new evidence | Final live ledger, final/rollback bindings and attributable cleanup still need real execution; preserve UNKNOWNs, held parents, rollback assets and historical cleanup uncertainty. |

Resume only `sprint/3/RP-S3/DevOpsWorkLoop` after the two new source/join
handoffs and original E2E. It is the current execution frontier, not a new
publisher. Earlier partial DevOps outcomes remain in review/retro reconciliation;
do not launch three deployments to revisit historical failures. Independent
rollback/effect work has no fixture dependency and can continue through that
existing owner before the resume gate. No user-only blocker is established.

Accessible inspection evidence now supports the separately labelled inspected
image ID, exported manifest and config digests. This addresses the evidence
gap under
`["yaml-loops-v1:sprint/1/RP-S1/DevOpsWorkLoop","release-binding-report-accuracy"]`,
not the failed package gate or historical startup timeout. Preserve that timeout
separately from later same-selection readiness; never replay startup.
The original
`["yaml-loops-v1:sprint/1/RP-S1/DevOpsWorkLoop","guarded-execution-and-closeout"]`
and selected-WSL exact-inventory boundaries remain binding. Four accepted exact
metadata reads are not common rollback bytes, trusted ingress or live memory.
All AC1-AC9/G1-G8 remain required; the original five-round accounting is unchanged.

## Current RP-S3: live evidence joins and retained Linux input closure (October 20, 2026)

This is the current cumulative overlay for **RP-S3**; earlier entries retain
their originating evidence and task boundaries, not current pending ownership.
Baseline is application `a066bdf8908f6873d0e0ae12a82e348a586f9a82` on
`feature/customer-hosted-session-prototype`, with reviewed source join
application `98128bb8` / selected feature lab `5da7a2ea`. Consume accepted
Architecture `cef352f4`, UX `6b6975c0`, ReleasePlan `48e3faf3` and current
SprintDesign `a066bdf8`. Opened original current-run audits `398b66fa`,
`5a82b2df`, `40c04f03`, `c803c95d` and `293c1688`: their original reviewers
accept the bounded architecture, plan, design, source join and local E2E
report. None establishes deployed acceptance. Opened stopped DevOps audit
`7e74a2ea`, including its single reconciled governance instruction set:
Architect, Critic and Developer each retain taskComplete false and four
unmet criteria. RP-S1 and RP-S2 remain partial at original DevOps boundaries.

### Canonical model, implemented state and smallest live joins

The authoritative [solutionModel](customer-prototype-architecture.md#solutionmodel)
is incorporated unchanged: ten components, five flows, eighteen steps and
the existing shared support links. This overlay adds neither component nor
flow, session manager, service, CLI/schema nor alternative execution path.
The following connects current approved criteria to its actual implementations.

| Criteria / canonical flow steps | Components and existing modules | State and smallest receiving contract |
| --- | --- | --- |
| AC7 / `release-join`, `release-package` | **Guarded lab release toolchain**; lab `Build-Demo.ps1`, `tests/test_release_identity_decision.py`, `tests/test_release_native_settings.py`; application `tests/test_workflow.py` | Reviewed application input/fixture correction is implemented and locally accepted. Actual application container run: 206 tests, 199 passed, seven platform/optional skips. Separate retained discovery: 184 run, 145 passed, 38 Windows-specific skips, one import error. New retained-input correction below needs source review, changed-join E2E and complete actual Linux execution; no package readiness yet. |
| AC9/G1/G8 / `release-package` | **Trusted identity and private transport**, toolchain; lab `Invoke-WslCodeRelease.ps1`, `wsl_release.py`, `observe_agent.py` | Exact selector implementation and join are accepted. Original DevOps/review records four accessible exact private version/package/identity matches and attributable new-resource closure. Complete common rollback ZIP-byte availability and effect ledger remain unproven; metadata is not rollback-byte proof. Independent accounting does not wait for Linux repair. |
| AC1/AC5 G1-G4 / `release-discriminate`, `collaboration-bind`, `collaboration-route`, `collaboration-design`, `collaboration-review`, `collaboration-return` | **Hosted coordinator**, **Hosted architect**, **Hosted reviewer**, **Decision-1 routing and admission**, shared state/artifacts/checkpoints; `demo/workflow.py`, `demo/specialist.py`, `demo/foundry.py`, `demo/routing.py`, `live_acceptance.py` | Implemented/local evidence is consumed, not redispatched. BOTH actual readiness exits still precede one publisher, trusted architect-before-reviewer ingress and actual common-bundle G1-G4. The completed non-held initial-parent handoff is missing, not implied by accepted E2E FAIL or exact metadata. |
| AC2/G5 / `continuity-revise`, `continuity-invoke`, `continuity-verify` | **Terminal client**, hosted roles, **Parent and specialist conversation state**, **Private Blob artifacts and effect journal**; `demo/terminal.py`, `demo/contracts.py`, `demo/foundry.py`, `demo/workflow.py`, `demo/specialist.py`, `live_acceptance.py` | Accepted fixture/history/presentation work remains implemented and locally verified. Live execution needs the actual completed initial parent and final common-bundle bindings, not acceptance of an entire earlier sprint. Compare observations and assertions independently as specified below. |
| AC4/G6 / `recovery-stop`, `recovery-resume`, `recovery-verify` | Toolchain, trusted transport, hosted roles, conversation state, **MAF workflow checkpoints**, artifacts/effects; `live_acceptance.py:stop_hosting_for_acceptance`, `demo/workflow.py` | Supported once-only stop requires completed non-held parent, durable intent and exact stopped/idle confirmation. No current live stop/resume evidence; uncertainty holds affected operations. |
| AC4/G7 / `isolation-bind`, `isolation-execute`, `isolation-verify` | Terminal, hosted roles, conversation state, artifact plane, trusted transport; `live_acceptance.py`, `demo/artifacts.py`, `demo/artifact_store.py`, `demo/foundry.py` | Accepted cross-scope fixtures remain. Live separate parent needs final deployed bindings and safe effects, not recovery success; its preparation is independent of the missing initial-parent continuation. |
| AC6-AC9/G8 / `release-close` | Terminal, toolchain, artifact plane; `README.md`, `demo/terminal.py`, `live_acceptance.py`, `docs/identity-recovery-plan.md` | Retain screens H-K, machine stdout/parser and opt-in human stderr. Existing integration/closeout joins actual proof, final-source/package checks, reviewed scoped pushes and new-resource cleanup; no customer-ready claim before all required criteria. |

The specialist model-history stages live in `demo/architect_agent.py` and
`demo/reviewer_agent.py`; `demo/specialist.py` is shared instructions/resource
lifecycle, while `demo/foundry.py:RemoteAgents.invoke` restores the coordinator's
per-child framework session. These are distinct continuation boundaries.

### Retained Linux correction: public test inputs, not a runtime repair

Apply the exact required reference
`["yaml-loops-v1:sprint/2/RP-S2/DevOpsWorkLoop","retained-linux-test-input-closure"]`.
Direct source inspection at selected lab `5da7a2ea` confirms:
`test_release_identity_decision.py` imports `identity_decision` at discovery,
but `Build-Demo.ps1` omits it from the explicit `/lab-tools` mounts.
The same test module's `NativeObservationTests` dynamically loads application
`tests/test_workflow.py`; the separate retained container invocation does not
supply that fixture and can skip the coverage when absent. Fix both public
input omissions in one bounded correction, not only the first import error.

Existing Scrum scopes the existing Developer precisely to lab
`foundry-tf/multi-agent/Build-Demo.ps1`,
`foundry-tf/multi-agent/tests/test_release_native_settings.py`,
`foundry-tf/multi-agent/tests/test_release_identity_decision.py` where needed
for missing-input coverage, and lab `.github/repo-index.md`. The fixture,
`identity_decision.py`, its existing dependencies, application Dockerfile,
runtime/ZIP allowlists and configuration are read-only inputs. There is no
application runtime or fixture behavior change authorized by this repair.
Shared index freshness belongs to the designated writer/integration handoff,
not competing source writers.

Supply `identity_decision.py` and the required workflow fixture through named
read-only mounts in the separate retained invocation. Trace their actual
import/inspection dependencies against the existing image and named mounts;
add only demonstrated required public inputs. Preserve explicit application/
reviewed-tool roots, loaded-source ownership, file-presence/reparse rejection,
exact mount equality, duplicate rejection, compilation, `--network none`,
runtime/package exclusions and separate application/retained suites.
Bind added test-only/helper bytes and their source owners separately from
runtime/Decision closure; an unchanged runtime hash cannot seal new inputs.
Do not mount a whole checkout, all scripts or private settings, alter discovery
to hide errors, or replace required native-observation coverage with fixture-
absence skips. Existing original-layout/platform exclusions must remain
attributed, not silently removed or counted as executed coverage.

Bounded source doneWhen is committed input/provenance correction with passing
affected exact-mount and retained-observation regressions plus applicable
offline checks, exact source/input hashes and original Architect/Critic
handoff. No engine startup, Linux build, authentication, transport or cloud
effect is part of that source assignment. Existing integration verifies actual
loaded roots/committed bytes, refreshes caller/index handoffs, accounts for
reviewed refs and returns the exact changed join to original E2E before original
DevOps reruns BOTH full Linux suites. Do not reuse the failed retained run or
application-only success as complete package evidence.

### RP-S3 observations, effect discipline and release closure

RP-S3 consumes a completed non-held initial parent with actual G1-G4 and exact
final common-bundle/three-role version, identity and parent/both-child bindings.
Retain the same private terminal session file for the queue follow-up. AC2
compares stable parent and both hosted/framework child identities and pins,
exactly two child creations across initial/follow-up, fresh response IDs per
new invocation, both roles on both turns, earlier private-ingress requirements
plus queue, current immutable prerequisites/hashes/revisions and invalidated
stale approval. Restored specialist model history is distinct from replayed
brief text; known-response retrieval is distinct from a new invocation.
Do not require complete serialized sessions to remain constant as continuation
advances. Offline controlled reject/revise/review remains AC3 evidence, not live.

For G6 retain `live_acceptance.py`'s durable `.hosting-restart.json` intent,
one supported stop, independent exact stopped/idle confirmation and original
bindings/checkpoints/effect reconciliation on continuation. A pending stop is
observed, never resent; missing confirmation is unresolved. Demonstrate actual
no-duplicate send/create effects, not only similar output. G7 separately compares
distinct actual parent/both-child identities and artifact namespaces, excludes
the first parent's requirements and retains cross-scope rejection. It has no
dependency on G6 success. Neither operation evades held state by inventing a
replacement parent. Account-wide Blob Contributor provides application-enforced
parent/role isolation, not storage-RBAC or malicious-host isolation.

Existing DevOps independently locates/hashes authorized retained common rollback
ZIP bytes against preexisting expectations and completes unresolved-effect
accounting. Four exact private observations do not replace those bytes or clear
historical UNKNOWNs. Revalidate source/operational freshness before later effects.
Both actual package and rollback/effect readiness exits gate the one original
serialized publisher. Publication, trusted architect then reviewer ingress,
final common bundle and completed initial parent remain unperformed.

Apply the original report-accuracy reference
`["yaml-loops-v1:sprint/1/RP-S1/DevOpsWorkLoop","release-binding-report-accuracy"]`
without flattening evidence provenance: the newer DevOps owner reports a
separate inspected image ID; original reconciled feedback keeps that ID
owner-attributed until accessible inspection evidence supports it. The mirrored
build log supports exported manifest/config digests, not that separate inspect
output. Their claimed equality does not retroactively validate the historical
mislabel. Preserve startup timeout separately from subsequent same-selection
readiness; no helper success or startup replay is inferred.

The other originating required references at
`yaml-loops-v1:sprint/1/RP-S1/DevOpsWorkLoop` remain bounded:
`linux-application-test-closure` is consumed as corrected source plus this
tested join's actual application success, not redispatched;
`selected-wsl-exact-inventory` is consumed as accepted source and inspected
exact-read receipts, not complete rollback readiness;
`guarded-execution-and-closeout` retains both exits, original E2E/DevOps
placement, scoped Git push/readback and actual cloud-test completion.
The accepted helper/mount reference
`["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-LINUX-ENGINE-READINESS/AssignedWorkDeveloperLoop","linux-engine-exact-mount-contract"]`
is closed in its source boundary; do not reopen helper/context/ownership work.
No disposition is superseded and no new user-only blocker is established.

Scrum's next plan may split retained-input source/integration from independent
rollback-byte/effect accounting and RP-S3 local evidence preparation. Do not
redispatch accepted fixtures or invent construction simply to fill capacity.
Use only necessary contract dependencies; no whole-sprint gate is added.
Serialize actual publisher/transport/profile/mount mutation with original
exclusive resources, and shared docs/index/Git reconciliation by designated
ownership. Existing closeout owns reviewed application `98128bb8` / lab
`5da7a2ea` and subsequent intended feature-ref push/readback, measured status
and durable task/commit/branch accounting. Preserve rollback assets, held
parents, historical UNKNOWNs/cleanup uncertainty and unrelated staged/dirty work.
Original five-consecutive-no-new-progress accounting is unchanged.

This Architect turn changes documentation contracts only. Document checks
cannot establish Linux/package readiness, private operational freshness, hosted
continuity/recovery/isolation or customer AC1-AC9. Original reviewers assess this
bounded deliverable; original sprint review/retro retains incomplete live gates.

## Current RP-S2: Linux test closure and selected-WSL exact inventory (October 20, 2026)

This entry governs the current correction; earlier entries retain their original
task/evidence boundaries. Inputs are accepted Architecture `cef352f4`, UX
`6b6975c0`, ReleasePlan `48e3faf3`, current SprintDesign `b29d9a0b` and
source join application `0cac08c9` / lab `1dab1e01`. Opened current-run audits
`398b66fa`, `bf7fed70`, `5a82b2df`, `c8ea93a8`, `c96ccaae`, `9932d390`,
`bc59f888` and `6024e98b`: original votes accept their bounded documents/source/
local checks, not cloud readiness. Opened stopped DevOps audit `d29bb042`
including its reconciled governance instructions: needs-replan, original
Architect/Critic/Developer taskComplete false. RP-S1 remains partial at that
execution boundary; RP-S2 remains incomplete and RP-S3 live verification pending.

### Stable model and localized construction

The authoritative [solutionModel](customer-prototype-architecture.md#solutionmodel)
remains unchanged: ten components, five flows, eighteen steps, including all
support links. This cumulative sprint artifact incorporates that model by
reference rather than forking it. The following are implementation-contract
refinements within **Guarded lab release toolchain** (`release-toolchain`) and
shared **Trusted identity and private transport** (`identity-boundary`), not new
services or a runtime architecture rewrite.

| Approved criterion / step | Actual modules and state | Missing construction / receiving handoff |
| --- | --- | --- |
| AC7, RP-S2 Linux validation / `release-package` | Lab `Build-Demo.ps1` mounts `scripts/diagnose_identity.py`, but not the `scripts/identity_handoff.py` imported by application discovery. Dockerfile correctly excludes that offline-only utility from hosting. Application `tests/test_scenario_evidence.py` mocks DecisionClient without owning required admission configuration. | Developer supplies explicit public read-only test inputs and isolated synthetic Decision settings; original source review and changed-join E2E precede complete DevOps Linux application AND retained suites. |
| AC9, G1/G8, RP-S2 fresh inventory / `release-package` | Lab `wsl_release.py:Release.observe` reads latest metadata. `observe_agent.py` already implements strict exact selectors, exact GET, package/identity comparison and sanitized absence results. Selected WSL has no caller contract for these exact reads. | Separate Developer correction exposes the existing exact-read validation through retained WSL transport. DevOps joins exact rollback availability with local package hashes and unresolved-effect accounting. Metadata alone cannot establish the full exit. |
| AC8 / `release-join`, `release-close` | Accepted helper/mount `1dab1e01`, integration `0cac08c9` and original exact-join E2E remain consumed. Runtime/Decision closure is separate from build/test/helper inputs. | Existing integration owner reconciles new reviewed commits, actual loaded roots/bytes, changed input hashes and push/readback, including `0cac08c9`; existing closeout refreshes only measured status. |
| AC1/AC5 G1-G4 / `release-discriminate`, all five `collaboration-*` steps | Hosted workflow, immutable artifacts, fencing, checkpoints, child bindings and finite identity runner are implemented and locally verified, not independently live-proven by this turn. | BOTH actual readiness exits precede one serialized publisher, trusted architect ingress before reviewer, common-bundle G1-G4 and completed non-held initial parent. |
| AC2-AC4 / `continuity-*`, `recovery-*`, `isolation-*` | Accepted RP-S1 binding/history/revision fixtures and terminal projection remain unchanged. | RP-S3 consumes actual final bindings; follow-up needs a completed non-held initial turn, supported stop/resume its once-only marker, isolation its own scope. Independent approved source/preparation need not wait for another full sprint. |

### Package branch: explicit test inputs, not hosted dependencies

Existing Scrum assigns the existing Developer application
`tests/test_scenario_evidence.py`, lab `foundry-tf/multi-agent/Build-Demo.ps1`,
`foundry-tf/multi-agent/tests/test_release_native_settings.py` and the two
repository indexes. These are the precise source ownership boundaries for this
correction. `scripts/identity_handoff.py`, `scripts/diagnose_identity.py`,
`demo/workflow.py`, Dockerfile and runtime/package allowlists are read-only
inputs, not permission to change behavior or broaden the shipped package.

Build-Demo supplies the demonstrated missing `scripts/identity_handoff.py` as
an explicit read-only application-test mount, using selected ApplicationRoot,
file-presence/reparse guards and test-input provenance hashing consistent with
the diagnostic input. Keep its existing diagnostic dependency available;
do not mount all scripts, a checkout, private settings or operational profiles.
Update affected exact input/mount/provenance regressions without weakening
exact equality, duplicate/file-presence, network-none, runtime exclusion,
compilation or separate application/retained-container assertions.
New test-only bytes must be bound separately even if the runtime seal is unchanged.

Scenario captures own synthetic `DECISION_REQUESTS_PER_MINUTE` and
`DECISION_MODEL_DEPLOYMENT` before calibration/graph capture, across initial,
follow-up, restart and isolated scenarios. Restore prior values AND prior
absence on success and setup failure, with cleanup registered before captures.
Use existing synthetic fixture conventions, not ambient lab configuration.
Cover environment-independent execution/restoration, retaining all current
artifact/journal and negative scenario assertions. Runtime's required settings,
admission limits and genuine live Decision-1 checks remain mandatory.

Bounded source doneWhen: committed explicit input/fixture correction and passing
affected application/retained/provenance checks returned to original
Architect/Critic review. This is not actual Linux readiness. Exclusions include
engine startup/build/cloud execution, identity-handoff/runtime behavior changes,
dependency installation without a missing-tool/manifest cause, settings edits,
package expansion and skips used to hide failed required checks.

### Inventory branch: a read-only exact selector on the existing route

Independent source ownership is lab
`foundry-tf/multi-agent/Invoke-WslCodeRelease.ps1`,
`foundry-tf/multi-agent/wsl_release.py`,
`foundry-tf/multi-agent/tests/test_release_exact_metadata.py`,
`foundry-tf/multi-agent/tests/test_release.py` and lab `.github/repo-index.md`.
Reuse `observe_agent.py` unchanged as the validation/observation contract;
do not duplicate its package/identity rules or modify publishing semantics.

Expose an all-or-none selector quartet on the existing wrapper:
`InventoryService`, `InventoryVersion`, `InventoryExpectedPackageSha256`,
`InventoryIdentityBaseline`, propagated as explicit corresponding Python
`--inventory-*` arguments. It is valid only in ReadOnly, never Publish,
InspectOwner or combined session monitoring. Absent selectors retain current
latest-only ReadOnly behavior. Exact service is one of the existing three;
version uses `exact_version`, hash uses `package_hash`, and baseline is an
existing validated private non-reparse file outside source repositories,
bound to that role's identity baseline. Validate selectors/combination/path
before starting owned transport or performing external work. Preserve the
separate application/tool/operational roots and loaded-source equality.

Within the already selected retained WSL route, perform only the exact version
GET and existing exact metadata validation, using the existing scoped credential,
strict host trust, remote-DNS/private-origin transport, bounded command handling,
read-only mount and owner containment/cleanup. Do not create another route,
switch profiles/contexts, read/copy credentials, infer expected identity from the
new observation, or fall back to latest/list/public access on a failed exact read.
Preserve existing `observe_exact`/`exact_metadata` sanitized fields: requested
and returned version, existence/status, expected-package match, identity match,
protocol presence and zero inference. An exact 404 is observed absence, never
availability; hash/identity mismatches or incomplete observations cannot satisfy
rollback readiness. Fail closed on invalid selector, malformed result,
authentication/transport/error/cleanup uncertainty; never emit success-shaped
readiness from a partial receipt. Private identity values and response bodies
stay outside public output/Git. Return accessible sanitized receipt evidence
through the approved mirror/handoff; access denials remain denials.

Bounded source doneWhen: committed wrapper/runner/regressions pass targeted and
applicable retained checks for valid exact reads, incomplete/invalid selectors,
wrong modes/roots, missing/unsafe baseline, absent versions, package/identity
mismatch, HTTP/transport failure, no fallback/inference and attributable cleanup.
Original Architect/Critic review and applicable changed-join E2E precede
execution of changed tooling. No live inventory or publication is required or
claimed by that source assignment. Existing DevOps continues feasible retained
rollback-package/effect-journal accounting independently; inventory construction
does not depend on the package branch or unused Windows-helper acceptance.

### Disposition application, execution and reporting

Apply exact origin `["yaml-loops-v1:sprint/1/RP-S1/DevOpsWorkLoop", ...]` for
`linux-application-test-closure`, `selected-wsl-exact-inventory`,
`release-binding-report-accuracy` and `guarded-execution-and-closeout`.
The different originating
`["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-LINUX-ENGINE-READINESS/AssignedWorkDeveloperLoop","linux-engine-exact-mount-contract"]`
is satisfied by original accepted helper/mount source; do not reopen it.

The opened DevOps report attributes a once-only startup command timeout followed
by later same-selection read-only readiness, not helper success. Do not replay
that startup. Image construction reached Linux/amd64/Python 3.13.15; application
discovery then had 191 tests, 14 errors and seven skips; separate retained Linux
checks were not reached. Exported manifest digest
`b0c7ebf170ae375553947a339ad894a134f8ca794b0c34b66705f6a4cad9d8c6`
is NOT an authoritative image ID; leave image ID unverified pending inspection.
These are attributed execution findings, not new Architect executions.
The fresh private route/cleanup receipt was unavailable to original reviewers;
its claims remain owner-reported, not independently accepted inventory.

Scrum records two independent bounded Developer corrections, minimal review/
integration handoffs and exclusive resources for actual shared writes. Lab index
edits require coordinated path-scoped reconciliation, not a dependency between
the two code contracts. Keep the accepted outer plan as history; existing Scrum
owns the scoped replacement dispatch and named integration, not this document.
Original E2E checks the changed exact join; original DevOps then revalidates the
same selected engine without startup replay, reruns complete Linux gates and
finishes exact rollback/effect readiness. BOTH actual exits gate one publisher.
Source review, image build, ReadOnly metadata or agreement on FAIL cannot meet
DevOps cloud-pass or the RP-S2 G1-G4/non-held-parent doneWhen.

Keep all historical UNKNOWNs, held parents, rollback assets, cleanup uncertainty,
five-consecutive-no-new-progress accounting and no new infrastructure/permissions.
No user-only action is established. Existing closeout pushes/readbacks intended
reviewed refs and updates stale measured README/recovery wording without
reopening customer clarity. No scripts, engine, settings or cloud effects are
executed in this architecture turn; tier updates refine only affected contracts.

## Scoped amendment: exact read-only helper mount regression (October 20, 2026)

This amendment applies only to `RP-S2-LINUX-ENGINE-READINESS`, under originating
reference `["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-LINUX-ENGINE-READINESS/AssignedWorkDeveloperLoop","linux-engine-exact-mount-contract"]`.
It implements the required reconciled disposition, not a new product decision
or approval stage. Opened scoped-replanning audit `3750c8de…` in current run
`0159ec9f-a89c-47f9-986f-80d9dfe6740a/context`, including original
Architect/Critic agreement with needs-replan and taskComplete false.
The accepted cumulative model and all earlier handoffs remain intact.

Read-only inspection of lab feature commits
`55a60e69df0e053be1b92da3b20d7875245e92e9` and
`1eec6d4750c4fff95bb08a047554e03e81c767f5` confirms that
`Build-Demo.ps1` mounts `Ensure-LinuxEngine.ps1` read-only, while
`NativeSettingsTests.test_exact_readonly_linux_mount_and_compile_closure_contains_new_helper`
in `foundry-tf/multi-agent/tests/test_release_native_settings.py` omits it from
the exact expected set. This is a confirmed caller/regression contract mismatch,
not a demonstrated permission or user-only blocker. Owner-reported targeted
13-pass and application 204-pass results do not waive the reported retained
gate: 203 passed, one failed, three inherited Linux-only skips. Those executions
were not independently rerun for this architecture amendment.

**Affected architecture disposition:** within **Guarded lab release toolchain**
(`release-toolchain`), **Exact-source guarded release** (`guarded-release`),
`release-package`, add only
`foundry-tf/multi-agent/tests/test_release_native_settings.py` to the existing
Developer's four-path ownership. The permitted edit is adding
`Ensure-LinuxEngine.ps1` to that regression's expected public read-only mount
set. Preserve exact equality, duplicate and file-presence checks, read-only and
network assertions, runtime-closure exclusions and compilation assertions.
Do not remove the necessary mount, skip the regression or weaken its contract.
The correction does not add the helper to the hosted runtime/package closure.
No coordinator/specialist tier, canonical component/flow/step ID, interface,
user requirement or execution authority changes.

Existing Scrum Master records this single-path ownership addition in a separate
one-assignment amendment; preserve the outer seven-task plan on disk and its
unrelated tasks. Keep the same task, Developer, doneWhen, exclusions, original
Architect/Critic reviews, exclusive resources and integration handoff. No new
dependency or Product Owner decision is required. Existing Developer commits
the exact correction, runs the affected regression and applicable retained
validation using explicit roots and pinned absolute Python, and returns exact
commit/hash/check evidence through original review. The passing retained gate
remains required; actual engine startup and Linux readiness are not prerequisites
for this bounded source assignment.

`release-join` still receives reviewed helper/test/build-input commits and hashes,
followed by original changed-join E2E before original DevOps executes recovery
and actual Linux/package gates. Both existing lab commits remain on the named
feature branch; no implementation is abandoned or redispatched here.
Independent selected-WSL rollback/effect inventory continues without this
correction. Preserve UNKNOWN effects, held parents, rollback assets, unrelated
work and five-consecutive-no-new-progress accounting. No real recovery,
Linux build, authentication, cloud, publication or live acceptance is asserted.
Only this cumulative document and the affected client-release tier contract
change; coordinator and specialist tier contracts remain applicable unchanged.

## Current RP-S1 continuation: retained session contracts and engine-readiness join (October 20, 2026)

This packet selects **RP-S1**, not a restart of its accepted implementation.
Consume accepted Architecture `cef352f4`, UX `6b6975c0`, ReleasePlan `48e3faf3`
and SprintDesign `5cc0f692`. Opened their original outcome audits
`398b66fa…`, `bf7fed70…`, `5a82b2df…` and `d8ab0784…` under current run
`0159ec9f-a89c-47f9-986f-80d9dfe6740a/context`: status agreed, all original
reviewers agree/taskComplete true with no unmet criteria within each bounded
document. These are input acceptances, not votes for this amendment.
No feedback or priorDispositions are supplied in this invocation; no historical
disposition is superseded. Earlier entries retain their originating boundaries.

Preserve completed predecessor RP-S1, **partial RP-S2** and pending RP-S3 live
work. The original stopped `sprint/2/RP-S2/DevOpsWorkLoop` in predecessor result
`71e45fd8-287f-40e8-89a9-d97021f8dee0/result.json` reports needs-replan;
Architect/Critic/Developer agree but each records taskComplete false. Its
selected Docker Linux endpoint was absent and no startup was attempted.
Retained WSL authenticated metadata reads succeeded, with mixed deployed
content, not final-common-bundle health or collaboration. Rollback-package
availability and complete unresolved-effect inventory remain open. No engine,
authentication, cloud or transport operation was repeated in this turn.

### Stable model, sprint criteria and actual source

The authoritative [solutionModel](customer-prototype-architecture.md#solutionmodel)
remains unchanged: ten components, five triggered flows, eighteen stable steps
and shared support links. This cumulative artifact references that model rather
than introducing a duplicate release component or renaming a customer flow.
RP-S1 retains **Remote design and review** and **Same-parent specialist
continuation**, all five `collaboration-*` and three `continuity-*` steps.
The new readiness handoff refines **Exact-source guarded release**,
`release-join` and `release-package`; it does not assert those steps now work.

| Approved boundary | Components and source modules | State and smallest receiving handoff |
|---|---|---|
| RP-S1 two-turn/revision bindings | **Hosted coordinator**, **Parent and specialist conversation state**: `demo/workflow.py`, `demo/foundry.py`, `tests/test_workflow.py` | Accepted offline source: parent/both hosted-framework child identities and pins remain stable, exactly two child creations, fresh responses/current requirements and stale-approval invalidation. Consume tests, do not recreate them. |
| RP-S1 actual model-history controls | **Hosted architect**, **Hosted reviewer**: `demo/specialist.py`, `demo/architect_agent.py`, `demo/reviewer_agent.py`, `tests/test_specialist_continuity.py` | Accepted offline reject/revise/review and persisted-history/fresh-history/known-response zero-send controls. Restored remote session is distinct from internal model history; neither fixture nor replayed brief proves live memory. |
| RP-S1 customer explanation | **Terminal client**: `README.md`, `demo/terminal.py`, `tests/test_demo.py`; accepted SprintDesign A-D, operator F/G | Accepted clarity implementation, opt-in finalized human stderr, unchanged stdout/parser and safe display aliases. Existing closeout owns stale measured-status wording, not renewed renderer work. |
| AC7 missing build prerequisite | **Guarded lab release toolchain**: proposed lab `foundry-tf/multi-agent/Ensure-LinuxEngine.ps1`, `tests/test_release_linux_engine.py`; retained `Release-Roots.ps1`, `Build-Demo.ps1` | Specified, not implemented/executed here. Scoped Developer source/tests -> original review -> integration/changed-join E2E -> original DevOps actual recovery and Linux checks. |
| AC8/AC9 source/effect closure | **Guarded lab release toolchain**, **Trusted identity and private transport**: retained `Invoke-WslCodeRelease.ps1`, source-root guards and package/preview wrappers | Accepted context callers lab `42a70533`, source integration `576b613`, latest handoff `0b6d99a` are consumed. Existing DevOps continues independent selected-route rollback/effect inventory. Exact new helper/build-test hashes must supplement unchanged runtime closure. |

Source acceptance and local integration PASS do not prove deployed operation.
Identity assessment remains explicitly unresolved live; neither A nor B is
selected by this local recovery contract. Preserve finite trusted architect
ingress/equality before reviewer, independent reviewer entry and deterministic
artifact gates before genuine Decision-1. No speculative identity bypass,
permission/infrastructure mutation or hidden local fallback.

### Recovery interface and precise construction boundary

Apply the accepted full-release
[existing-engine contract](customer-prototype-architecture.md#smallest-recovery-operation-and-caller-boundary)
without widening it. Existing Scrum Master assigns the existing Developer
`RP-S2-LINUX-ENGINE-READINESS` in the registered authorized lab feature sibling.
Owned scope: new `Ensure-LinuxEngine.ps1`, new
`tests/test_release_linux_engine.py`, only necessary read-only public test-input
mounts in `Build-Demo.ps1`, and lab `.github/repo-index.md`.
Application runtime, private settings, production/default profiles and canonical
dirty lab paths are not writable parts of this correction.

- Helper accepts explicit `ApplicationRoot` and `LabRepositoryRoot`, uses
  loaded `Release-Roots.ps1` ownership validation and a finite validated budget.
  It diagnoses only the effective selected existing local Docker Desktop Linux
  context/endpoint and conflicting overrides; context/config credential dumps
  are excluded. Ambiguous, remote, unsupported or changed selection fails closed.
- Already-responsive Linux server succeeds without startup. Supported recovery
  invokes `docker desktop start` at most once and observes the same selected
  Linux server within bounded command execution and readiness polling.
  Startup exit zero is not readiness. Report attempted startup, observed
  readiness/failure and elapsed waiting without private identifiers.
- Missing/unsupported tooling, failed/hung startup, selection drift and timeout
  fail nonzero, with no build/publication continuation. Bound owned commands,
  never kill unrelated processes or the existing engine. No installation,
  host/daemon reconfiguration, engine/context substitution or restart of a
  ready engine; no automatic authentication, grants or uncertain-effect replay.
- Required fake-command regressions cover ready/no-start, recoverable,
  failed-start, failed-readiness, wrong/changing selection, invalid/crossed
  roots, missing/unsupported tooling and hung commands. Assert no build or
  publication on failure. Windows executable coverage uses pinned absolute
  Python; justified Linux exclusions are not execution coverage.

Read-only inspection of lab `42a70533` confirms `Build-Demo.ps1` already gates
Linux/amd64 image inspection, actual application tests and a separate retained
release container suite. Its named public tool mounts omit the proposed helper.
Add only the necessary read-only source-inspection test input; do not make
Windows startup execute in the Linux container. Keep Build-Demo offline:
DevOps explicitly runs the reviewed helper first, then retained build on success.
Preserve dependency provenance, source/image bindings and every package guard.
Local Docker startup is not hosted G6 supported compute stop/resume.

### Minimal joins, independent work and cumulative live exit

1. **Scrum Master** owns precise assignment, critical path and Git reconciliation.
   No whole-RP-S2 acceptance dependency gates helper construction or independent
   selected-WSL rollback/effect inventory. Coordinate existing engine/stage
   exclusive resources separately from the one publisher's shared context,
   transport and mount resources; scheduler labels do not provide OS isolation.
2. **Developer/integration** returns scoped committed/reviewed helper, caller/test
   inputs and attributable results. Reconcile/push/read back intended reviewed
   feature refs, actual loaded-source equality and changed hashes through the
   existing owner. Do not certify a new helper with the old nine-lab-file closure.
   Original E2E checks the affected exact join before original DevOps execution.
3. **DevOps** continues selected-WSL rollback-package/effect inventory now using
   retained read-only tooling. The prior receipt is bounded route evidence,
   not freshness before later effects, rollback closure, inference or permission
   to clear historical UNKNOWNs. Unused Windows-helper acceptance cannot gate WSL.
4. **One original serialized DevOps publisher** joins BOTH actual Linux/package
   and private-route/rollback/effect readiness exits. Revalidate freshness, build/
   preview/bind/publish the exact final common bundle, reconcile every outcome,
   prove architect before reviewer and complete actual G1-G4 plus a non-held
   initial parent. Helper mocks, startup success and metadata never replace this.
5. **RP-S3** receives measured parent/both-child hosted-framework bindings/pins,
   current artifacts, checkpoints and reconciled effects for two-turn continuity,
   once-only confirmed supported recovery and separate-parent isolation.
   Isolation need not wait for recovery success; accepted fixtures support
   independent preparation, not invented missing construction or live proof.

All three tier contracts below carry this handoff without runtime changes.
Preserve historical UNKNOWNs, held parents, rollback assets, unrelated work and
historical cleanup uncertainty. AC1-AC9/G1-G8 remain actual release criteria;
account-wide Blob permissions imply application-enforced, not malicious-host,
isolation. Original five-consecutive-no-new-progress accounting is unchanged.
Feasible helper construction and independent inventory remain: work is not
exhausted and no user-only action is established. This deliverable is an
architecture contract, not engine, package, deployment or customer acceptance.

## Current RP-S2: validated source to initial hosted collaboration (October 20, 2026)

This entry governs **RP-S2**; earlier entries preserve their originating
observations and acceptance boundaries, not current implementation instructions.
Baseline is clean application feature `4a1b1addd2811b3c0524e75741ea54659d2eb873`.
Consume Architecture/UX retrospective `8e4019b`, ReleasePlan review `835713a`
and SprintDesign `4a1b1add`. The RP-S1 offline continuity, revision/history
controls and terminal work remain accepted source. Operational-context caller
correction `42a70533c567a8aed29f0ca076c0b5d58381fc77` and integration
`576b613eea651d21c712490bb3e84eadf5bcbbb6` are accepted handoffs, not assignments
to repeat. The tool/profile source-contract mismatch is **closed locally**;
runtime identity selection and the actual Linux/package/live exit remain open.

### Evidence consumed and disposition boundaries

Opened original outcome JSONs under the supplied run
`bf0d82d9-657b-4055-9f7c-6306ce08163d/context`, including original votes:

| Audit prefix | Accepted boundary used here |
|---|---|
| `e4962cb0` | Packaging-caller architecture amendment; Product Owner, Critic and Red Team agree. |
| `e0001d3b` | Changed-source integration; Architect/Critic agree. |
| `abd55a79` | E2E: local integration PASS / release acceptance FAIL; Architect/Critic/Product Owner agree. |
| `b53113c5` | DevOps preparation, not cloud-pass; Architect/Critic/Developer agree. |
| `f2f25e66`, `01e02e83` | Original sprint review and retrospective agree on unchanged sprint contracts and existing-owner closing actions. |
| `40236938` | RP-S2 SprintDesign; Product Owner/Critic agree on Screens A/B/D/F/G. |

Agreement accepts those bounded deliverables, not their unreached cloud gates.
ARM/account/model-metadata/host-trust observations and Docker Linux-engine
endpoint failure are **DevOps-owner-attributed**, not independently rerun here.
The Docker failure establishes unavailable selected engine, not a missing
permission, required installation or user-only remedy. Windows context account
checks are not WSL authentication, private transport or specialist ingress.

Apply the three exact references under
`yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-OPERATIONAL-CONTEXT/plan-round/2/AssignedWorkDeveloperLoop`:
`operational-context-caller-completion`, `operational-context-final-checks-handoff`
and `operational-context-package-caller-ownership`. Accepted correction,
integration and E2E consume them; do not reopen caller ownership or coding.
The exact prior references
`["yaml-loops-v1:sprint/1/RP-S1/SprintPlanLoop","sprint-plan-output-shape"]`,
`["yaml-loops-v1:sprint/1/RP-S1/SprintPlanLoop","sprint-plan-original-dispatch"]`
and
`["yaml-loops-v1:sprint/1/RP-S1/SprintRetroLoop","retrospective-release-plan-response-shape"]`
retain their originating response/dispatch boundaries. None is a new RP-S2
architecture criterion or waiver. No disposition is superseded here.

### solutionModel and current cross-tier contract

The authoritative [solutionModel](customer-prototype-architecture.md#solutionmodel)
remains unchanged: ten components, five triggered flows and eighteen steps,
including shared support links. Current scope is **Exact-source guarded release**
(`release-join`, `release-package`, `release-discriminate`) and **Remote design
and review** (all five `collaboration-*` steps). RP-S1 contracts remain cumulative;
`release-close`, continuity, supported recovery and isolation retain RP-S3's
actual prerequisites. No new service, framework, public schema or session manager.

| Tier | Current RP-S2 interface and closing observation |
|---|---|
| [Client/release](requirements/client-release/architecture.md#current-rp-s2-selected-route-and-exact-package-contract) | **Terminal client**, **Guarded lab release toolchain**, shared **Trusted identity and private transport**: consume exact source/local E2E; establish route-specific readiness, fresh inventory and immutable Linux common-package closure before serialized effects. F/G distinguish each reached boundary. |
| [Coordinator](requirements/coordinator/architecture.md#current-rp-s2-initial-parent-and-acceptance-contract) | **Hosted coordinator**, **Decision-1 routing and admission**, **MAF workflow checkpoints**: bind a fresh synthetic parent, gate genuine routing, call both remote roles and accept exact current immutable artifacts through ETag/fencing. Return useful result only with trustworthy finalization. |
| [Specialists](requirements/specialists/architecture.md#current-rp-s2-independent-trusted-ingress-contract) | **Hosted architect**, **Hosted reviewer**, shared **Parent and specialist conversation state**: prove architect entry before reviewer dispatch, then independently prove reviewer entry/current prerequisites. Preserve restored remote sessions and distinct internal model-history state. |
| Shared artifact support | **Private Blob artifacts and effect journal** remains one shared component. Actual private-path managed-identity operations, producer/hash/version/revision checks and effect reconciliation are required; no new store or inferred zero-effect observation. |

Keep implemented `ApplicationRoot` for portable source, `LabRepositoryRoot`
for reviewed loaded tools, and `OperationalLabRoot` for only the existing
dedicated context imported by unchanged `scripts/Use-Settings.ps1`. Preserve
profile/registry/imported scope equality, actual account/project/target checks,
WSL profile/azd selection, restoration, private-output exclusions and crossed-tool
rejection. Context never selects code. E2E's inspected source closure is
`8974f4cdae0850f8528d1261e6d9617e756e157316449385875d55e05f29b6f3`;
it is an attributed exact-join reference, not a seal for a future changed stage.

### Readiness branches, release order and original-owner handoff

1. **Existing Scrum Master** decomposes remaining work, owns Git reconciliation
   assignment and minimal dependencies. Linux-engine readiness and selected-route/
   fresh inventory preparation may proceed independently; no identity-trial
   dependency precedes read-only inventory. Names coordinate the scheduler,
   not OS/cross-run isolation. Serialize shared effects with `lab-hosted-release`,
   `lab-private-transport`, `lab-cli-context` and `lab-ssh-mount`.
2. **Original DevOps** restores existing Linux-engine availability within actual
   authority, then runs retained Linux/amd64/hosting-Python checks and exact
   common-package build. Executable presence or Windows skips cannot pass this.
   If recovery needs an unapproved host change, report its exact requirement;
   do not infer one from endpoint absence.
3. **Selected private route** must pass its own guards: retained WSL requires
   actual user/systemd/cgroup containment, dedicated WSL profile/authentication,
   pinned azd and read-only mount/owned cleanup. Windows requires independently
   accepted external helper source plus exact module/C# pins before import.
   Unused Windows-helper acceptance is not a WSL prerequisite. Do not use the
   unaccepted standalone launcher or adopt canonical dirty source/registry.
   Supplied accepted fingerprint is the trust input, not proof of SSH success.
4. **Original serialized DevOps** verifies current exact three-role targets,
   deployed/rollback bindings and unresolved effects through retained scripts;
   binds exact source/settings/ZIP and preview approvals; publishes only the
   intended package. Consume accepted E2E; if source changes, relevant exact-join
   E2E/checks must cover the new join, not merely an old accepted report.
5. **Finite identity discrimination** proves architect trusted ingress/equality
   before reviewer, then independently proves reviewer. Neither A nor B is
   live-selected. Existing specialist-only B source is not a tested A remedy
   or automatic fallback. Opaque call IDs are not delegated user identity.
   Current replan forbids infrastructure/permission mutation; a newly necessary
   material remedy returns through existing scope reconciliation, not an ad hoc
   grant. No provider submission or uncertain-effect replay.
6. **RP-S2 exit** requires three healthy exact versions on one final verified
   common bundle and retained rollback assets (G1), real remote current-artifact
   coordinator acceptance (G2), actual private MI Blob provenance (G3), genuine
   Decision-1 after deterministic gates (G4), and a completed non-held initial
   parent. Path selection, HTTP 200, upload and accepted reports are insufficient.
   Record precise unreached/held boundary on failure; do not manufacture another
   parent to hide failure or send follow-up into held state.

Only the actual exit supplies RP-S3's original parent/both-child bindings, pins,
current artifact refs, checkpoints and reconciled effects. Follow-up compares
stable identity fields with advancing response IDs; supported stop/resume retains
its once-only marker/confirmed stopped state. Separate-parent isolation has its
own release prerequisites and does not depend on recovery success. Account-wide
Blob Contributor gives application-enforced ownership/isolation, not malicious-host
or storage-RBAC isolation. Preserve historical UNKNOWNs, held parents, rollback
assets, unrelated work, historical cleanup uncertainty and original five-round
no-progress semantics; no productive-round cap or stop reset.

Existing measured-status closeout owner updates stale README/release notices
from actual results; do not redispatch accepted README or renderer work.
Retain Screens A/B/D/F/G, conditional human-view demonstration, unchanged
stdout/parser and private evidence outside customer Git. Integration/closeout
pushes reviewed architecture commits with exact ref readback after original
review. This documentation turn creates no deployment, authentication, package,
transport, inference or live proof and establishes no human-only action.

## Scoped amendment: operational-context packaging caller (October 20, 2026)

This amendment changes only the affected release-tier ownership handoff for
`RP-S2-OPERATIONAL-CONTEXT`; the cumulative RP-S1/RP-S2/RP-S3 design below
remains in force. Inspected clean application feature HEAD
`f4ec1496c6f59cb08142c3b875deefdf695de30c` and registered lab feature-sibling
HEAD `d0073536c2969e885bdcc767ddccbebd7deda7d5`. Opened the original
SprintArchitecture outcome `b785b84135b5bd353d7281c42469fa022bc3b02511ddacb7296463f1a311f66f.json`
and scoped-replan / reconciled-feedback audits
`da4ef440c2bfcab7052365c64dcd6bdf5cc3b8ec3b11326d98e7cd277dc91885.json` /
`ed4b8353a33c62428743c9ca036041095b8925471555ea749ab898abce2ec0cb.json`
in this run's existing workflow context. Original Product Owner/Critic/Red Team
accepted architecture `5906ee3`; original Architect/Critic agree with the
Developer's subsequent **needs-replan**, explicitly not task completion.
This amendment does not claim their votes for the new architecture disposition.

### Decision and exact acceptance boundary

Apply these originating references as one bounded set; none is superseded:

- `["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-OPERATIONAL-CONTEXT/plan-round/2/AssignedWorkDeveloperLoop","operational-context-package-caller-ownership"]`
- `["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-OPERATIONAL-CONTEXT/plan-round/2/AssignedWorkDeveloperLoop","operational-context-caller-completion"]`
- `["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-OPERATIONAL-CONTEXT/plan-round/2/AssignedWorkDeveloperLoop","operational-context-final-checks-handoff"]`

**Architect disposition:** include
`foundry-tf/multi-agent/bundle_package.py` in this same Developer assignment's
explicit writable paths, solely to propagate and validate the existing
operational-context contract. Existing Scrum Master records that one-path
ownership addition in the scoped replacement assignment; do not change the
outer plan or introduce a packaging rewrite, new task owner or approval stage.
Use the already-owned test paths for required regressions. Retain the original
doneWhen, exclusions, original Architect/Critic review and
`RP-S2-CONTEXT-INTEGRATE` handoff. The same Developer continues from the retained
partial commit; no accepted work is redispatched.

The two originating SprintPlan dispositions
`["yaml-loops-v1:sprint/1/RP-S1/SprintPlanLoop","sprint-plan-output-shape"]` and
`["yaml-loops-v1:sprint/1/RP-S1/SprintPlanLoop","sprint-plan-original-dispatch"]`
remain satisfied within their planning output/dispatch boundary. They are not
new architecture criteria, waivers or reasons to reopen the accepted plan.

### Technical basis and unchanged cross-tier contract

Read-only inspection of committed `bundle_package.py:package()` confirms it
sets `repo = roots.lab` and rejects `AZURE_CONFIG_DIR` unless it equals
`repo/.azure-cli/wsl`, before account readback and azd prerequisite checks.
Changing the five PowerShell entry points alone therefore cannot support
distinct tool and operational roots. This is an omitted necessary caller,
not a credential, permission, authentication or provider diagnosis.

Partial commit `d0073536` adds
`Resolve-ReleaseOperationalContext -Roots <resolved-tool-roots> -OperationalLabRoot <existing-context-root> [-RequireWsl]`
and `ReleaseRoots.operational_context(value=None, wsl=False)`, with synthetic
root validation tests. These are foundations, not wired release interfaces.
No proposed operational flag is a demonstrated customer command.

For `bundle_package.py` as for every affected caller, validate/select the
existing dedicated operational context under the three-root contract below;
do not derive the WSL profile from tool-source ownership. Preserve selected
`LabRepositoryRoot` / `roots.lab` for reviewed source loading, resolver/module
ownership, package-source binding and loaded-source equality. Operational
registry/imported scope equality, dedicated profile validation, actual account
readback, project/region/model/target checks and azd selection remain required
before effects. Do not merely remove the profile check or reassign the tool
root to the operational root. Operational private paths stay outside source,
stages, bundles and public evidence; preserve all uncertain-attempt/replay holds.

The same Developer must finish the five entry points and affected callers,
including this packaging caller, calibration, operational private-path
exclusions, WSL profile/azd propagation and success/failure environment
restoration. Required caller tests must exercise matched/distinct contexts and
reject invalid roots/profiles/scope before effects, while retaining crossed-tool
rejection and actual loaded-source equality. Run targeted, retained and required
application/repository checks on final committed caller-integrated source.
Resolve the reported native/retained fixture import collision with supported
fixture binding; keep originating justification for exclusions and never count
skips as completed Linux/native coverage. Earlier owner-reported passing tests
do not establish caller completion and are not rerun here for progress credit.

### Model, tiers and receiving owners

The authoritative `solutionModel` remains the referenced
[Architecture model](customer-prototype-architecture.md#solutionmodel):
ten components, five flows, eighteen steps, unchanged IDs and support links.
Only **Guarded lab release toolchain** (`release-toolchain`) and its shared
**Trusted identity and private transport** (`identity-boundary`) boundary are
refined, in **Exact-source guarded release** (`guarded-release`) steps
`release-join` / `release-package`. The
[client/release tier amendment](requirements/client-release/architecture.md#scoped-operational-context-packaging-caller-amendment)
records the implementation boundary. Coordinator and specialist contracts
below are unchanged; there is no hosted runtime, session or identity-path change.

Scrum returns a self-contained scoped replacement graph for this assignment;
it does not require later DevOps work before implementation. After the same
Developer's final scoped commits and original reviews, designated integration
receives exact commits, caller inventory, supported invocation contract,
root/source hashes, checks and limitations. Partial `d0073536` alone is
**not execution-ready**. Original changed-join E2E then serialized DevOps
Linux/common-package/publication/live gates remain unchanged; independent
preparation remains independent. README correction `f4ec1496` is already an
accepted handoff, not new clarity work. Preserve accepted ownership/runner/
integration, historical UNKNOWNs, held parents, rollback assets, unrelated
work and original five-consecutive-no-progress semantics. No human-only action
or operational readiness is established by this architecture amendment.

## Sprint architecture entry: RP-S1 canonical continuity contracts (October 20, 2026)

The current packet selects **RP-S1**, not the older RP-S3 overlay below.
Inspected clean application baseline `4532255524c8082027c4f3fe8fb9cba9e9cb2614`
on `feature/customer-hosted-session-prototype`. Consume Architecture
`f5fc1dec9b01e98745268e359808f3021a8906de`, UX
`063787500eb3404c1932ff921af5079a170d90ac`, ReleasePlan
`7a43d1fcab694fd1e3ce3532a144b3e5bdb92739` and SprintDesign
`4532255524c8082027c4f3fe8fb9cba9e9cb2614`. Independently opened all four
supplied outcome JSON files under the application's workflow context:
their original reviewers record `agree=true`, `taskComplete=true` and no
unmet criteria for those bounded artifacts. Those votes
do not transfer to this SprintArchitecture or establish live execution.
That entry's original packet supplied no completed sprints, assignments, separate
blocked-decision list, reconciled feedback or prior dispositions; the scoped
amendment above now consumes the subsequent bounded dispositions. Historical
overlays retain their originating boundaries; they are not newly imposed
acceptance demands.

### solutionModel and cumulative scope

The authoritative `solutionModel` is the existing
[Architecture model](customer-prototype-architecture.md#solutionmodel):
ten components, five triggered flows and eighteen uniquely identified steps.
This sprint references that model rather than duplicating or renaming it.
No components, services, public contracts, dependencies or model IDs change.

| Tier | Canonical components and implementation boundary |
|---|---|
| [Coordinator](requirements/coordinator/architecture.md#rp-s1-canonical-coordinator-contract) | `coordinator` (**Hosted coordinator**), `decision-routing` (**Decision-1 routing and admission**) and `workflow-checkpoints` (**MAF workflow checkpoints**). Retain explicit begin/route/execute/publish in `demo/workflow.py`, checkpoint wiring in `demo/host.py`, routing after deterministic gates and fenced current-output acceptance. |
| [Specialists](requirements/specialists/architecture.md#rp-s1-canonical-specialist-contract) | `architect` (**Hosted architect**), `reviewer` (**Hosted reviewer**) and shared `conversation-state` (**Parent and specialist conversation state**). Retain remote session restoration in `demo/foundry.py` and five-stage model-history paths in both role modules. |
| [Client/release](requirements/client-release/architecture.md#rp-s1-canonical-client-release-contract) | `terminal-client` (**Terminal client**) and `release-toolchain` (**Guarded lab release toolchain**). Retain opt-in finalized human stderr and unchanged stdout/parser. Separate reviewed tool source from existing dedicated operational context; correct stale README status through existing clarity ownership, not a new renderer. |
| Shared support, defined once | `artifact-plane` (**Private Blob artifacts and effect journal**) supports all three hosted roles; `identity-boundary` (**Trusted identity and private transport**) supports the terminal, roles and artifact plane. Keep their canonical support links, trusted scope, exact immutable refs, private MI path, ETag/fencing and unknown-effect holds. Tier references do not create separate stores or identities. |

| Canonical flow | Trigger, current refinement and cumulative boundary |
|---|---|
| `remote-collaboration` — **Remote design and review** | A fresh synthetic initial requirement triggers `collaboration-bind`, `collaboration-route`, `collaboration-design`, `collaboration-review`, `collaboration-return`. RP-S1 retains directly testable repeated-call contracts and Screens A-D. Actual trusted architect then reviewer ingress, common-bundle provenance and live coordinator acceptance remain RP-S2. |
| `two-turn-continuity` — **Same-parent specialist continuation** | A queue follow-up to a completed non-held parent triggers `continuity-revise`, `continuity-invoke`, `continuity-verify`. RP-S1 fixes the offline comparison boundary below; actual same-parent live proof remains RP-S3 after RP-S2's initial-parent gate. |
| `supported-recovery` — **Supported compute stop and resume** | One retained-script stop request triggers `recovery-stop`, `recovery-resume`, `recovery-verify`. Preserve durable once-only marker, independently confirmed stopped/idle state, original bindings, checkpoints and reconciled effects; no hard-crash or exactly-once claim. Execution remains RP-S3, not an RP-S1 exit condition. |
| `parent-isolation` — **Separate-parent isolation** | A separate synthetic parent on a verified release triggers `isolation-bind`, `isolation-execute`, `isolation-verify`. Require distinct child/history/artifact scope and first-parent requirement exclusion. Its release prerequisites and initial-parent comparison do not depend on successful follow-up/recovery. |
| `guarded-release` — **Exact-source guarded release** | Reviewed owned commits trigger `release-join`, `release-package`, `release-discriminate`, `release-close`. Consume accepted ownership/runner/integration; correct explicit operational-context propagation, rejoin changed source and revalidate through original local-script E2E before serialized DevOps exact-package/live gates. Containment/resource/trust/inventory preparation is independent of coding; no second publisher. |

### RP-S1 contract-first handoff

The actual source chain is parent-scoped `manifest.children.get(role)` in
`WorkflowRuntime.execute()` -> `RemoteAgents.invoke()` restoring
`AgentSession.from_dict(child.framework)` at the pinned version -> each
specialist's `load_or_create_llm_session()` loading `specialist_history_v2`
-> model call -> validated immutable output and stored model continuation.
The remote child framework session and specialist internal model history are
different. Compare stable identity fields and pins, not whole serialized state:
response IDs and continuation state must advance. Conversation history, MAF
checkpoints, artifacts and write-ahead effects remain four distinct concerns.

| RP-S1 criterion | Retained implementation/check interface and receiving owner |
|---|---|
| Two-turn continuity | `tests/test_workflow.py` binding assertions compare parent scope, both hosted/framework child identities and pins, exactly two child creations, both roles on both turns, fresh invocation responses, exact current prerequisite refs and stale-approval invalidation. Integration/E2E checks relevant joined source; alias equality and recalled requirements are insufficient. |
| Controlled repeated calls | Retain `test_reject_revise_review_reuses_both_children_with_fresh_responses`: architect -> blocked reviewer -> same architect -> same reviewer, four new responses and accepted current revisions. This controlled graph uses synthetic boundaries, never live specialist evidence. |
| Direct specialist history | Retain both roles' load/model/store and serialized-value assertions in `tests/test_specialist_continuity.py`, identical-brief fresh-history controls, exact-response zero-send recovery and held/mismatched-effect negatives. Replayed full briefs do not replace these controls. |
| Clarity without parser drift | Consume accepted SprintDesign Screens A-D and `HumanView` / `finalize_workflow_turn` in `demo/terminal.py`; retain `HumanTerminalTests` in `tests/test_demo.py`. Useful current candidate/review and chronological calls appear in opt-in human stderr after finalization. Machine stdout/parser and privacy/control neutralization remain unchanged; the human view is observational, not a continuity verifier. |
| Attributable checks and supported identity assessment | Original source-check/integration owners retain exact changed-source checks and the explicit repository-index closing action. Existing recovery assessment and finite A/B contract provide an actionable unresolved handoff. No new research, renderer or fixture assignment is justified merely by a blocked release. |

### Prior blockers and downstream decisions

Neither identity path is live-selected. The specialist-only B source candidate
is not a measured A correction, automatic fallback or proven ingress remedy.
Historical `NATIVE_HOST_PRINCIPAL` occurred before architect application
execution; it does not prove the current candidate fails, a provider defect or
a missing grant. Preparation rejection leaves receivers unreached. Original
DevOps must discriminate with actual trusted receiver evidence, architect before
reviewer, under the retained finite scripted contract. Necessary demonstrated
chosen-path permissions are pre-approved with exact scope/rationale and
readback; no speculative grant, opaque-call-ID user identity or receiver
equality relaxation is authorized. A material namespace/contract change uses
existing Scrum reconciliation and Architect-advised Product Owner decisions.

The accepted current Architecture/ReleasePlan consume predecessor
`bb3af682-2d1c-41cf-97e7-312f624ea669/result.json` and substantive original
Architect/Critic acceptance for the exact boundaries
`sprint/1/RP-S1/task/RP-S2-LAB-OWNERSHIP/AssignedWorkDeveloperLoop`,
`sprint/1/RP-S1/task/RP-S2-DECISION-RUNNER/AssignedWorkDeveloperLoop` and
`sprint/1/RP-S1/task/RP-S2-SOURCE-INTEGRATE/AssignedWorkDeveloperLoop`.
Consume lab correction `18429840e86d92c26611bae3ffdc7095ca87592d` and application
integration `1bd157d05116b076b0aa45b4fb6bfe531e5d28d0` without reopening them.
This supersedes only pending acceptance/write-block direction within those
originating boundaries, including the earlier ownership evidence-access
reference in this document's historical entries. It does not reset their
five-round stop, reconcile UNKNOWN effects or establish operational readiness.
The predecessor original E2E agreement is an actionable predeployment **FAIL**.
No ownership recapture, renewed designation or unchanged runner fix is assigned.

Architecture `f5fc1de` attributes the concrete failure to retained wrappers
deriving a profile from the feature tooling sibling instead of the existing
dedicated operational context. Its independently matched evidence hash is
`38ec94d9d218e25791b60a2ed0dac80877538b0dcb128e94452aac077571f8b2`.
This sprint consumes that source inspection; it does not rerun the capture or
inspect credentials. Configuration failure before external operations is not
an expired-credential diagnosis, ingress rejection or user-only blocker.

### Operational-context contract across the three tiers

Refine `release-join` and `release-package` in the existing
**Guarded lab release toolchain**, not the hosted runtime or canonical model:

| Input | Sole responsibility and fail-closed boundary |
|---|---|
| `ApplicationRoot` | Portable application source/package/test owner; never a profile selector. |
| `LabRepositoryRoot` | Reviewed feature-sibling tool-source owner. Absolute wrapper, resolver, Python modules and helper sources must match this selected root; preserve `LAB_TOOL_OWNER_MISMATCH`, crossed-tool negatives and raw-byte source closure. |
| `OperationalLabRoot` | Explicit existing dedicated operational context, propagated through affected callers. Select via unchanged `scripts/Use-Settings.ps1` import: imported `LAB_REPOSITORY_ROOT` supplies this argument and imported `AZURE_CONFIG_DIR` supplies its dedicated Windows profile. It never selects loaded tools or runtime bundle contents. |

The five affected retained entry points are `Test-LabPrerequisites.ps1`,
`Test-PrivateConnectivity.ps1`, `Build-CodePackage.ps1`,
`Build-BundledCodePackage.ps1` and `Invoke-WslCodeRelease.ps1`. Existing Developer
must correct their exact callers and necessary shared helper/tests as one bounded
contract. Scrum establishes new precise feature-sibling path ownership first;
the accepted eight-path runner designation does not own these additional files.
No canonical dirty-checkout edits, root-guard relaxation or private-settings edit.

Before effects, require canonical absolute existing directories, reject relative,
missing, reparse/escape and arbitrary/default/production profile substitutions.
Require the selected Windows profile to equal both imported dedicated
`AZURE_CONFIG_DIR` and operational-root `.azure-cli`; compare operational and
selected-tool registry tenant/subscription against imported expected scope
without displaying values. Retain project/region/model/target checks and actual
account readback. Registry scope equality does not approve dirty source adoption.
If the new argument is omitted for a legacy caller, only the selected lab root's
existing validated dedicated context may default; no search or silent fallback.

Windows uses that existing profile. WSL explicitly maps the same operational
root's retained `.azure-cli/wsl`, preserving path translation, Azure CLI/azd
selection and environment restoration on success/failure. Windows token-cache
readiness does not imply WSL readiness. Do not copy, inspect or symlink
credentials, create duplicate profiles or change private settings. Calibration
must compare its profile against the validated operational context, retaining
scope/source/no-replay checks. Operational metadata remains private and outside
source packages. `LAB_TOOLS` and resolver roots remain the selected tool source.

### Original-owner closing actions and cumulative release handoff

1. **Scrum/Developer:** scope the smallest five-entry-point/caller correction
   in the authorized feature sibling. Required synthetic coverage: legacy
   matched roots; distinct reviewed-tool/existing-context roots; missing,
   relative, reparse, default/mismatched profile and tenant/subscription rejection
   before effects; calibration; every affected caller; WSL mapping/azd selection;
   environment restoration; unchanged crossed-tool and actual loaded-source
   equality. Run targeted, affected retained and application/repository checks.
   Original Architect/Critic review actual scoped commits. This task is an
   RP-S2 release prerequisite, not an extra RP-S1 offline implementation demand.
2. **Integration Developer:** rejoin changed reviewed wrapper/helper roots,
   bytes/hashes and commits; push/read back scoped reviewed feature refs,
   including accepted `1bd157d` if still absent remotely. Record task/branch/
   commit accounting and any retained abandoned code branch/reason. Do not repeat
   the unchanged execution-unready integration report as the remedy.
3. **Original E2E then DevOps:** validate changed exact join through local
   repository scripts. Independent containment-source/resource, supplied strict
   trust, target/rollback inventory and unresolved-effect preparation can proceed
   separately. DevOps alone serializes actual Linux/amd64/hosting-Python checks,
   exact common-bundle preview/publication, architect-before-reviewer identity
   discrimination and live G1-G8. Preserve original actual live AC1-AC9 gates.
   If retained checks genuinely require authentication, surface the actual
   device URL/code when emitted; profile separation alone does not require
   human action. No infrastructure/permission mutation is part of this replan.
4. **Existing clarity/closeout owner:** apply accepted SprintDesign A/F/G status
   copy to remove stale README pending-ownership/write-block wording. State the
   accepted source handoffs, actual configuration correction and unmet live
   gates without advertising proposed `OperationalLabRoot` as a runnable customer
   command. Preserve A-D, existing renderer, stdout/parser and privacy controls.

Scrum owns minimal dependencies, actual shared exclusive resources and Git
reconciliation; this architecture creates no competing task graph or review
stage. RP-S1 retains the two-flow/eight-step offline contract above; RP-S2 still
requires an actual common-bundle accepted non-held initial parent; RP-S3 still
requires same-parent live continuation, once-only confirmed supported recovery,
independent separate-parent isolation and truthful closure. No sprint's bounded
document acceptance substitutes for those downstream outcomes.

The current ReleasePlan/SprintDesign consume the closed workflow-context
exclusion and successful unchanged repository checks. The older index-drift
failure below is attributed history, not a current blocker or new cleanup
assignment. Preserve ignored context; do not index it, delete unowned files or
redispatch accepted source-exclusion work. Current checks still apply to this
edit and subsequent integrated source; no AC7 waiver is implied.
All AC1-AC9/G1-G8 remain required for release. Preserve UNKNOWNs,
held parents, rollback assets, unrelated work and historical cleanup uncertainty.
Blob Contributor remains account-wide: isolation is application-enforced,
not storage-RBAC or malicious-host isolation.

### Validation of this sprint refinement

The direct in-memory check passed unchanged canonical ten-component/five-flow/
eighteen-step model equality with HEAD, unique IDs and component references,
all current tier links/anchors, four input commits and the five affected
caller contracts. The retained inventory generator refreshed without public
path changes. `scripts/Test-Repository.ps1` passed using the existing absolute
lab virtual-environment Python 3.12.10: current index, 80-file public boundary,
JSON, PowerShell, context frontmatter and whitespace checks. No dependencies
were installed. Four supplied audit files were independently
opened: all original input reviewers agree with `taskComplete=true` and no
unmet criteria. These are bounded input votes, not votes for this deliverable
or runtime proof. No lab source changes or credential/settings inspection are
needed for this sprint refinement. Unchanged application suites are not rerun
merely for progress credit; implementation's targeted/retained/application and
Linux hosting-package gates remain required for the actual correction.
The earlier refinement's 204 offline tests in 44.614 seconds and its
interpreter-selection failure are historical, not fresh checks of this edit.

Architect accepts this bounded current-sprint/cumulative/tier design for
original Product Owner, Critic and Red Team review; their votes for this loop
are not yet supplied.
No settings import, fresh cloud inventory, permission mutation, publication,
inference, stop/resume, operational integration, final push or live success is
claimed. Documentation completion is not new runtime progress.

<a id="current-rp-s3-gated-continuation-recovery-isolation-and-delivery-october-20-2026"></a>

## Historical RP-S3: gated continuation, recovery, isolation and delivery (October 20, 2026)

Current sprint is **RP-S3: live continuity, recovery, isolation and customer
delivery**. Inspected clean authorized feature baseline
`23a4d9a950a73a57c13f6b29a9ca6da685e5c987`, containing accepted current RP-S3
SprintDesign. Consume accepted RP-S2 architecture
`1bce6e1c4fe9e8deb8382fa02c44392bc2d25aea`, SprintReview
`1e5eb2adc7714875e07ed69ffd2e2db0ab8c7877` and retrospective
`afe6d4dba937102e12821d770c1f7da4788f1c2c`. Completed RP-S1/RP-S2 workflow
history does not establish their live release goals. Earlier overlays retain
their original attribution; this section governs the current sprint mapping.

### Cumulative design and entry boundary

Retain exactly three remote hosted roles and explicit coordinator
begin/route/execute/publish. The trusted parent manifest's `children.get(role)`
creates or reuses each specialist binding; `RemoteAgents.invoke()` restores
its framework `AgentSession` and pinned version. Each specialist separately
restores `specialist_history_v2` before its model call and persists history
after validated immutable output. Conversation/model history, MAF checkpoints,
immutable artifacts and fenced write-ahead effects are distinct responsibilities.
Keep trusted receiver equality, exact prerequisite/producer/version/revision/hash
checks, coordinator ETag/fencing, Decision-1 after deterministic gates and
unknown-effect holds. No runtime rewrite, new service, generic session manager,
schema, collector, ledger, flag, dependency or duplicate fixture work is needed.

**Entry is BLOCKED:** verified common-bundle G1-G4 and a completed non-held
initial parent are not established. Neither identity path is live-selected.
The latest ownership outcome remains substantively incomplete; runner writes
remain blocked. Supplied coordination and accepted host-trust references are
available, not missing authority. The reported prerequisite PASS remains
owner-attributed: inspected script scope is not independently inspected execution
or current deployment/rollback proof. This task does not refresh private evidence,
earlier access denials, operational installation or cloud state.

### RP-S3 evidence joins and execution dependencies

| Boundary | Required evidence and existing owner |
|---|---|
| Initial-parent readiness | Existing ownership Developer supplies actual nonsecret resolver/Git/path/hash/root-matrix evidence or restores already-authorized bounded read access; originating Architect/Critic substantive acceptance precedes eight-path sibling runner writes. Designated integration Developer reconciles reviewed commits and actual loaded roots/bytes/hashes with durable Git accounting. Original E2E validates that exact join. DevOps independently completes current trust/inventory/rollback/effect preparation, exact-source/retained-suite/Linux hosting-package gates and serialized guarded release; G1-G4 must establish one final common bundle, both remote artifacts, private managed-identity Blob provenance, genuine Decision-1 and the completed non-held initial parent. Accepted blocked reports do not supply readiness. |
| Queue follow-up / AC2, G5 | Original DevOps uses the same private session file and completed parent, not a replacement or held parent. Both roles execute on both turns: compare actual parent and both children's hosted/framework identity fields and pinned versions; continuation fields may advance. Exactly two child creations across the pair, fresh invocation response IDs, current queue-plus-private-ingress requirements and stale-approval invalidation are required. Useful output and safe aliases are presentation, not proof. |
| Repeated calls / AC3 | Consume accepted offline architect -> blocked reviewer -> same architect revision -> same reviewer controls and both-role restored-history/fresh-history tests. Direct model continuation is separate from replayed briefs; do not relabel mocked calls live or reimplement accepted tests. Live AC1/AC2 remain independent obligations. |
| Supported recovery / AC4, G6 | Once the original parent is completed and non-held, use the retained local stop/resume script path and durable once-only marker. Independently observe the same pinned parent stopped/idle with advanced stop metadata before continuation. Verify original parent/both-child bindings, retained checkpoints and reconciled cumulative effects with no duplicate creates/sends. A known-response GET is not a new invocation. Missing confirmation or unknown effects hold execution; no repeated stop, blind resend, hard kill or hard-crash claim. |
| Separate parent / AC4, G7 | DevOps creates a separate synthetic parent on the verified release only when its own source, trust, effect and resource prerequisites pass. Compare distinct child/history/artifact scope and exclusion of the first parent's requirements. This does not depend on successful recovery; serialize shared mutation without inventing a recovery dependency. Account-wide Blob Contributor means application-enforced isolation, not storage-RBAC or malicious-host isolation. |
| Delivery / AC6-AC9, G8 | Keep Screens H-K, README source path, useful current output and opt-in human stderr with unchanged stdout/parser. Private machine observations back a separate sanitized companion; no full identifiers, private roots, transcripts or evidence locators enter customer output/Git. Final exact-source/common-package checks, reviewed scoped feature push and durable integration or retained-branch accounting remain required. Record all AC/G outcomes, reproducible setup/command, exact final/rollback bindings, limitations and positively identified new owned cleanup separately from historical cleanup uncertainty. Missing proof yields BLOCKED, never customer-ready. |

### Observation contract, not a new acceptance implementation

Consume `live_acceptance.validate_scenario_evidence()` and
`tests/test_scenario_evidence.py`, documented in
[design.md](design.md#offline-cross-scenario-evidence-assertions). The existing
private inputs `initial`, `followup`, `restart`, `isolated` and `stopped_session`
join per-scenario proof, scoped manifests, complete cumulative operations,
independent create/send captures, checkpoints and confirmed stop observations.
Capture completeness and association with actual scoped stores remain execution
owner obligations. Do not synthesize requests from journal intentions, deduplicate
duplicate sends, omit unresolved transitions or infer measured zeroes from
missing observations. Caller-supplied JSON passing assertions proves internal
consistency, not independent provenance or live capability.

Original E2E validates the reviewed operational join through local scripts;
original DevOps owns actual collection, serialized release and live acceptance.
Scrum retains contract-first decomposition, minimal dependencies, named exclusive
resources for shared CLI/transport/mount/publication mutation and assignment of
Git reconciliation. Inventory remains independent of runner coding. No substitute
agents, extra approval stage, GitHub Actions or deployment occurs here.

### Dispositions and bounded architecture handoff

Preserve `["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-LAB-OWNERSHIP/AssignedWorkDeveloperLoop","lab-ownership-review-evidence-access"]`:
actual evidence and substantive originating acceptance remain required; do not
repeat denied probes or substitute summaries/trust receipts. Preserve accepted
source checks under
`["yaml-loops-v1:sprint/1/RP-S1/task/RP-S1-CURRENT-SOURCE-CHECKS/AssignedWorkDeveloperLoop","current-source-checks-completion-status"]`
and accepted FAIL reporting under
`["yaml-loops-v1:sprint/1/RP-S1/EndToEndTestLoop","e2e-report-completion-status"]`.
Keep bounded DevOps reports closed under
`["yaml-loops-v1:sprint/1/RP-S1/DevOpsWorkLoop","devops-bounded-assessment-completion-status"]`
while actual cloud-pass obligations remain under
`["yaml-loops-v1:sprint/1/RP-S1/DevOpsWorkLoop","devops-exact-release-cloud-pass"]`.
Upstream Architecture/UX/ReleasePlan and prior sprint design/architecture,
review and retrospective agreements remain closed within their originating
boundaries; no votes transfer to this RP-S3 architecture loop. No disposition
is superseded or actual acceptance failure waived.

The cumulative design and current [coordinator](requirements/coordinator/architecture.md),
[specialists](requirements/specialists/architecture.md) and
[client/release](requirements/client-release/architecture.md) slices are complete
for original Product Owner, Critic and Red Team assessment. Their current RP-S3
votes are not yet supplied. AC1-AC9/G1-G8 remain unestablished as a release;
preserve UNKNOWNs, held parents, rollback assets, unrelated work, originating
stops and no-progress history. Documentation changes are not runtime progress.

<a id="current-rp-s2-ownership-evidence-exact-execution-join-and-initial-collaboration-october-20-2026"></a>

## Historical RP-S2: ownership evidence, exact execution join and initial collaboration (October 20, 2026)

Current sprint is **RP-S2: supported repair and exact three-role remote
collaboration**. Inspected clean authorized feature baseline
`76c797b509f0e8ee53d11ce1fbc275d4ad8ccd59`, containing current RP-S2
SprintDesign. Consume accepted RP-S1 cumulative/tier architecture
`302d8866d3c4f4c4d61b7c63c7f4d24196da664d`, source-check handoff
`b74b84edb6c05fb4dc7f58ba7f88925e2402ddc9`, SprintReview
`350352282f6defafc777dff5c6748d7fb2da3b59` and retrospective
`30c4a534bad1aa38b6b8f46a246c9b84262ecf18`. RP-S1 is completed workflow
history, not a successful live release. Earlier overlays below retain their
original attribution; this section governs the current sprint mapping.

### Retained holistic design

Keep exactly three hosted roles and the existing coordinator's explicit
begin/route/execute/publish sequence. Parent-scoped manifest child lookup,
restored remote `AgentSession` and pinned versions preserve each specialist's
binding; each role separately restores `specialist_history_v2` for model
continuation. Conversation history, workflow checkpoints, immutable artifacts
and fenced write-ahead effects remain separate state concerns. Retain exact
prerequisite/producer/version/revision/hash acceptance, trusted receiver
equality, coordinator ETag/fencing, calibrated Decision-1 after deterministic
gates and unknown-effect holds. No framework rewrite, generic session manager,
fourth service, public schema, CLI flag or duplicate fixture implementation.

### Current blocker and contract-first execution joins

| Boundary | Required handoff and existing closing owner |
|---|---|
| Ownership evidence before runner writes | Under `["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-LAB-OWNERSHIP/AssignedWorkDeveloperLoop","lab-ownership-review-evidence-access"]`, the existing Developer recovers actual nonsecret sibling resolver contents, attributable branch/HEAD/base, eight-path statuses, owner-specific hashes with line-ending explanation and source-bound matched/crossed-root results through the approved external handoff, or restores already-authorized read access. Original Architect/Critic substantive acceptance remains required. Supplied writer/integration designations resolve coordination only; qualified report agreement does not enable writing. Do not repeat denied inspection or substitute reconstructed source, historical trust receipts or another summary. |
| Bounded retained runner | After substantive acceptance, Developer implements only the existing eight-path sibling assignment. Preserve `LAB_TOOL_OWNER_MISMATCH`, competing-owner rejection, scenario/source/package/version checks before parent creation, architect-before-reviewer order, exact-response recovery and unknown-effect holds. Negative fixtures measure zero create/send at rejected preparation boundaries; absent observations do not imply zero effects. No live path selection is claimed by offline tests. |
| Reviewed source to actual loaded source | Designated integration Developer reconciles reviewed application, runner and necessary operational-wrapper commits on authorized feature branches, preserving unrelated dirty/staged canonical work. Record actual loaded roots, bytes/hashes, matched-root success and crossed-root rejection tied to those bytes. Sibling registration, clean Git or a runner commit does not install the operational wrapper. Keep root guards; unresolved installation is not execution-ready. Record task/branch/commit/reason for retained abandoned work durably on the feature branch; preserve those branches. |
| Original E2E readiness | Validate the exact subsequent reviewed join through local repository scripts. Accepted application-only checks and the completed accurate predeployment FAIL report remain closed; neither establishes operational integration. Consume accepted tests rather than reimplementing them. |
| Independent DevOps preparation and release join | Current strict trust, validated sole-target context, deployed/rollback inventory and effect reconciliation are independent of offline coding. After the implementation/E2E join and actual preparation, original DevOps passes exact-source application/repository/retained-tooling, Linux/amd64/hosting-Python and exact-package gates, then uses the serialized guarded publisher for exactly three existing roles. A metadata receipt or mixed diagnostic bundle is not final G1. |

Accepted fingerprint/reference inputs are supplied; use them through retained
strict tooling rather than seeking renewed trust authority. Current transport
and rollback availability still require actual verification. No private
ownership evidence, resolver access, cloud state or receipt authentication was
refreshed in this architecture task. The supplied latest ownership outcome
remains incomplete and runner writing remains blocked. This is the existing
evidence-access closing condition, not a newly invented approval stage or a
request for expanded user authority.

### Supported identity decision and RP-S2 exit

Neither A2A/authentication correction nor specialist-only `x-ms-user-identity`
delegation is live-selected. Choose the smallest supported path only through
the retained finite scripted decision contract. Necessary chosen-path
permissions are already authorized at documented exact scope/rationale, with
retained deterministic execution and readback; speculative grants, opaque
call-ID-as-user substitution, receiver-equality weakening and automatic
fallback remain excluded. Preparation failure leaves receivers unreached;
observed rejection identifies the reached receiver boundary; uncertain effects
remain held and are not retried to produce a decisive-looking result.

Observe trusted architect ingress before reviewer dispatch, then independently
prove reviewer ingress using exact current immutable prerequisites. Selection
alone is not the sprint exit. G1-G4 additionally requires three healthy exact
versions on one verified common bundle, actual coordinator acceptance of both
roles' artifacts, private managed-identity Blob provenance and genuine
Decision-1 with deterministic final gates. Original DevOps owns those live
observations. Unresolved identity selection does not stop remaining artifacts,
but an actionable unresolved report cannot satisfy this live sprint goal.

Only an actual completed, non-held initial parent on that verified bundle
enables RP-S3's queue follow-up and supported once-only confirmed compute
stop/resume. Preserve parent/both-child hosted/framework bindings and pins,
fresh responses, exactly two child creations across the initial/follow-up
pair, current requirements and stale-approval invalidation. Retain accepted
four-call revision and direct-history/fresh-history controls as offline proof.
Separate-parent isolation remains independent of successful recovery and needs
distinct real child/history/artifact scope. Account-wide Blob Contributor
policy provides application-enforced, not storage-RBAC or malicious-host,
isolation. Preserve historical UNKNOWNs, held parents, rollback assets,
unrelated work and historical cleanup uncertainty; AC1-AC9/G1-G8 remain intact.

### Tier handoff and agreement scope

Current slices are [coordinator](requirements/coordinator/architecture.md),
[specialists](requirements/specialists/architecture.md) and
[client/release](requirements/client-release/architecture.md).
Scrum retains decomposition, minimal dependency edges, named exclusive resources
for actual shared mutation and Git reconciliation assignment. No task is
redispatched here. Original E2E and serialized DevOps retain their original
execution gates, using local scripts rather than GitHub Actions.

The five prior completion dispositions for Architecture, UX, ReleasePlan,
RP-S1 SprintDesign and RP-S1 SprintArchitecture remain confined to their exact
originating accepted handoffs. In particular,
`["yaml-loops-v1:sprint/1/RP-S1/SprintArchitectureLoop","sprint-architecture-completion-status"]`
closes RP-S1 only; its votes do not transfer to this RP-S2 loop.
Preserve accepted source checks and E2E FAIL reporting under their originating
completion references. Preserve the two distinct DevOps references
`["yaml-loops-v1:sprint/1/RP-S1/DevOpsWorkLoop","devops-bounded-assessment-completion-status"]`
and `["yaml-loops-v1:sprint/1/RP-S1/DevOpsWorkLoop","devops-exact-release-cloud-pass"]`:
bounded reports remain complete while enclosing cloud-pass remains unmet.
No disposition is superseded or acceptance criterion waived.

Architect considers this documentation handoff complete for original Product
Owner, Critic and Red Team review. Current RP-S2 reviewer votes are not supplied.
This task changes only architecture/navigation documentation; it claims no new
runtime, test-fixture, ownership, integration, identity-selection or live
capability progress. Documentation validation is reported in the owner handoff,
not inferred from earlier overlays' test results.

<a id="current-rp-s1-accepted-recovery-inputs-and-continuity-handoff-october-20-2026"></a>

## Historical RP-S1: accepted recovery inputs and continuity handoff (October 20, 2026)

This invocation selects **RP-S1: evidence-ready source and understandable
continuity**. No assignments, completed sprints or separate blocked-decision
list were supplied. Inspected clean feature-branch baseline
`a1e85442a90a2333bedd6e4beed1d8d849a68ad9`. Consume accepted Architecture
`25d182245a1bb40b842f5787196bd8f8244c4a7d`, UX
`c5e7189252886a653daa42cbf9021f0cf59691b2`, ReleasePlan
`0d0f17b928ba99517551ba20a0c0201801148d9d` and SprintDesign at that baseline.
Earlier overlays below are retained history; their sprint selection, votes,
execution counts and stops are not current observations.

### Holistic design and current criterion joins

Keep exactly three hosted roles, pinned MAF/Foundry and the existing explicit
coordinator begin/route/execute/publish sequence. Parent-scoped manifest
`children.get(role)` creates or reuses hosted/framework bindings and immutable
version pins. `RemoteAgents.invoke()` restores the child's `AgentSession`;
each specialist separately restores `specialist_history_v2` before its model
call. Conversation/model history, workflow checkpoints, immutable artifacts
and fenced write-ahead effects are distinct state responsibilities.

| RP-S1 obligation | Retained contract and evidence handoff |
|---|---|
| Two user turns | Compare actual parent and both roles' hosted/framework identity fields and pinned versions, not entire evolving serialized sessions. Both roles execute on both turns; exactly two children are created across the pair. New invocations have fresh responses, queue follow-up preserves private ingress, and current revisions invalidate stale approval. |
| Repeated orchestration | Preserve controlled architect -> blocked reviewer -> same architect revision -> same reviewer fixtures, both-role binding checks and fresh responses. Existing specialist load/model/store tests and identical-brief fresh-history controls prove continuation separately from replayed requirements. These remain offline controls. |
| Customer clarity | Consume accepted SprintDesign Screens A-D, README goal/diagram/source path and useful `--native --view human` stderr. Default stdout, delegation/result records and acceptance parsing stay unchanged; safe aliases alone prove nothing about bindings. |
| Exact-source checks and supported-remedy handoff | Existing Developer checks cover retained source/fixtures; original E2E owns formal joined-source validation. An actionable unresolved identity finding can satisfy bounded research, never live ingress or release acceptance. Report the reached boundary, missing evidence and existing closing action. |

No rewrite, generic session manager, fourth service, framework/dependency,
public schema, CLI flag or duplicate fixture/presentation implementation is
needed. Preserve trusted receiver equality, exact immutable prerequisites,
producer/version/revision/hash checks, coordinator ETag/fencing, calibrated
Decision-1 after deterministic gates and explicit unknown-effect holds.

### Blocker resolution boundaries and downstream closing actions

Accepted Architecture reports matching supplied host-trust references and
successful direct sibling Git inspection, but incomplete resolver inspection
after denied reads. These are attributed inputs, not refreshed here.
**Accepted trust input is supplied; current strict transport is unverified.**
DevOps must use that accepted fingerprint and evidence reference through the
retained strict wrapper, not request them again or replace them with a newly
observed key. Supplied ownershipRecoveryDefaults resolve missing writer
acknowledgement/integration designation only. Existing Developer completes
point-in-time eight-path sibling ownership/resolver evidence and original
ownership review before runner writes; never write the dirty canonical lab.

The designated Developer joins reviewed application, runner and actually
loaded operational wrapper bytes with matched roots, exact hashes and durable
task/branch/commit accounting. Preserve `LAB_TOOL_OWNER_MISMATCH`: a clean
sibling or committed runner is not operational installation. No guard bypass,
shared branch switch, uncertain resend or adoption of held parents is allowed.
Independent application checks and offline runner coding do not depend on live
inventory; DevOps trust/context/inventory can proceed independently of coding.

Neither A nor specialist-only B is live-selected. Evaluate the smallest
supported candidate through the retained finite scripted decision contract.
Reject source/root/scenario/package/version mismatches before creating a
parent; preparation failure is not receiver failure. Prove architect ingress
and trusted equality before reviewer dispatch, then prove reviewer ingress
independently. Necessary chosen-path permissions are already authorized at
documented exact scope/rationale through retained mechanisms/readback; no
speculative grant, call-ID-as-user substitution or equality relaxation.
Unresolved selection must not halt remaining artifacts.

Scrum retains decomposition, minimal dependencies, exclusive-resource planning
and integration assignment. Original E2E uses local repository scripts.
Original DevOps serializes publication/transport/profile/mount/stage mutation
and owns exact-source application/repository/retained-tooling and actual
Linux/amd64/hosting-Python package gates, guarded publication and live acceptance.
RP-S2 needs common-bundle G1-G4 and a completed non-held initial parent; only
then does RP-S3 continue that parent's queue turn and once-only confirmed
supported stop/resume. Separate-parent isolation needs the final release, not
successful recovery first. Preserve AC1-AC9/G1-G8, rollback assets, historical
UNKNOWNs, held parents and historical cleanup uncertainty. Account-wide Blob
Contributor isolation is application-enforced, not storage-RBAC or malicious-host
isolation. This design creates no new approval stage or release waiver.

### Tier outputs and bounded agreement

Current RP-S1 slices in [coordinator](requirements/coordinator/architecture.md),
[specialists](requirements/specialists/architecture.md) and
[client/release](requirements/client-release/architecture.md) implement this
mapping. Apply only the supplied originating completion dispositions:
`["yaml-loops-v1:ArchitectureLoop","architecture-completion-status"]`,
`["yaml-loops-v1:UserExperienceLoop","ux-completion-status"]`,
`["yaml-loops-v1:ReleasePlanLoop","release-plan-completion-status"]` and
`["yaml-loops-v1:sprint/1/RP-S1/SprintDesignLoop","sprint-design-completion-status"]`.
Those accepted handoffs stay closed; their votes do not transfer to this
SprintArchitecture Loop or originating ownership review.
Architect agrees with this cumulative/tier design for original Product Owner,
Critic and Red Team review. Current-loop reviewer agreement is not yet supplied.
No fresh private evidence, sibling resolver, cloud, deployed binding, identity
selection, push or release acceptance is claimed by this mapping.

### Verification of this handoff

Existing absolute lab Python 3.12.10 ran `Test-Demo.ps1` with explicit lab
root: dependency checks, **204 offline tests in 45.916 seconds**, compilation
and script exit 0. `scripts/Test-Repository.ps1` passed current index,
79-public-file boundary, JSON/PowerShell/context and whitespace checks.
No dependencies were installed. No runtime or retained lab source changed;
full retained lab suite, Linux hosting-package checks, formal E2E and cloud
operations were not run. These repeated local checks are not new live progress.

<a id="current-rp-s3-live-continuity-recovery-isolation-and-truthful-delivery-october-20-2026"></a>

## Historical RP-S3: live continuity, recovery, isolation and truthful delivery (October 20, 2026)

Current sprint is **RP-S3**. Inspected clean application HEAD
`1f24c9a07277d2f5b111f83b186db3ad6a5257aa` on
`feature/customer-hosted-session-prototype`. Consume accepted RP-S2 cumulative
and tier architecture at `74130a8bbda12c32ac8e84523b93b8f5e09794c0`,
retrospective at `dd7728cb80b503883d96d3317a3dd5dee28f1c6e`, and RP-S3
SprintDesign at inspected HEAD. RP-S1/RP-S2 are completed workflow history,
not completed live release gates. This section is the current mapping; earlier
overlays retain their attributed observations and technical history.

### Retained system and actual entry handoff

Retain exactly three hosted roles: terminal -> coordinator MAF
begin/route/execute/publish -> remote architect and reviewer -> deterministic,
fenced acceptance. Parent-owned manifest child lookup, restored remote
`AgentSession`, pinned versions and each specialist's `specialist_history_v2`
remain distinct continuation links. Conversations/model history, graph
checkpoints, immutable artifacts and write-ahead effects are separate state
concerns. No rewrite, fourth service, session manager, history migration,
framework, public schema, CLI flag or comparison ledger is introduced.

Live follow-up requires an actual completed, non-held initial parent with
G1-G4 evidence for the exact final common bundle: three healthy pinned roles,
remote accepted artifacts, private managed-identity provenance and genuine
Decision-1 after deterministic gates. An agreed failure report or selected
identity path does not establish that handoff. Supplied RP-S2 outcomes establish
neither it nor a live-selected identity path; current continuation remains
**BLOCKED**, not an instruction to send into absent or held state.

The existing Developer completes substantive recovery-record reconciliation,
current eight-path sibling status and no-write Python/PowerShell matched-root
acceptance and mismatched-root rejection for originating Architect/Critic
ownership acceptance before runner writes. Supplied designations suffice for
coordination, not proof. Reviewed runner implementation and actual loaded
operational/source integration follow under their existing assignments.
Independently, established transport-owner/user coordination supplies the
previously accepted fingerprint/reference or exact private evidence locator;
original DevOps compares through retained strict tooling before current private
inventory. No renewed designation, trust replacement, repeated unattended denied
probe or dependency from offline coding to live inventory is introduced.

### RP-S3 cross-tier evidence joins

| Obligation | Required comparison and existing execution boundary |
|---|---|
| AC2 / G5: two user turns | Reuse the completed parent's private session file. Compare actual parent and both roles' hosted/framework identity fields and pinned versions; both roles run on initial and queue follow-up turns, with exactly two child creations across that pair and fresh response IDs for new invocations. Preserve private ingress and earlier requirements, add the queue, invalidate stale approval and accept only current immutable prerequisites, revisions, hashes and producers. |
| AC3: repeated orchestration | Retain controlled architect -> blocked reviewer -> same architect -> same reviewer fixtures, both-role binding assertions and direct load/model/store continuation with identical-brief fresh-history controls. These are accepted offline controls, not live success or a new fixture implementation assignment. |
| AC4 / G6: supported compute recovery | Use the existing durable once-only stop marker, supported stop and confirmed stopped/idle state before same-conversation continuation. Compare original parent/both children, pins, checkpoint/effect retention and actual sends. Known-response retrieval is not a new invocation. Unconfirmed/unknown effects stay held; never delete markers, resend or infer no duplicates from resumed output alone. This is not hard-crash recovery or exactly-once deployment. |
| AC4 / G7: separate-parent isolation | Use a separate synthetic parent and private session file; verify distinct actual parent/both-child bindings and artifact scope, exclusion of first-parent requirements and passing cross-scope rejection regressions. Filenames or aliases are insufficient. Isolation and recovery have no invented dependency on each other; their actual shared mutations remain serialized. |
| AC6-AC9 / G8: understandable truthful delivery | Retain README and Screens H-K, useful opt-in human stderr and unchanged machine stdout/parser. Supply sanitized comparison outcomes separately from private exact evidence. Require final exact-source/package checks, reviewed scoped feature push/accounting, actual final/rollback bindings, reproducible setup/demo command, newly owned cleanup and explicit historical uncertainty. Customer-ready requires every AC1-AC9/G1-G8, not report agreement. |

Compare stable identity fields, not entire serialized sessions: continuation
state advances. Replayed briefs, plausible memory prose, display aliases and
HTTP success cannot prove hosted/framework continuity or model history.
Trusted receiver equality, specialist-only candidate delegation, immutable
prerequisites, coordinator ETag/fencing and unknown-effect holds remain intact.
Do not rekey specialist history, adopt held parents or substitute call IDs for
delegated identity. Account-wide Blob Contributor isolation remains
application-enforced, not storage-RBAC or malicious-host isolation.

### Exact-source execution and original-owner handoff

Consume the existing `live_acceptance.validate_scenario_evidence()` and
`tests/test_scenario_evidence.py` assertions for private scenario snapshots,
cumulative operation transitions and independently observed create/send counts.
They perform offline comparisons, not collection or cloud execution. Accepted
source checks and the revision-bound outgoing audit remain attributed accepted
inputs; no duplicate implementation or status-only rerun is requested.
Designated Developer integration supplies reviewed joined commits, actual loaded
roots/bytes/hashes and joined checks to subsequent formal E2E. Any concrete
missing execution join belongs to existing Developer/Scrum decomposition.

Original DevOps retains current strict trust/inventory, exact-source application,
repository and affected retained-tooling checks, Linux/amd64/hosting-Python
package validation, immutable source/package joins, fresh previews and guarded
publication before live gates. Use deterministic local repository scripts,
not GitHub Actions. Serialize publication, transport, CLI, mount and package
mutation; architecture dispatches no work. Preserve rollback assets, historical
UNKNOWN publications, held parents, unrelated dirty/staged work and historical
cleanup uncertainty. New owned cleanup cannot certify historical cleanup.

The supplied latest DevOps boundary is shellId 389, outer exit 2,
`HOST_TRUST_EVIDENCE_REQUIRED`; accepted RP-S2 E2E remains predeployment FAIL.
These are attributed reports, not fresh observations here. Structural recovery
JSON checks, historical trust strings and authenticated ARM prerequisites do not
prove substantive ownership, independent host trust, actual operational
installation or live specialist ingress. Bounded blocked reports can complete
their reporting contracts without satisfying DevOps cloud-pass.

Apply exact prior references
`["yaml-loops-v1:sprint/2/RP-S2/SprintArchitectureLoop","rp-s2-architecture-close-completed-deliverable"]`,
`["yaml-loops-v1:sprint/3/RP-S3/SprintDesignLoop","rp-s3-design-close-completed-deliverable"]`
and
`["yaml-loops-v1:sprint/2/RP-S2/SprintRetroLoop","rp-s2-retro-close-agreed-deliverable"]`
only within their accepted boundaries. They supply no current RP-S3 architecture
votes, ownership acceptance or release waiver; other accepted handoffs stay
closed. Material changed contracts return to existing Architect-advised
Product Owner/Scrum reconciliation, not weakened acceptance.

Architect doneWhen is this current cumulative mapping and the three linked
tier updates committed for original Product Owner/Critic/Red Team review.
Current RP-S3 architecture votes are not yet supplied. Scrum retains
contract-first decomposition, minimal dependencies, resource coordination and
Git-reconciliation assignment. Designated integration reconciles task commits
to authorized feature branches or retains named branches with task IDs, commit
IDs and abandonment reasons in a feature-branch commit message. This design
does not assert successful deployment, runtime progress or customer readiness.

<a id="current-rp-s2-supported-repair-and-exact-remote-collaboration-october-20-2026"></a>

## Historical RP-S2: supported repair and exact remote collaboration (October 20, 2026)

Current sprint is **RP-S2**; RP-S1 is supplied as completed workflow history,
not a successful deployment. Inspected clean application HEAD
`cf017c969720eda2dce6f2cec09f4fa142cbab2d` on
`feature/customer-hosted-session-prototype`. Consume the accepted RP-S1
cumulative/tier architecture at `c888336b1741dd5cbf77f0209749620949301adb`,
retrospective at `006574e6d664ec21d38a86c8e1f1cf15e162f89e`, and RP-S2
SprintDesign at inspected HEAD. Older overlays below retain technical/audit
history; this section selects the current sprint without reopening those
accepted handoffs or claiming fresh private observations.

### Retained holistic design and current acceptance joins

Exactly three hosted roles remain: terminal -> coordinator MAF
begin/route/execute/publish -> remote architect and reviewer -> fenced
acceptance. Parent-scoped manifest lookup, restored remote `AgentSession`,
pinned role versions and both specialists' `specialist_history_v2` remain
distinct continuation links. Conversations, checkpoints, immutable artifacts
and write-ahead effects retain their separate responsibilities. Preserve
both-role two-turn/four-call/history controls and parser-safe human stderr;
no rewrite, additional service, schema, framework or duplicate implementation.

| RP-S2 obligation | Closing owner and evidence boundary |
|---|---|
| Ownership and loaded roots | Existing Developer substantiates named recovery evidence, current eight-path sibling status and matched/mismatched resolver behavior; originating Architect/Critic acceptance precedes runner writes. Supplied writer/integration designations suffice for coordination, not acceptance. |
| Reviewed finite runner | Existing Developer implements the retained interface and offline rejection/unknown/root controls after ownership acceptance. Offline coding consumes agreed fixtures, not live inventory. Preserve `LAB_TOOL_OWNER_MISMATCH`; a sibling commit is not operational installation. |
| Operational/source join | Designated Developer integrates reviewed application, runner and required wrapper bytes at actual loaded roots, records exact commits/hashes/root mapping, reruns joined checks and records scoped push outcomes. Original formal E2E validates that join. |
| Strict trust and current inventory | Original DevOps independently compares the existing accepted host fingerprint via retained tooling, validates sole-target context and observes current three-role versions/packages/identities, rollback and held effects. ARM readiness and another task's historical receipt inspection do not establish this gate. |
| Exact release and actual G1-G4 | Original DevOps runs retained application/repository/tooling and Linux/amd64/hosting-Python checks for exact source/package, fresh previews and guarded publication. Actual common bundle, remote acceptance, private managed-identity provenance and genuine Decision-1 remain separate required proofs. |

The supplied RP-S1 source-check and E2E reports attribute 204 offline passes
to their executions; E2E remains **FAIL**. Supplied DevOps reporting attributes
an exit-2 `HOST_TRUST_EVIDENCE_REQUIRED` stop after partial authenticated ARM
inventory, without transport startup or current private deployment bindings.
Its recovery-file inspection is historical evidence, not transferable ownership
acceptance or a fresh observation here. The originating ownership report still
requires permission-capable bounded sibling/resolver/evidence reads and its
original review. Use the already-sufficient designations; do not request them
again, reset stopped history or treat session-specific access as blanket denial.

### Identity decision and effect boundary

Neither A nor B is live-selected. A requires an evidenced supported
authentication/configuration correction and matching reviewed source. Retained
specialist-only B is candidate code, not proof of delegated ingress. The finite
runner rejects source/root/scenario/package/actual-version mismatches before
parent creation. Preparation rejection is not receiver failure and supplies no
invented zero-send counts. Verify architect trusted ingress and receiver
principal equality before reviewer dispatch; reviewer needs independent evidence.
An unknown effect is held and observed, never automatically resent or retried
under the other identity path. No call-ID-as-user substitution, receiver-equality
relaxation, held-parent adoption or model-history rekey is allowed.

Necessary chosen-path lab permissions remain pre-approved only at documented
exact scope/rationale through retained scripts and readback; speculative grants
are not a remedy. Identity selection alone cannot pass G1-G4. A bounded
prerequisite-stop or actionable unresolved report may complete its reporting
contract while DevOps cloud-pass and customer readiness remain unmet.

### Handoff, cumulative obligations and disposition boundaries

Scrum retains task decomposition, minimal dependencies, shared-resource
serialization and Git-reconciliation assignment; no tasks are dispatched here.
Developer integration must reconcile task commits to authorized feature
branches or retain named branches with task/commit IDs and abandonment reason
in a feature-branch commit message. Preserve unrelated dirty/staged canonical
work; no branch switching, broad staging or root-guard bypass.
Original E2E and DevOps execute deterministic local scripts, not GitHub Actions.
Actual publication/profile/transport/mount/stage mutation remains serialized.

RP-S3 consumes actual G1-G4 and a completed non-held initial parent for live
two-turn continuity, once-only confirmed supported compute stop/resume with
checkpoint/effect preservation, separate-parent isolation and truthful delivery.
It does not consume an agreed failure report as a successful initial turn.
Preserve every AC1-AC9/G1-G8, historical UNKNOWN, held parent, rollback asset
and historical cleanup uncertainty. Account-wide Blob Contributor isolation
remains application-enforced, not storage-RBAC or malicious-host isolation.

The current RP-S2 sections in the linked
[coordinator](requirements/coordinator/architecture.md),
[specialists](requirements/specialists/architecture.md) and
[client/release](requirements/client-release/architecture.md) carry this join.
Apply exact prior references
`["yaml-loops-v1:sprint/1/RP-S1/SprintArchitectureLoop","sprint-architecture-close-completed-deliverable"]`
and
`["yaml-loops-v1:sprint/2/RP-S2/SprintDesignLoop","rp-s2-design-close-completed-deliverable"]`
only to their accepted RP-S1 architecture and RP-S2 design respectively.
Upstream Architecture/UX/ReleasePlan, RP-S1 source/E2E/review/retro closure
dispositions likewise remain bounded; no votes transfer to this architecture
or originating ownership acceptance. Architect agrees with this committed
design for original Product Owner/Critic/Red Team review; current votes and
checks are reported separately. No private inspection, live identity decision,
cloud operation, deployment or substantive runtime progress is claimed here.

<a id="current-rp-s1-accepted-inputs-and-evidence-ready-continuity-october-20-2026"></a>

## Historical RP-S1: accepted inputs and evidence-ready continuity (October 20, 2026)

The supplied sprint is **RP-S1: evidence-ready source and understandable
continuity**; no assignments, completed sprints or additional blocked-decision
list were supplied. Inspected clean application HEAD
`00b228bb78842df3289008be3c99ad6a88d3efe4` on
`feature/customer-hosted-session-prototype`. Consume accepted Architecture
`45318a50098c44843643ef1a7c5479edb4dfbd38`, UserExperience
`b7aa978584b144c1cb485bec5b54e9c8da989964`, ReleasePlan
`2f22642e6f68d841c7ef40097fe1299ccd366dd8` and SprintDesign at that HEAD.
Older RP-S1/RP-S2/RP-S3 overlays retain technical and audit history, not the
current sprint selection, fresh observations or task dispatch.

### Retained design and RP-S1 criterion map

Exactly three hosted roles use the existing pinned Python, MAF/Foundry,
Pydantic, private managed-identity Blob and PowerShell/Python/WSL tools.
Terminal -> coordinator begin/route/execute/publish -> remote architect and
reviewer -> deterministic, fenced acceptance remains the end-to-end flow.
Parent-owned manifest lookup creates or reuses each role's hosted/framework
binding and pinned version; remote `AgentSession` restoration and each
specialist's `specialist_history_v2` load are distinct continuation links.
Conversations retain history, checkpoints retain graph position, immutable
artifacts retain exact work and the write-ahead effect journal reconciles
sends. Responses and revisions advance without replacing session identities.

| RP-S1 criterion | Existing implementation/fixture boundary and handoff |
|---|---|
| Both-role two-turn proof | Retain parent and both specialists' hosted/framework identities and pins, exactly two child creations, both roles on both turns, fresh invocation responses, updated requirements and stale-approval invalidation. Compare identity fields, not entire serialized continuations. |
| Repeated orchestration and model history | Retain ordered architect -> blocked reviewer -> same architect -> same reviewer fixtures and both roles' actual load/model/store paths, persisted-value snapshots and identical-brief fresh-history controls. Replayed requirements are not model-history proof; fixtures remain offline. |
| Understandable continuity with unchanged parsing | Consume accepted README and SprintDesign Screens A-D, useful opt-in human stderr, safe aliases and unchanged machine stdout/parser. Aliases cannot establish actual binding equality. Required application/repository checks remain downstream source gates. |
| Supported decision or actionable unresolved handoff | Retained specialist-only B is candidate-only, not live selection. A needs an evidenced supported authentication/configuration correction and reviewed source. Report preparation versus receiver boundary, reached/unreached roles, missing evidence/remedy, existing closing owner and exact next action; do not invent live success. |

Trusted parent/receiver equality, exact immutable prerequisites, producer/
version/revision/hash checks, coordinator ETag/fencing, calibrated Decision-1
after deterministic gates and unknown-effect holds remain mandatory. No new
service, framework, schema, public event, session manager, UI, runtime selector
or duplicate fixture/presentation implementation is introduced.

### Blocked decisions and minimal execution joins

The accepted Architecture records successful direct sibling Git inspection,
but incomplete resolver/loaded-root verification after denied reads. This is
attributed upstream evidence, not a fresh sibling observation here; older
blanket claims that all Git inspection was denied are not current status.
Supplied Developer writer/integration designations resolve coordination only.
Use them with the supplied recovery evidence in the existing ownership task,
not as ownership acceptance or a renewed request for user designation.

```text
supplied coordination + current owned-path/resolver verification
  -> originating ownership review -> eight-path sibling runner work
accepted application + reviewed runner + required actual operational bytes
  -> designated Developer integration -> original E2E joined-source validation
established strict trust + verified sole-target context -> current inventory
joined source + inventory + exact Linux/package/version gates
  -> original DevOps guarded publication and finite decision -> live G1-G8
```

The existing Developer closes bounded resolver/loaded-root and owned-path
verification before originating review and runner writes. Keep the exact
eight-path allowlist and registered feature sibling boundary from accepted
Architecture; never write the dirty canonical lab. Preserve
`LAB_TOOL_OWNER_MISMATCH`: sibling commits do not install canonical wrappers.
Integration must join reviewed source to actual loaded roots/hashes, preserve
unrelated dirty/staged work and record task/branch/commit accounting and scoped
push. A necessary root/guard contract change returns to existing
Architect-advised Product Owner/Scrum reconciliation, not a guard bypass.

Ownership does not gate independent application checks; private inventory is
not a runner coding prerequisite. DevOps independently closes established
strict host trust and current sole-target inventory. Another role's receipt
reads, current known-host content or historical metadata cannot supply those
observations. Source/root/scenario/package/version rejection precedes parent
creation and is preparation, not observed receiver failure. Observe architect
trusted ingress/equality before reviewer dispatch; reviewer needs its own
evidence. Necessary chosen-path lab permissions remain pre-approved at exact
documented scope/rationale through retained scripts/readback, not speculative
grants. No call-ID-as-user conversion, equality relaxation, automatic fallback,
held-parent adoption or uncertain resend is permitted.

Scrum retains contract-first decomposition, minimal dependencies, integration
assignment and actual shared-resource coordination. Original E2E owns formal
integration; original DevOps owns exact-source Linux/amd64/hosting-Python
checks, guarded publication and cloud-pass through deterministic local scripts,
not GitHub Actions. Serialize publisher/profile/transport/mount/stage mutation
across runs; scheduler labels alone are not OS exclusion.

### Tier outputs, dispositions and completion boundary

The current RP-S1 sections in [coordinator](requirements/coordinator/architecture.md),
[specialists](requirements/specialists/architecture.md) and
[client/release](requirements/client-release/architecture.md) consume this map.
RP-S2 still requires actual common-bundle G1-G4 and a completed non-held initial
parent. RP-S3 retains live both-role two-turn continuity, once-only confirmed
supported compute stop/resume with checkpoints/effects and no duplicate sends,
distinct-parent child/artifact isolation and truthful exact-source delivery.
Account-wide Blob Contributor provides application-enforced isolation, not
storage-RBAC or malicious-host isolation.

Apply these exact supplied prior references only within their originating
accepted deliverables:
`["yaml-loops-v1:ArchitectureLoop","architecture-close-completed-deliverable"]`,
`["yaml-loops-v1:UserExperienceLoop","ux-close-completed-deliverable"]`,
`["yaml-loops-v1:ReleasePlanLoop","release-plan-close-completed-deliverable"]`,
`["yaml-loops-v1:sprint/1/RP-S1/SprintDesignLoop","sprint-design-close-completed-deliverable"]`.
None supplies this SprintArchitecture's Product Owner/Critic/Red Team votes,
originating ownership acceptance or live readiness. No upstream handoff is
reopened. Architect agrees with this cumulative/tier handoff for original
review; checks and current reviewer outcomes are reported separately.
No private receipt/resolver reinspection, lab change, identity selection,
deployment or cloud observation occurs here. Preserve all AC1-AC9/G1-G8,
UNKNOWN effects, held parents, rollback assets and historical cleanup uncertainty.

### Verification for this RP-S1 overlay

Existing absolute lab Python 3.12.10 ran `Test-Demo.ps1` with the explicit lab
root: dependency checking, **204 offline tests in 42.159 seconds**, compilation
and script exit 0. `scripts/Test-Repository.ps1` passed index,
**79-public-file** boundary, JSON/PowerShell/context and whitespace checks.
No dependency installation, retained lab source change, Linux hosting-package
check, formal E2E, cloud operation or push occurred. These repeated checks are
not new runtime progress or live acceptance evidence.

<a id="current-rp-s2-joined-execution-inputs-and-independent-trust-october-20-2026"></a>

## Historical RP-S2: joined execution inputs and independent trust (October 20, 2026)

This RP-S2 overlay consumes the supplied RP-S1 outcomes, retrospective
Architecture/UX/ReleasePlan updates at `a98410f479104a549fe6933df6eea3d4c6e6d132`
and accepted current SprintDesign at inspected clean application HEAD
`d558a721747ddea92a445b8bc45c786ba5c84664` on
`feature/customer-hosted-session-prototype`. Earlier overlays below are retained
technical and audit history, not fresh status or dispatch. RP-S1 reporting
closure is not RP-S2 execution acceptance.

### Architecture decisions carried forward, not reopened

Retain exactly three hosted roles: terminal -> coordinator's explicit MAF
begin/route/execute/publish flow -> remote architect/reviewer -> fenced acceptance.
The parent manifest creates or reuses each role's hosted/framework session and
pinned version; remote `AgentSession` restoration and each specialist's
`specialist_history_v2` load independently preserve continuation. Responses and
requirements/candidate/review revisions advance, bindings do not. Conversations,
checkpoints and immutable artifacts/write-ahead effects remain distinct.
Retain exact prerequisites, stale-approval invalidation, trusted receiver
principal equality, private managed-identity Blob and genuine Decision-1 after
deterministic gates. No new session abstraction, service, dependency, schema,
public event, UI or identity selector is required.

The retained application candidate is specialist-only B, not selected-B.
A requires an evidenced supported authentication/configuration correction and
its own reviewed source; relabeling the B package cannot select A. The finite
runner must reject source/root/scenario/package/actual-version mismatch before
parent creation. Local preparation rejection is not receiver failure.
Architect trusted ingress/receiver success precedes reviewer dispatch; each
role needs its own evidence. Neither ingress nor identity selection alone
proves accepted artifacts, private MI provenance or complete common-bundle G1-G4.
Necessary chosen-path lab permissions remain pre-approved at exact evidenced
scope/rationale using retained deterministic scripts and readback, not speculative
grants. No opaque call-ID conversion, equality relaxation, automatic fallback,
held-parent adoption or uncertain-effect replay is allowed.

### Two independent preparation lanes and the source-to-live join

```text
supplied designations + exact recovery evidence + current sibling/root proof
  -> original ownership acceptance -> reviewed eight-path runner work
accepted application + reviewed runner + required loaded operational wrappers
  -> designated Developer integration -> original E2E exact joined-input checks
previously accepted fingerprint/reference + verified sole-target context
  -> retained strict-trust checks -> authenticated private inventory
reviewed joined inputs + current inventory + final Linux/package/version gates
  -> original DevOps guarded publication and finite ingress decision
  -> actual common-bundle G1-G4 -> non-held initial-parent handoff to RP-S3
```

| Existing boundary | Supplied outcome, missing proof and closing action |
|---|---|
| Ownership before runner writes | Supplied Developer writer/integration designations resolve coordination only. Originating exact-file/sibling inspections were denied; registration is not current safe-writing proof. Developer resumes already-authorized bounded reads in a permission-capable session, substantiates branch/base/status, eight owned paths and loaded resolver behavior, then returns to original Architect/Critic review. No write probe, checkout recreation or repeated designation request. |
| Strict trust before private inventory | DevOps reports ARM/context/model readiness and exit 1 at `HOST_TRUST_EVIDENCE_REQUIRED`. These do not establish SSH/private ingress or current deployed/rollback/held-effect inventory. DevOps recovers the previously accepted ED25519 comparison value and acceptance reference from an exact private locator, then runs retained strict-trust/read-only inventory scripts. Current known-host content is not independent acceptance; do not replace trust. |
| Reviewed source at actual loaded roots | Developer integrates reviewed task commits and every required operational-wrapper delta against exact loaded paths/hashes, preserves unrelated work and records task/branch/commit accounting and scoped push. Sibling wrapper commits are not canonical installation. Preserve `LAB_TOOL_OWNER_MISMATCH`; the dirty canonical lab remains unwritable. An alternative operational root is not selected without all existing settings/profile/registry/stage/source guards passing; a necessary guard/location contract change returns to existing Architect-advised PO/Scrum reconciliation. |
| Joined validation and guarded execution | Original E2E validates the exact reviewed joined inputs when available. Original DevOps joins current inventory and held-effect reconciliation to exact-source Linux/amd64/hosting-Python, common-package/version checks, guarded publication and actual G1-G4. Only a completed non-held compatible initial parent can enter RP-S3 continuity/recovery. |

These are existing contracts and closing owners, not new tasks or approval
stages. Ownership does not gate independent application checks; inventory is
not a runner coding prerequisite. Another role's successful historical receipt
inspection does not supply originating ownership acceptance. Historical hashes,
offline checks and reported ARM observations remain attributed, not freshly
authenticated by this architecture turn. Private evidence stays outside Git.

Scrum retains contract-first assignment, minimal dependencies, Git reconciliation
and actual shared-resource coordination. Original DevOps serializes publisher,
CLI profile, private transport, mount and package-stage mutations across runs;
scheduler labels do not provide OS/cross-run exclusion. E2E and DevOps execute
through retained local scripts with explicit roots, never GitHub Actions.

### Cumulative tier handoff and completion boundary

| Tier | Current RP-S2 handoff |
|---|---|
| [Coordinator](requirements/coordinator/architecture.md#current-rp-s2-joined-execution-boundary) | Retain accepted two-turn/four-call fixtures, both-role bindings and pinned versions, exactly two children, fresh responses, current prerequisites and stale-approval invalidation. Integrate exact reviewed source; preparation success does not prove remote acceptance. |
| [Specialists](requirements/specialists/architecture.md#current-rp-s2-trusted-ingress-boundary) | Retain both real five-stage history paths, persisted-value/fresh-history controls and known-response zero-send recovery. Observe trusted ingress, receiver equality and private immutable output provenance separately for both roles. |
| [Client/release](requirements/client-release/architecture.md#current-rp-s2-trust-and-release-join) | Retain accepted README, Screens F/G, useful opt-in human stderr, safe aliases and unchanged stdout/parser. Report completed bounded assessments separately from unmet execution gates, then hand actual final/rollback bindings and non-held initial scope to RP-S3. |

Apply `["yaml-loops-v1:sprint/1/RP-S1/SprintArchitectureLoop","sprint-architecture-close-agreed-deliverable"]`
only to the accepted RP-S1 architecture; no duplicate implementation or renewed
RP-S1 review is requested. Apply
`["yaml-loops-v1:sprint/2/RP-S2/SprintDesignLoop","rp-s2-sprint-design-close-agreed-deliverable"]`
only to current design acceptance. The retrospective closure under
`["yaml-loops-v1:sprint/1/RP-S1/SprintRetroLoop","sprint-retro-close-agreed-deliverable"]`
supplies the evidence-attribution lesson, not runtime success.
The accepted E2E failure report remains closed under
`["yaml-loops-v1:sprint/1/RP-S1/EndToEndTestLoop","e2e-close-agreed-failure-report"]`;
future joined-input validation is still required. Preserve originating ownership
reference
`["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-LAB-OWNERSHIP/AssignedWorkDeveloperLoop","lab-ownership-review-evidence-access"]`
and its runner-write prohibition until its own evidence/review gates pass.

RP-S2 execution exit still requires actual G1-G4 on one final common bundle.
RP-S3 retains both-role two-turn continuity, once-only confirmed supported
compute stop/resume with checkpoints/effects and no duplicate sends, distinct
parent/child/artifact isolation and truthful customer delivery. Keep all
AC1-AC9/G1-G8, historical UNKNOWNs, held parents, rollback assets, unrelated work
and historical cleanup uncertainty. Account-wide Blob Contributor remains
application-enforced isolation, not storage-RBAC or malicious-host isolation.
Architect accepts this current cumulative/tier deliverable for original Product
Owner, Critic and Red Team review; RP-S1/upstream votes do not supply RP-S2 votes.
This overlay neither accepts ownership nor selects a remedy, deploys, or
certifies customer readiness.

## Current RP-S1 ownership-designation architecture (October 20, 2026)

This SprintArchitecture consumes agreed Architecture
`f72b0f3c1206418f08fc62a149e80f7c12c55e81`, UserExperience
`87253d3f5003d1d6f34724401b33c3b5ced2e64a`, ReleasePlan
`f9ccb6e85c80ce14f36e44cfb6e690fde0d81e80` and SprintDesign
`3103c14781b4509b2bd73ff1ba763cece0f1adf0`, the inspected clean application
baseline on `feature/customer-hosted-session-prototype`. No completed sprint,
assignments or separate blocked-decision list was supplied for this invocation.
Retain the cumulative RP-S1/RP-S2/RP-S3 technical contracts below; their dated
status and measurements are not current execution evidence.

### Resolved coordination input, unchanged technical contracts

Use the user's supplied Developer writer/integration designations and writer
acknowledgements as explicit coordination evidence with recoveryExceptionV1
for the original ownership review. Missing designation is no longer a human
input blocker. This does not establish accepted ownership, current sibling
exclusivity, transport trust, installed operational source or live readiness.
The exact originating boundary remains
`["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-LAB-OWNERSHIP/AssignedWorkDeveloperLoop","lab-ownership-review-evidence-access"]`.
Do not reset its stop or infer permission to write from this design.

Developer for `RP-S2-DECISION-RUNNER` owns only the eight lab paths listed in
[accepted release architecture](customer-prototype-architecture.md#current-ownership-designation-architecture-october-20-2026),
in the registered feature sibling only, never the dirty canonical lab.
Developer for `RP-S2-SOURCE-INTEGRATE` owns reviewed application/lab integration,
durable task/branch/commit accounting and scoped push. Preserve unrelated
dirty/staged work, explicit path ownership and `git commit --only`; no shared
branch switch, write probe, force-push or registration-as-ownership inference.
Scrum retains contract-first decomposition, minimal dependencies, actual shared
resource coordination and assignment of Git reconciliation; this is no dispatch.

Keep exactly three hosted roles and the explicit MAF begin/route/execute/publish
flow. The parent manifest's create-or-reuse lookup retains both specialists'
hosted/framework identities and pinned versions; remote `AgentSession`
restoration and each role's model-history load provide distinct continuation
links. New responses and current revisions advance without replacing children.
Conversations, checkpoints, immutable artifacts and fenced write-ahead effects
remain distinct. Retain exact prerequisites, stale-approval invalidation,
trusted principal equality, private managed-identity Blob, Decision-1 after
deterministic gates and UNKNOWN holds. No runtime/schema/dependency change,
generic session manager, extra service or identity selector is introduced.

### Cross-tier handoff and minimal execution joins

| Tier | RP-S1 retained contract and current coordination delta |
|---|---|
| [Coordinator](requirements/coordinator/architecture.md#current-rp-s1-ownership-designation-boundary) | Retain both-role two-turn/four-call binding, version, creation-count, fresh-response and current-artifact fixtures. Ownership acceptance gates runner writes; source/root/scenario/package/version rejection is preparation, not receiver evidence. |
| [Specialists](requirements/specialists/architecture.md#current-rp-s1-ownership-designation-boundary) | Retain both real five-stage history paths, value snapshots, identical-brief fresh-history negatives and exact-response zero-send recovery. Supplied designations do not establish ingress, receiver equality or live history for either role. |
| [Client/release](requirements/client-release/architecture.md#current-rp-s1-ownership-designation-boundary) | Retain accepted README, useful opt-in human stderr, safe aliases and unchanged stdout/parser. Separate coordination, original ownership acceptance, matched source, current trust/inventory and actual live evidence. |

```text
supplied designation + recovery evidence + current path verification
  -> original ownership acceptance -> bounded runner work
accepted application + reviewed runner + required operational source
  -> designated Developer integration -> original E2E scripted validation
existing strict trust + verified sole-target context -> fresh inventory
joined source + inventory + exact Linux/package gates
  -> original DevOps guarded publication/discriminator -> actual live gates
```

Ownership does not gate independent application checks; inventory is not a
coding prerequisite. Use the supplied recovery locator first when original
owners need evidence. Bounded read-only Git/sibling resolver inspection is
already authorized; any unavailable current observation needs its exact
existing-owner closing action, not another designation request. Architecture's
reported denied sibling inspection and historical receipts are consumed as
supplied observations, not independently reauthenticated here.

Preserve `LAB_TOOL_OWNER_MISMATCH` and explicit operational roots. Canonical
wrappers execute only with their canonical context and verified loaded bytes;
sibling fixes are not canonical installation. Integration must reconcile every
required operational-wrapper revision at its actual loaded path without writing
the dirty canonical lab or altering private settings. An alternative operational
root needs proof of existing settings/profile/registry/stage/source guards;
no unproven move is selected. Missing required source blocks execution. A new
writable location or changed root/guard contract returns to existing
Architect-advised PO/Scrum reconciliation, not a bypass or new approval stage.

Installed specialist-only B remains a candidate, not live selection. A requires
its own supported correction and reviewed source. The finite decision records
preparation rejection versus observed receiver failure and reached/unreached
roles; architect success does not establish reviewer entry. Necessary chosen-path
lab permissions remain pre-approved only at exact evidenced scope through
retained deterministic scripts and readback. No speculative grant, call-ID-as-user,
principal-equality relaxation, held-parent adoption or uncertain resend.
Original DevOps serializes actual publisher/profile/transport/mount mutations;
resource labels alone provide no cross-run exclusion. Local scripts, not GitHub
Actions, remain the execution mechanism.

### Sprint exit and acceptance boundaries

RP-S1 exits with retained source/fixtures/presentation, applicable source checks
and a supported decision baseline or actionable unresolved finding naming the
exact reached boundary, missing observation/remedy, closing owner and next action.
No duplicate fixture or presentation implementation is requested. RP-S2 still
requires actual common-bundle G1-G4 and a completed non-held initial parent;
RP-S3 requires actual both-role two-turn continuity, once-only confirmed supported
stop/resume without duplicates, distinct-parent isolation and truthful delivery.
Retained private-observation assertions collect/authenticate nothing by themselves.
AC1-AC9/G1-G8, rollback assets, historical UNKNOWNs, held parents and historical
cleanup uncertainty remain unchanged. Account-wide Blob Contributor means
application-enforced isolation, not malicious-host or storage-RBAC isolation.

Apply exact prior references
`["yaml-loops-v1:ArchitectureLoop","architecture-close-agreed-deliverable"]`,
`["yaml-loops-v1:UserExperienceLoop","ux-close-agreed-deliverable"]`,
`["yaml-loops-v1:ReleasePlanLoop","release-plan-close-agreed-deliverable"]` and
`["yaml-loops-v1:sprint/1/RP-S1/SprintDesignLoop","sprint-design-close-agreed-deliverable"]`
only to their originating accepted handoffs. None supplies this loop's reviewer
votes or release success. Architect agrees to this bounded cumulative/tier
handoff; current Product Owner, Critic and Red Team agreement is still required.
This documentation-only revision does not repeat private receipt/resolver
experiments, select a remedy, change lab source or execute cloud effects.
Current local checks are reported separately from historical measurements below.

### Local verification for this ownership-designation overlay

Existing absolute lab Python 3.12.10 and the explicit lab root were used:
`Test-Demo.ps1` passed dependency checking, **204 offline tests in 45.825 seconds**
and compilation. `scripts/Test-Repository.ps1` passed index,
**79-public-file** boundary, JSON/PowerShell/context and whitespace checks.
Structural validation passed **62 local links/anchors** and balanced fences
across all four architecture files. No dependencies were installed. These are
documentation/source compatibility checks, not new runtime or live progress.
No lab source changed; full retained lab and Linux hosting-package suites were
not run. No cloud operation, private receipt authentication or push occurred.

## Current RP-S1 recovery-entry architecture (October 20, 2026)

Historical recovery-entry overlay: use the ownership-designation section above
for current coordination inputs; retain the dated technical contracts below.

This is the current **RP-S1 SprintArchitecture** overlay, based on clean
application HEAD `160b38d202bd239ecd409b8f7de485b1d7f7e10e` on
`feature/customer-hosted-session-prototype`. It consumes agreed
[release architecture](customer-prototype-architecture.md) at `2f62e3c`,
[UX](customer-prototype-ux.md) at `8d6d6e0`,
[release plan](customer-prototype-release-plan.md) at `68c5bd8` and
[sprint design](customer-prototype-sprint-design.md) at `160b38d`.
No completed prior sprint or separate blocked-decision list was supplied for
this invocation. Earlier RP-S1/RP-S2/RP-S3 slices below remain cumulative
technical contracts and historical observations, not the current sprint,
new assignments, pending original reviews or fresh live evidence.

### Sprint decision and cross-tier invariants

Retain the three-role end-to-end design: terminal -> hosted MAF coordinator ->
remote architect -> remote reviewer -> fenced current-artifact acceptance.
The same parent manifest reuses both children and their pinned versions on a
revision or follow-up; `RemoteAgents.invoke()` restores their framework
`AgentSession`, and each specialist independently restores model history.
Fresh invocations advance response IDs and current outputs, not child identity.
Conversations, checkpoints and immutable artifacts/effect journals remain
distinct state planes. Keep the explicit lifecycle order, pinned dependencies,
trusted principal equality, private managed-identity Blob path, Decision-1
after deterministic gates, write-ahead effects and UNKNOWN holds.

The architecture delta is **recovery-entry interpretation and matched
operational source integration**, not a runtime rewrite or another identity
mechanism. The installed specialist-only B client remains a candidate.
A requires its own supported, evidenced authentication/configuration correction;
a scenario label cannot switch the installed B source to A. Neither is selected
live. No new service, history schema, public event, CLI flag, comparison ledger,
SessionManager, infrastructure or permission change is introduced here.

| Logical tier | Current RP-S1 boundary and retained handoff |
|---|---|
| [Coordinator](requirements/coordinator/architecture.md#current-rp-s1-recovery-entry-boundary) | Retain both-role two-turn/four-call fixtures, immutable snapshot comparisons, stale-approval invalidation and exact accepted refs. Candidate resource setup failure is preparation rejection, not a remote receiver observation. |
| [Specialists](requirements/specialists/architecture.md#current-rp-s1-recovery-entry-boundary) | Retain both real load/model/store paths, identical-brief fresh-history controls and exact-response zero-send recovery. Neither historical trust nor candidate source proves either role's trusted ingress or restored history live. |
| [Client/release](requirements/client-release/architecture.md#current-rp-s1-recovery-entry-boundary) | Retain accepted README/opt-in human stderr and unchanged machine parser. Join reviewed runner to matched operational wrappers/roots before execution; maintain separate current-trust/inventory and coding lanes. |

### Recovery evidence, source roots and actual closing actions

Consume the accepted release architecture's historical recovery-summary/receipt
locators and executed canonical/sibling resolver matrix without rerunning those
experiments. Those observations do not establish current writer exclusivity,
SSH trust, authenticated inventory, installed wrapper revisions or ingress.
The supplied recovery-exception locator is the first read-only evidence source
when original owners need that evidence; bounded Git/sibling-resolver inspection
is already authorized. Do not request new product permission for that inspection
or silently restart the historically stopped ownership task.

Preserve `LAB_TOOL_OWNER_MISMATCH`: load each retained wrapper with its own
operational lab root. A runner in a separately verified writable checkout may
invoke canonical wrappers explicitly in their canonical context. Reviewed
sibling wrapper changes are not installed canonical changes. Before effects,
integration must join runner, application and every required operational wrapper
revision/hash to the actual loaded paths. A missing required operational delta
is an integration failure, not permission to weaken the guard, copy credentials
or substitute a profile. This is the accepted composition boundary, not a new
third root abstraction.

| Existing owner | Bounded closing condition / downstream handoff |
|---|---|
| Developer / Scrum | Reconcile point-in-time writer/path ownership with supplied branch/status/resolver evidence and originating review before runner writes. Registration alone is insufficient; no write probe or shared branch switch. |
| Transport owner / DevOps | Substantiate the already approved module/source/fingerprint, verify current exact hashes and strict trust, then fresh sole-target authenticated inventory. Historical receipts are locators, not present trust or original-UNKNOWN cleanup. |
| Developer / integration | Retain accepted application fixtures, candidate, presentation and `validate_scenario_evidence()` assertions without redispatch. Complete concrete runner deltas with root/source/scenario/version, partial-role, preparation/receiver, unknown-effect and zero-send negative controls; integrate reviewed operational source. |
| Original E2E | Validate the exact joined implementation through local repository scripts. An agreed predeployment FAIL is not release readiness; architecture observations are not formal integration PASS. |
| Original DevOps | Join fresh inventory to exact-source/Linux/amd64/hosting-Python/common-package gates, retained preview/publication and finite trusted-ingress trial. Architect receiver success precedes reviewer; each reached/unreached role is recorded. Selection alone does not pass G1-G4. |

Writing ownership gates runner coding, not independent application checks.
Current trust and verified context gate inventory, not coding. Reviewed source
and fresh inventory join before release/trial. Only a demonstrated necessary
permission delta adds exact-scope scripted plan/write/readback; the user's lab
approval is retained, not speculative grant authority. Scrum owns task IDs,
minimal dependencies, actual shared-resource serialization and Git reconciliation
in existing planning/execution stages. Keep publication/profile/transport/mount
mutation serialized; scheduler resource names alone give no cross-run isolation.
No assignments or additional approval stage are created by this document.

### Sprint exit, later live gates and disposition boundaries

RP-S1 hands off retained source/fixtures/presentation, applicable current checks
and a supported identity baseline **or actionable unresolved finding**. Preserve
the historical `NATIVE_HOST_PRINCIPAL` result as history, not a fresh diagnosis.
The unresolved decision closes with the exact reached boundary, missing
observation/supported remedy, existing closing owner and next action. A material
principal-namespace or held-state finding goes to existing Architect-advised
PO/Scrum reconciliation, not equality relaxation or invented human approval.
Only genuinely unavailable human/provider information merits needs-input.
Continue the remaining artifacts while selection is unresolved.

RP-S2 still requires actual final common-bundle G1-G4 and a completed non-held
initial parent. RP-S3 still requires both-role two-turn exact continuity,
once-only confirmed supported stop/resume without duplicate effects, independent
separate-parent isolation and truthful exact-source delivery. Retained
`live_acceptance.validate_scenario_evidence()` asserts supplied observations;
it neither collects/authenticates them nor proves live acceptance by itself.
No alias, brief replay, HTTP 200, model memory text or agreed blocked assessment
substitutes for these gates. Account-wide Blob Contributor gives application-
enforced ownership/isolation, not storage-RBAC or malicious-host isolation.
Preserve historical UNKNOWN effects, held parents, rollback assets, unrelated
work and historical cleanup uncertainty.

Apply exactly
`["yaml-loops-v1:ArchitectureLoop","architecture-close-agreed-deliverable"]`,
`["yaml-loops-v1:UserExperienceLoop","ux-close-agreed-deliverable"]`,
`["yaml-loops-v1:ReleasePlanLoop","release-plan-close-agreed-deliverable"]` and
`["yaml-loops-v1:sprint/1/RP-S1/SprintDesignLoop","sprint-design-close-agreed-deliverable"]`
only within their originating acceptance. They preserve accepted handoffs,
not this loop's reviewer votes or release success. The stopped historical
ownership reference remains
`["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-LAB-OWNERSHIP/AssignedWorkDeveloperLoop","lab-ownership-review-evidence-access"]`;
new locatable evidence does not retrospectively accept it or reset its stop.
Architect accepts this bounded design; current Product Owner, Critic and
Red Team agreement remains required for this SprintArchitectureLoop.

### Checks for this recovery-entry overlay

Using the existing absolute canonical-lab Python 3.12.10 executable and
explicit lab root, `Test-Demo.ps1` passed dependency checking, **204 offline
tests in 46.940 seconds**, and compilation. No dependencies were installed.
After index refresh, `scripts/Test-Repository.ps1` passed index,
**78-public-file** boundary, JSON/PowerShell/context and whitespace checks.
Structural checks passed **55 relative links/anchors**, balanced fences in
all four architecture files and current RP-S1 source/root/exit/review boundaries.
These repeated checks validate source/document compatibility, not new runtime
capability or reviewer-verified experimental progress.

Only cumulative architecture, three tier files and navigation changed.
No lab source, runtime, dependency, assignment or machine contract changed;
retained lab release and Linux hosting-package suites were not run.
No private receipt inspection, resolver experiment, authenticated inventory,
cloud operation, identity trial, deployment, stop/resume or push occurred.
Historical measurements below remain historical.

## RP-S3 current sprint: continuity, recovery and isolation evidence joins

This slice retains the accepted RP-S2 architecture at
`8fc296f65589af88706396ecf50e27b0f75deaef`, application preparation at
`990467afd3e03efdf55aa236ee56ecc1bd04de66` and retrospective at
`585601f4ad3e8d87c029a6fdca2d0326a403e142`. The inspected clean baseline is
`7f7376b85e7b5f4e216dd382480cf6678d07eadf` on
`feature/customer-hosted-session-prototype`, containing the accepted
[RP-S3 screens H-K](customer-prototype-sprint-design.md#rp-s3-continuity-supported-recovery-and-truthful-delivery).
RP-S1/RP-S2 process completion is not delivery of their unmet live gates.
Earlier sections below are retained historical slices, not current pending
reviews or claims that no prior sprint has completed.

Exactly three hosted roles, explicit MAF execution order, existing dependency
pins, trusted parent binding and specialist-only B client isolation remain.
No session manager, history migration, fourth service, runtime selector, new
public event/schema, CLI option or comparison ledger is introduced.
The following joins refine existing AC1-AC9/G1-G8, not their requirements.

### Entry handoff and blocked execution

RP-S3 live continuation consumes an actual completed, non-held initial parent
with G1-G4 evidence: final common bundle and exact three-role versions, remote
accepted artifacts, private managed-identity Blob provenance and genuine
Decision-1/deterministic acceptance. Neither identity selection nor an
`ACCEPTED_ADVISORY` string alone establishes this handoff. Preserve its private
source/package/version and parent/child bindings; the queue follow-up uses that
same conversation, not another fresh parent manufactured for the report.

The supplied RP-S2 outcomes do not establish this entry handoff or either
successfully selected live identity path. Architecture can complete while those
effects remain blocked. Keep independent ownership/root and established-trust
lanes, reviewed runner/source integration, formal joined-source E2E and original
DevOps exact-package/publication/finite-trial execution from the RP-S2 joins.
Existing Developer/Scrum coordination delivers bounded existing setup evidence;
existing transport-owner coordination delivers the private accepted fingerprint,
approved module path and module/source SHA256 receipt locator. Failed evidence
lookup is not evidence absence. Do not restart stopped probes, derive replacement
trust, bypass blocked runner writing or repeat missing-trust checks as progress.

### Stable identity, advancing work and independent state

| Concern | Required comparison / owner boundary |
|---|---|
| Parent conversation | Actual hosted ID, framework identity and pinned coordinator version stay stable across initial, queue follow-up and supported continuation; retain the same private terminal session file |
| Both specialist children | Compare each role's actual hosted ID, framework identity, pinned name/version and parent scope in independent before/after snapshots; two total child creations for the initial/follow-up pair |
| New invocation | Both roles run on both user turns; each new call has a fresh response ID and current exact prerequisites; known-response retrieval is not another invocation |
| Requirements and acceptance | Follow-up preserves private ingress and adds the queue; prior approval is invalidated before new work; exact current candidate/review hashes, producers, revisions and fenced acceptance match |
| Specialist model history | Each real role restores its own model session/history; retained direct continuation and identical-brief fresh-history controls prove the offline boundary, not live capability from repeated brief text |
| Graph and effects | MAF checkpoints retain executor position; immutable artifacts, manifest ETag/fencing and write-ahead journals reconcile effects independently of conversation/history |

Do not compare complete serialized sessions as constant: framework service
continuation advances. Keep the retained four-call reject/revise/review fixture
as offline AC3 evidence; live two-turn AC1/AC2 remains separate. No fake/local
specialist or alias/memory-text comparison can fill a missing live observation.

### Supported recovery and separate-parent isolation

[`live_acceptance.py`](../live_acceptance.py) retains the native `restart`
scenario and `stop_hosting_for_acceptance()`: completed bound non-pending parent,
exact parent/version readback, exclusive durable `.hosting-restart.json` intent,
one supported stop request, then confirmed `idle` with a new finite positive
`stopped_at`. Existing `stop_pending` is observed without resending; another
phase rejects a repeated stop. HTTP 204, terminal restart or disconnect alone
does not satisfy G6. Missing confirmation stays unresolved, not permission to
delete the marker or issue another stop.

Original DevOps continues the same parent after confirmation and compares both
children, pinned versions, checkpoint/effect reconciliation and actual sends.
Verify no duplicate effects from journal/response/artifact evidence; do not infer
that from a resumed process or matching output text. Known responses are retrieved
exactly without send. Uncertain creation/send, binding drift and held effects
stop further effects; retain private evidence and the existing repair owner.
This tests supported compute deprovision/rehydration, not hard-crash recovery or
exactly-once platform/deployment effects.

A separate synthetic parent uses a distinct private session file, distinct
actual parent and both child bindings, separate artifact scope and an independent
brief excluding the first conversation's requirements. Verify content exclusion
and retained cross-scope rejection regressions as separate observations.
Different filenames, aliases or version numbers alone prove no isolation.
Account-wide Blob Contributor permits application-enforced role/parent checks,
not storage-RBAC or malicious-host isolation. Isolation and recovery have no
invented dependency on each other; Scrum assigns only their real shared resources.

### Exact-source evidence and delivery handoff

The retained acceptance utility emits per-scenario evidence and checks bindings,
versions and artifact envelopes; that output is not by itself the complete
cross-turn, creation-count, no-duplicate or separate-parent comparison.
Existing Developer/integration work must join actual snapshots and assertions
through deterministic local repository scripts and repair only concrete missing
checks. Original E2E validates joined implementation; original DevOps runs
hosting checks, release and live scenarios. No unimplemented comparison command
is promised here and no GitHub Actions execution is substituted.

| Gate / handoff | Closing evidence, without weakening preceding gates |
|---|---|
| G5 / AC2 | Initial and queue follow-up exact binding/creation/response/current-output comparisons for both roles, with stale approval invalidation |
| G6 / AC4 | Once-only durable stop intent and confirmed stop state joined to same-conversation continuation and no-duplicate-effect assertions |
| G7 / AC4 | Separate-parent bindings/scope, excluded first-parent content and passing cross-scope regressions |
| AC6 | Existing README commands and useful opt-in human stderr output; unchanged stdout/parser; sanitized comparison outcomes supplied separately from private exact proof |
| AC7-AC8 | Final exact-source application/repository and affected retained checks, actual Linux/amd64/hosting-Python package validation, reviewed feature-branch integration and scoped push outcomes |
| G8 / AC9 | Dated per-criterion evidence attribution, actual final/rollback bindings privately, generic setup and reproducible implemented demonstration command, owned cleanup and explicit limitations |

Keep Screens H-K illustrative reporting guidance. Existing aliases cannot
become VERIFIED continuity badges or new machine fields. Exact private bindings,
transcripts, hashes and evidence locators stay out of shareable source/output.
Original DevOps records positively identified newly owned processes, listeners
and mounts and their cleanup; new cleanup never certifies historical cleanup.
Preserve all historical UNKNOWN publications, held parents, rollback assets and
unrelated work. Report each AC/G gate verified, failed or unreached from actual
evidence, distinguishing local/mocked, Linux/package and hosted observations.
Customer-ready requires every mandatory gate; otherwise give the precise last
boundary, missing criterion, existing owner and supported closing action.

Applicable exact prior references remain bounded:

- `["yaml-loops-v1:sprint/2/RP-S2/SprintArchitectureLoop","rp-s2-sprint-architecture-close-agreed-deliverable"]`:
  retained RP-S2 architecture is closed, not current RP-S3 approval.
- `["yaml-loops-v1:sprint/3/RP-S3/SprintDesignLoop","rp-s3-sprint-design-close-agreed-deliverable"]`:
  accepted reporting screens remain closed without duplicate UI implementation.
- `["yaml-loops-v1:sprint/2/RP-S2/SprintRetroLoop","rp-s2-sprint-retro-close-agreed-deliverable"]`:
  retain independent evidence lanes and existing-owner closing actions.
- `["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-LAB-OWNERSHIP/AssignedWorkDeveloperLoop","lab-ownership-review-evidence-access"]`:
  remains unresolved with taskComplete=false, originating five-round stop and
  runner-writing block until substantiated and accepted by original reviewers.
- `["yaml-loops-v1:sprint/2/RP-S2/EndToEndTestLoop","rp-s2-e2e-close-agreed-failure-assessment"]`:
  closed prerequisite FAIL is neither joined-source PASS nor publication readiness.
- `["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-ISOLATED-CLIENT/AssignedWorkDeveloperLoop","isolated-client-close-agreed-handoff"]`:
  retain accepted candidate without renewed review or inferred live compatibility.

Scrum Master retains contract-first decomposition, minimal dependencies, exclusive
publication/transport/CLI ownership and Git reconciliation; architecture does not
dispatch new competing assignments. Material identity namespace, held-state or
source-contract changes return to existing Architect-advised Product Owner/Scrum
reconciliation, never equality relaxation or a release waiver.

## RP-S2 current sprint: evidence joins without a runtime rewrite

This cumulative `SprintArchitecture` carries forward accepted RP-S1 architecture
`4b3d0a4ecfda090f4721008de7c301e3fdf34cbc` and the retrospective
`b43f5569b97c37427cf7f1b47d103846dd350dca`. The RP-S1 sections below retain
their historical scope and observations; their earlier pending-review and
no-completed-sprint statements do not describe this RP-S2 handoff.
The current [RP-S2 design](customer-prototype-sprint-design.md#rp-s2-gated-identity-trial-and-truthful-collaboration-handoff)
is accepted at `9dfb73d5477994128b3d3136eee1a4bf9441314d`, the clean
application baseline inspected for this revision on the authorized feature
branch. RP-S1 process completion is not successful product delivery.

The technical design remains exactly three remote hosted roles, parent-scoped
children with pinned versions, restored framework sessions and specialist model
history. Immutable prerequisites/outputs, trusted receiver equality, coordinator
ETag/fencing, checkpoints, write-ahead effects and explicit unknown holds remain
unchanged. No new runtime selector, public field, CLI, history schema or service
is introduced. The tier contracts below carry the current sprint joins.

### Accepted work and unresolved prerequisite lanes

Apply the following exact prior references within their originating boundaries:

- `["yaml-loops-v1:sprint/1/RP-S1/SprintArchitectureLoop","sprint-architecture-close-agreed-deliverable"]`:
  retain accepted RP-S1 architecture; its votes are not RP-S2 approval.
- `["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-ISOLATED-CLIENT/AssignedWorkDeveloperLoop","isolated-client-close-agreed-handoff"]`:
  candidate `3aca5dc236695c5ec7eac98d0cd03bced40da7b8` and original
  both-role resource-factory review are accepted; do not duplicate them.
- `["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-LAB-OWNERSHIP/AssignedWorkDeveloperLoop","lab-ownership-review-evidence-access"]`:
  ownership/root setup remains incomplete despite agreement with its blocked
  report. Preserve the five-round stop and runner-writing block. Existing
  Developer/Scrum coordination supplies registration, branch/HEAD/status,
  canonical-work preservation, point-in-time writing ownership and positive/
  negative resolver evidence for permitted original-reviewer inspection.
  Do not restart unattended denied probes or recreate the checkout here.
- `["yaml-loops-v1:sprint/1/RP-S1/EndToEndTestLoop","e2e-close-agreed-failure-assessment"]`:
  retain the closed predeployment FAIL assessment, not integration PASS.
- `["yaml-loops-v1:sprint/1/RP-S1/SprintRetroLoop","sprint-retro-close-agreed-deliverable"]`
  and `["yaml-loops-v1:sprint/2/RP-S2/SprintDesignLoop","rp-s2-sprint-design-close-agreed-deliverable"]`:
  retain accepted evidence-boundary guidance and screens without duplicate work.

The independent transport lane needs the **existing independently accepted**
private fingerprint/transport-owner receipt locator before strict-trust
Metadata inventory. The supplied DevOps report stopped at
`HOST_TRUST_EVIDENCE_REQUIRED`; no invocation receipt was independently inspected
here. ARM readiness is not authenticated SSH readiness, and neither establishes
hosted version inventory or specialist ingress. Do not derive trust from a newly
observed key, retrieve key material or put private locators in shareable output.
Missing evidence delivery is not a newly established provider defect.

### Preparation, execution and acceptance joins

| Boundary / existing owner | Required handoff | Failure meaning |
|---|---|---|
| Checkout/root evidence / Developer and Scrum | Substantiated ownership plus canonical operational-root versus writable tooling-root contract, accepted by original setup reviewers | Setup remains unmet; runner writing blocked, not a remote runtime rejection |
| Runner / Developer | Reviewed retained executable and offline root, ownership, mismatch, redaction, partial-role, unknown-effect and zero-create/send fixtures | Coding failure; no inference or publication is authorized by a fixture |
| Joined source / assigned integration owner | Candidate ancestry, reviewed application/lab commits, exact joined checks, durable Git accounting and scoped push outcomes | Predeployment integration prerequisite failure |
| Inventory / DevOps, independent of coding | Strict-trust private current/rollback, package, identity, caller/effective-action and held-effect observations | Explicit missing observation, not evidence of absent permission |
| Formal integration / original E2E | Validate the reviewed joined source through local repository scripts | Accurate FAIL is actionable assessment, not cloud-pass |
| Exact release / original DevOps | Actual Linux/amd64/hosting-Python checks, final source/settings/package hashes, retained preview and guarded publication | Do not create a trial parent from an unjoined or drifted release |
| Finite trial / original DevOps | Rejoin scenario, reviewed source, final common package and actual three-role versions before parent creation; architect trusted ingress/receiver success before reviewer | Preparation rejection, observed receiver rejection, partial ingress and unknown outcomes remain distinct |
| RP-S2 acceptance / original E2E and DevOps | Three healthy common-bundle roles, accepted remote artifacts, private MI Blob provenance and genuine Decision-1 plus deterministic gates G1-G4 | Identity selection alone is insufficient |

The installed source is unconditional B, not a scenario switch. An A trial
requires its own supported corrected source/regression; relabeling B as A or
retrying unchanged A must fail before create/send. A permission write is a
conditional join only when fresh effective-action evidence establishes the
necessary authorized delta; document exact scope/rationale and deterministic
plan/write/readback. No speculative grants or new permission approval stage.

A selected path requires both roles' observed ingress and receiver validation.
Accepted remote collaboration additionally requires the exact candidate/review
prerequisites and coordinator acceptance, private managed-identity artifact
operations and genuine routing records. Preserve historical UNKNOWN publications,
held parents, rollback assets and cleanup uncertainty regardless of the result.
Known-response inspection retrieves the exact response without another send.
No automatic fallback, replacement parent or adoption of held histories.

RP-S3 still owns live two-turn continuity, once-only supported compute stop/resume,
separate-parent isolation and final AC1-AC9/G1-G8 closure. Account-wide Blob
Contributor provides application-enforced scope, not malicious-host/storage-RBAC
isolation. Material namespace/held-state changes return to the existing
Architect-advised PO/Scrum process; ordinary implementation stays with the
retained owners. This architecture revision neither resolves the stopped setup
task nor certifies live selection, transport, deployment or release acceptance.

## Scope, accepted baseline and cumulative design

This is the `SprintArchitecture` handoff for **RP-S1**, not an implementation,
SprintPlan, deployment or live acceptance result. The customer outcome remains
a hosted coordinator repeatedly calling remote architect and reviewer agents,
preserving each specialist's session within the same parent conversation.
Exactly three hosted deployments remain.

Accepted inputs are retained, not reopened:

- [Release architecture](customer-prototype-architecture.md), `cde76380c9c41201f19aedf4b290958c95472689`.
- [UX](customer-prototype-ux.md), `c17813567e7d3db09abe1d2403b948c98131c24f`.
- [Release plan](customer-prototype-release-plan.md), `f20ac1ee1cdbc561198d51fba53f14c90348de8d`.
- [Sprint design](customer-prototype-sprint-design.md), `6a24eaf3110bd964f992a87e01e6916f505e0dda`.

This revision inspected clean application baseline `6a24eaf3110bd964f992a87e01e6916f505e0dda` on
`feature/customer-hosted-session-prototype`. No completed prior sprint was
supplied. Retain the integrated RP-S1 work: coordinator fixtures `6614440`,
direct model-continuation fixtures `c454e50`, human view `56b762e`, documentation
`e24fcb9`, research `39c3b4e` and source reconciliation `24b883f`. These are
existing implementation history, not new progress or live acceptance here.
The cumulative design is the accepted release architecture plus this RP-S1
refinement. The existing [design](design.md), [migration boundary](migration-plan.md),
[implementation workflow](implementation-workflow.md) and
[recovery plan](identity-recovery-plan.md) remain applicable.

The tier documents below are derived architecture contracts, not a replacement
requirements source or new services. These logical tier names describe existing ownership:

| Logical tier | Architecture file | Existing code responsibility |
|---|---|---|
| Coordinator | [coordinator](requirements/coordinator/architecture.md) | Parent-scoped bindings, workflow, artifacts and fenced acceptance |
| Specialists | [specialists](requirements/specialists/architecture.md) | Both remote roles' own model history and immutable proposals |
| Client and release boundary | [client-release](requirements/client-release/architecture.md) | Terminal projection and retained exact-release/live verification |

The supplied October 19 customer specification remains authoritative. Do not
copy private delivery inputs, evidence or settings into these directories.
Older accepted documents' statements that this directory did not exist describe
their baseline, not a prohibition on the tier-specific output required here.

### Prior dispositions and bounded acceptance

Apply these exact provenance-qualified references only to their original outputs:

- `["yaml-loops-v1:ArchitectureLoop","architecture-close-agreed-deliverable"]`
  retains accepted full-release architecture and unresolved identity handoff.
- `["yaml-loops-v1:UserExperienceLoop","ux-close-agreed-deliverable"]`
  retains accepted UX; no redispatch of integrated presentation work.
- `["yaml-loops-v1:ReleasePlanLoop","release-plan-close-agreed-deliverable"]`
  retains accepted release planning and original downstream owners.
- `["yaml-loops-v1:sprint/1/RP-S1/SprintDesignLoop","sprint-design-close-agreed-deliverable"]`
  retains accepted RP-S1 screens and fixture-to-display handoff.

None supplies SprintArchitecture reviewer votes, selects an identity path,
waives live/package gates or reopens an accepted handoff. Scrum Master owns
delta decomposition and Git reconciliation, not a redispatch of accepted work.

## Data flow and sprint delta

```text
user turn -> trusted hosted parent -> begin / route / execute / publish
                                        |
                           manifest.children[role]
                                        |
                     restore bound framework AgentSession
                                        |
                   remote specialist hosted session/version
                                        |
                   role-local stored model history/continuation
                                        |
                immutable proposal -> exact-input validation -> acceptance

complete existing events/result -> optional human stderr projection
                               -> unchanged default stdout / acceptance parser
```

Retain Python, MAF, Foundry Responses, dependency pins and explicit execution
order. Conversations, checkpoints and artifact/effect state remain independent.
Do not add a generic SessionManager, new ledger, framework, fourth service,
browser UI, storage broker or toy orchestration loop.

The integrated `test_followup_invalidates_old_approval_and_preserves_children`
in `tests/test_workflow.py` now records both roles before/after each call and
in the final manifest via `assert_recorded_bindings`. It verifies stable scope,
hosted/framework identities, pinned names/versions, exactly two creations, four
distinct responses, current requirements and invalidation at the follow-up send.
`test_reject_revise_review_reuses_both_children_with_fresh_responses` records
the four-call reject/revise/review path and exact c2 acceptance. Retain these
fixtures and their value snapshots; do not assign their implementation again.
Source inspection is not a fresh execution or live acceptance result.

`RemoteAgents.invoke()` already restores `AgentSession.from_dict(child.framework)`;
`recover()` advances its service continuation from the exact retrieved response.
Both real specialist files already load `specialist_history_v2` / `"history"`
and pass the restored session to their model stage. Architecture does not infer
that these source paths prove hosted or model continuation: RP-S1 must observe
their actual arguments and persistence with controlled offline boundaries.
`tests/test_specialist_continuity.py` already supplies both roles' real
load/model/store execution, identical-brief fresh-history controls, exact-response
no-send recovery and failed-retrieval/existing-output cases. Preserve that
handoff; only a concrete uncovered defect justifies a new fixture task.

## October 20 cross-sprint executable handoff

The accepted release architecture now distinguishes the integrated offline
identity handoff (`13203ac`, reconciled by `bb1743d`) from a hosted candidate.
`scripts/identity_handoff.py` has no live mode; its unresolved exit is not a
runtime fix. The specialist-only client is implemented in
`3aca5dc236695c5ec7eac98d0cd03bced40da7b8` and present on this branch.
Retain it for its original review/integration, without declaring its task
accepted here. The retained decision runner remains a Developer implementation
handoff, not unfinished RP-S1 continuity/UX work.
No completed prior sprint was supplied; this section carries the cumulative
design forward without declaring RP-S1 or RP-S2 accepted.

### Runtime boundary carried into RP-S2

The following client contract is now installed source, not live-selected B.
`WorkflowRuntime.resources()` unconditionally constructs specialist-only B;
it cannot select an A path from a scenario label. Preserve the accepted
[source-to-trial contract](customer-prototype-architecture.md#source-identity-is-part-of-the-scenario-contract):
before trial-parent creation, join the explicit scenario to reviewed source,
the exact common package and actual deployed role versions. `B-candidate`
requires the installed candidate or reviewed descendant; `A-correction`
requires its own evidenced supported correction and regression. Relabeling
B as A or retrying unchanged historical A fails preflight without dispatch.
There is no new runtime selector, configuration knob or approval stage.

Within the existing request-owned `WorkflowRuntime.resources()` stack, keep
the original opaque-only project/header resources and yielded tuple semantics
for routing, parent/model/history/checkpoint operations. B receives a distinct
specialist-only `ProjectClient`, copied headers and independent OpenAI-client
cache, passed only to `WorkflowRemoteAgents`. Do not mutate shared headers,
ambient hosting context or the non-specialist project. A shared credential/
transport is allowed only with regression coverage for safe close ordering
and cleanup on setup failure, cancellation and normal exit.

Before deriving B delegation, reconstruct the full trusted
`ScopeBinding.from_platform(...)` from captured authenticated hosting context
and compare it to runtime scope. Move only necessary pure candidate logic to
runtime-owned source; hosted code cannot import the offline runner. Preserve
opaque-call forwarding and reject container-user headers, absent/forged users
and call-ID-as-user substitution. Receiver principal equality is unchanged.
The coordinator and specialist tier files specify the corresponding tests.

There is no new runtime path selector. DevOps binds a named candidate trial
to reviewed source, one common bundle and exact three-role versions in private
evidence. Existing deployed A remains until deliberate guarded publication;
no automatic switch after an error. A later required selector/settings change
is an explicit Architect/Scrum delta, not an undeclared environment option.
Old pinned/held conversations keep their versions, histories and journals.
Only a fresh synthetic parent may enter this candidate; no implicit migration.

### Contract-first lanes and true joins

These are handoff contracts, not task IDs or new assignments. Scrum Master
owns decomposition, actual dependencies, exclusive resources and integration.

| Lane / original owner | Bounded doneWhen | Join or exclusion |
|---|---|---|
| RP-S1 retained source / Developer | Preserve integrated binding, revision, history and presentation fixtures; repair only affected concrete failures; hand off current checks | Do not redispatch accepted implementation or claim live proof |
| RP-S1 fresh inventory / DevOps | Privately bind sole-target current/rollback versions, packages, protocol, identities, caller/effective action and unresolved owners/effects | Independent of candidate/runner coding; no assumed missing grant |
| RP-S2 isolated runtime / Developer | Retain installed `3aca5dc` and its real resource-factory regressions for original review/integration; repair only concrete failures and check joined source | No duplicate implementation, deployment, namespace relaxation, schema/dependency/history migration or UX rewrite |
| RP-S2 local decision tooling / Developer | After safe lab writing ownership, retained runner satisfies the client-release tier contract with offline ownership, failure, redaction and unknown-effect regressions plus affected retained suite | Coding does not wait for cloud inventory; original DevOps exclusively owns guarded publication and live execution |
| Git/source integration / Scrum-assigned owner | Reviewed task commits joined on the authorized feature branch, exact joined source checked; named retained branches/task/commit/reason recorded for any abandoned code | Establish lab writing ownership safely; never switch its shared dirty checkout under writers |
| Bounded decision / DevOps | Joined runtime/tooling, fresh inventory and exact-source/Linux/package gates precede retained publication and finite trusted-ingress trial | Conditional permission plan/write/readback joins only if a required delta is evidenced; no formal E2E/cloud-pass credit |

The prior lab observation was `feature/swc-think-fast-aca-dns` with eight dirty/
untracked paths; this revision does not refresh that status. None is adopted here.
Scrum must assign safe lab feature-
branch/worktree reconciliation before any lab writing; no new human approval
is required for that internal ownership action.

The decision handoff names each reached/unreached role and returns `selected-A`,
`selected-B` or actionable `unresolved`. Architect-only entry is not both-role
selection or remote collaboration. A resource-construction guard failure is a
local preparation rejection, not observed receiver failure or proof of missing
permission. Classify receiver failure only from an observed child result;
missing observation remains unknown. Missing/changed principal, receiver rejection,
version drift or an unknown effect stops that candidate without another send.
A namespace or held-state contract change returns to existing Architect-advised
PO/Scrum reconciliation; an unavailable supported provider finding is an exact
external stop, not a reason to repeat old research or block remaining artifacts.

## Cross-tier fixture contract

Use test-owned recording adapters around existing interfaces, not a production
protocol or customer-visible evidence database. Capture before/after snapshots
by value: a reused mutable object must not make a comparison pass accidentally.

| Observation | Assert in offline tests | Do not infer |
|---|---|---|
| Parent | Same trusted scope/parent across initial and follow-up | Local filename or alias proves hosted ownership |
| Child, per role | Stable hosted ID, framework `session_id`, agent name and pinned version at each call and final manifest; stored hosted key matches binding | Entire framework dictionary must remain equal |
| Invocation | Ordered role, operation, turn/revisions, exact input refs, response ID and continuation passed/returned | Recovered known response counts as another send |
| Creation | Exactly architect and reviewer once across two turns or the four-call revision fixture | Two visible aliases prove two creations |
| Model, per role | Store key/context, restored identity/state/service continuation actually passed to model call; persistence after output | Same full brief or plausible memory proves history |
| Acceptance | Current requirement/candidate refs and hashes; old approval invalidated before calls; final exact revised review | Blob existence or SDK completion is acceptance |

Initial/follow-up fixture: synthetic private-ingress application, then queue
addition retaining earlier requirements; architect/reviewer each called on both
turns, four distinct invocation responses and two child creations.
Revision fixture: architect c1 -> reviewer blocked c1 -> architect c2 ->
reviewer approves c2. Both repeated calls use the original binding/version;
review c2 consumes exact c2 plus current requirements, not stale c1 approval.
Use controlled routing responses with existing deterministic gates, budgets and
Decision-1 contracts; never force success by bypassing publication.

For model-history tests, hold the input brief constant in a negative-control
comparison so input replay cannot explain the observation. Run each real role's
load/model/store path with a persisted first-session continuation and then a
fresh/absent history store. Assert the model boundary differs as expected.
Known pending model response retrieves that exact ID with zero model sends;
unknown/mismatched pending state remains held. Existing crash, parsing,
cross-scope, transport, checkpoint and fencing cases remain intact.

## Blocker disposition and conditional repair

Historical `NATIVE_HOST_PRINCIPAL` occurs before architect application entry:
the captured outgoing opaque call context matched, but trusted child user was
absent. It is unresolved; no cause-specific remedy, missing grant or platform
defect is established here. No fresh cloud inventory or public-remedy research
is claimed by this architecture refinement.

RP-S1 retains independent offline proof, clarity, and fresh-inventory/remedy-assessment
boundaries. Neither remaining artifacts nor validation waits for a provider answer.
DevOps freshly inventories target versions/packages/identities through retained
tools after sole-target private-settings/context validation. Architect/Developer
assess public supported contracts against installed pins and the exact observed
boundary. A research handoff records source/date/version applicability, supported
correction plus reproducer if established, or the precise absent finding.
Repeating old negative research without new evidence is not progress.

The prior bounded negative research remains valid within its originating scope,
but does not reject the additionally authorized delegation alternative.
If server-side resolution is still the missing evidence after both alternatives
are assessed, the actionable exit is
an exact-pair caller-resolution trace and documented supported platform/SDK
remedy. The operator must separately arrange provider contact/disclosure;
this invocation does not authorize submission or private evidence transfer.
This bounded negative finding may complete research, not RP-S2's live goal.

October 19 authority permits ordinary scoped corrections and guarded releases
for only the existing three roles; the old consumed diagnostic exception is not
a blanket ban on this new work. It never permits uncertain-effect replay,
identity substitution, speculative headers/grants, infrastructure/network/quota
changes or another target. Preserve held parents and original publication UNKNOWN.
Material contract, held-state migration or architecture changes use existing
Scrum Master reconciliation and Architect-advised PO decisions, not an invented
human approval or endless research loop.

### Identity-path decision contract for this sprint

Use the accepted release architecture's
[supported alternatives and selection contract](customer-prototype-architecture.md#supported-identity-alternatives-and-selection-contract).
The October 19 additional approval permits necessary narrowly scoped lab
RBAC/permission changes for either supported path; earlier blanket permission
exclusions are not a new approval prerequisite. No permission mutation or
live discriminator is performed by this document.

| Outcome | Required discriminator | Failing condition / closing action |
|---|---|---|
| `selected-A` | A measured authentication/configuration or effective-caller mismatch, supported correction and fresh trusted specialist ingress passing receiver checks | No mismatch or the same opaque-header failure: do not republish unchanged; evaluate B |
| `selected-B` | Stable authenticated end-user delegation across create/read/send/retrieve; actual child principal compatible with the parent's trusted binding; specialist entry and receiver validation pass | Missing/changed principal, namespace mismatch or held effect: retain evidence, reject that candidate; never weaken equality |
| `unresolved` | Actual attempted checks, why neither path is selected, exact missing fact/remedy and an actionable next owner/step | Continue remaining artifacts; live acceptance stays unmet, not implicitly waived |

For B, `Assignment.validate_receiver()` compares platform-derived child principal
to `scope_binding.principal`. A nonempty user header alone is insufficient:
delegating a platform-derived identity may resolve a different namespace.
Do not use opaque call IDs, assignment JSON, model text or client identity
headers as authenticated user authority. Keep required opaque-call forwarding
unchanged; do not forward container-only `x-agent-user-id`. The legacy
`platform_identity_headers()` helper is not a drop-in delegation fix.
Verify supported header coexistence rather than guessing.

Cover `RemoteAgents.prepare`, `create`, `_check` / `recover_creation`, `invoke`
and `recover`, including the distinct raw SDK and Responses header paths.
`WorkflowRuntime.resources()` now isolates specialist delegation from the original
project/header/cache used by routing and other non-specialist callers; retain
that boundary so parent/model/history/checkpoint authority cannot change
accidentally. If trusted namespace compatibility requires a new
binding contract, bring the exact mismatch to this existing Architect/PO/Scrum
process. Do not migrate held histories or remove receiver equality to select B.

Before any permission write, resolve the actual outbound coordinator principal,
both existing specialist targets and effective explicit data actions. Historical
impersonation permission presence is not fresh readback or proof it is missing.
If needed, scope only the required action to each supported existing agent scope;
an unsupported scope requires a documented smallest supported project scope,
not account/resource-group/subscription escalation. Record exact private
principal/role/resource IDs, before/after state, rationale, ownership and readback.
Use deterministic reviewed lab-owned scripts with unknown-outcome reconciliation;
never create duplicate grants or replace identities for convenience.

The bounded local repository script contract requires explicit application/lab
roots, scenario/path, exact versions and fresh synthetic scope, a finite intended
call sequence and pre-send journal. Offline negative controls cover omitted/
invalid identity, forged assignment principal, cross-parent scope, both roles,
all lifecycle header paths and exact-response no-resend. Observe architect
before reviewer; stop on held/unknown effect. Record presence/match classifications,
entry/receiver result and exact private evidence locators without public raw IDs.
Selection requires actual trusted ingress; offline tests or HTTP 200 do not select.
Both roles must pass before claiming remote collaboration. A required new package
goes through original DevOps source/Linux/package/publication gates; architecture
does not deploy to force selection. Permission readback is not runtime success.

The handoff records `selected-A`, `selected-B` or `unresolved`, hypothesis and
supported source/version applicability, actual tests, principal compatibility,
permission delta/scope/rationale, held effects and closing action. Neither path
is currently live-proven. Bounded decision tests are permitted here; formal E2E
and cloud-pass remain in their original loops through local scripts, not GitHub
Actions. No provider submission/private evidence transfer is authorized.

## Integration, verification and downstream handoff

Scrum Master owns actual task decomposition, minimal dependency edges and Git
reconciliation. These tier contracts are not assignments or another approval
stage. Shared `tests/test_workflow.py` changes need one assigned writer or
serialized fixture handoff. Terminal and README work can use existing schemas
without waiting for new runtime event fields.

Integrate only reviewed related readability changes; preserve originals and
unrelated dirt. Owners commit explicit intended paths on
`feature/customer-hosted-session-prototype` before original review. Integration
uses that branch; retained unmerged code requires named branch, task/commit IDs
and abandonment reason in a feature-branch commit message. Keep abandoned
branches. No broad staging, branch switch beneath writers, force push or reset.

Original E2E owns formal integration validation; original DevOps owns packaging,
publication and cloud-pass. Bounded architecture/planning decision tests do not
replace either gate. Serialize actual
`lab-hosted-release` and `lab-private-transport`; use `application-git-integration`
and, if needed, `lab-git-integration`. Scheduler names are not OS/cross-run locks.
Never race publication against acceptance. The live chain remains supported
correction + reviewed integration -> exact source/Linux/package gates -> guarded
publication -> initial acceptance -> follow-up -> supported stop/resume.
Separate-parent comparison needs initial evidence, not restart.

| Acceptance boundary | RP-S1 output versus later obligation |
|---|---|
| AC1 / G2 | Preserve remote-only architecture; actual accepted remote collaboration remains RP-S2 |
| AC2 / G5 | Exact offline binding/response assertions now; live two-turn comparison remains RP-S3 |
| AC3 | Controlled four-call workflow plus direct model-history fixtures now, labeled offline |
| AC4 / G6-G7 | Retain recovery/isolation regressions; actual once-only supported stop/resume and separate-parent evidence remain RP-S3 |
| AC5 / G1-G8 | G1 final common bundle, G2 collaboration, G3 MI/private Blob, G4 genuine Decision-1, G5 continuity, G6 recovery, G7 isolation, G8 truthful closure remain live gates, not architectural PASS |
| AC6 | Retain integrated first-screen README and opt-in terminal contract, then real demonstration later |
| AC7 | Integrated targeted/application/repository checks now; exact Linux/amd64/hosting-Python package gate remains DevOps |
| AC8 | Review/integrate intended source, preserve unrelated dirt, commit then reviewed scoped push; no private artifacts in Git |
| AC9 / G8 | Later report actual demo/setup, sanitized proof, final/rollback bindings, cleanup and limitations; no success from this document |

Required source checks use existing validated Python by absolute path:
`Test-Demo.ps1 -Python <absolute-path> -LabRepositoryRoot <explicit-root>` and
`scripts/Test-Repository.ps1 -Python <absolute-path>`. Retained suite follows lab
tool changes. Revalidate final changed source/package, not historical counts.
No dependency install without manifest change or missing-tool failure.

### Historical verification of the preceding documentation revision

Using the existing validated absolute Python 3.12.10 executable, without
dependency installation, `Test-Demo.ps1` with explicit lab root passed dependency
checking, **177 offline tests in 19.520 seconds**, and compilation.
`Test-Repository.ps1` passed index, public-boundary (**70 public files**), JSON,
PowerShell, context and whitespace checks. Local documentation checks verified
**32 relative links/anchors across four architecture documents**, AC1-AC9 and
the identity-selection handoff fields.

These are local/offline results, not hosted proof. No lab files changed; its
full retained release suite was not rerun. No fresh cloud inventory, live path
discrimination, permission write, publication, Linux hosting-package validation,
formal E2E acceptance, stop/resume or live continuity/isolation occurred.
The pre-existing unrelated lab worktree remains untouched. Final exact-source/
common-bundle and AC1-AC9/G1-G8 live gates remain downstream obligations.

### Verification of the October 20 cross-sprint refinement

The current source-to-trial reconciliation starts at `6a24eaf` and supersedes
the earlier ownership/readiness description, not its retained test contracts.
Using the existing absolute Python executable with explicit lab root,
`Test-Demo.ps1` passed dependency checking, **192 offline tests in 25.671
seconds**, and compilation. `scripts/Test-Repository.ps1` passed index,
public-boundary (**74 public files**), JSON, PowerShell, context and whitespace
checks. A read-only documentation check verified **36 relative links/anchors**
and balanced fences across all four architecture documents. No dependencies
were installed. These fresh offline results do not retroactively execute the
denied checks recorded by SprintDesign or certify its earlier exact source.
No settings import, cloud inventory, permission change, publication, inference,
Linux-package check or formal acceptance was performed. Lab sources were not
changed; its full retained suite was not rerun. Live path selection remains
unresolved and historical unknowns/held parents remain preserved.

The following results describe the preceding refinement, not this exact source:

Using the existing absolute validated Python 3.12.10 executable with the
explicit lab root, `Test-Demo.ps1` passed dependency checking, **186 offline
tests in 18.803 seconds**, and compilation. `scripts/Test-Repository.ps1`
passed index, public-boundary (**73 public files**), JSON, PowerShell, context
frontmatter and whitespace checks. A local read-only documentation check passed
**34 relative links/anchors across all four architecture documents**, the four
accepted input commit references, lane/join fields and AC1-AC9/G1-G8 coverage.
The index was refreshed using `scripts/repo_index.py`; no paths were added or
deleted. No dependencies were installed.

These source/document results do not select A or B or close AC7's final Linux/
hosting-package requirement. No runtime, lab tooling or permission changed;
the full retained lab suite was therefore not rerun. No settings import, cloud
inventory, permission readback/write, inference, deployment, Linux package
check, formal E2E or live continuity/recovery/isolation test occurred.
The original UNKNOWN and held state are preserved; existing accepted upstream
votes do not supply votes for this sprint architecture refinement.

Architect handoff is this cumulative sprint design, navigable tier contracts
and concrete unresolved-blocker disposition, committed for original Product
Owner, Critic and Red Team review. Reviewer agreement is collected by the
existing loop, not asserted here. No runtime repair or live certification is
part of this handoff. Five consecutive rounds without reviewer-verified new
progress stop blocked; productive rounds remain uncapped.
