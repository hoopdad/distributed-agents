# Identity profiling: pinned SDK coverage inventory

The original inventory below retains its research baseline and negative probes.
The [SDK-POLICIES implementation delta](#sdk-policies-implementation-delta)
records the subsequent bounded application attachments and remaining call-site
handoffs. The [integration join](#ip-s1-integration-join) closes those application
call-site handoffs without extending coverage into SDK-owned stores or the
platform. No section is a universal coverage or live acceptance claim.

## IP-S3 continuation-1 private receipt retention

October 22, 2026; **IP-S3-C1-PRIVATE-RECEIPT-RETENTION** adds the opt-in
`demo/private_effect_capture.py` receiving consumer. This is local construction,
not an installed hosted collector, formal changed-source E2E or live acceptance.
All older sections below remain historical, including their runtime counts.

### Private interfaces and conditional accounting

- The owning caller supplies a **new exclusive**, readable/writable binary
  regular-file handle and trusted expected immutable `Binding` values to
  `PrivateEffectCapture(handle, expected=..., new_exclusive=True)`. Open with
  the caller's approved private `x+b` setup; the flag attests exclusivity rather
  than establishing OS locking or permissions. No path, settings, credential,
  client, host destination or logging secret is acquired by this module.
  Caller owns permissions, lifetime and attributable cleanup; it is not closed.
- Install the callable through existing `effect_observation.private_sink`
  **before task creation**. Each receipt is an explicit bounded canonical JSON
  line with sequence and preceding-line digest. Every phase/occurrence survives;
  each acknowledged append checks prior bytes, writes, flushes, calls local
  `os.fsync` and verifies exact readback. Errors latch unhealthy state without
  truncating/repairing raw partial evidence or changing transport behavior.
  Bounds (4 MiB, 4096 records, 4096 bytes/line) are capture limits, not workflow
  budgets; overflow fails closed. No arbitrary object serialization or output.
- Only after independently attributed quiescence of **all** inherited work,
  independently retain `checkpoint(quiescence_receipt=...)`'s byte length,
  SHA256, record count and expected-binding digest. `readback(anchor)` returns
  private raw bytes, receipts and constant issue codes. Canonical records,
  phases, bindings, ordering and occurrence state are checked strictly.
  Missing tails/closure, duplicate requests, late markers, pending streams,
  errors, early close and failed durability cannot supply complete accounting.
  Window closure/fsync alone proves no quiescence. Old anchors fail after late
  writes; earlier results remain conditional, not irrevocable certificates.
- `reconcile(anchor, state=..., manifest_sha256=..., manifest_etag=...,
  operations=..., stops=...)` joins the accepted scoped reader output against
  separately retained manifest/operation anchors and expected targets/pins.
  `OperationAnchor` references exact scoped journal names/digests, never counts
  journal transitions as requests. `StopAnchor` is the caller's independently
  reconciled durable-intent binding and attributed stopped/idle readback:
  the capture must also contain exactly one actual HTTP **204** stop occurrence.
  Intent, HTTP 200 or idle alone is insufficient. Failed reconciliation emits
  no creations/sends/stops candidates and retains the private raw capture.
  Successful tuples may populate the **existing** aggregate list fields;
  they do not authenticate aggregate provenance or establish execution success.

### Source and verification handoff

Accepted bridge correction `e377a32372f2f8e1a74c6e1c8c50323654da752c`,
reader `fa3937bdb7df9d831d6335ca66d9248fc9fee49e` and integration
`91758971d6ab0c1579c6701fbfdb4bbb3d242571` are feature ancestors.
Original bridge/reader/integration audits in the ledger below were opened:
current Architect/Critic votes agree/taskComplete true; earlier bridge negative
history is preserved. Architecture audit
`e96b7f8fa5392f69867c6451205f7e49de763576d9282aeaeb6698371443fb6e.json`
has original Product Owner/Critic/Red Team agreement on this bounded consumer.
No accepted bridge, reader, host or aggregate contract is modified.

`tests/test_private_effect_capture.py` covers durability, partial writes,
fsync failure/cancellation, corruption, invalid fields/bindings/phases,
pending/error/early-close/duplicate accounting, concurrent real public Project
clients, completed-then-late Responses traffic and known-response GET-only
recovery. It reuses pinned local host setup to install the sink before actual
resilient background creation and verifies capture after the ingress exits.
`tests/test_profiling_integration.py` retains all five baseline tests, adds a
durable subcase to the trusted workflow/public Project/Responses/Blob-reader
join, checks independent anchors and actual stop-204 accounting, and preserves
`SPECIALIST_EMPTY` and pre-send rejection. Synthetic public transports only.

The actual selected-lab `ReleaseRoots.select(...).runtime_files()` wildcard
includes the new demo module: **17 demo modules / 22 runtime inputs**, with
reader, live runner and tests still excluded. No lab edit or dependency change
is required. Exact check results and source-map digests accompany the owner
commit/report; a source mapping is **not** a package/build/publication receipt.

Final local checks: focused consumer **15 tests / 1.450 s**, joined integration
**5 tests / 1.961 s**, and documented `Test-Demo.ps1` with existing explicit
Python/selected-lab root **359 tests / 57.506 s**, all exit zero. Repository
checks passed against the preserved unowned specification/index overlay, not
a clean checkout. Initial fixture import/empty-output/pre-consumed-stream
mistakes were corrected without changing accepted runtime behavior. A focused
stderr-emptiness assertion failed during parallel load; the filtered summary
did not retain that captured message, so its exact cause is unproven. Asyncio
slow-task warnings were independently observed elsewhere. The assertion now
checks private sentinels while permitting debug warnings, not suppressing them.
Final focused and full runs passed. No dependency installation or retained
suite/Linux rerun occurred because manifests and retained tooling are unchanged.

### Remaining original-owner obligations

Original E2E/DevOps must qualify only affected new-source proofs, establish a
supported private hosted destination and caller ownership, install before the
actual execution/background interval, prove quiescence/anchor provenance and
owned cleanup, and bind actual state/stop receipts independently. No writable
hosted path or automatic activation is guessed. This API reads back the owning
process's injected handle; no crash-recovery reader, remote durability or
complete multi-process collector is asserted. Pre-install, terminal-parent,
SDK-internal/platform and consumed-model-history coverage remains absent.
Typed original-encoding aggregate/checkpoint limitations are unchanged.

The exact prior late-inherited-capture disposition remains satisfied only in
its accepted bridge boundary; this consumer does not reopen or waive it.
Original `RELEASE-COMMON-PACKAGE-PUBLICATION` and `RELEASE-LIVE-ACCEPTANCE`
references below remain required. No native-denial retry, packaging, publication,
live send/retrieval/stop, cleanup operation or push occurs in this task.
COMMON rollback provenance remains **WAIVED**, never PASS; all partial sprints,
actual AC1-AC9/G1-G8 and original review/retro/closeout remain incomplete.

## IP-S2 continuation-1 observation integration

October 22, 2026; **IP-S2-C1-OBSERVATION-INTEGRATION**, a bounded
Developer source join, not formal E2E, a durable collector or release acceptance.
The older source mappings and measured results below remain dated history.
Current integration commit is supplied in the owner report/commit, not a
self-referential document hash.

### Accepted task/source ledger

Inspected the actual original audits in
`gh-dynamic-workflows/.delivery-runs/eef04e5c-c5ab-4b88-90f6-4a99dd4692ed/context/`:

| Task | Accepted exact application commit(s) | Original audit |
| --- | --- | --- |
| Scoped state reader | `fa3937bdb7df9d831d6335ca66d9248fc9fee49e` | `45c1d10a62d88b37f68689d8281ce7e73598dd63e9ef1461788bc00565c4aca4.json` |
| Effect boundary bridge | `1a3a8966d96a32b6592c4e1d46ccd55381a430ba`, `946873e2b64f828ff0658f3bf7e654a752b577a7`, correction `e377a32372f2f8e1a74c6e1c8c50323654da752c` | `04e3e134c35df1bedab5acd8931d7434e2023fe62230ea048bff8bba5d140eb5.json` |
| Typed checkpoint qualification | `fcf301ee6e14d67e3cb94d58910de4a59a2a844d` | `a2b5fd546b4d4d3a9e714f0ae1e74a90cf83e2429af1f278375d5c59ab112a91.json` |

Each current audit's Architect/Critic votes are agree/taskComplete true, with
no unmet criteria; bridge governance history retains the earlier negative vote.
The accepted correction closes
`["yaml-loops-v1:sprint/2/IP-S2/continuation/1/task/IP-S2-C1-EFFECT-BOUNDARY-BRIDGE/AssignedWorkDeveloperLoop","EFFECT-LATE-INHERITED-CAPTURE"]`,
not the downstream completeness of a live collection. The planning audit
`ae9064e986ff6a387f363bbe559a8fb0ef5d35617c699fa1085f64428eae33e9.json`
retains original Product Owner/Architect/Critic agreement.

All five task commits passed ancestry checks against the authorized feature
HEAD `e377a323`; the accepted reader/typed/bridge owned bytes still match their
commits after LF normalization. No merge, branch switch, abandoned task branch,
history rewrite or push was needed. Selected-lab feature HEAD remains clean at
`9b4919d8bcdbf07203f32657936c27328ea6ccc1`; no retained tooling changed.
This integration owns only its fixture, coverage and index paths. Preserve the
preexisting untracked specification and its uncommitted index inventory line.

### Joined interfaces, actual fixtures and package closure

`tests/test_profiling_integration.py` retains all four original factory/package
cases and adds a joined observation case with retained/broken/absent sink
subcases. It runs actual `WorkflowRuntime.begin/route/execute`, existing trusted
gates/write-ahead transitions, `RemoteAgents.create/invoke`, public Project
Azure Core and OpenAI Responses transports. Only cloud boundaries, version
preparation/lookup and semantic routing are synthetic. Separate create/send
operation bindings and occurrences match the trusted child/version and journal.
An empty SDK-completed HTTP-200 envelope is held as `SPECIALIST_EMPTY` under
all sink modes, not upgraded to collaboration success; an invalid action is
still rejected before another request. The initial fixture incorrectly
expected `SPECIALIST_INCOMPLETE`; correcting that test expectation preserves
the actual more specific rejection, not a runtime/acceptance waiver.

The same synthetic owned backend bytes are then read through an injected real
`BlobServiceClient` with a synthetic public paginated transport, using
`scenario_state_reader.read_scoped_state(service, containers, scope, head,
head_etag, quiescence_receipt, refs, required_operations)` (keyword-only).
Exact manifests/artifacts and every named transition survive. Journal records
are not sends; a conditionally complete read of a held turn is still held.
Invalid refs reject before SDK I/O; head ETag movement makes collection
incomplete, leaves original state unchanged and does not close the caller's
client. This is a synthetic interface join, not an installed export command.

The private `private_sink(callable)` and immutable `Binding`/`Receipt` contract
remain optional. Install in the owning execution context before background
creation; retain every occurrence and late marker, never deduplicate attempts.
`window_closed` is not a final certificate: later inherited requests preserve
their original binding, emit `request_late/incomplete` and permanently invalidate
completeness. A broken sink cannot authorize/retry/suppress a rejection.
Capture coverage, HTTP response/stream completion and execution success remain
distinct. Neither adapter installs private durable storage or an aggregate
collector; production coverage cannot be inferred from an uninstalled sink.

The existing application `!demo/*.py` allowlists and Docker `COPY demo demo`
already include `demo/effect_observation.py`. The actual selected-lab public
`ReleaseRoots.select(...).runtime_files()` includes all 16 current `demo/*.py`
modules plus `main.py`, both requirements files and both routing JSON files:
**21 application runtime inputs**. No lab/allowlist modification is needed.
The root `scenario_state_reader.py`, `live_acceptance.py` and tests are excluded
from that hosted runtime closure; they remain private/offline acceptance inputs,
not a fourth hosted role. The new closure fixtures enforce these exclusions.

All 21 runtime files match feature HEAD after LF normalization. Reproducible
source mapping SHA256 (compact sorted-key JSON of path to SHA256 of bytes):
raw `fa1c97be62a0972b792c0affb9e0e02c9f821967cd2469c1ad7d6464caedae35`;
LF/committed `a28ffbe8825318ee4194e4b5029dadbaa60a999375c98ea93bba877b03407aed`.
These are source maps, not ZIPs, build receipts or release seals.
Affected package runtime bytes are `demo/effect_observation.py`,
`demo/foundry.py`, `demo/workflow.py`; coupled acceptance input is
`live_acceptance.py`. Other affected verification inputs are the joined fixture,
`scenario_state_reader.py`, its fixtures, bridge fixtures, typed qualification
fixtures and their retained actual-host harness. Existing pins/schema and
aggregate validation are unchanged.

### Verification and remaining handoff

Focused joined fixtures passed five tests (including all three sink subcases)
in 1.228 seconds using the existing explicit Python and linked selected lab.
`Test-Demo.ps1 -Python <existing-absolute-python> -LabRepositoryRoot
<explicit-selected-lab>` passed dependency checking, **344 tests in 54.940
seconds**, and compilation (exit zero). This includes the 30 reader, 18 bridge
and four typed-export cases, retained stop/unknown-effect/recovery fixtures,
and all original application cases. `scripts/Test-Repository.ps1 -Python
<existing-absolute-python>` passed current index, **125 public files**, public/
private boundary, JSON, PowerShell, frontmatter and whitespace (exit zero).
No dependency installation or retained-tooling edit occurred, so no retained
suite or Linux build was repeated. Earlier Linux evidence retains all its
recorded exclusions and does not certify the new runtime. These checks apply
to this shared checkout including the preserved specification/index overlay,
not clean-checkout certification.

Consume the accepted [typed qualification](identity-typed-checkpoint-export.md),
not a manufactured export capability: complete public local-file round-trip
works, but original persisted-encoding/unchanged-aggregate attachment remains
unsupported without a public original encoding/hash export and supported
restricted restoration. Matching re-encoding samples are not a canonical-byte
guarantee. No codec/projection/pin/schema or validator change is made here;
an essential follow-on contract change goes through original Architect/Scrum.
Consumed-model-history remains unobservable; pending snapshots and previous
response IDs are not proof of consumed input. Reader completeness is conditional,
not atomic/historical completeness; keep required-operation anchors and compare
prior immutable receipts across windows externally. Platform/SDK-internal,
pre-install, unbound dispatch and terminal parent traffic remain uncovered.

After original Architect/Critic review, original Architect/Scrum coordinates
only the necessary affected original E2E/DevOps routing with these accepted
changed refs and supplied canonical stage keys; this task emits no resume.
Earlier accepted unchanged-runtime evidence remains valid only in its original
boundary; it is not certification of the new bridge runtime. No blanket replay
of old stages, native-denial retry or replacement E2E/DevOps is requested.
At the original `yaml-loops-v1:sprint/1/IP-S1/DevOpsWorkLoop` origin,
`RELEASE-COMMON-PACKAGE-PUBLICATION` and `RELEASE-LIVE-ACCEPTANCE` remain
required. Current package/source/version/trusted-host/effect checks, final
common package/publication, live initial collaboration, continuity, once-only
recovery, isolation, attributable cleanup and original review/retro/closeout
are incomplete. Historical rollback provenance remains **WAIVED, never PASS**.
No permission/authentication resolution, supported live identity remedy or
cloud pass follows from this construction join. Held/UNKNOWN effects and all
historical inputs/proofs remain untouched.

## IP-S2 changed-source handoff to original E2E

October 22, 2026; Developer task **IP-S2-JOIN-HANDOFF**, not another
implementation or formal E2E stage. This current overlay consumes
[SprintArchitecture](customer-prototype-sprint-architecture.md#current-ip-s2-exact-changed-join-guarded-publication-and-live-localization)
`833b4ad90a8429cc6b1453abf5ece22eb54c51d1` and Scrum assignment
`4b30297d6b3c2282f034521f3e3a2b83034b7707`. Earlier results below remain history.
This handoff's documentation commit is supplied by the owner report rather
than a self-referential hash inside the document.

### Exact source, ownership and ancestry

Both checkouts are on `feature/customer-hosted-session-prototype`.
Independently inspected application candidate
`4b30297d6b3c2282f034521f3e3a2b83034b7707` retains runtime/test baseline
`c52786b7dd1595f3048a78061f893dc79635069f`. Its three later ancestors
`6aaf96018ab5c5f2b7ab8a74eceaf1fc09638ab5`,
`833b4ad90a8429cc6b1453abf5ece22eb54c51d1` and
`4b30297d6b3c2282f034521f3e3a2b83034b7707` change only index/design/
architecture/planning documents, not runtime, tests or check entry points.
The seven accepted implementation commits in the
[IP-S1 ledger](#ip-s1-integration-join), plus integration `c52786b7`,
all passed `git merge-base --is-ancestor <commit> HEAD`.

Selected-lab candidate is exactly
`9b4919d8bcdbf07203f32657936c27328ea6ccc1`; predecessor
`1e9ddb8560a5637d639f4657111f3bca49d38d78` passed the same ancestry check.
Inspected the complete correction diff: three named read-only application
test mounts (`.agentignore`, `.dockerignore`, `Dockerfile`) and retained
assertions in `foundry-tf/multi-agent/tests/test_release_native_settings.py`,
plus its index note. They repair the observed missing `/app/.agentignore`
test-input closure, not runtime construction or identity resolution.
Network-none isolation and nonzero failure propagation are unchanged.

Using the existing explicit Python and the two explicit roots in the private
execution input, actual imports resolved `demo` and `live_acceptance` to the
application; `release_roots`, `identity_decision`, `bundle_package`,
`wsl_release` and `observe_agent` to the selected lab's
`foundry-tf/multi-agent`. `ReleaseRoots.select(application, lab)` succeeded.
Actual PowerShell `Resolve-ReleaseRoots` loaded from that same selected
lab's `Release-Roots.ps1`, returned the matched application/lab/tools roots
and succeeded. No operational-context/profile/settings loader was invoked.
Machine-specific absolute roots stay in the private owner report, not Git.

Every source input in the following mappings matched its designated commit
after CRLF-to-LF normalization. All listed individual files also matched
current HEAD. These are reproducible **source mappings**, not package seals.
Each mapping is SHA256 of UTF-8 compact, sorted-key JSON
`{repository_relative_path: sha256(file_bytes)}`; LF mappings hash normalized
committed bytes, raw mappings hash current disk bytes.

| Mapping and exact membership | Entries | Raw mapping SHA256 | LF committed mapping SHA256 |
| --- | --- | --- | --- |
| Application `ReleaseRoots.runtime_files()` at `c52786b7` | 20 | `0f8ea042f49af384897360e3a2267f382be0694d62b8e43ca85a821c6daa3dc2` | `513b869ddc5d93a49871114476690b87b0be1a03579bf0f42817f202a91750a5` |
| Application tracked `demo`, `tests`, `scripts`, plus named verification inputs below, at `c52786b7` | 52 | `dd771282856e724af1e7331999e3353d46234cc1898a35ab346b34625e703b73` | `c2178cfb46837b99c258f1567c8151dcea5791b5975f02ea65d450903a06ee06` |
| Selected-lab tracked `.py`/`.ps1` files under `foundry-tf/multi-agent`, including tests, at `9b4919d8` | 41 | `94863da6cc284c3d5976b5942d0a472f12758d73947ee18e03d067cc4abc4aea` | `bfe967c0d1671a86dba00cec541e6b6286996e61c57d6f1682733f10235286d0` |

The application verification union adds `Test-Demo.ps1`, `Dockerfile`,
`.agentignore`, `.dockerignore`, `azure.yaml`, `main.py`, `requirements.txt`,
`requirements.lock.txt`, `native_proxy.py`, `agent_metadata.py`,
`package_guard.py`, `live_acceptance.py`, `config/routing-corpus.json` and
`config/routing-calibration.json`. Deduplicate/sort all paths before hashing.
Enumerate tracked paths with `git ls-files` at the bound candidate; read
baseline bytes with `git show <commit>:<path>`. These mappings intentionally
exclude documentation/private settings and are not a seal of every lab file.

| Individually relevant path (lab paths relative to `foundry-tf/multi-agent`) | Raw working SHA256 | LF committed SHA256 |
| --- | --- | --- |
| Application `tests/test_profiling_integration.py` | `b08e51e789e5efd0abd6c3bccdff4658d42915f486c76d4f309005ba0f816381` | `c2733455d42c1b138a87cd006899c48b0d93611ce0cf62a0899c6d4025cff3e0` |
| Application `Test-Demo.ps1` | `2d6bc0fd74c70908eec572a4b73d1ec196ff01b5c6f0f9ea75cb7bcdc95464d5` | same |
| Application `package_guard.py` | `187440c382fc1d56989593ac26865ccf24b2af0f932d70165666c79d374b88da` | `31b4f055f647cd0d8903f5b48e7a9c4a01251d271d80c3b17b0df60999f321cc` |
| Application `scripts/Test-Repository.ps1` | `8a50384140c74590ed31057f436c9bab7dcdcddd5c34feb2d055a0c446a0a1b2` | `01565e7b999f87d38622f13c0870566420f9981fb42d4f1a1358073d078dcf83` |
| Lab `Build-Demo.ps1` | `181cb84d999bf6a2b57ea2d7feb5c09bbaa62f9e9c919bdb9a44b14a859de209` | same |
| Lab `tests/test_release_native_settings.py` | `baa2c9a046e83cf84b97f0e35a504ac5786038c355001fd964a0bc242425e7f4` | same |
| Lab `release_roots.py` | `312c926b91a416c957efe66c387428dec179988f32164b6706892e0d5bb09fd1` | same |
| Lab `Release-Roots.ps1` | `8438d8bdbc04f94bd1b8380601fe8423a66b3045ddd561ec46bc69eb9e987e27` | same |

The three newly mounted application inputs also matched committed/raw bytes:
`.agentignore` `c0b0f1dcc150191c7ada339cdca597cb76e12410bd6f0c62ac706bec5f0a16c2`;
`.dockerignore` `07668721e93c114faef8d76b850e87457bce5b2d8daaf6ac7d534304c2e0172f`;
`Dockerfile` `8cf14b34577830191586eb3b744535b5772b841f4f32b44099767b4d843b1eeb`.

### Original reviews and applicable captured checks

Opened audits under the current run's
`gh-dynamic-workflows/.delivery-runs/eef04e5c-c5ab-4b88-90f6-4a99dd4692ed/context/`:

- Original E2E `da4425177dd7b48116a3b6eb9aa04742eb2f0cb3d4d4196494c5a4416c2e34a0.json`:
  Architect/Critic/Product Owner each agree and taskComplete, no unmet criteria,
  for the **earlier join**, not the changed lab prerequisite.
- Original DevOps `f7b942e94652c10a41c6e32a96cef0d447c00995ec1fbcd2a35cb65a28677dec.json`:
  Architect/Critic/Developer each agree with the bounded correction/report but
  each records taskComplete false. All retain changed-join E2E, common-package
  publication and actual cloud/live acceptance obligations.
- Current architecture `26adb308b85ae4732ca698f4dcdd8985c3c1096516154c481dad23e63ee9282f.json`:
  Product Owner/Critic/Red Team each agree and taskComplete for architecture.
  No document vote establishes passing deployment or live identity resolution.

Inspected the private DevOps `verification.json` and all three exact named
captures in delivery workspace evidence directory
`delivery-evidence/identity-profiling-devops-20261022T0402Z`.
Independently verified capture SHA256 values:
`linux-before.txt` `a682049e9fa814ba63375c75b5fdacdeef9f2fb10eae7e6bd7ff17ec00bab775`;
`windows-after.txt` `d73c6f3847da2e869bc9245949df20baffdbf0e15e48a4492cc5b0a38e171349`;
`linux-after.txt` `59fb415cd98193d889249c35d0d75c464e973387616a1f98792d9bc74e0b4cb7`.
The captures are copied combined tool-returned streams, not independently
separated OS stdout/stderr. They remain unmodified private evidence.

| Attributed execution, not rerun here | Applicable result and exclusions |
| --- | --- |
| Initial Linux application suite | 278 run, one error, eight skipped, 231.095 seconds; `/app/.agentignore` absent. Retain the actual failure as correction evidence, never as a pass. |
| Corrected linked Windows wrapper | 278/278 application passes in 56.625 seconds; retained 236/240 passes in 204.272 seconds, four excluded: three native-Linux bridge/artifact cases and the positive exact-clean-commit entrypoint case. Dependency and compilation checks passed. |
| Corrected Linux wrapper | Application 270/278 passes in 305.879 seconds, eight excluded; retained 197/240 passes in 322.453 seconds, 43 excluded. Wrapper exit zero is not 518 passing cases. The three Windows-excluded native-only cases passed here. |
| Runtime/image probe | Python 3.13.15, pinned core 2.2.0 / Responses 2.3.0 / hosting 1.0.0b261002; linux/amd64 image `mike-lab-multi-agent:74fa67b7acd0`, ID `sha256:b383102c8d67f753adb380e2930184317934248aa48fe656b8a39fc989e1612e`, source SHA256 `74fa67b7acd054750f564cf1dc4040e90c0cb17b2c4595209f9522423f0a6db3`. |

The eight application Linux exclusions are two PowerShell settings bootstrap
cases, two explicitly linked external connectivity cases, three Windows
CLI/file-lease cases, and
`PackageClosureTests.test_actual_selected_lab_runtime_closure_includes_all_application_modules`.
That last fixture lacks an explicit linked lab checkout in the network-none
Linux container; it **did not run there**. It passed with explicit linkage
in Windows. Retained Linux exclusions are the 43 individually named Windows/
PowerShell/Docker Desktop wrapper cases in `linux-after.txt`; they are not
native Linux coverage. The Windows positive exact-clean-commit exclusion
remains unproven by these captures, not silently closed by committing.
The captures warn of amd64-on-arm64 execution: no native-amd64-host claim,
new hosting-package gate, bundled ZIP or deployment proof follows.

Source/runtime/test comparisons above support reuse of these captured cases
at this exact join; original E2E decides applicability and any necessary
additional verification, not a blanket rebuild. The current Developer ran only
the four standalone `test_profiling_integration.py` cases with explicit lab
linkage (PASS, 0.255 seconds), and retained
`NativeSettingsTests.test_application_package_closure_inputs_are_named_readonly_test_mounts`
plus `test_docker_source_hash_binds_calibration_input_and_preserves_original_hash`
(PASS, two cases, 5.209 seconds). Use the existing absolute Python,
`OTEL_SDK_DISABLED=true` and `AZURE_LAB_SOURCE_ROOT=<selected-lab>/foundry-tf/multi-agent`;
load the retained test module from that same root. No dependency restoration
or full application/Linux suite was rerun by this task.

The documented `scripts/Test-Repository.ps1 -Python <existing-absolute-python>`
also passed: current index, 113 public files, public/private boundary, JSON,
PowerShell, frontmatter and whitespace. Direct assertions confirmed the two
linked headings and three audit files exist and the complete historical
coverage content after this overlay remains unchanged. Shared checkout note:
the independent prospective-evidence owner was editing
`docs/identity-candidate-handoff.md` during validation; that path is neither
reviewed nor committed by this task.

### Smallest continuation and remaining boundaries

Apply exact disposition
`["yaml-loops-v1:sprint/1/IP-S1/DevOpsWorkLoop","RELEASE-CHANGED-JOIN-HANDOFF"]`.
After this task's original Architect/Critic review, existing Scrum/orchestrator
routes the accepted source/evidence ledger through supported continuation to
the original `sprint/1/IP-S1/EndToEndTestLoop` prerequisite reassessment, with
its original Architect/Critic/Product Owner reviews. Bind the actual candidate,
loaded roots and any later documentation-only ancestry; assess these captures
and exclusions, verify only the changed join as necessary and issue the updated
handoff. Do not equate this Developer ledger with that still-missing acceptance.
No duplicate E2E, stage-state edit or additional approval gate is requested.

All supplied intended implementation/task commits are already ancestors on
their authorized feature branches; no merge, abandoned code branch, branch
switch or push was needed. This task adds only the current coverage/index
overlay. Preserve the pre-existing untracked specification and its uncommitted
index line; repository validation includes that overlay, not a clean-checkout
inventory certification. Subsequent independently owned document commits need
their own attribution, not runtime recertification solely for moving HEAD.

At that same exact DevOps origin, `RELEASE-COMMON-PACKAGE-PUBLICATION` and
`RELEASE-LIVE-ACCEPTANCE` remain original DevOps obligations after accepted
changed-join E2E. Current automated source/package/version/trusted-host/effect
checks, one serialized common-package publication for all three existing roles,
distinct privately recorded diagnostic intent, attributable cleanup and original
AC1-AC9/G1-G8/review/retro/closeout remain unmet by this document.
Historical COMMON rollback provenance stays **WAIVED**, never PASS.
The two SDK timeout dispositions at the exact SDK-POLICIES origin cited below
remain satisfied in their accepted source/test boundary, not reopened.
No supported identity remedy or authenticated outbound principal is established;
SDK-internal/platform visibility gaps and all held/unknown operations persist.
Independent prospective evidence and approved IP-S3 preparation are unaffected.

## Scope and evidence

Developer inventory for IP-S1-SDK-INVENTORY, against application baseline
`ddd376d9af37661e1126258896c72c1efdf73dc6` on
`feature/customer-hosted-session-prototype`. This is a source/constructor
inventory, **not installed profiling, a successful live hook or release acceptance**.
It consumes the October 21 IP-S1 overlay in
[SprintArchitecture](customer-prototype-sprint-architecture.md) at `9367939`
and its supplied agreement audit
`0ce2eb36318f8583f59e58ce5afac4b1b6edd92b02df6ff1d3db9af2211c17db`.
No prior dispositions or reconciled corrections were supplied for this task.
The existing trusted-identity, streaming, background, recovery and effect gates
remain mandatory. Historical rollback provenance is WAIVED, never PASS.

Installed distribution metadata was read using the existing linked lab Python:
Foundry hosting `1.0.0b261002`, AgentServer core `2.2.0`, Responses `2.3.0`,
AI Projects `2.7.0`, Blob `12.31.0`, Identity `1.25.3`, Azure Core `1.41.0`
and httpx2 `2.13.1`. These match the application manifest/lock pins.
SDK references below are paths **relative to that interpreter's site-packages**,
not suggestions to edit SDK files. Private settings, token caches and credential
values were not read. No dependency installation, network request or token
acquisition was used for this inventory.

## Source reference key

| Key | Exact pinned source seam |
| --- | --- |
| P | `azure/ai/projects/aio/_client.py:77-102`: default Azure Core policies and `AsyncPipelineClient(..., **kwargs)`; `_patch.py:155-224`: public OpenAI factory forwards kwargs to `AsyncOpenAI`. |
| C | `azure/core/_pipeline_client_async.py:130-141,185-264`: documented `per_call_policies`, `per_retry_policies`, `transport`; policy insertion retains the supplied default chain. |
| B | `azure/storage/blob/_shared/base_client_async.py:95-155`: constructs its own policy list and `AsyncPipeline(transport, policies=policies)`; `_shared/policies.py:328-338`: request hook consumes `raw_request_hook`; `_shared/policies_async.py:100-149`: async response hook consumes `raw_response_hook`. |
| I | `azure/identity/aio/_credentials/managed_identity.py:46-122`: environment-selected credential receives kwargs; `aio/_credentials/imds.py:45-60`, `aio/_internal/managed_identity_client.py:25-40`, `_internal/pipeline.py:39-96`: separate Identity pipeline builder. |
| H | `agent_framework_foundry_hosting/_responses.py:665-689,850-888`: host constructor exposes workflow factory, parser, `prepare_options`, checkpoint/session/response providers; `azure/ai/agentserver/core/_base.py:450-466`: public `add_middleware`. |
| W | `agent_framework_foundry_hosting/_workflow_responses.py:408-487`: request context -> trusted scope -> hosted request -> options hook -> workflow factory -> continuation stores -> input parser -> claim/execution. |
| S | `agent_framework_foundry_hosting/_scope.py:23-58`: hosted scope rejects missing trusted user/call or mismatched session before returning a scope. |
| Q | `azure/ai/agentserver/responses/hosting/_endpoint_handler.py:174-190,856-921,1071`: raw-header extraction and endpoint/stream request-context bind/reset; `core/_request_context.py:41-145`: public context accessor and opaque-call forwarding contract. |
| R | `azure/ai/agentserver/responses/hosting/_resilient_orchestrator.py:239-345,785-895,1111-1163`: reconstruction, task dispatch, durable input capture; `_resilient_input.py:54-83,194-264`: identity serialization/derivation; `_orchestrator.py:99-140`: per-iteration handler context bind/reset. |
| T | `agent_framework_foundry_hosting/_state_store.py:99-138,243-315,395-501`: checkpoint and session providers/stores; `_workflow_state.py:206-219`: SDK-owned workflow binding store. |
| U | `azure/ai/agentserver/core/storage/_state.py:86-186,242-298`: public `FoundryStateStore` construction/get-or-create accepts credential and kwargs, defaults to an owned `DefaultAzureCredential`; `storage/_client.py:55-88`: Azure Core transport/policy chain. |
| V | `azure/ai/agentserver/responses/store/_foundry_provider.py:139-205`: response provider creates its own Azure Core client with fixed policies; constructor accepts credential/settings/version callback, not pipeline kwargs. `responses/hosting/_routing.py:367-405`: hosted default creates this provider with its own `DefaultAzureCredential`; local fallback uses a file store. |

## Factory / transport / attachment matrix

Every proposed attachment below is **not yet implemented or behavior-tested by
this task**. A source-supported seam is not a coverage PASS. Send/headers/error
events do not establish stream or agent-execution completion.

| Path and application owner | Actual transport and supported observation choice | Observable events and safe binding | Explicit gaps and retained/proposed checks |
| --- | --- | --- | --- |
| Agent metadata and specialist session create/lookup: `demo/foundry.py:157-179` `ProjectClient`; `RemoteAgents.prepare/create/_check/recover_creation` at `253-301` | Azure Core `AIProjectClient`, default async transport (AioHttpTransport), **not** `data_client`. P/C support additive `per_call_policies` or `per_retry_policies` in the application's `super().__init__`. Prefer per-call observation of one logical SDK operation; use per-retry only if actual attempts are explicitly distinguished. Retain retry/auth/timeouts. | Bounded session-create, session-lookup and metadata route templates; timing/status/error category, role and allowlisted correlation only. Record header presence, not values; a per-call send checkpoint is before authentication, not proof of final bearer principal. | A Project policy cannot see OpenAI calls. Constructor insertion probe passed (below); SDK-POLICIES must prove actual session operations emit events through a fake transport, including failure and redaction. Preserve ambiguous-create lookup-only behavior. |
| Remote specialist Responses invoke/retrieve: `demo/foundry.py` `RemoteAgents`; `demo/workflow.py` `WorkflowRemoteAgents`; terminal `ProjectClient` | P factory passes application's `http_client` into OpenAI. `demo/foundry.py:95-179` `OriginTransport` / `data_client` is the actual httpx2 seam. TRANSPORT owns final-header send, headers, error and unbuffered stream wrapper. | Exact role endpoint -> fixed Responses route template. Correlate using reviewed event-contract bindings, not raw endpoint IDs, user hashes or bodies. Actual final-header presence is observable here, bearer identity is not. | Azure Core policy installation cannot cover this path. Test exact origin, no redirect/retry, stream chunks/close/cancel and known-response-only recovery. Preserve `WorkflowRemoteAgents.invoke/recover` rather than resend a failed held effect. |
| Specialist model/history calls: `demo/architect_agent.py:191-201`, `demo/reviewer_agent.py:192-202`; `FoundryChatClient(project_client=project)` | `agent_framework_foundry/_chat_client.py:248-258` obtains `project_client.get_openai_client`; thus the same application httpx2 transport for model requests and `responses.retrieve` recovery. | Model Responses template and send/headers/stream/error milestones, safe role/binding supplied by the application. | Model history in MAF `AgentSession` is not an HTTP request. Its persistence uses the session provider row below. Retain pending-model-response retrieval and immutable output tests; do not label model HTTP 200 an accepted candidate. |
| Decision-1: `demo/routing.py:249-280` `DecisionClient.score`; legacy `demo/foundry.py` `DecisionRouter.choose` | Shared httpx2 `data_client`; directly posts to `/providers/microsoft/v1/systemone`. Instrument at OriginTransport for both application clients, not a separate Azure Core policy. | Fixed Decision route, HTTP method/status/timing/category; only allowlisted request IDs/trace metadata. | Token acquisition is separate. Preserve deterministic gates/admission before the call, body/schema validation and machine stdout. Retain `tests/test_routing.py` and Decision adapter tests. |
| Native artifact/effect/manifest Blob access: `demo/workflow.py:142-151,521-550` -> `demo/artifact_store.py:85-104` `BlobArtifacts` | Explicit `AioHttpTransport(use_env_settings=False)` with Blob SDK's own pipeline B. **Generic `per_call_policies` does not insert a policy here** (negative probe below). Public raw request/response hooks can invoke safe policy callbacks at their supported positions. Public custom `transport` is a viable separate boundary for send exceptions, if required; preserve its ownership and existing options. | Fixed Blob operation classes (read/write/lease), status/timing; safe role/operation binding only. Raw hooks do not prove final wire headers or exception coverage; response hooks must not inspect payloads. | Do not use private `_additional_pipeline_policies` / `_pipeline` or replace the policy list to manufacture coverage. SDK-POLICIES must choose supported hooks/transport with tests, or explicitly record uncovered exception intervals. Preserve ETag/fencing, leases, immutable writes and retry_total=0. |
| Specialist injected Blob services: `demo/architect_agent.py:101-115`, `demo/reviewer_agent.py:104-118` | Each constructs its own `BlobServiceClient` and injects `service=` into `BlobArtifacts`. Same B transport/hooks, **bypassing the BlobArtifacts constructor factory**. | Same bounded Blob events; attributable role set by the owning application factory. | Editing only `artifact_store.py` does not cover these two services. SDK-POLICIES reports attachment choice to INTEGRATE; INTEGRATE/Scrum must coordinate these call sites if needed (outside SDK-POLICIES' current owned paths). They must remain explicitly uncovered until fixtures prove coverage. No silently expanded ownership. |
| Application credential acquisition: `demo/workflow.py:525`, `demo/foundry.py:447`, specialist resource factories | Async `ManagedIdentityCredential` uses its own Azure Core pipeline, selected by environment I. Standard `per_call_policies` is **not consumed** by its Identity pipeline builder (negative IMDS probe below). Public `transport` and raw hooks reach pipeline-based implementations; custom `policies` replaces defaults and is unsuitable here. | Fixed credential-acquisition route category, elapsed/status/error category only. Never log request headers, query, token response, principal, environment or exception text. Token cache hits have no HTTP send. | Do not use `_per_retry_policies` or select/patch private credential implementations. SDK-POLICIES must test the chosen public hook/transport with synthetic branches and keep untested environment branches/cache hits explicit. Preserve credential auth, IMDS probing/retries and transport ownership; no credential call was made by this inventory. |
| Terminal credential: `demo/terminal.py:268-272` | `AzureCliCredential` invokes the CLI subprocess (`azure/identity/aio/_credentials/azure_cli.py`), not the ProjectClient/httpx2 transport. | At most an application acquisition boundary; this inventory attaches nothing. | Azure Core/httpx2 policies cannot see CLI internals or cached token handling. No CLI execution, authentication or cache inspection is needed for this research. Keep uncovered rather than inventing pipeline coverage. |
| SDK agent-session/history persistence: `demo/foundry.py:181-209` `HostedJournal`; specialists' `AgentSessionStoreProvider(store_name="specialist_history_v2")`; host defaults | T uses `FoundryAgentSessionStore._get_store` -> `FoundryStateStore.get_or_create(..., user_isolation=True)` with no pipeline kwargs. U uses its own Azure Core client/default credential. Provider constructor accepts only `store_name`. | Application call-boundary checkpoints are reachable; SDK-internal HTTP send/status/errors remain uncovered by application Project/Blob policies. | H exposes provider replacement as a public abstraction, but the stock provider does not expose policy forwarding. Replacing persistence to add logging is not the minimal profiling attachment. Preserve user scope, ETags, serialization and call-ID forwarding. Retain session-history continuity tests; do not claim a Project policy profiles these stores. |
| MAF checkpoints and native workflow bindings: `demo/host.py:44` `CheckpointStoreProvider()`; W continuation preparation | T checkpoint provider exposes allowed types/get_store, not transport/policy kwargs. Both checkpoint and `_workflow_state.FoundryWorkflowBindingStore` construct U independently; the latter is SDK-owned, not the replaceable checkpoint provider. | Application workflow checkpoints/executor boundaries only; internal storage HTTP currently uncovered. | Public U supports constructor kwargs **when the application constructs U**, but these callers do not forward them. A custom checkpoint provider alone cannot cover native binding storage. No monkeypatch or storage rewrite; preserve MAF checkpoints and write-ahead unknown-effect holds. |
| SDK stored Responses / server-managed history | H has `store`/`response_store` provider injection; default hosting routing creates the provider separately. V uses Azure Core, owned credential and fixed policies, not Project or Blob client. Server-managed history may read stored Responses depending on the selected host history mode. | Response-provider call boundary could be decorated through public provider protocol in a separately scoped change; no generic HTTP policy injection in V's constructor. | Distinguish provider injection from policy injection. Stock internal requests remain uncovered. No provider replacement is required to complete this inventory; never claim coverage of all response/history stores or streamed replay because ProjectClient is profiled. |

## Host/context checkpoint reachability

| Boundary | Supported seam and pinned ordering | Meaning / retained gap / proposed fixture |
| --- | --- | --- |
| Raw ingress and ASGI response | H `server.add_middleware(PureASGIMiddleware)` before `run()`; inspect raw `scope["headers"]` without changing it. | Observe case-insensitive absent/empty/nonempty/duplicate/malformed presence for public delegation and platform user headers separately. Pass receive/send/messages/cancellation unchanged. ASGI final body means delivery milestone, not successful background execution. No context is guaranteed before endpoint parsing. |
| Endpoint context | Q extracts `x-agent-user-id` into `PlatformContext.user_id_key`; absent is None, empty is empty. Endpoint ambient `FoundryAgentRequestContext` uses `ctx.user_id or None` and `ctx.call_id or None`, collapsing empty into absent at this particular checkpoint. | Do not infer that all SDK layers preserve empty strings, or that a delegation header must survive. Record independently observed presence/coverage; never recover missing trusted identity from raw headers. |
| Preparation BEFORE application factory | W first reads ambient context and S validates hosted scope; only then builds `HostedResponseRequest` and runs public `prepare_options`. | Missing trusted user/call can reject before **both** options and factory hooks. Existing `demo/host.py` `WorkflowPreparationDiagnostics` filter observes the specific SDK preparation/RuntimeError log while its context is available. This is an exact pinned log event, not a universal exception hook. Keep existing rejection and allowlisted code; absent matching log/context is unavailable, not success. |
| Reachable preparation/options/factory | W calls `prepare_response_options` then resolver. Public `prepare_options` receives `HostedResponseRequest`; `create_workflow(request)` and `WorkflowRuntime.__init__` inspect request scope and ambient accessor. | Compare scope/request-context user or call equality only when representations match; report not-comparable otherwise. Do not compare public delegation to platform user values as if identical. Keep request-local immutable snapshots, no host/transport identity cache. |
| Parser and executors | W parser runs after continuation preparation, except recovery uses `run.recovery_turn()` and can skip parser. Application `parse_turn`, executor handlers and `WorkflowRuntime.resources` are reachable application hooks. | Instrument an actual executor/resource boundary as well as parser; parser alone cannot cover recovery. Execution completion must come from actual workflow outcome, not handler return or SDK-completed envelope. |
| Resilient background AFTER HTTP request exit | R persists user/call/session in durable input; reconstructs response context; `_iter_handler_with_request_context` binds ambient context for each `__anext__` and resets it in `finally`. Both resilient stream and nonstream dispatch are separate paths. | Observe inside the public request-aware factory/executor, not by replacing the private wrapper. Crash recovery has no new raw ingress and cannot retrospectively observe the original request. Test actual pinned host dispatch after endpoint exit, both success/rejection and concurrent reset/cancel. |

The existing
`tests/test_workflow.py::LiveObservationTests.test_pinned_sdk_resilient_identity_survives_serialization_and_handler_entry`
round-trips the pinned serializer and directly invokes its private handler
wrapper. It is useful retained evidence, **not** an actual full-host resilient
background test. INGRESS-CONTEXT still owes that acceptance fixture.
`test_sdk_preparation_filter_reports_only_missing_trusted_scope` is the retained
filter/redaction fixture; it does not establish raw ingress coverage.

## Minimal implementation handoff and verification

1. SDK-POLICIES: use additive Azure Core policy insertion for ProjectClient;
   do not copy that constructor option to Blob or credentials. B/I show why.
   Choose public raw hooks/custom transport where appropriate, preserving
   existing defaults; a missing send-exception hook must remain a named gap.
   Prove covered clients with actual fake-transport requests, not constructor
   presence alone. No private insertion knobs or new credential retrieval.
2. INGRESS-CONTEXT: use H plus public options/factory/parser/executors, retaining
   the preparation log filter. Test the early S failure separately from reachable
   hooks. Explicitly account for empty-value normalization and parser-skipped
   recovery. R is source evidence, not permission to patch SDK internals.
3. INTEGRATE: reconcile the two injected specialist Blob factories with the
   selected attachment, or retain their uncovered status; coordinate call-site
   ownership rather than silently expanding SDK-POLICIES. Refresh the shared
   repository index after incorporating this new document; this task owns only
   this document and preserves the pre-existing dirty index/specification.
4. TRANSPORT can proceed from its event-contract handoff independently. This
   inventory does not gate its httpx2 work or require full SDK coverage first.

Offline constructor probe, run with the existing explicit linked-lab Python:
`AIProjectClient(..., per_call_policies=[marker])` retained one marker;
`BlobServiceClient(..., per_call_policies=[marker])` retained zero;
`ManagedIdentityCredential(per_call_policies=[marker])` with an empty synthetic
environment (IMDS branch) retained zero. Assertions passed, clients were closed,
and the fake credential's `get_token` would raise if called. Read-only inspection
of constructed policy chains was used only for research assertions, not a runtime
private attachment. The two zero counts are actionable negative findings, not
working diagnostics or claims about every credential branch.

Validation executed in the shared checkout:

| Command / check | Actual result and scope |
| --- | --- |
| `./Test-Demo.ps1 -Python <linked-lab-root>/.venv/Scripts/python.exe -LabRepositoryRoot <selected-feature-lab-root>` | Exit 0. `pip check`: no broken requirements. 223 offline application tests passed in 57.198 seconds, including retained wrapper regressions; compilation succeeded. Existing explicit Python and selected-feature lab roots were supplied, with no installation. This was a concurrently changing checkout, not the later INTEGRATE exact-source E2E join. |
| `./scripts/Test-Repository.ps1 -Python <linked-lab-root>/.venv/Scripts/python.exe` | Exit 1 at `REPOSITORY_INDEX_STALE`. Later boundary/parser stages did not run. This is an executed stale-index failure, not the historical permission denial or a repository PASS. INTEGRATE owns index refresh and rerun; no unrelated index changes were absorbed here. |
| Installed metadata + manifest/lock comparison | The eight named versions above matched; no SDK version extrapolation was used. |
| Constructor insertion probes | Three assertions passed (Project insertion; Blob and IMDS non-insertion). No send/token calls. Downstream retained pipeline fixtures still required. |

The initial application source baseline above remains the inventory binding.
While checks ran, the independent event-contract owner committed `20c315e`;
its source is not adopted as a reviewed dependency by this inventory.
No runtime source was changed in this task. The new coverage document and
pre-existing untracked specification require an eventual shared-index refresh;
that concrete repository-check gap is retained for the integration owner.

Safe event bindings must consume the reviewed EVENT-CONTRACT API, not invent
raw identity hashes. Coverage (`observed`/`unavailable`/`not reached`) remains
independent of value presence. Redaction/failure-isolation tests must use sentinel
identities, headers, URLs/query, bodies, credential responses and exception text;
none may escape to private logs or machine stdout. No diagnostic authorizes a
request, suppresses rejection, repairs identity or proves platform translation.
The authenticated outbound principal and platform resolution interval remain
unobserved. No RBAC/platform defect or header substitution is justified here.

Original Architect/Critic review remains downstream of this inventory commit.
Exact-source E2E, newly identified common-package publication, synthetic intent
recording, live AC1-AC9/G1-G8 and attributable cleanup remain their original
owners' work. The held parent and unknown effects are untouched.

## SDK-POLICIES implementation delta

Consumes accepted EVENT-CONTRACT `20c315e`, SDK-INVENTORY `b7b4e0e` and
TRANSPORT `9c8dfdf` on the established feature branch. Their original
Architect/Critic agreement audits are respectively `49fb735d`, `8224c1af` and
`b5e33586` in the current IP-S1 run context. The original implementation was
`87de392`; the timeout-preservation correction below applies the reconciled
required dispositions from the same SDK-POLICIES loop. This delta changes only `demo/foundry.py`,
`demo/artifact_store.py`, this matrix and `tests/test_sdk_diagnostics.py`.
Previously reviewed transport code is preserved.

### Public attachments and exact coverage

| Application path | Implemented public seam / retained behavior | Proven offline coverage and explicit limits |
| --- | --- | --- |
| All application `ProjectClient` instances, including specialist session create/lookup and metadata calls | `SDKDiagnosticsPolicy` is an additive **per-call** `AsyncHTTPPolicy`. `ProjectClient` retains its default pipeline/auth, zero retries and original timeouts; optional keyword-only `transport` forwards the public test/transport seam without changing the default. | Actual pinned `agents.create_session`, `get_session` and `get` operations pass through a synthetic Azure Core transport, with default authentication still acquiring a synthetic bearer. Session routes are closed templates; metadata remains `other`. Logical send/response/error are observed; send is before downstream authentication/retry, and response is when the downstream policy chain returns, **not the instant wire headers arrive**. It is not a final-header principal observation. |
| `BlobArtifacts`' application-owned default service factory | `blob_diagnostics_transport(role=...)` wraps the existing explicit `AioHttpTransport(use_env_settings=False)` using the public `transport` option. No custom policy list or private insertion. Existing `retry_total=0`, size/timeouts, auth, ETag, leases and application scope checks remain unchanged. | Actual pinned Blob `get_blob_properties` and `upload_blob` traverse the default factory and emit per-attempt send/response; failed sends emit error and rethrow. Tests preserve request/response identity and original send options, without body reads or stream wrappers. A successful status is only HTTP evidence. |
| `foundry.create_hosted_agent` application credential factory | `ManagedIdentityCredential(**credential_diagnostics_options(role=...))` uses public raw request/response hooks, leaving transport construction, environment selection, branch defaults and retries entirely with Identity. The original eagerly supplied transport was incorrect and has been removed. | Synthetic IMDS and App Service branches execute the actual pinned credential pipeline with no network or real token acquisition. Paired request/response hooks emit per-attempt events without inspecting credential headers or payloads. IMDS retains its two-second connection default; App Service retains 300 seconds. Baseline/instrumented retry-budget fixtures verify equal configurations and a one-second budget clamped to 1 then 0.75 seconds. Cache hits emit no send. **No transport-error/cancellation hook is available through these callbacks**: a send without response is incomplete, not an inferred error or success. Other environment-selected implementations remain unverified. |
| Reusable public decorator `SDKDiagnosticsTransport` in `artifact_store.py` | Delegates `open`, `close`, `__aenter__`, `__aexit__`, `send(**kwargs)`, `sleep` and the inner optional `connection_config` to the original transport. Exceptions and cancellation propagate; diagnostic sink/schema failure cannot replace outcomes. | Blob transport-send failures remain covered, not failures in subsequent SDK decoding, body iteration, authentication outside this pipeline, or execution. Retry deadline fixtures prove the decorator exposes the original configuration and preserves connection-timeout clamping. It neither buffers nor replaces the response and emits no stream/execution-completion event. Project/Blob header presence comes from the SDK mapping, not raw duplicate-preserving wire headers. Credential factories no longer use this decorator. |

Each request/attempt takes an immutable local observation alias and inherits
only existing safe operation/response aliases. Policy state is local to its
`send` coroutine; credential-hook state uses the public per-request pipeline
context, not a shared client/global identity. Synthetic overlapping requests verify
separate bindings. An alias does not establish a private join or identity.
Only method, fixed route/stage/role, presence, status, elapsed milliseconds and
fixed category reach the closed event projection. No exception text, concrete
URL/query/resource name, bearer/credential payload, user identity or hash is
logged. HTTP errors still reject normally; neither policy nor transport
authorizes anything or changes trusted context.

### Explicit integration handoffs and uncovered intervals (historical task handoff)

INTEGRATE/Scrum coordinates the remaining **application call-site wiring**
through the original Developer ownership. The accepted inventory already
identified these out-of-task factories; this is not a new diagnostic
architecture or permission to silently expand any task's owned paths:

* `architect_agent.py` and `reviewer_agent.py` create and inject separate Blob
  services. They still bypass the `BlobArtifacts` default factory. Select the
  public `blob_diagnostics_transport(role=...)` for each existing explicit
  transport, preserving that factory's exact options, and retain constructor/
  pipeline regressions. Until that handoff is implemented and tested these
  two injected services are **uncovered**, not PASS.
* `WorkflowRuntime._resources` in `workflow.py`, plus the specialist resource
  factories, still construct their own `ManagedIdentityCredential()`. Wire the
  reviewed `credential_diagnostics_options(role=...)` as public credential
  keyword options, **not a preconstructed transport**; preserve the existing factory
  ownership/lifecycle. Only `foundry.create_hosted_agent` is wired by this
  assignment. Do not label all application token acquisition covered.
* The SDK-owned session/history/checkpoint/workflow-binding/response stores
  in T/U/V remain uncovered at internal HTTP boundaries: their stock callers
  do not forward the application policies/transports. The original pinned
  source evidence above remains applicable. No private SDK edit/provider
  replacement has been introduced. Azure CLI subprocess internals, credential
  cache hits/unverified branches and Foundry platform resolution remain outside
  coverage. The authenticated outbound principal remains unproven.
* Refresh the shared repository index after integrating the new tests/module
  paths, preserving its pre-existing notes/edits. Original E2E still owns the
  final exact-join full checks; original DevOps owns Linux/package/publication,
  synthetic intent, live acceptance and attributable cleanup. No lab release
  tooling changed here. Historical rollback provenance remains WAIVED.

The retained `tests/test_sdk_diagnostics.py` fixtures exercise constructor
attachments through real pinned public SDK pipelines, not merely private
policy-list inspection. They include HTTP rejection, send failures, default
Identity retries, cache non-observation, concurrent policy/transport isolation,
context reset, cancellation, response/body ownership, private redaction,
machine-stdout isolation and diagnostic-failure containment. All credentials,
responses, identities and endpoints in these fixtures are synthetic.

### Executed SDK-POLICIES checks

Commands used the existing absolute linked-lab Python and, for the documented
application entry point, the explicit selected-feature lab root. No dependency
installation, live call, secret acquisition or lab tooling edit occurred.

| Check | Observed result |
| --- | --- |
| `python -m unittest discover -s tests -p test_sdk_diagnostics.py -v` (`OTEL_SDK_DISABLED=true`) | Final **16 tests PASS in 0.464 seconds**. The initial 13-test iteration had one fixture error: the synthetic Project session used `id`, while the pinned model exposes `agent_session_id`. The fixture was corrected to the actual model and public `VersionRefIndicator` contract. No runtime contract was weakened. |
| `./Test-Demo.ps1 -Python <linked-lab-root>/.venv/Scripts/python.exe -LabRepositoryRoot <selected-feature-lab-root>` | Final exit 0: **270 tests PASS in 60.749 seconds**, dependency check and compilation passed. An earlier run before three additional test cases passed 267 tests in 64.323 seconds. These are shared-checkout observations including concurrent host work, not final exact-source integration certification. |
| `./scripts/Test-Repository.ps1 -Python <linked-lab-root>/.venv/Scripts/python.exe` | **FAIL**, exit 1 at `REPOSITORY_INDEX_STALE`; later parser/public-boundary stages did not run. The already dirty shared index is outside this task's owned paths. INTEGRATE retains refresh/preservation and rerun, not a waived gate. |
| Owned `py_compile` and `git diff --check` | PASS for the SDK source/tests and owned documentation (compilation applies to Python only). |

Original Architect/Critic review of this implementation remains pending.
All remaining application call-site gaps above are explicit construction
handoffs; the original live identity interval and release conditions remain
unproven. No HTTP or SDK envelope result closes AC1-AC9/G1-G8.

## IP-S1 integration join

The original handoffs above remain historical. The current integration consumes
their **agreed** original Architect/Critic audits; it does not reopen them.
All seven commits below are verified ancestors on
`feature/customer-hosted-session-prototype`. No task code is abandoned or
retained on an unmerged branch.

| Task / source | Exact accepted ancestry |
| --- | --- |
| EVENT-CONTRACT | `20c315e1d51908f8cbc56598fbb36052972079e8` |
| SDK-INVENTORY | `b7b4e0e7f6d19d659a76720461d9aa948d95e9d7` |
| TRANSPORT | `9c8dfdf0956978f46dcd6340e2fcd8f58940f73b` |
| INGRESS-CONTEXT | `742e46abb0a3d86e93ed602b2303fe71784766bd`; attribution `743c9e6678ae3e53dd3f5adc7da167e4eac9f207` |
| SDK-POLICIES | `87de392d3bf38f824b5c8dd1c78916edc8290a98`; accepted correction `4c58849be950931212bb858477ef69720001f72e` |

### Closed application call sites

`WorkflowRuntime.resources`, `ArchitectAgent.connect_and_load_assignment`
and `ReviewerAgent.connect_and_load_assignment` now pass
`credential_diagnostics_options(role=...)` to their existing
`ManagedIdentityCredential` factories. Identity still selects its environment
branch and owns transport defaults/retries; no transport or timeout is supplied
by these factories. Credential raw hooks retain the previously documented
send-error/cancellation, cache-hit and unverified-branch observation gaps.
Both specialists now inject `blob_diagnostics_transport(role=...)` into their
existing Blob service constructors. This is the smallest directly coupled
call-site completion named by the accepted SDK-POLICIES handoff, not a change
to specialist business logic. The wrapper retains the original
`AioHttpTransport(use_env_settings=False)` and connection configuration.
The same existing `AsyncExitStack` owns each credential, Project/HTTP client
and Blob service; no new service, dependency or retry is introduced.

`tests/test_profiling_integration.py` exercises the actual pinned injected
specialist Blob clients and workflow default Blob client against synthetic
Azure Core transports. It verifies role-attributed bounded events, credential
constructor hook-only options, transport closure and unchanged propagated
rejection. Retained `test_workflow` and `test_isolated_client` fixtures now
assert the public helper/hook seam while preserving their original cases.
The accepted SDK tests retain real synthetic credential branch/configuration
and retry-deadline comparisons; the new factory fixtures do not claim token
acquisition or private-network verification.

### Package closure and remaining interval

The retained selected-feature lab's public
`foundry-tf/multi-agent/release_roots.py:ReleaseRoots.runtime_files` includes
every application `demo/*.py`. Its actual method was exercised with explicit
application/lab roots and includes `demo/diagnostics.py` and both routing config
files. `bundle_package.runtime_archive` consumes that closure and `prepare`
checks it against source; these functions were inspected, **not executed**.
The application `.agentignore` and `.dockerignore` already allow `demo/*.py`,
and Dockerfile copies `demo` intact. No allowlist, `package_guard.py` or lab
tooling change is necessary. These offline closure checks are not an archive,
Linux-image, version, trusted-host, publication or current-effect receipt.

The event API remains `demo.diagnostics`' closed enums and frozen `Event`,
`Observation`/`Binding`, `observe_header`/`observe_value`, `compare_values`,
`bind`/`current_binding` and failure-isolated `emit`; see the accepted
`tests/test_diagnostics.py` fixtures. Host context checkpoints never populate
trusted scope. Outbound send/headers, stream end, ASGI final body and execution
context are independent observations, not a successful business outcome.
SDK-owned stores T/U/V, CLI internals and Foundry platform identity resolution
remain uncovered as previously evidenced. No authenticated principal, identity
translation/root cause or supported remediation is established locally.

The exact originating dispositions
`["yaml-loops-v1:sprint/1/IP-S1/task/IP-S1-SDK-POLICIES/AssignedWorkDeveloperLoop","SDK-CREDENTIAL-TIMEOUT-PRESERVATION"]`
and
`["yaml-loops-v1:sprint/1/IP-S1/task/IP-S1-SDK-POLICIES/AssignedWorkDeveloperLoop","SDK-TIMEOUT-REGRESSION-EVIDENCE"]`
remain applied through the accepted correction and retained combined tests;
they are not broadened into new requirements or waived.

Original Architect/Critic review of this integration is next. Original E2E
then owns the exact reviewed join's documented full verification, and original
DevOps owns Linux/hosting/package gates, guarded common-package publication
to all three roles, separately identified synthetic intent/live evidence and
attributable cleanup. Original review/retro/closeout and AC1-AC9/G1-G8 remain
required. Historical rollback provenance remains **WAIVED**, never PASS.
The held original parent and all unknown effects are untouched. No package
creation, deployment, live call, secret retrieval or dependency install occurs
in this integration.

### Integration verification and reproducible handoff

All commands execute from the application repository. Use the existing
absolute linked-lab Python and selected-feature lab root from the private
execution input; do not substitute a production profile. For the combined
focused suite set `OTEL_SDK_DISABLED=true` and `AZURE_LAB_SOURCE_ROOT` to the
explicit selected lab's `foundry-tf/multi-agent` directory, then:

```python
import sys, unittest
sys.path.insert(0, "tests")
import test_demo
names = [
    "test_diagnostics", "test_transport_diagnostics", "test_host_diagnostics",
    "test_sdk_diagnostics", "test_profiling_integration", "test_workflow",
    "test_isolated_client",
]
result = unittest.TextTestRunner(verbosity=1).run(
    unittest.defaultTestLoader.loadTestsFromNames(names)
)
raise SystemExit(not result.wasSuccessful())
```

| Executed check | Observed integration result |
| --- | --- |
| Combined focused command above | Final **137 tests PASS in 6.252 seconds** (preceding run: 7.595 seconds); includes actual pinned resilient background dispatch, concurrent isolation, redaction/header states, stream/disconnect/cancel/close, rejection, credential defaults/retry deadline, known-response-only recovery and new factory/closure fixtures. |
| Standalone `python -m unittest discover -s tests -p test_profiling_integration.py -v`, with the explicit lab linkage above | Final **4 tests PASS in 0.257 seconds**, including both specialists' actual Blob pipelines and unchanged synthetic rejection. |
| `./Test-Demo.ps1 -Python <absolute-existing-python> -LabRepositoryRoot <explicit-selected-lab-root>` | Final exit 0: **278 tests PASS in 53.398 seconds** after the standalone-bootstrap correction; `pip check` and Python compilation PASS. The preceding run passed 278 in 61.309 seconds. Includes retained deterministic routing, immutable outputs/exact refs, ETag/fencing, checkpoints, unknown-effect holds and terminal/parser tests. |
| Existing Python `scripts/repo_index.py`, then `./scripts/Test-Repository.ps1 -Python <absolute-existing-python>` | Exit 0: generated inventory current; public/private boundary reports 113 checked public files; JSON, PowerShell, context frontmatter and whitespace PASS. |
| Task commit ancestry and owned-path whitespace | All seven task commits above are ancestors of the integration baseline; whitespace PASS. No merge, branch switch, push or abandonment needed. |

Two standalone new-fixture runs passed three cases but failed the workflow
case at `CANDIDATE_PARENT_BINDING`: imports retained an inherited endpoint;
`setdefault` could not override it. Following the retained `test_demo`
bootstrap, this fixture now explicitly selects synthetic configuration before
application imports rather than inheriting operator endpoint settings.
The combined and full documented runs above passed with their synthetic
bootstrap; final verification below covers the corrected standalone case too.
The production trust gate is unchanged.

The pre-existing untracked profiling specification is not owned or committed
by INTEGRATE. Its pre-existing inventory line remains a working-tree overlay;
the committed index includes this task's additions/notes without absorbing that
line or rewriting earlier notes. Repository validation above includes the
preserved overlay. Runtime source/tests are the integration commit's exact
files; final original E2E must independently verify the reviewed join. Suite
durations are unittest timings, not total model/task usage.

### Timeout-preservation correction

Applies the exact originating required references
`["yaml-loops-v1:sprint/1/IP-S1/task/IP-S1-SDK-POLICIES/AssignedWorkDeveloperLoop","SDK-CREDENTIAL-TIMEOUT-PRESERVATION"]`
and
`["yaml-loops-v1:sprint/1/IP-S1/task/IP-S1-SDK-POLICIES/AssignedWorkDeveloperLoop","SDK-TIMEOUT-REGRESSION-EVIDENCE"]`.
The original tests above remain historical results, not proof of preserved
timeouts. Critic's source finding confirmed that supplying an eagerly constructed
transport skipped Identity's branch-specific construction. The decorator also
hid `connection_config` from Azure Core's retry deadline calculation.

The correction uses the already inventoried public raw hooks rather than
replicating environment selection or applying IMDS settings to all credentials.
Pinned references: Identity `aio/_credentials/imds.py:45-60` and
`_internal/pipeline.py:69-96`; Azure Core
`pipeline/policies/_custom_hook.py` (`CustomHookPolicy`) and
`pipeline/policies/_retry.py:359-390` (`_configure_timeout`).
No SDK/private patch, branch-selection replacement or dependency change is used.
Raw hooks have no send-error/cancellation callback. This explicit uncovered
credential interval replaces the former decorator's error coverage; the Blob
decorator and Project policy still observe their respective errors.
An incomplete credential pair must never authorize, retry, or infer an outcome.

Offline regressions compare uninstrumented/instrumented IMDS and App Service
factory configuration and actual synthetic retry attempts, including remaining
budget clamping. They retain synthetic cache, redaction, failure containment and
concurrent binding cases, plus propagation of cancellation with no invented
completion/error event. Test fixtures replace only network I/O and use no real
credential acquisition. Integration must consume the corrected options API.

Correction checks (existing absolute linked-lab Python; explicit selected-feature
lab root for `Test-Demo.ps1`):

| Check | Observed correction result |
| --- | --- |
| `python -m unittest discover -s tests -p test_sdk_diagnostics.py -v` with `OTEL_SDK_DISABLED=true` | **20 tests PASS in 0.459 seconds**. Initial 19-test iteration failed because the fixture passed the operation budget via `get_token`, which IMDS does not forward. The fixture now supplies the supported credential constructor timeout to both baseline and instrumented cases; both prove 1 then 0.75-second clamping. No runtime contract was relaxed. |
| `./Test-Demo.ps1 -Python <linked-lab-root>/.venv/Scripts/python.exe -LabRepositoryRoot <selected-feature-lab-root>` | Exit 0: **274 tests PASS in 46.620 seconds**, dependency check and compilation passed. Shared-checkout result, not final integration/E2E certification. |
| `./scripts/Test-Repository.ps1 -Python <linked-lab-root>/.venv/Scripts/python.exe` | **FAIL** at `REPOSITORY_INDEX_STALE`; subsequent stages did not run. Existing shared index edits remain untouched; INTEGRATE owns refresh and exact-join rerun. |
| Owned whitespace check | PASS. |

Return this correction to the original Architect/Critic reviewers. Their prior
votes on `87de392` are not collective acceptance of the new correction.
