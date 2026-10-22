# Typed checkpoint export: pinned public round-trip qualification

## Result and task boundary

**IP-S2-C1-TYPED-CHECKPOINT-EXPORT** qualifies a public local-file round-trip,
but **does not close the original persisted-encoding/aggregate attachment
interval**. This is an actionable bounded qualification result, not a runtime
collector, supported recovery PASS or an SDK/platform defect diagnosis.

Consumed accepted collection qualification `6e63951790af3d4b199e15f97fa1891eef4550c5`
and its actual-host negative finding, rather than repeating its generic seam
inventory. Opened originating audit
`gh-dynamic-workflows/.delivery-runs/eef04e5c-c5ab-4b88-90f6-4a99dd4692ed/context/91007b1bf7e28ab1ab8fa9dcf0a9db9a4da5e6c394f78b1073dd1bf9fb0db8f3.json`:
Architect/Critic agree and mark that bounded task complete. Current scope is the
typed-export row of `docs/customer-prototype-profiling-s2-continuation-1-architecture.json`
and its separate sprint-plan task. Initial inspected feature HEAD was
`cda8de2ae779d18ca910485c007770714704be55`.

Only this document and `tests/test_typed_checkpoint_export.py` are owned here.
Integration exclusively owns the shared index, package-closure fixtures and
full joined checks. No pins, schema, dependencies, validator, runtime or lab
source are changed by this task. Other parallel source work is not adopted.

## Exact executed interval

The new actual-host fixture executes the pinned unmodified
`ResponsesHostServer` in-process using `httpx2.ASGITransport`, public
`prepare_options`, public `CheckpointStoreProvider.get_store_for_scope`, and
resilient local background dispatch. It reuses the accepted harness's owned
temporary state root/stream cleanup. Only application cloud business work is
synthetic; no private SDK method or codec is imported, called or patched.

Two distinct synthetic responses have request-local response/scope associations
and distinct opaque provider contexts. After terminal completion, the fixture
uses each captured **actual store**, not a context/store name reconstructed
from hashes, to list and `load_with_hash` the real native architect checkpoints.
This is a specialist workflow, **not** actual coordinator collaboration or a
cloud stop/resume. Its synthetic local SDK identity is not authentication proof.

Observed focused run:

- Two scoped background responses; four complete native checkpoints.
- Eight nested `WorkflowInvocationKwargs` instances across the full records.
- Each checkpoint's entire `to_dict()` equals the value restored using public
  `FileCheckpointStorage.save/load`. No fields are removed or normalized:
  messages, state, pending events, metadata, graph, IDs, lineage, timestamp,
  iteration and version all participate in equality.
- An additional nonempty typed fixture preserves global/executor kwargs,
  tuple and byte values. An empty invocation-wrapper success alone would not
  establish those semantics.
- Original scoped store `load_with_hash` is repeated after the file round-trip;
  full decoded state and exact original persisted-encoding hash are unchanged.
  Public `validate_checkpoint_value` accepts each native record, but returns
  no encoded snapshot.
- All four local file encodings' canonical JSON hashes happened to match the
  original store hashes in that run. **Observed equality is not a canonical
  re-encoding guarantee.** The SDK explicitly documents why re-pickling loaded
  state is not a canonical way to recover original persisted bytes.
- All file reads are limited to the explicitly owned empty temporary export
  directories populated by public `FileCheckpointStorage.save`. The fixture
  reads their SDK-written JSON, not guessed Foundry state paths. The public
  file loader, not an application decoder, reconstructs the typed state.
  Temporary exports and the host state root are removed and fixture diagnostics/
  backend settings restored. No socket listener or child process is created.

## Supported versus unsupported public boundaries

| Public operation | Executed result / exact limitation |
| --- | --- |
| `FoundryCheckpointStore.load_with_hash(id)` on an already captured scoped store | Returns full typed checkpoint and hash of the **original encoded storage value**. Preserves original scope association externally; does not export that encoded value. |
| `WorkflowCheckpoint.to_dict/from_dict` | Shallow dataclass conversion only. It neither recursively encodes nor decodes `WorkflowInvocationKwargs` or `WorkflowMessage`. |
| `FileCheckpointStorage.save/load` in fixture-owned local directories | Full typed round-trip succeeds under the default restricted decoder with no custom type registration. The saved JSON is a persistence encoding, not the decoded checkpoint comparison state. Saving a loaded Foundry checkpoint is a **new encoding**, even when the tested hashes match. |
| `CheckpointStoreProvider.validate_checkpoint_value` | Successfully validates the actual typed values through the SDK's restricted path, but exposes neither the encoded value nor a public decoding operation for callers. |
| `AgentSession.to_dict` wrapping a typed checkpoint | Emits the pinned unsupported-type warning and leaves the invocation wrapper as an object. Strict JSON still raises `TypeError`; this is not an alternate public checkpoint codec. No custom `register_state_type` encoder is added. |
| `register_checkpoint_type` / `allowed_checkpoint_types` | Deserialization allowlists, not serialization/export callbacks. Framework types already round-trip through file storage; expanding the allowlist does not solve public original-encoding export. |

### Reproducible negative interval

1. The actual checkpoint has typed invocation values. Direct strict JSON of
   those values raises `TypeError: Object of type WorkflowInvocationKwargs is
   not JSON serializable`. Whole-record JSON also fails; depending on record
   traversal it can encounter `WorkflowMessage` first. The first fixture run
   exposed exactly that distinction; the corrected regression tests both the
   whole record and the specific invocation objects, without relying on which
   field JSON visits first.
