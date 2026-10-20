# Customer hosted-session prototype: release architecture

## Current architecture amendment: operational context is not tooling ownership

This entry supersedes only the pending ownership/runner and operational-root
handoffs in the earlier entry below. Inspected application baseline:
`1bd157d05116b076b0aa45b4fb6bfe531e5d28d0`, clean on
`feature/customer-hosted-session-prototype`. The registered feature lab sibling
is clean at `18429840e86d92c26611bae3ffdc7095ca87592d`. No runtime, settings,
credentials, lab source or cloud resources changed in this Architect turn.
The existing solutionModel below remains canonical: ten components, five flows,
eighteen steps. This amendment affects `release-toolchain`, `guarded-release`,
principally `release-join` and `release-package`; it adds no service/framework.

### Accepted predecessor and concrete defect

The predecessor `bb3af682-2d1c-41cf-97e7-312f624ea669/result.json` records
substantive original Architect/Critic acceptance (`agree` and `taskComplete`
true, no unmet criteria) for these exact originating boundaries:

- `sprint/1/RP-S1/task/RP-S2-LAB-OWNERSHIP/AssignedWorkDeveloperLoop`;
- `sprint/1/RP-S1/task/RP-S2-DECISION-RUNNER/AssignedWorkDeveloperLoop`;
- `sprint/1/RP-S1/task/RP-S2-SOURCE-INTEGRATE/AssignedWorkDeveloperLoop`.

Do not reopen them, renew designations, repeat unchanged runner fixes, or
redispatch accepted application continuity/history/presentation work. The
predecessor's `sprint/1/RP-S1/EndToEndTestLoop` has original Architect/Critic/
Product Owner agreement on an actionable **predeployment FAIL**, not live PASS.
Earlier pending-vote/write-block statements below are historical within those
accepted boundaries, not current prerequisites. All historical UNKNOWN effects,
held parents, rollback assets and original no-progress stop semantics survive.

The supplied operational-profile evidence's SHA256 was independently matched
to `38ec94d9d218e25791b60a2ed0dac80877538b0dcb128e94452aac077571f8b2`.
It records an existing configured dedicated profile matching the canonical lab
and no profile at the sibling-derived location. No credentials were inspected
or copied. Current sibling source inspection confirms:

| Entry point | Confirmed coupling that the correction must cover |
|---|---|
| `Test-LabPrerequisites.ps1` | Overwrites imported `AZURE_CONFIG_DIR` with tooling-root `.azure-cli` before account verification |
| `Test-PrivateConnectivity.ps1` | Calibration requires that same tooling-derived profile; calls prerequisites without an independent operational-context input |
| `Build-CodePackage.ps1` | Selects tooling-root `.azure-cli` before Azure CLI / azd bridge checks |
| `Build-BundledCodePackage.ps1` | Exports tooling-root `.azure-cli/wsl` into WSL |
| `Invoke-WslCodeRelease.ps1` | Calls prerequisites and exports tooling-root `.azure-cli/wsl` for publication |

This is a configuration/tooling contract defect, not evidence of an expired
credential, missing grant, unavailable transport or provider identity remedy.
Directory/linkage evidence establishes none of those live conditions. Separating
paths alone is not a user-only blocker and does not select identity path A/B.

### Smallest supported contract correction

Keep `ApplicationRoot` as application source and `LabRepositoryRoot` as the
selected **tool-source owner**. Every loaded wrapper, Python module and
PowerShell resolver must still belong to the selected reviewed feature sibling;
retain matched-root success, crossed-root `LAB_TOOL_OWNER_MISMATCH` rejection,
raw-byte source seals and actual loaded-source verification.

Add an explicit `OperationalLabRoot` input to the affected retained entry points
and propagate it through their callers. It selects only the existing dedicated
lab operational context, never wrapper/module/package source. For this delivery,
derive the supplied argument from the unchanged checked-in
`scripts/Use-Settings.ps1` import of `.local/lab-settings-native.json`:
the imported `LAB_REPOSITORY_ROOT` identifies that existing context and imported
`AZURE_CONFIG_DIR` identifies its dedicated Windows profile. Do not rewrite
private settings to make the feature sibling look like the operational root.
If preserving legacy callers with an omitted argument, default only to the
selected lab root's existing dedicated context, with the same validation;
never search for another profile or silently fall back.

Before Azure/azd/transport operations, validate canonical absolute paths,
reject reparse/escape substitutions and missing directories, and require the
selected Windows profile to equal the imported dedicated profile and the
operational root's `.azure-cli`. Compare the operational registry's registered
lab tenant/subscription with the selected tool registry and imported expected
scope; reject divergence before external operations. Preserve project/region/
model and exact target checks. Registry scope equality authorizes no adoption
of dirty registry/source changes, and does not replace account readback.
Do not output private values or inspect profile contents. Never accept a
default/production/arbitrary existing profile merely because account IDs match.

Windows callers reuse that existing profile. WSL callers must explicitly map
the same operational root's retained `.azure-cli/wsl` context, preserving WSL
path translation, Azure CLI/azd credential-selection checks and environment
save/restore on success and failure. Do not assume Windows and WSL token caches
are interchangeable. Do not copy, inspect or symlink credentials or create a
duplicate profile. DevOps must establish actual existing WSL-context readiness
through retained checks; if supported authentication is genuinely required,
surface the actual device URL/code when produced, not a hypothetical request.
An unavailable supported arrangement returns a precise failed prerequisite
for existing Scrum/Architect resolution, not automatic human escalation.

Keep operational-root/profile metadata private and outside the runtime bundle.
Do not replace `LAB_TOOLS`/selected resolver roots with `OperationalLabRoot`.
Calibration's profile equality must compare against the validated operational
profile rather than weakening equality; preserve its project, scope, source
and no-replay checks. Continue excluding evidence/stages/packages from both
source repositories and credential/private context trees. Retain source hash,
package, containment-source, strict host trust and read-only mount gates.

### Original-owner implementation and verification handoff

1. **ReleasePlan/Scrum Master:** assign the existing Developer one bounded
   operational-context correction in the authorized feature sibling. Own the
   five entry points above, their precise caller/retained regression files,
   and only directly necessary shared helper/docs/index paths. Establish that
   exact path set before writes; the earlier eight-path runner designation
   alone does not own these new paths. No canonical dirty checkout writes,
   branch switching, infrastructure/permission changes or workflow/input edits.
2. **Developer:** implement explicit context propagation and tests with
   synthetic profiles/CLI boundaries, then original Architect/Critic review.
   Required coverage: legacy matched-root behavior; feature tooling with the
   existing distinct operational root; missing/relative/reparse/default/
   mismatched profile and tenant/subscription rejection before effects;
   calibration and every affected caller including WSL mapping/azd selection;
   environment restoration; unchanged crossed-tool rejection and loaded-source
   equality. Run targeted plus affected retained suite and application/repository
   checks. Report skips/exclusions, do not count them as covered Linux gates.
3. **Designated integration Developer:** join reviewed correction commits and
   exact loaded wrapper/helper roots and raw hashes. Commit/push scoped reviewed
   feature refs, including accepted application integration commit `1bd157d`
   if not already remote, with readback. Preserve unrelated work and durable
   task/branch/commit accounting. This is a changed exact join requiring fresh
   validation, not a repeat execution-unready integration report.
4. **Original E2E then serialized DevOps:** run local-script validation of the
   corrected exact join. DevOps independently resolves retained containment
   source/resource readiness and current target/rollback inventory; runs actual
   Linux/amd64/Python package gates; binds exact common bundle/version preview;
   then guarded publication, finite architect-before-reviewer identity decision
   and live G1-G8/AC1-AC9. No concurrent deployer or uncertain-effect replay.
5. **Existing clarity/closeout owner:** remove the stale README ownership/write
   block after accepted handoffs, without replacing it with a live-success
   notice. Keep conditional demonstration commands and unmet live criteria.

Done for this architecture amendment means a concrete supported separation,
owned downstream correction and regression/caller contract, preserved canonical
model and original gates. It does not require implementing the Developer task
here. Source inspection and architecture checks cannot establish authentication,
cloud readiness, identity-path selection, Linux package or live acceptance.
Original Product Owner, Red Team and Critic review this deliverable next.

Validation in this turn: `scripts/Test-Repository.ps1` passed with the existing
validated absolute Python interpreter (80 public files, current inventory,
public/private boundary, JSON, PowerShell and whitespace). A direct architecture
check compared the parsed solutionModel with `HEAD`: unchanged ten components,
five flows and eighteen steps; IDs are unique, component references resolve,
and all five affected callers appear in this handoff. No dependencies were
installed. Unchanged runtime suites were not rerun for progress credit; targeted
and retained implementation regressions remain required for the actual fix.
No Linux/package, authentication, transport, deployment or inference check ran.

## Earlier architecture entry: canonical solution model (October 20, 2026)

This Architecture Loop inspected clean application baseline
`08ac1e71956c3f212f059b445c90b2fa40fa8aca` on
`feature/customer-hosted-session-prototype`. No reconciled feedback or
`priorDispositions` is supplied in this packet. Existing dated handoffs below
remain attributed history, not freshly collected acceptance votes or cloud
observations. Retain their principles, toolsets, identity selection contract,
bounded runner contract and AC1-AC9 matrix; do not redispatch implemented
continuity, specialist-history or terminal work merely because live gates fail.

The existing explicit `solutionModel` below remains unchanged: ten components,
five flows and eighteen steps. This revision consumes newly accessible
ownership/root evidence for `release-join`, not new services, storage,
framework abstractions or runtime contracts.
Downstream Architecture/SprintArchitecture artifacts and work cards reuse these
IDs and names. Implementation files remain mapped in the source trace below;
these names do not rename Python classes, CLI flags or diagnostic codes.

### solutionModel

