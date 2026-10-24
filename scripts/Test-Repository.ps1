#Requires -Version 7.2
[CmdletBinding()]
param([Parameter(Mandatory)][string]$Python)
$ErrorActionPreference = 'Stop'
function Test-ContextFrontmatter {
    param([string]$Text, [switch]$Agent)
    $header = '\A---\r?\nname: [a-z0-9-]+\r?\ndescription: [^\r\n]+\r?\n'
    if ($Agent) {
        $tool = '(?:"[a-z0-9_*/.-]+"|''[a-z0-9_*/.-]+''|[a-z0-9_*/.-]+)'
        $header += "(?:tools: \[[ \t]*(?:$tool(?:[ \t]*,[ \t]*$tool)*)?[ \t]*\]\r?\n)?"
    }
    return $Text -match ($header + '---\r?\n')
}
$root = Split-Path $PSScriptRoot -Parent
& $Python (Join-Path $PSScriptRoot 'repo_index.py') --check
if ($LASTEXITCODE -ne 0) { throw 'Repository index check failed.' }
& $Python (Join-Path $PSScriptRoot 'migration.py') public-check
if ($LASTEXITCODE -ne 0) { throw 'Public/private boundary check failed.' }
$files = & git -C $root ls-files --cached --others --exclude-standard
if ($LASTEXITCODE -ne 0) { throw 'Cannot enumerate public files.' }
foreach ($relative in ($files | Sort-Object -Unique)) {
    $path = Join-Path $root $relative
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { continue }
    if ($relative.EndsWith('.ps1')) {
        $tokens = $null; $errors = $null
        [Management.Automation.Language.Parser]::ParseFile($path, [ref]$tokens, [ref]$errors) | Out-Null
        if ($errors.Count) { throw "PowerShell syntax failed: $relative" }
    }
    if ($relative.EndsWith('.json')) {
        Get-Content -LiteralPath $path -Raw | ConvertFrom-Json -AsHashtable | Out-Null
    }
    if ($relative -like '.github/agents/*.agent.md' -or
        $relative -like '.github/skills/*/SKILL.md') {
        $text = Get-Content -LiteralPath $path -Raw
        if (-not (Test-ContextFrontmatter -Text $text -Agent:($relative -like '.github/agents/*.agent.md'))) {
            throw "Invalid agent/skill frontmatter: $relative"
        }
    }
    if ($relative.EndsWith('.md') -or $relative.EndsWith('.py') -or
        $relative.EndsWith('.ps1') -or $relative.EndsWith('.json') -or
        $relative.EndsWith('.yaml')) {
        $text = [IO.File]::ReadAllText($path)
        if ($text -match '(?m)[ \t]+\r?$') { throw "Trailing whitespace: $relative" }
    }
}
& git -C $root -c core.whitespace=cr-at-eol --no-pager diff --check
if ($LASTEXITCODE -ne 0) { throw 'Git whitespace check failed.' }
Write-Host 'Public boundary, index, JSON, PowerShell, context frontmatter and whitespace checks passed.'
