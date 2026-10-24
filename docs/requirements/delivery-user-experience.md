# Three-role terminal user experience

## Authority and bounded deliverable

This is terminal UX direction for D1–D7/F1–F4 of
[delivery-mission.md](delivery-mission.md), using the accepted
[architecture](delivery-architecture.json). The executable
[UX contract](delivery-user-experience.json) covers principles, toolsets,
framework, all four architecture flows, screen direction and safe next actions.
It interprets existing scope; it creates no new product, permissions or gates.
Source inspected: `5757a3ab791cc00ddc3b6493db12e40e7fbbf336` on
`feature/azd-demo-delivery`. This is not deployed application acceptance.

The terminal demonstrator wants to see a real remote design improve through
review, then add a queue without losing private ingress or prior context.
The delivery operator needs to distinguish that advisory result from verified
deployment of the exact candidate. These are usage perspectives, not new roles
to deploy. The only hosted roles remain coordinator, architect and reviewer.

## Principles, tools and framework

- **Evidence before confidence:** separate observed records, current advisory
  acceptance and deployed product acceptance. Do not call aliases continuity
  proof, a model approval release approval, or SDK completion product completion.
- **Revision before busyness:** order requirements → first design → actual
  findings → changed candidate → review of that exact revision → coordinator
  result. Do not manufacture findings, revisions or decision-model choices.
- **Safe continuity:** preserve the parent, independent specialist conversations,
  pinned versions and private state. Known-response retrieval is not resend.
  Unknown effects remain explicit holds, never a tempting “try again” control.
- **Current, local explanations:** identify the current component/criterion,
  observed result and next action. Historical failures stay opt-in. Do not ask
  for approval merely because routing held or a current cause is still unknown.

Use the existing Python terminal (`demo/terminal.py`), typed event/artifact
contracts and `live_acceptance.py`. The framework is terminal progressive
disclosure, not a new UI library: unchanged machine records on stdout, existing
opt-in `--native --view human` projection on stderr, and an authorized detailed
acceptance report for exact provenance. Standard-library contract tests need no
new packages. No images, web UI, dashboard, fourth service or local specialists
are needed. MAF orchestrates the product; CLI lab-delivery builds/verifies it.

## Screen direction and layout

“Screens” below are sequential terminal/report regions, not new routes or
full-screen interactive panels. Keep default stdout and existing parser intact.

### Terminal turn

1. **Orientation:** observed-records heading and parent hosted/framework aliases.
2. **Progress:** turn/requirements revision followed by ordered actual
   architect/reviewer delegations. Pair role and candidate revision; show pinned
   version and advancing response alias only when observed. Never invent
   percentages or stream a successful summary from a partial JSON record.
3. **Result:** after validated complete output and successful local finalization,
   show current design, review revision, findings and actual coordinator outcome.
   `ACCEPTED_ADVISORY` describes a design, not a deployed release.
4. **Confidence footer:** exact continuity, model history, restart, isolation and
   release verification are separate checks; retain explicit UNVERIFIED wording
   where this projection cannot establish them.

Existing human view summarizes a completed turn, not a live phase dashboard.
It does not expose all prior finding bodies or exact Blob/decision refs. Inspect
those through authorized private artifacts/evidence; this direction does not
claim they already appear in the human summary or add a new event protocol.

### Terminal exception

Put the actual held/error status before explanatory data. Show whether there is
a known pending response; preserve the state file and state the no-resend rule.
For malformed/missing results or failed finalization, show BLOCKED and no accepted
summary. A held effect dominates a plausible candidate/review message.
Distinguish a completed `REQUEST_INPUT` (actual missing fact), `ROUTING_HOLD`
(unaccepted semantic choice), and `LIMIT_REACHED` (no success, no limit reset).
None automatically establishes a user-only action. Do not infer permission,
network or identity diagnoses from an error label alone.

Known pending response: existing `--native --recover-only` retrieves that exact
saved response, with the same verified SOCKS path and private session file.
Unknown effect: supported reconciliation, not a reset, new parent or retry.
A new isolated scenario is not a replacement for a held original parent.
Supported hosted-session stop/resume belongs to authorized acceptance tooling;
it is not a terminal button and is not VM power or hard-crash proof.

### Component report

Keep a compact header with exact source, runtime/run outcome and freshness.
State intended environment and actually observed deployed versions, otherwise
NOT VERIFIED. Use one row per canonical component with the mission columns:

`Component | RAG | Evidence (revision/run/environment + freshness) | Remaining work/next action`

Green means fresh end-to-end pass for that component in the intended environment
on the exact candidate; amber means partial/not executed/unverified/stale; red
means a current evidenced failure or blocking criterion. Never derive green
from schema tests, final message text, SDK completion, uploads or healthy hosts.
Keep advisory acceptance distinct from the report's component RAG.

### Readability, color and light/dark behavior

