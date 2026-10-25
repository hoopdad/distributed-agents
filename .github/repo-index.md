# Repository index

Current source and current observed outcomes guide delivery. Historical failures,
denials, planning ownership and exhausted task lists do not establish current
blockers. Unexecuted live checks are unverified, not failed.

Use the entry points below before searching. Refresh both inventories with
`scripts\repo_index.py`; `--check` fails on drift. `--search-files` lists the
current public search scope. Private context and external lab files are excluded.

## Default search scope

The `ignore` field excludes historical context from the main inventory and
`--search-files`, not from Git or filesystem access. Do not include it in broad
searches. Open `.github\repo-history-index.md` only for a specific historical
question required by current evidence; then search explicit historical paths.
History may explain a finding but never creates a current blocker by itself.

<!-- search-scope:start -->
{
  "ignore": [
    ".github\\repo-history-index.md",
    ".github\\agents\\workflow-owner.agent.md",
    ".github\\agents\\workflow-reviewer.agent.md",
    "gh-dynamic-workflows/*",
    "docs\\customer-prototype-*",
    "docs\\identity-*.md",
    "docs\\migration-plan.md",
    "docs\\migration-map.json",
    "docs\\requirements\\delivery-architecture.*",
    "docs\\requirements\\delivery-user-experience.*",
    "docs\\requirements\\delivery-release-plan.*",
    "docs\\requirements\\delivery-sprint-*",
    "docs\\requirements\\checks\\delivery-*",
    "docs\\requirements\\client-release\\delivery-sprint-architecture.md",
    "docs\\requirements\\coordinator\\delivery-sprint-architecture.md",
    "docs\\requirements\\shared-context\\delivery-sprint-architecture.md",
    "docs\\requirements\\specialists\\delivery-sprint-architecture.md",
    "docs\\requirements\\client-release\\architecture.md",
    "docs\\requirements\\coordinator\\architecture.md",
    "docs\\requirements\\specialists\\architecture.md"
  ]
}
<!-- search-scope:end -->

## Architecture and search entry points

| Area | Entry points | Responsibility |
|---|---|---|
| Application workflow | `main.py`, `demo\host.py`, `demo\workflow.py` | MAF graph: begin, route, execute, publish; trusted scope, checkpoints and write-ahead effects |
| Specialist agents | `demo\architect_agent.py`, `demo\reviewer_agent.py`, `demo\specialist.py` | Independent remote conversations; exact assigned inputs, model response recovery, immutable outputs |
| Contracts/configuration | `demo\artifacts.py`, `demo\contracts.py`, `demo\config.py`, `config\settings.example.json` | Typed artifacts, assignments, manifests and validated settings |
| Blob/routing | `demo\artifact_store.py`, `demo\routing.py`, `config\routing-corpus.json`, `config\routing-calibration.json` | Exact provenance, coordinator ETag publication, calibrated Decision-1 choices |
| Foundry integration | `demo\foundry.py`, `agent_metadata.py`, `azure.yaml` | Host/session/provider adapters and exactly three remote services |
| Terminal/acceptance | `demo\terminal.py`, `native_proxy.py`, `live_acceptance.py` | Terminal flow, exact-origin transport and actual remote continuity/recovery/isolation checks |
| Identity-path probe | `demo\identity_probe.py`, `demo\host.py`, `live_acceptance.py` | Bounded Invocations and native Responses context/discovery diagnostics on existing hosts; diagnostic-only direct-call header comparison and known child-response receipts, ordinary workflows unchanged, no model/business-artifact work, automatic retry or production transport switch |
| Delegation diagnostics | `demo\delegation_diagnostics.py`, `scripts\diagnose_delegation.py`, `demo\identity_probe.py`, `tests\test_diagnose_delegation.py`, `tests\test_identity_probe.py` | Shared redacted wire/error capture; terminal versus genuine coordinator-hosted MCP discovery, pinned delegated sources and private request correlation; no tool/model/artifact work or assumed root cause |
| Tests/package | `tests`, `Test-Demo.ps1`, `package_guard.py`, requirements and Dockerfile | Offline regressions and build/package validation, not live acceptance |
| Normal azd delivery | `scripts\check_azd_source.py`, `scripts\build_azd_bundle.py`, `.agentignore`, `azure.yaml`, `tests\test_azd_source.py`, `docs\requirements\azd-walking-skeleton.md` | Bounded public-source checks and unchanged pinned Linux dependency bundles for normal azd; wheel/closure/RECORD validation before packaging, legacy exact-package tools unchanged, deployed verification still required |
| Current delivery | `delivery-input.json`, `docs\requirements\delivery-mission.md`, `docs\NEXT-SESSION-PROMPT.md`, `docs\implementation-workflow.md` | Authorized azd delivery and seven-component acceptance based on fresh observations |
| Design | `docs\design.md`, `docs\requirements\delivery-architecture.md`, `docs\requirements\delivery-architecture.json` | Current source lifecycle plus D1-D7 solution model, state-plane contracts, source/test joins and exact-candidate delivery handoff; architecture checks are not live acceptance |
| Terminal UX | `docs\requirements\delivery-user-experience.md`, `docs\requirements\delivery-user-experience.json`, `tests\test_delivery_user_experience.py` | Mission-traceable terminal principles, all architecture journeys, screen/state direction and executable UX contracts; design/schema completion is not deployed acceptance |
| Release planning | `docs\requirements\delivery-release-plan.md`, `docs\requirements\delivery-release-plan.json`, `tests\test_delivery_release_plan.py` | D1-D7 sprint goals, deployed-first skeleton, dependency/resource contracts and exact-candidate DevOps/E2E handoffs; planning validation is not live acceptance |
| Sprint terminal design | `docs\requirements\delivery-sprint-design.md`, `docs\requirements\delivery-sprint-design.json`, `tests\test_delivery_sprint_design.py` | Current sprint task-to-screen joins, terminal wireframes, private revision trail and inherited safe actions; contract checks do not establish deployed acceptance |
| Sprint architecture | `docs\requirements\delivery-sprint-architecture.md`, `docs\requirements\delivery-sprint-architecture.json`, `tests\test_delivery_sprint_architecture.py` | Holistic solution-model reuse, four tier designs, six approved task/source/test/flow joins and unchanged exact-candidate verification handoffs; no runtime or deployed acceptance |
| Sprint dispatch planning | `docs\requirements\delivery-sprint-plan.md`, `docs\requirements\delivery-sprint-plan.json`, `scripts\build_sprint_plan.py`, `tests\test_delivery_sprint_plan.py`, `tests\test_delivery_sprint_dispatch.mjs` | Six approved owner/card assignments, critical-path estimates and deployed-first dependency fan-out; local schema/synthetic scheduler checks are not implementation dispatch or deployed acceptance |
| Local configuration/checks | `scripts\Use-Settings.ps1`, `scripts\Test-Repository.ps1`, `scripts\repo_index.py` | Allowlisted private configuration, public boundary checks and current/history search partition |

