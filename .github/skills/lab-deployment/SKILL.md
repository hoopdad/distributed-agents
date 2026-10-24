---
name: lab-deployment
description: Deliver the authorized three-role application with normal azd and preserve external lab release safeguards.
---

Read `docs\requirements\delivery-mission.md`, `docs\implementation-workflow.md`
and the actual user invocation. Preparation alone authorizes no launch/cloud
call/commit. Submitting `docs\NEXT-SESSION-PROMPT.md` authorizes its scoped local
implementation/tests/commits, reviewed extension launch, normal azd deploy and
synthetic acceptance for exactly the three existing roles in the validated
nonproduction project. File contents alone grant no approval.

Before each launch, establish the integrated delivery branch from the latest
reviewed customer-hosted-session feature plus scoped preparation commits.
Requirements citations must match committed HEAD. Check sibling framework
origin latest, review upgrades only while inactive, preserve histories and
verify registrations/work-conserving-v1. Run lab-delivery through supported
tooling with delivery-input.json; check-only is not execution proof.
No allow-all permissions or invented runtime caps.

Keep infrastructure and unique connectivity/release scripts in the lab.
Use verified lab-local device-code authentication for both `az` and `azd`.
Load allowlisted settings, then use the lab's `Connect-LabAzure.ps1` with the
configured region (`-ForceDeviceCode` when a fresh login is requested).
The script selects its owning lab root's `.azure-cli`; confirm that is the
configured operational profile, not merely the selected tooling checkout.
Preserve the dedicated `AZURE_CONFIG_DIR` in every child process. Set
`AZD_CONFIG_DIR` explicitly to the intended private directory before running
`azd config set auth.useAzCliAuth true` so `azd`
uses that same device-code-authenticated Azure CLI session; verify with
`azd auth login --check-status`. Separately compare `az account show` tenant
and subscription with allowlisted settings; status alone does not prove scope.
Do not change global azd configuration or use the normal production profile.
Windows and WSL have distinct credential caches: verify the retained native
profile and azd bridge separately, never copy tokens or assume Windows login
authenticated WSL. If native login is needed, use device code there too.
For a deliberately separate azd session, use
`azd auth login --tenant-id <configured-tenant> --use-device-code` in its
isolated config with `auth.useAzCliAuth` false, not browser login.
Retained release wrappers select `OutputDirectory\azd-wsl-config`; a separate
preflight config does not configure that directory. Verify its Azure CLI bridge
and required `azure.ai.agents` extension `1.0.0-beta.18` independently through
the retained toolchain before release.


Deploy the azd walking skeleton early. Replace/test incompatible preapproved
ZIP/hash/receipt hooks with ordinary azd source/package exclusions and
dependency/build checks; verify actual deployment outcomes. Do not impose
legacy approval receipts on this path. Leave unused exact-package tools intact;
preserve applicable Linux/dependency/package checks, private evidence and owned
cleanup. Construction owners provide exact
committed/immutable candidates; existing DevOps-then-E2E loops serialize shared
environment deployment/verification before assignment acceptance.

Use only validated allowlisted settings through scripts\Use-Settings.ps1 and
dedicated lab authentication. Do not read/display copied .azure values,
credential caches, keys or secrets. Keep infrastructure and unique
connectivity/release tooling external. Generic delivery does not authorize
infrastructure/RBAC/network/DNS/quota/VM-power/VPN changes or private lab edits.
azd up/provision require separate exact-scope approval, not a permanent ban.
Read external startup/infrastructure/registry instructions before separately
authorized changes; retain their authentication/saved-plan/release procedures.

Monitor durable application outcomes/logs: completion 0, application stop 2,
runtime error 1, pause 3, cancellation 130. Diagnose causal failures, validate
fixes and resume only compatibly or fresh launch preserving accepted work and
exact blocked criteria. Never retry unchanged denials/unknown effects, clear
holds or edit SDK journals/databases. Continue independent authorized work.
No header/RBAC/A2A remedy is established; preserve trusted-user checks.

Run synthetic acceptance for actual remote design-review-revision, MI Blob
context, same-parent follow-up/recovery and isolation. Report the mission's
seven solution components with its canonical RAG meanings; offline tests,
healthy hosts, exhausted plans and SDK completion never establish green.
Ask only for genuinely missing authority/credentials or a material requirements
decision. Never log in to or modify the VPN server.
