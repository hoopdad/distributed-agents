# Direct application delivery

**Design -> develop -> deploy -> test case -> remediate -> iterate.**

Work directly on the existing three-agent application. Use the
[mission](requirements/delivery-mission.md) for product acceptance, not a CLI
delivery workflow. No role/reviewer orchestration, planning loops, approval
ceremonies or governance artifacts. Retained delivery tooling and old plans
are inactive history, not prerequisites. The application's MAF workflow remains
part of the product.

Make the smallest coherent implementation change, deploy it with normal
`azd deploy`, exercise a real case, inspect actual application results and fix
the cause. Repeat until the intended flow works or current evidence identifies
a genuine unavailable target, credential or out-of-scope operation. Local
regressions help catch defects before deployment; they are not deployed success.

Use the integrated `feature/azd-demo-delivery` source, preserve unrelated work,
and commit scoped non-secret changes with required trailers; no push.
Normal azd packaging uses `.agentignore`, pinned dependencies and
`scripts\check_azd_source.py`, not legacy ZIP/hash/private approval receipts.
Keep unused lab release tools intact without imposing them on this path.

Use the existing nonproduction project and exactly coordinator, architect and
reviewer. Keep native MAF, genuine Decision-1 semantic routing, remote specialists
and managed-identity Blob context. Test real design, review, revision, follow-up,
recovery and independent-parent isolation. Preserve exact prerequisite refs,
producer/session/version bindings, immutable outputs, coordinator ETags,
checkpoints and actual held/unknown effects. Never replay an uncertain send.

Import verified private configuration through `scripts\Use-Settings.ps1` and
use dedicated lab authentication, not production profiles or copied credentials.
No specific historical filename is required. Do not guess a target or invent
credentials. Existing authority covers application deployment and supported
hosted-session stop/resume, not infrastructure, RBAC, networking, DNS, quota,
VM power, secret retrieval, VPN changes or private lab edits.

Use existing checks as applicable:

```powershell
.\Test-Demo.ps1 -Python <absolute-python-path>
.\scripts\Test-Repository.ps1 -Python <absolute-python-path>
```

Use `-LabRepositoryRoot <explicit-root>` for external wrapper regressions.
Use the isolated pinned environment rather than unrelated global packages.
Do not edit calibration observations, historical hashes, SDK journals or
databases to manufacture a pass. Current observations determine blockers;
unexecuted live checks remain unverified. Report actual product outcomes using
the mission's seven components, not process activity.
