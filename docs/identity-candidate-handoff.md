# RP-S1-ID-HANDOFF: offline identity candidates, live selection unresolved

## Boundary and result

Developer assignment `RP-S1-ID-HANDOFF` starts from application
`0c43d599760b5213a5b5bd82cfd4e40aede895fa` on
`feature/customer-hosted-session-prototype`. This handoff adds an executable
**offline-only** discriminator and a non-installed delegation candidate. It
does not change hosted runtime behavior, dependencies, lab files, permissions,
deployment or machine-readable acceptance output.

**Selection: `unresolved`.** A tests the existing opaque-call plumbing; it does
not establish an authentication/configuration mismatch or correction. B adds
the documented delegated header to an isolated specialist client in synthetic
tests. The real child principal/namespace, effective permissions, and platform
handling of simultaneous call/delegated headers remain unmeasured. Neither path
is live-selected. HTTP serialization success is not trusted specialist ingress.

The five upstream completion dispositions remain closed within their original
boundaries, including
`["yaml-loops-v1:ArchitectureLoop","architecture-loop-status-reconciliation"]`,
`["yaml-loops-v1:UserExperienceLoop","ux-loop-status-reconciliation"]`,
`["yaml-loops-v1:ReleasePlanLoop","release-plan-loop-status-reconciliation"]`,
`["yaml-loops-v1:sprint/1/RP-S1/SprintDesignLoop","sprint-design-loop-status-reconciliation"]`
and
`["yaml-loops-v1:sprint/1/RP-S1/SprintArchitectureLoop","sprint-architecture-loop-status-reconciliation"]`.
No accepted continuity, terminal or documentation implementation is redispatched.
These dispositions do not supply this assignment's Architect/Critic votes.

## Source and version applicability

Public contracts re-read on October 20, 2026 UTC:

| Source | Applicable finding |
|---|---|
| [User isolation](https://learn.microsoft.com/azure/foundry/agents/how-to/isolate-sessions-per-user), revision `f5104405dfd0231d706f8198fb841f45826595b9`, October 13 | `x-ms-user-identity` accepts 1-256 ASCII letters/digits or `._:-@`; derive it from authenticated server-side identity. The explicit `Microsoft.CognitiveServices/accounts/AIServices/agents/endpoints/UserIdentityImpersonation/action` is required; built-in role names or wildcard coverage do not prove it. |
| Same user-isolation contract | Delegated identities are **not fenced from each other** by the platform. Delegation requires application-owned user/session routing. Header presence alone cannot establish parent isolation or equality with the original platform-derived principal. |
| [Hosted runtime contract](https://learn.microsoft.com/azure/foundry/agents/concepts/hosted-agent-contract), revision `69a226754528e8d4d032ec652eba7d82e584f648`, September 28 | Retain opaque-call forwarding; do not forward the container-only user header. The public contract does not demonstrate which principal a nested call plus explicit delegation produces. |

Inspected installed Windows AMD64 Python **3.12.10**:
Core **2.2.0**, Responses **2.3.0**, Foundry integration **1.14.0**,
AI Projects **2.7.0**. The command audits the complete lock against the installed
environment. These are not fresh container observations.

Relevant current source boundaries:

- `demo/workflow.py`, `WorkflowRuntime.resources()`, shares its project/header
  resources with model/routing/state paths. Do **not** simply replace its shared
  headers with B; the offline candidate is not wired there.
- `demo/foundry.py`, `RemoteAgents.prepare/create/_check/recover_creation`,
  passes explicit headers to raw Azure SDK operations.
- `RemoteAgents._client/invoke/recover` and `ProjectClient.get_openai_client`
  use a separate OpenAI/Responses default-header path. Recovery retrieves the
  exact response with its child session query; it is not another send.
- `demo/artifacts.py`, `Assignment.validate_receiver()`, compares the actual
  trusted child principal to the parent binding, and validates child version,
  parent manifest and exact prerequisites. Do not remove equality to select B.

## Executable offline handoff

Use the existing pinned Python by **absolute path**. No installation is needed.
Run from the application root:

```powershell
$python = '<absolute-validated-python>'
& $python .\scripts\identity_handoff.py `
  --application-root '<absolute-application-root>' `
  --lab-repository-root '<absolute-lab-root>' `
  --scenario offline-A-B `
  --coordinator-version '<inventory-coordinator-version>' `
  --architect-version '<inventory-architect-version>' `
  --reviewer-version '<inventory-reviewer-version>'
```

All three versions are required positive decimal strings, explicitly reported
as **operator-declared, not cloud-observed**. They are not silently used to
claim tested/deployed versions: synthetic remote fixtures use version `7`.
The runner verifies absolute repository roots, audits lock pins, fingerprints
the candidate/tests and relevant runtime source, then runs nine named probes
in one captured child process with a 120-second local watchdog. That watchdog
is not a live traffic budget or a new delivery limit.

Output is sanitized JSON on stdout: no header values, full session IDs,
transcripts, tokens or root paths. Exit **2** means offline candidate verified
but live selection **unresolved**; **1** means an input/runtime/probe failure.
There is deliberately no live option and no exit-0 live PASS.

`candidate_headers()` lives only in the script. Its arguments must come from
the authenticated host, not assignment/client/model JSON. It checks the complete
parent scope, copies rather than mutates SDK context headers, rejects unexpected
platform header keys and invalid delegation syntax, and refuses a user equal
to the opaque call ID. Python object equality cannot independently attest that
its caller supplied trusted context; production wiring must preserve that trust
boundary. A remains the unchanged SDK opaque context; B adds only
`x-ms-user-identity`, never `x-agent-user-id`.

### What the new tests actually establish

`tests/test_identity_handoff.py` exercises:

1. Both A/B candidates and both roles through real `RemoteAgents` lifecycle
   methods. `prepare/create/_check/recover_creation` headers are observed at
   **mocked raw SDK operation arguments**, not a real Azure wire or server.
2. Real `ProjectClient`/`FoundryAgent` Responses serialization reaches a captured
   `httpx2.MockTransport`: one intentional failed POST then exact known-response
   GET, carrying the candidate headers on both paths. No application specialist
   executes. Each recovery adds zero POSTs and no creates.
3. Failed exact retrieval stays `SPECIALIST_INCOMPLETE`, without creating,
   sending, or advancing framework state.
4. Actual `Assignment.validate_receiver()` for both roles accepts a matching
   synthetic fixture but rejects absent/changed-namespace/forged principals and
   another parent's manifest. These are controlled receiver inputs, not an
   observed platform namespace mapping.
5. Missing/invalid user, opaque-call substitution, forged/cross-parent scope,
   changed hosting session, container-header injection and shared-header
   mutation controls fail closed.
6. Invalid CLI roots/versions do not run probes or print supplied private paths;
   even verified offline results retain unresolved selection and exit 2.

These checks are additional offline evidence, not AC1/AC2 or G1-G8 live proof.
Raw SDK serialization and effective authorization still require the downstream
bounded test; the mocked arguments must not be cited as measured ingress.

## Exact unresolved execution boundary and next owner

No cause-specific A mismatch is currently measured. The B header mechanism is
documented, but nested opaque/delegated coexistence and principal compatibility
are not established by that documentation or the local tests. The current
runtime shares resources with non-specialist operations; this script is not
installed in a hosted bundle and cannot make existing versions execute B.
This assignment excludes publication, inference, permission writes and lab
edits. Therefore there is **no executable live discriminator in this change**.
This is an actionable unresolved handoff, not a claim that B is unsupported
or that provider action is the only remaining route.

Scrum Master with Architect advice should reconcile the concrete next delta
under the existing Product Owner scope process:

1. Join the separate fresh-inventory handoff: exact active versions/packages,
   actual outbound coordinator principal, both targets, explicit effective
   impersonation data action and held-operation locators. Do not reuse this
   document's declared versions as inventory.
2. Assign an isolated specialist-only project/header resource candidate and its
   lifecycle wiring, without changing routing/model/history/checkpoint authority.
   Any runtime/package or lab-runner work goes through the existing internal
   replanning handoff; no new user approval is requested for already-authorized
   ordinary scoped work.
3. Assign a deterministic lab-owned bounded decision runner. It must journal
   the source/package/exact target versions and **fresh synthetic scope before
   each intended effect**, retain unknown outcomes and stop on held work. Keep
   private IDs/evidence outside both repositories.
4. Proposed finite B sequence: architect metadata/create/read, one invocation,
   exact response retrieval if known, trusted entry/receiver comparison; only
   on success repeat for reviewer. Stop on namespace mismatch, absent principal,
   held/unknown effect or changed binding. Never retry a failed/uncertain send
   to obtain a successful-looking trace. A requires an observed supported
   configuration correction before a new trial, not unchanged republication.
5. If a permission delta is demonstrated, use reviewed lab scripts for the exact
   existing agent scope (or smallest documented supported project scope), record
   before/after/readback privately and reconcile uncertain writes before retry.
   No permission delta has been measured or executed here.
6. Required new bundle publication remains with DevOps after source/review/
   Linux/package gates; formal integration acceptance remains with E2E. A
   principal namespace mismatch requiring binding-contract change returns to
   Architect-advised PO/Scrum, not a receiver bypass.

Preserve original UNKNOWN publication, held parents, rollback bindings and
historical cleanup uncertainty. No effects were replayed; no live resources,
listeners or mounts were created here. No support case or private evidence was
submitted. The lab's existing unrelated dirty work remains untouched.

## Verification

Using the existing pinned lab Python 3.12.10 executable by absolute path:

- Final `Test-Demo.ps1 -Python <absolute-path> -LabRepositoryRoot <explicit-root>`
  passed dependency checking, **186 offline tests in 40.019 seconds**, and
  compilation. An initial new receiver fixture omitted its candidate revision;
  that fixture was corrected before these passing final checks.
- `scripts/Test-Repository.ps1` passed index, public/private boundary
  (**73 public files**), JSON, PowerShell, context and whitespace checks.
- The executable command verified **109 installed lock pins** and **nine
  offline probes**, returning intentional exit **2** and selection `unresolved`.
  The example execution supplied historical `23/17/15` only as declared version
  labels; it did not inventory or validate those deployments.
- Private settings were loaded solely through `Use-Settings.ps1`; local
  project syntax and lab/registry tenant/subscription linkage passed without
  printing values. Cloud authentication/context was not queried.

No dependencies were installed. The full retained lab release suite was not
rerun because no lab tooling changed. Final common-bundle/Linux checks, fresh
cloud inventory, permission readback, actual child ingress and release
acceptance remain downstream obligations. This artifact is ready for the
original Architect and Critic review; their agreement is not asserted here.
