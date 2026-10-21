# Customer hosted-session prototype: blocked release notes

## Release decision

**October 21, 2026 — BLOCKED; not customer-ready. No release PASS.**
The customer goal is a hosted coordinator repeatedly calling remote architect
and reviewer agents while preserving each specialist's session within one
parent conversation. Exactly three hosted roles and no hidden local fallback
remain required.

### Current measured execution and evidence boundary

Original repaired-join E2E **actually executed** on application
`b42ab2f84e023f52c6c70e46c93d77b86949831d` and selected lab
`885801565ae11878a7c4f33c29f6b45b0eb19af7`. The original report and original
Architect, Critic and Product Owner records were opened for this correction:

- Application wrapper: 206 tests passed.
- Complete corrected retained wrapper: another 206 application tests passed;
  233 retained tests were reported, with 230 passes, three explicit native-Linux
  exclusions and no failures/errors. All seven fresh-process discovery
  regressions and the committed split-root case passed; application imports
  resolved to their intended owner.
- The E2E owner accounted for documentation/index-only ancestry after accepted
  application integration `8b50f343`. These Windows Python 3.12.10 results
  cover that reported join, not a final Linux/amd64/Python 3.13 package.
- All three original reviewers agreed to completion of bounded E2E reporting
  with **predeployment FAIL**. Required `scripts/Test-Repository.ps1`
  validation remains **unexecuted** under its exact interactive-approval
  denial: no user response was available and no affirmative approval followed.
  This is not an executed test failure or a diagnosed Azure permission defect.

Original DevOps then entered and reported an accurate incomplete outcome.
Its owner followed a provenance-linked original stage proof and reported a
matching commitment for the **diagnostic** package. The package bytes were
not rehashed. Original reviewers' direct proof reads were denied; the
proof-content/hash comparison remains owner-attributed, not independently
confirmed here. That finding does not locate or verify common rollback ZIP
bytes, reconcile the separate historical UNKNOWN publication, or establish
next-operation effect readiness. Original reviewers agreed with the
incomplete report, with `taskComplete=false`; cloud-pass remains unmet.

