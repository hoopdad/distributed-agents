import json
from pathlib import Path, PureWindowsPath
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class DeliveryInputTests(unittest.TestCase):
    def setUp(self):
        self.input = json.loads((ROOT / "delivery-input.json").read_text(encoding="utf-8"))

    def test_portable_project_and_specification_binding(self):
        self.assertEqual(self.input["projectRoot"], ".")
        relative = PureWindowsPath(self.input["specification"])
        self.assertFalse(relative.is_absolute())
        self.assertNotIn("..", relative.parts)
        specification = ROOT.joinpath(*relative.parts)
        self.assertTrue(specification.is_file())
        repositories = {item["id"]: item for item in self.input["repositories"]}
        self.assertEqual(repositories["application"]["path"], ".")
        self.assertEqual(repositories["application"]["access"], "write")
        framework = repositories["framework-source"]
        self.assertEqual(framework["access"], "read")
        self.assertFalse(PureWindowsPath(framework["path"]).is_absolute())

    def test_acceptance_uses_canonical_solution_components(self):
        relative = PureWindowsPath(self.input["specification"])
        mission = ROOT.joinpath(*relative.parts).read_text(encoding="utf-8")
        requirements = re.findall(r"^\| (D[1-7]) \| `([^`]+)` \|", mission, re.MULTILINE)
        self.assertEqual(len(requirements), 7)
        self.assertEqual(len({component for _, component in requirements}), 7)
        acceptance = self.input["acceptance"]
        for requirement, component in requirements:
            matches = [item for item in acceptance if item.startswith(f"{component}:")]
            self.assertEqual(len(matches), 1, component)
            self.assertIn(f"mission {requirement};", matches[0])
        for key in ("attempts", "maxSprints", "maxNoProgressRounds", "concurrency", "limits"):
            self.assertNotIn(key, self.input)

    def test_current_state_amendment_replaces_inherited_blockers_not_safety(self):
        amendment = self.input["authority"]["currentStateAmendment"]
        self.assertIn("do not establish current blockers", amendment)
        self.assertIn("actual held/unknown effects", amendment)
        mission = (ROOT / "docs" / "requirements" / "delivery-mission.md").read_text(encoding="utf-8")
        self.assertIn("Historical failures do not establish current blockers.", mission)
        self.assertIn("never clear or replay uncertain effects", mission)
        self.assertNotIn("Keep an unrepaired recorded blocker visible.", mission)
        instructions = (ROOT / ".github" / "copilot-instructions.md").read_text(encoding="utf-8")
        self.assertNotIn("Live acceptance is blocked on trusted-user propagation", instructions)


if __name__ == "__main__":
    unittest.main()
