"""D1/F1 regressions for ordinary azd source delivery, not live acceptance."""
import os
import base64
import csv
import hashlib
import io
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import yaml

from scripts.check_azd_source import DATA_FILES, IGNORE_RULES, ROOT, bundle_files, regular, validate


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
        self.assertEqual(report["dependencyMode"], "bundled")
        self.assertFalse(report["bundleChecked"])
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

    def test_gitignore_semantics_exclude_private_and_include_checked_bundle(self):
        # The installed extension uses gitignore syntax. This exercises that syntax
        # with Git, not a claim to have run the extension's actual ZIP/upload path.
        subprocess.run(["git", "init", "-q", str(self.root)], check=True, capture_output=True)
        shutil.copyfile(self.root / ".agentignore", self.root / ".gitignore")
        excluded = [
            ".env", ".local/settings.json", ".azure/dev/.env", ".azure-cli/token.json",
            ".git/config", ".foundry/evidence.json",
            "demo/__pycache__/host.pyc", "demo/nested/private.py", "config/private.json",
            "scripts/check_azd_source.py", "tests/test_azd_source.py", "azure.yaml", "package_guard.py",
        ]
        included = ["main.py", "requirements.txt", "requirements.lock.txt",
                    "demo/host.py", "demo/workflow.py", "packages/site.py", *DATA_FILES]
        for name in excluded + included:
            with self.subTest(name=name):
                result = subprocess.run(
                    ["git", "-C", str(self.root), "-c", "core.excludesFile=",
                     "check-ignore", "--no-index", "-q", name], capture_output=True,
                )
                self.assertEqual(result.returncode, 0 if name in excluded else 1)

    def test_three_existing_roles_use_platform_hooks_and_bundled_dependencies(self):
        descriptor = yaml.safe_load((ROOT / "azure.yaml").read_text())
        agents = {key: value for key, value in descriptor["services"].items()
                  if value["host"] == "azure.ai.agent"}
        self.assertEqual(set(agents), {
            "multi-agent-coordinator", "multi-agent-architect", "multi-agent-reviewer",
        })
        for service in agents.values():
            self.assertEqual(service["project"], ".")
            self.assertEqual(service["codeConfiguration"], {
                "runtime": "python_3_13", "entryPoint": "main.py", "dependencyResolution": "bundled",
            })
            self.assertEqual(service["protocols"], [
                {"protocol": "responses", "version": "2.0.0"},
                {"protocol": "invocations", "version": "2.0.0"},
            ])
            self.assertEqual(service["hooks"]["prepackage"], {
                "windows": {"shell": "pwsh", "run": "python scripts/check_azd_source.py --bundled; exit $LASTEXITCODE"},
                "posix": {"shell": "sh", "run": "python3 scripts/check_azd_source.py --bundled"},
            })

    def synthetic_bundle(self, *, tag="py3-none-any", requires="", extra_files=None):
        metadata = "synthetic-1.0.dist-info"
        files = {
            f"{metadata}/METADATA": (
                "Metadata-Version: 2.1\nName: synthetic\nVersion: 1.0\n" + requires
            ).encode(),
            f"{metadata}/WHEEL": f"Wheel-Version: 1.0\nTag: {tag}\n".encode(),
            "synthetic.py": b"value = 1\n",
            **(extra_files or {}),
        }
        record = io.StringIO(newline="")
        writer = csv.writer(record)
        for name, data in files.items():
            digest = base64.urlsafe_b64encode(hashlib.sha256(data).digest()).decode().rstrip("=")
            writer.writerow((name, "sha256=" + digest, len(data)))
        writer.writerow((f"{metadata}/RECORD", "", ""))
        files[f"{metadata}/RECORD"] = record.getvalue().encode()
        for name, data in files.items():
            path = self.root / "packages" / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        (self.root / "requirements.txt").write_text("synthetic==1.0\n")
        return {"synthetic": ("1.0", None)}

    def test_bundle_hashes_exact_linux_pins_and_validates_linux_markers(self):
        pins = self.synthetic_bundle(requires='Requires-Dist: windows-only; sys_platform == "win32"\n')
        self.assertIn("packages/synthetic.py", bundle_files(self.root, pins))
        with self.assertRaisesRegex(ValueError, "every Linux lock pin"):
            bundle_files(self.root, {**pins, "missing": ("1.0", None)})

    def test_bundle_accepts_older_manylinux_and_abi3_wheels(self):
        for tag in ("cp313-cp313-manylinux1_x86_64", "cp36-abi3-manylinux2010_x86_64"):
            with self.subTest(tag=tag):
                pins = self.synthetic_bundle(tag=tag)
                self.assertIn("packages/synthetic.py", bundle_files(self.root, pins))

    def test_bundle_rejects_missing_changed_and_unrecorded_files(self):
        pins = self.synthetic_bundle()
        module = self.root / "packages" / "synthetic.py"
        module.write_text("value = 2\n")
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            bundle_files(self.root, pins)
        module.unlink()
        with self.assertRaisesRegex(ValueError, "missing a recorded"):
            bundle_files(self.root, pins)
        self.synthetic_bundle()
        (self.root / "packages" / "extra.json").write_text("{}")
        with self.assertRaisesRegex(ValueError, "unrecorded"):
            bundle_files(self.root, pins)

    def test_bundle_rejects_foreign_wheel_and_native_binary(self):
        for tag, files, message in (
            ("cp313-cp313-win_amd64", {}, "wheel must support Linux"),
            ("py3-none-any", {"bad.pyd": b"bad"}, "foreign binary"),
            ("py3-none-any", {"bad.so": b"bad"}, "Linux x86_64 ELF"),
        ):
            with self.subTest(tag=tag, files=files):
                if (self.root / "packages").exists():
                    shutil.rmtree(self.root / "packages")
                pins = self.synthetic_bundle(tag=tag, extra_files=files)
                with self.assertRaisesRegex(ValueError, message):
                    bundle_files(self.root, pins)

    def test_bundle_requires_complete_dependency_closure_including_extras(self):
        pins = self.synthetic_bundle(requires='Requires-Dist: missing; extra == "socks"\n')
        bundle_files(self.root, pins)
        (self.root / "requirements.txt").write_text("synthetic[socks]==1.0\n")
        with self.assertRaisesRegex(ValueError, "dependency closure"):
            bundle_files(self.root, pins)

    def test_bundle_rejects_link_before_reading_distribution_metadata(self):
        pins = self.synthetic_bundle()
        with patch("scripts.check_azd_source.checked_path", side_effect=ValueError("Linked source")), patch(
            "importlib.metadata.distributions"
        ) as read:
            with self.assertRaisesRegex(ValueError, "Linked source"):
                bundle_files(self.root, pins)
            read.assert_not_called()

    @unittest.skipUnless(shutil.which("pwsh"), "PowerShell 7 is unavailable")
    def test_windows_hook_propagates_real_python_failure(self):
        descriptor = yaml.safe_load((ROOT / "azure.yaml").read_text())
        hook = descriptor["services"]["multi-agent-coordinator"]["hooks"]["prepackage"]["windows"]["run"]
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

    def test_bundle_builder_rejects_wrong_runtime_without_installing(self):
        from scripts.build_azd_bundle import build
        with patch("scripts.build_azd_bundle.sys.platform", "win32"), patch(
            "scripts.build_azd_bundle.subprocess.run"
        ) as install:
            with self.assertRaisesRegex(RuntimeError, "LINUX_X86_64_PYTHON_3_13"):
                build(self.root)
            install.assert_not_called()

    def test_bundle_builder_reuses_existing_bundle_without_installing(self):
        from scripts.build_azd_bundle import build
        (self.root / "packages").mkdir()
        report = {"lockedDependencies": 2}
        with patch("scripts.build_azd_bundle.sys.platform", "linux"), patch(
            "scripts.build_azd_bundle.sys.version_info", (3, 13)
        ), patch("scripts.build_azd_bundle.platform.machine", return_value="x86_64"), patch(
            "scripts.build_azd_bundle.validate", return_value=report
        ) as check, patch("scripts.build_azd_bundle.subprocess.run") as commands, patch(
            "scripts.build_azd_bundle.sys.path", sys.path.copy()
        ):
            self.assertEqual(build(self.root), report)
            self.assertEqual(check.call_args_list[-1].kwargs, {"bundled": True})
            self.assertEqual(commands.call_count, 1)
            self.assertIn("runpy.run_module('pip'", commands.call_args.args[0][4])


if __name__ == "__main__":
    unittest.main(verbosity=2)
