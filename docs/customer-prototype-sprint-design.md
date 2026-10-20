# RP-S1 sprint design: understandable, evidence-ready continuity

## Assignment and accepted inputs

Sprint **RP-S1** retains evidence-ready source and customer clarity while
establishing the supported identity-selection handoff. This is the Sprint
Design Loop's
`SprintDesign` deliverable: terminal user flows, screen layouts and fixture
handoffs, not a new implementation, SprintPlan or live acceptance report.

Accepted inputs, unchanged by this design:

- [Architecture](customer-prototype-architecture.md), commit `0a244702c7ccf01f1916c4b3a2580346ffb02fea`.
- [User experience](customer-prototype-ux.md), commit `ef5c79d94114f156ab0d03497fafffd1e348aabf`.
- [Release plan](customer-prototype-release-plan.md), commit `5449ff49af6a79dbc9fef75c1314d6689cdba6d3`.

Inspected clean feature-branch baseline `5449ff49af6a79dbc9fef75c1314d6689cdba6d3`
for this October 20 reconciliation.
Related implementation is already integrated in `24b883f`; terminal view
`56b762e`, workflow fixtures `6614440` and specialist fixtures `c454e50` are
retained work, not new progress or tasks to redispatch. The invocation supplies
no new assignments or separate open blocked-backlog list. The known identity
blocker remains in
[the recovery plan](identity-recovery-plan.md); it does not block this bounded
design reconciliation. Neither authorized identity path is live-selected.
Scrum Master reconciles concrete delta assignments and Git ownership; missing
assignments are not a request for user approval.

Apply these prior dispositions only within their originating deliverables:
`["yaml-loops-v1:ArchitectureLoop","architecture-loop-status-reconciliation"]`,
`["yaml-loops-v1:UserExperienceLoop","ux-loop-status-reconciliation"]` and
`["yaml-loops-v1:ReleasePlanLoop","release-plan-loop-status-reconciliation"]`.
Keep those handoffs accepted. They neither supply SprintDesign reviewer votes
nor waive live/package acceptance. No SprintDesign correction feedback was
supplied this turn.

## Sprint slice and navigation

| RP-S1 slice | Concrete design decision | Downstream boundary |
|---|---|---|
| README clarity | Retain integrated opening sequence below; chronology remains in recovery document | Update measured live status only from new evidence |
| Terminal presentation | Implemented `--native --view human`, stderr only after finalization evaluation | Retain default stdout, schemas and acceptance parser |
| Two-turn proof | Initial and follow-up storyboards separate observations from exact comparisons | Developer supplies binding/response assertions; DevOps later supplies live proof |
| Controlled revision | Retain all four ordered calls; current final design/review shown separately | Preserve workflow assertions and renderer capture fixtures |
| Specialist history | Explicitly separate model-history proof from hosted response aliases | Developer tests both real specialist history stages and recovery |
| Identity selection | Selected-A / selected-B / unresolved stays in the bounded engineering handoff, not a terminal selector | Original owners record trusted-ingress evidence or actionable unresolved boundary |

Source reading order for these screens:
[terminal](../demo/terminal.py) -> `WorkflowRuntime.delegation_event()` and
`result()` in [workflow](../demo/workflow.py) ->
[remote restore/invoke](../demo/foundry.py) ->
[architect](../demo/architect_agent.py) /
[reviewer](../demo/reviewer_agent.py) history stages.
The machine acceptance consumer remains
[`live_acceptance.events()`](../live_acceptance.py).
No new web UI, renderer dependency, framework, session database or public
evidence schema is introduced.

## Screen A: README opening and demonstration entry

Use the accepted UX opening hierarchy, with this sprint's reading order:

```text
distributed-agents
A hosted coordinator repeatedly calls remote architect and reviewer agents,
keeping each specialist's session within the same parent conversation.

User -> coordinator (MAF workflow)
          -> architect: design / revise
          -> reviewer: review exact candidate
          <- coordinator: validate, accept or repeat

1. Design a synthetic application with private ingress only.
2. Add an asynchronous queue; keep private ingress and earlier requirements.
Same parent + both child hosted/framework identities + pinned versions.
New invocation responses; current design and review. Separate parent: own children.

Live status: historically blocked at NATIVE_HOST_PRINCIPAL before architect
application execution. Follow-up, recovery and isolation remain unverified.
This source/documentation change is not a deployed-release verification.

Read source: workflow -> remote session restore -> specialist model history.
Run: setup and two-turn terminal example below. Evidence: separate private JSON.
```