```json
{
  "components": [
    {"id": "terminal-client", "name": "Terminal client", "supports": []},
    {"id": "coordinator", "name": "Hosted coordinator", "supports": []},
    {"id": "architect", "name": "Hosted architect", "supports": []},
    {"id": "reviewer", "name": "Hosted reviewer", "supports": []},
    {"id": "conversation-state", "name": "Parent and specialist conversation state", "supports": ["coordinator", "architect", "reviewer"]},
    {"id": "workflow-checkpoints", "name": "MAF workflow checkpoints", "supports": ["coordinator"]},
    {"id": "artifact-plane", "name": "Private Blob artifacts and effect journal", "supports": ["coordinator", "architect", "reviewer"]},
    {"id": "identity-boundary", "name": "Trusted identity and private transport", "supports": ["terminal-client", "coordinator", "architect", "reviewer", "artifact-plane"]},
    {"id": "decision-routing", "name": "Decision-1 routing and admission", "supports": ["coordinator"]},
    {"id": "release-toolchain", "name": "Guarded lab release toolchain", "supports": ["terminal-client", "coordinator", "architect", "reviewer"]}
  ],
  "flows": [
    {
      "id": "remote-collaboration",
      "name": "Remote design and review",
      "persona": "Prototype evaluator",
      "trigger": "A synthetic initial user requirement arrives in a fresh parent conversation.",
      "steps": [
        {"id": "collaboration-bind", "description": "Terminal submits the requirement; coordinator validates trusted parent scope and persists the current requirements revision.", "components": ["terminal-client", "coordinator", "identity-boundary", "artifact-plane"]},
        {"id": "collaboration-route", "description": "Coordinator applies deterministic readiness and effect gates, records a genuine Decision-1 choice when needed, and checkpoints graph progress.", "components": ["coordinator", "decision-routing", "artifact-plane", "workflow-checkpoints"]},
        {"id": "collaboration-design", "description": "Coordinator creates or reuses the pinned architect binding and restores its remote session; architect loads model history and exact inputs, then writes an immutable candidate.", "components": ["coordinator", "architect", "conversation-state", "identity-boundary", "artifact-plane"]},
        {"id": "collaboration-review", "description": "Coordinator invokes the pinned reviewer with restored history and exact current requirements/candidate; reviewer writes an immutable review. A rejection can repeat the same specialist bindings.", "components": ["coordinator", "reviewer", "conversation-state", "identity-boundary", "artifact-plane"]},
        {"id": "collaboration-return", "description": "Coordinator validates producer, hashes, prerequisites and revisions before fenced acceptance; terminal returns design/review content with separate truthful continuity presentation.", "components": ["coordinator", "artifact-plane", "terminal-client"]}
      ]
    },
    {
      "id": "two-turn-continuity",
      "name": "Same-parent specialist continuation",
      "persona": "Prototype evaluator",
      "trigger": "After a completed non-held initial turn, the evaluator adds an asynchronous queue to the same parent.",
      "steps": [
        {"id": "continuity-revise", "description": "Terminal reuses its parent binding; coordinator retains earlier requirements, appends the follow-up and invalidates stale candidate/review approval.", "components": ["terminal-client", "coordinator", "conversation-state", "artifact-plane"]},
        {"id": "continuity-invoke", "description": "Remote design and review runs again with the same parent, both hosted/framework child identities and pinned versions; model histories and response continuations advance.", "components": ["coordinator", "architect", "reviewer", "conversation-state", "artifact-plane", "identity-boundary"]},
        {"id": "continuity-verify", "description": "Compare actual binding identities, exactly two child creations across the pair, fresh invocation response IDs and current artifacts; return the revised result without treating aliases or recalled text as proof.", "components": ["coordinator", "artifact-plane", "terminal-client", "release-toolchain"]}
      ]
    },
    {
      "id": "supported-recovery",
      "name": "Supported compute stop and resume",
      "persona": "Lab operator",
      "trigger": "The retained local acceptance script requests one supported compute stop for a completed non-held parent.",
      "steps": [
        {"id": "recovery-stop", "description": "Persist the once-only stop marker and confirm the exact parent's stopped/idle state through the retained wrapper; an uncertain stop remains held.", "components": ["release-toolchain", "identity-boundary", "conversation-state", "artifact-plane"]},
        {"id": "recovery-resume", "description": "Continue that parent with retained checkpoints, pinned children and history; retrieve known responses or reconcile outputs instead of resending effects.", "components": ["coordinator", "architect", "reviewer", "conversation-state", "workflow-checkpoints", "artifact-plane"]},
        {"id": "recovery-verify", "description": "Independently compare checkpoint retention and actual create/send observations, then report continuity and no duplicate effects or the precise unmet gate.", "components": ["release-toolchain", "artifact-plane", "terminal-client"]}
      ]
    },
    {
      "id": "parent-isolation",
      "name": "Separate-parent isolation",
      "persona": "Prototype evaluator",
      "trigger": "After final-release prerequisites are met, a separate synthetic parent starts independently of recovery success.",
      "steps": [
        {"id": "isolation-bind", "description": "Create a distinct trusted parent scope and its own two specialist bindings; never adopt held children or copy another parent's scope.", "components": ["terminal-client", "coordinator", "conversation-state", "identity-boundary"]},
        {"id": "isolation-execute", "description": "Run remote design and review in the separate artifact namespace and enforce cross-scope rejection at assignment and artifact boundaries.", "components": ["coordinator", "architect", "reviewer", "artifact-plane", "identity-boundary"]},
        {"id": "isolation-verify", "description": "Compare both parents' actual child/scope bindings and verify exclusion of first-parent requirements; disclose that Blob isolation is application-enforced.", "components": ["release-toolchain", "artifact-plane", "terminal-client"]}
      ]
    },
    {
      "id": "guarded-release",
      "name": "Exact-source guarded release",
      "persona": "Lab operator",
      "trigger": "Reviewed owned task commits are ready for integration and the next scoped release attempt.",
      "steps": [
        {"id": "release-join", "description": "Designated integration owner joins reviewed application and lab commits with actual loaded roots and hashes, preserves unrelated work and records retained or abandoned task branches durably.", "components": ["release-toolchain"]},
        {"id": "release-package", "description": "Formal E2E validates the joined source through local scripts; DevOps verifies current target/rollback inventory, source tests, Linux hosting checks, immutable common bundle and exact-version preview.", "components": ["release-toolchain", "identity-boundary"]},
        {"id": "release-discriminate", "description": "DevOps serializes guarded publication and the finite source-bound identity trial, architect before reviewer; select A or B only on trusted receiver evidence and hold unknown effects.", "components": ["release-toolchain", "coordinator", "architect", "reviewer", "identity-boundary", "artifact-plane"]},
        {"id": "release-close", "description": "Run live G1-G8 against the final common bundle, join independent provenance with scenario assertions, and return AC1-AC9 status, exact final/rollback bindings, scoped push and owned cleanup without clearing historical unknowns.", "components": ["release-toolchain", "terminal-client", "artifact-plane"]}
      ]
    }
  ]
}
```

### Current evidence and bounded handoff

Fresh direct canonical lab Git inspection observed the unrelated active branch
with six modified and two untracked paths; all were preserved. The new
user-supplied mirrored ownership/root capture, collected October 20 at 18:30 UTC,
is accessible and its complete-file SHA256 matches the supplied comparison.
Its embedded sources and execution results were inspected, not rerun. This is
substantive new evidence availability, not another denied-inspection report.
The originating blocked result and original Architect/Critic unmet criteria
were also inspected; their agreement was explicitly not task acceptance.

| Originating unmet evidence | Newly inspected capture | Remaining boundary |
|---|---|---|
| Direct sibling branch, HEAD/base and owned-path status | Direct Git snapshots show the feature sibling at `bdd6b2a491ecbe0fc3b7570b86f297ac00bd2703`, the same merge base, empty full status and empty eight-path status | A point-in-time snapshot does not grant ownership or prove absence of later writers; use the supplied explicit designations, not cleanliness |
| Actual resolver contents, hashes and line endings | Canonical and sibling Python/PowerShell contents are included with raw and LF-normalized hashes; recorded normalized hashes match within each canonical/sibling pair | Contents and recorded hashes were inspected; independent embedded-source hash recomputation was tool-denied. Source inspection does not prove operational installation of future runner commits |
| Source-bound positive and negative controls | Four Python and four PowerShell results bind the loaded resolver and selected root: both matched roots succeed; both crossed roots reject with `LAB_TOOL_OWNER_MISMATCH` | These are inspected captured executions, not newly executed tests in this Architecture turn; formal exact-join E2E remains downstream |
| Preservation and safe-writing handoff | Before/after branch, HEAD and full status agree for application, canonical lab and sibling; all eight designated paths are listed | Original Developer/Scrum must submit this evidence and existing designations to originating Architect/Critic before dependent writes |

The recorded eight-case root results and normalized source comparisons agree.
No capture contents, private absolute roots or private settings are copied into
customer Git; the external evidence locator/hash belongs in the workflow
handoff. Earlier sections describing unavailable direct evidence remain
attributed historical observations and do not override this accessible capture.
Do not recreate setup or repeat the same capture merely to replace attribution.
No settings were imported in this turn.

Accepted host fingerprint and reference remain supplied trust inputs; their
earlier comparisons are historical observations, not rerun here. They do not
establish current SSH success, containment-source/resource readiness, inventory,
effective permission or live specialist entry. Use the supplied trust first
under the retained strict wrapper; do not request renewed trust authority.

For the exact originating ownership reference
`["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-LAB-OWNERSHIP/AssignedWorkDeveloperLoop","lab-ownership-review-evidence-access"]`,
use this packet's `ownershipRecoveryDefaults` as writer acknowledgement and
integration designation. Existing Developer/Scrum consume the accessible capture
through that originating task's original Architect/Critic review; do not create
a replacement ownership task or reset its five-round stop. This Architecture
Loop does not cast those task votes. Dependent eight-path runner writes remain
blocked until substantive originating acceptance. No renewed authority or
designation is needed. This architecture deliverable does not require that
downstream task to finish.

Scrum retains the existing bounded contracts below: ownership verification and
independent containment-source/resource plus trusted-inventory preparation can
proceed separately; Developer runner coding waits only for its real ownership
prerequisite. Designated Developer then reconciles reviewed commits and actual
loaded operational roots, preserving `LAB_TOOL_OWNER_MISMATCH`. Formal local-script
E2E checks the exact join. Original DevOps alone serializes publication/transport,
exact Linux/package/version gates, finite identity trial and live acceptance.
The current specialist-only B source remains an unselected candidate, not an A
selector or a live fix. Unsupported namespace change returns to existing
Architect-advised Product Owner/Scrum scope decisions, never relaxed equality.

The minimal downstream handoff is evidence consumption, then gated execution:

1. **Developer/Scrum:** return the new capture and existing designations to the
   originating ownership reviewers against their exact unmet criteria. Done
   means substantive safe-writing/root acceptance, not agreement on a blocked
   report. Exclude renewed setup, application redispatch and runner writes
   before that decision.
2. **Developer:** after that acceptance, implement the existing finite runner
   contract on its eight designated sibling paths, run targeted and retained
   regressions and commit only owned paths. Designated integration joins
   reviewed task commits and the actually loaded wrapper roots/hashes, retaining
   abandoned branches and durable task/commit/reason accounting. Matched-root
   evidence does not authorize crossed-root execution or canonical dirty writes.
3. **E2E/DevOps:** validate the actual joined source in the original E2E loop;
   independently finish containment-source/resource and inventory preparation.
   Original DevOps then owns serialized exact-package publication and bounded
   architect-before-reviewer ingress selection, followed by final common-bundle
   G1-G8. A/B remains unresolved until actual trusted receiver success.
4. **Release closeout:** only an accepted non-held initial parent permits the
   queue follow-up and supported once-only stop/resume. Separate-parent isolation
   has its own release prerequisites, not a recovery-success dependency.
   Preserve AC1-AC9, historical UNKNOWNs, held parents and rollback assets.

The solution model and evidence matrix are owner-ready for original Product
Owner, Red Team and Critic review. This is architectural completion, not agreement
on release acceptance. No deployment, permissions, cloud inference, stop/resume,
push or live AC1-AC9 verification is claimed; historical UNKNOWNs, held parents,
rollback assets and application-enforced Blob-isolation limits remain unchanged.

### Validation and attribution of this revision

Current read-only operations succeeded for application/canonical lab Git,
the originating outcome and original ownership reviews, the capture's complete
SHA256, embedded resolver contents and recorded matrix. The external capture
hash matches the user's supplied comparison. Its execution results remain
attributed to that capture, not this turn. Original ownership acceptance is
still pending; no reviewer vote is inferred from this architecture.

A mixed evidence-consistency/model/check command was denied by the tool layer
because no interactive response was available. A separate repository-local
model/check attempt, then isolated `scripts/Test-Repository.ps1` and
`Test-Demo.ps1` invocations with the existing absolute Python and explicit lab
root were also denied. No script execution or independent embedded-source hash
recomputation succeeded in this turn. The underlying access-policy requirement
is unidentified; this does not establish a missing Azure permission, project
authority, designation or user-only remedy. Do not bypass those denials.

The canonical model is retained unchanged, including ten components, five flows,
eighteen steps and the AC1-AC9/G1-G8 matrix. The previous architecture reported
an in-memory model check, 204 offline tests in 47.820 seconds, compilation and
repository checks; these remain historical results, not checks of this edit.
Current validation must be rerun through the authorized execution mechanism
before this revision is treated as newly repository-verified. No dependency,
runtime or lab source changed; no dependency installation, retained lab suite,
Linux hosting-package gate, settings import or cloud operation was performed.

## Current RP-S3 retrospective — preserve observation provenance and independent preparation (October 20, 2026)

