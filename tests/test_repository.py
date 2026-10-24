import json
from pathlib import Path
import shutil
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]
HEADER = "---\nname: example-agent\ndescription: A bounded test agent.\n"


@unittest.skipUnless(shutil.which("pwsh"), "PowerShell 7 repository validation")
class ContextFrontmatterTests(unittest.TestCase):
    def check_cases(self, cases):
        procedure = str(ROOT / "scripts" / "Test-Repository.ps1").replace("'", "''")
        harness = f"$procedure = '{procedure}'\n" + r"""
$ErrorActionPreference = 'Stop'
$tokens = $null; $errors = $null
$ast = [Management.Automation.Language.Parser]::ParseFile($procedure, [ref]$tokens, [ref]$errors)
if ($errors.Count) { throw 'Repository checker syntax failed.' }
$functions = @($ast.FindAll({ param($node)
    $node -is [Management.Automation.Language.FunctionDefinitionAst] -and
    $node.Name -eq 'Test-ContextFrontmatter'
}, $true))
if ($functions.Count -ne 1) { throw 'Frontmatter validator not unique.' }
. ([scriptblock]::Create($functions[0].Extent.Text))
foreach ($case in ([Console]::In.ReadToEnd() | ConvertFrom-Json)) {
    $actual = Test-ContextFrontmatter -Text $case.text -Agent:([bool]$case.agent)
    if ($actual -ne $case.expected) { throw "Frontmatter case failed: $($case.name)" }
}
"""
        result = subprocess.run(
            ["pwsh", "-NoProfile", "-NonInteractive", "-Command", harness],
            input=json.dumps(cases), capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_existing_headers_and_agent_tool_flow_lists(self):
        cases = []
        for newline in ("\n", "\r\n"):
            for tools in (
                "",
                'tools: ["read", "search", "execute"]\n',
                "tools: ['read', 'github/*']\n",
                "tools: [read, search, execute]\n",
                'tools: ["*"]\n',
                "tools: []\n",
            ):
                cases.append({
                    "name": repr((newline, tools)), "agent": True, "expected": True,
                    "text": (HEADER + tools + "---\n\nBody.\n").replace("\n", newline),
                })
            cases.append({
                "name": "unchanged skill", "agent": False, "expected": True,
                "text": (HEADER + "---\n").replace("\n", newline),
            })
        self.check_cases(cases)

    def test_installed_profiles_remain_valid_without_edits(self):
        self.check_cases([
            {
                "name": path.name, "agent": True, "expected": True,
                "text": path.read_text(encoding="utf-8"),
            }
            for path in sorted((ROOT / ".github" / "agents").glob("*.agent.md"))
        ])

    def test_invalid_headers_and_tool_lists_are_rejected(self):
        invalid = [
            HEADER.replace("---\n", "", 1) + "---\n",
            HEADER.replace("name: example-agent\n", "") + "---\n",
            HEADER.replace("example-agent", "invalid name") + "---\n",
            HEADER.replace("description: A bounded test agent.\n", "") + "---\n",
            HEADER.replace("A bounded test agent.", "") + "---\n",
            HEADER + "Body without a closing delimiter.\n",
            HEADER + "unexpected: true\n---\n",
            HEADER + 'tools: ["read", "execute"\n---\n',
            HEADER + 'tools: ["read",]\n---\n',
            HEADER + 'tools: ["read",, "execute"]\n---\n',
            HEADER + 'tools: ["read\']\n---\n',
            HEADER + "tools: read\n---\n",
            HEADER + 'tools: [{"name": "execute"}]\n---\n',
            HEADER + 'tools: ["read"] # unchecked content\n---\n',
            HEADER + 'tools: ["read"]\ntools: ["execute"]\n---\n',
            HEADER + 'tools: ["read"]\nunexpected: true\n---\n',
        ]
        self.check_cases([
            {"name": str(index), "text": text, "agent": True, "expected": False}
            for index, text in enumerate(invalid)
        ] + [{
            "name": "skills do not gain tools", "agent": False, "expected": False,
            "text": HEADER + 'tools: ["execute"]\n---\n',
        }])

    def test_json_validation_accepts_npm_package_keys_but_not_malformed_json(self):
        procedure = str(ROOT / "scripts" / "Test-Repository.ps1").replace("'", "''")
        lockfile = str(ROOT / "gh-dynamic-workflows" / "package-lock.json").replace("'", "''")
        harness = (
            f"$procedure = '{procedure}'\n$lockfile = '{lockfile}'\n" + r"""
$ErrorActionPreference = 'Stop'
$tokens = $null; $errors = $null
$ast = [Management.Automation.Language.Parser]::ParseFile($procedure, [ref]$tokens, [ref]$errors)
if ($errors.Count) { throw 'Repository checker syntax failed.' }
$commands = @($ast.FindAll({ param($node)
    $node -is [Management.Automation.Language.CommandAst] -and
    $node.GetCommandName() -eq 'ConvertFrom-Json'
}, $true))
if ($commands.Count -ne 1) { throw 'JSON validator not unique.' }
$validate = [scriptblock]::Create('param($text) $text | ' + $commands[0].Extent.Text)
foreach ($text in @('{"packages":{"":{"name":"example"}}}', (Get-Content -LiteralPath $lockfile -Raw))) {
    & $validate $text | Out-Null
}
$rejected = $false
try { & $validate '{"packages":' | Out-Null } catch { $rejected = $true }
if (-not $rejected) { throw 'Malformed JSON accepted.' }
"""
        )
        result = subprocess.run(
            ["pwsh", "-NoProfile", "-NonInteractive", "-Command", harness],
            capture_output=True, text=True, timeout=30,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
