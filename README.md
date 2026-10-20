# distributed-agents

A hosted coordinator repeatedly calls remote architect and reviewer agents,
keeping each specialist's session within the same parent conversation.
This educational Python solution uses Microsoft Agent Framework (MAF) and
Microsoft Foundry with exactly three hosted roles:

```text
User -> coordinator (MAF workflow)
          -> architect: design / revise
          -> reviewer: review the exact candidate
          <- coordinator: validate, accept or repeat
```

1. **Initial turn:** Design a synthetic application with private ingress only.
2. **Follow-up:** Add an asynchronous queue; keep private ingress and all earlier requirements.

**Continuity invariant:** the parent and both specialists keep their hosted
session IDs, framework session IDs and pinned deployed versions. New
invocations get new response IDs and produce current design/review artifacts.
A separate parent gets its own child bindings and artifact scope.

**Release status — blocked, not customer-ready (October 20, 2026):**
originating ownership, runner corrections and source integration handoffs are
accepted, but a release-tooling configuration correction is still required.
Reviewed tool source and the existing dedicated operational context must be
selected separately, without copying credentials or substituting profiles.
The predecessor check failed before deployment on that configuration mismatch;
it did not establish an authentication failure or specialist rejection.
The changed exact source join must pass original E2E validation, followed by
serialized guarded Linux/package, publication and live gates. Current
containment/resource readiness and deployed/rollback inventory also require
DevOps verification; supplied host trust alone is not current transport proof.

Accepted offline assertions are not a live demonstration. Neither identity
path is live-selected; live two-turn continuity, supported compute stop/resume
and separate-parent isolation remain unverified. The historical remote failure
was `NATIVE_HOST_PRINCIPAL`, before the architect application executed; this
is not a fresh observation of the current candidate. The mixed diagnostic
deployment is not a final common-bundle release.
[Release notes and requirement status](docs/customer-prototype-release-notes.md)
retain the earlier blocked closeout; the
[current release plan](docs/customer-prototype-release-plan.md) routes the
configuration correction and remaining gates. Final deployed and rollback
bindings remain unverified.
[Recovery evidence and gates](docs/identity-recovery-plan.md)
retain the publication **UNKNOWN**, held parents and unproven historical
cleanup; none may be cleared or replayed to make a demo pass.

