# Distributed agents: MAF/Foundry workflow and shared artifacts

## Reviewed selected-WSL exact-inventory source join

Task `RP-S2-INVENTORY-SOURCE-JOIN` consumes original Architect/Critic acceptance
of lab inventory commit `410b9a0c9627a8a69e5be57e84468d427a4025b9`
(current-run audit `4f2b6c31`). It implements the originating disposition
`["yaml-loops-v1:sprint/1/RP-S1/DevOpsWorkLoop","selected-wsl-exact-inventory"]`
only at its source/caller boundary, not as actual rollback readiness.
Selected reviewed inputs are application
`88d365f28a22cee725e4e60253ac505399216d5a` and lab
`903614f9b2d3e41453dfff551fb310bec8451168` on
`feature/customer-hosted-session-prototype`. Both exact inputs were pushed and
read back from origin, including retained integration `0cac08c9`, planning
`b29d9a0b`/`1e705fd3`/`aa236e8a` and inventory `410b9a0c`.
The concurrently completed, separately accepted Linux fixture/input commits
`88d365f2`/`97bba71c`/`903614f9` are also retained in this ancestry (audit
`f0698a28`); this smaller inventory handoff does not certify their final Linux
join. No merge, abandoned code, branch switch or canonical dirty adoption was
needed. The documentation/index commits from this integration await original
review before their later explicit push by existing integration/closeout.
The lab companion index is retained at
`f6e7d8b598db8907295954bf52df6efc56c187ef`; it changes navigation only.

### ReadOnly exact-inventory caller contract

After the unchanged application settings import, the retained lab
`foundry-tf/multi-agent/Invoke-WslCodeRelease.ps1` takes explicit
`ApplicationRoot`, reviewed `LabRepositoryRoot` and imported
`OperationalLabRoot`. Keep the dedicated context separate from loaded source.
With the retained host fingerprint, private output and approved read-only SSH
mount guards, supply **all four** selectors together:

| PowerShell parameter | Python argument |
| --- | --- |
| `InventoryService` | `--inventory-service` |
| `InventoryVersion` | `--inventory-version` |
| `InventoryExpectedPackageSha256` | `--inventory-expected-package-sha256` |
| `InventoryIdentityBaseline` | `--inventory-identity-baseline` |

Use `-Mode ReadOnly` only, for one of `multi-agent-architect`,
`multi-agent-reviewer`, `multi-agent-coordinator`. Version is a canonical
positive decimal of at most nine digits; package expectation is a 64-hex
SHA256. The baseline must already exist as an absolute private regular file,
at most 131072 bytes, outside the protected application/tool/operational
roots, with no reparse file or ancestor. Its matching `agent`, `exists: true`
and nonempty `instance_identity.principal_id` / `client_id` expectations must
be established independently **before** observation. Never derive expectations
from the response being checked or print their private values.

Partial quartets, Publish, InspectOwner and combined session monitoring fail
closed; absent selectors retain the prior latest-only ReadOnly behavior.
`wsl_release.inventory_selection` checks selectors, baseline and actual
`observe_agent.py` owner before transport. The inventory branch uses the
retained strict-trust/private-DNS/scoped-credential route for exact
`GET /agents/<service>/versions/<version>?api-version=v1`, reusing unchanged
`observe_agent.exact_metadata`. It does not list/latest-fallback or invoke
a session. Sanitized receipt `inventory` fields retain requested/returned
version, existence/status, package/identity matches, Responses protocol and
zero-inference evidence, not identity values or environment contents.
Absence, mismatches, malformed/HTTP/transport failures cannot pass; observation
alone is not rollback readiness before attributable outer cleanup and complete
rollback-package/effect accounting.

### Changed source evidence and downstream validation

Fresh no-effect imports verified actual owners for `release_roots`,
`identity_decision`, `bundle_package`, `wsl_release` and `observe_agent` in the
selected feature lab. Loaded PowerShell `Resolve-ReleaseRoots` belongs to that
same checkout and validates the matched explicit roots. All 22 application and
nine lab entries from `identity_decision.source_files` match committed source
after LF normalization. Its compact sorted-key JSON SHA256 is now
`bfd6ed4d380a354a11104e1207605f169991d16a08b71db7344e4cea7e9815e9`;
the historical `8974f4cd...` seal does **not** cover changed WSL bytes.
This runtime/Decision source set is not the wrapper, helper or Linux test-input
closure. Separately checked raw and LF-normalized hashes (equal here), all
matching committed bytes:

| Lab path under `foundry-tf/multi-agent/` | SHA256 |
| --- | --- |
| `Invoke-WslCodeRelease.ps1` | `25413d7100e93b8edd367b254986e57d736a7fb630123673e50dd3ba1ba5c37e` |
| `wsl_release.py` | `fb4bd55eae6554856f2f2d3955ce175f479f3da521374a674ec4a0c0d0d3aaf4` |
| `observe_agent.py` (unchanged) | `8768c3e4d7fa97886b2152db46bc1c950843fad35a3be763a678dc16298f7afe` |
| `release_roots.py` (unchanged) | `312c926b91a416c957efe66c387428dec179988f32164b6706892e0d5bb09fd1` |
| `Release-Roots.ps1` (unchanged) | `8438d8bdbc04f94bd1b8380601fe8423a66b3045ddd561ec46bc69eb9e987e27` |
| `tests/test_release_exact_metadata.py` | `7ea3800530e996be759768bdf908d304d0971a9d486a2f5a4905b0271dfa81d7` |
| `tests/test_release.py` | `3e548833c1401a17a98973c8fe147e829e5b515f157689e220c11316ae36fea9` |

Affected explicit-root/caller, exact-inventory and release/cleanup discovery
ran 100 tests in 50.001 seconds: 97 passed, zero failures, three inherited
native-Linux exclusions. Application `demo` and `live_acceptance` were explicitly
bound before retained discovery using the existing absolute validated Python.
These are local fixtures, not actual route or Linux/container results.
Source-owner complete suite evidence remains in audit `4f2b6c31`; it is not
reclaimed as fresh integration execution.

Original applicable E2E validates this inventory join before original DevOps
`RP-S2-FRESH-INVENTORY` executes exact private reads and joins local rollback/
effect preparation. It need not wait for package correction or unused Windows
helper acceptance. `RP-S2-CORRECTION-SOURCE-JOIN` separately owns final joined
input hashes, complete offline validation and measured README refresh before
actual Linux gates. Both actual readiness exits still gate one publisher and
common-bundle G1-G4/non-held initial parent. No settings import, authentication,
engine/build, transport/cloud, publication or inference occurred here.
Historical UNKNOWNs, held parents, rollback assets and cleanup uncertainty
remain; older sections below retain their originating evidence, not current
source seals or pending push status.

