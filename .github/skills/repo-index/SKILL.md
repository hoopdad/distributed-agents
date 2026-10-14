---
name: repo-index
description: Read and deterministically refresh this repository's bounded source index before search.
---

Read README, `.github\copilot-instructions.md` and `.github\repo-index.md`
before searching. Use the index's areas to select exact files instead of broad
recursive scans. Private context and external lab sources are not indexed.

Run `scripts\repo_index.py --check` using an explicitly available Python.
If stale or absent, run the script without `--check`, then read the index.
Refresh after file additions/deletions and update the architecture summary
manually when responsibilities change. The script does not install dependencies
or make network calls.

Do not search `.azure`, token caches, private evidence, keys or session files.
The checked-in migration map identifies retained external lab tooling; resolve
its actual root only through ignored private settings and user scope.