This is a wireframe, not a new status observation. Keep the first screen brief;
do not put historical hashes/test totals before the customer goal. Preserve the
long diagnostic history in the recovery document, with links rather than lost
observations. After verified release, update the notice from actual dated
evidence. Keep historical UNKNOWN publication/cleanup and application-enforced
Blob ownership limitations reachable next to that notice.

Use the accepted UX's existing two-command demonstration shape with the same
private session file; follow-up requires a completed, non-held initial turn.
`--native --view human` is implemented; use the README's two commands with the
same private session file, mandatory verified SOCKS endpoint and existing pinned
Python. Omit `--view human` for default output; without `--native` it is rejected.
This is runnable syntax, not a successfully executed live demonstration.
Exact setup and guarded transport remain in existing documentation; no private
lab literals or copied SSH commands here.

## Screen B: turn summary and continuity observations

Human mode is a second presentation of existing records. Without it, preserve
today's output, including the parent header; stdout is not pure JSONL.
With it, stdout remains identical for identical inputs. Stderr gets human
summaries only. Existing `--show-ids` stays out of shareable commands.

The implemented `HumanView.render()` projects the accumulated complete records
once `finalize_workflow_turn()` evaluates finalization. It is not a per-call
streaming progress view; raw machine output retains its existing streaming.
Fragmented chunks are not human events. Preserve chronological order and
repeated calls.
Render accepted output only after normal turn finalization; a pending effect,
schema failure or failed finalization overrides success-looking content.
Do not display `ACCEPTED_ADVISORY` based on partial output.

Illustrative **offline fixture**, not a live transcript. `P1`, `A1`, `AF1`, etc.
are storyboard symbols; implementation uses existing safe aliases and actual
configured versions, not these constants.

```text
HOSTED COLLABORATION | observed records
Parent hosted alias: P1
Parent framework alias: PF1
Turn 1 | requirements revision 1
1. architect | candidate revision 1
  stable hosted alias: A1
  stable framework alias: AF1
  pinned version: <observed numeric version>
  advancing response alias: A-R1
2. reviewer | candidate revision 1
  stable hosted alias: R1
  stable framework alias: RF1
  pinned version: <observed numeric version>
  advancing response alias: R-R1
Child bindings: observed aliases; exact continuity UNVERIFIED
New child creations / exact response inequality: not observed
Design r1/c1
  <private-ingress design from current result>
Review r1/c1: approved
  <current recommendation>
Coordinator: ACCEPTED_ADVISORY | current result finalized
Model-history / restart / isolation: not established by this display
Release acceptance: separate private report; not certified here
```

All actual rendered lines use the `  | ` prefix, including labels; it is
omitted in these wireframes for readability. Offline labeling describes the
fixture/report context, not an automatic runtime mode detector. A label such
as `stable hosted alias` names an identity category, not a comparison result.

Follow-up uses the same layout headed `Turn 2 | requirements revision 2`.
Show current
queue design/review, not the cached first design or old approval. A new response
alias is an observation, not by itself an exact-ID inequality check. Without
exact comparisons, say `follow-up continuity UNVERIFIED` rather than `same child`.
In the private acceptance report, separately compare stable parent, both hosted
and framework child IDs and pinned versions; compare advancing responses, not
entire serialized framework dictionaries.

When exact existing binding checks are available, the separate private report
may state
`bindings VERIFIED` and the instrumented creation count with its evidence scope.
The implemented human view remains unverified; public delegation events alone
do not supply that proof. Do not add a verified badge, external read or new
comparison ledger as an RP-S1 enhancement.
No new external read, public raw identifiers, saved comparison ledger or
provider call is required just to make the display more reassuring.

At narrow widths stack each role's hosted/framework/version/response labels
on separate indented lines. Wrap content to available width without truncating
status or findings; a labeled design preview can refer to the retained full
JSON result without another inference. Use default terminal colors, no ANSI
layout, and explicit status words in both light and dark themes.
Prefix every line of generated content with `  | ` after neutralizing
escape/control sequences, including carriage return/backspace and multiline
status/banner spoofing. This is terminal safety, not a guarantee that arbitrary
customer text is safe to share; the demonstration uses synthetic content only.

