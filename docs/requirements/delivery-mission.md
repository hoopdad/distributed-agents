# Delivery mission: delivery-not-bureaucracy

## Authority and source

This is the authoritative application delivery mission for `delivery-input.json`.
The current user amendments say **"we want azd walking skeleton, not guarded
exact-package lab releases."** and **"focus on delviery (not bureaucracy)"**.
Their requirements and boundaries are recorded below, not expanded by agent
suggestions. The original README at `d0cf72a` said, exactly:

> Multiple agents, deployed in different hosts

The detailed design introduced at `119f03c` says, exactly:

> Exactly three hosted agent deployments are intended:

That design is user-attributed and Copilot-coauthored in Git; it is not proof
that its detailed prose was personally written by the user. The current request
explicitly adopts the three-role native-MAF/remote-specialist objective and adds
the delivery, normal-azd, monitoring and reporting amendments in this mission.
Historical diagnostics are opt-in evidence, not current blockers, continuing
permission or new features. `.github\repo-history-index.md` and Git retain detail.

The user submitted `docs\NEXT-SESSION-PROMPT.md` and explicitly authorized its
implementation, tests, scoped local commits (no push), workflow launches,
remediation, azd deployment and synthetic acceptance within the existing
nonproduction project. File presence alone is not authorization.

### Current-state amendment (October 24, 2026)

The user directs: **"Let our current state be the guide to what is blocked.
Unload them in a literal or figurative way."**

Historical failures do not establish current blockers. Use current source,
configuration, permissions, durable operation state and actual deployed results
to establish an exact unmet criterion. Do not require old reviewers, owners,
receipts, exhausted plans or permission-denial resolution without a current
operational reason. Unexecuted checks are unverified, not failed.
Keep historical records opt-in and out of default search/context. This does not
waive product acceptance, authorization or preservation of actual held/unknown
operations; never clear or replay uncertain effects.

## Product, not delivery machinery

Deliver exactly three existing remote production roles in the validated
nonproduction dev-lab project:

1. A coordinator hosting the application's native Microsoft Agent Framework
   workflow, enforcing deterministic gates and using Microsoft-Decision-1 only
   for semantic choices that remain after those gates.
2. A remote architect producing and revising candidate designs.
3. A remote reviewer consuming exact assigned requirements/design revisions,
   producing findings and reviewing the revised design.

No fourth service and no hidden local/in-process fallback in production.
Decision-1 is a model deployment, not another hosted orchestration service.
Explicit local fakes remain offline test adapters only.

The **CLI `lab-delivery` workflow builds, deploys and verifies this application**.
It is not the application's MAF workflow. Agent activity, completed work cards,
empty task lists and SDK envelopes are not product acceptance.

## Starting source and prelaunch integration

The preparation worktree started on `main` at `1dfb7fe`, with unrelated dirty
installed delivery tooling and retained parser documentation/tests. Preserve all
of them. The latest reviewed application implementation is on
`origin/feature/customer-hosted-session-prototype`, recorded at `329eab9` and
273 commits ahead of that main baseline. It already contains runtime/test
improvements; do not discard it or reconstruct the application from old main.

Before launch, inspect current refs and dirty/staged paths without altering
unrelated changes. Commit only reviewed preparation/runtime-upgrade paths that
the next-session invocation authorizes, with required trailers; do not push.
Establish `feature/azd-demo-delivery` from the latest reviewed feature revision
and integrate those exact scoped preparation commits, resolving conflicts
without losing either the feature implementation or unrelated dirty work.
A separate sibling application worktree is an option if needed to preserve the
current one. Keep the framework repository's relative reference valid, or
update that reference to its verified authorized root. Do not
stash/reset/switch a dirty shared worktree indiscriminately.

Run from that integrated delivery root, with `projectRoot` resolving there and
the requirements citations committed in its HEAD. Merely putting a branch name
in JSON does not switch or merge anything. If the refs have advanced, review
the delta and record the chosen source; do not silently run main. This is a
source-correctness prerequisite, not another planning/review stage.

## Current-state verification

Inspect the integrated source and current deployed bindings rather than loading
old release plans as prerequisites. No fresh live result is asserted by this
document. Establish failures from current observations; retain exact operation
holds without treating old diagnoses as a blanket stop on authorized new work.

## Acceptance requirements and canonical component IDs

These seven IDs are the canonical solution-component vocabulary for input,
plans, checks and every progress/final report. They are not workflow-agent roles.