Consume accepted SprintReview `be996f84694f9c94f163448f8afcc3ddce095223`
and its [retrospective decisions](customer-prototype-release-plan.md#current-rp-s3-retrospective--accepted-observation-handoff-without-live-entry-october-20-2026).
The accepted executable/observation map binds retained assertions to application
revision `673d1e9`; it neither installs external tooling nor authenticates
supplied observations. Raw terminal output, enriched cross-scenario inputs and
independently observed live provenance remain distinct. Never derive actual
create/send captures from journal intentions or reconstruct missing evidence.

Keep independent preparation executable: the existing transport owner with
Scrum coordination locates the accepted containment-source handoff; DevOps
verifies current module path, both source hashes and serialized resources before
retained Metadata execution. Historical hashes alone do not establish that
binding, nor prove the handoff absent everywhere. This is an existing safeguard,
not a new receipt format or approval stage, and not a runner-coding dependency.

Separately retain originating substantive ownership acceptance before sibling
writes, reviewed actual loaded-root integration and original exact-join E2E.
Continuation still requires verified common-bundle G1-G4 and a completed
non-held initial parent. Isolation keeps its own release prerequisites, not a
recovery dependency. No runtime contract, trusted receiver equality, root guard,
UNKNOWN hold or application-enforced Blob-isolation limit changes here.

## Current RP-S2 retrospective — evidence availability is distinct from check scope (October 20, 2026)

Consume accepted SprintReview `1e5eb2adc7714875e07ed69ffd2e2db0ab8c7877`
and its [retrospective decisions](customer-prototype-release-plan.md#current-rp-s2-retrospective--single-round-handoffs-without-live-progress-october-20-2026).
This adds no runtime contract and reopens no accepted architecture.
Inspecting a prerequisite script establishes its scope, not execution of that
script. A shell identifier alone is owner-attributed evidence when the original
reviewers cannot inspect the capture. Preserve that distinction in the existing
handoff; do not rerun a check merely to replace an unavailable capture.

Keep three independent boundaries explicit: substantive ownership/root evidence
before sibling writing; actual loaded-source integration before exact-join E2E;
and current trust/inventory plus exact-package gates before guarded DevOps
execution. Fresh host trust cannot discharge ownership, and accepted application
tree identity cannot establish external wrapper installation. Inventory remains
independent of runner coding under existing containment/resource guards.
Existing owners recover available original captures outside customer Git,
attribute missing observations, and retain the original closing actions.
No new evidence schema, ledger, approval stage, identity selection or acceptance
waiver is introduced. Trusted receiver equality, root guards, UNKNOWN holds and
application-enforced rather than malicious-host Blob isolation remain unchanged.

## RP-S1 retrospective — acceptance is not execution (October 20, 2026)

The current [retrospective decisions](customer-prototype-release-plan.md#rp-s1-retrospective--workflow-quality-and-blocked-outcomes-october-20-2026)
consume accepted SprintReview `350352282f6defafc777dff5c6748d7fb2da3b59`.
This is a process clarification, not a reopened architecture acceptance or
changed runtime contract. Earlier dated overlays retain their original scope.

Carry three distinct facts in the existing ownership/integration handoff:
supplied writer designation, originating substantive ownership/root acceptance,
and actual loaded operational source. A clean sibling or matching historical
trust field cannot supply the latter two. Existing Developer supplies actual
resolver contents, attributable Git/path/hash observations and source-bound
matched/crossed-root results outside customer Git; originating Architect/Critic
assess them before runner writes. Do not repeat denied inspections or replace
the capture with another summary. Preserve `LAB_TOOL_OWNER_MISMATCH`.

Designated integration Developer then joins reviewed commits with actual loaded
roots/bytes/hashes and durable task/branch/commit accounting. Original E2E checks
that subsequent exact join; original DevOps retains exact-package and cloud-pass
gates. These are existing dependencies, not an added approval stage. Independent
accepted source checks and bounded reports stay closed. No identity path is
selected, no equality guard relaxed, and no historical UNKNOWN or held parent
is cleared by retrospective agreement. Account-wide Blob access remains
application-enforced isolation, not malicious-host or storage-RBAC isolation.

## Architecture Loop recovery handoff — accepted trust input (October 20, 2026)

This invocation began on clean application `a1bca5d` on
`feature/customer-hosted-session-prototype`. No reconciled feedback or
`priorDispositions` was supplied. Retain the full-release principles, framework,
state design, identity alternatives, runner contract and AC1-AC9 matrix below.
This handoff changes no runtime, dependency, acceptance contract or authority.
Earlier "current" sections are dated observations, not fresh execution evidence.

### Verified input versus remaining execution proof

The eight specifically supplied recovery JSON files were read from the external
nonsecret mirror first; each parsed successfully. A value-suppressed comparison
now establishes that `accepted-host-trust-extract.json#accepted_host_fingerprint`
and `multi-agent-zip-25508ac5e30744cbae8a6b5b7682b5f2.attempt.json#host_fingerprint`
both exactly match this invocation's user-accepted fingerprint. The extract's
acceptance reference and source locator are present. These are private input
comparisons, not a new host-key observation or cryptographic authentication of
historical receipts. Do not copy their values or the private mirror into Git.

**Architecture disposition:** the independent accepted comparison value and its
evidence locator are supplied; do not request them again or substitute a newly
observed key. Original DevOps still verifies the actual current owner module/
source against independent acceptance and runs the retained strict prerequisite
wrapper using that accepted value. Accepted trust input is not current SSH
success, authenticated inventory, publication authority for historical effects,
or live specialist entry. Distinguish a missing input from a failed current
validation when reporting the next result.

`Use-Settings.ps1` loaded only the existing native settings. Suppressed-value
comparisons passed for canonical lab linkage and the historical approved
attempt's project and lab root. This verifies local linkage, not Azure login,
effective RBAC, current tenant/subscription readback or current deployed versions.
The approved historical attempt remains consumed; matching settings do not
authorize its replay.

Fresh direct Git inspection reports a clean registered feature sibling at
`bdd6b2a491ecbe0fc3b7570b86f297ac00bd2703`. Canonical lab registration now
reports `b7a47edf6172b1dd5dc4b0dc5a3db555fe762b2f` on its unrelated branch;
six modified and two untracked canonical paths were observed and left untouched.
Direct sibling resolver reads were denied by the tool permission layer in this
invocation. No alternate read or resolver execution was attempted after denial.
Neither file sizes, registration nor clean Git status establishes inspected
resolver contents, loaded hashes, exclusivity or substantive ownership acceptance.
The historical root matrix below is not a freshly executed matrix.

### Existing-owner closing actions, not another architecture or approval stage

For the exact originating reference
`["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-LAB-OWNERSHIP/AssignedWorkDeveloperLoop","lab-ownership-review-evidence-access"]`,
consume `ownershipRecoveryDefaults` as explicit writer acknowledgement and
integration designation evidence. No new designation is required. Existing
Developer completes point-in-time owned-path/resolver proof through the approved
inspection mechanism and original Architect/Critic ownership review; denied
inspection must remain disclosed, not silently promoted to acceptance.

The smallest supported release path remains conditional B evaluation, unless a
measured supported A correction is found. B is implemented candidate source,
not live-selected. Preserve specialist-only client delegation, trusted receiver
equality, immutable prerequisites, pinned parent/both-child sessions, model
history, checkpoints and fenced write-ahead effects as distinct contracts.

Scrum's existing planning stages retain these minimal lanes:

1. Originating ownership verification enables only the eight-path sibling runner
   assignment; offline coding does not wait for cloud inventory or SSH success.
2. In parallel, DevOps consumes the supplied accepted trust input for current
   strict-trust/context/inventory checks. Record precise failed prerequisites,
   not a renewed request for the fingerprint or designations already supplied.
3. Designated Developer integration joins reviewed application, runner and
   actually loaded operational wrapper bytes with explicit matched roots and
   durable task/branch/commit accounting. Keep `LAB_TOOL_OWNER_MISMATCH`;
   sibling commits alone do not install canonical wrappers. No canonical dirty
   checkout writes or shared branch switching are permitted.
4. Original E2E validates joined source through local scripts. Original DevOps
   serializes real publication/transport resources, performs exact-source Linux/
   amd64/hosting-Python package gates and guarded common-bundle publication, then
   the finite architect-before-reviewer identity decision and live G1-G4.
5. Only a completed non-held initial parent enables same-parent queue follow-up
   and once-only supported stop/resume. Independent-parent isolation needs the
   final release and comparison evidence, not successful recovery first.
   Preserve AC1-AC9/G1-G8, historical UNKNOWNs, held parents and rollback assets.

Unresolved A/B selection does not stop remaining artifacts. Actual namespace
mismatch returns through existing Architect-advised PO/Scrum reconciliation,
never equality relaxation or a new user-approval demand. Account-wide Blob
access still provides application-enforced, not malicious-host/RBAC isolation.
No cloud, permission, inference, stop/resume, publication or push was performed
by this architecture handoff. Owner-ready design is not Product Owner, Red Team
or Critic agreement; the existing Architecture Loop reviewers decide acceptance.

Validation used the existing absolute Python 3.12.10 executable:
`Test-Demo.ps1` with explicit canonical lab root passed dependency checks,
204 offline tests in 64.706 seconds and compilation (exit 0).
`scripts/Test-Repository.ps1` passed index, public-boundary (79 files), JSON,
PowerShell, context and whitespace checks. No dependencies were installed.
No lab code changed; retained full lab and Linux hosting-package gates were not
run. These local checks neither refresh the live blocker nor pass release gates.

## Current RP-S3 retrospective — assertions are not observation provenance

Accepted SprintReview `0f2e6276bb53f84605d745db24cafd1991133d21`
and the revision-bound RP-S3 executable/observation handoff distinguish a
validator's consistency checks from independent evidence of actual execution.
The [RP-S3 retrospective](customer-prototype-release-plan.md#current-rp-s3-retrospective--inspectable-evidence-and-continuation-entry-october-20-2026)
retains this distinction without adding a collector, ledger or contract.
The enriched scenario proof, raw terminal capture, cumulative effect transitions,
independent request-boundary counts and scoped checkpoint records are different
inputs; matching JSON cannot authenticate private Blob operations, genuine
Decision-1 execution or deployed common-bundle identity.

Integration consumes the accepted invocation/observation map once, joins actual
loaded operational roots and reviewed bytes, and supplies joined checks to formal
E2E. DevOps supplies independent private observations under the existing gates.
An accepted blocked report cannot supply the completed non-held initial parent
needed for continuation. Isolation still depends on G1-G4, not recovery success.
Substantive originating ownership acceptance remains required before runner
writes; independent established host trust is not an offline coding dependency.
No accepted architecture, session/state, identity or acceptance contract changes.

## Current RP-S2 retrospective — separate evidence joins

Recovery-entry input is accepted SprintReview
`16a57b6f6a77d4d2e8fbb58ecd179d115cf4e0b8`. The
[current retrospective](customer-prototype-release-plan.md#current-rp-s2-retrospective--evidence-reuse-and-executable-handoffs-october-20-2026)
consumes the accepted revision-bound application outgoing audit without
repeating unchanged checks. Local-reference ancestry and drift acceptance do
not establish current server state, a push, sibling ownership or installation
of reviewed wrappers at their actual loaded operational roots.

Keep structural recovery-file validity separate from substantive reconciliation
and current no-write resolver/owned-path proof. Existing Developer supplies that
proof for originating Architect/Critic ownership acceptance before runner
writes; the supplied designations already satisfy coordination input. Another
role's successful evidence read cannot supply the missing acceptance.
Independent established host trust/current private inventory remains DevOps-owned
and is not a prerequisite for offline runner implementation.

Integration still joins reviewed application/runner/operational bytes, roots
and hashes with joined checks and durable task/branch/commit and scoped push
accounting. Original formal E2E and DevOps exact-package/live gates remain.
Per-role ingress selection alone does not prove actual common-bundle G1-G4
or provide the completed non-held initial parent required by RP-S3.
No session, identity, provenance, root guard, dependency or architecture contract
changes. All accepted architecture handoffs remain closed; private observations
are attributed, not refreshed by this documentation delta.

## Current Architecture Loop: partial direct inspection (October 20, 2026)

Inspected application baseline `6e08b5470f7cd21ba46505e0c8628d8f1185bc34`
on `feature/customer-hosted-session-prototype`, initially clean. This invocation
supplies no prior dispositions or reconciled feedback. Retain the complete
principles, toolsets, state/identity design, runner contract and AC1-AC9 matrix
below; no framework, dependency, runtime, public contract or scope change is
needed. Older dated observations are history, not current execution evidence.

### New evidence closes part, not all, of the ownership inspection gap

The supplied recovery locator was used first: the three required summaries and
four named receipt candidates all exist and parse as JSON. Only file names and
top-level key names were displayed, not their private values. This establishes
availability in this session, not receipt authenticity, accepted fingerprint,
effective permission, current deployment or cleanup. `Use-Settings.ps1` loaded
the existing native settings, and a value-suppressed comparison confirmed the
canonical lab-root link. No authenticated cloud readback was performed.

Bounded direct Git inspection of the registered feature sibling **succeeded**:
its branch is `feature/customer-hosted-session-prototype`, HEAD is
`bdd6b2a491ecbe0fc3b7570b86f297ac00bd2703`, and `status --short`
returned no entries. Registration independently reports that same HEAD/branch.
This is new direct point-in-time evidence, unlike registration alone or the
earlier denied direct inspection. It is not exclusive ownership or permission
to write. Canonical lab HEAD remains
`63348876535de7c264dc1e9139bb6fd2684b0052` on the unrelated
`feature/swc-think-fast-aca-dns` branch, now with eleven modified and two
untracked paths. All thirteen remain untouched; canonical is not a runner or
integration writing location.

A combined read-only command also returned resolver source text, but its
aggregate output was truncated. Subsequent direct `view` calls for the sibling's
`release_roots.py` and `Release-Roots.ps1` were denied by the tool permission
layer. No alternate read or execution was attempted after that denial. Thus
this turn does **not** establish complete resolver inspection, a current
root-matrix execution, loaded-source hashes or wrapper compatibility. Successful
Git reads must not be generalized into those separate claims.

For the exact originating reference
`["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-LAB-OWNERSHIP/AssignedWorkDeveloperLoop","lab-ownership-review-evidence-access"]`,
carry this partial evidence and the supplied Developer writer/integration
designations to the existing ownership review. Do not reopen accepted source
handoffs, request those designations again, or infer reviewer acceptance.
The concrete remaining action is complete permission-capable bounded resolver/
loaded-root and owned-path verification by the existing Developer, then original
Architect/Critic verification before runner writes. This is an existing task
closing action, not a new stage or expanded user authority.

### End-to-end handoff remains unchanged

Exactly three hosted roles use pinned MAF/Foundry/Python, strict Pydantic
contracts, private managed-identity Blob and retained PowerShell/Python/WSL
tools. The parent manifest, restored remote framework sessions, each
specialist's model history, graph checkpoints and fenced effect journal keep
their separate responsibilities. Preserve trusted receiver equality, exact
immutable prerequisites, role versions, new response IDs and unknown-effect
holds. B remains candidate-only; A requires a demonstrated supported correction.

Scrum retains minimal contract-first tasks and Git reconciliation. Accepted
ownership enables the eight-path sibling runner task; designated Developer
integration joins reviewed application, runner and actually loaded operational
wrappers without canonical writes or root-guard bypass. DevOps independently
owns established transport trust and fresh sole-target inventory. Original E2E
validates joined source through local scripts; original DevOps owns final
Linux/amd64/hosting-Python package gates, guarded publication, finite both-role
ingress selection and live G1-G8. Actual release/transport resources must be
serialized, not merely scheduler-labeled. No GitHub Actions or new infrastructure.

No cloud, permission, publication, inference or supported-stop operation occurs
in this architecture turn. Current final/rollback bindings remain unverified,
historical UNKNOWNs/held parents remain preserved, and no release criterion
passes from these observations. Account-wide Blob Contributor still provides
application-enforced, not malicious-host/storage-RBAC, isolation. Original
Product Owner, Red Team and Critic agreement is not supplied in this invocation;
this owner handoff does not fabricate it.

### Validation of this documentation revision

The existing absolute Python 3.12.10 executable ran `Test-Demo.ps1` with the
explicit canonical lab root: dependency checking, **204 offline tests in
64.134 seconds**, and compilation passed (script exit 0). `Test-Repository.ps1`
passed index, public-boundary (**79 public files**), JSON, PowerShell, context
and whitespace checks. No dependencies were installed. No lab source changed,
so its full retained suite was not rerun. These checks are not Linux hosting-
package validation, formal E2E, fresh runtime progress or live release proof.

## Current RP-S1 retrospective — inspectable evidence is not transitive

Recovery-entry input is accepted SprintReview
`ca4345d5761d053e201747da4018e29c7720dd25`. Its current ownership
task remains unaccepted; DevOps reports historical-file access and an exit-2
strict-trust stop, not current ingress. Earlier successful sibling Git reads
and older denied reads are separately dated observations, not a combined
current safe-writing proof. This clarification changes no architecture contract.

The [current retrospective](customer-prototype-release-plan.md#current-rp-s1-retrospective--closure-and-inspectable-handoffs-october-20-2026)
refines evidence handoff practice, not the accepted architecture. Supplied writer
and integration-owner designations resolve coordination input; they do not prove
current sibling branch/base/status, owned-path preservation or loaded resolver
behavior. Historical receipt linkage, point-in-time safe writing, strict host
trust and successful specialist ingress remain separate facts.

DevOps reports reading the named recovery files; the originating ownership
assignment and reviewers report permission-denied reads and sibling inspection.
Do not silently promote one role's observation to another role's accepted setup.
Resume the already-authorized bounded evidence inspection in a permission-capable
session and present substantiated proof through the existing Architect/Critic
ownership review. Keep runner writes gated under
`["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-LAB-OWNERSHIP/AssignedWorkDeveloperLoop","lab-ownership-review-evidence-access"]`;
do not request supplied designations again, probe writes or recreate checkouts.

Existing Developer integration then reconciles reviewed application, runner and
required operational-wrapper revisions against actual loaded roots, preserves
unrelated work and records durable task/branch/commit accounting and scoped push.
Independent strict-trust inventory remains with DevOps. Original E2E validates
exact joined inputs before DevOps exact-package/publication/live acceptance.
No root guard, trusted receiver equality, session/history contract, dependency,
identity remedy or AC1-AC9/G1-G8 criterion changes. Accepted architecture stays
closed; this retrospective neither reapproves it nor proves live readiness.

## Current ownership-designation architecture (October 20, 2026)

This Architecture Loop inspected initially clean application HEAD
`4212a7b59270a0fe791735385a4359a6ab30cb68` on
`feature/customer-hosted-session-prototype`. This overlay consumes the current
user's `ownershipCoordinationApproval` and `ownershipRecoveryDefaults`; it is
not a new runtime design or a claim that the stopped task has passed review.
This invocation supplies no prior dispositions or reconciled feedback.
Older sections retain their technical contracts and dated observations; where
they describe missing writer acknowledgement/designation, apply the narrowly
scoped current evidence below rather than requesting the same approval again.

### Architecture decision: consume explicit coordination, retain acceptance

For the originating reference
`["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-LAB-OWNERSHIP/AssignedWorkDeveloperLoop","lab-ownership-review-evidence-access"]`,
Scrum and Developer may now present the supplied recovery evidence **together
with the user's explicit designations** to the original reviewers. This closes
the missing-designation input, not the entire ownership criterion. It neither
rewrites an originating disposition nor restarts runner writes by inference.
No accepted candidate, continuity, terminal or assertion handoff is reopened.

| Designation | Exact task boundary | What remains before use |
|---|---|---|
| Tooling writer: Developer | `RP-S2-DECISION-RUNNER`, lab repository, registered feature sibling only | Original ownership acceptance and current point-in-time checkout/path coordination; never write the dirty canonical lab |
| Integration owner: Developer | `RP-S2-SOURCE-INTEGRATE`, application and lab | Reviewed task commits, explicit owned paths, preservation of unrelated work and durable branch/commit accounting |
| Writer acknowledgements | Canonical dirty/staged paths preserved; task-owned writes only; `commit --only`; no shared branch switch, force-push or destructive cleanup | Actual compliance and original reviewer verification; registration/clean status alone still grants no ownership |

The writer's allowlist is exactly these lab-relative paths:

```text
foundry-tf/multi-agent/identity_decision.py
foundry-tf/multi-agent/Invoke-IdentityDecision.ps1
foundry-tf/multi-agent/tests/test_release_identity_decision.py
foundry-tf/multi-agent/Test-PrivateConnectivity.ps1
foundry-tf/multi-agent/observe_agent.py
foundry-tf/multi-agent/release_roots.py
foundry-tf/multi-agent/Release-Roots.ps1
.github/repo-index.md
```

This is path ownership for the named task, not authority to modify unrelated
infrastructure or private settings. Scrum's existing planning stages consume
the designation in their task contracts and preserve original acceptance gates.
If another substantive ownership failure is found, name it and its closing
action; do not relabel missing designation as a new user-input requirement.

### Fresh read-only observations and their limits

The supplied recovery-exception locator was used for the seven exact named
files, with no credential-tree scan. All seven exist and parse as JSON.
Allowlisted comparisons confirm the historical successful publication retained
identity, original UNKNOWN and held parent; the mixed deployment is explicitly
not live accepted and no provider defect is established. The approval record's
project and lab root match settings loaded only through `Use-Settings.ps1`.
The loader passed local validation, the registry parsed, and the configured lab
root matches canonical. These checks do not authenticate Azure or verify a
current effective grant, active version, transport fingerprint or tenant/
subscription readback.

Fresh canonical Git inspection reports the same lab HEAD
`63348876535de7c264dc1e9139bb6fd2684b0052`, unrelated branch, six modified
and two untracked paths. Registration reports the feature sibling at
`bdd6b2a491ecbe0fc3b7570b86f297ac00bd2703`. A direct sibling read/status
attempt was denied by the tool permission layer; no current sibling cleanliness,
exclusive writer state or loaded-source hash is asserted. No attempt was made
to circumvent that denial. Original owners use the existing approved inspection
mechanism to finish the bounded handoff; this is not missing user approval for
the supplied designation and does not block this design artifact.

The earlier executed root matrix remains dated evidence, not a new experiment.
Keep `LAB_TOOL_OWNER_MISMATCH` and explicit matched operational wrapper roots.
A sibling-developed runner may invoke canonical retained wrappers only with
their canonical root and verified loaded sources. If a required wrapper fix is
only on the sibling, that is not canonical installation: integration must
resolve it without canonical writes or changed private settings. An alternative
sibling operational root requires proof of all existing settings/profile/
registry/stage/source guards before effects; no unproven move is selected here.
Any solution requiring a new writable location or changed guard returns to
Architect-advised PO/Scrum scope reconciliation, not a silent bypass.

### Unchanged full-release design and minimal downstream join

Retain pinned Python, Microsoft Agent Framework/Foundry, Pydantic contracts,
managed-identity private Blob and PowerShell/Python/WSL tooling. Exactly three
hosted roles remain: coordinator's `begin -> route -> execute -> publish` MAF
graph calls the two remote specialists. The parent manifest creates or reuses
each role's pinned hosted/framework binding; remote `AgentSession` restoration
and specialist model-history loading provide separate continuation links.
Requirements/review revisions and response IDs advance, bindings do not.
Conversations, graph checkpoints, immutable artifacts and fenced write-ahead
effects remain independent; no generic session abstraction or rewrite is added.

Installed B remains only a specialist-local client candidate. A needs an
evidenced supported correction and its own reviewed source. The existing
scenario/source/package/version join, trusted receiver equality, exact immutable
prerequisites, ETag/fencing, Decision-1 deterministic gates and unknown-effect
holds are unchanged. No automatic fallback, opaque-call-as-user conversion,
held-parent adoption, namespace relaxation or speculative permission change.
Necessary chosen-path permissions remain pre-approved only at exact documented
scope through retained scripts and readback.

```text
designation + historical evidence + current ownership -> original ownership review
accepted ownership -> Developer runner and root/source regression handoff
accepted application + reviewed lab runner/tools -> Developer source integration
existing trust + verified context -> DevOps fresh inventory (independent of coding)
joined source -> original E2E formal scripted checks
joined source + inventory + final Linux/package gates -> DevOps guarded trial
trusted both-role selection -> original DevOps full live G1-G8 / AC1-AC9 evidence
```

The ownership reviewer handoff excludes runner writes until acceptance.
Runner doneWhen remains the deterministic runner contract below, including
pre-dispatch mismatch/preparation/competing-owner/unknown-effect negatives,
exact-response zero-send recovery, redaction and reached/unreached role results.
Integration doneWhen is exact loaded application/tool source closure plus
reviewed feature-branch task/commit accounting and preserved unrelated paths;
abandoned code stays on named branches with task/commit/reason recorded in a
feature-branch commit. Formal E2E remains local-script validation, not cloud-pass.
DevOps alone owns final Linux/amd64/Python package checks, guarded publication,
finite discriminator and subsequent live acceptance. Serialize actual
`lab-hosted-release` and `lab-private-transport` mutation resources; scheduler
names alone do not establish cross-run exclusion. No GitHub Actions or new stage.

The existing AC1-AC9/G1-G8 evidence matrix below is unchanged: real remote
collaboration; both-role two-turn continuity; controlled offline revision and
history proof; supported once-only stop/resume and separate-parent isolation;
private MI/provenance/Decision-1; honest terminal/README; final exact-source
checks; reviewed scoped push; exact final/rollback/cleanup handoff. Account-wide
Blob Contributor remains application-enforced isolation, not malicious-host or
storage-RBAC isolation. Historical UNKNOWNs, held sessions, old versions/packages
and cleanup uncertainty remain preserved. Artifact generation continues while
identity selection is unresolved; no live PASS follows from this architecture.

### Verification and owner handoff

This turn changes only this release architecture and repository navigation.
No runtime, lab source, public schema, dependency, cloud, publication, inference
or Linux hosting-package operation is performed. Current deployed/rollback
bindings remain unverified. Required local validation results are reported in
the loop handoff, scoped to this exact documentation revision, not reused from
the historical results below. Original Product Owner, Red Team and Critic
agreement remains required; this owner does not invent their votes.

## Current recovery-entry architecture (October 20, 2026)

This dated recovery-entry handoff is retained at its original link anchor.
Apply the ownership-designation overlay above for this invocation.
This section records the Architecture Loop handoff at inspected application
HEAD `3d731c00e8373774bf8254a8f060eac621d0e928`, on
`feature/customer-hosted-session-prototype`, initially clean. The older
architecture, tier contracts, accepted source and blocked release notes remain
history and retained contracts; they are not fresh execution evidence.
The supplied `priorDispositions` and reconciled feedback are empty for this
invocation. Historical originating references below identify their own bounded
acceptance, not new votes or authority for this loop.

### Decision and unchanged end-to-end design

Retain Python and the pinned Microsoft Agent Framework/Foundry Responses
implementation, Pydantic artifact contracts, Azure managed-identity private Blob
access and the existing PowerShell/Python/WSL release chain. No dependency,
framework, schema, hosting role or infrastructure change is required by this
architecture delta. The installed specialist-only B client remains a candidate,
not a live-selected repair. A remains available only as an evidenced supported
authentication/configuration correction with its own reviewed source.

The complete release remains:

```text
synthetic terminal -> same hosted coordinator parent
  -> MAF begin / gated Decision-1 route / remote execute / fenced publish
  -> same parent-owned architect child -> immutable current candidate
  -> same parent-owned reviewer child  -> exact candidate review
  -> deterministic current-reference acceptance, or revise and repeat
follow-up -> same parent and both children; fresh responses/current outputs
supported stop/resume -> same bindings, retained checkpoints/effects, no resend
separate parent -> separate children, artifact scope and requirements
```

Preserve trusted principal equality, immutable exact prerequisites and outputs,
ETag/fencing, request-local client authority, model-history continuation,
bounded calls, checkpoints and write-ahead effects. Conversations, workflow
position and artifact/effect state remain distinct. Never derive delegation
from an opaque call ID, change receiver equality to make B work, adopt held
parents or infer model memory from replayed requirements.

### Newly inspected recovery evidence: what it establishes

The supplied recovery-exception locator was used first for procedural recovery.
Read-only inspection of the three named summaries and four named connectivity/
metadata receipts establishes the following **historical** evidence:

- `publication-summary.json` reports one successful coordinator 22 -> 23
  diagnostic publication, unchanged identity and newly owned cleanup. It
  explicitly preserves the original publication UNKNOWN.
- `diagnostic-summary.json` binds matching outbound opaque context, absent
  trusted architect user and `NATIVE_HOST_PRINCIPAL`, with the operation held.
  Reviewer entry was not reached; the mixed diagnostic bundle is not final.
- All four named receipts report independently accepted fingerprint matching
  the existing entry and closure of their own jobs/listeners. This supplies an
  inspectable historical trust/closure locator, not a new fingerprint, current
  host verification, module-path attestation or original-publication cleanup.
- Loading the existing native settings **only** through `Use-Settings.ps1`
  passed local schema validation. Local comparisons passed lab-root/region/
  registry tenant/subscription linkage, the attempt's project linkage and all
  four receipts' tenant/subscription/origin linkage, without displaying values.
  No authenticated Azure context, active versions or effective grant was read.

Keep private paths, receipt contents, principals and full session identifiers
outside this repository. The workflow handoff carries exact private locators.
Receipt claims are not independently authenticated by these local comparisons.
The historical `further_dispatch_or_inference_authorized=false` and consumed
single-attempt authorization do not override the newer user-approved run;
neither does the newer authority close historical unknown effects.

### Observed root compatibility and implementation boundary

Read-only Git inspection found:

| Checkout | Observed branch / HEAD | Meaning |
|---|---|---|
| Canonical lab | `feature/swc-think-fast-aca-dns` / `63348876535de7c264dc1e9139bb6fd2684b0052` | Six modified and two untracked paths remain unrelated, unadopted and untouched |
| Existing registered sibling | `feature/customer-hosted-session-prototype` / `bdd6b2a491ecbe0fc3b7570b86f297ac00bd2703` | Clean at inspection; registration and branch name do not prove exclusive writing ownership or runner implementation |

Both actual resolver implementations were read and exercised without mutation,
authentication, package creation or network calls. Each loaded resolver was
tested with the application and each lab root:

| Resolver loaded from | Supplied lab root | PowerShell result | Python result |
|---|---|---|---|
| Canonical lab | Canonical lab | Pass | Pass |
| Canonical lab | Sibling | `LAB_TOOL_OWNER_MISMATCH` | `LAB_TOOL_OWNER_MISMATCH` |
| Sibling | Canonical lab | `LAB_TOOL_OWNER_MISMATCH` | `LAB_TOOL_OWNER_MISMATCH` |
| Sibling | Sibling | Pass | Pass |

All eight expected outcomes passed. Python ran with `-B`; no resolver global
was patched and no settings or path guard was changed. This is actual local
resolver execution, not just source inspection. It proves a source/root pairing
constraint, **not** writer exclusivity, cloud-profile compatibility, full runner
integration or permission to execute effects from the sibling.

**Architecture decision:** do not pass the canonical operational lab root to a
sibling-owned wrapper (or vice versa), and do not weaken `LAB_TOOL_OWNER_MISMATCH`.
Keep the canonical operational context and any separately assigned writable
tooling checkout explicit. A runner developed in the sibling can orchestrate
canonical retained wrappers only as an explicit separate invocation rooted in
their own canonical lab. The reviewed runner/tool revisions and source hashes
must be joined before execution; sibling changes to wrappers are not installed
canonical changes. If the required wrapper delta is absent at the operational
root, integration is incomplete and effects must not start.

Alternatively moving execution to the sibling would require proof that every
retained profile, registry, settings, stage and source-owner guard remains
compatible. This document does not choose that unproven move or authorize copying
credentials/settings, changing CLI profiles or switching a shared branch.
The smallest current path is explicit runner-to-existing-operational-wrapper
composition, with existing guards intact, not a third root abstraction.

The historical stopped task reference is
`["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-LAB-OWNERSHIP/AssignedWorkDeveloperLoop","lab-ownership-review-evidence-access"]`.
The current user's explicit read-only Git/sibling-resolver approval permits
the observations above; it does not retrospectively mark that task complete,
restart its writes, supply a missing original review or supersede an accepted
handoff. Scrum reconciles this new evidence through the existing original
owners/reviewers. Do not redispatch accepted candidate, continuity, UX or
assertion work. No new user approval is needed for the already authorized
bounded inspection, and no new approval stage is introduced.

### Minimal closing work for original planning and execution owners

These are concrete handoff contracts; ReleasePlan/Scrum owns task IDs,
assignment, minimal edges and Git reconciliation.

| Owner / boundary | Done when | Exclusions / handoff |
|---|---|---|
| Developer / Scrum: checkout ownership | Reconcile the observed sibling branch/HEAD/status and both resolver matrices with actual point-in-time writer ownership; original reviewers can inspect the bounded evidence | Registration alone is insufficient; no write probe, worktree recreation, branch switch or restart of the stopped task by inference |
| Transport owner / DevOps: existing trust | Consume the named historical trust receipts; locate the already approved owner module/source and fingerprint through the existing bounded inspection mechanism, verify current exact hashes and strict trust before Metadata | Historical `host_trust` text is not a fingerprint/module path; do not generate replacement trust, scan credentials or treat new cleanup as historical closure |
| Developer: retained runner | Implement/review deterministic local runner against the existing decision-runner contract, explicit matched wrapper roots and fail-closed source/scenario/package/version join; include root mismatch and unknown-effect negatives | Coding waits for writing ownership, not cloud inventory; no automatic fallback, public event/schema change, live claim or second evidence ledger |
| Integration owner / Scrum | Join reviewed application/runner/wrapper revisions, account for drift, preserve unrelated work and record scoped task commits/retained branches on the feature branch | Do not assume sibling wrapper commits are installed at canonical root; no broad commit or shared-checkout branch switch |
| Original E2E | Run formal checks on the exact joined implementation through local scripts, including retained assertion and root mismatch cases | Accurate predeployment FAIL is allowed; architecture probes are not formal E2E or release PASS |
| Original DevOps | Fresh verified sole-target inventory/grant/rollback/unknown readback, exact-source/Linux/common-package gates, guarded publication and finite trusted ingress discriminator; then full live G1-G8 if selected | No unchanged-A experiment, held-parent resend, speculative grant or repeated uncertain stop/publication |

Application preparation/assertion work can continue independently of lab
ownership and transport. Trust plus verified context enables fresh read-only
inventory independently of runner coding. Reviewed source integration and fresh
inventory join before publication/trial; only a demonstrated necessary grant
adds scripted exact-scope plan/write/readback. All actual cloud effects stay
with DevOps. Formal integration stays with E2E. Scheduler resources
`lab-hosted-release` and `lab-private-transport` serialize their corresponding
publisher/profile/mount effects but do not create cross-run OS isolation.

The finite trial must still observe architect trusted entry and receiver
success before reviewer, preserving reached/unreached distinctions. B's
principal namespace compatibility and effective permission remain unresolved.
An observed mismatch returns to this Architect-advised PO/Scrum process; no
namespace bypass is preapproved. Unresolved selection does not block remaining
release/planning artifacts. Provider action is required only for a specific
supported remedy that cannot be resolved within the authorized alternatives;
case submission/private disclosure remain excluded.

### Acceptance, evidence categories and owner completion

The existing AC1-AC9 matrix below remains binding: real collaboration and
two-turn continuity; controlled offline revision/history proof; once-only
supported recovery and separate-parent isolation; full private MI/provenance/
Decision-1 G1-G8 gates; truthful human terminal/README alongside unchanged
machine evidence; final-source application/repository/retained/Linux checks;
reviewed scoped feature-branch push; and exact final/rollback/cleanup handoff.
Account-wide Blob Contributor still means application-enforced ownership and
isolation, not malicious-host or storage-RBAC separation.

This turn supplies local recovery-entry evidence and an executable-root
boundary, not identity-path selection or customer-ready delivery. It makes no
cloud mutation, deployment, inference, Linux-package or live acceptance claim.
Exact current deployed/rollback versions remain unknown. The completeWhen for
this Architecture Loop still requires original Product Owner, Red Team and
Critic agreement on the committed architecture; none is fabricated by the owner.

Local verification for this delta used the existing absolute validated Python
3.12.10 executable and explicit canonical lab root: `Test-Demo.ps1` passed
dependency checking, **204 offline tests in 47.776 seconds**, and compilation.
`scripts/Test-Repository.ps1` passed index, **78 public files**, JSON/PowerShell/
context and whitespace checks. The architecture's relative links/anchors and
AC1-AC9/identity/root contract checks passed. No dependencies were installed.
No lab source changed, so the full retained lab suite was not rerun; the eight
resolver observations above are bounded read-only checks, not that suite or a
Linux hosting-package gate.

## RP-S3 retrospective: assertion correctness is not observation provenance

The [RP-S3 retrospective](customer-prototype-release-plan.md#rp-s3-retrospective--offline-proof-and-unreached-live-outcomes)
consumes accepted assertion commits `dcdb5e4` and `552e466`; it does not reopen
their implementation acceptance. The repaired join binds each final artifact
to exactly one current producing operation and identical ordered `input_refs`.
Consistent negative fixtures must change cumulative transitions together while
preserving valid artifact envelopes, so rejection exercises the intended join
rather than unrelated malformed evidence. Retain the legitimate revision and
JSON round-trip controls.

Passing these assertions proves consistency of supplied observations, not their
collection, authenticity or live origin. Integration consumes the accepted
executable/private-input contract, revalidates source drift and joins the reviewed
runner; original E2E validates exact joined revisions. DevOps separately supplies
actual private observations and exact-source/Linux/package/version provenance.
An accepted prerequisite FAIL supplies neither integration readiness nor a
completed non-held initial parent. Actual G1-G4 entry remains necessary for
continuity and independently for isolation; supported recovery additionally
requires verified two-turn completion.

Keep ownership/root evidence and established transport trust as independent
stopped lanes. Preserve the originating stop and runner-writing block under
`["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-LAB-OWNERSHIP/AssignedWorkDeveloperLoop","lab-ownership-review-evidence-access"]`.
No new collector, ledger, public field, identity rule or approval stage is
introduced. Trusted receiver equality, checkpoints, fencing and UNKNOWN-effect
holds remain unchanged.

## RP-S2 retrospective: evidence joins remain independent

The [RP-S2 retrospective](customer-prototype-release-plan.md#rp-s2-retrospective--stopped-prerequisites-and-evidence-delivery)
retains accepted architecture, not a new identity or release contract. Application
preparation at `990467a` is an accepted independent handoff; its local tracking-ref
audit does not prove remote freshness or joined runner readiness. Integration
must revalidate drift and join reviewed application/tooling revisions before
formal E2E, followed by exact Linux/package gates in DevOps.

Keep two explicit prerequisite lanes: Developer/Scrum supplies the stopped
ownership/root evidence for original Architect/Critic inspection; existing
transport-owner/Scrum coordination supplies established private trust evidence
to DevOps. Neither approval of source nor agreement with a blocked assessment
substitutes for either lane. Preserve the originating five-round stop and
runner-writing block under
`["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-LAB-OWNERSHIP/AssignedWorkDeveloperLoop","lab-ownership-review-evidence-access"]`.
No unattended verification restart, replacement trust or new approval stage is
introduced. Scenario/source/package/actual-version consistency still precedes
parent creation; trusted receiver equality and unknown-effect holds are unchanged.

## RP-S1 retrospective evidence boundary

The [RP-S1 retrospective](customer-prototype-release-plan.md#rp-s1-retrospective--evidence-handoffs-and-truthful-closure)
improves operational handoffs without reopening the accepted architecture.
Source-contract approval, safely owned tooling checkout, authenticated transport
and live ingress are distinct facts. A reported checkout or inspected resolver
source is not proof of sibling execution or point-in-time writing ownership.
Retain the stopped ownership assignment until its original reviewers can inspect
the bounded evidence specified in
`["yaml-loops-v1:sprint/1/RP-S1/task/RP-S2-LAB-OWNERSHIP/AssignedWorkDeveloperLoop","lab-ownership-review-evidence-access"]`.
Do not repeat denied probes, recreate the worktree or unblock runner writing
through an architecture approval. Existing Developer/Scrum coordination owns
that handoff; existing DevOps separately obtains established private transport
trust and fresh inventory. Neither blocks independent application source review.

The scenario/source/package/actual-version join remains required before trial
creation. No identity namespace, receiver equality, resource lifecycle, dependency
edge or release gate changes here. Architecture agreement under
`["yaml-loops-v1:ArchitectureLoop","architecture-close-agreed-deliverable"]`
remains closed within its original boundary; it supplies no new live evidence.

## Scope and authority

This is the Architecture Loop handoff for the October 19, 2026 customer prototype.
The outcome is a hosted coordinator repeatedly invoking the same two remote
specialists within one parent conversation, not a new orchestration system.
It complements [design.md](design.md) and the measured history in
[identity-recovery-plan.md](identity-recovery-plan.md). It does not assert
deployment, live acceptance, or reviewer agreement.

The run's supplied customer specification is the release acceptance source.
`docs/requirements/{coordinator,specialists,client-release}/architecture.md`
now contains derived logical-tier contracts, not replacement requirements.
Do not invent requirements or copy private delivery control-plane inputs into
this repository.
The October 19 invocation authorizes scoped application/release-tool changes,
reviewed feature-branch delivery, guarded publications to the existing three
roles, synthetic tests, supported hosted compute stop/resume, the existing
read-only SSH mount, and starting the existing registered command VM if needed.
Older documents' consumed single-diagnostic authorization describes history,
not the entirety of this run's authority. Conversely, this run does not reconcile
the old UNKNOWN publication, authorize a held-parent resend, or permit speculative
identity changes. The additional October 19 path-selection and permission
approval permits either supported authentication-configuration correction or
`x-ms-user-identity` delegation, including necessary scoped RBAC/permission
changes in this lab. This narrow exception replaces this document's earlier
blanket permission prohibition, not its identity checks or release gates.
No new infrastructure, quota, network, DNS, VPN, provider submission, new
service, or alternate project is in scope. Do not replace existing identities
merely to obtain a different caller.

## Current source-to-trial decision (October 20, 2026)

This owner inspected clean application HEAD
`3aca5dc236695c5ec7eac98d0cd03bced40da7b8` on
`feature/customer-hosted-session-prototype`. The isolated runtime candidate is
now implemented there; the earlier baseline sections below are historical.
`WorkflowRuntime.resources()` unconditionally builds B's specialist-only
headers/client for this source. The original six-resource tuple still exposes
opaque-only authority to non-specialist callers. No runtime A/B selector exists.
Installed source is **not** live selection: principal compatibility, effective
permission and both specialist receivers remain unmeasured in this turn.

### Source identity is part of the scenario contract

The required runner's scenario label must describe the actual reviewed source,
not configure behavior that this runtime cannot select:

| Trial | Required source/package join | Fail-closed result |
|---|---|---|
| `B-candidate` | Reviewed `3aca5dc` candidate or its reviewed descendant, integrated with the lab runner, then exact-source Linux/common-package/version closure | A pre-candidate package is not B even if the runner labels it B |
| `A-correction` | A separate reviewed source revision containing a concrete supported opaque-path correction, with its own regression and package/version closure | Current unconditional B source cannot be relabeled A; unchanged historical A is not a correction |
| Existing held parent or unknown operation | Retain its original exact source/version/session binding and inspect only known effects | Neither scenario adopts it, changes its identity namespace or sends again |

This is an input-consistency rule for retained local runner/preflight tooling, not a
new receipt protocol, runtime selector, acceptance ledger or approval stage.
Reject mismatched scenario/source/package/actual-version joins before creating
a trial parent. Record the mismatch without dispatch. If A becomes the smallest
evidenced repair, implement it as ordinary reviewed source through the existing
Developer/DevOps loops; do not silently toggle a private environment variable,
edit a sealed stage or switch the shared checkout to an old revision.

The candidate's guards run while resources are constructed, before remote
dispatch. A missing/invalid captured user, full-scope mismatch or forbidden
header is therefore a **local preparation rejection**, not evidence of remote
ingress absence or a denied permission. Only an observed child result can
classify child receiver failure. An absent observation remains unknown.
Keep these distinctions in existing sanitized decision outcomes; no raw identity
or header values belong in the public report.

### Current ownership and readiness join

The existing SprintPlan at `4f2e02d` assigns
`RP-S2-DECISION-RUNNER` to **Developer**, after
`RP-S2-LAB-OWNERSHIP`; DevOps retains inventory, package/publication and the
live trial. This supersedes only the earlier architecture's suggested coding
owner, not the runner contract or DevOps execution ownership.
`RP-S2-ISOLATED-CLIENT` has implementation commit `3aca5dc`; retain it for
original review/integration, without redispatching candidate or RP-S1 UX/
continuity work. This turn does not assert that its task reviews are accepted.

The current minimal join is:

```text
lab writing ownership -> Developer runner ------------------+
implemented B source -> original review -------------------+-> source integration
fresh inventory (DevOps, independent) --------------------------+
source integration -> final-source/Linux/package gates --------+-> DevOps trial
```

Source integration must cover the reviewed application commit and reviewed
lab-tool commit on their authorized feature branches. Existing lab checkout
`feature/swc-think-fast-aca-dns` and its unrelated dirty files remain untouched
here. Establish safe lab writing ownership rather than switching it underneath
another writer. An evidenced permission delta adds only its own scripted
plan/write/readback edge. Scheduler resource names do not provide OS exclusion.

The lab file inventory inspected here contains retained App/Observe and
publisher tooling but no new decision-runner entry point. That does not prove
no task exists on another worktree; require the actual named commit/entry point
at integration, not a guessed command. Before the finite live trial, DevOps
must demonstrate scenario/source mismatch rejection, pre-dispatch preparation
failure, competing owner, unknown effect hold, exact-response zero-send
recovery, redaction and partial-role outcomes in the retained runner tests.
Architect success alone leaves reviewer unverified. All original AC1-AC9 and
G1-G8 remain downstream and unchanged; this architecture makes no cloud claim.

### Local verification of this source-to-trial update

Using the existing absolute validated Python 3.12.10 executable and explicit
lab root, `Test-Demo.ps1` passed dependency checking, **192 offline tests in
23.678 seconds** and compilation. `scripts/Test-Repository.ps1` passed index,
public-boundary (**74 public files**), JSON, PowerShell, context and whitespace
checks. No dependency installation or runtime change was needed. These repeat
local checks are not new live progress or selection of B.

No settings import, authenticated cloud query, permission change, deployment,
inference, Linux hosting-package gate or release acceptance was performed in
this architecture turn. Lab sources were not changed; the retained full lab
suite was not rerun. Original Product Owner, Red Team and Critic review of this
delta remains required; owner documentation does not assert their agreement.

## Previous architecture decision and inspected baseline

The preceding architecture revision started from application commit
`24b883f910dedbc8dc524177f29f59e061be265e` on
`feature/customer-hosted-session-prototype`, with a clean application worktree.
The previous RP-S1 source/clarity integration is retained, not reopened:
`6614440` added workflow continuity fixtures, `c454e50` added direct specialist
continuation fixtures, `56b762e` added the opt-in terminal view, and `24b883f`
integrated the reviewed source and runnable README. These are implementation
history, not freshly verified live capability or new work credited to this loop.
The lab remained on its existing unrelated feature branch with pre-existing
dirty work. This architecture turn makes no lab edits or branch changes.

No prior dispositions or reconciled feedback were supplied for this invocation.
The new user approval, rather than a newly inferred permission or an older
research task's exclusions, governs identity-path evaluation below.

**Decision:** retain the complete three-role architecture and its current
contracts. Evaluate the smallest supported correction first; permit explicit
delegation as a real alternative, not an already-proven repair. Neither path
has demonstrated successful specialist ingress in this turn. Continue release
and sprint artifact generation while selection is unresolved. Do not declare
a provider-only stop solely because the previous opaque-context research was
unresolved: the newly authorized delegation alternative must be assessed too.
Formal E2E validation stays in the End-to-End Test Loop; deployment and
cloud-pass stay in the DevOps Work Loop. Architecture/planning can run bounded
decision tests, but cannot promote their results to those acceptance gates.

### Verification of the preceding architecture revision

Using the existing validated absolute Python 3.12.10 executable, without
installing dependencies:

- `Test-Demo.ps1 -Python <absolute-validated-python> -LabRepositoryRoot
  <explicit-lab-root>` passed dependency checking, **177 offline tests in
  23.705 seconds**, and compilation.
- `scripts/Test-Repository.ps1 -Python <absolute-validated-python>` passed
  index, public-boundary (**70 public files**), parser and whitespace checks.
- Local documentation checks verified 11 relative links/anchors and the
  presence of AC1-AC9 and the identity-selection handoff fields.

No retained lab source changed, so its full release suite was not rerun.
Linux hosting-package checks, live identity-path selection, deployed/rollback
inventory and formal release acceptance were not executed. Original Product
Owner, Red Team and Critic agreement is not asserted by this owner handoff.

## October 20 architecture delta: executable candidate boundary

This Architecture Loop inspected clean application HEAD
`bb1743d85cb10e6520c92efaa42df0702178f57a` on
`feature/customer-hosted-session-prototype`. The lab remains on
`feature/swc-think-fast-aca-dns` with unrelated dirty work; this turn neither
changes that branch nor edits lab files. The integrated
[`identity-candidate-handoff.md`](identity-candidate-handoff.md) adds nine
offline probes in `13203ac`, reconciled by `bb1743d`. Its current executable
has **no live mode** and intentionally returns exit 2 with unresolved selection.
Neither that command nor this architecture executes a hosted B candidate.

At that inspected baseline, the handoff identified a concrete implementation gap:
`WorkflowRuntime.resources()` supplied one `ProjectClient`/header set
to both `WorkflowRemoteAgents` and non-specialist operations. Runtime candidate
installation and a journaled live decision runner are absent. Resolve that
internal design gap here rather than sending the same unresolved research
back to Scrum without an implementation contract.

**Architecture decision:** retain A as the existing opaque-call baseline.
Prepare B as a reviewed, exact-source candidate with a separate specialist-only
project/header client. This is permission to design/assign the candidate, not
selection of B, a claim that parent-derived delegation preserves namespace, or
authority to weaken the receiver. No new framework, schema, deployed role,
user approval stage or infrastructure is introduced. The existing public
delegation references and caveats below still apply.

### Request-local client ownership and unchanged trust

Within the existing `WorkflowRuntime.resources()` `AsyncExitStack`:

1. Keep the original managed-identity credential, exact-origin/no-retry HTTP
   transport and opaque-only project/header resources for routing, model,
   parent/history/checkpoint and other non-specialist uses. Keep the yielded
   resource tuple's meaning/order so callers need no orchestration rewrite.
2. For the B candidate, construct a distinct `ProjectClient` with a **copied**
   specialist header dictionary and a separate OpenAI-client cache. Sharing
   the request-owned credential/HTTP transport is permitted; client lifecycle
   tests must prove cleanup does not invalidate another client while in use.
   Do not mutate `project.call_headers`, SDK ambient context or a shared dict.
3. Derive B's user exclusively from captured authenticated hosting context.
   Revalidate the full `ScopeBinding.from_platform(...)` against the runtime's
   scope before constructing delegated headers. Apply the offline candidate's
   syntax, missing-user, unexpected-header and call-ID-substitution guards.
   Move only the needed pure logic into runtime-owned source; hosted code must
   not import a script/test runner. Never forward `x-agent-user-id`.
4. Give only `WorkflowRemoteAgents` the specialist project/header pair.
   Preserve unchanged opaque-call forwarding alongside B's delegated header.
   Cover metadata/prepare, create, check, ambiguous-create inspection, send
   and exact-response retrieval. Raw Azure SDK explicit headers and Responses
   default headers are separate paths and both require assertions.
5. Do not change `Assignment.validate_receiver()` or specialist history/storage
   construction. The actual child principal must still match the parent's
   trusted principal and all existing scope/version/prerequisite checks.
   Principal absence or namespace change fails the candidate, even if hosting
   returns HTTP 200 or a response can be retrieved.

No new runtime selector is required by this design. Bind an explicitly named
B trial to its reviewed source commit/common package/three target versions in
the private decision record; do not infer a path from errors or switch paths
automatically. The existing bundle retains A until a candidate is deliberately
published by DevOps. If downstream work instead needs a configuration selector,
its source/settings/package closure is an explicit Architect/Scrum delta,
not an undeclared environment variable outside retained settings validation.

Old pinned sessions remain on their old bindings/versions. Do not adopt any
existing held parent, translate its principal/history or attach old children
to the candidate. The candidate starts a fresh synthetic parent. A failed
trial is retained as failed/held evidence; rollback versions and immutable
packages remain available. A later final release may use B only after trusted
ingress selection and full release gates; no old-state migration is implied.

### Deterministic decision runner contract

The assigned Developer supplies the local, lab-owned runner using retained
wrappers; original DevOps executes it. This section defines required behavior,
**not an existing command**. Formal E2E and deployment/cloud-pass ownership
do not move. The current source/scenario join above also applies.

| Input / stage | Required behavior |
|---|---|
| Invocation | Explicit absolute application/lab roots, existing validated Python, scenario (`A-correction` or `B-candidate`), exact reviewed source/package/role-version bindings and private evidence destination outside both repositories |
| Preflight | Load only `Use-Settings.ps1` with the existing native settings; verify sole-target linkage and dedicated authenticated tenant/subscription; join fresh inventory, actual caller/effective action and rollback records. Declared versions from the offline runner are not inventory. |
| Mutation ownership | One owner for `lab-hosted-release` and `lab-private-transport`; journal exact intended effect/bindings before dispatch. Serialize actual publisher/CLI/mount use, including across workflow runs; scheduler labels alone provide no OS exclusion. |
| Publication | If a new candidate bundle is needed, use reviewed source checks, actual Linux/amd64/hosting-Python gate, immutable stage, fresh preview and retained publisher. This is original DevOps work, not an architecture deployment shortcut. |
| Finite trial | One fresh parent; attempt architect first, then reviewer only after trusted architect entry/receiver success. Record the finite intended role calls before starting. Routing/model calls retain existing admission/deadline budgets. A needs a measured supported correction; do not trial unchanged A again. |
| Observation | Privately bind exact actual role/version/parent/child/framework/response and artifact scope; publicly expose presence/match/entry classifications only. Verify the receiver passed, not only nonempty ingress identity. Coexistence of opaque and delegated headers remains a measured question. |
| Failure/recovery | Stop on missing/changed principal, version drift, receiver rejection, unknown create/send or held effect. Retrieve a known exact response only; never create/send again to obtain a missing receipt. Preserve absent evidence as unknown rather than negative proof. |
| Result | `selected-A`, `selected-B` or `unresolved`; actual tests and evidence kind, principal compatibility for each reached role, private locators, permission delta/readback, holds, cleanup and next closing action. Report unreached reviewer explicitly. A successful architect discriminator alone is not three-role collaboration. |

Reuse existing assignments and exact immutable prerequisites for the trial.
Do not invent an unprotected diagnostic endpoint, ask the model to assert its
identity, bypass Blob validation or add a second acceptance ledger. If retained
App/Observe modes cannot express the finite decision sequence safely, extend
them with targeted lab regressions rather than improvising external commands.
Unknown effect records must be inspectable without dispatch. Missing permission
is a conditional delta, not an assumed prerequisite: read back the existing
explicit grant before planning any scoped write.

### Minimal downstream delta and stop conditions

Scrum Master owns actual task IDs, assignments and Git reconciliation. The
following bounded contracts refine the existing release plan, not replace it:

| Delta / original owner | Done when | Hard handoff / exclusions |
|---|---|---|
| Isolated B runtime / Developer | Exact-source candidate wires specialist-only clients; real resource-factory tests prove both-role lifecycle headers, unmodified non-specialist context, cleanup, trusted binding negatives and known-response zero-send recovery; complete application/repository checks pass | Uses integrated offline handoff; excludes deployment, namespace relaxation, dependency migration and duplicate continuity/UX implementation |
| Fresh inventory / DevOps | Sole-target active/rollback package/version/identity/protocol, actual caller/effective explicit action and unresolved operation records are current and privately bound | Independent of runtime coding; no assumed missing grant or mutation from metadata alone |
| Decision tooling / assigned Developer | Retained local runner implements the table above; offline failure/unknown/ownership/redaction fixtures and affected retained suite pass | Runner coding can parallel runtime coding against this contract; live execution remains DevOps and waits for inventory plus reviewed candidate/source/Linux/package gates |
| Bounded ingress decision / DevOps | Execute the finite trial under existing authority and record selected/unresolved with receiver evidence for each reached role | No formal acceptance credit; stop on held/unknown work. Unsupported namespace requires an explicit end-to-end authenticated design through Architect-advised PO/Scrum, never an equality bypass. |
| Integration / Scrum-assigned owner | All reviewed task commits are on the authorized feature branch, or named retained branches/commit IDs/reasons are recorded in a feature-branch commit; exact integrated source rechecked | Do not switch a shared lab checkout underneath other work; establish its feature branch safely before writing, or use a separate branch/worktree with explicit integration ownership |

Only an evidenced required permission delta introduces its corresponding
scripted plan/write/readback dependency. A genuine unavailable platform remedy
can stop execution with an actionable external finding; unresolved candidate
research alone does not stop remaining artifacts. Continue ReleasePlan and
SprintPlan outputs even while selection is unresolved. Original AC1-AC9 and
G1-G8, including final common bundle, two-turn/revision/continuation evidence,
private MI provenance, stop/resume, isolation, truthful terminal and closeout,
remain unchanged. Do not redispatch the already integrated RP-S1 fixtures/UX.

The owner considers this conditional end-to-end design ready for the original
Product Owner, Red Team and Critic review. Their agreement and live feasibility
are not claimed by a documentation change.

### Verification of the October 20 delta

Using the existing absolute validated Python executable and explicit lab root,
`Test-Demo.ps1` passed dependency checking, **186 offline tests in 23.995
seconds**, and compilation. `scripts/Test-Repository.ps1 -Python
<absolute-validated-python>` passed index, public-boundary (**73 public files**),
JSON, PowerShell, context and whitespace checks. A targeted local check passed
the architecture contract fields and all three relative links/anchors.
No dependencies were installed and no runtime source changed.

These are local source/document checks, not newly credited continuity proof.
No cloud inventory, settings import, permission readback/write, inference,
publication, Linux hosting-package check or live acceptance was performed.
No lab tool changed, so the retained full lab release suite was not rerun.
The remaining executable candidate/runner and all live gates are explicitly
downstream; historical unknowns and unrelated dirty work are untouched.

## Principles, framework and tools

- Retain the existing explicit execution order and role-local five-stage flows.
  No architecture rewrite, generic session manager, framework replacement, browser
  UI, fourth hosted service, or line-count-driven splitting.
- Use Python, Microsoft Agent Framework, Microsoft Foundry hosted Responses,
  Pydantic contracts and Azure managed-identity Blob adapters already in this
  repository. Keep `requirements.txt` / `requirements.lock.txt` pins; change them
  only for an evidenced compatible remedy with held-state implications reviewed.
  Current direct pins include MAF core 1.21.0, Foundry integration 1.14.0,
  hosting 1.0.0b261002, agentserver Core 2.2.0 and Responses 2.3.0.
- Keep Microsoft-Decision-1 for bounded semantic coordinator choices after
  deterministic gates. It is a model deployment, not another hosted agent.
- Use retained PowerShell/Python/WSL build, Linux package, preview, publication
  and connectivity tools from the linked lab with explicit application/lab roots.
  No direct mutation shortcut or runtime/control-plane replacement.
- Test behavior and provenance, not success-shaped text. Offline fixtures,
  Linux package validation, deployed metadata and live acceptance are distinct
  evidence categories and must remain distinguishable in every report.

## End-to-end call and state design

```text
terminal user turn -> Foundry coordinator parent P
                       MAF begin -> route -> execute -> publish -> route ...
                                             |
                         +-------------------+-------------------+
                         v                                       v
                  remote architect A(P)                  remote reviewer R(P)
                  own model history                      own model history
                         |                                       |
                  immutable candidate                  immutable exact review
                         +----------> coordinator acceptance <---+

second user turn -> same P -> same A(P), R(P); new response IDs and revisions
separate parent Q         -> different A(Q), R(Q) and artifact namespace
```

These are exactly three deployments, not three conversations globally.
Every parent has its own two child bindings. Architect/reviewer calls are causal:
the reviewer needs the accepted current candidate; it cannot run speculatively
in parallel with its producer.

### Source trace and continuity contract

1. `demo/host.py` configures the request-aware `create_workflow` / `parse_turn`
   entry points, `CheckpointStoreProvider` and resilient background hosting.
   The descriptor's `DEMO_RUNTIME=native` and remote specialist configuration
   remain technical configuration names; presentation cleanup must not silently
   rename runtime options or diagnostic codes.
2. `WorkflowRuntime.begin()` in `demo/workflow.py` binds trusted parent scope,
   persists the new requirements revision, invalidates candidate/review approval,
   and retains the parent's manifest children. It must preserve earlier user
   requirements when appending the asynchronous-queue follow-up.
3. `route()` enforces readiness, pending-effect, deadline and budget gates,
   then records a genuine validated Decision-1 choice where needed.
4. `execute()` looks up `manifest.children[role]`. Only a missing role prepares
   a new `ChildBinding`. `RemoteAgents.prepare()` in `demo/foundry.py` prepares a
   framework `AgentSession`, hosted session ID and pinned deployed version.
   The manifest journals creation before `create_session`. Ambiguous creation
   recovers that exact ID; it must not generate another child.
5. Every invocation validates the stored hosted binding and version.
   `RemoteAgents.invoke()` restores `AgentSession.from_dict(child.framework)`
   and passes that session to the remote client's `run`. It records the new
   response ID immediately and retains the updated framework representation.
   Recovering a known response retrieves it for the same hosted session and
   advances the continuation without another send.
6. Each specialist's `load_or_create_llm_session()` restores `"history"` from
   `AgentSessionStoreProvider(store_name="specialist_history_v2")` in its
   hosting context. Its model-generation stage receives that restored session;
   model pending-operation state records input digest, deployment and response.
   `store_design()` / `store_review()` writes the immutable artifact, clears the
   completed pending operation and persists history. The hosting response ID
   and the internal model-response continuation are different identities.
7. `publish()` validates exact input references, schema, scope, producer
   role/session/version/response, content hash and current revisions before
   fenced/ETag manifest acceptance. An old approval cannot approve new requirements.

The stable contract is parent hosted identity, both children hosted identities,
both framework session identities and pinned versions. Serialized framework
state is not wholly immutable: response continuation must advance. Compare stable
identity fields separately from evolving service-response IDs/state. New
invocations require new response IDs; retrieval of the same known response does
not. Never equate safe display aliases, repeated full requirements or plausible
memory text with actual session continuation.

### Three independent state concerns

| Concern | Durable owner and purpose | Not a substitute for |
|---|---|---|
| Conversations | Parent hosting state, child binding framework dictionaries and specialist model history | Artifact provenance or authorization |
| Workflow position | MAF hosting checkpoints with stable executor IDs | Remote-effect outcome reconciliation |
| Artifacts and effects | Private Blob scope, immutable prerequisites/outputs, manifest and write-ahead journal | Framework/model conversation history |

Use existing `demo/artifacts.py` and `demo/contracts.py` schemas, not a second
protocol. Assignment/output locators are version 1. Typed assignments bind
trusted scope, exact prerequisite refs, operation, expected producer, revisions,
permitted output and deadline. The model cannot select scope or write authority.
Specialists write only their immutable proposals; the coordinator alone accepts.
Creation uses immutable writes; acceptance uses ETag/fencing. A publication
conflict causes reconciliation, not another specialist call.

## Identity and recovery boundaries

Foundry trusted project/tenant/principal/parent binding is mandatory.
The pinned `context.platform_headers()` forwards the opaque call context; it
does not authorize copying the container user header or deriving authority from
an assignment body. Keep exact-origin transport, no automatic effect retry,
private-path checks, bounded calls, managed identity and sanitized diagnostics.

Historical evidence, not a fresh observation in this architecture loop, shows
matching outbound opaque call context and missing trusted user at the architect,
failing `NATIVE_HOST_PRINCIPAL` before specialist application execution.
The older public supported-remedy assessment found no cause-specific correction;
neither a platform defect nor missing grant is established. Downstream work may
research current public supported contracts and reproduce a concrete SDK defect.
It may implement a supported scoped correction with a failing-before regression.
Do not republish the same speculative change or label identity repair verified
without actual successful remote execution.

### Supported identity alternatives and selection contract

Public sources checked for this revision:

| Source | Observed revision / applicable fact |
|---|---|
| [Hosted runtime contract](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agent-contract#platform-request-headers-container-protocol-200) | Source `69a226754528e8d4d032ec652eba7d82e584f648`, updated September 28, 2026: container protocol 2.0.0 forwards the opaque call ID unchanged to other agents; the injected user header is container-only. |
| [Per-user isolation and delegation](https://learn.microsoft.com/azure/foundry/agents/how-to/isolate-sessions-per-user#isolate-sessions-for-your-own-users) | Source `f5104405dfd0231d706f8198fb841f45826595b9`, updated October 13, 2026: `x-ms-user-identity` is a supported trusted-service contract; value is a stable authenticated end-user identifier, 1-256 permitted characters, not a call ID. Delegated-session access is not fenced between delegated users. |
| [Hosted agent permissions](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agent-permissions#delegate-the-end-user-identity) | Source `bd74da57b5293b70e0538b76b75d983ab2e67d80`, updated September 23, 2026: delegation requires the explicit `Microsoft.CognitiveServices/accounts/AIServices/agents/endpoints/UserIdentityImpersonation/action` data action, not a built-in role or wildcard assumption. |

The installed Core 2.2.0 `platform_headers()` was inspected again: it emits
only `x-agent-foundry-call-id`; it does not send a delegated or container user.
The existing offline diagnostic returned `OFFLINE_VERIFIED_LIVE_UNRESOLVED`
(intentional exit 2). Settings were loaded solely with `Use-Settings.ps1`;
local schema and expected lab linkage passed without displaying values.
These are local observations, not authenticated cloud-context validation.
No cloud version/permission readback, inference, permission mutation or
publication occurred in this architecture turn.

| Path | Smallest admissible change | Selection evidence / rejection condition |
|---|---|---|
| A: agent-to-agent authentication/configuration correction | Preserve existing Responses transport and unchanged opaque-call forwarding. Correct only a measured endpoint, protocol, effective-caller permission or supported authentication configuration mismatch. Here agent-to-agent is the interaction, not a requirement to introduce a new A2A wire protocol. | Fresh exact bindings and relevant effective permissions establish the mismatch, then a bounded synthetic invocation reaches the specialist with trusted context and passes existing receiver checks. HTTP 200, health, permission presence or another identical opaque-header publication do not select A. |
| B: explicit `x-ms-user-identity` delegation | Use the existing authenticated coordinator as the trusted middle tier for the two specialists. Derive the identifier exclusively from authenticated server-side user context; validate its permitted syntax and stability. Never derive it from `call_id`, model output, assignment JSON, a client-supplied identity or a default principal. | Exact SDK/HTTP checks show a consistent delegated namespace on session create/read, Responses send and known-response retrieve. A fresh synthetic parent reaches specialist application entry and passes principal/assignment validation. A changed/missing principal, namespace mismatch, 403 or held effect is a failed discriminator, not permission to relax checks. |

Do not combine call-context forwarding and explicit delegation by guesswork.
For B, establish from the supported contract and a bounded test whether both
headers can coexist and which identity the platform actually resolves. Forward
the opaque call ID unchanged wherever the platform contract requires it; never
recast it as a delegated user or suppress it to escape a failure. Do not forward
`x-agent-user-id` outbound. The legacy `platform_identity_headers()` currently
adds both user headers and is **not** a drop-in B implementation.

#### Binding compatibility is a required discriminator

`Assignment.validate_receiver()` in `demo/artifacts.py` compares the child's
platform-injected principal to the parent's `scope_binding.principal`.
The delegation docs do not promise that delegating an already platform-derived
user ID returns that same principal rather than a newly derived identity.
Therefore a nonempty child user alone cannot select B. Privately compare the
actual trusted identities, exposing only match/presence classifications publicly.

A valid B design must use one stable, authenticated delegation scheme across
the affected lifecycle. Verify all existing boundaries: `RemoteAgents.prepare`,
`create`, `_check` / `recover_creation`, `invoke` and `recover`; raw Azure SDK
session operations and OpenAI Responses clients use different header plumbing.
At the earlier baseline `WorkflowRuntime.resources()` shared a project/header
client with routing and other project operations. Candidate `3aca5dc` now
separates specialist delegation while retaining original model, checkpoint,
history and parent authority. Preserve that explicit separation and execution
order; no generic session manager or second protocol is needed.

If B changes the principal namespace, do not remove the equality assertion,
trust the supplied assignment principal, migrate old histories or silently
reinterpret saved bindings. Return the exact mismatch to this existing
Architect/PO/Scrum process for an authenticated end-to-end namespace/binding
design and focused negative tests. That is an internal bounded contract
decision, not a request for new permission already granted by the user.
An alternative that cannot preserve or securely establish the required binding
is not selected merely because it makes the host gate nonempty.

#### Permission exception: exact scope, not blanket mutation

Before any write, freshly resolve the actual outbound authenticated coordinator
principal, the two existing specialist resources and existing role definitions/
assignments from the validated sole-target lab context. Historical evidence
says an explicit impersonation grant already exists: verify its actual caller,
data action and effective scope rather than create a duplicate or infer it is
missing. Record private exact resource/principal/role IDs, before/after state,
reason and operation outcome; public source contains only generic contracts.

For B, if genuinely missing, grant only the impersonation data action to that
verified coordinator identity, assigned at each existing specialist's supported
agent scope. If that scope is unsupported, document the observed constraint
and smallest supported project scope before mutation; never expand to a
subscription/resource-group/account assignment for convenience. A custom role's
assignable scope is not an instruction to assign it at that broader scope.
For A, any additional interaction permission likewise needs a demonstrated
missing data action at the exact target; no generic Owner/Contributor remedy.
Specialists need no impersonation grant just to serve incoming calls.

Perform necessary changes via deterministic, reviewed lab-owned scripts using
the dedicated verified profile. They must compare installed state, plan the
exact approved delta, record effect ownership before sending, avoid duplicate
assignments, reconcile unknown outcomes and report readback separately from
runtime success. This exception permits required permissions only; it does
not authorize new infrastructure, identity replacement, credentials, model
capacity, network/DNS changes or public ingress. No permission change is made
by this document. Existing account-wide Blob policy is unchanged.

#### Bounded decision procedure and downstream handoff

Scrum Master decomposes these contracts into tasks, not another approval stage:

1. **Read-only inventory and fixture contract:** resolve fresh role/version/
   package/protocol/caller/grant bindings through retained tools; preserve
   rollback and UNKNOWN records. Define a local scripted decision test with
   explicit roots, path, exact versions and a new synthetic scope. Source and
   tests must cover omitted/invalid user, forged assignment identity, two parent
   scopes, both roles, all SDK header boundaries and exact-response no-resend.
2. **Smallest discriminating correction:** A only if a concrete supported
   mismatch is found; otherwise evaluate B against its documented delegation
   contract and binding-compatibility checks. Developer owns application changes,
   DevOps owns any required package/publication or lab permission execution.
   Do not redeploy A unchanged as an experiment. Each candidate must have its
   own hypothesis and failing-before/passing-after local regression.
3. **Bounded ingress observation:** use an in-repo local script, synthetic data
   and a fresh decision-test parent, journaled before sends. Capture exact role/
   version/session/response, header-presence and principal-match flags,
   application-entry/receiver-check outcome and cleanup. Try architect before
   reviewer; stop the candidate on a held/unknown effect. Never resend to get a
   missing receipt. Review existing exact responses instead. Any deployment
   prerequisites still use the original DevOps source/Linux/package gates and
   retained publisher, not an architecture-loop bypass.
4. **Decision output:** `selected-A`, `selected-B`, or `unresolved`, with cause,
   actual tests, binding-compatibility result, exact private evidence locators,
   changed permission scope/rationale (if any), held effects and closing action.
   A selected path needs successful trusted specialist ingress, not merely the
   offline probes. Confirm both roles before claiming release collaboration.
   The decision test is not AC1-AC5 or G1-G8 release acceptance.
5. **Continue artifacts regardless:** unresolved selection does not block
   remaining design, release planning, fixtures or documentation. A true
   provider-only finding needs a specific unavailable supported remedy after
   these alternatives are assessed; external contact/disclosure remains excluded.

The script must require an explicit scenario and record its finite intended
call sequence, not run uncontrolled inference or a benchmark. Diagnostic
inference permission is not automatic authority to repeat an unknown effect.
If the existing environment cannot exercise B without a new package, hand the
minimal reviewed change to original DevOps; do not silently deploy during
architecture to force path selection.

If only provider-side caller resolution can supply the remedy, preserve exact
private evidence and report the required human/provider action; provider contact
or evidence transfer is not authorized. A bounded research task can close with
actionable negative findings without closing the release. A material proposed
contract/architecture change returns through Architect/PO scope decisions.

Keep write-ahead operation IDs and explicit unknown-effect holds at every
external boundary. Known response -> retrieve; verified immutable output ->
reconcile acceptance; unknown send without recoverable identity -> hold.
Old held parents and publication UNKNOWNs remain retained. New guarded operations
require their own exact source/package/version/owner records and reconciled
outcomes; a new run, package or version is not a replay permission.

Recovery acceptance is one supported hosted compute stop with its durable
marker, confirmed stopped/idle state and same-parent continuation. Preserve
checkpoints, children and effect journals; prove no duplicate sends. It is not
hard-kill testing, exactly-once infrastructure, or a general crash guarantee.
Never repeat an uncertain stop or clear its marker to retry.

The lab's account-wide Blob Contributor policy means role/parent restrictions
are application-enforced. They do not protect against a malicious hosted process
using its identity outside these adapters. Do not claim storage-enforced tenant
isolation to satisfy the prototype. The identity-remediation permission exception
above does not require changing this Blob policy.

## Downstream implementation and fixture handoffs

The Scrum Master owns task decomposition, actual assignments, minimal dependency
edges and Git reconciliation. The following are architecture contracts, not
additional approval stages or a replacement sprint plan.

| Work boundary | Done when / handoff | Exclusions |
|---|---|---|
| Developer: continuity regression | Extend `test_followup_invalidates_old_approval_and_preserves_children` to record both roles' hosted/framework IDs, versions, response sequence, exactly two creations, both turn invocations, current requirements and stale approval invalidation | No live claim from fakes; do not compare entire changing framework dictionaries as immutable |
| Developer: controlled revision fixture | Force architect -> blocked reviewer -> same architect -> same reviewer; record exact bindings, new response IDs, revised candidate and review refs and final approval | Do not replace the actual workflow with a toy loop or treat this as live AC3 proof |
| Developer: model continuation | Exercise each real specialist stage with restored history and captured model-session/continuation arguments; prove the second model call uses prior stored history, plus fresh/absent history negative control and known-response no-resend recovery | Replaying a full brief or checking memory text alone is insufficient |
| Developer: supported runtime correction | Evidence-backed failing-before regression and smallest supported path A/B fix under the selection contract above; preserve identity, artifacts, routing and recovery contracts | No speculative headers/grants, history reset or fourth service; authorized necessary permissions are not categorically excluded |
| Designer: customer clarity | First-screen README goal/diagram/two-turn invariant/source path/status, plus concise terminal continuity display derived from validated real events and useful design/review output | No UI/framework rewrite; diagnostic chronology belongs in the existing recovery document |
| DevOps: exact release and live proof | Required source checks, actual Linux hosting-package gate, guarded exact-package preview/publication, final common bundle and synthetic G1-G8 evidence or precise external stop | No metadata-only PASS, mixed diagnostic final release or repeated unknown effect |

Keep acceptance JSON/envelopes and delegation parser unchanged. Prefer opt-in
or separate terminal presentation if readable lines would disturb the existing
machine stream. Presentation must label stable parent/child aliases versus new
response aliases, and indicate verified checks versus unavailable observations.
Generate aliases from actual validated bindings; no raw private IDs, tokens,
real customer transcripts or private lab configuration. Existing machine
evidence remains the acceptance source; do not introduce a parallel ledger.

## Release verification and evidence matrix

| Criterion | Evidence required by downstream original owner loops |
|---|---|
| AC1 / G2 | Real three-role remote execution and accepted current candidate/review, exact requirements and producer/hash/revision checks; no local specialist |
| AC2 / G5 | Synthetic private-ingress initial turn then asynchronous-queue follow-up; same parent, both hosted/framework children and versions, new role responses, no new children |
| AC3 | Controlled offline reject/revise/review fixture with binding and model-history continuation assertions, explicitly labeled offline; AC1/AC2 independently live |
| AC4 / G6-G7 | Once-only supported stop/resume with no duplicate effects, plus distinct second-parent child bindings/artifact scope and no cross-parent requirement leakage |
| AC5 / G1-G8 | G1: final common bundle, exact healthy deployed versions/unchanged identities; G2: remote collaboration; G3: real MI/private Blob provenance; G4: genuine Decision-1; G5: continuity; G6: recovery; G7: isolation; G8: truthful cleanup/unknowns |
| AC6 | Customer-readable first screen and actual two-turn terminal view with unchanged separately available machine evidence |
| AC7 | Exact-source `Test-Demo.ps1 -Python <absolute-validated-python> -LabRepositoryRoot <explicit-root>`, `scripts/Test-Repository.ps1 -Python <absolute-validated-python>`, targeted tests, retained regressions after lab changes, actual source-bound Linux/amd64/hosting-Python package tests |
| AC8 | Reviewed related readability integration, intended explicit-path commits/push on the feature branch, preserved originals/unrelated dirt/history; no private evidence/settings/packages/runtime in Git |
| AC9 / G8 | Reproducible setup/terminal command, sanitized continuity proof, checks actually run, exact final/rollback bindings, owned cleanup and unverified limitations |

DevOps must freshly inventory actual versions/identities/package hashes through
retained tools after private settings validation, not adopt historical
architect17/reviewer15/coordinator23 as current release identity. Build source and
dependency provenance, immutable stage, approved ZIP/version preview and Linux
gate must bind the exact delivered revision/common bundle; no resealing old
migration hashes or installing dependencies without manifest change/missing tool.

The critical live chain is supported identity remedy -> verified source/package
-> guarded final publication -> initial accepted parent -> follow-up -> supported
stop/resume -> evidence closeout. Offline tests and clarity can proceed independently
of remedy discovery. Separate-parent live execution needs the final release and
initial-parent evidence for comparison, not the first parent's restart.
Only the DevOps work loop publishes and establishes cloud-pass. Bounded decision
tests are allowed during design/planning as described above, not formal E2E
acceptance; all tests use deterministic local repository scripts, never GitHub
Actions. The E2E loop owns formal integration validation. Serialize the
publisher and retained transport/mount/CLI resources; the scheduler is not an OS
lock. Suggested `exclusiveResources` names for Scrum assignment are
`lab-hosted-release`, `lab-private-transport` and `application-git-integration`;
map them to actual shared resources rather than assuming cross-run enforcement.

This architecture turn excludes deployment, formal acceptance execution, support
submission, runtime repair and unreviewed dirty-source integration. Those remain
downstream. Future bounded decision tests may be assigned within architecture/
planning under the current user authority without moving release gates.
Owners commit explicit owned paths before review; reviewed scoped work is pushed
on `feature/customer-hosted-session-prototype`. Preserve unrelated staged/dirty
work; integrate task commits there or durably record named retained branches,
commit IDs and abandonment reasons in feature-branch commit messages.
Use existing sprint review/retro and release closeout, not new approval stages.
Five consecutive rounds without reviewer-verified new progress stop blocked;
productive rounds remain uncapped. This conditional architecture is not a
guarantee that a supported provider remedy exists or that AC1-AC9 will pass.
