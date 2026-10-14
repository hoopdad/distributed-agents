#Requires -Version 7.2
[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$Python,
    [string]$LabRepositoryRoot
)
$ErrorActionPreference = 'Stop'
$oldTelemetry = $env:OTEL_SDK_DISABLED
$oldLabSource = $env:AZURE_LAB_SOURCE_ROOT
$pushed = $false
try {
    $env:OTEL_SDK_DISABLED = 'true'
    if ($LabRepositoryRoot) {
        $source = Join-Path $LabRepositoryRoot 'foundry-tf\multi-agent'
        if (-not (Test-Path -LiteralPath (Join-Path $source 'Test-PrivateConnectivity.ps1') -PathType Leaf)) {
            throw 'Explicit lab source is missing the retained connectivity regression target.'
        }
        $env:AZURE_LAB_SOURCE_ROOT = (Resolve-Path -LiteralPath $source).Path
    } else {
        Remove-Item Env:AZURE_LAB_SOURCE_ROOT -ErrorAction SilentlyContinue
    }
    Push-Location $PSScriptRoot
    $pushed = $true
    & $Python -m pip check
    if ($LASTEXITCODE -ne 0) { throw 'Pinned runtime dependency check failed.' }
    & $Python -m unittest discover -s tests -v
    if ($LASTEXITCODE -ne 0) { throw 'Multi-agent offline acceptance failed.' }
    & $Python -m compileall -q demo tests scripts main.py native_proxy.py agent_metadata.py package_guard.py live_acceptance.py
    if ($LASTEXITCODE -ne 0) { throw 'Python compilation failed.' }
} finally {
    if ($pushed) { Pop-Location }
    $env:OTEL_SDK_DISABLED = $oldTelemetry
    $env:AZURE_LAB_SOURCE_ROOT = $oldLabSource
}
