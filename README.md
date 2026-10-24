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

**Current mission:** deliver the
[three-role azd demo](docs/requirements/delivery-mission.md), not another
exhausted diagnostic plan. Native MAF workflow and Blob artifact-plane source
are largely implemented; the handwritten/in-process adapter remains an explicit
offline regression path, never a hidden production fallback.

**Latest recorded status, not fresh cloud verification:** main historically
records architect 17 / reviewer 15 / coordinator 23; the later reviewed
`origin/feature/customer-hosted-session-prototype` at `329eab9` records
19 / 17 / 25. Prior Windows suites recorded main 159 tests (2 skips), feature
364 tests (3 skips); these are not new checks in this preparation.
Live acceptance remains blocked on trusted-user propagation
(`NATIVE_HOST_PRINCIPAL` / `SPECIALIST_INCOMPLETE`). Explicit delegation and an
existing impersonation permission have not established a fix. No platform
cause is proven. Completed remote work, MI Blob provenance, follow-up,
recovery and parent isolation are not freshly verified.

The deployment descriptor already has the existing project and three
Responses 2.0.0 remote-build services. Its current `package_guard.py` hooks still
require a preapproved ZIP/hash/private receipt: implementing a safe normal
`azd deploy` path is real mission work, not merely adding a README command.
Preserve exact-package lab release safeguards and all held/unknown effects.
Historical diagnostics and the consumed exception remain in
[identity-recovery-plan.md](docs/identity-recovery-plan.md) and Git.

**Continuity invariant:** the parent and both specialists keep their hosted
session IDs, framework session IDs and pinned deployed versions. New
invocations get new response IDs and produce current design/review artifacts.
A separate parent gets its own child bindings and artifact scope.

**Release status — partial correction; blocked, not customer-ready (October 22, 2026):**
the original changed-join E2E reassessment is accepted for application
`13aecc39` (runtime/tests `c52786b7`) and selected lab `9b4919d8`.
Original Architect/Critic/Product Owner agreed to the bounded **offline PASS**,
not a release PASS. Repository validation passed. Attributed corrected captures
report 278 Windows application passes and 236/240 retained passes (four
exclusions); Linux reports 270/278 application passes (eight exclusions) and
197/240 retained passes (43 exclusions), on an arm64 host running linux/amd64.
The reassessment verified applicable captures and ran focused join checks;
these are not newly repeated full suites or native-amd64-host certification.

Original DevOps prepared and verified a runtime ZIP and Linux dependency stage,
**not a final common bundle**. Native WSL pinned-tool/dedicated-authentication
preflight received a noninteractive tool-permission denial. Its exact missing
permission and native readiness remain unproven; do not retry or bypass that
denial. The operator resolves that specific approval through supported
interactive controls, then original DevOps continues the existing prepared
stage and automated current source/package/version/trusted-host/effect checks.
Routine guarded three-role publication is already authorized, not awaiting a
new project sign-off. Historical COMMON rollback ZIP/build provenance is
**WAIVED, never PASS**; the old repository-check denial and rollback
investigation are dated history, not current prerequisites.

Final correction-package publication and current deployed bindings, non-held
initial collaboration, same-parent continuity, once-only supported stop/resume,
independent separate-parent isolation, attributable cleanup and original
review/retro/closeout remain incomplete. Authenticated outbound principal,
platform identity resolution and a supported identity remedy remain unproven.
Preserve the held original parent, all **UNKNOWN** effects and historical
unproven cleanup; no uncertain operation may be replayed. Independent IP-S3
evidence/status preparation continues without consuming missing live handoffs.
See [current measured evidence and exact reviewed refs](docs/customer-prototype-release-notes.md#current-measured-correction-status--october-22-2026)
and [current sprint handoffs](docs/customer-prototype-sprint-architecture.md#current-ip-s3-continuity-once-only-recovery-and-independent-isolation).
Historical reviewed delivery through application `8b50f343` / lab `88580156`
is retained, not proof of remote delivery of later correction commits.
The original closeout owner must deliver/read back exact reviewed refs, never
an automatic moving-HEAD push.

**Read the source:** [workflow](demo/workflow.py) (`begin` -> `route` ->
`execute` -> `publish`) -> [remote session restore/invoke](demo/foundry.py)
-> [architect](demo/architect_agent.py) / [reviewer](demo/reviewer_agent.py)
model-history stages. [State and source map](docs/design.md#how-the-same-specialist-session-is-reused).

## Authorized delivery invocation

Open this repository in Copilot and submit the invocation in
[docs/NEXT-SESSION-PROMPT.md](docs/NEXT-SESSION-PROMPT.md). It explicitly
authorizes scoped implementation/tests/commits, reviewed `lab-delivery` launch,
normal azd deployment and synthetic acceptance for the three existing roles
in the validated nonproduction project. Reading it is not authorization;
**this preparation session performs no launch, cloud call, commit or deployment**.

The actual input is `delivery-input.json`; the
[mission](docs/requirements/delivery-mission.md) is authoritative for components,
flows, source integration and consistent RAG reports. Integrate scoped preparation
onto `feature/azd-demo-delivery` based on the latest reviewed customer-hosted-session
feature before launching; do not run old main because JSON names a branch.
Before each launch review the sibling framework origin's latest revision,
upgrade only while inactive and confirm registrations/`work-conserving-v1`.
The CLI delivery workflow is distinct from the application's native MAF graph.
Monitor actual durable outcomes, causally fix/validate failures and safely
resume/relaunch while retaining accepted work and exact unmet criteria.
`--check-only`, SDK completion, healthy hosts and offline tests are not acceptance.

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

`scripts\Test-Repository.ps1 -Python <absolute-python-path>` checks the public
boundary, index, syntax and whitespace. Its bounded context-frontmatter check
requires the existing `name`/`description` header; agents may additionally use
an optional `tools` YAML flow list of tool identifiers (plain, single-quoted or
double-quoted). Skill headers remain unchanged; this is not a general YAML parser.


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
Historical reconciliation and diagnostic attempts, including the consumed
exception, are retained in the [recovery plan](docs/identity-recovery-plan.md).
Do not turn them into new publication/inference authority, replay a held
operation or infer never-sent from HTTP404, empty logs or an absent PID.
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
The historical 2026-10-15 triage matched 109 lock pins and passed five offline
probes; later exact-response diagnostics captured matching outbound call context
but no trusted user at architect ingress. These are not fresh cloud checks or
an established platform/header/RBAC fix.
The lab wrapper's explicit `recover` scenario retrieves only a known pending
response. Known-parent `followup` and opt-in `restart` scenarios do not create a
replacement parent. `-Mode Acceptance -HostingRestart` additionally tests the
supported hosted-session compute stop/resume API with a durable no-resend
marker. This preserves the session volume and is not a hard-crash recovery test.
These expanded live gates have not yet been run successfully.

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

Normal existing-service `azd deploy` is the next invocation's application scope,
after the mission's predeploy-contract implementation/tests. `azd up` or
`azd provision` require separate exact provisioning authority, not a permanent
tool ban. No infrastructure/RBAC/network/DNS/quota/VM-power/secret/VPN changes
are authorized by generic delivery. Before any separately authorized retained
lab release, verify explicit cross-repository roots and all source/package,
Linux/WSL, trust-receipt and cleanup safeguards. An azd environment copy alone
establishes neither those checks nor deployment permission.

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
- Use the mission's normal azd path for current delivery; leave retained lab
  exact-package tools and safeguards intact. `azd up`/`azd provision` require
  separate provisioning authority. No speculative identity headers/grants or
  unknown-effect replay.

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
