import json
import subprocess
import sys
import unittest
from unittest.mock import patch

from scripts import repo_index


class RepositoryIndexTests(unittest.TestCase):
    def test_default_search_excludes_history_but_keeps_current_source(self):
        current = repo_index.INDEX.read_text(encoding="utf-8")
        patterns = repo_index.search_exclusions(current)
        for name in (
            ".github/repo-history-index.md",
            "docs/customer-prototype-profiling-continuation-3-sprint-plan.json",
            "docs/identity-recovery-plan.md",
            "docs/migration-plan.md",
        ):
            self.assertTrue(repo_index.is_historical(name, patterns), name)
        for name in (
            "docs/requirements/delivery-mission.md",
            "docs/design.md",
            "docs/implementation-workflow.md",
            "demo/workflow.py",
            "tests/test_scenario_evidence.py",
            "scripts/diagnose_identity.py",
        ):
            self.assertFalse(repo_index.is_historical(name, patterns), name)

    def test_indexes_partition_every_public_path_without_dropping_history(self):
        names = [
            "demo/workflow.py",
            "docs/requirements/delivery-mission.md",
            "docs/customer-prototype-release-plan.md",
            ".github/repo-history-index.md",
        ]
        with patch.object(repo_index, "public_files", return_value=names):
            rendered = repo_index.render()
        for name in names:
            entry = f"- `{name.replace('/', chr(92))}`"
            occurrences = sum(
                entry in text.split(repo_index.START)[1].split(repo_index.END)[0]
                for text in rendered.values()
            )
            self.assertEqual(occurrences, 1, name)
        self.assertIn("Preserved source joins", rendered[repo_index.HISTORY])
        self.assertNotIn("Preserved source joins", rendered[repo_index.INDEX])

    def test_search_exclusions_are_explicit_repository_relative_patterns(self):
        for patterns in (None, "docs/*", [""], [None], ["../outside"], ["C:\\private"], ["\\private"]):
            text = (
                repo_index.SCOPE_START + json.dumps({"ignore": patterns}) +
                repo_index.SCOPE_END
            )
            with self.subTest(patterns=patterns), self.assertRaises(RuntimeError):
                repo_index.search_exclusions(text)

    def test_refresh_is_idempotent_and_does_not_change_archived_narratives(self):
        for path, expected in repo_index.render().items():
            current = path.read_text(encoding="utf-8")
            self.assertEqual(current, expected, path.name)
            self.assertEqual(
                current.split(repo_index.START)[0],
                expected.split(repo_index.START)[0],
            )

    def test_search_files_command_emits_only_current_paths(self):
        result = subprocess.run(
            [sys.executable, str(repo_index.ROOT / "scripts" / "repo_index.py"), "--search-files"],
            capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        names = result.stdout.splitlines()
        self.assertIn("demo\\workflow.py", names)
        self.assertIn("docs\\requirements\\delivery-mission.md", names)
        patterns = repo_index.search_exclusions(repo_index.INDEX.read_text(encoding="utf-8"))
        self.assertTrue(names)
        self.assertFalse(any(repo_index.is_historical(name, patterns) for name in names))


if __name__ == "__main__":
    unittest.main()
