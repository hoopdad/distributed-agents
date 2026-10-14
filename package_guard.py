from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import stat


def verify_native_package(directory, expected):
    if not re.fullmatch(r"[a-fA-F0-9]{64}", expected):
        raise RuntimeError("APPROVED_PACKAGE_HASH_REQUIRED")
    root = Path(directory)
    info = root.lstat()
    if not stat.S_ISDIR(info.st_mode) or info.st_uid != os.getuid() or info.st_mode & 0o077:
        raise RuntimeError("PRIVATE_PACKAGE_DIRECTORY_REQUIRED")
    artifacts = list(root.glob("azd-code-deploy-*.zip"))
    if len(artifacts) != 1:
        raise RuntimeError("EXACT_NATIVE_PACKAGE_REQUIRED")
    artifact = artifacts[0]
    info = artifact.lstat()
    if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid():
        raise RuntimeError("NATIVE_PACKAGE_OWNER_REQUIRED")
    actual = hashlib.sha256(artifact.read_bytes()).hexdigest()
    if actual != expected.lower():
        raise RuntimeError("APPROVED_PACKAGE_MISMATCH")
    return {"package": str(artifact), "sha256": actual, "checked_before_upload": True}


def main():
    receipt = verify_native_package(os.environ["TMPDIR"], os.environ["DEMO_APPROVED_PACKAGE_SHA256"])
    Path(os.environ["DEMO_PACKAGE_RECEIPT"]).write_text(json.dumps(receipt, indent=2))
    print(json.dumps(receipt))


if __name__ == "__main__":
    main()
