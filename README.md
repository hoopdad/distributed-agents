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
[three-role azd demo](docs/requirements/delivery-mission.md). The MAF workflow
and Blob artifact-plane source are implemented; offline adapters never replace
remote production specialists. Current source, deployed bindings and actual
operation outcomes determine status. Unexecuted live checks are unverified,
not failed. Prior failures, denials and planning handoffs are opt-in
[historical context](.github/repo-history-index.md), not current blockers.

The deployment descriptor has the existing project and three Responses 2.0.0
bundled-dependency services. Normal `azd deploy` uses
[bounded source/pin checks](docs/requirements/azd-walking-skeleton.md) and
`.agentignore`, without a preapproved ZIP/hash/private receipt. Actual deployment
and separate exact-candidate probes remain required; offline checks are not a
deployed pass. Exact-package lab safeguards and all held/unknown effects remain.
After remote dependency builds failed, the same locked Linux dependencies are
installed locally with `scripts\build_azd_bundle.py`, then checked against their
wheel tags, dependency closure and RECORD hashes before normal azd packaging.
Use Linux x86_64 CPython 3.13 with pip to run that script from this repository.
It reuses a valid `packages/` tree without reinstalling and never replaces an
existing invalid tree. Generated dependencies remain ignored by Git.

**Continuity invariant:** the parent and both specialists keep their hosted
session IDs, framework session IDs and pinned deployed versions. New
invocations get new response IDs and produce current design/review artifacts.
A separate parent gets its own child bindings and artifact scope.