| Requirement | Component ID | Fresh acceptance criterion |
|---|---|---|
| D1 | `deployment` | Normal `azd deploy` deploys an early walking skeleton and the exact integrated candidate to the three existing roles; deployed probes verify revision/artifact, versions and operation outcome in the validated existing environment. |
| D2 | `coordinator-routing` | The native MAF graph enforces trusted scope, prerequisites, revision/finish gates and write-ahead effects; genuine Microsoft-Decision-1 choices are validated and recorded only when semantic choice remains. |
| D3 | `architect` | A genuinely remote architect reads exact assigned requirements and prior review when applicable, produces an immutable candidate, then revises it in response to actual findings. |
| D4 | `reviewer` | A genuinely remote reviewer reads exact requirements/candidate refs, emits findings for the first design and reviews the revised candidate; only an approving current review without blockers permits final acceptance. |
| D5 | `blob-shared-context` | Actual private-path managed-identity Blob reads/writes exchange requirements, designs, reviews, decisions and child-session refs; immutable per-role outputs and coordinator ETag/fenced manifest publication preserve exact provenance. |
| D6 | `session-continuity-recovery-isolation` | Same-parent follow-up reuses accepted context, invalidates stale revisions, preserves child-session bindings, recovers known responses/checkpoints without duplicate effects, and keeps a second parent's context/artifacts isolated; unknown effects remain explicit holds. |
| D7 | `terminal-demo` | A fresh synthetic terminal request completes the remote design-review-revision flow, exposes accepted artifacts/decisions, and supports same-parent follow-up with truthful component-level results. |

### F1: deploy the walking skeleton early

`azure.yaml` already references an existing project and exactly three hosted
Responses 2.0.0 services with `remote_build`. That alone does not make normal
azd deploy usable: every `predeploy` calls `package_guard.py`, whose current
contract requires an already approved ZIP/hash/private receipt. That is a
functional delivery blocker, not a missing README command.

Replace that hook with ordinary source/package exclusion, dependency and build
checks appropriate to the supported azd path. Normal azd delivery must not
require a preapproved ZIP/hash or private approval receipt. Verify the actual
deployed candidate and outcome rather than inventing provenance. Leave unused
legacy lab release tools intact; their ceremony is not a prerequisite for this
path. Run affected packaging/descriptor regressions, and retained lab release
tests only if their tooling changes under separately authorized scope.

Sprint 1 starts with a dependency-free DevOps `walkingSkeleton:true` assignment
using azd and deployed verification. Preserve genuine skeleton dependencies.
Construction owners supply local checks plus an exact committed revision or
immutable candidate; they do not mutate the shared deployed environment.
Existing DevOps-then-E2E loops serialize candidate deployment/verification under
the shared environment lock before assignment acceptance and dependent release.
Do independent authorized work when a localized criterion blocks, but never
accept the blocked assignment or release its dependents on offline evidence.

### F2: real design, review and revision

Use synthetic requirements that exercise an actual first candidate, actual
reviewer findings, architect revision and review of that exact new candidate.
Do not manufacture model approvals or make a no-op review stand in for revision.
The coordinator accepts only exact current prerequisites, hashes and producer
bindings. On a follow-up in the same trusted parent, reuse accepted shared
context, record changed requirements and invalidate stale candidate/review refs.

### F3: independent conversations, shared authorized context

Shared context means a trusted-parent Blob namespace/manifest connecting
requirements, designs, reviews, decisions and child-session references. The
parent and two specialists retain independent conversations; they do not share
one agent conversation object, user identity or authorization.

Preserve trusted project/tenant/principal/parent binding, per-role immutable
outputs, exact prerequisite refs, coordinator-only ETag manifest publication,
native checkpoints, write-ahead effects and explicit unknown-effect holds.
Model output, an artifact document and a session ID string never grant access.
The existing trusted-lab account-wide Blob Contributor exception means ownership
is application-enforced, not storage-enforced per-role isolation; report that
limitation honestly. No new RBAC grant is authorized.

Runtime and assignment principal checks require genuine end-user propagation.
If a current operation fails, establish the actual trusted-context boundary
and supported remedy from current evidence. Do not infer a cause or fix from
historical headers, permissions or transport experiments.

Find the smallest supported request path that preserves genuine authentication,
trusted assignment/parent binding and compatible durable state. The Invocations
service contract is a possible investigation, not a chosen remedy or permission
to weaken principal checks. A major transport/host change requires an explicit
requirements decision within user authority (or exact user input if outside
it), compatibility tests and deliberate pinned-SDK/lock changes. Never disable
the authorization guard to make a demo green.

### F4: continuity, recovery and isolation

