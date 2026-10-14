from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "docs" / "migration-map.json"
SNAPSHOT = ROOT / ".migration" / "baseline"
IGNORED_SOURCE_DIRECTORIES = {".azure", "__pycache__", ".pytest_cache"}
PRIVATE_DIRECTORIES = {".azure", ".azure-cli", ".local", ".migration", ".foundry", ".venv"}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(root: Path, name: str) -> Path:
    path = root.joinpath(*name.replace("\\", "/").split("/"))
    if not path.resolve().is_relative_to(root.resolve()) or path.is_symlink():
        raise RuntimeError(f"PATH_OUTSIDE_ROOT: {name}")
    return path


def files(root: Path, *, omit_generated: bool = False) -> dict[str, Path]:
    result = {}
    for path in sorted(root.rglob("*")):
        if path.is_symlink() or path.is_junction():
            raise RuntimeError("LINKED_SOURCE_NOT_SUPPORTED")
        parts = path.relative_to(root).parts
        if omit_generated and any(part in IGNORED_SOURCE_DIRECTORIES for part in parts):
            continue
        if path.is_file():
            result[str(path.relative_to(root))] = path
    return result


def copy_identical(source: Path, target: Path) -> None:
    if target.exists():
        if not target.is_file() or digest(source) != digest(target):
            raise RuntimeError(f"REFUSING_TO_OVERWRITE: {target.relative_to(ROOT)}")
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    if digest(source) != digest(target):
        raise RuntimeError("COPY_VERIFICATION_FAILED")