## Reviewed Linux-engine recovery source join

Task `RP-S2-ENGINE-SOURCE-JOIN` integrates reviewed application input
`7f8805dbb796e1ccc4299006449e89f91390488d` with reviewed lab input
`1dab1e012e510865eeec35fac69b1d43382c5595` on
`feature/customer-hosted-session-prototype`. Both exact refs were pushed and
independently read back from origin. Application ancestry retains previously
reviewed integration `576b613`/`0b6d99a`, current architecture/UX/release/sprint
planning `cef352f4`, `6b6975c0`, `48e3faf3`, `5cc0f692`, `ed986858`,
`a6398f06`, accepted README status `13e3b4b1`, and scoped mount amendments
`2f832f56`/`7f8805db`. Lab ancestry retains accepted context `42a70533`,
helper implementation `55a60e69`, startup-budget correction `1eec6d47`
and exact expected-mount correction `1dab1e01`. No merge, branch switch,
canonical dirty adoption or abandoned task code was needed.

Original Architect/Critic source acceptance was inspected in current run
`0159ec9f-a89c-47f9-986f-80d9dfe6740a`, audits `c96ccaae` and `b7e2c819`;
current planning and amendment audits also contain substantive agreement.
Originating disposition
`["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-LINUX-ENGINE-READINESS/AssignedWorkDeveloperLoop","linux-engine-exact-mount-contract"]`
is closed within its source-task boundary, not reopened as an execution gate.
This new integration documentation awaits its own original review and later
existing closeout push; it is not included in the reviewed-input push above.

Fresh no-effect `ReleaseRoots.select`, `identity_decision.source_files` and
`Resolve-ReleaseRoots` checks confirmed actual loaded Python modules
`release_roots`, `identity_decision`, `bundle_package`, `wsl_release` and the
PowerShell resolver belong to the selected reviewed tooling checkout, with
loaded/selected source equality. The compact sorted-key source closure remains
`8974f4cdae0850f8528d1261e6d9617e756e157316449385875d55e05f29b6f3`
(22 application and nine lab files). **That unchanged runtime/Decision seal
does not bind the new recovery helper or build-test inputs.** Their separately
verified SHA256 values, LF-normalized and matched to committed source, are:

| Lab path under `foundry-tf/multi-agent/` | LF-normalized SHA256 |
| --- | --- |
| `Ensure-LinuxEngine.ps1` | `08b47f61b38f5855906c552753896ecb2e57d58222d2070b01c953b8bd573ac5` |
| `tests/test_release_linux_engine.py` | `08c833156dd08e49dacce6ad40037bee1147f2606457de8769e2ee8ce9f9f3da` |
| `Build-Demo.ps1` | `ef9a78e75edf875f83454a12239dbf18f8cad775c7b14b1a29285df4467edf82` |
| `tests/test_release_native_settings.py` | `3642a111747ecd22669a11b96a5df537a6f98e815502728b03b6efebb1a0f622` |
| `Release-Roots.ps1` (unchanged) | `8438d8bdbc04f94bd1b8380601fe8423a66b3045ddd561ec46bc69eb9e987e27` |

The Windows helper and helper-test working copies use CRLF: their raw hashes
are respectively `6f07700ad8c11990ed203969a004b7bd3530fb0bdccba0f9cf75ef1ea8cc2324`
and `f70f04d40aed0057d8a0e4d90cd91d27e81575c0405198d3e3e37001e0d94c2e`;
the other three raw hashes equal the table. Do not treat normalization as
permission to reseal a package or historical receipt.

Changed-join Windows validation passed 204 application tests (50.179 seconds),
dependency and compilation checks, and complete retained `test_release*.py`
discovery: 207 tests, 204 passed, zero failed, three inherited native-Linux
credential-bridge/code-artifact exclusions (155.226 seconds). Retained discovery
explicitly bound application `demo` and `live_acceptance` before loading lab
tests; it includes all 13 synthetic-command/source helper cases and affected
root/build/mount regressions. No real Docker command was used for recovery.
The selected Git working trees were clean before and after source verification
and tests; only this assignment's three documentation paths are then changed.

Original E2E receives this changed exact join before original DevOps runs
the reviewed helper and actual Linux/amd64/hosting-Python/package gates.
`Build-Demo.ps1` remains offline; its helper mount is a public read-only
test input, not automatic engine startup. Existing three-root/context guards,
unchanged settings import, dependency/source/image checks and separate retained
Linux suite stay mandatory. Independent selected-WSL rollback/effect inventory
does not depend on the helper or this join. Both actual readiness exits still
gate one serialized publisher and final G1-G4/non-held initial parent; RP-S3
retains live continuity, supported stop/resume, isolation and truthful closeout.
No settings import, authentication, engine startup, Linux build, cloud query,
transport, publication or inference occurred here. Preserve historical UNKNOWNs,
held parents, rollback assets and cleanup uncertainty.

## RP-S2 current reviewed source and ref handoff

Task `RP-S2-RELEASE-SOURCE-HANDOFF` selects reviewed application feature input
`03a8c284bdbee2e8a81cbbf13a154d088c7ba436` and reviewed lab feature
`42a70533c567a8aed29f0ca076c0b5d58381fc77`. Both use
`feature/customer-hosted-session-prototype`. The current input includes accepted
integration `576b613`, sprint review `835713a`, retrospective `8e4019b`,
RP-S2 design `4a1b1add`, architecture `3d615f11` and execution plan `03a8c28`.
Original outcome audits `e0001d3b`, `f2f25e66`, `01e02e83`, `40236938`,
`76141390` and `295a22cb` were opened, including their agreement,
task-complete and empty unmet-criteria votes. These references belong to run
`bf0d82d9-657b-4055-9f7c-6306ce08163d`; acceptance is bounded source/planning
acceptance, not release acceptance.

Both selected working trees were clean. Accepted application integration
`1bd157d` and lab runner/foundation `1842984`/`d0073536` remain ancestors;
no merge, branch switch, abandoned code or canonical dirty-file adoption was
needed. The reviewed application input was pushed and independently read back
as the exact full `03a8c284` commit above. The lab push was already up to date
and remote readback equaled the exact full `42a70533` commit above.
This task's new documentation commit requires original review before its push;
the subsequent execution-documentation reconciliation owner handles that ref.

