# Identity propagation recovery: design and execution plan

## Application objective and definition of done

Deliver one working application with exactly three production hosted roles:
the coordinator runs a native Microsoft Agent Framework workflow and bounded
Microsoft-Decision-1 routing; the remote architect creates/revises a candidate;
the remote reviewer reviews its exact prerequisites; the coordinator validates
and conditionally accepts their immutable Blob artifacts.

The user-facing outcome is a terminal conversation that produces an accepted
synthetic design, remembers changed requirements across turns, resumes after
supported hosting compute stop/resume, and remains separate from another
conversation. A successful upload, HTTP 200, or diagnostic capture is not done.

| Gate | Required evidence |
|---|---|
| G1: release identity | Three healthy, exact version/package bindings on one final bundle; unchanged or explicitly reviewed identities; rollback versions/packages retained |
| G2: remote collaboration | Architect produces a candidate; reviewer consumes that candidate and exact requirements; coordinator accepts matching hashes/revisions/producers through its ETag/fencing gates |
| G3: runtime provenance | Actual managed-identity Blob operations use the private path; immutable requirements/decisions/assignments/outputs and accepted refs are verified |
| G4: routing | Genuine Decision-1 results and final deterministic gates are recorded; no substitute model or local specialist |
| G5: continuity | Initial and followup turns preserve the parent and each role's child session, update requirements and invalidate stale outputs |
| G6: hosting recovery | Supported compute stop is confirmed once; the same parent and children continue with native checkpoints and the effect journal, without duplicate effects |
| G7: isolation | A separate parent has distinct child bindings and artifact scope; its results exclude the first parent's synthetic requirements; existing cross-scope rejection tests pass |
| G8: truthful closure | Pending unknown operations and any accepted risk exception remain visible; positively identified new owned processes/listeners/mounts close; deployed/rollback bindings and historical cleanup limitations are recorded, without false closure |

G6 is supported compute deprovision/rehydration with persistent volume, not
hard-crash recovery. The lab's approved account-wide Blob Contributor grants
mean per-role write ownership and per-parent isolation are application-enforced,
not storage-RBAC or malicious-host isolation guarantees.

## Measured baseline, not assumptions

As last verified on 2026-10-15:

- Before the prospective diagnostic, architect 17, reviewer 15 and coordinator 22
  were active on bundle
  `51064aa426d28d0cfa6b126eac7fce5ab0e9a5a0667267ef105884c1805adde2`,
  with Responses protocol 2.0.0 and unchanged identities.
- The original coordinator22 -> intended23 diagnostic package is
  `03aa0da34942ca66283a37dae8b6edab04ac053291937eebdc2464cdb8f839d9`.
  Before the new attempt, exact GETs returned 404; the original outcome remains **UNKNOWN**. Forensic
  evidence records Publish at 13:54:04.645Z, background execution at
  13:54:55.834Z and a still-running read at 14:01:28.899Z. No terminal,
  launch-source, generated Linux owner or server correlation was recovered.
  Eight owner receipts, five coordinator package receipts and five complete
  workspace seals are foreign; one unsealed workspace is not ownership proof.
  Original mount/cgroup/listener closure is unproven. Negative metadata is
  not a safe resend finding. All role versions must be checked freshly before
  a new attempt; intended23 is not an assumed next version.
- For one exact preserved coordinator22/architect17 pair, coordinator ingress
  has user/call identity; architect ingress has call identity but no user.
  The parent-correlated architect POST used the expected Responses path and
  configured origin and returned HTTP 200. The child failed preparation at
  `NATIVE_HOST_PRINCIPAL`; reviewer execution was not reached.
- The deployed SDK identity path matches eight inspected installed SDK files
  byte-for-byte. Five actual SDK/mock-HTTP probes pass; 109 local pins match.
  Latest full results are 132 application and 138 retained release tests on
  Windows and Linux, with expected platform skips. These are revision-bound gates,
  not evidence for a future changed package.
- Actual live outbound call/context equality is now captured below;
  background-handler entry is not independently established. No platform defect,
  call-ID expiry or new grant is proven.

### Latest executed result: diagnostic exception consumed

The one prospective coordinator publication succeeded: coordinator 23 is active
on `03aa0da34942ca66283a37dae8b6edab04ac053291937eebdc2464cdb8f839d9`,
with unchanged identity; architect 17/reviewer 15 retain their prior common
bundle. The new exclusive owner record preceded prerequisites, mount and dispatch.
Its strict journal binds reviewed sources, exact package/stage and 22 -> 23;
one dispatch, CLI zero and exact active-version readback are recorded.
Publication, runner cleanup and outer cgroup/listener/mount closure are separately
proven. The original attempt and historical cleanup remain UNKNOWN/unproven.

