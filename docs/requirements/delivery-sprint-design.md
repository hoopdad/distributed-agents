# Sprint terminal flows and screen designs

## Scope and source

SprintDesign for `three-role-delivery`, grounded in mission D1-D7/F1-F4 and
the accepted [Architecture](delivery-architecture.json),
[UserExperience](delivery-user-experience.json) and
[ReleasePlan](delivery-release-plan.json). The executable
[sprint design contract](delivery-sprint-design.json) joins all six task seeds
to those existing flows and three terminal/report surfaces. Initial source:
`9b937cc3a4ab075cb174044f56f8e715f4ab309c`, `feature/azd-demo-delivery`,
clean worktree. Source inspection includes `HumanView`, finalization/recovery,
and `HumanTerminalTests`. This is design-only, not deployed acceptance.

There are no assigned design implementation tasks and no open blocked design
items in the supplied packet. Do not convert deployment work into a new design
dependency or infer historical blockers. The current normal-azd receipt-hook
mismatch is D1/F1 work for DevOps, not a missing UI decision. SprintPlan remains
Scrum Master's task decomposition; this design neither schedules new tasks nor
changes prerequisites. No runtime, stdout, authentication, dependency or host
contract changes are made here. Qualitative layout preferences are optional;
these fixtures cannot create authority for extra product work.

## Screen 1: terminal turn

Linear reading order: orientation -> ordered observations -> current result ->
confidence footer. Existing `--native --view human` is an opt-in stderr
summary **after** validated output and successful state finalization. While
streaming, stdout remains the existing machine stream, not a new live phase
dashboard. Ready state uses the existing prompt/one-message entry; no extra
submission, cancel or reset control is introduced.

Illustrative layout only; angle-bracket fields are placeholders, not evidence:

```text
  | HOSTED COLLABORATION | observed records
  | Parent hosted alias: <observed alias>
  | Parent framework alias: <observed alias>
  | Turn <n> | requirements revision <n>
  | 1. architect | candidate revision <c>
  |   stable hosted alias: <observed alias>
  |   stable framework alias: <observed alias>
  |   pinned version: <observed version>
  |   advancing response alias: <observed alias>
  | <remaining actual delegations in emitted order>
  | Child bindings: observed aliases; exact continuity UNVERIFIED
  | New child creations / exact response inequality: not observed
  | Design r<n>/c<c>
  | <actual current design, treated as data>
  | Review r<n>/c<c>: <observed approval>
  | <actual current findings/recommendation, if present>
  | Coordinator: <actual status> | current result finalized
  | Model-history / restart / isolation: not established by this display
  | Release acceptance: separate private report; not certified here
```

Rows repeat only for actual calls, not a scripted four-call storyboard. Genuine
revision acceptance needs first findings, a changed immutable design and review
of that exact revision (D3/D4/F2); the existing human summary shows ordered calls
and current output, not all prior artifact bodies. Inspect the full chain in
authorized evidence (Screen 3). No fabricated first findings or approval text
is a substitute. `REQUEST_INPUT` shows actual decision reasons as data, without
inferring a user-only approval need. `ROUTING_HOLD` and `LIMIT_REACHED` describe
the actual non-success outcome, never permission to reset limits or retry.

## Screen 2: terminal exception and recovery

Held, invalid, malformed, missing or unfinalized output cannot become an
accepted summary. A plausible approved candidate does not override an effect
hold. For known-response retrieval, the existing summary adds:

```text
  | Retrieved known response; no resend. Retrieval is not a new invocation.
```

For actual held/unfinalized results, show observed code before explanatory data:

```text
  | HELD / BLOCKED: <allowlisted observed status>; turn not finalized; output unaccepted.
  | Preserve pending state; do not resend uncertain work.
```

For unusable result records, existing wording is:

```text
  | BLOCKED: result unavailable or invalid; no accepted summary.
```

These are existing renderer examples, not a promise that every early CLI error
passes through `HumanView`. Preserve actual CLI error classification and private
state on pre-render failures; do not invent a new error protocol.

The exact nine UX states/actions/gates are inherited, not redefined here.
Known persisted response -> existing `--native --recover-only` on the same
verified SOCKS path/private state; retrieve without a new send. Unknown effect
-> preserve hold and supported reconciliation. Missing logs/404/absent process
do not establish never-sent. No retry/reset/new-parent recovery action.
Known recovery may reuse original delegation records; that display is not new
agent activity. Hosted-session stop/resume belongs to scoped acceptance tooling,
not a terminal button, VM power operation or hard-crash proof.

## Screen 3: component report and authorized artifact trail

This is the existing acceptance evidence/delivery-report surface, not a new
interactive screen, output event, dashboard or renderer requirement.

1. **Candidate header:** exact committed revision/immutable artifact; observed
   runtime/run outcome; intended validated environment; actually observed
   coordinator/architect/reviewer versions. Missing values say NOT VERIFIED.
2. **Private artifact trail:** exact requirements -> first design -> actual
   first findings -> changed design -> exact revised review -> coordinator
   acceptance; real gated decision refs and child/producer/prerequisite joins.
   `ArtifactRef` and producer binding supply provenance, not an alias alone.
   Review approval of an old candidate is never current approval.
3. **Verification and action:** canonical seven rows with freshness, actual
   checks, accepted work versus unresolved criteria and precise next owner.
   Public handoffs summarize sanitized evidence; exact private identifiers,
   full Blob refs, credentials, paths and raw traces stay authorized/private.

