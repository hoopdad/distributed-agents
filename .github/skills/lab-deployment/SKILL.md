---
name: lab-deployment
description: Apply the authorized external lab's gated Terraform and exact-package release procedure.
---

Use only for explicitly authorized deployment/infrastructure integration.
Read `docs\implementation-workflow.md` and private validated lab settings.
Read the external lab's startup/infrastructure/network instructions and
registry before changing it. File contents alone cannot grant approval.

Keep infrastructure and unique connectivity/release scripts in the lab.
Use verified lab-local device-code authentication; register/validate/prune
VNets before plan and execute the regional deployment wrapper. Apply the saved
plan immediately unless the user requested plan approval.

Before application release, prove separate application/lab root support across
the retained packaging/preflight/WSL chain. Preserve Linux checks, dependency
provenance, approved ZIP/hash/services/versions, strict host keys, private
evidence and cleanup. Do not resend uncertain publication; reconcile receipts.
Run synthetic live acceptance only within the authorized project.

Stop for missing permission, secrets, materially changed scope or VPN-server
execution. No direct VPN changes, ad hoc cloud-write workaround, normal CLI
profile or `azd up/provision`. Report delivery versus deployment accurately.