**Read the source:** [workflow](demo/workflow.py) (`begin` -> `route` ->
`execute` -> `publish`) -> [remote session restore/invoke](demo/foundry.py)
-> [architect](demo/architect_agent.py) / [reviewer](demo/reviewer_agent.py)
model-history stages. [State and source map](docs/design.md#how-the-same-specialist-session-is-reused).

## Setup and offline checks

This repository owns portable application code, contracts, tests and generic
configuration. Infrastructure, private connectivity and guarded release tooling
remain in the separate lab repository; no infrastructure is provisioned here.

The hosting descriptor targets Linux/amd64/Python 3.13. Existing Windows
validation uses a pinned Python 3.12.10 environment; it does not replace the
hosting-package gate. Use PowerShell 7.2+ and the existing validated Python
absolute path when available. Do not reinstall dependencies for documentation
changes. For a **new environment**, review the package index and existing pins
in `requirements.txt` and `requirements.lock.txt` before installation:

```powershell
python -m venv .venv
$python = (Resolve-Path .\.venv\Scripts\python.exe).Path
& $python -m pip install -r requirements.txt
```

With the existing validated environment selected:

```powershell
$python = '<absolute-path-to-validated-python.exe>'
$lab = '<absolute-lab-repository-path>'
.\Test-Demo.ps1 -Python $python -LabRepositoryRoot $lab
.\scripts\Test-Repository.ps1 -Python $python
```

Offline tests use synthetic inputs and mocked Foundry/storage boundaries;
they need no Azure login and are **not live acceptance evidence**. The explicit
lab root enables Windows retained-connectivity wrapper regressions; omitting it
reports those cases as skipped. Linux hosting-package checks and affected lab
release regressions remain separate required release gates.

Copy `config\settings.example.json` to ignored `.local\settings.json` and replace
the placeholders with verified configuration. Use a dedicated Azure CLI profile,
never a production profile. Import only through the allowlisted loader:

```powershell
.\scripts\Use-Settings.ps1 -Path .\.local\settings.json
```

`.env.example` is reference documentation, not an automatically loaded
environment. Model deployment **aliases**, not model catalog names, are
required; the decision alias must resolve to Microsoft-Decision-1.
The six artifact/routing settings are required together. Container names must
be distinct, private IPv4 addresses must match the managed Blob private endpoint,
and the request limit must match verified Decision capacity. Do not guess
private addresses, capacity or confidence thresholds.

For this linked-lab checkout, use the existing ignored
`.local\lab-settings-native.json` with `Use-Settings.ps1`; do not overwrite it or
inspect copied `.azure` environment files. Validate the configured project,
tenant/subscription, lab root and dedicated profile without displaying values.
Do not substitute another project or CLI profile. Authenticate the dedicated
profile using device code when needed, then verify its tenant/subscription.
The loader validates local configuration; it is not cloud authentication proof.

## Two-turn terminal demonstration

This is the **implemented command shape**, not a claim the blocked live
demonstration has passed. The Windows-only terminal uses `msvcrt` for its
session lease. It requires compatible deployed agents and an already established
owned SOCKS tunnel to the configured project. `--socks` is mandatory; substitute
the verified local port from the retained lab connectivity tooling, not a new
public route or an ad hoc tunnel.

Run from the application root after loading settings and authenticating:

```powershell
$sessionDirectory = Join-Path $env:LOCALAPPDATA 'distributed-agents'
New-Item -ItemType Directory -Path $sessionDirectory -Force | Out-Null
# Choose a new filename for this synthetic parent; preserve every existing file.
$session = Join-Path $sessionDirectory 'synthetic-private-ingress-01.json'
$socks = 'socks5h://127.0.0.1:<verified-owned-port>'

& $python -m demo.terminal --native --view human --socks $socks --session-file $session `
    --message 'Design a synthetic application with private ingress only.'

# Only after the first turn completes with no pending/held effect:
& $python -m demo.terminal --native --view human --socks $socks --session-file $session `
    --message 'Add an asynchronous queue; keep private ingress and all earlier requirements.'
```

Do not issue the follow-up if the first turn fails or is held. Reuse the same
private session file for a completed conversation; never delete uncertain state
to force another request. Omit `--message` for interactive input; `/quit` closes
the client, not its separately managed tunnel. Use only synthetic text in
shareable demonstrations and omit `--show-ids`.

The default terminal prints a parent alias and existing machine
delegation/result records; stdout is not pure JSONL. Repeated calls remain in
chronological order. Matching display aliases or plausible memory text alone
do **not** verify exact continuity, new child creation counts or model history.
Private acceptance evidence must compare actual parent/child hosted and
framework IDs, pinned versions, fresh response IDs and current artifact refs.
Useful design/review content is part of the result, not proof of live release
acceptance by itself.

`--view human` is implemented: both commands add a separate stderr summary
after complete records are finalized, showing ordered specialist calls and
current design/review output. Omit it to retain the default presentation;
stdout and the acceptance parser are unchanged. The summary labels exact
continuity and child creation counts as unverified/not observed because aliases
cannot establish them. Known-response retrieval is labeled as recovery, not a
new invocation. Offline capture tests cover these behaviors, not live success.

## What is preserved, and what changes?

| State | Stable within one parent | Advances |
|---|---|---|
| Coordinator conversation | Hosted/framework session IDs, pinned version | User turns and response continuation |
| Architect child | Own hosted/framework IDs and pinned version | Design/revision calls and responses |
| Reviewer child | Own hosted/framework IDs and pinned version | Reviews of exact current prerequisites and responses |
| Artifacts | Immutable accepted object references and provenance | Requirements/candidate revisions; old approval is invalidated |
| Workflow recovery | Trusted scope and durable operation records | MAF checkpoint position and reconciled effect state |

The parent's manifest holds `children[role]`; `WorkflowRuntime.execute()` looks
there before creating a child. `RemoteAgents.invoke()` restores that child's
`AgentSession` and passes it to the remote agent. Each specialist separately
loads its own persisted model history before generating or recovering a model
response. These are distinct mechanisms, not replayed requirements masquerading
as session continuity. See the [full source explanation](docs/design.md).

`--native`, `DEMO_RUNTIME=native`, `native_workflow` and `NATIVE_*` retain their
compatibility spellings; they do not denote another framework. Saved runtime or
version bindings cannot be silently migrated. `--recover-only` retrieves the
exact persisted pending parent response without sending another turn; it does
not resolve a held unknown specialist effect or authorize retry. MAF checkpoints
do not replace the fenced write-ahead journal.

## Release boundaries and current limitations

- Exactly three hosted services; no hidden local specialist fallback.
  Decision-1 is a routing helper/model, not a fourth agent deployment.
- Managed-identity private Blob access and exact immutable provenance must pass
  **live**, alongside remote collaboration, continuity, supported compute
  stop/resume and separate-parent isolation. An upload, HTTP 200, metadata or
  passing mocks is insufficient.
- The linked lab grants account-wide Blob Contributor access. Role ownership
  and parent isolation are **application-enforced**, not storage-RBAC or
  malicious-host isolation.
- Preserve unknown publications, held sessions, old versions/packages and
  historical cleanup uncertainty. The supported compute stop/resume gate is not
  hard-crash recovery.
- Release packages require the exact routing corpus/calibration and explicit
  nonempty calibrated `DEMO_FACT_SHEET`, forwarded to all roles. The offline
  `scripts\calibrate_routing.py --validate-runtime` check validates loaded
  settings without model calls; never edit observations/hashes to pass it.
- Use only the retained lab packaging/preflight/WSL publication chain with
  explicit application/lab roots and current user authority. No `azd up`,
  `azd provision`, speculative identity headers/grants or unknown-effect replay.

For engineering/release gates, read the [implementation workflow](docs/implementation-workflow.md).
The [recovery plan](docs/identity-recovery-plan.md) owns detailed diagnostic
chronology and historical version/package bindings; those are not a fresh
deployment inventory. The [release plan](docs/customer-prototype-release-plan.md)
maps the customer outcome to source, exact-package and live acceptance.
The [migration plan](docs/migration-plan.md) and
[migration map](docs/migration-map.json) retain original-source preservation
history, not permission to reseal changed source or deploy a stale lab copy.

License: [MIT](LICENSE). Private settings/evidence, session files, SSH identities,
packages, infrastructure and workflow control-plane tooling do not belong in
the customer application distribution.