Authorization and unknown-effect safety are runtime invariants, not historical
review ceremonies. Preserve actual persisted held operations; do not replay
uncertain effects. Current observations determine whether a new operation is
blocked. No historical status is a substitute for inspecting the current state.

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
- `delivery-input.json`
- `demo\__init__.py`
- `demo\architect_agent.py`
- `demo\artifact_store.py`
- `demo\artifacts.py`
- `demo\config.py`
- `demo\contracts.py`
- `demo\coordinator_agent.py`
- `demo\delegation_diagnostics.py`
- `demo\diagnostics.py`
- `demo\effect_observation.py`
- `demo\foundry.py`
- `demo\host.py`
- `demo\identity_probe.py`
- `demo\private_effect_capture.py`
- `demo\reviewer_agent.py`
- `demo\routing.py`
- `demo\specialist.py`
- `demo\terminal.py`
- `demo\workflow.py`
- `docs\NEXT-SESSION-PROMPT.md`
- `docs\design.md`
- `docs\implementation-workflow.md`
- `docs\requirements\azd-walking-skeleton.md`
- `docs\requirements\checks\azd-all-regressions.txt`
- `docs\requirements\checks\azd-application-gate.txt`
- `docs\requirements\checks\azd-context-preflight.txt`
- `docs\requirements\checks\azd-demo-regressions.txt`
- `docs\requirements\checks\azd-descriptor-schema.txt`
- `docs\requirements\checks\azd-repository-check.txt`
- `docs\requirements\checks\azd-source-check.txt`
- `docs\requirements\checks\azd-source-regressions.txt`
- `docs\requirements\delivery-mission.md`
- `docs\requirements\shared-artifacts\delivery-sprint-architecture.md`
- `live_acceptance.py`
- `main.py`
- `native_proxy.py`
- `package_guard.py`
- `requirements.lock.txt`
- `requirements.txt`
- `scenario_state_reader.py`
- `scripts\Initialize-LabSettings.ps1`
- `scripts\Test-Repository.ps1`
- `scripts\Use-Settings.ps1`
- `scripts\build_azd_bundle.py`
- `scripts\build_sprint_plan.py`
- `scripts\calibrate_routing.py`
- `scripts\check_azd_source.py`
- `scripts\diagnose_delegation.py`
- `scripts\diagnose_identity.py`
- `scripts\identity_handoff.py`
- `scripts\migration.py`
- `scripts\repo_index.py`
- `tests\test_artifacts.py`
- `tests\test_azd_source.py`
- `tests\test_config.py`
- `tests\test_delivery_architecture.py`
- `tests\test_delivery_input.py`
- `tests\test_delivery_release_plan.py`
- `tests\test_delivery_sprint_architecture.py`
- `tests\test_delivery_sprint_design.py`
- `tests\test_delivery_sprint_dispatch.mjs`
- `tests\test_delivery_sprint_plan.py`
- `tests\test_delivery_user_experience.py`
- `tests\test_demo.py`
- `tests\test_diagnose_delegation.py`
- `tests\test_diagnose_identity.py`
- `tests\test_diagnostics.py`
- `tests\test_effect_observation.py`
- `tests\test_host_diagnostics.py`
- `tests\test_identity_handoff.py`
- `tests\test_identity_probe.py`
- `tests\test_isolated_client.py`
- `tests\test_private_effect_capture.py`
- `tests\test_profiling_integration.py`
- `tests\test_repo_index.py`
- `tests\test_repository.py`
- `tests\test_routing.py`
- `tests\test_scenario_collection_seams.py`
- `tests\test_scenario_evidence.py`
- `tests\test_scenario_state_reader.py`
- `tests\test_sdk_diagnostics.py`
- `tests\test_specialist_continuity.py`
- `tests\test_transport_diagnostics.py`
- `tests\test_typed_checkpoint_export.py`
- `tests\test_workflow.py`

<!-- inventory:end -->
