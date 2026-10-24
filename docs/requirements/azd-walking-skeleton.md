# D1/F1: ordinary azd walking-skeleton delivery

Authority: [delivery-mission.md](delivery-mission.md) D1 and F1, and the assigned
`azd-walking-skeleton` task. This implements the approved replacement, not new
acceptance criteria or a waiver of deployed verification.

All three existing services retain `python_3_13`, Responses `2.0.0` and
`remote_build`. Their platform-specific predeploy hooks run
`scripts/check_azd_source.py` with Python, without an approved ZIP/hash, private
receipt or dependency on `TMPDIR`. The standard-library check verifies the
bounded `.agentignore` allowlist, the existing verified dependency feed,
direct-to-lock exact pins, source compilation and routing JSON syntax. It reads
only the selected public source, rejecting linked source. It does not inspect
private settings, authenticate, upload, install dependencies or mutate Azure.

`.agentignore` includes only the entrypoint, manifests, flat application Python
modules and the two routing documents. Bundled `packages/` is no longer included
in this remote-build path. `.dockerignore`, Dockerfile, dependency manifests,
`package_guard.py` and unused external exact-package release tools are unchanged.
Dependency resolution and Linux build success remain the supported remote
builder's responsibility; a local syntax check never proves them.

## Verified supported packaging interface

Observed installed toolchain: azd `1.37.1`, `azure.ai.agents` `1.0.0-beta.21`,
`azure.ai.projects` `1.0.0-beta.14`. Public source tag
`azd-ext-azure-ai-agents_1.0.0-beta.21` resolves to
`a0f69c325fa54ec6591fc6bf74dada3b500ea8be` in `Azure/azure-dev`.
Its `internal/project/service_target_agent.go` functions `packageCodeDeploy`
and `zipSourceDir` build the native ZIP, compute its hash and honor
`newAgentIgnoreMatcher`/`ShouldExclude`; `internal/project/agentignore.go`
defines root `.agentignore` with gitignore syntax. No extension packaging API,
temp ZIP interception or hand-built substitute artifact is introduced.

Source:
https://github.com/Azure/azure-dev/tree/azd-ext-azure-ai-agents_1.0.0-beta.21/cli/azd/extensions/azure.ai.agents/internal/project

## Checks and deployment handoff

Run `python -m unittest discover -s tests -p test_azd_source.py -v` and affected
`test_demo.py` regressions with the available application interpreter. Run
`python scripts/check_azd_source.py`. The source-check output hashes the selected
files for comparison; it is not an approval receipt or a deployed ZIP hash.
Git-based exclusion fixtures test policy semantics, not actual extension upload.

After importing validated settings through `scripts/Use-Settings.ps1`, verify
the dedicated lab Azure CLI/azd authentication, tenant/subscription and existing
project bindings without exposing private values. Under the existing shared
environment/configuration lock, select a clean exact committed candidate and run
normal `azd deploy --all --no-prompt`. Do not provision. Inspect each actual
operation before any retry; a timeout is not permission to resend.

Keep the lock for the separate EndToEndTestLoop probes of the same candidate:
all three existing role bindings, actual observed versions, source/artifact
identity, remote build outcome and supported invocation must be established.
An azd exit, uploaded bundle, source hash or healthy host alone cannot complete
D1. No dependent assignment is released by offline checks.

## Current execution observation

This turn started on `feature/azd-demo-delivery` at
`7fb5eef8f527ab6ac51819c9f63064d74e678a2e`, with a clean checkout.
Current local checks and their actual outputs are under
[`checks/azd-source-regressions.txt`](checks/azd-source-regressions.txt),
[`checks/azd-demo-regressions.txt`](checks/azd-demo-regressions.txt) and
[`checks/azd-all-regressions.txt`](checks/azd-all-regressions.txt).
These checks are offline; synthetic SDK/identity successes in their output are
not observations of the deployed project.

[`checks/azd-context-preflight.txt`](checks/azd-context-preflight.txt) records
that the deployment binding/profile/artifact settings are not populated in this
process, `.local` is absent, and no authoritative private settings path was
supplied to the assignment. No credential cache or copied `.azure` values were
inspected. This does **not** establish absent credentials or require any
historical filename. The user need only identify the current authoritative
allowlisted settings file; then DevOps can load it through the existing loader
and verify dedicated authentication and exact scope before deploying.
No `azd deploy`, remote build, role-version probe, runtime upgrade or new
workflow launch occurred. This owner is already executing inside the existing
delivery run; it does not start a recursive delivery workflow.

[`checks/azd-application-gate.txt`](checks/azd-application-gate.txt) separately
records a current `Test-Demo.ps1` exit 1: the available Python 3.13 installation
contains an unrelated `jetset-bank-demo-agents` distribution requiring older
framework versions, so `pip check` stops that wrapper before its tests.
Standalone application regressions are reported separately, not relabeled as
the wrapper passing. No shared Python packages were removed or replaced and
no dependency manifest was changed to waive this failure.

| Component | RAG | Evidence/freshness | Remaining work/next action |
|---|---|---|---|
| deployment | 🔴 | Current scoped-context preflight and local wrapper gate above; hooks replaced locally, no cloud attempt | Identify validated settings; resolve isolated local check environment; deploy exact commit and separately probe all three versions |
| coordinator-routing | 🟠 | Offline regressions only; no fresh deployed run | Verify trusted gates and genuine Decision-1 |
| architect | 🟠 | No fresh remote candidate | Verify actual findings-driven immutable revision |
| reviewer | 🟠 | No fresh remote review | Verify exact revised-candidate review |
| blob-shared-context | 🟠 | No fresh private MI exchange | Verify provenance and fenced publication |
| session-continuity-recovery-isolation | 🟠 | No fresh deployed scenarios | Verify follow-up, known recovery, supported stop/resume and isolation |
| terminal-demo | 🟠 | No fresh deployed terminal demonstration | Execute synthetic remote revision and follow-up |