**Read the source:** [workflow](demo/workflow.py) (`begin` -> `route` ->
`execute` -> `publish`) -> [remote session restore/invoke](demo/foundry.py)
-> [architect](demo/architect_agent.py) / [reviewer](demo/reviewer_agent.py)
model-history stages. [State and source map](docs/design.md#how-the-same-specialist-session-is-reused).

## Authorized delivery invocation

**Design -> develop -> deploy -> test case -> remediate -> iterate.**
Work directly from the integrated `feature/azd-demo-delivery` source using normal
azd. No CLI delivery workflows, planning loops, approval artifacts or role/reviewer
orchestration. The application's MAF graph remains required.

The current user authorized scoped implementation/tests/commits (no push),
existing-project azd deployment and synthetic acceptance for the three roles.
The [mission](docs/requirements/delivery-mission.md) defines product acceptance;
the [continuation prompt](docs/NEXT-SESSION-PROMPT.md) preserves the scope.
Deploy working increments, test actual outcomes, fix causes and repeat.
Offline tests, healthy hosts and SDK completion do not establish live success.

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

Before cloud operations, load the validated private configuration through
`Use-Settings.ps1`; no historical settings filename is a workflow launch gate.
Do not overwrite private settings or inspect copied `.azure` environment files.
Validate the configured project,
tenant/subscription, lab root and dedicated profile without displaying values.
Do not substitute another project or CLI profile. Authenticate the dedicated
profile using device code when needed, then verify its tenant/subscription.
The loader validates local configuration; it is not cloud authentication proof.

## Two-turn terminal demonstration

This is the **implemented command shape**, not a claim the live
demonstration has passed. The Windows-only terminal uses `msvcrt` for its
session lease. It requires compatible deployed agents and an existing route
to the configured project. Select either `--socks` with a verified owned
loopback tunnel or `--direct` to use the existing route without a proxy.
Both retain exact-origin TLS, no redirects, no environment proxies and zero
transport retries. Neither option creates or changes a network route.

Authentication defaults to the dedicated Azure CLI profile. An already
authenticated dedicated azd profile can instead use `--credential-source azd`
with an explicit absolute `AZD_CONFIG_DIR`. This verifies an authenticated user
and the expected tenant/subscription through ARM before using the standard
`AzureDeveloperCliCredential`; it never copies tokens or falls back to another
profile. Saved parent ownership and hosting principal gates remain unchanged.
`live_acceptance.py` supports the same explicit options and verifies the actual
deployed archive hash for either bundled or remote-build code.

The native hosts also expose a bounded `identity-probe-v1` Invocations diagnostic,
explicitly authorized after a fresh Responses identity failure.
`live_acceptance.py --scenario identity-probe` uses the same route/auth/hash
options and a new private session/evidence pair. It records reserved IDs before
dispatch, creates only diagnostic sessions on the existing roles, and never
resends an uncertain probe. It calls no model, touches no application artifacts
and reports only trusted-context presence/equality. Responses workflows,
principal gates and held parents remain unchanged. Even a passing probe is not
end-to-end acceptance or an automatic specialist-transport migration.
`--identity-forwarding user-only` compares the
[documented direct-call delegation header](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/multiplex-session-users)
with the original parent-call-plus-user header set. Only the diagnostic
children use this selector: the trusted coordinator scope is still revalidated,
child call context is left to the service, and application callers remain
unchanged. Use a new private session/evidence pair; never resend an old probe.
Add `--specialist-protocol responses` to compare the same diagnostic through the
application's Responses transport. Its native specialist graph only inspects
trusted context; it does not run the design/review graph, a model or application
artifact access. Known child response IDs/statuses are returned even when native
preparation fails. A failed or pending response never implies absent identity
without host evidence, and a pending response is never resent.
Responses probes use the pinned public project/OpenAI client, including its
preview headers and zero retries. `--session-creation first-response` tests the
documented first-Responses-call session creation instead of explicit creation.
It is Responses-only and diagnostic-only: verify the actual created version,
retain every reserved ID, and never change existing application bindings.

For the authorized signed-in-user A2A experiment, use the existing diagnostic
toolbox (not a new agent) with the same dedicated azd profile:

```powershell
& $python scripts\diagnose_delegation.py --toolbox '<existing-diagnostic-toolbox>' --version 2 --credential-source azd --direct --evidence '<new-absolute-private-json-path>'
```

This checks the two fixed specialist sources, delegated authentication/card
settings and account network configuration, compares direct user card access
with managed MCP discovery, and saves allowlisted HTTP status, timing and
request IDs. It never invokes tools/models, creates sessions, changes Azure
configuration or touches held work. Metadata/ARM reads use the existing direct
route; `--socks` optionally replaces `--direct` for card/MCP traffic only.
The documented service-default card policy is valid for Foundry targets;
separate card credentials aren't required by the diagnostic configuration gate.
The hosted discovery comparison also accepts the official
[A2A 0.3 delegation sample's](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/agent-framework/a2a/01-delegation)
preview-tool profile with its exact `agentCard/v0.3` path. It uses the same
two delegated connections and pinned roles, requires authenticated card fetch,
and remains discovery-only. This is not a production transport switch; the
terminal diagnostic command above continues to check the A2A 1.0 profile.
Evidence must be new and outside this repository. Exit 2 means blocked,
incomplete or failed collection; discovery success is not user propagation or
application acceptance. A remote 403 is distinct from toolbox-entry rejection;
subnet configuration is not reachability proof. Broker-to-card routing and
correlation remain explicitly unobserved unless independently captured.
Raw exception text, tokens, identities, URLs, card content and tool schemas are
excluded; safe correlation IDs remain in private evidence. Do not repeat a
denied discovery without a material diagnostic/configuration change.

`live_acceptance.py --scenario delegation-discovery --toolbox-name <existing-name>
--toolbox-version 2` adds a coordinator-hosted comparison using the usual
route/auth/hash/private session/evidence arguments. It reserves a fresh
coordinator session before dispatch, verifies genuine principal/call/session
context and the two pinned delegated sources, then forwards only the SDK's
genuine opaque call context with managed-identity toolbox authentication.
Platform-provided toolbox preview flags are preserved, matching the pinned
hosted toolbox wrapper; evidence records only whether such flags were present.
Use `--scenario delegation-discovery-responses` with a new private session/evidence
pair to compare the same discovery through a foreground, stored, nonstreaming
native Responses workflow. The explicit diagnostic metadata selector grants no
authority: genuine hosted coordinator principal/call/session gates still apply.
Ordinary requests retain their existing workflow/parser. This comparison runs
no business graph and records a known response ID before interpreting its result;
uncertain requests are never resent. It does not adopt A2A for application calls.
Only MCP discovery runs: no specialist session creation, tool call, model or
Blob operation. It shares the terminal diagnostic's redaction/request observer.
Missing context/configuration, remote rejection and uncertain dispatch remain
explicit; discovery success still does not prove downstream user propagation.

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
with source checks and actual deployed verification. `azd up` or
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
The [historical index](.github/repo-history-index.md) retains prior diagnostics,
release plans and migration context for targeted provenance questions. None is
an active dispatch plan, release gate or current deployment inventory.

License: [MIT](LICENSE). Private settings/evidence, session files, SSH identities,
packages, infrastructure and workflow control-plane tooling do not belong in
the customer application distribution.
