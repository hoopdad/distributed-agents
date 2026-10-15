# Implementation and lab deployment workflow

This is a checked-in gated engineering process, not a registered dynamic
multi-agent workflow. The native MAF workflow described in `design.md` is the
application being built. Do not launch a large agent orchestration merely
because this document says "workflow."

Each gate self-approves only when its objective evidence passes. Use explicit
inputs and deterministic checked-in scripts for repeated validation, build,
comparison, preflight and release steps. No routine approval pauses between
gates. Stop for a material unresolved decision, secret boundary, ambiguous
destructive scope, failed gate with no justified remedy, user authentication,
VPN-server execution, or unapproved mutation.

## Gate 1: Scope and baseline

Read README, Copilot instructions, index, design, migration map/plan and this
workflow. Load ignored private settings without displaying their values.
Resolve the external lab repository; read its startup, infrastructure workflow,
registry, network design and affected roots before changing it.

Pass: cleanly distinguish existing baseline from planned behavior; account for
every retained capability and relevant dirty change; validate configured
project/region/aliases; establish existing offline test results. Preserve
source snapshots, old sessions and unrelated changes.

## Gate 2: Application contracts and native workflow

Implement strict versioned artifact/assignment/manifest/operation schemas,
typed Blob adapters, identity binding and per-role access; native checkpointed
MAF orchestration; remote Responses specialists; Decision-1 contract validation
and bounded routing/admission control. Preserve the recoverable write-ahead
effects journal. Model outputs cannot grant authority or publish themselves.

Pass: focused tests cover publication crash boundaries, ETag/fencing conflicts,
immutable duplicates, parent isolation, malformed/stale output, response
recovery, unknown-effect holds, native checkpoint resume, routing prerequisites
and provider errors; the complete application suite passes with existing pins
or a documented compatible update. Three production deployments use remote
mode with no silent local fallback. Legacy session policy is explicit.

## Gate 3: External lab infrastructure

Any infrastructure/network/DNS/monitoring/region change follows the external
lab's `docs\infrastructure-change-workflow.md` in full. Use AVM-first Terraform,
private connectivity and managed identities. Keep Terraform and environment
resource definitions in the lab, not here. Derive region/subscription/address
allocations from `ip-registry.json`, register VNets before planning, validate
and perform fail-on-stale pruning; never automatically delete stale entries.

Pass: lab design/registry/implementation/security/cost gates pass; private
Blob identity/network permissions and hosted compute reachability are proven
in design and preflight, not assumed. Private DNS additions include both
private/public-equivalent VPN forwarding entries in the same change. Update
lab `docs\network-design.md` for topology/operational-boundary changes.

Commit and push only scoped non-secret changes after repository checks and
the required review. Inspect the exact staging list. This does not deploy the
VPN-server configuration and does not authorize unrelated changes.

## Gate 4: Verified Terraform execution

Run these commands **from the external lab root** for the registered region:

```powershell
.\scripts\Connect-LabAzure.ps1 -Region <region-key>
.\scripts\Invoke-HubDeployment.ps1 -Region <region-key>
```

The first command uses the repository-local `.azure-cli` profile and
`az login --tenant <registered-tenant-id> --use-device-code`. Communicate the
displayed device URL/code and continue after the user completes authentication.
Verify selected tenant/subscription before resource queries. Do not use normal
production credentials, browser login or cached context as a substitute.

The deployment wrapper enforces registry validation and monitors Terraform
init, fmt/check, validate, plan and apply. Default: apply the **exact saved plan**
immediately after successful plan. Pause between plan/apply only if the user
explicitly requested plan approval. Never bypass the wrapper to execute another
root or unverified context.

On failure, diagnose the concrete output, make the smallest coherent fix,
rerun affected gates, commit/push the safe fix, and retry. Stop for secret or
material scope boundaries; do not replace Terraform with ad hoc Azure writes.
Read-only Azure metadata queries are allowed in verified lab context, except
secret/key/token/connection-string retrieval. Ad hoc mutating scripts require
explicit approval of the complete script and exact resource scope.

