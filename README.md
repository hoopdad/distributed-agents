# distributed-agents

Three Microsoft Foundry hosted agents: a coordinator, an architect, and a
reviewer. This repository owns reusable application code, contracts, tests, and
generic configuration. Infrastructure and environment-specific connectivity
remain in the separate Azure lab repository.

**Status:** native Microsoft Agent Framework (MAF) workflow and shared Blob
artifact-plane source are implemented; 89 application tests pass on Windows
and Linux/amd64 (seven expected Windows-only skips on Linux).
`azure.yaml` selects native orchestration and remote hosted specialists; the
legacy handwritten/in-process adapter remains available for regression tests.
**This iteration is not deployed or live-accepted.** The lab's scoped artifact
infrastructure apply added 14 resources; a subsequent scoped plan/apply confirmed
zero changes. Read-only metadata verifies private containers, role-scoped grants
and retention. Native bundled packaging, publication and synthetic live
acceptance remain outstanding; infrastructure metadata and three declared
services do not prove remote calls or private managed-identity storage access.

**Approved lab permission model:** the linked lab now grants its project agents
account-wide Blob Contributor access. The original container grants remain, but
do not provide effective per-role isolation. Role ownership, immutable output
handling and coordinator publication are enforced by trusted application code,
not by storage permissions. This is not a storage-enforced isolation guarantee.

**Calibration verified:** the first twelve-case evaluation failed with two of
eight ready cases correct. Routing policy/input v2 clarifies first-draft versus
review prerequisites and exposes complete verified semantic inputs. A second
evaluation on the unchanged frozen corpus passed all eight ready cases, with no
wrong dispatches, at threshold 0.9 and margin 0. Both private journals are
retained (24 real calls total); no coverage gate or expected label was changed.
The validated successful result is `config\routing-calibration.json`.

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
routing-v2 evaluation of the frozen twelve-case corpus, whose v1 dataset metadata
remains unchanged. Request hashes bind instructions, criteria, alias and state.
`scripts\calibrate_routing.py` retains a private, flushed observation
journal even on failure; an existing output/journal cannot be silently reused.
Offline synthetic fixtures are tests, never release calibration. Its
`--export-successful <private-result> --output config\routing-calibration.json`
mode validates provenance and permits only identical idempotent re-export.

Add `--native` only for a verified native deployment. A client state's recorded
runtime and versions cannot be silently migrated. `--recover-only` retrieves
the exact persisted pending parent response instead of sending another request.
Native checkpoints restore the graph, while the fenced write-ahead journal
reconciles known response IDs and explicitly holds unknown effects.

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
