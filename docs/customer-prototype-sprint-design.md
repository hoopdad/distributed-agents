# RP-S1 sprint design: understandable, evidence-ready continuity

## Assignment and accepted inputs

Sprint **RP-S1: Evidence-ready source and understandable continuity** makes
offline proof and customer clarity implementable while supported-remedy
assessment proceeds independently. This is the Sprint Design Loop's
`SprintDesign` deliverable: terminal user flows, screen layouts and fixture
handoffs, not an implementation, SprintPlan or live acceptance report.

Accepted inputs, unchanged by this design:

- [Architecture](customer-prototype-architecture.md), commit `1f690f5011bef61494b8181fd14e779fa55d858e`.
- [User experience](customer-prototype-ux.md), commit `0f2a2b22a23fdb614e666274eec29c612da0a92f`.
- [Release plan](customer-prototype-release-plan.md), commit `a2d0f9a06bfa9fd6df7fd932c94491eccb87035d`.

No open blocked-backlog list, assigned task IDs, prior dispositions or reconciled
feedback were supplied. The known identity blocker remains in
[the recovery plan](identity-recovery-plan.md); it does not block this bounded
offline design. Do not invent a new remedy, reopen the accepted UX, or treat
missing task assignments as a request for user approval. Scrum Master supplies
task decomposition and Git reconciliation next.

## Sprint slice and navigation

| RP-S1 slice | Concrete design decision | Downstream boundary |
|---|---|---|
| README clarity | Opening sequence below; detailed chronology remains in the existing recovery document | Developer integrates related dirty README work deliberately |
| Terminal presentation | Proposed `--view human`, stderr only; render completed records, not arbitrary stream chunks | Developer preserves existing default stdout and CLI compatibility |
| Two-turn proof | Initial and follow-up storyboards separate observations from exact comparisons | Developer supplies binding/response assertions; DevOps later supplies live proof |
| Controlled revision | Show all four causal calls in order, not a deduplicated two-role list | Developer drives the real workflow with controlled offline adapters |
| Specialist history | Explicitly separate model-history proof from hosted response aliases | Developer tests both real specialist history stages and recovery |
| Supported-remedy assessment | Hold and exact missing observation are visible; no automatic repair/retry affordance | Original research/runtime owner records a supported correction or negative finding |

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
`--view human` is still **proposed, not implemented**; do not present it as
runnable until the Developer adds it. Exact setup and guarded transport remain
in existing documentation; no private lab literals or copied SSH commands here.

## Screen B: turn summary and continuity observations

Human mode is a second presentation of existing records. Without it, preserve
today's output, including the parent header; stdout is not pure JSONL.
With it, stdout remains identical for identical inputs. Stderr gets human
summaries only. Existing `--show-ids` stays out of shareable commands.

Render a delegation row only after its complete JSON record parses; fragmented
chunks are not events. Preserve chronological order and repeated calls.
Commit the final summary after normal turn finalization; a pending effect,
schema failure or failed finalization overrides success-looking content.
Do not display `ACCEPTED_ADVISORY` based on partial output.

Illustrative **offline fixture**, not a live transcript. `P1`, `A1`, `AF1`, etc.
are storyboard symbols; implementation uses existing safe aliases and actual
configured versions, not these constants.

```text
HOSTED COLLABORATION | OFFLINE FIXTURE
Turn 1 | parent P1 | requirements r1
  1 architect | hosted A1 | framework AF1 | version <observed> | response A-R1
  2 reviewer  | hosted R1 | framework RF1 | version <observed> | response R-R1
Child bindings: observed aliases; exact continuity UNVERIFIED
New child creations: not observed
Design r1/c1
  | <private-ingress design from current result>
Review r1/c1: approved
  | <current recommendation>
Coordinator: ACCEPTED_ADVISORY | current result finalized
Model-history / restart / isolation: not established by this display
Release acceptance: separate private report; not certified here
```

Follow-up uses the same layout headed `Turn 2 | requirements r2`. Show current
queue design/review, not the cached first design or old approval. A new response
alias is an observation, not by itself an exact-ID inequality check. Without
exact comparisons, say `follow-up continuity UNVERIFIED` rather than `same child`.
In the private acceptance report, separately compare stable parent, both hosted
and framework child IDs and pinned versions; compare advancing responses, not
entire serialized framework dictionaries.

When exact existing binding checks are available, the report may state
`bindings VERIFIED` and the instrumented creation count with its evidence scope.
The current public delegation events alone do not supply that proof.
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

The controlled fixture must yield this causal trace, visibly labeled offline:

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

## Fixture-to-design handoff and doneWhen

The rows below are acceptance examples for existing downstream work, not new
assigned task IDs or an extra approval stage.

| Example / check | Required observable assertion | Handoff |
|---|---|---|
| Initial and queue follow-up | Both roles on both turns; stable actual parent/hosted/framework/version bindings; two total child creations; new responses; updated requirements; stale approval invalidated | Existing workflow regression plus separate human stderr/stdout capture |
| Controlled rejection | Four calls above, same two bindings, fresh responses, exact c2 review inputs; no stale approval | Real workflow fixture; compare event order with rendered trace |
| Both specialist continuations | Restored history passed to each role's actual model stage, fresh-history negative controls, known-response recovery without resend | Specialist tests; display continues to say history not established by itself |
| Evidence absent | Aliases may appear but exact continuity/count remains unverified/not observed | Human renderer tests; no invented evidence fields |
| Fragmented and recovered records | No partial JSON interpreted as success; one final summary; known retrieval not a new invocation | Terminal stream/recovery fixtures |
| Held or malformed result | No accepted banner; existing error/hold semantics and nonzero exits preserved | Existing finalization and failure tests plus presentation assertions |
| Hostile/multiline content and narrow width | No active controls or unprefixed generated banners; findings retained and labels readable without color | Deterministic text fixtures, no model calls |
| Default and opt-in output | Identical stdout bytes for identical records; existing acceptance parser still consumes both; human text only on stderr | Parser/terminal regression comparison |
| README customer path | Goal/diagram/two-turn invariant/status before history, actual source links and runnable implemented syntax | Documentation review and local link checks |

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
pre-existing readability edits are changed by this handoff.