## Screen C: reject, revise, review again

The controlled workflow fixture retains this causal trace. This is an
**offline causal storyboard**, not literal human stderr:

```text
Turn 1 | OFFLINE FIXTURE | requirements r1
  1 architect A1/AF1 -> A-R1 | candidate c1
  2 reviewer  R1/RF1 -> R-R1 | BLOCKED c1
    | <all blocking and unresolved findings>
  3 architect A1/AF1 -> A-R2 | revised candidate c2
  4 reviewer  R1/RF1 -> R-R2 | approved c2
Coordinator: ACCEPTED_ADVISORY | exact revised candidate/review
Exact reuse/creation assertions: offline test report, not alias equality
```

Do not collapse calls 1/3 or 2/4 into one latest-only row. Preserve version
labels as in Screen B. Never carry c1 approval or findings forward as c2
approval. Include useful current design/recommendation after the trace.
Binding reuse, exactly two child creations, fresh responses and prerequisite
revisions are fixture assertions, not claims earned by this wireframe.
The implemented human projection lists all four calls and the final c2
design/review; intermediate BLOCKED c1 findings are explained by the controlled
workflow fixture, not fabricated from delegation records that lack them.
Do not require a new public per-call findings schema or replay inference to
reconstruct intermediate content. Retain final blocking/unresolved findings
when actually present in the current result.

## Screen D: held, incomplete and recovered work

| Observed condition | Human output / safe next step |
|---|---|
| Result has pending effect | `HELD`, actual allowlisted status, partial output explicitly unaccepted; preserve state, no resend |
| Missing/malformed/multiple result | `BLOCKED: result unavailable or invalid`; no accepted heading, retain existing nonzero behavior |
| Timeout without captured identity diagnostic | Show timeout/incomplete condition, not an inferred `NATIVE_HOST_PRINCIPAL` |
| Owner/scope/version mismatch | Fixed observed failure code; stop before sending, no switch to a replacement parent |
| Known parent response recovered | `retrieved known response; no resend`; do not count retrieval as a new invocation |
| Actual missing user requirement | Show the existing `request_input` reason as untrusted text; no invented approval stage |

Historical identity information must say **historical** unless actually
observed now. Do not print raw logs, IDs, effect payloads or artifact paths.
For an unknown send, explain that known-response retrieval is available only
if the durable ID exists; do not offer clearing the hold as an escape.
Recovery summaries use the same complete-record handling as normal streaming
and must not double-count the prefix already displayed.
Supported compute stop/resume stays in DevOps tooling, not a new UI command.
RP-S1 designs the recovery message; it does not execute AC4/G6.

## Identity-selection journey: same customer flow, separate engineering evidence

No terminal identity dropdown, caller-ID input, permission wizard or retry
button is added for A versus B. Both supported paths preserve Screens A-D and
the trusted session invariant. Necessary narrowly scoped lab permissions are
already authorized; no routine user approval prompt is designed.

| Engineering outcome | Customer-facing consequence / original handoff |
|---|---|
| `unresolved` | Retain historical status and observed hold; record which A/B boundary remains untested, why, and the closing action privately. Continue remaining artifacts. Do not claim provider-only impossibility from older research. |
| `selected-A` or `selected-B` from bounded scripted discrimination | Record trusted specialist application entry and actual principal-binding compatibility, not HTTP 200 or header presence alone. Selection is not release acceptance; README must not say customer-ready. |
| Principal namespace mismatch or required contract/state migration | Preserve hold and old bindings. Scrum reconciliation with Architect-advised Product Owner handles internal replanning; do not ask for permissions already supplied or weaken equality checks. |
| Published final common bundle and independently verified live gates | Original E2E/DevOps supply dated evidence before updating release status and demonstration proof. Planning does not publish or award cloud-pass. |

Keep exact identities, scoped permission plans/readback and decision evidence
private. Never turn opaque call IDs, model text or assignment JSON into
delegated user identity. Preserve historical UNKNOWN publication, held parents,
rollback bindings and cleanup uncertainty regardless of path choice.

