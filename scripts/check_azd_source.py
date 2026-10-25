"""Source and optional Linux dependency checks for normal azd; never approves a ZIP."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat


ROOT = Path(__file__).resolve().parents[1]
INDEX = "--index-url https://packagefeedproxy.microsoft.io/pypi/simple"
IGNORE_RULES = (
    "*", "!main.py", "!requirements.txt", "!requirements.lock.txt",
    "!demo/", "!demo/*.py", "!config/", "!config/routing-corpus.json",
    "!config/routing-calibration.json", "demo/__pycache__/",
    "!packages/", "!packages/**",
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


def bundle_files(root, locked):
    import csv
    import base64
    from importlib.metadata import distributions
    from pathlib import PurePosixPath

    from packaging.markers import default_environment
    from packaging.requirements import Requirement
    from packaging.tags import compatible_tags, cpython_tags, parse_tag
    from packaging.utils import canonicalize_name
    from packaging.version import Version

    directory = checked_path(root, "packages", directory=True)
    paths = []
    for parent, directories, files in os.walk(directory, followlinks=False):
        for name in directories + files:
            relative = (Path(parent) / name).relative_to(root)
            checked_path(root, relative, directory=name in directories)
        paths.extend((Path(parent) / name).relative_to(root).as_posix() for name in files)
    expected = {name: version for name, (version, marker) in locked.items() if not marker}
    installed = {}
    recorded = {}
    record_files = set()
    platforms = ["manylinux2014_x86_64", "manylinux2010_x86_64", "manylinux1_x86_64"]
    platforms.extend(f"manylinux_2_{minor}_x86_64" for minor in range(5, 18))
    supported = set(cpython_tags((3, 13), platforms=platforms))
    supported.update(compatible_tags((3, 13), interpreter="cp313", platforms=platforms))
    for distribution in distributions(path=[str(directory)]):
        name = canonicalize_name(distribution.metadata["Name"])
        require(name not in installed and expected.get(name) == distribution.version,
                "Bundle contains an unexpected or mismatched distribution")
        installed[name] = distribution
        wheel = distribution.read_text("WHEEL") or ""
        tags = set()
        for line in wheel.splitlines():
            if line.startswith("Tag: "):
                tags.update(parse_tag(line[5:]))
        require(bool(tags & supported), "Bundle wheel must support Linux x86_64 CPython 3.13")
        python = distribution.metadata.get("Requires-Python")
        if python:
            from packaging.specifiers import SpecifierSet
            require(Version("3.13") in SpecifierSet(python), "Bundle Python version mismatch")
        record = distribution.read_text("RECORD")
        require(record is not None, "Bundle distribution RECORD is required")
        for relative, digest, size in csv.reader(record.splitlines()):
            path = PurePosixPath(relative)
            require(not path.is_absolute() and "\\" not in relative, "Invalid bundle RECORD path")
            if ".." in path.parts:
                require(relative.startswith(("../bin/", "../../bin/")),
                        "Invalid bundle RECORD traversal")
                continue
            if digest:
                algorithm, encoded = digest.split("=", 1)
                require(algorithm == "sha256", "Bundle RECORD requires SHA-256")
                value = base64.urlsafe_b64decode(encoded + "=" * (-len(encoded) % 4)).hex()
                require(relative not in recorded or recorded[relative] == value,
                        "Conflicting bundle RECORD entries")
                recorded[relative] = value
            else:
                require(relative.endswith(".dist-info/RECORD") and not size,
                        "Only RECORD itself may omit its hash")
                record_files.add(relative)
    require(set(installed) == set(expected), "Bundle must contain every Linux lock pin")
    environment = default_environment()
    environment.update({
        "sys_platform": "linux", "os_name": "posix", "platform_system": "Linux",
        "platform_machine": "x86_64", "python_version": "3.13",
        "python_full_version": "3.13.0", "implementation_name": "cpython",
        "platform_python_implementation": "CPython",
    })
    extras = {name: set() for name in installed}
    for line in regular(root, "requirements.txt").decode().splitlines():
        if PIN.fullmatch(line.strip()):
            requirement = Requirement(line)
            extras[canonicalize_name(requirement.name)].update(requirement.extras)
    pending = set(installed)
    while pending:
        name = pending.pop()
        for text in installed[name].requires or []:
            requirement = Requirement(text)
            if requirement.marker and not any(
                requirement.marker.evaluate({**environment, "extra": extra})
                for extra in {""} | extras[name]
            ):
                continue
            dependency = canonicalize_name(requirement.name)
            require(not requirement.url and dependency in installed and
                    Version(installed[dependency].version) in requirement.specifier,
                    "Bundle dependency closure does not satisfy Linux requirements")
            additional = set(requirement.extras) - extras[dependency]
            if additional:
                extras[dependency].update(additional)
                pending.add(dependency)
    hashes = {}
    for relative in paths:
        require(not relative.lower().endswith((".pyd", ".dll", ".exe", ".whl", ".pyc")),
                "Bundle contains a foreign binary or build artifact")
        data = regular(root, relative)
        digest = hashlib.sha256(data).hexdigest()
        package_relative = relative.removeprefix("packages/")
        require(package_relative in recorded or package_relative in record_files,
                "Bundle contains an unrecorded file")
        if package_relative in recorded:
            require(recorded[package_relative] == digest, "Bundle RECORD hash mismatch")
        if relative.endswith(".so") or ".so." in relative:
            require(data[:6] == b"\x7fELF\x02\x01" and data[18:20] == b"\x3e\x00",
                    "Bundle native library must be Linux x86_64 ELF")
        hashes[relative] = digest
    require(set(recorded) <= {name.removeprefix("packages/") for name in hashes},
            "Bundle is missing a recorded file")
    require(bool(hashes), "Bundle is empty")
    return hashes


def validate(root=ROOT, *, bundled=False):
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
    if bundled:
        hashes.update(bundle_files(root, locked))
    return {
        "check": "azd-source", "dependencyMode": "bundled", "bundleChecked": bundled,
        "scope": (
            "Offline source, Linux wheel/closure and RECORD integrity; not hosted execution or acceptance"
            if bundled else
            "Offline allowlist, direct/lock pins, source compilation and JSON; not a Linux build or deployment"
        ),
        "files": hashes, "lockedDependencies": len(locked),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundled", action="store_true")
    args = parser.parse_args()
    try:
        report = validate(bundled=args.bundled)
        if args.bundled:
            report["bundledFiles"] = sum(name.startswith("packages/") for name in report["files"])
            report["files"] = {name: digest for name, digest in report["files"].items()
                               if not name.startswith("packages/")}
    except (OSError, ValueError, SyntaxError, UnicodeError) as error:
        # Never include file contents, environment values or absolute paths in a public log.
        print(json.dumps({"check": "azd-source", "status": "failed", "errorType": type(error).__name__}))
        return 1
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