Fresh no-effect checks used checked-in `ReleaseRoots.select`,
`identity_decision.source_files` and PowerShell `Resolve-ReleaseRoots`.
The actual imported `release_roots`, `identity_decision`, `bundle_package`
and `wsl_release` modules and loaded PowerShell resolver all belonged to the
selected reviewed tool root. Raw resolver hashes and the 22-application/
nine-lab-file compact sorted-key JSON closure remain exactly the hashes in
the source-join section below, including closure
`8974f4cdae0850f8528d1261e6d9617e756e157316449385875d55e05f29b6f3`.
Before/after source-check Git snapshots matched. All ten changed paths since
accepted E2E input `576b613` were documentation/index paths; no runtime closure
drift was found. These are fresh source/ref observations, not new continuity
implementation or repeated-suite progress. No settings import, operational
profile validation, authentication, package build or cloud call ran here.

Original E2E receives the current exact join, including this documentation-only
commit after review. It must not infer package/live success from unchanged
runtime bytes or the prior Windows checks. Original-phase DevOps owns actual
Linux/hosting-Python checks and selected-route/fresh inventory readiness; one
publisher joins successful handoffs for guarded common-package release and
G1-G4. Unused Windows-helper acceptance is not a WSL-route prerequisite.
Preserve historical UNKNOWNs, held parents, rollback assets and cleanup
uncertainty; RP-S3 retains live continuity, recovery, isolation and closeout.

## Reviewed source join and operational-root handoff

The source join consumes, rather than reimplements, the accepted application
continuity, presentation, specialist-history and isolated-client work. The
application input is `57585e0f52a5c616af1e88bc8f06b2ef231dd800`, including
accepted integration `1bd157d05116b076b0aa45b4fb6bfe531e5d28d0` and README
correction `f4ec1496c6f59cb08142c3b875deefdf695de30c`. The reviewed lab input is
`42a70533c567a8aed29f0ca076c0b5d58381fc77`, including validation foundation
`d0073536c2969e885bdcc767ddccbebd7deda7d5` and accepted runner correction
`18429840e86d92c26611bae3ffdc7095ca87592d`. All are already ancestors on the
authorized `feature/customer-hosted-session-prototype` refs. No cherry-pick,
branch switch, abandoned task branch or canonical dirty-file adoption was
needed. Both reviewed input refs were pushed and exact remote refs read back;
the integration documentation itself awaits original review before its push.

Originating Architect and Critic substantively accepted the ownership/root
handoff and then the runner corrections. Their votes supersede the older
incomplete ownership report only within that originating boundary; stopped
history, unknown effects and downstream live gates remain intact.

**Keep three root roles separate.** `ApplicationRoot` selects application
source; `LabRepositoryRoot` selects the registered feature sibling's reviewed
tools; `OperationalLabRoot` selects only the existing dedicated context imported
by unchanged `scripts/Use-Settings.ps1`. Context never selects helper source.
Use the existing absolute validated Python and explicit reviewed tool root for
these no-effect checks:

```powershell
$python = '<existing-validated-absolute-python>'
$application = '<absolute-application-root>'
$lab = '<absolute-registered-feature-sibling-root>'
& "$application\Test-Demo.ps1" -Python $python -LabRepositoryRoot $lab
& "$lab\foundry-tf\multi-agent\Test-Demo.ps1" -Python $python `
    -ApplicationRoot $application -LabRepositoryRoot $lab
