# Identity profiling: workflow execution input

## Objective and current boundary

Implement paired HTTP transport, server-ingress and SDK-context diagnostics,
then use their findings to correct supported coordinator-to-specialist identity
propagation and complete the existing three-role prototype acceptance.
This is a material construction/remediation increment, not an unchanged
DevOps-only retry. Use the current `lab-delivery` owner/reviewer workflow.

The latest observed deployment succeeded for all three roles, but its initial
live turn failed architect preparation with `NATIVE_HOST_PRINCIPAL`. Outbound
delegation-header presence was observed; the architect's resolved trusted user
identity was absent. The actual authenticated outbound principal and effective
platform delegation resolution remain unproven. Neither missing RBAC nor a
platform defect has been established.

The prior parent is held at `SPECIALIST_INCOMPLETE`. Preserve it and all known
response IDs and unknown effects. New instrumentation cannot retroactively
observe its original HTTP ingress. Do not resend that operation to obtain logs.

## Source findings and implementation

The reference is `RequestResponseProfilerPolicy` in
[foundry-hosted-agent-profiled/server_host.py](https://github.com/hoopdad/foundry-hosted-agent-profiled/blob/main/server_host.py#L196-L254).
It records Azure Core client timing, sanitized URL, status and exceptions, not
headers. It is attached to credential/Blob clients; it is not a universal
inbound/outbound interceptor. Reuse its profiling approach, not its entire
storage-probe server, DNS monkeypatches or invocation protocol.

The application pins `azure-ai-agentserver-core==2.2.0`,
`azure-ai-agentserver-responses==2.3.0` and
`agent-framework-foundry-hosting==1.0.0b261002`. Examination of matching local
SDK source established that the receiving Responses endpoint reads
`x-agent-user-id` into its execution context and request context. It does not
populate `user_id` directly from `x-ms-user-identity`.

```text
Coordinator trusted request context
  -> specialist header construction / client defaults
  -> actual outbound HTTP request: x-ms-user-identity
  -> Foundry platform: resolution is not visible inside application code
  -> specialist raw ingress: x-ms-user-identity / x-agent-user-id presence
  -> SDK execution context / resilient background context
  -> request.scope.user_id and get_request_context().user_id
  -> trusted scope and exact assignment validation
```

1. Extend `demo\foundry.py`'s existing `OriginTransport` for relevant outbound
   Foundry requests, responses and exceptions. The inner OpenAI Responses
   client uses this `httpx2` transport, not an Azure Core policy pipeline.
   Retain exact-origin enforcement, TLS, no redirects and zero automatic
   retries. Do not consume or buffer streaming bodies to profile them.
2. Add pure-ASGI ingress/response middleware to the existing
   `ResponsesHostServer` in `demo\host.py`, using the pinned host's public
   `add_middleware()` extension point before `run()`. Observe raw request
   headers before SDK parsing; pass ASGI receive/send through without changing
   bodies, disconnect handling, streaming, background execution or cancellation.
3. Add safe context checkpoints at the workflow-preparation boundary and the
   request/background execution boundaries reachable through supported hooks.
   Distinguish absent, empty and nonempty identity values. Record both scope
   and request-context presence and safe equality checks where the values are
   expected to have the same representation. Do not populate trusted context
   from arbitrary inbound values just to make a diagnostic pass.
4. Profile other relevant application-controlled outbound SDK clients through
   their supported Azure Core policies where needed: session creation/lookup,
   storage/checkpoint calls and credential acquisition. Inventory actual paths;
   explicitly identify any SDK-internal calls not covered. Do not claim that
   installing one policy covers all transports or the Foundry gateway.
5. Correlate events with the existing operation/response bindings and
   allowlisted request/trace correlation metadata. Distinguish request send,
   HTTP response headers, stream completion and execution completion. A
   successful HTTP status is not a successful agent turn.

Log structured, bounded diagnostics: role, stage, method, sanitized route,
header/context presence, safe match results, timing, HTTP status and error
category. Do not log raw user identity values, bearer tokens, credential
responses, complete headers, bodies, query strings or private settings.
Do not introduce a shared logging secret or new infrastructure as a diagnostic
prerequisite. Logs remain private evidence; no external upload is authorized.

The literal public delegation header need not survive unchanged into the
container. Compare its presence with the platform-delivered `x-agent-user-id`
and resolved SDK identity. Platform identity translation or loss must not be
inferred merely from absence of `x-ms-user-identity` at ingress.

## Required acceptance

1. Focused offline tests demonstrate the new checkpoints, missing/empty header
   handling, header-name casing, concurrent-request isolation, redaction,
   outbound failures and unchanged streaming/cancellation behavior. Include
   resilient background context and known-response-only recovery regressions.
   Show that diagnostics themselves neither authorize a request nor suppress
   an existing rejection.
2. Run the documented application and repository checks with an explicit
   existing Python and explicit linked lab root. Run affected retained lab
   release checks if release tooling changes; preserve baseline cases.
   Install dependencies only after a manifest change or missing-tool failure.
3. Original owners/reviewers assess the bounded correction, supported pinned
   SDK hooks and remaining uncertainty. Preserve exactly three hosted roles,
   remote specialists, deterministic gates before Decision-1 choices, trusted
   parent binding, immutable role outputs, exact prerequisite refs, ETag
   publication, MAF checkpoints and write-ahead unknown-effect holds.
4. Publish a reviewed, tested, newly identified common package through the
   retained lab release procedure when required. All three roles must use the
   same new package. No deployment of unchanged code just to manufacture work.
5. After current-effect readiness, use a separately identified synthetic
   diagnostic invocation when new live traffic is necessary. Record its
   purpose and effect intent before sending. Never reuse the held operation
   or call retrieval a new invocation. Collect evidence and prove attributable
   cleanup for newly owned processes/listeners.
6. Localize the identity failure to the observable interval. Correct only a
   source/SDK/configuration defect justified by evidence and supported
   contracts, then repeat affected checks and guarded release/acceptance.
   No guessed header substitution, call-ID-as-user value or trust-gate removal.
7. The final goal remains the existing AC1-AC9/G1-G8 acceptance: completed
   non-held initial collaboration, same-parent follow-up continuity,
   once-only supported stop/resume, separate-parent isolation, original
   review/retro/closeout and attributable cleanup. A good diagnostic report,
   agreed partial outcome or SDK-completed envelope is not release acceptance.

## Execution authority and nonblocking operation

The October 21 overnight handoff requests autonomous workflow execution,
monitoring, evidence-based remediation and changed-condition reruns. It covers
routine scoped source/test/documentation corrections, original-role review,
normal checks, dependency restoration when justified, reviewed commits/pushes
and guarded repeated packaging/publication of the three existing nonproduction
roles. The private launch input binds the actual repositories and evidence.
The operator launches the next session; preparing this document does not start
the overnight run.

Do not ask again for routine operations already within that scope, including
the documented test commands, index refresh, current package creation and
retained publication procedure. Historical one-shot/manual-approval wording
does not impose a fresh user approval on those newly authorized operations.
An actual CLI/policy denial still cannot be bypassed.

The historical COMMON rollback ZIP/build-provenance prerequisite remains
explicitly user-waived for this nonproduction release. Record it as WAIVED,
not PASS. Do not recreate it as a prerequisite. Current package/source/version
bindings, trusted-host checks and current-operation effect readiness remain:
calculate them automatically, explain material mismatches and repair stale
current references when justified. Do not invent manual checksum sign-offs,
freeze new work to historical planning hashes, or reseal historical evidence.

No new infrastructure, RBAC grants, quota/network/DNS/registry/VPN changes,
production-profile use, secret retrieval, provider-case submission,
destructive history changes or uncertain-effect replay is authorized by this
handoff. These boundaries are not routine test approvals. If authoritative
platform tracing or another external action is genuinely required, prepare a
private bounded handoff and continue all independent authorized construction.

## Before leaving the session unattended

Use the latest reviewed local controller distribution and Studio, preserving
their dirty source, project instructions and historical runs. Compare source
and installed bytes at an inactive boundary; update only when there is actual
drift. Do not modify a live run's runtime, input or workflow definition.

Preflight the actual execution route, not only a JSON parser: tool permission
mode, all explicit sibling/evidence roots, extension loading, supported
workflow registration, CLI authentication, dedicated lab authentication,
retained connectivity, required tools and the current launcher. Confirm the
operator can execute the normal checked-in test entry point and original
workflow agents have equivalent scoped execution permissions. A launcher's
`--check-only` proves configuration readability, not child-agent execution.
Resolve an actual denial through supported operator permission controls
before unattended execution; do not retry the same denied call through another
tool. Do not alter global CLI policy or claim a permission-propagation fix
without evidence.

Autopilot continuation, tool approval, path/URL approval and user-question
suppression are different settings. The installed CLI help reported a default
of five programmatic continuations, while current online reference described
an unlimited default. Do not silently rely on an assumed default or guess an
unlimited sentinel. Prefer the interactive `/autopilot` handoff, inspect its
effective limits and resolve unintended continuation limits before leaving it.
Do not add workflow sprint/attempt/credit/time caps the user did not request.
Keep existing application safety budgets; this handoff does not remove them.

## Monitoring, remediation and completion

Use the supported launcher from the delivery workspace and its original
owner/reviewer loops, with a fresh immutable correction input referencing this
document and the private historical handoff. Do not use the old four-node
DevOps-only definition for the construction increment. Use the latest full
loop definition for delta planning/construction and carry accepted prior work
as evidence, rather than rebuilding its original backlog.

Maintain one monitor for the exact current run. Persist run/session IDs,
launch directory, input/specification paths, actual approval mode, monitor
identity and the current next action in the new session's durable state.
Observe workflow-owned agents through Studio/supported workflow observation,
not ordinary agent messaging or SQLite writes. Monitor source outputs,
process health and bounded file/journal metadata as well as phase changes;
slow workspace preparation is not proof of inactivity.

Inspect the real application outcome and original reviews at each stop.
Localize failures; let existing Architect/Scrum coordination split and schedule
independent useful work. Remediate justified defects and invoke a changed,
reviewed continuation through the appropriate original roles. Preserve prior
inputs/results; no unchanged retry carousel, cap reset, duplicate publisher,
accepted-work replay or hidden local specialist.

Stop only on verified completion or an evidenced boundary after a
work-exhaustion audit. Persist what is implemented, locally verified, deployed
and live-accepted separately, exact remaining criteria, owned-effect cleanup,
and the smallest genuine external unblock action. Do not describe the session
as unattended-ready until its permission/authentication preflight is proven.
