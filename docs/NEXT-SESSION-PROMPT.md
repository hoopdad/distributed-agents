# Next-session invocation

Start Copilot in the `distributed-agents` repository and submit the following
prompt. Merely reading this file is not deployment approval: authority comes
from the user submitting the invocation, with the private configured scope.

---

Implement and deploy the next iteration described in `docs\design.md`, following
`docs\implementation-workflow.md` and the external lab's checked-in
infrastructure workflow. Complete the engineering and deployment loop, not
just a proposal or partial scaffolding.

First read README, `.github\copilot-instructions.md`, `.github\repo-index.md`,
the design, migration plan/map and implementation workflow. Invoke the local
repo-index skill before searching. Load `.local\lab-settings.json` through
`scripts\Use-Settings.ps1` without displaying private values. It specifies the
authorized existing lab project/region, model aliases, external repository root,
and dedicated lab CLI profile. Validate its scope against the lab registry.
If the private file is missing or scope has changed, stop for explicit inputs.
Do not read/display copied `.azure` environment values or any secret material.

I authorize changes to this application's code/configuration/tests/docs and
the linked lab's required Terraform/network/DNS/identity/release integration
for this design. Keep all infrastructure and unique tunnel/WSL deployment
tooling in the lab. Keep portable code/generic config in this repository.
Preserve original snapshots, dirty work, existing release safeguards and
unrelated applications. Do not delete originals or change quotas.

Build exactly three hosted deployments: coordinator hosting a **native MAF
workflow**, remote architect, remote reviewer. Use Microsoft-Decision-1 for
bounded coordinator semantic choices after deterministic authorization,
prerequisite, revision, schema and budget gates. Consult the sibling think-fast
decision-provider/runtime contracts and shared-routing-policy design for the
typed bounded-state pattern; do not copy private configuration or assume its
proposal is implemented. Verify SDK/provider APIs against pins and update
dependencies only with a specific compatibility reason.

Implement the shared Blob artifact plane keyed by the **trusted parent Foundry
session binding**, not an arbitrary supplied string. Separate native histories,
workflow checkpoints and artifacts. Use managed identity/private access, three
role-owned containers, immutable operation outputs, exact hashed prerequisite
refs, coordinator-only ETag manifest publication, and a recoverable write-ahead
effect journal. Preserve child/version bindings, unknown-response holds and
cross-instance fencing. Make restart, concurrency, malformed output, stale
revision, isolation, provider failure and interrupted publication tests pass.
Do not silently fall back to in-process production calls or another model.

Before deployment, parameterize and test the lab-owned build/preflight/WSL
release chain for separate application/lab roots. Existing `ProjectDirectory`
staging alone does not fix its original-source assumptions. Preserve Linux
native dependency/ELF checks, exact approved ZIP hashes, locked provenance,
strict host fingerprints, scoped versions and bounded process cleanup.

Use deterministic checked-in scripts and objective gate evidence. Gates are
self-approved when their pass criteria succeed; do not ask routine approval
between them. After required repository checks/review pass, commit and push
only scoped non-secret application and lab changes, inspecting staged files
first. Include required Copilot trailers. Run lab `Connect-LabAzure.ps1` then
`Invoke-HubDeployment.ps1` for the configured region. Use device-code login
and verified tenant/subscription with the lab-local `.azure-cli` profile.
Communicate the device URL/code if authentication is needed and resume after
I finish it. The default is successful plan followed immediately by applying
the exact saved plan; I am not requesting a separate plan-approval pause.

I authorize application code publication through the reviewed lab release
procedure to **only the three named services in the privately configured existing
Foundry project**, and synthetic live acceptance against that same project and
its Terraform-managed artifact storage. This includes the temporary **read-only**
SSH identity mount required by that procedure, without reading/copying keys,
and use of existing service versions only after the release preview verifies
their exact configured-project binding and expected versions. Generate and
verify the exact package hash and scoped preview before publication; do not
publish stale lab application code. If any scope, version or required approval
is unresolved, stop for confirmation. Do not invoke real customer workloads.

Ad hoc Azure mutation scripts, new accounts, quota changes, unrelated services,
destructive migrations, and broader publish scopes are not authorized.
Do not use `azd up/provision`, browser login or cached production credentials.
Diagnose failing checks/deployments, make the smallest coherent fixes, rerun
the affected gates, commit/push safe fixes and retry only when reconciliation
proves retry is safe. Never resend an uncertain remote response or publication
to make progress.

Never log in to or modify the VPN server. For required forwarding changes,
deliver reviewed non-secret lab configuration and exact `cd ~/azure-lab`
pull/review/install/validate/restart/rollback instructions; stop until I confirm
the server change. Never read/stage VPN secrets. A secret boundary, unsupported
native hosting API, material unresolved design/cost/residency decision,
unrecoverable unknown effect or failed objective gate is a stop condition,
not permission for a workaround.

Finish only after offline suites and synthetic live acceptance prove:
the intended three versions are healthy; specialists are remote; MI Blob
access uses the private path; exact prerequisites and accepted outputs are
verified; Decision-1 routing is recorded; one parent continues across turns and
restart; two parents remain isolated; pending uncertain work is surfaced; and
the exact deployed package and rollback versions are recorded. Explain any
blocked or undeployed condition plainly. Update README/design/index to match
what actually shipped.

---
