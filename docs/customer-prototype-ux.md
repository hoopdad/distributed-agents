# Customer hosted-session prototype: user experience

## Boundary and design basis

Designer handoff for the October 19, 2026 User Experience Loop. The customer
wants a hosted coordinator to call remote specialists repeatedly while keeping
each specialist's session within the same parent conversation. This document
defines the terminal and documentation experience, not a browser application.
It supplies the UX design deliverable and reconciles the integrated terminal
and README presentation; live proof remains downstream work. Wireframes below
are illustrative, not execution logs.

The supplied customer specification is the requirements source;
`docs/requirements/{coordinator,specialists,client-release}/architecture.md`
contains derived logical-tier contracts, not replacement requirements. Follow
the accepted
[architecture](customer-prototype-architecture.md), especially its stable
binding/advancing continuation distinction and downstream fixture boundaries.
This revision inspects clean application baseline
`2a736d94cb99c01aca0c516aeaf920e61ddb8fbd` on
`feature/customer-hosted-session-prototype`. Terminal implementation `56b762e`
and README/source integration `24b883f` already exist; they are not new work
credited to this UX revision. Prior disposition
`["yaml-loops-v1:ArchitectureLoop","architecture-loop-status-reconciliation"]`
closes the Architecture Loop only. Retain that accepted handoff without
claiming its reviewer votes apply to this UX artifact.

Neither authorized identity path is live-selected. The architecture's supported
authentication/configuration correction and `x-ms-user-identity` delegation
alternatives have the same customer journey: no identity selector, permission
wizard or caller-ID input is added to the terminal. Required scoped lab
permissions are already authorized; do not ask the customer to approve routine
repair work again. Decision tests may discriminate paths, but formal E2E and
DevOps live gates remain with their original owners. A call ID is never a
delegated user identity. Continue the UX/artifact handoff while selection is
unresolved; do not present either path as a working repair.

## UX principles, tools and framework

1. **Explain the invariant first.** One parent, one architect child and one
   reviewer child per conversation; repeated calls are not repeated creation.
2. **Evidence before reassurance.** Distinguish a retrieved known response,
   a new invocation, a completed specialist output and coordinator acceptance.
   Neither a matching alias nor plausible memory text proves continuation.
3. **Useful work beside continuity.** Show the design and reviewer findings,
   not merely IDs and progress counters.
4. **Truthful failure is a first-class outcome.** Keep holds, missing
   observations and unverified live gates visible. Never turn HTTP success,
   model prose or an SDK-completed response into release PASS.
5. **Private by default.** Share synthetic examples and safe aliases only.
   Full evidence, identifiers, settings and client state stay private.
6. **Progressive disclosure.** Customer summary first, current source path and
   setup next, detailed diagnostics in the existing recovery document.

Use existing Python/argparse/plain-text terminal output, PowerShell setup,
Markdown and fenced ASCII diagrams. Retain MAF, Foundry, strict typed
contracts and existing pins; no Rich/Textual dependency, new protocol,
session manager, service or orchestration framework is needed.
Use ordinary stdout/stderr and unittest fixtures for presentation checks.
The interaction framework is a conversation with a turn-level summary, not a
dashboard requiring a new state store or additional provider calls.

## User journeys and screen direction

| Journey | User action | Visible outcome and boundary |
|---|---|---|
| Understand | Open README | Goal, three-role diagram, two-turn invariant, dated/historical live status, short source path |
| Prepare | Load validated generic settings, authenticate dedicated profile and open retained private transport | Setup prerequisites, not proof of deployment or permission to replace trust |
| Start | New private session file; submit synthetic private-ingress request | Parent identity aliases; architect then reviewer calls; accepted design only after final gates |
| Continue | Reuse that exact file; add asynchronous queue | Same verified parent/children/framework identities and versions; new responses; revised design/review retaining private ingress |
| Revise within a turn | Reviewer blocks candidate | Findings followed by same architect and reviewer bindings with fresh responses; approval only for revised current candidate |
| Recover known work | Use existing recover-only path when a response is persisted | Retrieve the exact known response, explicitly say no resend; do not count retrieval as new invocation |
| Resume compute | DevOps executes existing guarded stop/resume acceptance | Confirmed stop then same bindings/no duplicate effects only when evidenced; not hard-crash recovery |
| Isolate | Use separate private file and synthetic parent | Distinct child bindings/scope, no first-parent requirements; not malicious-host isolation |
| Diagnose | Encounter failure/hold | Fixed diagnostic code, unmet observation and safe next action; no automatic retry/new parent to evade an uncertain effect |