def write_json(path: Path, body: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(body, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def public_paths() -> list[Path]:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        check=True, capture_output=True,
    )
    return [ROOT / name.decode("utf-8") for name in result.stdout.split(b"\0") if name]


def check_public_boundary() -> int:
    paths = public_paths()
    forbidden = [
        b"-----BEGIN " + kind + b"PRIVATE KEY-----"
        for kind in (b"", b"OPENSSH ", b"RSA ", b"EC ", b"DSA ", b"ENCRYPTED ")
    ]
    settings_path = ROOT / ".local" / "lab-settings.json"
    if settings_path.is_file():
        settings = json.loads(settings_path.read_text(encoding="utf-8"))
        for key in ("EXPECTED_AZURE_TENANT_ID", "EXPECTED_AZURE_SUBSCRIPTION_ID",
                    "LAB_REPOSITORY_ROOT"):
            forbidden.append(settings[key].encode("utf-8"))
        endpoint = urlsplit(settings["FOUNDRY_PROJECT_ENDPOINT"])
        forbidden.extend([endpoint.hostname.encode("utf-8"),
                          endpoint.path.rsplit("/", 1)[-1].encode("utf-8")])
    for path in paths:
        name = path.relative_to(ROOT)
        if any(part in PRIVATE_DIRECTORIES for part in name.parts):
            raise RuntimeError(f"PRIVATE_FILE_VISIBLE_TO_GIT: {name}")
        if path.suffix.lower() in {".pem", ".key", ".pfx", ".p12", ".zip"}:
            raise RuntimeError(f"PRIVATE_FILE_VISIBLE_TO_GIT: {name}")
        if ((path.name == ".env" or path.name.startswith(".env."))
                and path.name != ".env.example") or path.name in {
                    "ipsec.secrets", "id_rsa", "id_ed25519"
                }:
            raise RuntimeError(f"PRIVATE_FILE_VISIBLE_TO_GIT: {name}")
        if path.is_file():
            content = path.read_bytes()
            if any(value.lower() in content.lower() for value in forbidden):
                raise RuntimeError(f"LAB_IDENTIFIER_IN_PUBLIC_FILE: {name}")
    return len(paths)


def stage(source: Path, mapping: dict, copy_azure: bool) -> None:
    source = source.resolve(strict=True)
    if source.is_relative_to(ROOT) or ROOT.is_relative_to(source):
        raise RuntimeError("DISTINCT_SOURCE_AND_TARGET_REQUIRED")
    names = mapping["portable"] + mapping["retained_in_lab"]
    actual = files(source, omit_generated=True)
    if len(names) != len(set(names)) or set(actual) != set(names):
        raise RuntimeError(f"UNCLASSIFIED_SOURCE: {sorted(set(actual) ^ set(names))}")
    for name in names:
        copy_identical(actual[name], relative(SNAPSHOT, name))
        if name in mapping["portable"]:
            copy_identical(actual[name], relative(ROOT, name))
    mapping["source_sha256"] = {name: digest(actual[name]) for name in sorted(names)}
    write_json(MAP, mapping)
    if copy_azure:
        state = files(source / ".azure")
        for name, path in state.items():
            copy_identical(path, relative(ROOT / ".azure", name))
        write_json(ROOT / ".migration" / "azure-state.json",
                   {"sha256": {name: digest(path) for name, path in sorted(state.items())}})
    print(json.dumps({"classified_source_files": len(names),
                      "portable_files_staged": len(mapping["portable"]),
                      "private_azure_copied": copy_azure, "source_deleted": False}))


def seal(mapping: dict) -> None:
    check_public_boundary()
    for name, expected in mapping["source_sha256"].items():
        if digest(relative(SNAPSHOT, name)) != expected:
            raise RuntimeError(f"BASELINE_CHANGED: {name}")
        if name in mapping["portable"] and name not in mapping["adaptations"]:
            if digest(relative(ROOT, name)) != expected:
                raise RuntimeError(f"UNDECLARED_ADAPTATION: {name}")
    mapping["target_sha256"] = {
        name: digest(relative(ROOT, name)) for name in sorted(mapping["portable"])
    }
    write_json(MAP, mapping)
    print(json.dumps({"portable_snapshot_sealed": len(mapping["target_sha256"])}))


def verify(source: Path, mapping: dict) -> None:
    source = source.resolve(strict=True)
    actual = files(source, omit_generated=True)
    if set(actual) != set(mapping["source_sha256"]):
        raise RuntimeError("SOURCE_CENSUS_CHANGED")
    for name, expected in mapping["source_sha256"].items():
        if digest(actual[name]) != expected or digest(relative(SNAPSHOT, name)) != expected:
            raise RuntimeError(f"ORIGINAL_OR_BASELINE_CHANGED: {name}")
    for name, expected in mapping["target_sha256"].items():
        if digest(relative(ROOT, name)) != expected:
            raise RuntimeError(f"PORTABLE_SNAPSHOT_CHANGED: {name}")
    test_name = "tests\\test_demo.py"
    def test_cases(path: Path) -> set[tuple[str, str]]:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        return {
            (node.name, method.name)
            for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
            for method in node.body if isinstance(method, (ast.FunctionDef, ast.AsyncFunctionDef))
            and method.name.startswith("test_")
        }
    baseline_cases = test_cases(relative(SNAPSHOT, test_name))
    if not baseline_cases.issubset(test_cases(relative(ROOT, test_name))):
        raise RuntimeError("BASELINE_TEST_CASE_LOST")
    private = ROOT / ".migration" / "azure-state.json"
    state = json.loads(private.read_text(encoding="utf-8"))
    original, copied = files(source / ".azure"), files(ROOT / ".azure")
    if set(original) != set(state["sha256"]) or set(copied) != set(original):
        raise RuntimeError("PRIVATE_AZD_CENSUS_CHANGED")
    for name, expected in state["sha256"].items():
        if digest(original[name]) != expected or digest(copied[name]) != expected:
            raise RuntimeError("PRIVATE_AZD_COPY_CHANGED")
    count = check_public_boundary()
    result = {
        "original_files_preserved": len(actual),
        "portable_files_verified": len(mapping["target_sha256"]),
        "baseline_core_test_cases_preserved": len(baseline_cases),
        "private_azure_files_verified": len(copied),
        "public_files_checked": count,
        "source_deleted": False,
        "azure_cli_cache_copied": False,
        "deployed": False,
    }
    write_json(ROOT / ".migration" / "validation.json", result)
    print(json.dumps(result, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser(description="Copy-first migration checks; no Azure operations.")
    parser.add_argument("mode", choices=("stage", "seal", "verify", "public-check"))
    parser.add_argument("--source-root", type=Path)
    parser.add_argument("--copy-azure-state", action="store_true")
    args = parser.parse_args()
    mapping = json.loads(MAP.read_text(encoding="utf-8"))
    if args.mode in {"stage", "verify"} and args.source_root is None:
        parser.error("--source-root is required")
    if args.mode == "stage":
        stage(args.source_root, mapping, args.copy_azure_state)
    elif args.mode == "seal":
        seal(mapping)
    elif args.mode == "verify":
        verify(args.source_root, mapping)
    else:
        print(json.dumps({"public_files_checked": check_public_boundary()}))


if __name__ == "__main__":
    main()
