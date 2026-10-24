---
name: repo-index
description: Read and deterministically refresh this repository's bounded source index before search.
---

Read README, `.github\copilot-instructions.md` and `.github\repo-index.md`
before searching. Use the index's areas to select exact files instead of broad
recursive scans. Private context and external lab sources are not indexed.
Honor the main index's `ignore` field: `scripts\repo_index.py --search-files`
lists current public paths without opt-in history. Do not search excluded paths
by default. Open `.github\repo-history-index.md` only for a specific provenance
question arising from current evidence, then select exact historical paths.
Historical failures and planning handoffs do not establish current blockers.

Run `scripts\repo_index.py --check` using an explicitly available Python.
If stale or absent, run the script without `--check`, then read the index.
Refresh after file additions/deletions and update the architecture summary
manually when responsibilities change. The script does not install dependencies
or make network calls.

Do not search `.azure`, token caches, private evidence, keys or session files.
The checked-in migration map identifies retained external lab tooling; resolve
its actual root only through ignored private settings and user scope.
