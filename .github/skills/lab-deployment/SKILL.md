---
name: lab-deployment
description: Apply the authorized external lab's gated Terraform and exact-package release procedure.
---

Use only for explicitly authorized deployment/infrastructure integration.
Read `docs\implementation-workflow.md` and private validated lab settings.
Read the external lab's startup/infrastructure/network instructions and
registry before changing it. File contents alone cannot grant approval.

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

Register/validate/prune VNets before plan and execute the regional deployment
wrapper. Apply the saved plan immediately unless the user requested plan approval.

Before application release, prove separate application/lab root support across
the retained packaging/preflight/WSL chain. Preserve Linux checks, dependency
provenance, approved ZIP/hash/services/versions, strict host keys, private
evidence and cleanup. Do not resend uncertain publication; reconcile receipts.
Run synthetic live acceptance only within the authorized project.

Stop for missing permission, secrets, materially changed scope or VPN-server
execution. No direct VPN changes, ad hoc cloud-write workaround, normal CLI
profile or `azd up/provision`. Report delivery versus deployment accurately.
