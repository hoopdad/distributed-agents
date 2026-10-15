# distributed-agents

Three Microsoft Foundry hosted agents: a coordinator, an architect, and a
reviewer. This repository owns reusable application code, contracts, tests, and
generic configuration. Infrastructure and environment-specific connectivity
remain in the separate Azure lab repository.

**Status:** native Microsoft Agent Framework (MAF) workflow and shared Blob
artifact-plane source are implemented; 109 application tests pass on Windows
and Linux/amd64 (seven expected Windows-only skips on Linux).
`azure.yaml` selects native orchestration and remote hosted specialists; the
legacy handwritten/in-process adapter remains available for regression tests.
**Deployed, but not live-accepted:** architect 16, reviewer 14 and coordinator 21
are active on corrected bundle
`b3556f4241232bb301c80cfe4a57a726cc7411f2dba105a27fcfb573cb49da86`.
Their identities are unchanged; earlier versions and diagnostic packages are retained.
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
identity-presence booleans for the exact known response. The next observation
could not connect because the approved lab command VM is deallocated; starting
it requires separate approval, not a VPN or permission change.
No failed turn was resent or pending state cleared. The lab's scoped
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