### README first screen

Target approximately 30 lines at ordinary terminal width, without making an
exact viewport size a new release criterion. Put this sequence ahead of
class names, setup detail, historical hashes and diagnostic chronology:

```text
# distributed-agents

A hosted coordinator repeatedly calls a remote architect and reviewer,
preserving each specialist's session within the same parent conversation.

User -> coordinator (MAF workflow)
          -> architect: design/revise
          -> reviewer: review exact candidate
          <- coordinator: validate and accept, or revise again

Turn 1: Design a synthetic private-ingress application.
Turn 2: Add an asynchronous queue; retain private ingress.
Same parent + both child hosted/framework IDs + pinned versions.
New invocation responses and current design/review revisions.
Another parent gets its own children and artifact scope.

Status: historical live execution is blocked before architect application
execution at NATIVE_HOST_PRINCIPAL. Follow-up/recovery/isolation are unverified.
This UX change is not a fresh deployed-version check or a live acceptance result.

Read: workflow begin/route/execute/publish -> foundry child restore/invoke
      -> architect/reviewer history load -> artifact validation/publication.
Next: configure, run the terminal demo, inspect private machine evidence.
```

Link the reading path to `demo/workflow.py`, `demo/foundry.py`,
`demo/architect_agent.py`, `demo/reviewer_agent.py` and
`docs/design.md#following-a-request-through-the-source`. Link status to
`identity-recovery-plan.md` and full design to this document/architecture.
After fresh live verification, replace the notice with measured release status
and its date, not a permanent unsupported claim. Keep known limitations nearby:
unknown historical publication/cleanup remains unresolved, and account-wide
Blob Contributor makes role/parent isolation application-enforced.
Move lengthy existing diagnostic chronology to the existing recovery document,
preserving distinct observations and history rather than deleting evidence.
README readability work was integrated in `24b883f`; preserve it. This revision
does not re-credit those changes or turn their integration into live proof.

### Terminal: implemented opt-in human view

Keep today's default machine-compatible output and existing CLI spellings.
`--native --view human` selects the implemented optional presentation in
`demo/terminal.py` (`HumanView`, `finalize_workflow_turn`); absence preserves
the default. `--view human` without `--native` is rejected by argparse.
Human text goes to stderr after complete records and finalization are evaluated,
not for arbitrary stream fragments; stdout retains
the existing parent header and delegation/result JSON without schema changes.
Do not describe the default stdout as pure JSONL: it already has a parent
header. `live_acceptance.events()` selects JSON lines beginning with `{`.
Never interleave prose inside a JSON record or alter the locator/result parser.
Existing `--native`, `--recover-only` and diagnostic codes retain their spelling.

Illustrative implemented layout using symbolic aliases (not a current live run
or literal 12-character alias values). Every rendered line is prefixed `  | `;
long labels and content wrap to terminal width:

```text
HOSTED COLLABORATION | observed records
Parent hosted alias: P1
Parent framework alias: PF1
Turn 2 | requirements revision 2
1. architect | candidate revision 2
  stable hosted alias: A1
  stable framework alias: AF1
  pinned version: <observed numeric version>
  advancing response alias: A-R2
2. reviewer | candidate revision 2
  stable hosted alias: R1
  stable framework alias: RF1
  pinned version: <observed numeric version>
  advancing response alias: R-R2
Child bindings: observed aliases; exact continuity UNVERIFIED
New child creations / exact response inequality: not observed
Design r2/c2
  <current design text, wrapped; private ingress and queue described>
Review r2/c2: approved
  <current recommendation; blocking/unresolved findings if any>
Coordinator: ACCEPTED_ADVISORY | current result finalized
Model-history / restart / isolation: not established by this display
Release acceptance: separate private report; not certified here
```