Evidence references: original E2E outcome `bc39274e` and original DevOps
outcome `15229112` in delivery run
`490ad8fa-3d48-4905-a216-d2159f43d446`, including their original reviewer
records; [accepted repaired-source join](design.md#reviewed-discovery-repair-source-join);
[current continuation architecture](customer-prototype-repaired-join-continuation-architecture.json);
[remaining release plan](customer-prototype-repaired-join-remaining-release-plan.json).
These are inspected, attributed execution results, **not tests rerun by this
documentation correction**. No settings, engine, cloud or denied proof access
was attempted here. Agreement on a FAIL report cannot waive AC1–AC9/G1–G8.

### Current closing owners and localized gates

1. **Exact repository-check approval:** obtain affirmative approval of the
   previously denied bounded execution and its actual interactive tool prompt,
   then run and pass the required validation. No retry before approval,
   alternate-path bypass or constituent-check substitute is permitted.
2. **Existing original DevOps, coordinated by Scrum:** independently obtain
   provenance-backed common-package ZIP and operation-bound unresolved-effect
   record locators, then verify the actual bytes and applicable effects.
   This lane does not require Linux success. The diagnostic finding is a
   bounded record boundary, not global absence, exhaustion or a user-only
   locator problem. Do not repeat denied access or uncertain effects.
3. **Dependent original DevOps execution:** after required source checks pass,
   revalidate the same selected engine read-only without startup replay or
   Docker restart; run both complete corrected actual Linux suites and
   hosting/package gates. Actual package readiness **and** independent common
   rollback-byte/effect readiness must pass before one serialized publisher.
4. **Live acceptance:** verify actual final common-bundle G1–G4 and a completed
   non-held initial parent before same-parent follow-up and once-only supported
   stop/resume. Separate-parent isolation requires final deployed bindings,
   not recovery success. Preserve all continuity, provenance and cleanup gates.
5. **Existing integration/final-closeout Developer:** retain reviewed delivery
   through application `8b50f343` and lab `88580156`. The sibling delivery
   assignment is pinned to earlier reviewed application `b42ab2f8`, excluding
   this correction and subsequent planning. This correction needs its own
   original Architect/Critic review before later exact-ref delivery; no
   moving-HEAD push or completed final AC8 claim is authorized.

Final deployed/common-bundle and rollback bindings remain unverified.
Historical UNKNOWN publications, held parents and cleanup uncertainty remain
open. Independent investigation and reviewed-document delivery are not blocked
by Linux success; dependent execution is not unlocked by this status update.
The sprint and release remain partial.

## Historical October 20 source and bounded handoffs

The following source history is retained, not redispatched. The October 21
measured status and closing owners above supersede obsolete pending-construction
and pending-E2E assertions below, without erasing their original outcomes.

The earlier closeout inspected application
`23e7d48d4b227638638294072092427942a15e7e` on the feature branch with a clean
worktree/index, comparing unchanged runtime, tests, scripts, configuration,
dependencies and release descriptors to baseline
`b74b84edb6c05fb4dc7f58ba7f88925e2402ddc9`. That was source inspection, not
operational installation or new test execution. It reported accepted RP-S3
predeployment FAIL and an unmet DevOps cloud-pass condition. Those historical
findings remain distinct from the repaired-join execution reported above.

- Customer-first README and opt-in human stderr presentation remain implemented.
  Machine delegation/result contracts and acceptance parsing are unchanged.
- Two-turn, controlled four-call reject/revise/review, both-specialist restored
  model-history/fresh-history and exact-response no-resend fixtures remain
  retained offline controls, not a live demonstration.
- Accepted RP-S1 source/check handoff:
  `b74b84edb6c05fb4dc7f58ba7f88925e2402ddc9`.
- Accepted RP-S2 application preparation at
  `0e9add565d22b2cb617485e257875e72984907af` consumes the earlier outgoing audit
  at `61a99cba878b62fe5df0d1de361a178d87c273a9` and inspects subsequent drift.
  Its local tracking comparison was 84 ahead/zero behind, with no configured
  feature upstream. Those are attributed historical local-reference counts,
  not current server freshness or authorization to push every outgoing commit.
- Accepted RP-S3 executable/observation mapping:
  `673d1e9e9913bd636c35c91aa9b013b05b355d69`. It maps
  `live_acceptance.py`, workflow/history fixtures and private input requirements.
  Supplied JSON consistency is not independently authenticated provenance.
- Historical accepted RP-S3 backlog review:
  `be996f84694f9c94f163448f8afcc3ddce095223`; retrospective:
  `23e7d48d4b227638638294072092427942a15e7e`.

The [release plan](customer-prototype-release-plan.md) preserves RP-S1, RP-S2
and RP-S3 contracts. Accepted architecture, UX, planning, application checks,
observation mapping and accurate FAIL reports remain closed only within their
originating boundaries. Neither identity-remediation path is live-selected.
The historical `NATIVE_HOST_PRINCIPAL` failure occurred before architect
application execution; it is not a newly observed candidate failure or proof
of a provider defect or missing grant.

## Requirement completion ledger

| Criterion | Current disposition | Remaining proof / closing owner |
|---|---|---|
| AC1: remote collaboration | Blocked; live proof not established | Original DevOps must verify actual three-role current artifact collaboration after reviewed integration and release gates. |
| AC2: two user turns | Unreached live | Compare actual parent and both roles' hosted/framework bindings and pins, exactly two child creations, fresh responses and current requirements. |
| AC3: repeated orchestration | Accepted offline coverage | Retain controlled four-call revision and direct model-history/fresh-history controls in joined-source validation; not live AC1/AC2 proof. |
| AC4: recovery/isolation | Unreached live | Confirm once-only supported compute stop/resume with retained checkpoints/effects and no duplicates; separately prove distinct-parent bindings/scope/content. |
| AC5: G1–G8 | Not passed | See gate ledger; no verified final common bundle or completed non-held initial parent. |
| AC6: customer clarity | Implemented; live demonstration unreached | README/source path and opt-in human view retained; actual two-turn demonstration remains unobserved. |
| AC7: exact release validation | Incomplete; original repaired-join offline suites passed | Required repository validation remains unexecuted under the exact approval denial; both corrected actual Linux suites and final hosting/package validation remain outstanding. |
| AC8: shareable source/push | Partial; reviewed source delivery retained | Application `8b50f343` / lab `88580156` delivery is accepted; existing closeout retains exact reviewed-document delivery, current correction review and final scoped Git accounting. |
| AC9: truthful delivery | Blocked documentation supplied; verified delivery incomplete | Conditional setup/demo available; exact final/rollback bindings, actual continuity proof, final package/push and release-owned cleanup remain unestablished. |

| Gate | Current disposition |
|---|---|
| G1 | Healthy exact three-role final common-bundle and rollback bindings unestablished; historical mixed deployment is not final. |
| G2 | Current actual accepted remote specialist collaboration unverified. |
| G3 | Actual final managed-identity private Blob operations and immutable accepted provenance unverified. |
| G4 | Genuine Decision-1 and deterministic final gates for the completed current parent unverified. |
| G5 | Actual both-turn/both-role continuity unreached. |
| G6 | Once-only confirmed supported stop/continuation/checkpoint/effect proof unreached; no hard-crash claim. |
| G7 | Separate-parent live binding/scope/content-exclusion proof unreached; offline controls retained. |
| G8 | Truthful blocked status documented; fresh exact bindings and release-owned cleanup proof incomplete; historical UNKNOWNs remain open. |

## Historical October 20 closing owners and stops (superseded routing)

These were the earlier closeout's actions, not current assignments. Accepted
ownership, runner, integration and repaired-join E2E work must not be reopened.
Use the current closing-owner list above for remaining work.

1. **Existing ownership Developer and originating Architect/Critic:** provide
   actual nonsecret Python/PowerShell resolver contents, attributable sibling
   branch/HEAD/base, eight-path statuses, owner-specific hashes with line-ending
   explanation and source-bound matched/crossed-root results through the
   approved external handoff, or arrange restoration of already-authorized
   bounded read access. Obtain substantive originating acceptance before runner
   writes. Qualified agreement with an incomplete report does not enable writing.
   Coordination designations already suffice; no renewed authority, write probe,
   checkout recreation or repeated denied probe is requested.
2. **Existing transport owner with Scrum coordination, then DevOps:** locate
   the existing accepted containment-source handoff; verify the current
   operational module path, module/source hashes and serialized resource
   availability. Supplied accepted host trust is usable, not missing authority.
   Execute retained Metadata tooling with approved settings loading and explicit
   roots to observe current versions/packages/identities, rollback assets,
   effective actions and unresolved effects. This lane is independent of coding.
   No new receipt format, trust regeneration or approval stage is required.
3. **Runner Developer and designated integration Developer:** after substantive
   ownership acceptance, implement/review the retained eight-path runner.
   Consume accepted application/observation handoffs, inspect later drift,
   reconcile reviewed commits with actual loaded roots/bytes/hashes, run joined
   checks and complete durable Git accounting and reviewed scoped push.
4. **Original E2E and DevOps:** validate the exact operational join. Pass
   exact-source application/repository/retained-suite, Linux/amd64/hosting-Python
   and immutable-package gates before serialized guarded publication and finite
   ingress. Reconcile effects before further operations. Verify G1–G4 and a
   completed non-held initial parent before follow-up. Recovery follows completed
   two-turn state; isolation has its own release prerequisites, not a recovery
   dependency. Deliver per-criterion evidence and positively identified cleanup.

Exact applicable prior references remain binding:

- `["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-LAB-OWNERSHIP/AssignedWorkDeveloperLoop","lab-ownership-review-evidence-access"]`:
  actual evidence and substantive originating acceptance remain required.
- `["yaml-loops-v1:sprint/1/RP-S1/task/RP-S1-CURRENT-SOURCE-CHECKS/AssignedWorkDeveloperLoop","current-source-checks-completion-status"]`:
  keep accepted source checks closed without unchanged reruns.
- `["yaml-loops-v1:sprint/1/RP-S1/EndToEndTestLoop","e2e-report-completion-status"]`:
  reporting completion preserves FAIL and does not establish joined readiness.
- `["yaml-loops-v1:sprint/1/RP-S1/DevOpsWorkLoop","devops-bounded-assessment-completion-status"]`
  and `["yaml-loops-v1:sprint/1/RP-S1/DevOpsWorkLoop","devops-exact-release-cloud-pass"]`:
  accepted bounded reports remain closed; enclosing cloud-pass remains unmet.

Historical RP-S3 review/retro acceptance is consumed through its own supplied
original agreements, not transferred earlier votes. No prior disposition is
superseded, release criterion waived or originating stop/no-progress history
reset. No authoritative stop-count inference is made from aggregate rounds.

## Conditional setup and reproducible demonstration

Use [README setup](../README.md#setup-and-offline-checks): existing absolute
validated Python, PowerShell 7.2+, explicit lab root, allowlisted settings loader,
verified dedicated CLI context and owned strict-trust private connectivity.
Validate linkage without displaying private settings. Hosting remains
Linux/amd64/Python 3.13; Windows Python checks do not replace that gate.

The [two-turn commands](../README.md#two-turn-terminal-demonstration) are
implemented instructions, **conditional and not executed/live-verified here**:

```powershell
& $python -m demo.terminal --native --view human --socks $socks --session-file $session `
    --message 'Design a synthetic application with private ingress only.'
# Continue only after complete, non-held initial-parent evidence:
& $python -m demo.terminal --native --view human --socks $socks --session-file $session `
    --message 'Add an asynchronous queue; keep private ingress and all earlier requirements.'
```

Resolve `$socks` from the retained owned connectivity tooling and `$session`
to a new private synthetic-parent filename outside both repositories. Preserve
every existing session file. Actual reviewed release readiness is required
before sending. Never replace held parents or replay unknown effects to obtain
a demonstration. Omit `--show-ids`; use only synthetic text and safe aliases.
No sanitized actual live continuity proof is available to publish.

Raw terminal capture is not enriched cross-scenario evidence. DevOps must
associate actual request captures, manifests, immutable artifacts, cumulative
journals and checkpoints; do not reconstruct observed sends from intentions.

## Historical validation attribution, bindings, Git and cleanup

This section preserves the October 20 closeout's attributed observations and
then-outstanding work. It is not a fresh inventory or the current E2E/DevOps
status. See the October 21 execution and ownership sections above.

Supplied accepted RP-S1 Developer evidence reports 204 Windows offline tests
in **47.262 seconds**, dependency/compilation checks and repository validation.
Separate accepted RP-S1 E2E evidence reports 204 tests in **40.207 seconds**
and repository validation covering 79 public files. These are distinct
historical executions, not rerun by closeout. The unclosed Proactor transport
ResourceWarning remains disclosed; no warning-free, final Linux/package or
live-success claim is made.

The supplied RP-S2 prerequisite PASS remains owner-attributed: reviewers
inspected script scope, not the execution capture. Current RP-S3 DevOps reached
local retained-contract and named historical-evidence inspection only; it
reported no settings import, transport, cloud query, publication, inference or
compute stop. No new prerequisite rerun is requested merely for review credit.
Documentation-only closeout validation is reported separately by the owner.

**Final exact deployed versions/common package: not established. Exact rollback
bindings: not freshly verified. Final scoped push: not verified.** The supplied
earlier Metadata observation listed architect 17, reviewer 15 and coordinator 23,
with different coordinator versus specialist content hashes and zero inference.
Those are historical mixed diagnostic bindings, not current final/rollback
inventory. The [recovery chronology](identity-recovery-plan.md) retains
historical bindings, the original publication UNKNOWN and held parents.
No package was built/published or rollback asset removed by this closeout.

Supplied Scrum reviews place current sprint documentation/planning commits on
the authorized application feature branch and identify no additional
current-sprint task-code commit requiring abandonment accounting. That is
attributed review evidence, not fresh comprehensive cross-repository inspection.
No runtime code or abandoned task branch is created by this documentation work.
RP-S2-SOURCE-INTEGRATE still owns full task/branch/commit reconciliation, actual
loaded-root installation and final scoped push. Every task commit must reach
authorized feature history or remain on a named retained branch with its task,
commits and concrete abandonment reason recorded in a feature-branch commit
message. This closeout does not certify that outstanding integration.

No cloud transport, mount, listener, inference or deployment process is started
here; no cleanup of historical or unknown-owner resources is attempted. Preserve
canonical dirty/staged work, retained branches, old sessions/packages/versions,
UNKNOWN effects and historical cleanup uncertainty. Account-wide Blob
Contributor provides application-enforced role/parent isolation, not malicious-
host or storage-RBAC isolation. SDK at-least-once journals do not guarantee
exactly-once deployment effects.

Product Owner submits these blocked notes and updated README for the existing
ReleaseCloseoutLoop's Stakeholder, Architect and Critic review. Their current
closeout votes are not supplied. Documentation acceptance cannot complete the
unmet customer outcome.
