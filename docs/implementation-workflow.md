# Implementation and lab deployment workflow

This is a checked-in gated engineering process, not a registered dynamic
multi-agent workflow. The native MAF workflow described in `design.md` is the
application being built. Do not launch a large agent orchestration merely
because this document says "workflow."

For the current live identity blocker, use
[identity-recovery-plan.md](identity-recovery-plan.md) for the measured baseline,
publication/inference separation, dependency-ready parallel lanes and G1-G8
completion gates. It specializes this workflow without granting new authority.

Each gate self-approves only when its objective evidence passes. Use explicit
inputs and deterministic checked-in scripts for repeated validation, build,
comparison, preflight and release steps. No routine approval pauses between
gates. Stop for a material unresolved decision, secret boundary, ambiguous
destructive scope, failed gate with no justified remedy, user authentication,
VPN-server execution, or unapproved mutation.

## Gate 1: Scope and baseline

Read README, Copilot instructions, index, design, migration map/plan and this
workflow. Load ignored private settings without displaying their values.
Resolve the external lab repository; read its startup, infrastructure workflow,
registry, network design and affected roots before changing it.

Pass: cleanly distinguish existing baseline from planned behavior; account for
every retained capability and relevant dirty change; validate configured
project/region/aliases; establish existing offline test results. Preserve
source snapshots, old sessions and unrelated changes.

## Gate 2: Application contracts and native workflow

Implement strict versioned artifact/assignment/manifest/operation schemas,
typed Blob adapters, identity binding and per-role access; native checkpointed
MAF orchestration; remote Responses specialists; Decision-1 contract validation
and bounded routing/admission control. Preserve the recoverable write-ahead
effects journal. Model outputs cannot grant authority or publish themselves.

Pass: focused tests cover publication crash boundaries, ETag/fencing conflicts,
immutable duplicates, parent isolation, malformed/stale output, response
recovery, unknown-effect holds, native checkpoint resume, routing prerequisites
and provider errors; the complete application suite passes with existing pins
or a documented compatible update. Three production deployments use remote
mode with no silent local fallback. Legacy session policy is explicit.

## Gate 3: External lab infrastructure

Any infrastructure/network/DNS/monitoring/region change follows the external
lab's `docs\infrastructure-change-workflow.md` in full. Use AVM-first Terraform,
private connectivity and managed identities. Keep Terraform and environment
resource definitions in the lab, not here. Derive region/subscription/address
allocations from `ip-registry.json`, register VNets before planning, validate
and perform fail-on-stale pruning; never automatically delete stale entries.

Pass: lab design/registry/implementation/security/cost gates pass; private
Blob identity/network permissions and hosted compute reachability are proven
in design and preflight, not assumed. Private DNS additions include both
private/public-equivalent VPN forwarding entries in the same change. Update
lab `docs\network-design.md` for topology/operational-boundary changes.

Commit and push only scoped non-secret changes after repository checks and
the required review. Inspect the exact staging list. This does not deploy the
VPN-server configuration and does not authorize unrelated changes.

## Gate 4: Verified Terraform execution

Run these commands **from the external lab root** for the registered region:

```powershell
.\scripts\Connect-LabAzure.ps1 -Region <region-key>
.\scripts\Invoke-HubDeployment.ps1 -Region <region-key>
```

The first command uses the repository-local `.azure-cli` profile and
`az login --tenant <registered-tenant-id> --use-device-code`. Communicate the
displayed device URL/code and continue after the user completes authentication.
Verify selected tenant/subscription before resource queries. Do not use normal
production credentials, browser login or cached context as a substitute.

The deployment wrapper enforces registry validation and monitors Terraform
init, fmt/check, validate, plan and apply. Default: apply the **exact saved plan**
immediately after successful plan. Pause between plan/apply only if the user
explicitly requested plan approval. Never bypass the wrapper to execute another
root or unverified context.

On failure, diagnose the concrete output, make the smallest coherent fix,
rerun affected gates, commit/push the safe fix, and retry. Stop for secret or
material scope boundaries; do not replace Terraform with ad hoc Azure writes.
Read-only Azure metadata queries are allowed in verified lab context, except
secret/key/token/connection-string retrieval. Ad hoc mutating scripts require
explicit approval of the complete script and exact resource scope.

## Gate 5: Cross-repository application release