& "$application\scripts\Test-Repository.ps1" -Python $python
```

The implemented operational contract for the five guarded entry points is:

```text
-ApplicationRoot <application-source>
-LabRepositoryRoot <reviewed-tool-checkout>
-OperationalLabRoot <existing-imported-operational-root>
```

This applies to `Test-LabPrerequisites.ps1`, `Test-PrivateConnectivity.ps1`,
`Build-CodePackage.ps1`, `Build-BundledCodePackage.ps1` and
`Invoke-WslCodeRelease.ps1`. `Get-DeploymentPreview.ps1` and
`Invoke-IdentityDecision.ps1` propagate the same context; Python
`bundle_package.py` and `wsl_release.py` accept `--operational-lab-root`.
Calibration retains tool ownership while validating the operational profile.
`Build-Demo.ps1`, historical diagnostic/InspectOwner and legacy Decision Check
without explicit context remain offline source paths, not context selectors.

After the unchanged settings import, the operational root must match imported
`LAB_REPOSITORY_ROOT`; Windows `AZURE_CONFIG_DIR` must equal that root's existing
`.azure-cli`. WSL maps that same root's existing `.azure-cli/wsl` and retains
az/azd selection and environment restoration. Canonical existing directories,
tool/operational registry scope equality with imported tenant/subscription,
actual account/project/target checks and private-output exclusions remain
required. Omitted context permits only the tools' existing validated context:
no discovery, credential copy, duplicate/default profile or root-guard bypass.

**The source-contract mismatch is corrected and exercised offline, not
operationally certified.** Joined Windows checks passed 204 application tests
(49.814 seconds), dependency checks and compilation; retained discovery passed
194 tests (88.192 seconds), with three originating Linux-only exclusions.
Retained discovery explicitly bound application `demo` and `live_acceptance`
before importing the retained tests, avoiding the historical fixture collision.
`tests/test_release_roots.py:OperationalContextTests` exercises distinct/matched
roots, caller propagation, rejected roots/profiles/scope, calibration, WSL
mapping, restoration, loaded-source bytes and crossed-owner rejection.
The committed split-root Decision Check regression uses synthetic ZIP/version
inputs, not a hosting package or deployed inventory.

Direct module inspection also confirmed the selected sibling supplies
`release_roots.py`, `identity_decision.py`, `bundle_package.py` and
`wsl_release.py`; PowerShell's loaded resolver path and bytes equal that same
tool root. The checked-in `identity_decision.source_files` closure contains
22 application and nine lab files; SHA256 of its compact sorted-key JSON is
`8974f4cdae0850f8528d1261e6d9617e756e157316449385875d55e05f29b6f3`.
Raw resolver SHA256 values are
`312c926b91a416c957efe66c387428dec179988f32164b6706892e0d5bb09fd1`
(Python) and
`8438d8bdbc04f94bd1b8380601fe8423a66b3045ddd561ec46bc69eb9e987e27`
(PowerShell). Regenerate raw seals for the exact source before execution;
normalized historical equality is not a replacement. Private absolute paths
and per-file binding maps stay outside the customer repository.

Original E2E receives this changed exact source join, then original serialized
DevOps joins containment/resource/trust readiness and executes actual
Linux/common-package, guarded publication and live gates. This integration
does not inspect profiles, authenticate, query cloud inventory, use transport
or certify actual operational readiness. Preserve historical UNKNOWNs, held
parents, rollback assets and historical cleanup uncertainty. New internal
contract failures return to existing Scrum reconciliation, not invented
human-only authentication requirements.

## How the same specialist session is reused

The customer invariant is one hosted coordinator conversation repeatedly
invoking the same remote architect and reviewer sessions. The three hosted
roles are not three in-process objects. Read the following path in order:

1. [`demo/terminal.py`](../demo/terminal.py) restores the parent's framework
   `AgentSession` from its private session file, verifies the hosted session's
   pinned coordinator version and sends the next user turn with that session.
   A pending or held turn is not permission to send a follow-up.
2. [`demo/workflow.py`](../demo/workflow.py) derives the artifact scope from
   trusted hosting context. In `WorkflowRuntime.execute()`, the locked
   parent-scoped manifest's `children.get(role)` is the create-or-reuse lookup.
   Only a missing role calls `RemoteAgents.prepare()`; the resulting hosted ID,
   framework representation and pinned version are persisted before creation.
   `remote.create()` binds that exact child to its version. An uncertain create
   is inspected through `recover_creation()`, not blindly repeated.
3. [`demo/foundry.py`](../demo/foundry.py), `RemoteAgents.invoke()`, verifies the
   child still exists at its pinned version, restores
   `AgentSession.from_dict(child.framework)` and calls the remote
   `FoundryAgent.run(..., session=session, stream=True)`. The completed session
   representation is saved back to the child; coordinator publication persists
   the binding with the accepted effect. The same lookup and restored session
   apply on a within-turn revision and on a later completed user turn.
4. Inside each remote specialist, `load_or_create_llm_session()` loads
   `"history"` through `AgentSessionStoreProvider`'s `specialist_history_v2`
   store scoped by the hosting context. A new model `AgentSession` is created
   only if history is absent. The architect's `design_solution()` and reviewer's
   `review_solution()` pass that session to their model call; `store_design()`
   and `store_review()` persist it after validating/writing the immutable
   output. Follow these stages in
   [`architect_agent.py`](../demo/architect_agent.py) and
   [`reviewer_agent.py`](../demo/reviewer_agent.py).

The coordinator-to-specialist framework session and the specialist's internal
model-history session are distinct. Hosted/framework **identity fields** and
pinned versions remain stable within a parent; response IDs and service
continuations advance. Do not compare entire serialized sessions as if every
field should stay constant. Known model-response recovery retrieves the exact
journaled response and updates continuation without another model send; unknown
effects remain held.

The requirements artifact also carries earlier requirements, but replaying that
brief or producing plausible memory text does not prove model continuation.
Proof needs actual binding comparisons plus direct restored-history tests and
fresh-history controls for both specialists. Offline fixtures are not live
proof. A separate parent must have separate children and artifact scope; a
model-provided ID cannot establish trusted scope.

### Isolated specialist client candidate (RP-S2-ISOLATED-CLIENT)

The source candidate implements the
[accepted B client contract](customer-prototype-architecture.md#request-local-client-ownership-and-unchanged-trust)
in `WorkflowRuntime.resources()`. The original six-element tuple keeps its
meaning: store, remote specialists, original project, credential, HTTP, original
headers. Only the remote specialists receive a separate `ProjectClient`,
header copy and OpenAI-client cache. Routing, parent and model callers retain
opaque-only authority. Both project clients share the request-owned credential
and exact-origin, zero-retry HTTP transport; the exit stack closes project
pipelines before HTTP and credential.

`demo/foundry.py:specialist_identity_headers()` re-derives the full scope from
captured hosting context and the configured tenant/project, then compares it to
the runtime scope. It rejects unexpected platform headers, invalid delegation
syntax and call-ID-as-user substitution. The specialist copy carries the
unchanged opaque call header plus `x-ms-user-identity`, never `x-agent-user-id`.
It does not use the legacy `platform_identity_headers()` helper. Receiver
principal equality, pinned versions, child/history lookup, effect journals and
unknown-effect holds are unchanged.

`tests/test_isolated_client.py` exercises the actual resource factory and
SDK/Responses clients with controlled network/storage boundaries. Both roles
cover prepare, create, check, ambiguous-create inspection, attempted send and
exact-response recovery; restored hosted/framework/version bindings remain
intact. Negative tests cover changed/forged scope, invalid identity, failed
retrieval without send/create, and cleanup after success, setup failure,
binding failure and cancellation. Closing the specialist project does not
invalidate the original model client's shared HTTP transport. The existing
wire-log test now verifies candidate-only delegation and unchanged original
resources; diagnostic values remain redacted.

Local verification: the existing validated Python 3.12.10 environment passed
dependency checks, **192 offline tests in 23.865 seconds**, and compilation via
`Test-Demo.ps1 -Python <absolute-python> -LabRepositoryRoot <explicit-lab-root>`.
No dependencies were installed. These results do not prove principal namespace
compatibility, permission effectiveness, live specialist entry or release
acceptance. The candidate has no automatic path selector. Existing deployed
versions remain unchanged until the original DevOps loop deliberately publishes
the reviewed exact-source/common package. Source integration must join this
commit with the independently implemented lab runner, then run final-source
and Linux/package gates. Use only a fresh synthetic parent; never adopt held
historical parents or replay uncertain effects.

### Conversations, checkpoints and artifacts are different state

| Concern | Responsible source | Purpose |
|---|---|---|
| Parent and child conversations | `demo/terminal.py`, `demo/foundry.py`, each specialist's history stages | Keep hosted/framework identities and model continuation for the appropriate conversation |
| MAF checkpoints | `demo/host.py`, `create_workflow()` in `demo/workflow.py` | Resume graph/executor position at supported boundaries |
| Blob artifacts, manifest and effects | `demo/artifact_store.py`, `demo/artifacts.py`, `WorkflowRuntime` | Preserve exact requirements/outputs, accepted revisions, provenance, fenced publication and write-ahead effect reconciliation |

None substitutes for the others. New requirements invalidate the prior
candidate/review approval, not the parent/child session bindings. Checkpoints
alone cannot make a remote send exactly once. Application ownership/scope
checks are not storage-RBAC isolation under the linked lab's account-wide
Blob Contributor policy. See [recovery gates](identity-recovery-plan.md) for
the historical live blocker and [the terminal example](../README.md#two-turn-terminal-demonstration)
for baseline syntax, not a live-success transcript.

### Offline cross-scenario evidence assertions

`live_acceptance.validate_scenario_evidence()` joins existing per-scenario
acceptance proofs with private source observations. It performs no collection,
network call, inference, stop or retry. Existing `live_acceptance.py` arguments,
stdout events/parser and opt-in human presentation are unchanged. This callable
is an assertion entry point for retained local execution, not another persistent
comparison ledger or a new release gate.

Run from the application root with the existing absolute validated Python.
`$EvidenceInput` is an absolute private JSON path outside both repositories,
assembled by the execution owner from actual observations:

```powershell
& $Python -c 'import json,sys; from demo.terminal import private_state_path; from live_acceptance import validate_scenario_evidence; validate_scenario_evidence(**json.loads(private_state_path(sys.argv[1]).read_text(encoding="utf-8"))); print("Supplied scenario observations passed offline assertions.")' $EvidenceInput
```

Input keyword keys are `initial`, `followup`, `restart`, `isolated` and
`stopped_session`. Each scenario snapshot contains:

- `proof`: the existing full JSON proof emitted by `live_acceptance.run()`,
  including actual parent framework state, version, child-session metadata,
  delegations and result/artifact envelopes. Aliases alone are insufficient.
- `manifest`: the corresponding completed parent-scoped `Manifest` document,
  including both children's actual hosted/framework identities, pinned versions,
  current accepted references and parent response ID.
- `operations`: the complete cumulative immutable documents from that parent's
  existing `operations/<operation>/<transition>.json` namespace, each retaining
  its original `scope_binding` and `effect`. Include all transitions, not only
  accepted records; missing intent/dispatch, unresolved effects and changed old
  transitions fail closed.
- `creations` and `sends`: cumulative lists of operation IDs, **one entry per
  actually observed specialist create/request send**, from independent boundary
  captures, not lists deduplicated or reconstructed from journal intentions.
  Known-response GETs are not sends. Duplicate entries, missing operations,
  additional creations and response reuse fail. Collection completeness and
  source attribution remain execution-owner obligations.
- For `followup` and `restart`, `checkpoints`: a private capture association with
  `scope_binding` and `records` containing serialized MAF checkpoint documents
  from that parent's existing checkpoint store. Preserve all document fields
  (SDK message enums serialized to their values). The collector must bind the
  association to the actual scoped store; the SDK graph state alone contains
  no parent identity. Assertions require same scope, retained unchanged prior
  checkpoints, new checkpoints and unchanged graph signature after continuation.
- For `restart`, `stops`: one parent ID per actually observed stop POST. Supply
  the existing confirmed durable marker as `proof.hosting_restart`, not an
  invented success flag. `stopped_session` is the actual GET observation of the
  same pinned parent in idle state with matching newly advanced `stopped_at`.

Successful assertions mean the supplied observations are internally consistent:
stable actual parent/both-child identities and versions, new responses on each
turn, exactly two child creations, both-role invocation/effect/output joins,
current hashed requirements/artifacts and invalidated stale approval; confirmed
once-only supported stop plus retained checkpoints/effects without duplicate
sends; and separate-parent child/artifact scope with synthetic requirement
exclusion. The helper checks the fixed Harbor/Cedar synthetic scenarios, not
arbitrary customer transcripts. It rejects Harbor/queue leakage in isolated
candidate/review content (the isolated input deliberately mentions Harbor only
to exclude it). This is application-enforced isolation, not malicious-host or
storage-RBAC isolation.

No self-authenticating provenance or live capability follows from caller-supplied
JSON. DevOps must supply complete, source-bound private observations; original
E2E validates the joined implementation and the existing release gates still
apply. Missing captures are an unmet evidence condition, not authority to
recreate parents, repeat stops or resend unknown effects. Diagnostics from the
new helper are fixed codes without private values.

`tests/test_scenario_evidence.py` executes the real offline graph with controlled
remote/storage/router boundaries and real MAF checkpoints. Its initial fixture
forces four architect/reviewer revision calls. Positive JSON round-trip and
negative binding, version, missing-input, stale/current-output, queue-omission,
extra-create, duplicate-send/response, held-effect, stop/checkpoint, scope,
content-leak and release-drift controls are synthetic only. They do not perform
hosted compute stop/resume or replace live G1–G8 evidence.

## Following a request through the source

For Foundry hosting, `demo\host.py` hands request parsing and graph construction
to the top-level `parse_turn()` and `create_workflow()` functions
in `demo\workflow.py`. The coordinator graph reads in order:

1. **Begin:** append the user requirement to the shared artifact history.
2. **Route:** load accepted prerequisites, apply deterministic gates, and
   record a validated Decision-1 choice.
3. **Effect:** prepare and dispatch the selected remote specialist operation.
4. **Publish:** validate its assigned output, update the coordinator manifest,
   then return to routing or finish with a result.

For a teaching-oriented reading path, follow `WorkflowRuntime.begin()`, `route()`,
`execute()`, and `publish()` in `demo\workflow.py`. These lifecycle methods are
consecutive, in execution order; shared resource, provenance, journal and result
helpers follow them. Numbered stage comments keep each event's sequence visible
inline. `begin()` names the requirements content, immutable artifact and accepted
reference separately, then resets each turn field explicitly. `execute()` spells
out each role's output type/path and whether the candidate revision advances.
In particular, `route()` reads top to bottom:
resume the turn, validate prerequisites and deterministic finish/budget gates,
recover or prepare the journaled decision, request a model choice only if needed,
then validate and accept that choice. There is no private routing pipeline to
trace through. Shared helpers retain the storage, provenance and journal rules;
this readability refactor does not remove recovery or authorization checks.

Coordinator events open `BlobArtifacts` via `WorkflowRuntime.resources()`;
specialist classes construct their Azure SDK clients in their role-local code. The
`control` container holds requirements, decisions, operation records, and the
coordinator manifest; architect outputs go to `candidates`, and reviewer
outputs go to `reviews`. The coordinator owns manifest publication. These Blob
documents are distinct from MAF workflow checkpoints and Foundry agent-session
history; neither checkpoint nor conversation state replaces the write-ahead
effect record.

`demo\architect_agent.py` and `demo\reviewer_agent.py` define the two
specialist agent classes and contain their complete assignment lifecycles:

- **Architect:** `ArchitectAgent.run_assignment()` validates the assignment, reads
  requirements and any assigned prior design/review from Blob Storage, generates
  a `Candidate` design, validates its revisions, and writes an immutable candidate
  JSON artifact before returning its reference.
- **Reviewer:** `ReviewerAgent.run_assignment()` validates the assignment, reads the
  exact requirements and candidate from Blob Storage, generates a `Review`,
  validates its revisions/approval, and writes an immutable review JSON artifact
  before returning its reference.

The architect's `run_assignment()` is a five-stage recipe. The five methods sit
directly beneath it in execution order:

1. `connect_and_load_assignment()` registers Azure clients on the caller's
   `AsyncExitStack`, verifies the private storage path and assignment, and returns
   the Blob store, Foundry project, headers, assignment and any existing design.
2. `read_requirements_and_prior_work()` returns the model's input brief.
3. `load_or_create_llm_session()` returns the LLM conversation session store,
   session and model deployment, reconciling any completed design or pending call.
4. `design_solution()` generates design text or recovers a known model response.
5. `store_design()` validates and writes the candidate, saves the session, and
   returns its artifact reference.

The reviewer's `run_assignment()` uses the same five-stage pattern, with its
methods also directly beneath it:

1. `connect_and_load_assignment()` returns the Blob store, Foundry project,
   headers, validated assignment and any existing review, registering clients on
   the caller's `AsyncExitStack`.
2. `read_requirements_and_design()` returns a brief containing the exact
   requirements and candidate design.
3. `load_or_create_llm_session()` returns the reviewer's LLM conversation session
   store, session and deployment, reconciling any completed review or pending call.
4. `review_solution()` generates review text or recovers a known model response.
5. `store_review()` validates the review/revisions, writes the immutable review,
   saves the session, and returns its artifact reference.

Only each role's `run_assignment()` invokes its stage methods; stages do not call
each other. Completed-design/review early returns remain visible after session
reconciliation, without repeating inference or storage. Each orchestrator owns its
`AsyncExitStack`, including cleanup when connection setup fails partway through.
No pipeline framework or shared runtime wrapper is involved.

Both roles keep their own
pending-model journal, known-response recovery and existing-output reconciliation;
the read/generate/write sequence remains understandable within each role's file.
Both roles' first stages explicitly construct
Azure SDK `ManagedIdentityCredential`, `BlobServiceClient`, and the Foundry
`ProjectClient` (an `AIProjectClient` subclass). The stack closes these clients
on success, failure, or cancellation.
Private-path verification precedes artifact reads. The existing exact-origin,
no-retry Foundry transport is retained, as are Blob timeouts, private-network
checks and disabled proxy inheritance. There is no specialist dependency on
`WorkflowRuntime`, resource tuple, or new service abstraction.
The model itself receives input content and returns JSON; it has no storage tools.
Shared scoped access, serialization and immutable writes remain in
`demo\artifact_store.py`. `demo\specialist.py` shares only model instruction
formatting and agent resource cleanup; it is not another deployed agent.
`WorkflowRuntime.specialize()` passes explicit trusted hosting values to the appropriate class method.
MAF graph execution, trusted hosting checks, coordinator resource setup and coordinator
publication remain in `demo\workflow.py`. Locator contracts live with the
artifact/assignment schemas in `demo\artifacts.py`. Routing helpers remain in
`demo\routing.py`; Decision-1 is not a fourth hosted service.
Assignment/output locators require integer schema version 1 in their Pydantic
contracts, so agent/coordinator flows do not repeat version branches. Unsupported
versions fail as `ValidationError`; the coordinator retains an uncertain effect
without accepting the output. Deployment checks can validate fixed configuration,
but cannot replace request-time identity/scope, revision, deadline, artifact
integrity or model-response recovery checks. Those gates remain in the live path.
The migration map retains the original source filenames and hashes as history,
not as a current application-file inventory.
This source map describes code paths; it is not evidence that live
managed-identity Blob access or hosted acceptance has passed.

## Implementation status

This describes implemented source, not live acceptance or a fresh deployment
inventory. The workflow/artifact/routing code and offline tests exist; the
descriptor configures MAF hosting and remote specialists. Historical live
execution reached requirements and Decision-1 routing but held
`SPECIALIST_INCOMPLETE`: the architect failed `NATIVE_HOST_PRINCIPAL` before its
application executed. Matching outbound opaque call context did not supply the
missing trusted user at child ingress. Neither a provider defect nor a missing
grant is established. Reviewer completion, end-to-end managed-identity private
Blob provenance, continuity, supported compute stop/resume and isolation remain
unverified.

The [recovery plan](identity-recovery-plan.md#measured-baseline-not-assumptions)
retains exact historical versions/packages, diagnostics and the consumed
one-attempt exception. Its mixed diagnostic bundle is not final common-bundle
acceptance. The original publication UNKNOWN, held parents and historical
cleanup uncertainty remain preserved. No new diagnostic chronology or cloud
observation is asserted here.

The October 19 invocation authorizes new evidence-backed scoped corrective
work and guarded releases in the existing project; the older consumed exception
neither forbids all such work nor permits unknown-effect replay. Deployment and
live acceptance remain with DevOps. No speculative principal/header/grant
substitution or provider submission is authorized. See
[the implementation workflow](implementation-workflow.md) for source/package
gates and [G1-G8](identity-recovery-plan.md#application-objective-and-definition-of-done)
for the actual release proof.
The solution uses a Microsoft Agent Framework workflow, Foundry parent/child
sessions, strict specialist contracts, a durable operation journal and remote
Responses transport.

Exactly three hosted agent deployments are intended:

| Deployment | Responsibility | State/output ownership |
|---|---|---|
| Coordinator | Host the MAF workflow, authenticate the request, enforce gates, use Microsoft-Decision-1 for semantic choices, invoke remote specialists | Parent conversation, workflow checkpoint, operation journal, requirements and authoritative manifest |
| Architect | Read assigned requirements/review revisions and propose a candidate | Own child conversation and immutable candidate outputs |
| Reviewer | Read the exact assigned candidate and requirements and evaluate them | Own child conversation and immutable review outputs |

Do not instantiate specialists inside the coordinator in production or add a
fourth orchestration deployment. A local fake/in-process implementation remains
useful only as an explicit offline test adapter.

## State planes and identity

Three independent state planes have different purposes:

1. **Foundry conversation history:** the parent and each child have their own
   hosted session IDs and framework session representations. Pin each deployed
   version. Never use another agent's conversation object as shared storage.
2. **MAF workflow checkpoints:** resume stable workflow/executor IDs at supported
   superstep boundaries using the hosting SDK's supported checkpoint provider.
   Store through the supported Foundry-backed state integration, not in mutable
   conversation messages. Confirm APIs against the pinned SDK before coding.
3. **Blob artifact plane:** prerequisite documents, immutable specialist
   deliverables, validated decision records, a write-ahead operation record,
   and the authoritative manifest connecting accepted revisions.

Use a request-aware workflow factory and the supported
`CheckpointStoreProvider` integration if supported by the pinned hosting SDK.
Do not base the host on deprecated `workflow.as_agent()` APIs. If the pins cannot
support Foundry workflow hosting, document the exact incompatibility and make the smallest
coherent dependency update with compatibility tests and a regenerated lock.

The artifact conversation key is the **coordinator's trusted parent Foundry
hosted session ID**. A caller-supplied string or model-produced `session_id` is
not authorization. Derive the binding from validated request/platform identity.
Namespace it by canonical project, tenant and authenticated principal:

```text
v1/<project-scope-digest>/<tenant-principal-digest>/<parent-session-digest>/
    requirements/<requirements-revision>/<operation-id>.json
    decisions/<requirements-revision>/<operation-id>.json
    assignments/<operation-id>.json
    operations/<operation-id>/<transition>.json
    manifest.json
