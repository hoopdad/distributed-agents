# distributed-agents

Three Microsoft Foundry hosted agents: a coordinator, an architect, and a
reviewer. This repository owns reusable application code, contracts, tests, and
generic configuration. Infrastructure and environment-specific connectivity
remain in the separate Azure lab repository.

**Status:** native Microsoft Agent Framework (MAF) workflow and shared Blob
artifact-plane source are implemented; 132 application tests pass on Windows
and Linux/amd64 (seven expected Windows-only skips on Linux).
`azure.yaml` selects native orchestration and remote hosted specialists; the
legacy handwritten/in-process adapter remains available for regression tests.
**Deployed, but not live-accepted:** architect 17 and reviewer 15 retain bundle
`51064aa426d28d0cfa6b126eac7fce5ab0e9a5a0667267ef105884c1805adde2`.
Coordinator 23 is active on diagnostic bundle
`03aa0da34942ca66283a37dae8b6edab04ac053291937eebdc2464cdb8f839d9`;
coordinator 22 and earlier versions/packages are retained. Identities are unchanged.
This intentional mixed diagnostic deployment is not final common-bundle acceptance.
Earlier diagnostics identified `DECISION_CALIBRATION_PROVENANCE`: the Windows loader
represented absent `DEMO_FACT_SHEET` as an empty variable during calibration,
whereas deployment omitted it and used the public nonempty default. The loader
now truly removes absent settings; native release requires explicit nonempty
facts, forwarded to all roles and validated before packaging. A genuine fresh
calibration with those facts exposed a missing-workload routing ambiguity.
Routing-v3 clarifies that facts supply constraints, not a missing user purpose.
The corrected facts and genuine calibration are deployed. The first live turn
passed preparation, wrote requirements and a routing decision, then held the
architect operation after timeout. Read-only exact-response observation confirms
the architect failed during SDK hosting preparation (`RuntimeError`, provider
`storage_error`), not a proven storage permission failure. The known parent and
child IDs and uncertain operation remain preserved without resend.
Deployed diagnostics identify the exact architect gate:
`NATIVE_HOST_PRINCIPAL`. The SDK receives no trusted user identity before the
application factory can run. An actual pinned-SDK HTTP-edge regression confirms
the outgoing delegated-identity headers are preserved; read-only role inspection
confirms the coordinator already has the explicit documented
`UserIdentityImpersonation/action` permission. The remaining blocker is trusted
identity propagation, not evidence for additional storage grants.
Deployed native clients recover stream errors only through persisted response
IDs; unknown effects remain held. Continuity, hosting stop/resume and isolation
were not reached. A supported platform/SDK identity-propagation remedy remains
required; a session string, model output or copied user header cannot replace
the missing trusted hosting identity.
Offline regression also verifies that the pinned SDK preserves supplied
identity through durable background-task serialization and handler entry, and
rejects missing identity. Local read-only observation can extract only ingress
identity-presence booleans for the exact known response. An earlier observation
could not connect because the approved lab command VM was deallocated. Existing
Azure Monitor query access subsequently confirmed the known coordinator's
ingress has both user and call identity, but the known architect's ingress
has call identity only; its correlated Responses POST returned HTTP 200.
Those observations do not expose header values or prove the live outbound
headers, which telemetry did not capture.
**Deployed propagation change, still blocked live:** native internal calls use
the pinned SDK's `context.platform_headers()` directly. Its documented contract
resolves caller context from the opaque call ID; native code no longer re-delegates the already-derived
platform user ID or forwards the unsupported container-only user header.
The legacy adapter remains unchanged, and missing trusted identity still fails
closed. A real resource/client/HTTP-edge regression fails before this change and
passes after it, with exact endpoint and JSON session binding. After explicit
operator approval, the existing command VM was started and fresh guarded
connectivity passed. Publication of all three versions succeeded with exact
package hashes, unchanged identities and proven process/mount cleanup.
Fresh initial acceptance nevertheless held `SPECIALIST_INCOMPLETE`. Read-only
observation of that exact child confirms `NATIVE_HOST_PRINCIPAL` again:
architect 17 receives call identity but no trusted user identity. The supported
SDK propagation change did not resolve the live failure. Its cause remains
unresolved; neither a platform defect nor a different permission grant has
been established. Followup, hosting restart and isolation were not reached.
Both acceptance and observation closed their owned jobs/listeners.
**Diagnostic deployed and exercised:** the native HTTP transport records only
fixed-role presence/match booleans at the actual specialist Responses POST
boundary, correlated by a hash of the parent response ID. It never logs header
values, tokens, identities, request content or the raw response ID. Read-only
observation also reads the exact parent's bounded logs when its known child
fails. One approved prospective coordinator-only publication succeeded with
durable pre-dispatch source/package/version/owner evidence and separately proven
runner and outer process/listener/mount cleanup. One fresh synthetic parent
then wrote requirements and a genuine Decision-1 result but held
`SPECIALIST_INCOMPLETE`. Exact-response read-only observation captured the actual
architect outbound call header: present and equal to the captured SDK context.
No delegated-user or container-user header was sent. The exact architect child
still received call identity without trusted user identity and failed
`NATIVE_HOST_PRINCIPAL`. Diagnostic and observation jobs/listeners closed.
The instrumentation gap is closed; this is not a
verified identity-propagation fix or authorization mechanism. Legacy transport
and all request/scope gates remain unchanged.
The single-attempt exception is consumed. The original interrupted publication
remains `UNKNOWN`, with original ownership/cleanup unproven; the new successful
attempt does not reconcile it. No held turn was resent or cleared. The next
step is a provider trace of the exact new pair and a supported platform/SDK
remedy, not another speculative publication, identity bypass or permission
change. No platform defect has been proven; the prepared provider case is unsent.
The lab's scoped
artifact infrastructure apply added 14 resources; a subsequent scoped plan/apply
confirmed zero changes. Read-only metadata verifies private containers, retained grants
and retention. Completed remote specialist work, end-to-end managed-identity
artifact provenance, parent isolation and actual hosting
restart remain unverified. Publication and metadata do not establish those gates.