Adapt the **lab-owned** release tooling to accept explicit application and lab
roots before invoking it. Test the original root and new root against all
source/package/preflight/WSL paths. Preserve strict host verification, temporary
read-only SSH mount authorization, private evidence outside both repositories,
native Linux build/tests, package allowlists/ELF checks, pinned provenance,
approved ZIP/hash/version/service scope and process/mount cleanup.

Create the package from this repository's code, never from a stale copy in the
lab. Include new modules and declared dependencies intentionally. Produce an
exact hash and sanitized preview mapping the three target services to the
approved project and expected versions. Do not run `azd up`, `azd provision`,
or an unreviewed direct publish shortcut. The copied `.azure` directory is
private context, not release authority.

Pass: all applicable portable and retained release tests pass; package preview
matches the intended source/lock/roles; the exact publication and existing
version use are covered by the user's invocation or a new specific approval.
If the wrapper requires an approval not supplied by that invocation, ask rather
than bypass it. The current next-session scope is the single prospective
coordinator diagnostic exception; final publication/live acceptance require
separately confirmed authority within the configured existing project.
That single diagnostic scope is now consumed. The corrected publisher
successfully activated coordinator 23 on the diagnostic bundle with exact
source/package/version binding, unchanged identity and independently proven
runner/outer cleanup. One fresh App/native parent and its read-only observation
captured matching actual outbound call context but no trusted user at the exact
architect child (`NATIVE_HOST_PRINCIPAL`). App/Observe owners closed; the held
parent and original publication UNKNOWN remain. Resume the provider-dependent
supported-remedy branch, not D/T or another speculative release. The mixed
diagnostic bundle does not satisfy final G1-G8 acceptance.

A publish timeout is not permission to resend. Inspect the existing operation/
receipt/version and reconcile uncertain sends first. The only alternative here
is the explicitly approved single prospective diagnostic risk disposition in
the recovery plan: it retains the original UNKNOWN and does not authorize replay
or final U. R's exception plus L's local durable publisher/release gates can
make D ready, not final acceptance. Keep retries bounded; a new unknown outcome
or ownership consumes this exception and stops further attempts.
Record deployed versions and rollback package/versions privately.

For an authorized new diagnostic or corrected release, the lab's `bundle_package.py runtime`
mode creates an exclusive, deterministic allowlisted source archive using explicit
application/lab roots and a private `--output`. It does not read or change an
azd environment or upload code. `Build-BundledCodePackage.ps1 -OutputPackageName`
selects a new basename inside the existing private output directory, preserving
the previous ZIP, seals, receipts and pinned private azd configuration. Use a
new staging directory for an authorized attempt, not to evade an unknown hold;
verify its exact image, source/archive hashes, package
closure and preview before the retained publisher. Never edit a sealed stage
to turn a failed release into a different package.

Load the exact calibrated `DEMO_FACT_SHEET` with the native settings before
packaging. `scripts\calibrate_routing.py --validate-runtime` is an offline,
read-only gate; retained packaging invokes it before dependency extraction.
Facts are allowlisted, committed into the private settings proof and forwarded
to all roles. Historical ten-field snapshots remain verifiable but do not
authorize a new descriptor requiring facts. Do not recalibrate or rewrite
observations merely to bypass configuration drift.

## Gate 6: Live acceptance and handoff

Use synthetic requirements only and private evidence outside both repositories.
Prove native workflow restart/resume, distinct specialist child sessions,
remote invocation, exact artifact prerequisites/hashes, conditional coordinator
publication, Decision-1 outcomes, private MI Blob access, and isolation between
parents. Verify actual service versions/health and the terminal path. A live
test must not query secrets or use real customer documents.

The retained wrapper supports individual `-AcceptanceScenario` selections.
`followup`, `recover` and `restart` require an existing private parent within
the evidence directory. `recover` retrieves its known pending response only.
`restart` requires `-HostingRestart`; full Acceptance with that switch runs
initial/followup/restart/isolated and checks parent/child continuity and
separation. The supported hosted-compute stop/resume API preserves the session
volume; it does not prove hard-crash recovery. Preserve uncertain stop markers
and pending responses rather than sending either operation again.
Native acceptance validates returned artifact envelopes/hashes, exact reviewer
prerequisites, accepted content, producer sessions/versions and decision records,
not just a success-shaped final message.