One fresh App/native parent wrote requirements and a genuine Decision-1
`ask_architect`, then held `SPECIALIST_INCOMPLETE`. Read-only exact-parent
observation issued zero inference and captured:

| Boundary | Actual fixed flags |
|---|---|
| Architect outbound at coordinator HTTP edge | `has_call_id=true`, `call_matches_context=true`, `has_delegated_user=false`, `has_container_user=false` |
| Exact architect child SDK ingress | `has_call_id=true`, `has_user_id=false` |
| Exact child preparation | `NATIVE_HOST_PRINCIPAL`; child failed; reviewer not reached |

The parent response completing does not mean specialist work succeeded.
Its operation hold is retained; App and Observe owners closed. R/L/D/T have
executed under the approved exception, not passed G1-G8. The next unmet step
is F's provider-dependent branch: obtain an exact-pair server-side caller-resolution
trace and documented supported platform/SDK remedy. S's packet is prepared and
unsent. No further publication/inference, old-parent replay, speculative grant
or header/principal substitution is authorized. These flags isolate the
investigation boundary; they do not establish a platform defect.

## Recovery design

### Preserve the trust model

The terminal authenticates through the isolated Azure CLI credential. Its
local `state.user` protects the saved client file; it is not the platform
user identifier. Foundry injects the coordinator's user/call context.
The hosting SDK maps the user header through execution context, resilient
input and ambient `FoundryAgentRequestContext`; the workflow captures it.

`NativeRuntime.resources()` intentionally calls `context.platform_headers()`.
The pinned method forwards only the opaque call ID. Foundry is expected to
resolve the caller and inject the specialist's trusted user identity:

```text
Terminal credential -> Foundry -> coordinator trusted user/call context
  -> native workflow -> captured opaque call ID -> specialist HTTP request
  -> Foundry caller resolution -> architect trusted user/call context
  -> accepted candidate -> coordinator -> reviewer through the same boundary
  -> exact review -> coordinator conditional artifact acceptance
```

The first observed missing field is the architect SDK's
`request.headers.get(USER_ID)`, before the native workflow factory. This is
not an identified Python assignment that clears coordinator identity.
The assignment body also contains `scope_binding.principal`, but input data
cannot supply missing platform authority. A session ID identifies an execution
environment; it does not replace authenticated user ownership.

Keep all trusted scope, exact prerequisite, schema/revision, ETag, fencing,
checkpoint and write-ahead-effect gates. Do not add headers or grants by guess,
forward the container-only user header, fabricate a principal, replace user
identity with a session ID, or fall back to local specialists.

