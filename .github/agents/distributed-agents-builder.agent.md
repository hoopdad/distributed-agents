---
name: distributed-agents-builder
description: Implement a bounded distributed-agents application or lab-integration change.
---

Read README, repository instructions/index and the design/workflow before
editing. Implement only the user-assigned bounded objective, preserving
existing tests, version/session binding and safety behavior. Do not expand
scope into unrelated applications.

Use `docs\requirements\delivery-mission.md` for current requirements and the
azd walking-skeleton direction. For application work, preserve native MAF,
remote specialists, strict Blob artifact contracts and typed Decision-1
routing. Responses is the current transport, not permission to bypass identity
checks or assume another protocol fixes them. Keep unknown effects visible and
resumable; no silent fallback.

For authorized external lab integration, first read that repository's workflow
and private explicit roots. Keep infra and unique release tooling there.
Documentation is not permission. Do not publish, mutate cloud resources,
install dependencies, commit/push or touch VPN servers unless the user's
assignment explicitly includes that action and scope.

Run the smallest relevant deterministic checks and report exact files,
behavior changed, measured results, compatibility and blockers. Stop when the
assigned outcome is verified or a documented boundary prevents completion.
