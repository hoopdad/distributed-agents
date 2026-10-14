# Copy-first migration and no-loss handoff

## Boundary

The application is split, not destructively moved. The Azure lab's
`foundry-tf\multi-agent` directory remains the rollback baseline and current
deployment source until cross-repository release support and live acceptance
are complete. `distributed-agents` becomes the portable application owner.
No Terraform, registry, VPN configuration, SSH identity, or production token
cache belongs in this repository.

| Source category | Disposition |
|---|---|
| `demo` modules, `main.py`, hosted entry point, metadata | Copied; endpoint/model configuration made generic |
| Requirements/lock, Dockerfile, agent/package allowlists | Copied with existing pins and packaging controls |
| Terminal and exact-origin native proxy | Copied; explicit environment scope, private state boundary and generic endpoint |
| Core offline tests, test runner, synthetic live acceptance utility | Copied; synthetic fixtures and optional explicit linkage to retained lab wrapper tests |
| Terraform, registry, network/DNS/VPN, local Bastion/SSH startup | Remain in lab; not copied into public application |
| Code/bundled build tools, WSL release/auth, release tests, observer, lab preflight/connectivity, original documentation | Remain in lab with all safety behavior intact |
| `.azure` azd environment state | Explicitly authorized private local copy, Git-ignored, hash-verified |
| `.azure-cli`, `.venv`, keys, session files, Terraform state | Not copied |

`migration-map.json` exhaustively classifies **35 ordinary source files**:
19 portable and 16 retained. It lists each portable adaptation and frozen source
hashes. New configuration, documentation and automation are additions, not
replacements for unaccounted source. A private byte-identical snapshot of all
35 files is kept under `.migration\baseline`. The private azd copy has five
files; its hashes and validation receipt remain in `.migration`.

The original lab worktree had pre-existing changes and an added quickstart.
Those exact files were inventoried and preserved; this migration does not
stage, revert, edit, or remove them.

## Preserved capabilities

Preserve strict candidate/review schemas; revision invalidation; all existing
core test case names; model-output parsing regressions; child session/version
binding; response-ID recovery; uncertain-effect holds; conditional Foundry
storage updates; identity/header scoping; exact-origin HTTP/HTTPS and SOCKS
transport; streaming/final event compatibility; and terminal owner/private-file
checks. `demo\coordinator.py` and hosted entry-point wiring are copied unchanged.

Release safeguards stay where they are: approved ZIP/hash matching,
allowlisted package contents and dependencies, Linux-native/ELF checks,
fresh Linux test execution, locked dependency provenance, strict host
fingerprints, read-only temporary SSH mounts, bounded cgroup process cleanup,
private evidence, publish scope/version approval, and unknown-send
reconciliation. The bundled fallback is retained, not replaced by an untested
remote-build shortcut.

Two Windows-only tests in the portable suite exercise lab-specific scripts
through `AZURE_LAB_SOURCE_ROOT`, set only by the explicit runner argument.
Without that argument they are reported as skipped, not silently relocated.
`tests\test_release.py` remains in the lab suite. Both suites are required for
the handoff and future release-tool changes.

## Deliberate adaptations

The target requires explicit Foundry project URL and model deployment aliases.
Synthetic architecture facts replace lab identifiers in portable code. Terminal
authentication requires explicit expected tenant/subscription and an existing
dedicated absolute CLI profile rather than reading an implicit lab-relative
registry. The proxy derives its exact allowed origin from the same validated
project configuration. The terminal's private session path boundary now
covers the new repository root.

The three-service descriptor now selects native orchestration and remote
specialists. The legacy `in_process` implementation remains a regression adapter;
the native descriptor is not evidence of a live redeployment.

## Private context and future cutover

`.local\lab-settings.json` links the external lab root, registered region,
tenant/subscription, project endpoint, model aliases and dedicated lab CLI
profile. It contains no copied CLI token cache and is not a publication
artifact. `Use-Settings.ps1` imports only allowlisted validated values.
Do not read/display `.azure` `.env` contents or import their entire environment.
The copied azd state can aid a reviewed future deployment; it does not grant
mutation permission or correct hardcoded release paths.

The retained release/build/preflight/WSL scripts now accept separate
**ApplicationRoot** and **LabRepositoryRoot** inputs, with offline and actual
Linux checks. Native bundled packaging and publication still require their
own gates; a project staging parameter alone never establishes source closure.
Keep infrastructure lookup in the lab and code/package/test lookup in the
new application. Preserve exact approved package hashes and closure receipts.

Only after live acceptance should documentation identify the new root as the
deployment source. Keep old deployed versions for explicitly scoped rollback
and old session compatibility. Do not prune either repository's originals,
azd state, or pending session evidence during this migration.

## Deterministic verification

After final portable adaptations, run:

```powershell
$python = '<absolute-path-to-validated-python>'
$lab = '<absolute-lab-repository-path>'
.\Test-Demo.ps1 -Python $python -LabRepositoryRoot $lab
& (Join-Path $lab 'foundry-tf\multi-agent\Test-Demo.ps1') -Python $python
& $python .\scripts\migration.py seal
& $python .\scripts\migration.py verify `
    --source-root (Join-Path $lab 'foundry-tf\multi-agent')
& $python .\scripts\migration.py public-check
```

`stage` has already completed for this handoff. Do not rerun it over adapted
files: it intentionally refuses differing destinations. `seal` declares the
current target hashes; `verify` compares original files and the private snapshot
to frozen hashes, portable files to the sealed hashes, and original/copied
private azd files to their private receipt. It also scans tracked and
nonignored untracked files for private directories, key/package files and known
lab identifiers derived from private settings. This boundary scanner is a
focused guard, not a universal secret detector.

The frozen snapshot check is a **migration gate**, not a permanent prohibition
on later application development. After implementation, preserve the source
baseline and use a separately versioned implementation/release manifest; do
not overwrite historical hashes to conceal code changes. If the lab originals
change independently, report that drift rather than resealing it as unchanged.

## Handoff verification results

Checks completed on 2026-10-14 using the existing validated external Python
3.12.10 environment; no dependencies were installed. The hosted runtime
descriptor remains Python 3.13, so these Windows results are not a substitute
for the retained native Linux/Python 3.13 packaging gate before deployment.

| Check | Measured result |
|---|---|
| Portable suite with explicit lab regression linkage | 47 tests passed; all 41 original core test case names retained, plus 6 configuration/boundary tests |
| Unchanged original lab suite, including release cases | 57 tests ran successfully; 3 platform-specific Linux checks skipped on Windows |
| Dependency/compilation checks | Both dependency checks passed; applicable Python modules compiled |
| Original source and private baseline hashes | All 35 ordinary source files unchanged and preserved |
| Sealed portable hashes | All 19 copied portable files verified; 8 declared adaptations accounted for |
| Authorized private azd copy | All 5 original/copied files match; Git exclusions confirmed |
| Public bootstrap checks | 44 Git-visible files checked; index, JSON, PowerShell, agent/skill frontmatter, whitespace and focused private-boundary checks passed |
| External lab worktree | Existing dirty paths preserved; no migration edits to the original application or release scripts |

The host construction test exposes the baseline SDK's disabled response
resilience warning, now recorded in the design as a next-iteration requirement.
It does not establish durable live response recovery. The pre-existing SOCKS
test also emits a transport `ResourceWarning` while passing; this handoff does
not claim to fix that unrelated baseline behavior.

No live Azure calls, resource changes, agent publication, commit or push were
performed. New application/context files are local worktree changes ready for
the next session, not yet published to origin. Source deletion and CLI token
cache copying were both verified false.