**Approved lab permission model:** the linked lab now grants its project agents
account-wide Blob Contributor access. The original container grants remain, but
do not provide effective per-role isolation. Role ownership, immutable output
handling and coordinator publication are enforced by trusted application code,
not by storage permissions. This is not a storage-enforced isolation guarantee.

**Calibration verified:** four twelve-case evaluations are preserved (48 real
calls): the first failed, the second passed with blank facts, the third
identified a missing-workload error with nonempty facts, and routing-v3 passed
all eight ready and four missing-input cases. The unchanged selection algorithm
chose threshold 0.5/margin 0 for the new observations; no expected label, corpus,
coverage requirement or observation was edited. The historical calibration is
retained byte-for-byte privately and in Git history. The genuine new result is
`config\routing-calibration.json`.

## Start the next implementation session

Open this repository in Copilot and submit the invocation in
[docs/NEXT-SESSION-PROMPT.md](docs/NEXT-SESSION-PROMPT.md). It establishes scope,
the gated implementation/deployment workflow, safety boundaries, and acceptance
criteria. Repository instructions, two bounded agents, three project skills,
and a repository index are included; no external plugin is required.

For the current identity blocker, the
[recovery design and dependency-analyzed plan](docs/identity-recovery-plan.md)
defines the application objective, parallel investigation lanes, publication
reconciliation, diagnostic decision tree and final live acceptance gates.
The next-session invocation resumes that plan rather than rebuilding the app.
Its supported-remedy assessment cites the current runtime contract and relevant
SDK fixes: none reviewed establishes a correction for the captured missing-user
ingress. The provider-dependent execution gate remains blocked; no speculative
dependency upgrade or identity-header workaround was applied.

Read the [design](docs/design.md), [migration plan](docs/migration-plan.md), and
[implementation workflow](docs/implementation-workflow.md) first. The exhaustive
[migration map](docs/migration-map.json) accounts for every original application
file. Originals and lab release tooling have not been deleted.

## Configure the baseline

Use Python 3.13 and PowerShell 7.2+. The hosting SDK is preview and its existing
dependency versions are pinned in `requirements.txt` and `requirements.lock.txt`.
Review the configured package index before installing in a new environment.

```powershell
python -m venv .venv
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\Test-Demo.ps1 -Python .\.venv\Scripts\python.exe
```