Current live blocker: the nested architect fails SDK preparation at
`NATIVE_HOST_PRINCIPAL`, before the application factory. The pinned-SDK
HTTP-edge regression preserves the delegated identity headers and read-only
RBAC inspection confirms the coordinator's explicit impersonation grant.
Follow the supported [delegated-user isolation contract](https://learn.microsoft.com/azure/foundry/agents/how-to/isolate-sessions-per-user)
and inspect the platform/SDK propagation path; do not add speculative storage
grants, synthesize a trusted user or relax the hosting scope gate. The first
operation remains held, so continuation/restart/isolation were not reached.
The reviewer release reported a nonzero CLI exit after version 14 became
active with the exact hash. Its observed receipt was reconciled without
resending; only the coordinator, explicitly never attempted in that receipt,
was published separately. Preserve both receipts and all rollback packages.
Local observation now accepts only SDK ingress identity-presence booleans bound
to the exact known response ID. This separates missing inbound platform headers
from possible later SDK context loss without logging private header values.
The pinned SDK's offline durable-input/handler-entry regression preserves valid
identity and rejects either missing user or missing call identity. A subsequent
read-only observation stopped at SSH because the existing lab command VM was
deallocated; owned listeners/processes were proven closed. Do not power it on
without exact operator approval. Existing Azure Monitor query access subsequently
provided exact-response ingress evidence without that VM: coordinator user/call
present, architect user absent/call present, correlated Responses POST HTTP 200.
Queries returned only presence flags and fixed request/status classifications,
not raw log messages, header values or tokens. No matching service audit record
or captured live outbound headers was found; absence of capture is not proof of
header absence.
The deployed native propagation change uses the SDK's opaque-call propagation
method, `context.platform_headers()`, instead of applying the legacy helper's explicit
user re-delegation to internal Foundry calls. A real-resource/client transport
regression verifies exactly one request, correct endpoint, JSON session binding
and only the SDK's caller-context header; its assertions run outside the SDK
exception boundary so a wrapped assertion cannot falsely pass the probe.
Following explicit operator approval, the existing command VM was started and
fresh guarded connectivity passed. Architect 17/reviewer 15/coordinator 22 are
active on bundle
`51064aa426d28d0cfa6b126eac7fce5ab0e9a5a0667267ef105884c1805adde2`.
All three CLI publications exited zero, exact package hashes were checked
before upload, identities were unchanged, and cgroup/listener/mount closure
passed. Fresh full acceptance was requested with `HostingRestart`, but stopped
on its initial turn: `SPECIALIST_INCOMPLETE`. Read-only observation of the exact
new child proves architect 17 again receives call identity without user
identity and fails `NATIVE_HOST_PRINCIPAL`. Both owned connections closed.
The SDK-supported propagation change did not resolve the live failure.
Its cause remains unresolved; do not infer a platform defect, add speculative
grants, restore an unsupported container-only header, substitute a principal,
or clear/resend either held operation. Followup, restart and isolation did not
run. Further remediation requires a supported, evidence-backed propagation
path; publication alone is not acceptance.
Local diagnostics now close the missing live outbound-header observation:
native resources bind the HTTP transport to their captured call context and
response-ID hash. Only actual POSTs to the three known hosted Responses paths
emit fixed-role presence/match booleans; no raw values or content are logged.
The legacy transport is unchanged. Read-only known-child observation also
reads the exact parent's logs, retaining each stream's 30-second/128-KiB bound.
This diagnostic change is not deployed and does not prove propagation or
authorize a replay. Its real-resource/client/transport regression and all
116 application tests pass on Windows/Linux; guarded publication must precede
any claim about live outbound headers.

The [runtime contract](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agent-contract#platform-request-headers-container-protocol-200)
and [protocol migration guide](https://learn.microsoft.com/azure/foundry/agents/how-to/migrate-hosted-agent-preview#container-protocol-200)
explicitly include calls to **other agents** in opaque-call propagation.
They keep the platform-injected user identifier container-side. External
middle-tier delegation examples do not establish a different supported nested
identity mechanism or precedence when both headers are supplied. Do not treat
reintroducing user delegation as an evidenced fix for this failure.

An interrupted diagnostic publication must be disposed independently of
inference. Latest-agent metadata establishes the currently active version, not
the absence of another version or the original publisher's outcome. An empty
log or missing local PID likewise cannot authorize another publication.
Inspect exact version metadata and original release ownership through bounded
read-only tooling; preserve the original UNKNOWN when either remains unresolved.
For the operator-approved ONE prospective diagnostic exception, retain the
delayed-original-publication and unproven historical-cleanup risks in the
parent's private exact authority/attempt record. Before dispatch, the corrected
publisher must durably bind owner/launch-source/package/project/service/version,
persist fixed flushed phases and exposed server IDs, and record publication
terminal independently of cleanup with explicit unknowns. Local publisher tests
and all source/package/trust gates must pass; this cannot repair historical loss.
Freshly check all existing services and reviewed package/source provenance, not
an assumed next23. Isolate new output/stage/ports/owner; serialize the publisher.
No unknown-owner cleanup or certification of original mount/cgroup/listener
closure is allowed. New unknown outcome/ownership means STOP, exception consumed.
After exact diagnostic version/package/identity and new owned cleanup pass,
ONE fresh synthetic App/native parent and exact-response read-only observation
are permitted. Mixed diagnostic deployment is not common-hash final acceptance.
Mismatch means precise wiring fix/regression; matching context/missing child
user requires supported provider resolution. Missing capture is not header
absence and does not authorize speculative releases. Original inference holds
remain. Provider packets are unsent; no provider-case submission or infra/RBAC/
network/DNS/quota/VM-power/VPN/secret/`azd up` mutation is included.

Identity troubleshooting is independent of publication reconciliation. Run
`scripts\diagnose_identity.py` with the pinned Python environment to audit the
lock and exercise the existing real-SDK mocked HTTP, durable-context,
missing-principal, diagnostic-redaction and origin-fencing regressions.
Supply only an explicit sanitized trace to `--trace`: schema version 1,
boolean `correlation_verified`, `observations` with role, exact-response binding
and user/call presence, and optional `outbound` with role, exact-response binding,
call presence/context match and delegated/container user presence.
Unbound observations or separately observed roles do not establish a call chain.
An ingress discrepancy does not prove the live outbound call matched its
captured context. Missing wire evidence remains the next discriminator, not
proof of a platform defect or permission failure. The script returns exit 2
while the live cause is unresolved, including when all offline probes pass.
Optional exact-version deployment metadata is allowlisted separately from
historical per-response flags; healthy protocol metadata cannot establish
the identity context of a particular nested request. The retained lab's
`diagnose_identity_trace.py` extracts bound evidence without replay, and
`diagnose_release.py` verifies the explicit ZIP/seal and reports publication
phase hypotheses against a pinned source revision. The latter confirms the
provided successful receipt belongs to the previous package, not diagnostic
23. Buffered child output and final-only receipt persistence explain why an
empty outer log cannot identify the failed phase; neither is proof that an
upload occurred or never occurred.

The follow-on read-only Azure Monitor observation binds the exact preserved
coordinator 22 / architect 17 response pair through the existing observer
receipt and checkpoint. Within a ten-minute window, coordinator ingress at
13:20:17.972678Z contains both user and call identity; architect ingress at
13:20:41.821326Z contains call identity only. The parent-operation-correlated
POST at 13:20:41.599649Z returned HTTP 200 and matches the expected architect
Responses path and configured project origin. Two correlated response GETs
also returned 200. These are 2026-10-15 historical request timestamps, not new
inference. No outbound context-match diagnostic was captured, and dependency
properties contain no call-header-name capture; neither absence establishes
an absent header. Request admission is not successful agent execution.
This narrows wrong-endpoint/origin and parent-ingress hypotheses without
proving a platform defect, call-ID expiry, or background-entry behavior.
Another exact coordinator-23 observation still returns 404 and proves its own
observer cleanup only, not the original publisher's outcome or mount closure.
Live wire capture requires verified diagnostic publication/new owned cleanup
after either strict reconciliation or the recorded single prospective exception
and durable local release gates; this document does not report execution.

Pass: all live acceptance criteria in `design.md` succeed; no pending unknown
operation is concealed; rollback/version/session compatibility is documented.
G8 must disclose any accepted exception and unproven historical cleanup, not
certify original closure from a new attempt's cleanup. Diagnostic approval
alone does not pass U or G1-G8.
If unavailable, state exactly which condition failed. Do not label offline
coverage or a successful ZIP upload "deployed and verified."

Never connect to or change the VPN server. If configuration delivery is needed,
provide branch/commit, `cd ~/azure-lab`, pull/diff-review instructions, exact
installation target, expected impact, validation, restart, rollback and secret
handling. Do not read or stage `conf\ipsec.secrets`. A Git push is delivery only;
the VPN-server deployment remains incomplete until the user confirms install
and verification. Such a dependency is a documented stop, not a reason to
claim end-to-end success.
