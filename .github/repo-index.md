# Repository index

Read this index before searching. Refresh the inventory with
`scripts\repo_index.py`; `--check` fails on drift. Only public Git-visible files
are indexed; ignored state, dependencies and external lab files are excluded.

## Architecture and search entry points

| Area | Entry points | Responsibility |
|---|---|---|
| Orchestration | `main.py`, `demo\host.py`, `demo\workflow.py`, `demo\coordinator.py` | Native checkpointed MAF graph; explicit preserved legacy coordinator |
| Contracts/configuration | `demo\artifacts.py`, `demo\contracts.py`, `demo\config.py`, `config\settings.example.json` | Strict artifacts/assignments and atomic generic native settings |
| Blob/routing | `demo\artifact_store.py`, `demo\routing.py`, `config\routing-corpus.json`, `scripts\calibrate_routing.py` | Role-owned immutable outputs, fenced journal/manifest, typed calibrated Decision-1 and shared admission |
| Foundry integration | `demo\foundry.py`, `agent_metadata.py`, `azure.yaml` | Trusted host/state/provider adapters; three native remote-mode services deployed, not live-accepted |
| Local client/transport | `demo\terminal.py`, `native_proxy.py`, `live_acceptance.py` | Private terminal, exact-origin proxy, bounded diagnostics, artifact-envelope audit and guarded compute stop/resume acceptance |
| Tests/package | `tests`, `Test-Demo.ps1`, `package_guard.py`, requirements and Dockerfile | Offline acceptance and preserved package controls |
| Design/handoff | `docs\design.md`, `docs\NEXT-SESSION-PROMPT.md`, migration plan/map, workflow | Target Blob/native-workflow design, exhaustive copy-first boundary |
| Local context/checks | `scripts\Use-Settings.ps1`, `Initialize-LabSettings.ps1`, `migration.py`, `Test-Repository.ps1` | Validated private linkage, deterministic preservation/public checks |
| Identity triage | `scripts\diagnose_identity.py`, `tests\test_diagnose_identity.py` | Lock-pin audit, synthetic SDK/HTTP probes and sanitized exact-response evidence analysis; no cloud calls or retry authority |
| Copilot context | `.github\copilot-instructions.md`, agents and skills | Bounded implementation/review and deployment gates |