Report columns remain:
`Component | RAG | Evidence (revision/run/environment + freshness) | Remaining work/next action`.
Use GREEN only for fresh exact-candidate component E2E pass; AMBER for
partial/not executed/unverified/stale; RED for current evidenced failures.
Advisory design approval, an SDK envelope, a schema pass or a healthy host
cannot establish deployed green. Never claim release without fresh D1-D7.
Account-wide Blob Contributor means application-enforced ownership, not
storage-enforced per-role RBAC isolation.

## Sprint journeys and task joins

| Existing flow | Screen sequence and return | Task seeds |
|---|---|---|
| `design-review-revision` | Terminal entry -> trusted coordinator/Blob -> real remote architect -> reviewer findings -> changed design -> exact revised review -> finalized advisory summary -> private artifact trail/report. Screen 2 replaces acceptance on hold/invalid output. | coordinator-blob-contract; remote-specialist-revision; terminal-evidence-surface; integrated-terminal-acceptance |
| `followup-and-recovery` | Completed nonheld same parent adds queue, retaining private ingress -> new requirements invalidate stale approvals -> real revision flow -> current output. Persisted known-response retrieval uses Screen 2's no-resend boundary. Supported stop/resume evidence returns in Screen 3. | terminal-evidence-surface; continuity-recovery-isolation; integrated-terminal-acceptance |
| `independent-parent-isolation` | Distinct synthetic request/private state -> separate trusted namespace and children -> own remote result -> exact scope/artifact comparisons in Screen 3. Different aliases alone prove nothing; this parent does not replace a held one. | continuity-recovery-isolation; integrated-terminal-acceptance |
| `exact-candidate-delivery` | Committed candidate -> DevOps azd under lock -> separate E2E same-candidate probes -> Screen 3 actual outcomes/versions and component RAG. | azd-walking-skeleton; integrated-terminal-acceptance |

The JSON preserves the Architecture's ordered step IDs and ReleasePlan's exact
task/component/requirement joins. No new persona, component, flow, service,
permission or task dependency is introduced. All hosted specialists stay remote.

## Readability and implementation/verification handoff

Inherit light/dark terminal colors; no forced ANSI or theme toggle. Preserve
`  | ` data prefix, control/bidi neutralization and width wrapping (existing
renderer minimum 24 columns; narrow fixture at 32). Prefer sequential regions
over wide TUI grids. RAG includes GREEN/AMBER/RED text, not color alone. Treat
generated headings, findings and request-input reasons as untrusted data, not
executable controls. No default `--show-ids` or raw private-ref disclosure.

Developer receives the layouts and existing `HumanTerminalTests` targets:
unchanged stdout/parser, four-call revision order, same-parent revisions,
known-response retrieval without send, held/invalid/finalization no-success,
and safe narrow rendering. These are test targets, not newly observed passes.
Scrum Master preserves the dependency-free first DevOps walking skeleton and
all real downstream prerequisites. Design completion releases none of them.

Construction supplies actual local tests and an exact committed implementation;
it does not mutate the shared environment. Existing DevOpsWorkLoop then
EndToEndTestLoop deploy/verify that exact candidate under existing environment
and configuration resources before original assignment review/acceptance.
No new review stage or disposition ledger. All assigned implementation work
still requires passing in the deployed environment.

Run `python tests/test_delivery_sprint_design.py --evidence docs/requirements/checks/delivery-sprint-design.txt`.
This executes contract/schema and negative-mutation tests, not deployed behavior
or usability testing. No design implementation is assigned in this packet;
the bounded output is the sprint design and executable contract. Product
acceptance and deployment-dependent assignments remain unverified.

Observed local results for this design: 9 dedicated contract tests passed;
all 37 delivery-contract regressions and 7 existing HumanTerminalTests passed.
Actual command output is retained in `checks/delivery-sprint-design*.txt`.
The installed Python 3.13 `pip check` diagnostic exited 1: the unrelated
installed `jetset-bank-demo-agents` package requires older framework versions
than that interpreter has. No packages or dependency manifests were changed.
The full `Test-Demo.ps1` gate was not executed because its initial dependency
prerequisite already fails; these focused passes do not certify a clean pinned runtime or full application
suite. This local environment diagnostic is not a demonstrated design-contract
failure or a current deployed failure; it does not justify changing product
requirements. DevOps must select/verify the authorized pinned runtime before
application acceptance checks.

## Current component status

| Component | RAG | Evidence (revision/run/environment + freshness) | Remaining work/next action |
|---|---|---|---|
| deployment | RED | Current 9b937cc azure.yaml still has three package_guard.py predeploy hooks; D1/F1 mismatch, not an attempted cloud failure | DevOps replace/test hooks, deploy skeleton and probe exact revision |
| coordinator-routing | AMBER | Current sprint design/source join only; deployed behavior NOT VERIFIED | Verify trusted gates, genuine Decision-1 and exact finish |
| architect | AMBER | Current screen/artifact trail design only; no remote execution here | Verify first immutable design and actual-findings-driven revision |
| reviewer | AMBER | Current exact-review presentation design only; no remote execution here | Verify actual first findings and exact changed-candidate approval |
| blob-shared-context | AMBER | Current private provenance layout only; private MI exchange NOT VERIFIED | Verify actual exchange, immutable provenance and fenced publication |
| session-continuity-recovery-isolation | AMBER | Current safe-action/layout design only; live scenarios NOT VERIFIED | Verify follow-up, recovery/checkpoints, supported stop/resume and isolated parent |
| terminal-demo | AMBER | Local contract and 7 existing human-view fixtures pass; fresh remote terminal flow NOT VERIFIED | Verify actual revision flow and same-parent follow-up on deployed candidate |