Offline tests use synthetic configuration and mocked Foundry/storage boundaries;
they do not need Azure login. Windows connectivity wrapper regression cases
require the optional `-LabRepositoryRoot <absolute-lab-path>` argument.

Copy `config\settings.example.json` to an ignored `.local\settings.json`, replace
all placeholders, and create a dedicated Azure CLI profile directory. Then:

```powershell
.\scripts\Use-Settings.ps1 -Path .\.local\settings.json
```

The loader validates an allowlisted configuration document before changing
process variables. `.env.example` is reference documentation, not an
automatically loaded environment. Deployment **aliases**, not model catalog
names, are required. The decision alias must resolve to Microsoft-Decision-1.
Do not use the normal Azure CLI production profile.

The six artifact/routing settings in the example are required together for
native hosting. Legacy clients may omit all six. Container names must be distinct,
private IPv4 addresses must match the Terraform-managed Blob private endpoint
exactly, and the request limit must be verified against the deployed Decision
model. Never guess private IPs, capacity or a confidence threshold.

Native packages additionally require the exact public `config\routing-corpus.json`
and `config\routing-calibration.json`. The latter contains the successful real
routing-v3 evaluation of the frozen twelve-case corpus, whose v1 dataset metadata
remains unchanged. Request hashes bind instructions, criteria, alias and state.
`scripts\calibrate_routing.py` retains a private, flushed observation
journal even on failure; an existing output/journal cannot be silently reused.
Offline synthetic fixtures are tests, never release calibration. Its
`--export-successful <private-result> --output config\routing-calibration.json`
mode validates provenance and permits only identical idempotent re-export.
Run `--validate-runtime` after loading the intended settings to check the
existing calibration without authentication, model calls or file writes.
The calibrated `DEMO_FACT_SHEET` must also be forwarded to every hosted role;
changing facts requires genuine calibration, not editing observation hashes.

Add `--native` only for a verified native deployment. A client state's recorded
runtime and versions cannot be silently migrated. `--recover-only` retrieves
the exact persisted pending parent response instead of sending another request.
Native checkpoints restore the graph, while the fenced write-ahead journal
reconciles known response IDs and explicitly holds unknown effects.
The acceptance utility's `observe` scenario retrieves only the preserved pending
response. For a failed response it reads at most 30 seconds/128 KiB of the pinned
hosted-session log stream through the same exact-origin transport, exposing only
allowlisted workflow phase/exception classifications, not arbitrary log content.
Diagnostic-enabled native versions additionally log an allowlisted failing
preparation check, never the rejected identity, endpoint, value or exception text.
This is diagnosis, not retry permission or a hosting restart test.
Read-only reconciliation on 2026-10-15 confirmed coordinator 22 remains active
and an exact coordinator-version-23 GET returns HTTP 404. The interrupted
diagnostic publisher has no recoverable package-bound owner/completion receipt;
its outcome and original mount closure remain unknown. The retained lab now
has exact-version observation and a separate non-mutating owner inspector.
Neither negative metadata nor an absent process authorizes publication replay.
The operator has explicitly approved ONE prospective coordinator-only lab
diagnostic risk exception, retaining that original publication as **UNKNOWN**
with delayed-publication and unproven historical-cleanup risks. Before the new
attempt, the retained publisher must pass local gates for durable pre-dispatch
owner/source/package/project/version binding, flushed phases/server IDs and
independent terminal/cleanup outcomes. The parent owns the private exact
authority/attempt record and freshly checks all deployed services; version23 is
not assumed next. The reviewed diagnostic package must match current source;
any rebuild needs exact provenance/review. New output/stage/ports/owner must be
isolated and the publisher serialized; only positively identified new owned
resources may be cleaned. A second unknown outcome or ownership consumes the
exception and stops further attempts. After exact diagnostic version/package/
identity and new owned cleanup are verified, ONE fresh synthetic App/native
parent and read-only exact-response observation may discriminate outbound
context mismatch from downstream missing identity. A mixed diagnostic bundle is
not final acceptance. See the [recovery plan](docs/identity-recovery-plan.md)
for R/L/D gates and finite exits. This documents approval, not execution:
original inference holds, historical cleanup uncertainty and unmet G1-G8
remain; no provider submission or speculative further release is authorized.
For repeatable identity triage, run
`<absolute-python-path> scripts\diagnose_identity.py` with the existing pinned
environment. It checks all applicable dependency-lock pins and runs five
synthetic, mocked SDK/HTTP-boundary probes without cloud access. Optional
`--trace <private-sanitized-trace.json>` analyzes exact-response ingress and
outbound presence flags; it never consumes raw logs or session state.
The report distinguishes local contract verification from missing live evidence:
exit 1 means offline verification failed, and exit 2 means the live cause remains
unresolved or input inspection failed. Offline success never grants retry,
identity-substitution or permission-change authority.
The 2026-10-15 diagnostic run matched all 109 installed lock pins and passed
all five offline probes. Fresh exact-version metadata independently confirms
architect 17, reviewer 15 and coordinator 22 are active with Responses protocol
2.0.0, the expected bundle and unchanged identities. Retained exact-response
evidence still shows the architect arriving with call identity but no user
identity. The live outbound call/context match and background-entry timing
were not captured, so transport versus platform resolution remains unresolved.
A subsequent bounded Azure Monitor query for the exact coordinator 22 /
architect 17 response pair confirms both identities at coordinator ingress,
call identity only at architect ingress, and a correlated HTTP 200 POST to
the expected architect Responses endpoint on the configured project origin.
This rules out a different endpoint/origin in that captured request, not
incorrect outbound call context: dependency telemetry contains no call-header
capture. A fresh exact coordinator-23 GET still returns 404; the interrupted
publication hold remains unresolved and no request was replayed.
The lab wrapper's explicit `recover` scenario retrieves only a known pending
response. Known-parent `followup` and opt-in `restart` scenarios do not create a
replacement parent. `-Mode Acceptance -HostingRestart` additionally tests the
supported hosted-session compute stop/resume API with a durable no-resend
marker. This preserves the session volume and is not a hard-crash recovery test.
These expanded live gates have not yet been run successfully.