Show actual observed versions, not the placeholder above. A label such as
`stable hosted alias` names the identity category, not a verified comparison.
Preserve causal event order, including every repeated architect/reviewer call;
never sort or deduplicate a revision trace into two rows. The controlled offline
sequence is architect -> blocked reviewer -> same architect revision -> same
reviewer, with four fresh response observations and the final current result.
On narrow terminals use one labeled role block per
line instead of clipping identities or requiring horizontal scrolling. Wrap
design/recommendation text; show all blocking and unresolved findings. Long
designs may have an explicitly labeled preview, but must provide a way to
read the full current design without another inference (the retained JSON
result is sufficient). Do not summarize design prose with an extra model call.
Use plain labels such as `VERIFIED`, `UNVERIFIED`, `HELD` and `BLOCKED`;
color is not required or semantic. No ANSI cursor controls, spinner-only
progress or interactive clear-screen behavior. This works with light/dark
terminal defaults, redirection, screen readers and no-color environments.

### Evidence-to-display contract

| Display | Existing source / required comparison | If evidence is absent |
|---|---|---|
| Parent hosted/framework/version | Validated terminal private state, `AgentSession`, session resource/version check; compare previous completed turn in same scope | `UNVERIFIED`; no stable-parent claim |
| Child hosted/framework/version | `WorkflowRuntime.delegation_event()` plus actual manifest child binding and pinned resource checks; compare exact values privately | Show observed aliases only; do not label verified from alias equality |
| New response | Known recorded effect response and parent response; compare exact response IDs within role/scope | `UNVERIFIED`; recovery of same response says `retrieved; no resend` |
| Child creation count | Actual creation records/fixture instrumentation or verified binding inventory, not number of delegation events | `not observed`; never infer zero just because roles repeat |
| Design/review | Current result candidate/review and validated artifact evidence, exact requirements/candidate revisions and producer refs | `unavailable` or `unverified output`; no accepted heading |
| Completion/hold | Result status, pending effect and successful client finalization; preserve nonzero failure behavior | `BLOCKED` for malformed/missing result; partial rows are not success |
| History/restart/isolation | Dedicated continuation/recovery/isolation acceptance evidence | `not established by this display` |

`delegation_event()` already emits aliased hosted/framework/response values,
version, role and artifact ref. These are useful observation labels, not all
the raw evidence needed for exact continuity proof. Preserve the JSON contract.
Where only these events are available, human mode must explicitly remain
unverified for exact child continuity/count; show full verified claims only
when the existing private acceptance/binding checks provide them. If achieving
verified human claims would require a new external read or changed public
contract, return that concrete dependency through Scrum/Architect/PO rather
than inventing proof or adding a parallel evidence ledger.

Reuse the safe `demo/contracts.py` alias convention for observed IDs, label
each identity type, and scope comparisons to the exact parent. The symbolic
P1/A1/R1 labels above are wireframe notation, not fabricated bindings. Do not
persist a second alias/session database or expose full IDs via human mode.
Keep existing explicit `--show-ids` out of customer/shareable demo commands;
do not expand its exposure or print artifact paths, raw logs or credentials.
Render candidate/review content as untrusted plain text: neutralize terminal
escape/control sequences and line-prefix it so generated prose cannot impersonate
status banners. Do not automatically echo arbitrary real customer transcripts.
Synthetic-only guidance is not a general-purpose content redaction guarantee.

### Failure and recovery layout

```text
HELD / BLOCKED: SPECIALIST_INCOMPLETE; turn not finalized; output unaccepted.
Preserve pending state; do not resend uncertain work.
```

The implemented view renders observed calls before this hold notice, omits
accepted design/review output, and preserves the failure/nonzero exit. Missing
or malformed result records instead say
`BLOCKED: result unavailable or invalid; no accepted summary.` A held result
does not imply the historical identity failure. The README/recovery link
provides the retained exact-response diagnosis path; it is not an automatic
terminal retry affordance.

Display only allowlisted observed diagnostic codes. Do not infer the historical
identity failure for every timeout. For missing/malformed output say that exact
condition; for owner/version/scope mismatch stop before another send. For
`request_input`, surface the actual missing requirement without inventing a
human approval stage. An operation hold overrides a visually successful design.
The supported compute-stop action remains in DevOps tooling, not a new terminal
button or automatic recovery action.

## Reproducible demonstration direction

Current runnable command shape from the application root (not executed here):

