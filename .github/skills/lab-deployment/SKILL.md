---
name: lab-deployment
description: Implement and deploy the authorized three-role application directly with normal azd.
---

Follow the actual user scope and `docs\requirements\delivery-mission.md`.
Design -> develop -> deploy -> test case -> remediate -> iterate.
Do not launch delivery workflows, role/reviewer orchestration, planning loops,
approval ceremonies or governance artifacts. The application's MAF graph
remains part of the product.

Use normal azd deployment for the three existing roles in the existing validated
nonproduction project. `.agentignore`, dependency pins and source/build checks
replace legacy ZIP/hash/private approval receipts on this path. Leave unused
lab release tooling intact. Validate current deployed behavior, not SDK
completion, historical failure reports or offline tests alone.

Load verified configuration through `scripts\Use-Settings.ps1`; use dedicated
authentication and keep private values out of source/logs. Preserve trusted
identity, exact prerequisites, immutable artifacts, checkpoint recovery and
actual unknown-effect holds. No principal substitution or uncertain replay.
No infrastructure/RBAC/network/DNS/quota/VM-power/secret/VPN changes, production
profiles, private lab edits or push. Do not invent target configuration.

Run relevant existing regressions, deploy, exercise real cases, inspect results
and remediate causes. Continue useful independent work around localized issues.
State actual missing scope/credentials or failed criteria precisely; no ritual
reapproval, invented limits or new process gates.