2. The SDK file is JSON-compatible, but `WorkflowCheckpoint.from_dict` on its
   encoded content **does not decode** the state. Its state differs from the
   full typed state returned by `FileCheckpointStorage.load`. Supplying those
   encoded rows to the unchanged aggregate could compare encoding-shaped data
   rather than actual checkpoint state; this task does not do so or assert that
   the validator would detect every such substitution.
3. `load_with_hash` supplies the correct original hash, not a public original
   encoded snapshot. A file re-save is useful lossless local persistence, but
   cannot unconditionally be labeled the original exact encoding. Hashing
   `str(typed_state)`, guessing paths or invoking the SDK private codec would
   not close that interval.

`live_acceptance.py` retains its complete-record equality/graph/ID comparisons
at the recovery join. No lossy projection, `default=str`, custom codec,
pickling by the application, encoded-state substitution or validator waiver
is implemented. Local specialist checkpoints are not fabricated coordinator
`distributed-agents-v1` aggregate inputs. Recovery equality remains required.

## Exact source and version anchors

Executed with the existing explicit Python **3.12.10**, without installation.
Installed versions match the current manifest:
`agent-framework-core==1.21.0`,
`agent-framework-foundry-hosting==1.0.0b261002`,
`azure-ai-agentserver-core==2.2.0`,
`azure-ai-agentserver-responses==2.3.0`.

Paths below are relative to that interpreter's `site-packages`. Underscored
paths are read-only implementation references behind public APIs, not hooks.

| Source | SHA256 |
| --- | --- |
| `agent_framework/_workflows/_checkpoint.py` (`WorkflowCheckpoint`, `FileCheckpointStorage`) | `b00f0624c8c2f689c2c1583370f7b9a578a2c2ea612044268888a5c60e040d4d` |
| `agent_framework/_workflows/_workflow.py` (`WorkflowInvocationKwargs`) | `f46606a08831f298c9febdf5de86ce4ef44a49dcbbb86ebc70eadad3583515cf` |
| `agent_framework/_sessions.py` (`AgentSession` serialization) | `70b3c42341472430160befec538b6c917aaafb4a67bd19e071b1625bd241149c` |
| `agent_framework_foundry_hosting/_state_store.py` (scoped persistence, original hash, validation) | `8b7dcc45484f2a10f2b460bf51e40c1d6c4bea174bc4728c77d667a4294754ac` |
| `agent_framework_foundry_hosting/_responses.py` (public host options/provider) | `a8655a2a2cb4cd2702a009f76c5680b39a30e2dcc25d9fbd5e175b87da7dd5ad` |

These are inspected source anchors, not package/release seals. No positive
Python 3.13/Linux or cloud certification follows from this Windows fixture.

## Smallest receiving handoff

**IP-S2-C1-OBSERVATION-INTEGRATION / original Architect and Scrum Master:**
consume the tested positive local typed persistence interval and the exact
remaining negative above. Independent reader/transport adapters can integrate;
this qualification does not gate them. Keep this result negative for
unconditional original-encoding/aggregate export, not a recovery PASS.

For an exact pinned SDK capability handoff, the missing operation is a public
export of an **already attributed existing checkpoint's original JSON-compatible
encoded value and its acknowledged hash**, paired with a supported public
restricted restore yielding the complete typed checkpoint. It must preserve
the externally captured response/scope/context association; no remote
get-or-create probing, name derivation, credential acquisition or custom
deserializer. Equality must remain over complete decoded state, graph and IDs,
not encoding-shaped substitutes. This names a capability, not a request to
patch/upgrade the SDK or submit an external case.

A separately approved fail-closed file bridge could compare each re-encoded
snapshot hash to the captured original hash and reject every mismatch; this
test establishes four matching samples only. No universal determinism or
runtime bridge is approved by these samples. Any essential encoding envelope,
SDK pin or aggregate-contract change belongs to the existing Architect/Scrum
scope decision (`needs-replan` for that change), not this qualification's hidden
implementation.

Original reviewers remain Architect/Critic. The integration owner refreshes
the index and runs `Test-Demo.ps1` with the existing absolute Python and explicit
selected-lab root, then `scripts/Test-Repository.ps1` on the actual joined source.
Full checks are deliberately not run concurrently in this initial task, per
the accepted sprint-plan governance. Existing E2E/DevOps own subsequent
exact-source release and actual comparison evidence.

Prior references
`["yaml-loops-v1:sprint/1/IP-S1/DevOpsWorkLoop","RELEASE-COMMON-PACKAGE-PUBLICATION"]`
and
`["yaml-loops-v1:sprint/1/IP-S1/DevOpsWorkLoop","RELEASE-LIVE-ACCEPTANCE"]`
remain required in their original boundaries. Other accepted timeout,
changed-join and planning dispositions are not reopened or superseded.
Native denial, held parents, UNKNOWN effects and original live requirements
remain untouched. Historical COMMON rollback provenance remains **WAIVED,
never PASS**. No native retry, remote operation, package, publication, live
stop/resume, push or external upload occurred.

## Focused verification

From the application root, using the existing explicit Python:

```powershell
& '<existing-absolute-python>' -m unittest discover -s tests -p test_typed_checkpoint_export.py -v
```

Four tests passed in **1.007 seconds** after correcting the test-only assumption
about JSON's first failing typed field. The final rerun and source/whitespace
verification are recorded in the Developer handoff/commit. No baseline fixture
was removed. Full joined application/repository checks remain integration's
handoff, not claimed here.
