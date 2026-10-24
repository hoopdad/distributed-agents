"""Offline source checks for normal azd remote_build; never uploads or approves a ZIP."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import stat


ROOT = Path(__file__).resolve().parents[1]
INDEX = "--index-url https://packagefeedproxy.microsoft.io/pypi/simple"
IGNORE_RULES = (
    "*", "!main.py", "!requirements.txt", "!requirements.lock.txt",
    "!demo/", "!demo/*.py", "!config/", "!config/routing-corpus.json",
    "!config/routing-calibration.json", "demo/__pycache__/",
)
DATA_FILES = ("config/routing-corpus.json", "config/routing-calibration.json")
PIN = re.compile(
    r"([A-Za-z0-9][A-Za-z0-9._-]*)(?:\[[A-Za-z0-9,._-]+\])?"
    r"==([A-Za-z0-9.!+_-]+)(; sys_platform == \"win32\")?"
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def checked_path(root, relative, *, directory=False):
    """Reject links/reparse points before reading selected public source only."""
    current = root
    for part in Path(relative).parts:
        current = current / part
        info = current.lstat()
        require(not stat.S_ISLNK(info.st_mode) and not (
            getattr(info, "st_file_attributes", 0) & 0x400
        ), "Linked source is not supported")
    require(stat.S_ISDIR(info.st_mode) if directory else stat.S_ISREG(info.st_mode),
            "Expected a regular source file or directory")
    return current


def regular(root, relative):
    return checked_path(root, relative).read_bytes()


def dependency_pins(text, *, constraints):
    lines = [line.strip() for line in text.splitlines()
             if line.strip() and not line.lstrip().startswith("#")]
    require(lines.count(INDEX) == 1, "Use the verified dependency index exactly once")
    if constraints:
        require(lines.count("-c requirements.lock.txt") == 1, "Dependency lock is required")
    pins = {}
    for line in lines:
        if line == INDEX or (constraints and line == "-c requirements.lock.txt"):
            continue
        match = PIN.fullmatch(line)
        require(match is not None, "Only exact dependency pins and the supported marker are allowed")
        name = re.sub(r"[-_.]+", "-", match[1]).lower()
        require(name not in pins, "Duplicate dependency pin")
        pins[name] = (match[2], match[3])
    require(bool(pins), "Empty dependencies are not supported")
    return pins


def validate(root=ROOT):
    root = Path(root).resolve()
    rules = tuple(line.strip() for line in regular(root, ".agentignore").decode("utf-8").splitlines()
                  if line.strip() and not line.lstrip().startswith("#"))
    # This intentionally validates this small policy, not a second gitignore engine.
    require(rules == IGNORE_RULES, "Normal azd source allowlist differs from the checked policy")
    locked = dependency_pins(regular(root, "requirements.lock.txt").decode("utf-8"), constraints=False)
    direct = dependency_pins(regular(root, "requirements.txt").decode("utf-8"), constraints=True)
    for name, pin in direct.items():
        require(locked.get(name) == pin, "Direct dependency does not match the lock")
    modules = checked_path(root, "demo", directory=True)
    selected = ["main.py", "requirements.txt", "requirements.lock.txt", *DATA_FILES]
    selected.extend(sorted("demo/" + path.name for path in modules.glob("*.py")))
    require("demo/__init__.py" in selected and "demo/host.py" in selected,
            "Application entrypoint package is missing")
    hashes = {}
    for relative in selected:
        data = regular(root, relative)
        if relative.endswith(".py"):
            compile(data, relative, "exec", dont_inherit=True)
        elif relative.endswith(".json"):
            json.loads(data)
        hashes[relative] = hashlib.sha256(data).hexdigest()
    return {
        "check": "azd-source", "dependencyMode": "remote_build",
        "scope": "Offline allowlist, direct/lock pins, source compilation and JSON; not a Linux build or deployment",
        "files": hashes, "lockedDependencies": len(locked),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    try:
        report = validate()
    except (OSError, ValueError, SyntaxError, UnicodeError) as error:
        # Never include file contents, environment values or absolute paths in a public log.
        print(json.dumps({"check": "azd-source", "status": "failed", "errorType": type(error).__name__}))
        return 1
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