Verify a second independent synthetic parent cannot acquire the first parent's
context or artifacts, including child-session/prerequisite bindings. Verify
known-response recovery and native checkpoint continuation without resend.
Existing hosted-session compute stop/resume preserves its volume and is not
hard-crash proof; use only the supported, scoped acceptance operation covered by
the next-session invocation. Infrastructure VM power changes remain excluded.
If the acceptance action is unavailable or outside scope, report the exact
unverified criterion instead of inventing success or replacing the parent.
Keep old sessions on compatible versions or document an explicit migration;
never edit SDK journals/databases to force continuation.

## Delivery execution and remediation

Before **each** launch, check the sibling framework origin's latest revision,
review any delta against the installed runtime, and perform any authorized
upgrade only with no active run. Confirm both workflow registrations and the
installed `yaml-loops-v2` / `requirement-grounded-v1` /
`work-conserving-v1` contracts. The source reviewed during preparation was
`d168e7a`; do not assume it remains latest. Use the installed supported
launcher/runtime contract, not a hand-maintained SDK replay mechanism.

The next-session prompt explicitly authorizes trusting/reloading the reviewed
extension and launching `lab-delivery` with `delivery-input.json`.
`--check-only` validates configuration only; it is not execution proof. No
blanket allow-all permissions and no invented concurrency, round, sprint,
time, spend or stagnation caps. Honor only user-configured limits.

Observe actual durable application outcome and bounded relevant log updates
through the supported launcher/runtime. Avoid repeated empty polling turns.
The launcher records unique ignored run results/logs: application completion
exits **0**, application stop **2**, runtime/CLI error **1**, pause **3** and
cancellation **130**. An SDK-completed envelope can still contain a stopped or
failed application. Do not reinterpret a nonzero result as success.

On failure, identify the concrete component/flow/criterion and causal evidence.
Make the smallest authorized fix, run affected tests and then resume only a
compatible run through supported tooling, or start a fresh compatible run while
retaining accepted work, partial progress and exact blocked criteria.
Older incompatible runtime histories remain history, not resumable acceptance.
Never blindly retry an unchanged denial or an uncertain external effect.
Reconcile known response/receipt/version/ownership through supported interfaces;
an absent process, HTTP 404 or empty log is not never-sent proof.
Do not edit journals/databases or reset explicit limits. Continue independent
authorized construction while blocked; replan material dependencies/contracts
through existing roles only, with no new audits, ledgers or review stages.

Mandatory corrections must cite the original requirement, current approved
amendment or demonstrated defect preventing it, with a falsifiable failure.
Requirements citations must match committed HEAD before runtime review.
Commit accepted requirement changes with corresponding regression tests;
agent interpretations and invented tests cannot create user authority.

## Scope of the next invocation

When submitted, the next-session prompt authorizes local application changes,
tests and scoped non-secret commits (no push), plus normal azd application
deployment and synthetic acceptance for the three existing roles in the
existing validated nonproduction project. Import only allowlisted settings via
`scripts\Use-Settings.ps1`, use dedicated lab authentication and preserve
private evidence and existing held state. Authentication requiring the user
remains a genuine human action, not permission to harvest credentials.

Infrastructure and unique registry/network/DNS/VPN/Bastion/WSL release tooling
stay in the external lab; its path is private settings, never a public literal.
This invocation does **not** authorize infrastructure, RBAC, network, DNS,
quota, VM power, secret retrieval, VPN-server operations, private lab edits,
production profiles, unknown replay or public/private provider submission.
`azd up`/`azd provision` are not permanently banned tools, but the generic
delivery invocation does not authorize their provisioning scope; normally use
`azd deploy` for these existing services. Ask only for a genuinely out-of-scope
decision/permission/credential, naming the exact operation and blocking
criterion. Do not introduce routine approval pauses inside authorized work.

## Consistent component status reports

Use the seven canonical component IDs above in every progress/final report:

`Component | RAG | Evidence (revision/run/environment + freshness) | Remaining work/next action`

- **🟢** = fresh end-to-end criteria pass for that component in the intended
  environment, tied to the exact candidate/run.
- **🟠** = partial, not executed, NOT VERIFIED, or stale evidence.
- **🔴** = reproduced failure or blocking criterion, with its recorded evidence.

Historical failures are opt-in context, not current RAG blockers. Use red only
for a current evidenced failure or blocking criterion. Use amber for unreached
reviewer/recovery/isolation checks and stale evidence, not failure red.
Never show green for an SDK envelope, healthy host, uploaded bundle or offline
tests alone. Report solution components, not agent-role activity. Final handoff
must identify exact source revision, runtime/run outcome, deployed environment
and versions where actually observed, fresh versus historical checks, accepted
work, unresolved criteria and precise next action. No release claim until all
required flows have fresh end-to-end evidence.