### October 20 sprint delta: decision evidence to customer screens

The accepted architecture now defines a separate specialist-only B client and
a finite, journaled local decision runner. These are RP-S2 implementation
handoffs, not implemented terminal options. Retain the integrated RP-S1 screens
and fixtures. The retained offline handoff (`13203ac`, integrated by `bb1743d`)
returns exit 2 / `unresolved` and has no live mode; that is not an observed
customer-conversation failure. Fresh inventory and executable candidate/runner
work remain downstream. Do not repeat completed research to fill that gap.

Use this ordered interpretation when reviewing affected documentation or the
eventual private decision report. The labels are design examples, not new
public event fields, runtime-generated banners or an additional evidence ledger.

| Decision checkpoint | Safe summary / customer-screen consequence | Closing handoff |
|---|---|---|
| Offline candidate checks only | `OFFLINE ONLY; live selection unresolved`. Leave README historical status and Screens A-D unchanged. | Runtime and runner owners implement accepted contracts independently; inventory remains a separate lane. |
| Candidate deliberately published; fresh trial declared | `CANDIDATE TRIAL; not release acceptance`. A predeclared fresh synthetic parent stays separate from old pinned/held conversations. | Original DevOps binds reviewed source, exact package/three versions and finite intended calls before dispatch. No invented runnable command before the script exists. |
| Trusted architect receiver passes; reviewer not reached | `Architect receiver passed; reviewer unreached; selection unresolved`. Do not display three-role success or a verified two-turn example. | Record exact reached boundary privately. Reviewer runs only after architect trusted entry/receiver success; unknown/held effects stop the sequence. |
| Both receiver checks pass and decision selects A or B | `Identity path selected; customer release unverified`. This does not change alias-based continuity to VERIFIED or change the README to customer-ready. | Formal E2E plus DevOps final-common-bundle/live gates remain required, including genuine current artifact acceptance. |
| Principal missing/changed, version drift, held or unknown effect | Preserve actual failure/hold; no success, automatic path switch, retry or replacement-parent suggestion. | Inspect known exact responses without resend. Contract/namespace changes go through existing Scrum reconciliation and Architect-advised Product Owner, never receiver-equality relaxation. |
| Final release gates independently verified | Update README status from dated evidence; retain historical limitations and provide the real two-turn command/proof. | Original DevOps/E2E supply final/rollback bindings and evidence; documentation review alone does not award release PASS. |

There is no migration screen. A deliberately published candidate's fresh trial
must not reuse a historical held session file, translate principals or adopt
old children. Nor may a failed trial be replaced to evade its hold. Once a final
release is verified, the customer's initial and queue follow-up turns use the
same newly chosen private session file; follow-up still requires a completed,
non-held initial turn. Recovery retrieval never counts as a new invocation.
Show only sanitized classifications in a shareable summary; full principal,
binding, permission readback and evidence locators stay private.

**Affected-change review examples:** a new specialist client must not add a
terminal identity selector or alter default stdout; an architect-only pass must
not become three-role success; `selected-B` must not become continuity VERIFIED;
an unresolved offline exit must not be relabeled live FAIL. These checks use
the existing report and renderer fixtures, with no new provider read or
inference for presentation. Developer owns any concrete implementation repair;
Designer reviews affected screens against this contract. Scrum Master assigns
actual task IDs, dependencies and Git integration; this document creates no
competing SprintPlan or deployment owner.

## Fixture-to-design handoff and doneWhen

The rows below are acceptance examples for existing downstream work, not new
assigned task IDs or an extra approval stage.

