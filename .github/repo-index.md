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
    "docs\\customer-prototype-*",
    "docs\\identity-*.md",
    "docs\\migration-plan.md",
    "docs\\migration-map.json",
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
| Tests/package | `tests`, `Test-Demo.ps1`, `package_guard.py`, requirements and Dockerfile | Offline regressions and build/package validation, not live acceptance |
| Current delivery | `delivery-input.json`, `docs\requirements\delivery-mission.md`, `docs\NEXT-SESSION-PROMPT.md`, `docs\implementation-workflow.md` | Authorized azd delivery and seven-component acceptance based on fresh observations |
| Design | `docs\design.md` | Current source lifecycle, conversations, state planes and correctness invariants |
| Local configuration/checks | `scripts\Use-Settings.ps1`, `scripts\Test-Repository.ps1`, `scripts\repo_index.py` | Allowlisted private configuration, public boundary checks and current/history search partition |
| CLI delivery workflow | `gh-dynamic-workflows`, `.github\extensions\autonomous-delivery\extension.mjs` | Registered lab-delivery runtime, distinct from the application's MAF graph |

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
- `.github\agents\workflow-owner.agent.md`
- `.github\agents\workflow-reviewer.agent.md`
- `.github\copilot-instructions.md`
- `.github\extensions\autonomous-delivery\extension.mjs`
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
- `demo\diagnostics.py`
- `demo\effect_observation.py`
- `demo\foundry.py`
- `demo\host.py`
- `demo\private_effect_capture.py`
- `demo\reviewer_agent.py`
- `demo\routing.py`
- `demo\specialist.py`
- `demo\terminal.py`
- `demo\workflow.py`
- `docs\NEXT-SESSION-PROMPT.md`
- `docs\design.md`
- `docs\implementation-workflow.md`
- `docs\requirements\delivery-mission.md`
- `gh-dynamic-workflows\.gitignore`
- `gh-dynamic-workflows\DELIVERY-PRINCIPLES.md`
- `gh-dynamic-workflows\LAB-CONTRACT.md`
- `gh-dynamic-workflows\LAB-DESIGN.md`
- `gh-dynamic-workflows\QUICKSTART.md`
- `gh-dynamic-workflows\README.md`
- `gh-dynamic-workflows\RESEARCH.md`
- `gh-dynamic-workflows\WORK-CARD-DEFINITIONS.md`
- `gh-dynamic-workflows\extension.mjs`
- `gh-dynamic-workflows\install.mjs`
- `gh-dynamic-workflows\lab-loops.mjs`
- `gh-dynamic-workflows\lab-workflow.mjs`
- `gh-dynamic-workflows\loop-source.mjs`
- `gh-dynamic-workflows\loop-workflow.mjs`
- `gh-dynamic-workflows\loops.yml`
- `gh-dynamic-workflows\package-lock.json`
- `gh-dynamic-workflows\package.json`
- `gh-dynamic-workflows\run.mjs`
- `gh-dynamic-workflows\scheduling.mjs`
- `gh-dynamic-workflows\task-context.mjs`
- `gh-dynamic-workflows\templates\extension.mjs`
- `gh-dynamic-workflows\templates\workflow-owner.agent.md`
- `gh-dynamic-workflows\templates\workflow-reviewer.agent.md`
- `gh-dynamic-workflows\test\evidence.fixture.mjs`
- `gh-dynamic-workflows\test\install.test.mjs`
- `gh-dynamic-workflows\test\lab-loops.test.mjs`
- `gh-dynamic-workflows\test\lab-sdk.test.mjs`
- `gh-dynamic-workflows\test\lab-workflow.test.mjs`
- `gh-dynamic-workflows\test\run.test.mjs`
- `gh-dynamic-workflows\test\scheduling.test.mjs`
- `gh-dynamic-workflows\test\scope-governance.test.mjs`
- `gh-dynamic-workflows\test\task-context.test.mjs`
- `gh-dynamic-workflows\test\work-cards.test.mjs`
- `gh-dynamic-workflows\work-cards.mjs`
- `gh-dynamic-workflows\workflow.mjs`
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
- `scripts\calibrate_routing.py`
- `scripts\diagnose_identity.py`
- `scripts\identity_handoff.py`
- `scripts\migration.py`
- `scripts\repo_index.py`
- `tests\test_artifacts.py`
- `tests\test_config.py`
- `tests\test_delivery_input.py`
- `tests\test_demo.py`
- `tests\test_diagnose_identity.py`
- `tests\test_diagnostics.py`
- `tests\test_effect_observation.py`
- `tests\test_host_diagnostics.py`
- `tests\test_identity_handoff.py`
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