```

Candidates and reviews use the same trusted scope in their respective
containers. Digests produce safe bounded path components; persist the canonical
binding privately so digest equality is not mistaken for authorization.
Specialist child sessions differ from the parent. Issue a server-validated
assignment binding child role/session/version to that parent scope, operation,
exact inputs, permitted output type, and deadline. Verify the assignment on
every call, including resume. Do not let the model choose container names,
accounts, blob paths, tenant IDs, or parent IDs.

Existing hosted identities were observed and their exact container-scoped
grants applied. Actual runtime managed-identity Blob access and its private
network path have **not** been proven; verify them during live acceptance.
The subsequently approved trusted-lab policy adds account-wide Blob Contributor
for project agents, superseding effective per-role storage isolation.
Missing trusted principal context is a fail-closed condition, not permission to
use a default user. A terminal's UUID alone is not proof of ownership.

The baseline host's offline construction reports SDK response resilience
disabled: `store=true` alone does not recover an in-flight response after an
ungraceful crash. In the next iteration configure supported resilient hosting,
verify its storage integration, and test hard-kill/restart behavior. Where a
remote response remains unrecoverable, retain the explicit uncertain hold.
Neither a workflow checkpoint nor a stored conversation fixes this by itself.
The explicit acceptance restart uses the pinned hosted-session `:stop` API,
requires HTTP 204 and a new provider `stopped_at` in idle state, then continues
the same parent. Its durable write-ahead marker prevents resending an uncertain
stop. This tests supported compute deprovision/rehydration with persistent
volume, not an ungraceful hard kill or in-flight crash recovery.

## Blob access and network boundaries

Default to three containers in one private storage account: `control`,
`candidates`, and `reviews`. The names are generic configuration, not fixed
resource identities. Use separate managed identities for the three deployments.

| Identity | Control | Candidates | Reviews |
|---|---|---|---|
| Coordinator | Read/write | Read | Read |
| Architect | Read prerequisites | Read/write own outputs | Read assigned prior findings |
| Reviewer | Read prerequisites | Read assigned candidate | Read/write own outputs |

**Approved trusted-lab exception:** project agents now have account-wide Blob
Contributor access in the linked lab. The above matrix remains the application
adapter's ownership contract, not the effective Azure permission matrix.
Container-scoped grants are retained but cannot restrict an additional broader
grant. Immutable writes, assignment/parent checks and coordinator-only manifest
publication depend on trusted application code; an agent identity used outside
those adapters can read, overwrite or delete other roles' blobs. Do not claim
storage-enforced single-writer isolation or malicious-host isolation for this
lab. Live acceptance must report this limitation rather than expect RBAC
denials for cross-role access. This exception does not weaken schema, hash,
ETag, fencing, prerequisite or unknown-effect gates.

Use the least-privilege container-scoped data roles available; writer identities
may have delete permissions under built-in contributor roles. Enforce
append-only output semantics in application adapters, enable appropriate
soft-delete/versioning/retention, and assess custom roles or a broker if strict
storage-level immutability is required. The above matrix is a workload boundary,
not per-user isolation: Blob RBAC does not authorize arbitrary path prefixes.
Authenticate and authorize each artifact request in deterministic application
code. Do not expose general-purpose Blob read/write tools to the language model.
If directly invoked specialists cannot validate assignments with trusted
context, introduce a narrowly scoped broker capability or stronger service
authorization; do not pass storage account keys or trust JSON claims.

Use managed identity + HTTPS, disable public network and shared-key access,
avoid connection strings/account keys/SAS in prompts or evidence, and give the
runtime private DNS/network reachability to the Blob endpoint. Add DFS endpoints
and the corresponding DNS only if the selected storage mode actually uses DFS.
Verify checkpoint/history storage needs independently of this artifact account.
Do not assume creating a private endpoint makes hosted compute reach it.

Terraform, network/DNS configuration, registry allocations, and private
connectivity live in the lab repository. When adding a private zone there, also
add the private and public-equivalent VPN conditional forwarding entries in
the same change. Installation on the VPN server remains a user action.

## Artifact contracts

Use strict, versioned schemas with unknown fields rejected and bounded payloads.
An artifact envelope contains:

| Field | Requirement |
|---|---|
| `schema_version`, `artifact_type` | Supported version and typed document kind |
| `scope_binding` | Trusted project/tenant/principal/parent binding or its verified digest |
| `operation_id` | Application-issued idempotency key, not a model-generated ID |
| `producer` | Agent role, deployed name/version, child session and response IDs when applicable |
| `input_refs` | Exact immutable object names, hashes, schema and requirements/candidate revisions |
| `requirements_revision`, `candidate_revision` | Explicit causal relationship; review refers to the exact candidate |
| `content`, `content_sha256` | Canonical UTF-8 payload and deterministic verified digest |
| `publication_state` | Output is a proposal until coordinator acceptance |

Hash canonical serialization with nonfinite numbers rejected. Separate service
metadata from model-produced content. Define maximum bytes, nesting depth,
artifact count, and allowed media types before implementation. Treat text in
artifacts as untrusted data, not authority or executable instructions.
Do not substitute an alias, a mutable "latest" link, or a newly generated
requirements summary for the exact referenced source. Keep source provenance
and explicit ordered chunks when bounded routing context is constructed.

Specialists read only the assigned immutable inputs through typed adapters.
Architect emits a candidate whose revisions match the assignment; reviewer
emits an approval or blockers whose requirements and candidate revisions both
match. A review cannot approve while containing blockers. Malformed,
truncated, oversize, contradictory or stale outputs do not become ready
artifacts. Preserve existing baseline parsing/normalization regression tests,
but document intentional tightening instead of silently repairing content.

## Manifest publication and concurrency

The coordinator is the **sole authoritative manifest writer**. Specialists
write immutable operation-specific proposals, never the shared manifest.
Create outputs with `If-None-Match: *`; verify an existing object's hash and
provenance before treating it as an idempotent duplicate. A name collision with
different content is an integrity error.

Publish in this order:

1. Load and verify the session binding and current manifest generation/ETag.
2. Persist a pending operation with exact prerequisite references and reserved
   output name before any remote effect.
3. Invoke the pinned child session/version; record its response ID as soon as
   observable, without waiting for a final answer.
4. Specialist reads assigned inputs and writes its immutable proposed output.
5. Coordinator validates completion, ownership, input hashes, strict schema,
   revisions, producer version, and output hash; then conditionally updates
   the manifest with `If-Match: <observed-etag>`.
6. Mark the operation accepted and record the resumable workflow checkpoint.

On an ETag conflict, reread and reconcile the recorded operation and revisions.
Do not issue another specialist call as a conflict retry. One active writer
lease or equivalent fenced claim per parent must protect cross-instance turns;
ETag checks still protect publication if a lease expires. Define lease renewal,
fencing and crash recovery explicitly. A Windows local file lock is not
distributed coordination.

Downstream prerequisites are ready only when listed as accepted by the
manifest. Blob existence or a child completion event alone is insufficient.
New user requirements create a new revision and invalidate the current
candidate/review chain. No previous approval carries over automatically.

## Recovery and exactly-once limits

MAF superstep checkpoints are not a distributed transaction with Foundry
Responses or Blob publication. **Keep an application write-ahead journal** and
stable operation IDs to reconcile uncertain remote side effects.

| Observed recovery state | Safe action |
|---|---|
| Child creation pending, ID persisted | Query that exact session and reconcile its version/binding |
| Call pending, response ID persisted | Recover that response; do not create another response |
| Output exists, manifest not published | Verify exact provenance/hash and publish conditionally |
| Manifest accepted, checkpoint older | Reconcile the accepted operation without replaying the effect |
| Call may have happened, no recoverable response ID | Hold as uncertain; surface the condition for reconciliation |
| Expired/deleted session, changed deployment version, incompatible state | Stop or use an explicit reviewed migration; never silently start over |

Retries are bounded and permitted only where idempotency/recovery is established.
Record retry budgets and reconcile before resending. Resume restores child IDs,
deployed versions, requirements revision, artifact refs, pending effect,
manifest generation, and MAF workflow position. A new process must not
clear pending state or switch from remote to in-process to appear successful.

Define retention, user deletion/export, and encryption policies across all
three state planes. Ordinary cleanup must not delete pending operations or
prerequisites needed by resumable sessions. Deletion requires explicit scope
and authorization; do not write an automatic destructive migration.

## Microsoft-Decision-1 routing

Use Microsoft-Decision-1 for the coordinator's semantic choices, not to generate
designs or authorize actions. Reuse the **contract pattern**, not environment
secrets or the whole application, from the sibling think-fast project:
`.contracts/decision-provider.yml`, `.contracts/decision-runtime.yml`, and
`docs/shared-routing-policy-design.md`. The shared-routing design is a proposal;
verify implemented provider behavior against the pinned API/SDK.

Deterministic code first computes allowed actions:

| Choice | Deterministic prerequisites |
|---|---|
| Ask architect | Bound session, accepted requirements, remaining budget, no unresolved effect |
| Ask reviewer | Accepted current candidate and exact requirements refs |
| Finish | Current review approves the current candidate with no blockers |
| Request input | Safe clarification/hold path; cannot conceal transport or integrity errors |

Do not call a model when a deterministic next action suffices or no safe action
is available. Where a semantic choice remains, send bounded application-owned
state, explicit alternatives, decision criteria, exact revision/provenance
references, and relevant findings. Do not share mutable agent conversations.
The criteria should distinguish missing user information, needed design
revision, review readiness, and final readiness.

Validate the provider response against its actual decision wire contract:
typed action/probability associations, unique allowed choices, finite values
in range, valid distribution where required by that contract, and bounded
usage metadata. Do not invent a probability format or treat a generative
response as a Decision-1 result. Pin the deployment alias through configuration.
Persist the input schema/policy/model versions, state hash, candidate choices,
provider outcome, probability information, measured usage, and final gated
action in an immutable decision record.

Probability is a selection signal, **not** permission. Calibrate confidence
threshold and margin/abstention policy using a checked-in evaluation corpus;
do not copy a hardcoded threshold just to avoid clarification. Invalid,
unavailable, or low-confidence routing is explicit; it never falls back to
an unapproved model or bypasses prerequisites. A deterministic safe hold may
be used with its reason, distinct from user-information clarification.

The earlier lab context recorded a 17 RPM Decision-1 deployment limit; that is
historical context, not a new quota check or a portable default. Verify live
capacity before deployment. Use configured bounded admission control and
shared enforcement across coordinator instances, cancellation, deadlines, and
bounded 429 handling. Do not create a scaling/benchmark loop or alter quota
under this task.

## Compatibility, evidence, and acceptance

The current blocked identity-propagation recovery is specified in
[identity-recovery-plan.md](identity-recovery-plan.md), including the objective,
conditional feasibility, dependency graph, safe parallelism and G1-G8 live
exit criteria. It preserves this architecture rather than replacing user
identity with a session ID or an assignment field.

Preserve the Responses streaming/final aggregation contract, role routing,
alias-versus-real-ID distinction, terminal pending-turn holds, strict revision
checks, stored remote response recovery, and credential-free artifact contents.
Version new manifest/workflow schemas independently of the baseline ledger.
Document whether old sessions remain on their old version or migrate through
an explicit adapter; do not reinterpret old state as new schema.

Offline acceptance covers role access, trusted scope isolation, exact-input
revision checks, malformed artifacts, duplicate/conflicting publication,
cross-instance ETag/fencing conflicts, Decision-1 contracts, budgets, transport
errors, cancellation, and crashes at each publication boundary. It must prove
no duplicate remote effect after process restart where recovery is possible,
and an explicit hold where it is not.

Live acceptance must prove all three intended deployments/versions, remote
specialist calls rather than in-process calls, actual managed identity Blob
access over the private path, parent continuity across turns/restart,
isolated parents, prerequisite consumption, accepted candidate/review hashes,
and Decision-1 routing evidence. Inspect synthetic outputs and sanitized
metadata, not secret-bearing transcripts. A passing offline test, copied azd
environment, successful upload, or healthy host alone is not this acceptance.