## Gate 5: Cross-repository application release

Adapt the **lab-owned** release tooling to accept explicit application and lab
roots before invoking it. Test the original root and new root against all
source/package/preflight/WSL paths. Preserve strict host verification, temporary
read-only SSH mount authorization, private evidence outside both repositories,
native Linux build/tests, package allowlists/ELF checks, pinned provenance,
approved ZIP/hash/version/service scope and process/mount cleanup.

Create the package from this repository's code, never from a stale copy in the
lab. Include new modules and declared dependencies intentionally. Produce an
exact hash and sanitized preview mapping the three target services to the
approved project and expected versions. Do not run `azd up`, `azd provision`,
or an unreviewed direct publish shortcut. The copied `.azure` directory is
private context, not release authority.

Pass: all applicable portable and retained release tests pass; package preview
matches the intended source/lock/roles; the exact publication and existing
version use are covered by the user's invocation or a new specific approval.
If the wrapper requires an approval not supplied by that invocation, ask rather
than bypass it. The next-session prompt authorizes synthetic live acceptance
and scoped application publication only within the configured existing project.

A publish timeout is not permission to resend. Inspect the existing operation/
receipt/version and reconcile uncertain sends first. Keep retries bounded.
Record deployed versions and rollback package/versions privately.

For a new diagnostic or corrected release, the lab's `bundle_package.py runtime`
mode creates an exclusive, deterministic allowlisted source archive using explicit
application/lab roots and a private `--output`. It does not read or change an
azd environment or upload code. `Build-BundledCodePackage.ps1 -OutputPackageName`
selects a new basename inside the existing private output directory, preserving
the previous ZIP, seals, receipts and pinned private azd configuration. Use a
new staging directory; verify its exact image, source/archive hashes, package
closure and preview before the retained publisher. Never edit a sealed stage
to turn a failed release into a different package.

Load the exact calibrated `DEMO_FACT_SHEET` with the native settings before
packaging. `scripts\calibrate_routing.py --validate-runtime` is an offline,
read-only gate; retained packaging invokes it before dependency extraction.
Facts are allowlisted, committed into the private settings proof and forwarded
to all roles. Historical ten-field snapshots remain verifiable but do not
authorize a new descriptor requiring facts. Do not recalibrate or rewrite
observations merely to bypass configuration drift.

## Gate 6: Live acceptance and handoff

Use synthetic requirements only and private evidence outside both repositories.
Prove native workflow restart/resume, distinct specialist child sessions,
remote invocation, exact artifact prerequisites/hashes, conditional coordinator
publication, Decision-1 outcomes, private MI Blob access, and isolation between
parents. Verify actual service versions/health and the terminal path. A live
test must not query secrets or use real customer documents.

The retained wrapper supports individual `-AcceptanceScenario` selections.
`followup`, `recover` and `restart` require an existing private parent within
the evidence directory. `recover` retrieves its known pending response only.
`restart` requires `-HostingRestart`; full Acceptance with that switch runs
initial/followup/restart/isolated and checks parent/child continuity and
separation. The supported hosted-compute stop/resume API preserves the session
volume; it does not prove hard-crash recovery. Preserve uncertain stop markers
and pending responses rather than sending either operation again.
Native acceptance validates returned artifact envelopes/hashes, exact reviewer
prerequisites, accepted content, producer sessions/versions and decision records,
not just a success-shaped final message.

Pass: all live acceptance criteria in `design.md` succeed; no pending unknown
operation is concealed; rollback/version/session compatibility is documented.
If unavailable, state exactly which condition failed. Do not label offline
coverage or a successful ZIP upload "deployed and verified."

Never connect to or change the VPN server. If configuration delivery is needed,
provide branch/commit, `cd ~/azure-lab`, pull/diff-review instructions, exact
installation target, expected impact, validation, restart, rollback and secret
handling. Do not read or stage `conf\ipsec.secrets`. A Git push is delivery only;
the VPN-server deployment remains incomplete until the user confirms install
and verification. Such a dependency is a documented stop, not a reason to
claim end-to-end success.