External lab tooling is mapped in `docs\migration-map.json`; resolve its root
from private settings. There is no Terraform root or SSH launcher here.
`config\routing-calibration.json` records the successful real routing-v3
evaluation (eight ready and four missing-input cases correct, selected threshold
0.5/margin 0) on the unchanged frozen corpus. All four real evaluation journals
and the retired blank-facts calibration are retained. Request hashes bind policy
and explicit nonempty facts; no offline fixture is
release evidence. Application Windows/Linux gates pass; artifact infrastructure
is applied with scoped zero-change convergence. Reproduced native publication
is complete: architect 17/reviewer 15/coordinator 22 are active on
common bundle `51064aa426d28d0cfa6b126eac7fce5ab0e9a5a0667267ef105884c1805adde2`
with unchanged identities and earlier versions retained. Coordinator 19 proved
`DECISION_CALIBRATION_PROVENANCE`: absent facts became blank in the Windows
loader but defaulted nonempty in hosting. The local correction truly unsets
missing options, forwards explicit facts to all roles and validates the fresh
genuine calibration before packaging. Live execution now writes requirements and
a routing decision; the architect fails SDK preparation (`RuntimeError`,
`storage_error`) and its known operation is explicitly held. Deployed SDK-scope
diagnostics prove `NATIVE_HOST_PRINCIPAL`: no trusted user reaches the architect.
An actual HTTP-edge test preserves delegation headers; the required explicit
coordinator impersonation permission already exists. A supported platform/SDK
identity-propagation remedy remains blocked, with no principal substitution.
The pinned SDK preserves supplied identity through durable task recovery in an
offline regression. Exact-response read-only ingress-presence observation is
implemented. An earlier Bastion observation could not connect because the lab
command VM was deallocated. Existing
Azure Monitor query access independently confirms user/call present at the
coordinator and user absent/call present at the architect, with correlated
Responses POST HTTP 200. Deployed native calls now forward SDK
`context.platform_headers()` directly, without re-delegating the derived platform
user or forwarding the container-only user header. Legacy behavior and strict
scope checks remain unchanged. Explicit operator approval permitted starting
the existing command VM; fresh guarded connectivity and three-service
publication passed with exact hashes, unchanged identities and proven cleanup.
Fresh initial acceptance still holds `SPECIALIST_INCOMPLETE`; exact-response
observation confirms architect 17 again fails `NATIVE_HOST_PRINCIPAL`, with
call identity present and user identity absent. Supported opaque propagation
did not resolve the live failure; its cause remains unresolved. No platform
defect or missing permission has been established. Followup/restart/isolation
were not reached; acceptance/observation jobs and listeners closed.
Local, undeployed HTTP-edge diagnostics report only fixed-role header
presence/context-match flags correlated by a response-ID hash; no header
values, raw IDs, tokens or content are logged. Known-child failure observation
also reads the exact parent's bounded logs. A real native resource/client/
transport regression verifies this wiring; all 116 application tests pass on
Windows and Linux. These diagnostics do not authorize calls or resolve the
propagation failure.
Read-only exact-version reconciliation confirms coordinator 23 returns HTTP
404 while coordinator 22 remains active. The original diagnostic publisher's
owner and outcome are unbound; new retained lab observation/inspection tools
do not authorize publication replay or establish original mount closure.
Repeatable identity triage verifies 109 local lock pins and five mocked SDK
probes. Fresh exact-version metadata confirms the three deployed roles use
Responses 2.0.0 with the expected package and identities; actual nested
outbound context matching remains uncaptured. The current application suite
has 132 passing Windows/Linux tests (seven expected Linux skips).
Known-response stream recovery is deployed. The known
responses and pending parent are preserved, not resent. Completed remote work, MI private
Blob access, artifact provenance, isolation and actual hosting restart are unverified.
The approved linked-lab policy gives project agents account-wide Blob
Contributor: ownership/publication gates remain application-enforced, not
storage-enforced per-role isolation.
Do not search ignored `.azure`, `.azure-cli`, `.local`, `.migration` or
conversation/credential stores.

<!-- inventory:start -->

## Public file inventory

- `.agentignore`
- `.dockerignore`
- `.env.example`
- `.gitattributes`
- `.github\agents\distributed-agents-builder.agent.md`
- `.github\agents\distributed-agents-reviewer.agent.md`
- `.github\copilot-instructions.md`
- `.github\repo-index.md`
- `.github\skills\distributed-agent-implementation\SKILL.md`
- `.github\skills\lab-deployment\SKILL.md`
- `.github\skills\repo-index\SKILL.md`
- `.gitignore`
- `Dockerfile`
- `LICENSE`
- `README.md`
- `Test-Demo.ps1`
- `agent_metadata.py`
- `azure.yaml`
- `config\routing-calibration.json`
- `config\routing-corpus.json`
- `config\settings.example.json`
- `demo\__init__.py`
- `demo\artifact_store.py`
- `demo\artifacts.py`
- `demo\config.py`
- `demo\contracts.py`
- `demo\coordinator.py`
- `demo\foundry.py`
- `demo\host.py`
- `demo\routing.py`
- `demo\terminal.py`
- `demo\workflow.py`
- `docs\NEXT-SESSION-PROMPT.md`
- `docs\design.md`
- `docs\implementation-workflow.md`
- `docs\migration-map.json`
- `docs\migration-plan.md`
- `live_acceptance.py`
- `main.py`
- `native_proxy.py`
- `package_guard.py`
- `requirements.lock.txt`
- `requirements.txt`
- `scripts\Initialize-LabSettings.ps1`
- `scripts\Test-Repository.ps1`
- `scripts\Use-Settings.ps1`
- `scripts\calibrate_routing.py`
- `scripts\diagnose_identity.py`
- `scripts\migration.py`
- `scripts\repo_index.py`
- `tests\test_artifacts.py`
- `tests\test_config.py`
- `tests\test_demo.py`
- `tests\test_diagnose_identity.py`
- `tests\test_routing.py`
- `tests\test_workflow.py`

<!-- inventory:end -->
