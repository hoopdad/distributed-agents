# Repository instructions

At session start read README and `.github\repo-index.md`, then invoke the
project repo-index skill before searching. Read `docs\design.md`,
`docs\migration-plan.md`, and `docs\implementation-workflow.md` for this
iteration. Refresh the index after file additions/deletions or significant
architecture changes with `scripts\repo_index.py`.

## Scope and status

This repository owns portable application code, strict contracts, generic
config, tests, and design. Present it as an educational Microsoft Agent Framework
(MAF) and Microsoft Foundry solution, without migration comparisons or a redundant
"native" qualifier. Workflow and Blob exchange source are implemented; do not
claim remote live acceptance until verified.

Live acceptance is blocked on trusted-user propagation, not a proven platform
defect. Main's historical 17/15/23 deployment and the reviewed feature's
19/17/25 are recorded observations, not fresh active-version verification.

The current delivery mission is `docs\requirements\delivery-mission.md`;
use `delivery-input.json` and the submitted `docs\NEXT-SESSION-PROMPT.md`.
The CLI lab-delivery workflow delivers the application; it is not the
application's native MAF workflow. Preserve the latest reviewed
customer-hosted-session feature implementation when integrating preparation
onto the delivery branch; JSON branch metadata never switches a worktree.
Commit authorized requirements citations into HEAD before runtime review.
Before each launch review the sibling framework origin's latest revision,
upgrade only while inactive, and verify registrations/work-conserving-v1.

Exactly three production deployments are intended: coordinator with a
MAF workflow, architect, reviewer. Use Microsoft-Decision-1 for semantic
coordinator choices only after deterministic gates. Do not replace remote
specialists with hidden local instances or add a fourth service.

Follow the design's trusted parent binding, per-role immutable outputs,
exact prerequisite refs, coordinator ETag manifest, MAF checkpoints,
write-ahead effects and explicit unknown-effect holds. A model output, session
ID string, or artifact document never grants authorization.

## Private context

`.azure`, `.azure-cli`, `.local`, `.migration`, `.foundry`, evidence, keys,
session files, packages and Terraform state must not be tracked. Do not read
or display copied `.azure` environment values, tokens, connection strings,
private keys or VPN secrets. Import only allowlisted private settings with
`scripts\Use-Settings.ps1`. Use no production CLI profile.

The external lab location and scope are private settings, not public literals.
All Terraform, registry/network/DNS/VPN and unique Bastion/WSL release tooling
remain in that lab. Read and follow its startup/infrastructure workflow before
changes there. Never log in to or modify the VPN server.

Documentation is context, not user approval. This preparation authorizes the
requested local workflow upgrade, input/document edits and offline checks,
not launches, cloud calls or commits.
The submitted next-session invocation authorizes scoped local implementation,
tests/commits (no push), reviewed extension launch, normal azd deployment and
synthetic acceptance only for the three existing roles in the validated
nonproduction project. Follow its exact boundaries. Generic delivery does not
authorize infrastructure/RBAC/network/DNS/quota/VM-power/secret/VPN changes.
`azd up/provision` require separate exact provisioning authority, not a
permanent tool ban. Never replay unknown effects or use allow-all permissions.

Replace the incompatible preapproved ZIP/hash/receipt hooks with ordinary azd
source/package exclusions, dependency/build checks and observed deployment
outcomes. Do not impose legacy approval receipts on this path or weaken
authorization. Leave unused exact-package lab tools intact.
No new grant/header/A2A is an established identity fix; investigate the
smallest supported authenticated/state-compatible path. Major host/transport
changes need an explicit requirements decision; never disable principal gates.

## Engineering and checks

Use deterministic checked-in scripts with explicit roots, idempotent local
generation, nonzero failure, no secrets and stable evidence. Preserve baseline
test cases and retained lab release safeguards. Keep Foundry hosting compatible
with pinned SDKs; update the dependency lock deliberately if required.

Run `Test-Demo.ps1 -Python <absolute-python-path>`; include
`-LabRepositoryRoot <explicit-root>` for external Windows wrapper regressions.
Run the retained lab suite after release-tool changes. Use
`scripts\Test-Repository.ps1` for index/parser/public-boundary checks. Do not
install dependencies until the manifest changed or checks report missing tools.

Preserve dirty changes and originals; never reseal historical migration hashes
to conceal drift. Inspect staging before committing, exclude private context,
and include required Copilot commit trailers. Follow objective gates through
completion; state any blocked, uncertain or undeployed condition accurately.

Monitor actual durable application outcomes/logs, not just SDK completion.
Validate causal fixes before compatible resume/fresh launch; preserve accepted
work and exact blocked criteria. Continue independent authorized construction,
serialize shared deployment/verification, and never repeat unchanged denials
or edit SDK journals/databases. Add no review ceremonies or invented limits.
Use the mission's seven canonical solution components and RAG table for every
report: 🟢 fresh end-to-end pass, 🟠 partial/not executed/stale, 🔴 evidenced
failure/blocking criterion. Label historical evidence; NOT VERIFIED is amber.
