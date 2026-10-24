"""D1/F1 regressions for ordinary azd source delivery, not live acceptance."""
import os
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import yaml

from scripts.check_azd_source import DATA_FILES, IGNORE_RULES, ROOT, regular, validate


class AzdSourceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "demo").mkdir()
        (self.root / "config").mkdir()
        for name in (".agentignore", "requirements.txt", "requirements.lock.txt", "main.py",
                     "demo/__init__.py", "demo/host.py", *DATA_FILES):
            shutil.copyfile(ROOT / name, self.root / name)

    def test_current_source_and_pins_pass_without_approval_environment(self):
        with patch.dict(os.environ, {}, clear=True):
            report = validate()
        self.assertEqual(report["dependencyMode"], "remote_build")
        self.assertIn("demo/workflow.py", report["files"])
        self.assertGreater(report["lockedDependencies"], 100)
        self.assertNotIn("package_guard.py", report["files"])
        self.assertIn("not a Linux build or deployment", report["scope"])

    def test_missing_or_changed_lock_rejected(self):
        for text in (
            "--index-url https://packagefeedproxy.microsoft.io/pypi/simple\nopenai==0.0.1\n",
            (self.root / "requirements.txt").read_text().replace("-c requirements.lock.txt", ""),
            (self.root / "requirements.txt").read_text().replace("openai==3.24.0", "openai>=3.24.0"),
            (self.root / "requirements.txt").read_text().replace("packagefeedproxy.microsoft.io", "example.invalid"),
        ):
            (self.root / "requirements.txt").write_text(text)
            with self.assertRaises(ValueError):
                validate(self.root)

    def test_expanded_allowlist_rejected_without_reading_private_files(self):
        for extra in ("!packages/\n!packages/**\n", "!.local/settings.json\n", "!demo/**\n"):
            (self.root / ".agentignore").write_text("\n".join(IGNORE_RULES) + "\n" + extra)
            with self.assertRaisesRegex(ValueError, "allowlist"):
                validate(self.root)

    def test_invalid_source_and_json_rejected(self):
        (self.root / "demo/host.py").write_text("def broken(:\n")
        with self.assertRaises(SyntaxError):
            validate(self.root)
        shutil.copyfile(ROOT / "demo/host.py", self.root / "demo/host.py")
        (self.root / DATA_FILES[0]).write_text("{invalid}")
        with self.assertRaises(ValueError):
            validate(self.root)

    def test_missing_entrypoint_rejected(self):
        (self.root / "main.py").unlink()
        with self.assertRaises(OSError):
            validate(self.root)

    def test_linked_source_rejected(self):
        target = self.root / "other.py"
        target.write_text("# synthetic\n")
        linked = self.root / "demo/linked.py"
        try:
            linked.symlink_to(target)
        except OSError:
            self.skipTest("Symlinks unavailable to this Windows identity")
        with self.assertRaisesRegex(ValueError, "Linked source"):
            validate(self.root)

    def test_link_and_windows_reparse_rejected_before_read(self):
        for info in (
            SimpleNamespace(st_mode=stat.S_IFLNK, st_file_attributes=0),
            SimpleNamespace(st_mode=stat.S_IFREG, st_file_attributes=0x400),
        ):
            with self.subTest(info=info), patch.object(Path, "lstat", return_value=info), patch.object(
                Path, "read_bytes"
            ) as read:
                with self.assertRaisesRegex(ValueError, "Linked source"):
                    regular(self.root, "main.py")
                read.assert_not_called()

    def test_gitignore_semantics_exclude_private_and_bundled_dependencies(self):
        # The installed extension uses gitignore syntax. This exercises that syntax
        # with Git, not a claim to have run the extension's actual ZIP/upload path.
        subprocess.run(["git", "init", "-q", str(self.root)], check=True, capture_output=True)
        shutil.copyfile(self.root / ".agentignore", self.root / ".gitignore")
        excluded = [
            ".env", ".local/settings.json", ".azure/dev/.env", ".azure-cli/token.json",
            ".git/config", ".foundry/evidence.json", "packages/site.py", "packages/native.pyd",
            "demo/__pycache__/host.pyc", "demo/nested/private.py", "config/private.json",
            "scripts/check_azd_source.py", "tests/test_azd_source.py", "azure.yaml", "package_guard.py",
        ]
        included = ["main.py", "requirements.txt", "requirements.lock.txt",
                    "demo/host.py", "demo/workflow.py", *DATA_FILES]
        for name in excluded + included:
            with self.subTest(name=name):
                result = subprocess.run(
                    ["git", "-C", str(self.root), "-c", "core.excludesFile=",
                     "check-ignore", "--no-index", "-q", name], capture_output=True,
                )
                self.assertEqual(result.returncode, 0 if name in excluded else 1)

    def test_three_existing_roles_use_platform_hooks_and_remote_build(self):
        descriptor = yaml.safe_load((ROOT / "azure.yaml").read_text())
        agents = {key: value for key, value in descriptor["services"].items()
                  if value["host"] == "azure.ai.agent"}
        self.assertEqual(set(agents), {
            "multi-agent-coordinator", "multi-agent-architect", "multi-agent-reviewer",
        })
        for service in agents.values():
            self.assertEqual(service["project"], ".")
            self.assertEqual(service["codeConfiguration"], {
                "runtime": "python_3_13", "entryPoint": "main.py", "dependencyResolution": "remote_build",
            })
            self.assertEqual(service["protocols"], [{"protocol": "responses", "version": "2.0.0"}])
            self.assertEqual(service["hooks"]["predeploy"], {
                "windows": {"shell": "pwsh", "run": "python scripts/check_azd_source.py; exit $LASTEXITCODE"},
                "posix": {"shell": "sh", "run": "python3 scripts/check_azd_source.py"},
            })

    @unittest.skipUnless(shutil.which("pwsh"), "PowerShell 7 is unavailable")
    def test_windows_hook_propagates_real_python_failure(self):
        descriptor = yaml.safe_load((ROOT / "azure.yaml").read_text())
        hook = descriptor["services"]["multi-agent-coordinator"]["hooks"]["predeploy"]["windows"]["run"]
        # Run the real shell text with a controlled Python command, not azd/cloud.
        for status in (0, 7):
            with self.subTest(status=status):
                code = "function python { & pwsh -NoProfile -Command 'exit " + str(status) + "' }; " + hook
                result = subprocess.run(["pwsh", "-NoProfile", "-Command", code], capture_output=True)
                self.assertEqual(result.returncode, status)

    def test_descriptor_change_does_not_modify_legacy_package_guard(self):
        # Preserve the retained exact-package implementation byte-for-byte.
        import hashlib
        self.assertEqual(hashlib.sha256((ROOT / "package_guard.py").read_bytes()).hexdigest(),
                         "31b4f055f647cd0d8903f5b48e7a9c4a01251d271d80c3b17b0df60999f321cc")


if __name__ == "__main__":
    unittest.main(verbosity=2)
