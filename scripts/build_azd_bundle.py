"""Build the unchanged Linux lock into packages/ for normal azd bundled delivery."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.check_azd_source import ROOT, dependency_pins, regular, validate


def build(root=ROOT):
    root = Path(root).resolve()
    if sys.platform != "linux" or sys.version_info[:2] != (3, 13) or platform.machine() != "x86_64":
        raise RuntimeError("BUNDLE_BUILD_REQUIRES_LINUX_X86_64_PYTHON_3_13")
    validate(root)
    target = root / "packages"
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONNOUSERSITE="1")
    if not target.exists():
        (root / ".local").mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="azd-bundle-", dir=root / ".local") as temporary:
            staged = Path(temporary) / "packages"
            # Install exact pins without optional feed metadata sidecars; check closure below.
            subprocess.run([
                sys.executable, "-I", "-m", "pip", "--isolated", "install",
                "--disable-pip-version-check", "--no-input", "--no-deps", "--no-compile",
                "--only-binary=:all:", "--platform", "manylinux2014_x86_64",
                "--python-version", "3.13", "--implementation", "cp",
                "--use-deprecated=legacy-resolver", "--target", str(staged),
                "-r", str(root / "requirements.lock.txt"),
            ], check=True, cwd=root, env=environment)
            # Console scripts are not part of the module-based hosted entrypoint.
            import shutil
            if (staged / "bin").exists():
                shutil.rmtree(staged / "bin")
            staged.rename(target)
    sys.path.insert(0, str(target))
    report = validate(root, bundled=True)
    subprocess.run([
        sys.executable, "-I", "-B", "-c",
        "import sys,runpy; sys.path.insert(0,sys.argv.pop(1)); "
        "sys.argv=['pip','check']; runpy.run_module('pip',run_name='__main__')",
        str(target),
    ], check=True, cwd=root, env=environment)
    pins = dependency_pins(regular(root, "requirements.lock.txt").decode(), constraints=False)
    count = sum(marker is None for _, marker in pins.values())
    print(f"Validated {count} unchanged Linux dependency pins.")
    return report


def main():
    argparse.ArgumentParser(description=__doc__).parse_args()
    build()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
