# Client and release boundary: RP-S1 projection and evidence architecture

Derived from [RP-S1 sprint architecture](../../customer-prototype-sprint-architecture.md)
and the accepted [SprintDesign](../../customer-prototype-sprint-design.md).
This logical tier adds neither a service nor a release owner.

## Presentation contract

[`demo/terminal.py`](../../../demo/terminal.py) remains the Windows terminal.
`--view human` is proposed, not implemented by this document. Developer implements
the accepted opt-in view on stderr; identical input keeps identical stdout,
existing default behavior, delegation/result schemas and
[`live_acceptance.py`](../../../live_acceptance.py) parsing unchanged.

Use complete parsed records, preserve repeated calls in order, and finalize
before an accepted summary. Fragmented/recovered prefixes cannot become duplicate
invocations; missing/multiple/malformed results or pending effects cannot become
success. Known-response retrieval is not a new send. Human content includes
current useful design and review findings, not only session labels.

Existing public events expose aliases, not enough exact evidence for a VERIFIED
continuity or creation-count assertion. With those events alone display
unverified/not observed. Do not add raw IDs, external reads or another comparison
ledger just to strengthen the display. Private acceptance compares exact actual
bindings separately. Neutralize terminal controls and prefix every generated
line; support narrow widths and non-color status labels.

[`README.md`](../../../README.md) opens with customer goal, three-role diagram,
two-turn example, stable bindings versus advancing responses, source path and
truthful historical live status. Keep chronology in the recovery plan.
Shareable commands use synthetic input, private state, safe aliases and only
implemented syntax. Follow-up requires a completed, non-held first turn.

Developer doneWhen: implemented view/README plus fixtures for stdout/parser
compatibility, missing evidence, fragmented/recovered streams, finalization,
holds and hostile/multiline content. Designer reviews against accepted screens.
No browser UI, parser replacement, live success from aliases or CLI stop command.

## Fresh inventory and supported-remedy research

DevOps validates sole-target settings/linkage and authenticated lab context
without displaying private values, then records fresh versions, identities,
packages, rollback and unresolved operations through retained tools.
Architect/Developer research source/date/version-specific supported remedies;
historical matching call context/missing trusted user is unresolved, not proof
of missing RBAC or a provider defect.

Research doneWhen: supported correction with a concrete reproducer and held-state
implications, or actionable negative finding specifying the missing exact-pair
caller-resolution trace/documented remedy. No provider submission/private transfer,
speculative publication, new permission/network/infra or uncertain-effect replay.
Completed research does not pass the live release goal.

## Release ownership and later gates

Original DevOps exclusively owns retained packaging, preview, WSL publication
and live testing with explicit ApplicationRoot/LabRepositoryRoot. Serialize
publisher/shared CLI/stage and transport/mount resources. Preserve strict SSH,
read-only mount, private evidence outside both repositories, exact source/settings/
ZIP hashes, allowlists, dependency provenance, actual Linux/amd64/hosting-Python
checks, unchanged identities, rollback versions and owned cleanup.

RP-S2 requires one final common three-role bundle, real remote accepted outputs,
private MI artifact provenance and genuine Decision-1 (G1-G4). RP-S3 requires
exact two-turn binding/response proof (G5), once-only supported compute stop/resume
with marker and confirmed stopped/idle state/no duplicate effects (G6), distinct
parent children/artifact scope (G7), and truthful closure (G8). This is not
hard-crash or exactly-once deployment certification.

Final AC1-AC9 reporting distinguishes offline, Linux-package and live evidence,
records exact final/rollback bindings, setup/demo command and unverified limits.
Preserve original publication UNKNOWN, held parents, historical cleanup uncertainty
and account-wide Blob Contributor's application-only isolation limitation.
Reviewed scoped commits/push and source reconciliation remain downstream.
