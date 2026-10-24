from __future__ import annotations

import argparse
from fnmatch import fnmatchcase
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / ".github" / "repo-index.md"
HISTORY = ROOT / ".github" / "repo-history-index.md"
START, END = "<!-- inventory:start -->", "<!-- inventory:end -->"
SCOPE_START, SCOPE_END = "<!-- search-scope:start -->", "<!-- search-scope:end -->"
PRIVATE = {".azure", ".azure-cli", ".local", ".migration", ".foundry", ".venv"}


def search_exclusions(current: str) -> list[str]:
    if current.count(SCOPE_START) != 1 or current.count(SCOPE_END) != 1:
        raise RuntimeError("SEARCH_SCOPE_MARKERS_INVALID")
    scope = json.loads(current.split(SCOPE_START)[1].split(SCOPE_END)[0])
    patterns = scope["ignore"]
    if not isinstance(patterns, list) or any(
        not isinstance(pattern, str) or not pattern or
        pattern.startswith(("/", "\\")) or ":" in pattern or
        ".." in pattern.replace("\\", "/").split("/")
        for pattern in patterns
    ):
        raise RuntimeError("SEARCH_EXCLUSIONS_INVALID")
    return [pattern.replace("\\", "/") for pattern in patterns]


def is_historical(name: str, patterns: list[str]) -> bool:
    return any(fnmatchcase(name.replace("\\", "/"), pattern) for pattern in patterns)


def inventory(current: str, names: list[str]) -> str:
    if current.count(START) != 1 or current.count(END) != 1:
        raise RuntimeError("INDEX_MARKERS_INVALID")
    before, tail = current.split(START)
    _, after = tail.split(END)
    entries = "\n\n## Public file inventory\n\n" + "\n".join(
        f"- `{name.replace('/', chr(92))}`" for name in names
    ) + "\n\n"
    return before + START + entries + END + after


def public_files() -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        check=True, capture_output=True,
    )
    names = sorted({
        name.decode("utf-8") for name in result.stdout.split(b"\0")
        if name and (ROOT / name.decode("utf-8")).is_file()
    })
    if any(any(part in PRIVATE for part in Path(name).parts) for name in names):
        raise RuntimeError("PRIVATE_PATH_VISIBLE_TO_GIT")
    return names


def render() -> dict[Path, str]:
    names = public_files()
    current = INDEX.read_text(encoding="utf-8")
    patterns = search_exclusions(current)
    historical = [name for name in names if is_historical(name, patterns)]
    active = [name for name in names if not is_historical(name, patterns)]
    return {
        INDEX: inventory(current, active),
        HISTORY: inventory(HISTORY.read_text(encoding="utf-8"), historical),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Deterministic public file inventory; no network.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--search-files", action="store_true",
                      help="List current public search paths, excluding opt-in history.")
    args = parser.parse_args()
    if args.search_files:
        patterns = search_exclusions(INDEX.read_text(encoding="utf-8"))
        print("\n".join(name.replace("/", "\\") for name in public_files()
                        if not is_historical(name, patterns)))
        return
    expected = render()
    if args.check:
        for path, text in expected.items():
            if path.read_text(encoding="utf-8") != text:
                raise RuntimeError(f"REPOSITORY_INDEX_STALE: {path.name}; run scripts\\repo_index.py")
        print("Repository indexes are current.")
    else:
        for path, text in expected.items():
            path.write_text(text, encoding="utf-8", newline="\n")
        print("Repository indexes refreshed.")


if __name__ == "__main__":
    main()