| Example / check | Required observable assertion | Handoff |
|---|---|---|
| Initial and queue follow-up | Both roles on both turns; stable actual parent/hosted/framework/version bindings; two total child creations; new responses; updated requirements; stale approval invalidated | Existing workflow regression plus separate human stderr/stdout capture |
| Controlled rejection | Four calls above, same two bindings, fresh responses, exact c2 review inputs; no stale approval | Retained workflow fixture plus renderer's ordered calls/current final output; no invented intermediate findings |
| Both specialist continuations | Restored history passed to each role's actual model stage, fresh-history negative controls, known-response recovery without resend | Specialist tests; display continues to say history not established by itself |
| Evidence absent | Aliases may appear but exact continuity/count remains unverified/not observed | Human renderer tests; no invented evidence fields |
| Fragmented and recovered records | No partial JSON interpreted as success; one final summary; known retrieval not a new invocation | Terminal stream/recovery fixtures |
| Held or malformed result | No accepted banner; existing error/hold semantics and nonzero exits preserved | Existing finalization and failure tests plus presentation assertions |
| Hostile/multiline content and narrow width | No active controls or unprefixed generated banners; findings retained and labels readable without color | Deterministic text fixtures, no model calls |
| Default and opt-in output | Identical stdout bytes for identical records; existing acceptance parser still consumes both; human text only on stderr | Parser/terminal regression comparison |
| README customer path | Goal/diagram/two-turn invariant/status before history, actual source links and runnable implemented syntax | Documentation review and local link checks; preserve integrated README |
| Identity unresolved/selected | No selector or routine permission prompt; selection alone never becomes release PASS | Original scripted decision-test/private report and Scrum handoff, no renderer/schema change |

Scrum Master retains concrete assignments, minimal dependencies, shared-resource
serialization and explicit-path Git reconciliation. Independent terminal,
documentation and offline proof work need not wait for an identity remedy.
Designer owns only this document and navigation; Developer owns implementation
and tests. Original DevOps owns exact-source/Linux/package gates, publication
and live demonstrations. Do not certify AC1-AC5/G1-G8 from fixtures; AC6 is
implemented only when actual README/terminal changes meet this contract.
Required application/repository checks support AC7/AC8; reviewed commits/push
and exact-source final-package certification remain downstream.
AC9 requires the actual command, measured proof, release/rollback bindings,
cleanup and limitations, not this storyboard.

Designer doneWhen: RP-S1 flows/screens and bounded implementation examples are
committed and available to the original Product Owner and Critic. Their
agreement is collected by the existing Sprint Design Loop, not asserted here.
No runtime files, accepted input documents, private state, lab tooling or
pre-existing readability edits are changed by this handoff. New original Product
Owner/Critic SprintDesign agreement is not supplied by earlier-loop approvals.

## Verification of the October 20 sprint delta

Inspected clean application baseline `5449ff49af6a79dbc9fef75c1314d6689cdba6d3`
on `feature/customer-hosted-session-prototype`; changed only this document and
the index. All 10 relative document links resolve, screen fences balance and
`git diff --check` passes. No runtime, dependency, CLI or evidence-schema
changes were made.

Attempts to run `Test-Demo.ps1` with explicit lab root and
`scripts/Test-Repository.ps1`, using the previously recorded absolute
Python 3.12-x64 executable, were denied by the execution tool because no
interactive approval response was available. Neither command ran; current
dependency, full offline-suite, generated-index and public-boundary success
are not claimed. The historical results below do not cover this revision.
Run these retained checks when tool execution is available; no dependency
installation or broader Azure authority is requested.

The Designer agrees with this bounded screen/handoff design. Original Product
Owner and Critic agreement on this revision remains outstanding. No cloud
inventory, permission operation, candidate trial, deployment, live acceptance,
Linux package gate or push occurred; no lab source was changed.

## Historical verification of the preceding sprint-design revision

Using the existing absolute validated Python 3.12.10 executable, without
dependency installation:

- `Test-Demo.ps1 -Python <absolute-validated-python> -LabRepositoryRoot
  <explicit-lab-root>` passed dependency checks, 177 offline tests in
  23.401 seconds and compilation.
- `scripts/Test-Repository.ps1 -Python <absolute-validated-python>` passed
  index, focused public-boundary (70 public files), parser and whitespace gates.
- All 10 local document links resolve; screen fences and A/B/unresolved
  handoff labels checked. Inspected `HumanView.render()` and
  `finalize_workflow_turn()` plus terminal capture fixtures against the layouts.

These repeated checks validate retained source and this documentation; they
are not newly implemented capability or live proof. No lab source, runtime,
dependency or machine contract changed. No fresh cloud inventory, identity
discrimination, permission change, live inference, deployment, stop/resume,
Linux hosting-package validation or retained lab release-suite execution was
performed. Final exact-source/package and live gates remain with their original
owners; historical unknown effects and held parents remain untouched.