```powershell
$python = '<absolute-path-to-existing-validated-python>'
$state = '<absolute-private-directory-outside-both-repositories>\harbor.json'
$socks = 'socks5h://127.0.0.1:<owned-port>'
.\scripts\Use-Settings.ps1 -Path .\.local\lab-settings-native.json
& $python -m demo.terminal --native --view human --socks $socks --session-file $state `
  --message 'Design and review a synthetic application with private ingress only.'
# Only after a completed, non-held first turn, reuse the exact same $state:
& $python -m demo.terminal --native --view human --socks $socks --session-file $state `
  --message 'Add an asynchronous queue; retain private ingress and earlier requirements.'
```

Prerequisites: existing pinned environment, validated sole-project settings,
dedicated authenticated lab CLI profile, retained trusted private transport,
and exact reviewed hosted release. Follow the linked lab's retained quickstart
and guarded connectivity tooling; do not copy its private literals here.
Do not reinstall dependencies merely to run this demonstration. No command
above creates infrastructure or authorizes replay. These commands use the
implemented view, but were not executed against hosted agents in this UX turn.
The full acceptance demonstration still uses `live_acceptance.py` through
retained tooling and private evidence; these two commands do not replace G1-G8.

## Downstream acceptance and handoff

Scrum Master owns task IDs, assignments, dependencies and Git reconciliation.
This is a design contract, not a new sprint/review stage. Designer scope ends
with this committed specification and its navigation; original Product Owner
and Critic review the actual commit. Agreement is collected by the existing
loop, not asserted by this document.

| Owner / work | Done when / evidence | Exclusions |
|---|---|---|
| Developer: terminal presentation | Retain integrated opt-in view, default stream and parser; regression coverage for two turns, repeated reject/revise calls, advancing responses, partial/missing/malformed results, holds, recovery no-resend, absent evidence and terminal control sanitization | No claim from fake events is live; no new provider effect for rendering |
| Developer: README clarity | Retain integrated first-screen hierarchy, short source links, setup/two-turn command and truthful status; update measured release notice only after fresh evidence | No stale test counts/deployment metadata as current proof |
| Developer: continuity tests | Architecture's two-role binding/version/create-count/model-history fixtures establish what display may label verified; human text agrees with unchanged machine result | UX fixtures cannot replace AC2/AC3 model/session tests |
| DevOps: customer demonstration | Exact final source/package gates, real synthetic two-turn view and private machine evidence match; status/versions updated only from fresh observations | No mocked acceptance, inferred recovery or mixed-bundle final release |

Verification checklist for implementation review:

- AC6: opening README explains original goal without scrolling through history;
  reader can locate create/reuse, restored session invocation and specialist
  history in the source path above without searching the repository.
- AC1/AC2/AC3: show both roles and useful design/review output; label stable
  identity separately from new response; revision loop repeats bindings, not
  creations; offline cases are visibly offline.
- AC4/AC5: no restart/isolation/provenance claim without its own evidence;
  accepted advisory is not release PASS; pending effects remain held.
- AC7/AC8: run targeted presentation/parser tests, required application and
  repository checks; keep private evidence out of Git; integrate reviewed
  related dirty source deliberately on the authorized feature branch.
- AC9: handoff includes runnable actual syntax, setup, measured sanitized
  comparison, limitations and private exact release/rollback evidence.

## Validation of this UX revision

Using the existing validated absolute Python 3.12.10 executable, without
dependency installation:

- `Test-Demo.ps1 -Python <absolute-validated-python> -LabRepositoryRoot
  <explicit-lab-root>` passed dependency checking, 177 offline tests in
  18.231 seconds, and compilation. These tests include the existing human-view
  and unchanged-machine-stream regressions; rerunning them is not new runtime
  capability.
- `scripts/Test-Repository.ps1 -Python <absolute-validated-python>` passed
  index, focused public-boundary (70 public files), parser and whitespace
  checks.
- Inspected `HumanView.render()`, `finalize_workflow_turn()` and argparse
  wiring against the revised screen and command descriptions.

No runtime or lab source changed. The retained lab release suite and Linux
hosting-package checks were not run for this documentation-only handoff.
Product Owner and Critic agreement on this revision must come from the existing
loop's original reviews; architecture approvals do not supply UX approval.

No deployment, live inference, stop/resume, fresh cloud inventory or identity
remedy is established by this UX work. Full implementation and final AC1-AC9
release acceptance remain with their original downstream owners.
