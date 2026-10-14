#Requires -Version 7.2
[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$LabRepositoryRoot,
    [Parameter(Mandatory)][string]$Region,
    [Parameter(Mandatory)][string]$ProjectEndpoint,
    [Parameter(Mandatory)][string]$SpecialistModelDeployment,
    [Parameter(Mandatory)][string]$DecisionModelDeployment
)
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$lab = (Resolve-Path -LiteralPath $LabRepositoryRoot).Path
$registry = Get-Content -LiteralPath (Join-Path $lab 'ip-registry.json') -Raw |
    ConvertFrom-Json -AsHashtable
if (-not $registry.regions.ContainsKey($Region)) { throw 'Region is not registered.' }
$subscription = $registry.subscriptions[$registry.regions[$Region].subscription_key]
if (-not $subscription) { throw 'Registered subscription is missing.' }
$settings = [ordered]@{
    LAB_REPOSITORY_ROOT = $lab
    LAB_REGION = $Region
    FOUNDRY_PROJECT_ENDPOINT = $ProjectEndpoint
    SPECIALIST_MODEL_DEPLOYMENT = $SpecialistModelDeployment
    DECISION_MODEL_DEPLOYMENT = $DecisionModelDeployment
    EXPECTED_AZURE_TENANT_ID = $subscription.tenant_id
    EXPECTED_AZURE_SUBSCRIPTION_ID = $subscription.subscription_id
    AZURE_CONFIG_DIR = Join-Path $lab '.azure-cli'
}
$directory = Join-Path $root '.local'
New-Item -ItemType Directory -Path $directory -Force | Out-Null
$path = Join-Path $directory 'lab-settings.json'
& git -C $root check-ignore --quiet -- $path
if ($LASTEXITCODE -ne 0) { throw 'Private settings destination is not Git-ignored.' }
$temporary = Join-Path $directory 'lab-settings.pending.json'
if (Test-Path -LiteralPath $temporary) { throw 'Pending settings file already exists; inspect it privately.' }
try {
    $settings | ConvertTo-Json | Set-Content -LiteralPath $temporary -Encoding utf8NoBOM
    # Child scope validates without changing the caller's environment.
    & pwsh -NoProfile -File (Join-Path $PSScriptRoot 'Use-Settings.ps1') -Path $temporary
    if ($LASTEXITCODE -ne 0) { throw 'Private settings validation failed.' }
    Move-Item -LiteralPath $temporary -Destination $path -Force
} finally {
    if (Test-Path -LiteralPath $temporary) { Remove-Item -LiteralPath $temporary }
}
Write-Host 'Private lab settings saved. No token cache was copied and no Azure changes were performed.'