Authoritative contracts:
[runtime headers](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agent-contract#platform-request-headers-container-protocol-200)
and [user isolation](https://learn.microsoft.com/azure/foundry/agents/how-to/isolate-sessions-per-user).
Reverify a proposed remedy against the installed pins and supported contract.

### Dispose publication risk independently of inference

Strict historical reconciliation must bind the original package, configured
project/service, operation/owner and terminal outcome. The separate cleanup finding must
establish original ownership and closure or an explicitly reviewed safe
resolution; another observer's cleanup cannot substitute.

Use original receipts/completion or authoritative provider operation evidence.
`diagnose_release.py`, exact-version observation and `InspectOwner` are
read-only aids, not retry grants. A 404, empty log, absent PID/scope or foreign
receipt cannot prove never-sent. Do not repeat those checks without a changed
state hypothesis. An arbitrary new version/package cannot evade this hold.

**One prospective lab diagnostic exception was approved and is now consumed.** The
operator's 2026-10-15 16:17:21-04:00 “implement your recommendation” accepts
the risks of delayed original publication and unproven historical cleanup,
while retaining the original as UNKNOWN. R may pass either by strict historical
reconciliation or by the parent recording this scope-specific risk disposition
for this single new attempt. It is not failed/never-sent/completed/closed,
retroactive proof, a blanket unknown-effect override, or cleanup permission.
The parent owns the private authority and exact attempt/package/version record;
settings, source, docs, model output and journals cannot grant authority.

For that attempt, the corrected retained publisher was required to durably write owner,
launch source, exact package hash, project/service and freshly checked version
binding. Persist fixed, flushed phases and any exposed server operation IDs;
record publication terminal status independently of cleanup, with explicit
UNKNOWN fields when evidence is missing. Require local publisher tests and
release/source/trust gates before D. New journaling cannot repair historical loss.

Recheck all three existing services, exact source/package provenance, preview,
scope and identities. The reviewed `03aa0...` diagnostic package may be used
only if it still matches current source; a rebuild needs its own exact provenance
and review. Isolate the attempt's private output/stage, ports and owner; serialize
the shared publisher. Clean only positively identified newly owned resources,
never unknown or foreign owners. Do not certify original mount/cgroup/listener
closure from new cleanup. If the new attempt's outcome or ownership becomes
unknown, STOP: the exception is consumed and no further retry is authorized.

### Run one discriminating diagnostic, then repair

After publication safety and local release gates pass, verify a scoped
coordinator-only diagnostic preview against the actual active versions.
Reuse a verified completed diagnostic deployment if one is recovered;
otherwise publish only under strict reconciliation or the recorded single-attempt
exception above, after durable publisher readiness. This does not authorize U.
Do not assume coordinator23 is still the correct version to create.

Only after exact diagnostic package/version/identity and NEW owned cleanup are
verified, use ONE fresh synthetic parent, never a held parent. Current common-hash
acceptance requires all roles on one bundle and cannot certify this mixed
diagnostic subset. Use the retained explicit terminal App/native path for
one diagnostic message; retain its new parent/response state on any failure.
Then use bounded exact-response observation, not another inference call.

Capture only parent-response hash binding, fixed target role, actual outbound
call-header presence/equality to captured context, delegated/container user
presence flags, paired ingress presence and correlated route/status/timing.
Do not log IDs/header values, credentials, request content or raw exceptions.
If further background-entry instrumentation is needed, scope and test its
redaction locally and obtain new exact approval before another diagnostic;
no speculative releases or probe matrix before a supported repair.

| Actual observation | Permitted next action |
|---|---|
| Outbound absent/mismatched | Locate the context capture/header merge loss; make a focused fix and a regression that fails without it |
| Outbound matches, child user absent | Provider traces server-side caller resolution for the exact pair; use a documented platform/SDK correction, not an application identity bypass |
| Child user present, later preparation fails | Follow the newly observed gate; do not assume identity repair proves artifact or reviewer success |
| Missing/conflicting capture | Preserve uncertainty and stop live attempts; improve observation locally, not by automatic release/retry; a missing log is not a missing header |

Prepare the provider case in parallel using existing evidence. Request nested
hosted-agent opaque-context resolution and stored/background-response behavior,
not a presupposed defect. Separately request original publication disposition.
Submission/contact requires operator action or exact authorization for its
destination and sanitized contents; documentation alone does not send a case.
An external answer is required before adopting a provider-dependent remedy,
not before preparing local probes or the case.

### Supported-remedy assessment and execution gate

Checked against authoritative public sources on 2026-10-15. **No published
cause-specific fix was identified for this captured boundary.** This is not
proof that no fix exists; a provider response is still required. Do not label
a proposed workaround, unrelated release or this runbook a verified remedy.

The [protocol 2.0 runtime contract](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agent-contract#platform-request-headers-container-protocol-200)
requires forwarding `x-agent-foundry-call-id` unchanged so Foundry resolves the
caller, and explicitly says the container's `x-agent-user-id` is not forwarded.
The [SDK protocol implementation](https://github.com/Azure/azure-sdk-for-python/blob/b29aa0aa60b79cffcb758185634f7b0480cf5f34/sdk/agentserver/azure-ai-agentserver-core/azure/ai/agentserver/core/_request_context.py)
implements that exact rule: `platform_headers()` emits the call ID only.
Forwarding both headers is not a supported correction.

| Candidate | Authoritative evidence and applicability |
|---|---|
| Restore request context in durable handlers | The [Responses changelog](https://github.com/Azure/azure-sdk-for-python/blob/6c4871c93cfab4b5cb23c9476bcef584b8a3fda1/sdk/agentserver/azure-ai-agentserver-responses/CHANGELOG.md) records the fix in 2.1.0b2. Installed Responses 2.3.0 already contains it; the existing real-SDK serialization/handler-entry regression passes. It preserves supplied identity, not a missing ingress user. |
| Repair stale Toolbox call IDs | [Agent Framework issue 7690](https://github.com/microsoft/agent-framework/issues/7690) and [merged fix 9059](https://github.com/microsoft/agent-framework/pull/9059) concern reused MCP writer/session context. This native path creates a request-owned runtime and HTTP resources, not a FoundryToolbox connection, and the measured outbound call matches captured context. That fix is not an evidenced remedy for this pair. |
| Apply the .NET protocol migration | [Agent Framework issue 6799](https://github.com/microsoft/agent-framework/issues/6799) fixes .NET protocol/context propagation. It is not a Python missing-ingress-user fix; this application already uses Responses 2.0.0. |
| Upgrade blindly to the new previews | [Core 2.3.0b1](https://github.com/Azure/azure-sdk-for-python/blob/6c4871c93cfab4b5cb23c9476bcef584b8a3fda1/sdk/agentserver/azure-ai-agentserver-core/CHANGELOG.md) and Responses 2.4.0b1 describe lifecycle/replay/user-partition changes, not a demonstrated correction for this ingress discrepancy. The Responses preview changes stored-state ownership/layout and requires draining active work; it is not a safe speculative upgrade with held work. |
| Send `x-ms-user-identity` instead | [User isolation guidance](https://learn.microsoft.com/azure/foundry/agents/how-to/isolate-sessions-per-user#isolate-sessions-for-your-own-users) defines separate trusted-service delegation, with explicit permission and a server-authenticated end-user identifier. It does not authorize re-delegating a derived container user or treating an assignment principal as authority. This is not the current native opaque-context design's supported fix. |

The installed baseline remains Core 2.2.0, Responses 2.3.0 and
`agent-framework-foundry-hosting` 1.0.0b261002. The remedy assessment rechecked
all 109 lock pins and the five existing offline SDK/transport probes:
native HTTP propagation, durable identity, missing-principal rejection,
redacted wire diagnostics and exact-origin fencing. All pass, without cloud
requests. These checks establish local compatibility, not live identity repair.
No runtime dependency, header, identity permission or deployment was changed
for this assessment.

Proceed through the provider-dependent remedy as follows:

1. Use the prepared unsent case and exact new response pair. Through an
   operator-approved support destination, request the server-side resolution
   of the forwarded call ID, whether a trusted user was resolved before child
   dispatch, and the documented correction for the configured protocol/SDK
   versions. Ask for a causal trace, not a generic recommendation to upgrade
   or grant broader access. Following the operator's broader project-progress
   approval, the private Microsoft Azure Support route was selected and its
   current Microsoft Foundry / Agents / Hosted Agents classification verified
   through the Support REST API. Required contact details and specific private
   locator disclosure confirmation are still missing; no ticket was submitted.
2. Record the actual provider answer, source/case reference, affected versions
   or rollout requirements, and state/identity implications. If it prescribes
   a platform change, obtain its exact scope through the lab workflow; do not
   manufacture a response, reopen the diagnostic exception or mutate RBAC.
3. For an application/SDK correction, first reproduce the specific defect
   offline and add a focused regression that fails before the fix. Preserve
   trusted parent binding, immutable role outputs, exact prerequisites, ETags,
   native checkpoints and explicit unknown-effect holds. Require a supported
   migration strategy before any dependency change that affects held state.
4. Run affected tests, then required application/retained Windows and one
   source-bound Linux gate. Review the new exact package, current versions,
   identity bindings and preview. Use the corrected durable publisher only
   under separately established exact release/inference authority; the old
   single-attempt exception remains consumed.
5. Verify actual live child trusted-user presence, accepted architect and
   reviewer outputs and private managed-identity artifact provenance. Then
   prove final common-bundle G1-G8, including continuity, supported hosting
   recovery and isolation. Never resend a held parent to test the remedy.

**Current execution stop:** submitting step 1 requires an actual support contact
(name, email, country and preferred support time zone/language) and specific
private locator disclosure confirmation. The operator was unavailable when
those fields were requested. A private source-bound draft is retained; contacts
and support entitlement were not invented, no plan was purchased and no ticket
was submitted. Applying a correction separately requires an actual provider
finding. Local assessment and case preparation are complete; implementation
cannot safely proceed by inventing the missing supported correction. Neither
current public documentation nor the passing offline probes establish a
server-side remedy.

## Dependency-analyzed execution plan

`B`, `R`, etc. below are task IDs, not numbered phases imposing barriers.
Start any ready task immediately, subject to the resource locks below.

| ID | Work and objective exit | Hard prerequisites |
|---|---|---|
| B | Read current docs/settings scope, inspect dirty work and existing evidence; distinguish deployed code from diagnostics | None |
| R | Strictly reconcile original disposition/closure OR record the operator-approved single prospective diagnostic risk disposition, preserving original UNKNOWN; record the exact authorized scope | B |
| S | Prepare provider case from existing bound evidence; operator submits if authorized; record authoritative findings when available | B |
| L | Verify durable pre-dispatch publisher evidence, flushed phases/terminal/separate cleanup and tests; check pins, diagnostic wiring and exact source/package/stage provenance with affected local/retained/Linux gates | B |
| D | Verify or safely publish coordinator-only diagnostic and confirm exact version/package/identity/cleanup | R, L |
| T | One fresh synthetic diagnostic parent; observe actual outbound match and exact child ingress; classify the boundary | D |
| F | Implement supported cause-specific repair with regression; if provider-dependent, wait for the relevant S finding | T; S finding only on provider-dependent branch |
| Q | Run affected gates, then full app/retained/Linux release checks as applicable; review scoped changes and final package/preview | F |
| U | Publish consistent final three-role bundle only under separately confirmed final-release authority/risk disposition; reconcile each attempt and confirm exact versions/identities/hash/new owned closure; R's diagnostic exception alone cannot pass U | Q, R; final-release authority/disposition |
| E | Fresh final-bundle initial turn proves G1-G4 and first-parent artifact acceptance | U |
| N | Followup on E's completed parent proves G5 | E |
| H | Supported hosting stop/resume on N's completed parent proves G6 | N |
| J | Independent final-bundle synthetic parent proves G7; compare with E's completed bindings/evidence | U; E for comparison only |
| K | Audit G1-G8, pending holds, cleanup, rollback and truthful docs; commit/push only scoped changes after gates and separate authorization | H, J |

Logical dependency graph:

```text
B -> R ------------------> D
 \-> L ------------------> D -> T -> F -> Q -> U -> E -> N -> H -> K
 \-> S ---- conditional ----------> F          \-> J -----------> K
                                                   E -> J comparison
R -- separately scoped final disposition --> U
```

S is a preparation/external-response lane, not a mandatory global barrier.
If provider evidence already establishes an authoritative supported remedy
and renders a new diagnostic unnecessary, document that evidence and explicitly
replan D/T out of the graph; never run redundant diagnostic inference just to
complete a checklist. Do not skip R or the final acceptance gates. Under the
current exception, D becomes ready only when R's private risk record and L's
durable release gates pass. T still waits for D's verified new owned cleanup;
U and final acceptance do not become authorized by that readiness.

### Parallelism and contention

- After B, run R, S and L independently. R's publication uncertainty does not
  prohibit offline work or case preparation. A missing provider reply should
  not idle available local work.
- After U, J's independent turn may overlap E/N/H only if admission, separate
  parent state and connection ownership permit. J's cross-parent comparison
  waits for E, but J does not wait for followup or hosting restart.
- E -> N -> H is necessarily serial: one parent's state/lease, exact accepted
  artifacts and completed pending state are true prerequisites. Architect ->
  reviewer -> coordinator acceptance is also a true data dependency, not a
  safe place for speculative parallel reviewer calls.
- One publisher at a time per project/service and shared private CLI workspace;
  never run concurrent publishers. An isolated new attempt alongside the retained
  historical uncertainty requires the exact recorded exception, not inferred safety.
  No publisher and acceptance run may race to change the latest version.
- Each connection owns distinct unused ports, jobs, evidence paths and parent
  files. If wrappers share fixed ports/mounts/CLI state, serialize that resource
  or use supported explicit independent ports; do not weaken ownership guards.
- Keep shared Decision-1 admission/budgets and configured capacity enforced.
  Parent independence does not imply unlimited safe inference concurrency.
- Separate app and lab Windows tests may overlap in isolated processes.
  Do not duplicate the full Linux build/test gate across workers; use one
  canonical image/source-bound run covering both suites.
- Use at most three bounded worker lanes if delegation helps: R, S, and L.
  One driver owns integration, publication and acceptance. Assign disjoint
  files/worktrees where needed; report findings without duplicating searches
  or editing another worker's scope. No workflow/agent fleet is required.

### Efficiency validation and feasibility

The DAG is acyclic. Earliest logical readiness is B; then R/S/L; then D;
T; F; Q; U; then E and J's independent run; then N; H; K.
J comparison waits for E but not N/H. Readiness is not a layer-wide barrier.
The known live critical chain is
`B -> (R and L) -> D -> T -> F -> Q -> U -> E -> N -> H -> K`;
S joins only if the repair requires a provider finding. Without durations or
provider response times, no numerical speedup or completion date is justified.
Run stages once per source/package revision; repeat only for changed evidence
or failed checks. Reuse verified receipts/images/calibration without rewriting
historical seals or treating old tests as coverage of new behavior.

Prior documentation validation parsed all 14 task rows and checked both the local-fix
and provider-dependent DAGs for cycles/missing nodes. Splitting J into its run
and comparison gives 15 executable nodes: R/S/L are ready together after B;
E and J-run are ready together after U; J comparison and N are ready after E;
H waits only for N; K joins H and J. All eight objective gates and local
document links were checked, and repository index/public-boundary/parser/
whitespace checks passed for that prior revision. These are not checks of the
new exception or proof of operational execution. This validates planning
structure, not deployment feasibility or live acceptance; resource locks may
reduce actual concurrency.

All G1-G8 have an owner/exit in the plan; neither capture nor provider escalation
replaces final acceptance. The architecture has a plausible route to the
objective, but **success is conditional**, not guaranteed: the approved exception
can unblock only D after R/L pass; it does not automatically unblock U or final
G1-G8 acceptance. Matching outbound context with missing downstream identity
requires supported provider resolution. Stop on a second uncertainty, missing
durable release evidence or unsupported repair. A fourth service, identity bypass,
unapproved SDK upgrade or session-only redesign is not an acceptable shortcut.

## Tooling, evidence and session handoff

Use the existing scripts before adding tools:

| Purpose | Entry point |
|---|---|
| Local pins and five SDK boundary probes | Application `scripts\diagnose_identity.py` |
| Package/phase forensics | Lab `foundry-tf\multi-agent\diagnose_release.py` |
| Exact preserved identity trace | Lab `foundry-tf\multi-agent\diagnose_identity_trace.py` |
| Publisher ownership inspection | Lab `Invoke-WslCodeRelease.ps1 -Mode InspectOwner` |
| Exact versions, one new App/native turn, known-response observation | Lab `Test-PrivateConnectivity.ps1` with explicit mode/scope |
| Source-bound Linux gate and exact release | Lab retained build/package/preview/WSL release chain |

Run application `Test-Demo.ps1 -Python <absolute-existing-python>` with explicit
`-LabRepositoryRoot`; run the retained suite after release-tool changes.
Use `scripts\Test-Repository.ps1` and refresh `scripts\repo_index.py` after
file additions/deletions. Do not install dependencies unless a manifest changed
or a check reports missing tools. Preserve actual Python/runtime distinctions.

Private evidence is outside both repositories. The immediately preceding
session is `68fb3c6e-2469-411e-8e04-ba8b4e793df1`; its `files` directory holds
`identity-combined-diagnostic.json`, `release-phase-diagnostic.json`,
`publisher-inspection-20261015.json`, and
`continue-boundary-20261015-1320\monitor-boundary.json` / `escalation.json`.
The latter is unsent. Its explicit retained-source locators identify the older
session's exact parent, Observe receipt and identity checkpoint. Read those
named artifacts only; never scan session/credential stores for secrets.
`observe_known_boundary.py` in that session's files is a one-case private
read-only query, not a checked-in supported general diagnostic.

Historical application delivery is `efb5abd` (prior scripts `b12d35a`); lab
diagnostics are `a480e34`. Resolve current roots/heads/versions at startup,
not from this document alone. Preserve unrelated lab dirty files.
No cloud, inference, support submission or publication is authorized by merely
reading this plan. The reusable invocation is
[NEXT-SESSION-PROMPT.md](NEXT-SESSION-PROMPT.md).
Session `a99d90b1-7e1d-4be5-9b08-f1844da4117c` retains its private
`files\recovery-exception-v1` directory: `operator-authority.json`,
`approved-attempt.json`, `publication-summary.json`, `diagnostic-summary.json`,
the exact owner attempt/journal/final receipt, App parent and Observe receipt.
The summaries bind exact retained evidence without header values or raw IDs.
Its `files\provider-case.txt` includes the new exact-pair hashes and remains unsent.
The implementation and diagnostic results above are executed, not a fresh
permission grant; the single exception cannot be reused. Current
authority excludes provider-case submission, infrastructure/RBAC/network/DNS/
quota/VM-power/VPN/secret/`azd up` mutation. Provider packets remain prepared
and unsent; original parent inference holds and unmet G1-G8 remain unchanged.
