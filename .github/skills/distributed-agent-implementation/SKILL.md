---
name: distributed-agent-implementation
description: Implement native MAF orchestration, remote Foundry specialists and typed shared artifacts.
---

Use for this application's native workflow, Blob artifacts, Decision-1 routing,
session recovery or cross-instance correctness changes. Read repository
instructions and `docs\design.md` plus `docs\implementation-workflow.md`.

Establish the missing acceptance criterion and bounded change first. Preserve
the three-deployment design, strict schema/revision/provenance validation,
trusted parent scope, role-owned immutable outputs and coordinator-only ETag
publication. Native checkpoints do not replace the write-ahead effect journal.
Verify hosting/provider APIs against pins; never improvise a wire contract.

Add focused tests that fail without the change, including affected crash/
uncertainty edges. Run the targeted cases and complete application suite as
appropriate. Refresh the index and documentation to actual behavior.
Do not deploy unless explicitly authorized; follow lab-deployment for that.