Inherit the user's terminal foreground/background in light and dark themes.
No forced ANSI colors or theme toggle. RAG always includes a text meaning so
color/emoji is not the only signal; plain `GREEN`, `AMBER`, `RED` is an equivalent
report rendering when glyph support is absent. Use linear reading order,
short headings and wrapping, not a wide TUI grid for generated prose.
The current human renderer prefixes every generated line with `  | `, neutralizes
terminal/control/bidi characters and wraps to available width. Retain those
safeguards and keyboard/one-message operation; `/quit` exits at the prompt, not a
remote cancellation guarantee. `--show-ids` is explicit sensitive disclosure,
not a default. Keep full session IDs, private paths, credentials, raw traces and
exact private refs out of the ordinary human summary/public evidence.

## Full-scope user journeys

| Architecture flow | Trigger and cross-component path | User return / confidence boundary |
|---|---|---|
| `design-review-revision` | Synthetic request → terminal-demo → coordinator-routing trusted gates/Decision-1 → blob-shared-context requirements → remote architect → remote reviewer findings → architect changed candidate → reviewer exact revised review → coordinator publication | Current advisory design/review and actual decision/artifact refs in authorized evidence. No fabricated transcript or release claim. |
| `followup-and-recovery` | Completed same parent adds queue → coordinator records requirements and invalidates stale refs → same architect/reviewer children → new exact design/review. Known pending response retrieves without resend; native checkpoints/Blob effects reconcile. Authorized stop/resume verifies retained state. | New revisions, retained private ingress and stable alias observations. Exact continuity/recovery need source-bound checks; unknown effects stay held. |
| `independent-parent-isolation` | Distinct synthetic request → separate trusted parent/children/Blob namespace → remote design/review → independent output and negative scope checks | Separate result; aliases alone do not prove isolation. Account-wide Blob Contributor means application-enforced ownership, not storage-enforced per-role RBAC. |
| `exact-candidate-delivery` | Committed skeleton/candidate → DevOps normal azd deployment under lock → E2E same candidate → canonical component report before acceptance/dependent release | Actual operation/probe outcomes and observed versions, not an uploaded-bundle success screen. Construction does not mutate the shared environment. |

Each journey's exact Architecture flowSteps and requirement joins are in the
JSON contract. The state/action matrix covers ready, streaming, accepted,
request-input, routing-hold, limit-reached, known-response recovery,
unknown-effect hold and failed/invalid output. It is presentation direction,
not a change to runtime authorization or automatic retry logic.

## Checks, implementation handoff and current component status

Run `python tests/test_delivery_user_experience.py --evidence docs/requirements/checks/delivery-user-experience.txt`.
It validates structure, D1–D7 and architecture joins, screen coverage, RAG
semantics, source references and safe actions, with negative mutations.
These are UX schema checks, not remote behavior tests or usability certification.
Existing HumanTerminalTests in `tests/test_demo.py` map to stdout compatibility,
revision order, no-resend recovery, held/invalid output and safe wrapping.
Their presence is a test target, not a claim that they ran in this UX turn.

Scrum Master uses the existing architecture dependencies when decomposing work;
Developer implements only authorized presentation gaps, without modifying the
machine protocol. DevOps then E2E verify the exact committed implementation under
the existing environment lock before assignment acceptance. This UX schema pass
completes direction only; it does not release deployment-dependent tasks.
No additional approval stage or disposition ledger is introduced.

| Component | RAG | Evidence (revision/run/environment + freshness) | Remaining work/next action |
|---|---|---|---|
| deployment | 🔴 RED | Current `5757a3a` source: all three azure.yaml predeploy hooks invoke package_guard.py; no deployed operation attempted here | DevOps replaces/tests incompatible receipt hooks, deploys skeleton and probes exact candidate |
| coordinator-routing | 🟠 AMBER | Current UX/source mapping only; intended dev-lab live gates NOT VERIFIED | Verify genuine gated decisions and exact-current finish |
| architect | 🟠 AMBER | Current remote-flow direction; no fresh live design/revision | Verify first design and actual-findings-driven change |
| reviewer | 🟠 AMBER | Current exact-revision direction; no fresh live review | Verify real findings and revised-candidate approval |
| blob-shared-context | 🟠 AMBER | Current private-provenance direction; no fresh MI/private-path operation | Verify immutable exchange, producer refs and fenced publication |
| session-continuity-recovery-isolation | 🟠 AMBER | Current state/action design; no fresh live continuity/recovery/isolation | Verify same-parent follow-up, known recovery, supported stop/resume and independent parent |
| terminal-demo | 🟠 AMBER | UX contract only; no fresh synthetic remote demonstration | Exercise full revision flow and same-parent follow-up with truthful report |

No deployed versions or runtime operation outcomes were observed in this design
turn. Qualitative layout preferences are non-blocking; any mandatory correction
must identify an original mission criterion and a falsifiable failure.