The baseline terminal is Windows-only because its session lease uses `msvcrt`.
It is a terminal application, not a browser UI:

```powershell
# Authenticate the dedicated profile to the configured tenant using device code;
# verify the tenant and subscription before continuing.
$sessionDirectory = Join-Path $env:LOCALAPPDATA 'distributed-agents'
New-Item -ItemType Directory -Path $sessionDirectory -Force | Out-Null
& .\.venv\Scripts\python.exe -m demo.terminal `
    --session-file (Join-Path $sessionDirectory 'session.json')
```

The configured project must already contain compatible hosted agent deployments
and be reachable. For a private project, add `--socks socks5h://127.0.0.1:1080`
only when the separately managed tunnel is ready. `/quit` ends the client; it
does not stop separately managed tunnels. Session files must be outside this
repository, even in Git-ignored directories. Do not delete uncertain pending
state to force a retry.

## Private lab handoff

The local handoff includes an ignored `.azure` copy and validated
`.local\lab-settings.json`. Neither is public configuration, deployment
permission, nor proof of authentication. No Azure CLI token cache was copied.
The base settings do not include the native release inputs. After validating
that scope, load the existing `.local\lab-settings-native.json` through
`scripts\Use-Settings.ps1`, requiring the same lab, region, project,
tenant/subscription, dedicated profile and model aliases. Require all six
artifact/routing settings and explicit nonempty `DEMO_FACT_SHEET`, then run
`scripts\calibrate_routing.py --validate-runtime` with the pinned Python.
Do not overwrite either private file or treat a calibration check using
defaults as proof that the native release environment is loaded.
For another checkout, `scripts\Initialize-LabSettings.ps1` can derive private
tenant/subscription context from an explicitly selected external lab registry.
It does not provision resources, log in, or read copied `.azure` environment
values.

Do not run `azd up` or `azd provision` here. Before using the lab's retained
release tools, verify their explicit cross-repository application root support
as described in the workflow. That support has been added to the linked lab's
retained source and tested offline; Linux/WSL publication and existing trust
receipt validation remain separate gates. An azd environment copy alone does
not establish those gates.

License: [MIT](LICENSE). Environment state, private evidence, SSH identities,
and infrastructure are not part of the portable application distribution.
