import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from demo.config import ConfigurationError, project_scope, required

ROOT = Path(__file__).resolve().parents[1]


class ConfigurationTests(unittest.TestCase):
    def test_missing_and_unresolved_model_alias_fail_closed(self):
        for value in ("", "<deployment>", "alias\nother"):
            with self.subTest(value=value), patch.dict(
                os.environ, {"DECISION_MODEL_DEPLOYMENT": value}
            ):
                with self.assertRaises(ConfigurationError):
                    required("DECISION_MODEL_DEPLOYMENT")

    def test_canonical_project_scope(self):
        with patch.dict(os.environ, {
            "FOUNDRY_PROJECT_ENDPOINT": "https://example.services.ai.azure.com/api/projects/demo/"
        }):
            self.assertEqual(project_scope(), (
                "https://example.services.ai.azure.com/api/projects/demo",
                "https://example.services.ai.azure.com",
            ))

    def test_untrusted_project_endpoints_are_rejected(self):
        for value in (
            "http://example.services.ai.azure.com/api/projects/demo",
            "https://example.services.ai.azure.com.evil.test/api/projects/demo",
            "https://user:pass@example.services.ai.azure.com/api/projects/demo",
            "https://example.services.ai.azure.com:bad/api/projects/demo",
            "https://example.services.ai.azure.com:444/api/projects/demo",
            "https://example.services.ai.azure.com/api/projects/demo?x=1",
            "https://example.services.ai.azure.com/api/projects/demo#fragment",
            "https://example.services.ai.azure.com/api/projects/demo/extra",
            "https://example.services.ai.azure.com/api/projects/",
        ):
            with self.subTest(value=value), patch.dict(
                os.environ, {"FOUNDRY_PROJECT_ENDPOINT": value}
            ):
                with self.assertRaises(ConfigurationError):
                    project_scope()

    def test_terminal_does_not_use_ambient_cli_profile(self):
        with patch.dict(os.environ, {
            "FOUNDRY_PROJECT_ENDPOINT": "https://example.services.ai.azure.com/api/projects/example-project"
        }):
            from demo.contracts import DemoError
            from demo.terminal import verify_lab
        with patch.dict(os.environ, {
            "EXPECTED_AZURE_TENANT_ID": "11111111-1111-1111-1111-111111111111",
            "EXPECTED_AZURE_SUBSCRIPTION_ID": "22222222-2222-2222-2222-222222222222",
        }, clear=True), patch("demo.terminal.subprocess.run") as run:
            with self.assertRaises(DemoError) as error:
                verify_lab()
            self.assertEqual(error.exception.code, "CLIENT_CONFIGURATION")
            run.assert_not_called()

    def test_private_session_boundary_covers_new_repository(self):
        with patch.dict(os.environ, {
            "FOUNDRY_PROJECT_ENDPOINT": "https://example.services.ai.azure.com/api/projects/example-project"
        }):
            from demo.contracts import DemoError
            from demo.terminal import private_state_path
        with self.assertRaises(DemoError) as error:
            private_state_path(str(ROOT / ".local" / "session.json"))
        self.assertEqual(error.exception.code, "SESSION_FILE_MUST_BE_PRIVATE")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "session.json"
            self.assertEqual(private_state_path(str(path)), path.resolve())

    @unittest.skipUnless(shutil.which("pwsh"), "PowerShell 7 settings bootstrap")
    def test_settings_are_validated_before_environment_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            settings = {
                "FOUNDRY_PROJECT_ENDPOINT": "https://example.services.ai.azure.com/api/projects/demo",
                "SPECIALIST_MODEL_DEPLOYMENT": "specialist",
                "DECISION_MODEL_DEPLOYMENT": "decision",
                "EXPECTED_AZURE_TENANT_ID": "11111111-1111-1111-1111-111111111111",
                "EXPECTED_AZURE_SUBSCRIPTION_ID": "22222222-2222-2222-2222-222222222222",
                "AZURE_CONFIG_DIR": directory,
            }
            script = str(ROOT / "scripts" / "Use-Settings.ps1").replace("'", "''")
            settings_path = str(path).replace("'", "''")
            command = (
                f"& '{script}' -Path '{settings_path}'; "
                "if ($env:DECISION_MODEL_DEPLOYMENT -ne 'decision') { throw 'Not loaded' }; "
                "if ($env:DEMO_FACT_SHEET) { throw 'Optional value leaked' }"
            )
            path.write_text(json.dumps(settings), encoding="utf-8")
            env = dict(os.environ, DEMO_FACT_SHEET="stale facts")
            result = subprocess.run(
                ["pwsh", "-NoProfile", "-Command", command],
                capture_output=True, text=True, env=env, timeout=30,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            settings["UNSUPPORTED_SECRET"] = "must-not-import"
            path.write_text(json.dumps(settings), encoding="utf-8")
            command = (
                "$env:DECISION_MODEL_DEPLOYMENT = 'unchanged'; "
                f"try {{ & '{script}' -Path '{settings_path}'; throw 'Unexpected success' }} "
                "catch { if ($_.Exception.Message -notlike 'Unsupported settings key:*') { throw } }; "
                "if ($env:DECISION_MODEL_DEPLOYMENT -ne 'unchanged') { throw 'Partial import' }; exit 0"
            )
            result = subprocess.run(
                ["pwsh", "-NoProfile", "-Command", command],
                capture_output=True, text=True, timeout=30,
            )
            self.assertEqual(result.returncode, 0, result.stderr)

    @unittest.skipUnless(shutil.which("pwsh"), "PowerShell 7 settings bootstrap")
    def test_native_settings_are_atomic_and_bound_to_private_storage(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "settings.json"
            settings = {
                "FOUNDRY_PROJECT_ENDPOINT": "https://example.services.ai.azure.com/api/projects/demo",
                "SPECIALIST_MODEL_DEPLOYMENT": "specialist",
                "DECISION_MODEL_DEPLOYMENT": "decision",
                "EXPECTED_AZURE_TENANT_ID": "11111111-1111-1111-1111-111111111111",
                "EXPECTED_AZURE_SUBSCRIPTION_ID": "22222222-2222-2222-2222-222222222222",
                "AZURE_CONFIG_DIR": directory,
                "ARTIFACT_STORAGE_ENDPOINT": "https://examplestorage.blob.core.windows.net",
                "ARTIFACT_CONTROL_CONTAINER": "control", "ARTIFACT_CANDIDATES_CONTAINER": "candidates",
                "ARTIFACT_REVIEWS_CONTAINER": "reviews", "ARTIFACT_PRIVATE_IPS": "10.1.2.3",
                "DECISION_REQUESTS_PER_MINUTE": "17",
            }
            script = str(ROOT / "scripts" / "Use-Settings.ps1").replace("'", "''")
            settings_path = str(path).replace("'", "''")
            path.write_text(json.dumps(settings), encoding="utf-8")
            result = subprocess.run(
                ["pwsh", "-NoProfile", "-Command", (
                    f"& '{script}' -Path '{settings_path}'; "
                    "if ($env:ARTIFACT_PRIVATE_IPS -ne '10.1.2.3') { throw 'Native settings not loaded' }"
                )], capture_output=True, text=True, timeout=30,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            for changes in (
                {"ARTIFACT_PRIVATE_IPS": None},
                {"ARTIFACT_STORAGE_ENDPOINT": "https://example.com"},
                {"ARTIFACT_REVIEWS_CONTAINER": "control"},
                {"ARTIFACT_PRIVATE_IPS": "203.0.113.1"},
                {"ARTIFACT_PRIVATE_IPS": "10.1.2.3,10.1.2.3"},
                {"DECISION_REQUESTS_PER_MINUTE": "0"},
            ):
                invalid = {**settings, **changes}
                invalid = {name: value for name, value in invalid.items() if value is not None}
                path.write_text(json.dumps(invalid), encoding="utf-8")
                result = subprocess.run(
                    ["pwsh", "-NoProfile", "-Command", (
                        "$env:DECISION_MODEL_DEPLOYMENT = 'unchanged'; "
                        "$rejected = $false; "
                        f"try {{ & '{script}' -Path '{settings_path}' }} catch {{ $rejected = $true }}; "
                        "if (-not $rejected) { throw 'Invalid native settings accepted' }; "
                        "if ($env:DECISION_MODEL_DEPLOYMENT -ne 'unchanged') { throw 'Partial import' }"
                    )], capture_output=True, text=True, timeout=30,
                )
                with self.subTest(changes=changes):
                    self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
