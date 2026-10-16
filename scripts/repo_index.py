from __future__ import annotations

import argparse
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / ".github" / "repo-index.md"
START, END = "<!-- inventory:start -->", "<!-- inventory:end -->"
PRIVATE = {".azure", ".azure-cli", ".local", ".migration", ".foundry", ".venv"}


def render() -> str:
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
    current = INDEX.read_text(encoding="utf-8")
    if current.count(START) != 1 or current.count(END) != 1:
        raise RuntimeError("INDEX_MARKERS_INVALID")
    before, tail = current.split(START)
    _, after = tail.split(END)
    inventory = "\n\n## Public file inventory\n\n" + "\n".join(
        f"- `{name.replace('/', chr(92))}`" for name in names
    ) + "\n\n"
    return before + START + inventory + END + after


def main() -> None:
    parser = argparse.ArgumentParser(description="Deterministic public file inventory; no network.")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = render()
    if args.check:
        if INDEX.read_text(encoding="utf-8") != expected:
            raise RuntimeError("REPOSITORY_INDEX_STALE: run scripts\\repo_index.py")
        print("Repository index is current.")
    else:
        INDEX.write_text(expected, encoding="utf-8", newline="\n")
        print("Repository index refreshed.")


if __name__ == "__main__":
    main()
