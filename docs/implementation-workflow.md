# Application delivery and lab deployment workflow

The current objective and user amendments are authoritative in
[requirements/delivery-mission.md](requirements/delivery-mission.md).
Use `delivery-input.json` with the submitted
[next-session invocation](NEXT-SESSION-PROMPT.md). Current state and actual
operation outcomes establish blockers. Historical failures, permission denials,
owners and exhausted plans are opt-in context, not required release gates.

The CLI **`lab-delivery` workflow delivers the application**. The application's
**MAF workflow coordinates remote architect/reviewer calls**. They are different
systems; neither SDK completion nor completed delivery cards proves the
application works. File presence alone supplies no launch or deployment authority.

## Source-correct launch

Read README, repository instructions/index, the mission, design and migration
plan/map before implementation. Preserve unrelated dirty files and retained
lab safeguards. Main `1dfb7fe` is not the latest implementation: the reviewed
feature baseline was `origin/feature/customer-hosted-session-prototype` at
`329eab9`. Under the submitted invocation's authority, integrate scoped preparation
commits onto `feature/azd-demo-delivery` based on the latest reviewed feature
revision. Do not reset, overwrite or indiscriminately stash shared dirty work.

Mission citations must match committed HEAD before runtime evaluation. Inspect
the staging list and commit only authorized paths with required trailers;
no push. Run from the integrated delivery root. `git.featureBranch` in the
input is context, not an automatic branch switch.

Before each launch, check the sibling framework origin's latest revision and
review changes against the installed runtime. Upgrade only when inactive and
within explicit scope; never replace an active runtime. Preserve old run
histories. Verify `autonomous-delivery` and `lab-delivery` registrations and
the `yaml-loops-v2`, `requirement-grounded-v1`, `work-conserving-v1` contracts.
Incompatible histories are not resumable through the new engine.

After the user submits the invocation and establishes ordinary scoped
permissions, use the supported launcher:

```powershell
node .\gh-dynamic-workflows\run.mjs --workflow lab-delivery --input delivery-input.json --check-only
node .\gh-dynamic-workflows\run.mjs --workflow lab-delivery --input delivery-input.json --add-dir ..\enterprise-copilot-fleet-controller
```

The first command only reads configuration; it does not prove execution.
Registration/loading grants no cloud or blanket tool permission. Do not invent
round/sprint/concurrency/time/spend/stagnation limits; use only user-configured
limits.

## Preserve customer continuity

Start with the [two-turn example](../README.md#two-turn-terminal-demonstration)
and [create-or-reuse source path](design.md#how-the-same-specialist-session-is-reused).
Within a parent, preserve both specialists' hosted/framework identities and
pinned versions while response continuations advance. The manifest child lookup,
restored remote `AgentSession` and each specialist's model history are separate
links in that chain. Conversations retain history; MAF checkpoints resume graph
position; immutable artifacts and the fenced effect journal establish accepted
work and reconcile side effects. None replaces another.

Keep baseline machine delegation/result output and acceptance parsing unchanged.
The implemented `--native --view human` summary is an opt-in stderr projection.
Exact continuity needs actual binding checks, not alias equality. Existing capture
tests cover unchanged stdout/parser, fragmented streams and known-response
recovery; these offline checks are not live certification. A follow-up is allowed
only after a completed, non-held initial turn. Known-response retrieval is not
a new send or specialist invocation.

## Deliver the smallest working flow early

Sprint 1 starts with a dependency-free DevOps `walkingSkeleton:true` azd
deployment and a real deployed probe. Other assignments preserve genuine
skeleton prerequisites. Existing `azure.yaml` defines an existing project and
three remote-build Responses 2.0.0 hosted services.
The [normal-azd source contract](requirements/azd-walking-skeleton.md) replaces
the incompatible preapproved ZIP/hash/private-receipt hooks with bounded
source/package exclusions, dependency pins and local compilation checks.
No preapproved ZIP/hash or private approval receipt is required for this path.
Remote Linux builds and separate deployed probes still must verify the actual
candidate and outcome. Unused legacy lab release tools remain intact,
without imposing their ceremony on normal azd delivery.

Construction owners may work concurrently on independent authorized tasks,
providing actual local checks plus the exact committed revision/immutable build
candidate, without mutating the shared environment. Existing DevOps-then-E2E
loops deploy and verify that candidate under one shared environment lock before
assignment acceptance and dependent release. Never deploy an unrelated mutable
checkout. A localized failure does not stop unrelated authorized construction,
but offline work cannot satisfy deployed acceptance or release blocked
dependents. Replan material contract/dependency changes through existing roles;
add no continuation amendments, exhaustion audits or new review stages.

Keep exactly the three roles, MAF, gated Microsoft-Decision-1 routing,
remote specialists and private managed-identity Blob exchange. Exercise actual
design-review-revision, same-parent follow-up, independent parent isolation
and supported recovery. Keep trusted parent binding, immutable role outputs,
exact refs, coordinator ETag publication, MAF checkpoints and write-ahead
effects/unknown holds. See D1-D7/F1-F4 in the mission for falsifiable criteria.

## Validate the candidate, not an assumed baseline

Use the existing pinned environment; install/restore dependencies only after a
manifest change or an actual missing-tool/package failure. Start with affected
tests, then the applicable application gate:

```powershell
.\Test-Demo.ps1 -Python <absolute-python-path>
.\scripts\Test-Repository.ps1 -Python <absolute-python-path>
```

Include `-LabRepositoryRoot <explicit-root>` for external Windows wrapper
regressions. Resolve that root privately; do not publish it. Run retained lab
tests after authorized release-tool changes. Preserve original tests, package
allowlists, lock provenance, Linux checks, strict host fingerprints, private
evidence and owned process/mount cleanup. Do not reseal historical migration
hashes to hide drift. Refresh the public index after file additions/deletions.

Before cloud operations, import only allowlisted private settings using
`scripts\Use-Settings.ps1`; never display copied `.azure` values, token caches,
keys or connection strings. Require matching existing project/region/tenant/
subscription/profile/model aliases and artifact settings, including explicit
nonempty calibrated `DEMO_FACT_SHEET`. Check calibration offline with
`scripts\calibrate_routing.py --validate-runtime` in the pinned environment.
Do not invent missing configuration or mutate calibration observations.
A historical settings filename is not a workflow admission gate or proof that
credentials are absent. Continue independent local work around a cloud blocker.

Use dedicated device-code authentication for `az` and `azd`, preserving the
validated `AZURE_CONFIG_DIR` in child processes. Set `AZD_CONFIG_DIR` explicitly
to an isolated private directory before configuring `auth.useAzCliAuth true`;
verify `azd auth login --check-status` and separately compare `az account show`
tenant/subscription against validated scope. Do not change global azd config
or use the production profile. Windows and WSL have separate caches; never copy
tokens or assume authentication transfers. Retained wrappers select their own
`OutputDirectory\azd-wsl-config` and pinned extension; a separate preflight
config does not configure their release context.

## Deployment authority and external lab boundary

The submitted invocation authorizes normal **`azd deploy` and synthetic
acceptance only for the three existing roles in the existing validated
nonproduction project**, including supported hosted-session compute stop/resume.
It authorizes scoped local commits, not push. It does not authorize infrastructure,
RBAC, network, DNS, quota, VM power, secret retrieval, VPN operations, production
credentials, private lab edits or provider submission. Historical broader
invocations do not expand this invocation's scope.

Infrastructure and unique registry/network/DNS/VPN/Bastion/WSL release tools
remain in the external lab. Read its startup/infrastructure instructions before
any separately authorized change. Such work follows its registry, authentication,
saved-plan and release safeguards; this application workflow does not replace
them. `azd up`/`azd provision` require separate exact provisioning authority.

The retained exact-package lab path remains available with its original
approved ZIP/hash/receipt, source/lock, Linux, service/version, ownership and
cleanup checks. Do not weaken it while enabling the normal-azd path.
Load private root/scope through validated settings, never public literals or
the production CLI profile. Never log in to or modify the VPN server.

## Monitor, remediate, resume safely

Use the supported launcher's actual durable results and bounded relevant logs,
avoiding repeated empty polling. Ignored `gh-dynamic-workflows\.delivery-runs`
retains outcomes/logs. Exit codes distinguish completion **0**, application
stop **2**, runtime/CLI error **1**, pause **3**, cancellation **130**.
Inspect application outcome and unresolved feedback, not the SDK envelope.

Localize failure to the component, flow and criterion. Diagnose its concrete
cause, implement the smallest authorized fix and run affected validation before
resuming compatibly or fresh launching. Retain accepted work, partial sprints,
exact unmet criteria and unblock conditions. Reconcile known responses/receipts/
versions through supported interfaces. Empty logs, absent PIDs and HTTP404 do
not prove never sent. Never blindly repeat unchanged denials or unknown effects,
clear held state, reset limits or edit SDK journals/databases.

If a current operation fails trusted-user propagation, inspect the actual
request boundary and current SDK/platform contract before choosing a remedy.
Do not load a historical diagnosis as the current cause. Investigate the
smallest supported authenticated/state-compatible request path. Major
host/transport changes need an explicit requirements decision. Never substitute
a principal or disable runtime/assignment checks.

Continue independent authorized work while a localized criterion remains blocked.
Ask only when the required operation truly needs new scope, credentials or a
material requirements decision. Normal engineering needs no ritual reapproval.

## Acceptance and handoff

Run synthetic live acceptance against the exact deployed candidate: remote
architect and reviewer, actual revision, private MI Blob provenance, Decision-1,
same-parent follow-up, checkpoint/known-response recovery and an isolated parent.
Supported hosting stop/resume is not hard-crash proof. Preserve uncertain stop
markers and pending responses instead of repeating operations. Validate exact
artifact hashes/prerequisites, producer session/version bindings and decisions,
not just a success-shaped final message. Account-wide trusted-lab Blob grants
mean ownership is application-enforced, not storage-enforced role isolation.

Every progress/final report uses the mission's seven components and table:
`Component | RAG | Evidence/freshness | Remaining work/next action`.
Green requires fresh end-to-end component acceptance; amber means partial,
unexecuted, unverified or stale; red means an evidenced failure/blocker.
Label historical failures/versions; unreached checks are amber. Offline tests,
healthy hosts, uploads and SDK completion never establish green.

Completion requires D1-D7 with fresh evidence. Otherwise report exact accepted
work, source/run/environment, unmet criteria and precise next action. An empty
exhausted plan is incomplete delivery, not success.
