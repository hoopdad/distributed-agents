#Requires -Version 7.2
[CmdletBinding()]
param([Parameter(Mandatory)][string]$Path)
$ErrorActionPreference = 'Stop'
$settings = Get-Content -LiteralPath $Path -Raw | ConvertFrom-Json -AsHashtable
$required = @(
    'FOUNDRY_PROJECT_ENDPOINT', 'SPECIALIST_MODEL_DEPLOYMENT', 'DECISION_MODEL_DEPLOYMENT',
    'EXPECTED_AZURE_TENANT_ID', 'EXPECTED_AZURE_SUBSCRIPTION_ID', 'AZURE_CONFIG_DIR'
)
$native = @(
    'ARTIFACT_STORAGE_ENDPOINT', 'ARTIFACT_CONTROL_CONTAINER', 'ARTIFACT_CANDIDATES_CONTAINER',
    'ARTIFACT_REVIEWS_CONTAINER', 'ARTIFACT_PRIVATE_IPS', 'DECISION_REQUESTS_PER_MINUTE'
)
$allowed = $required + $native + @('LAB_REPOSITORY_ROOT', 'LAB_REGION', 'DEMO_FACT_SHEET')
foreach ($name in $settings.Keys) {
    if ($name -notin $allowed) { throw "Unsupported settings key: $name" }
    $value = $settings[$name]
    if ($value -isnot [string] -or [string]::IsNullOrWhiteSpace($value) -or
        $value.Contains('<') -or $value.Contains('>') -or $value -match '[\r\n]') {
        throw "Invalid or unresolved setting: $name"
    }
}
foreach ($name in $required) {
    if (-not $settings.ContainsKey($name)) { throw "Missing setting: $name" }
}
$endpoint = $null
if (-not [Uri]::TryCreate($settings.FOUNDRY_PROJECT_ENDPOINT, [UriKind]::Absolute, [ref]$endpoint) -or
    $endpoint.Scheme -cne 'https' -or $endpoint.Port -ne 443 -or $endpoint.UserInfo -or
    $endpoint.Query -or $endpoint.Fragment -or
    $endpoint.Host -notmatch '\.(services\.ai|ai)\.azure\.com$' -or
    $endpoint.AbsolutePath -notmatch '^/api/projects/[A-Za-z0-9_-]+/?$') {
    throw 'Invalid Foundry project endpoint.'
}
foreach ($name in @('EXPECTED_AZURE_TENANT_ID', 'EXPECTED_AZURE_SUBSCRIPTION_ID')) {
    $parsed = [Guid]::Empty
    if (-not [Guid]::TryParse($settings[$name], [ref]$parsed) -or $parsed -eq [Guid]::Empty) {
        throw "Invalid UUID setting: $name"
    }
}
if (-not [IO.Path]::IsPathFullyQualified($settings.AZURE_CONFIG_DIR) -or
    -not (Test-Path -LiteralPath $settings.AZURE_CONFIG_DIR -PathType Container)) {
    throw 'AZURE_CONFIG_DIR must name an existing dedicated absolute directory.'
}
$nativeKeys = @($native | Where-Object { $settings.ContainsKey($_) })
if ($nativeKeys.Count -gt 0) {
    if ($nativeKeys.Count -ne $native.Count) { throw 'Native artifact/routing settings must be supplied together.' }
    if ($settings.ARTIFACT_STORAGE_ENDPOINT -cnotmatch '^https://[a-z0-9]{3,24}\.blob\.core\.windows\.net/?$') {
        throw 'Invalid artifact storage endpoint.'
    }
    $containers = @($settings.ARTIFACT_CONTROL_CONTAINER, $settings.ARTIFACT_CANDIDATES_CONTAINER,
        $settings.ARTIFACT_REVIEWS_CONTAINER)
    if (@($containers | Select-Object -Unique).Count -ne 3) { throw 'Artifact containers must be distinct.' }
    foreach ($container in $containers) {
        if ($container -cnotmatch '^[a-z0-9][a-z0-9-]{1,61}[a-z0-9]$' -or $container.Contains('--')) {
            throw 'Invalid artifact container.'
        }
    }
    $addresses = $settings.ARTIFACT_PRIVATE_IPS.Split(',')
    if (@($addresses | Select-Object -Unique).Count -ne $addresses.Count) { throw 'Duplicate artifact private IP.' }
    foreach ($address in $addresses) {
        $parsed = $null
        if (-not [Net.IPAddress]::TryParse($address, [ref]$parsed) -or
            $parsed.AddressFamily -ne [Net.Sockets.AddressFamily]::InterNetwork -or
            $parsed.ToString() -cne $address) { throw 'Invalid artifact private IPv4 address.' }
        $bytes = $parsed.GetAddressBytes()
        if (-not ($bytes[0] -eq 10 -or ($bytes[0] -eq 172 -and $bytes[1] -ge 16 -and $bytes[1] -le 31) -or
            ($bytes[0] -eq 192 -and $bytes[1] -eq 168))) { throw 'Artifact IP must be RFC1918 private IPv4.' }
    }
    if ($settings.DECISION_REQUESTS_PER_MINUTE -notmatch '^[1-9][0-9]{0,3}$' -or
        [int]$settings.DECISION_REQUESTS_PER_MINUTE -gt 1000) { throw 'Invalid verified Decision request limit.' }
}
# Validate the complete document before changing any process configuration.
foreach ($name in $allowed) {
    if ($settings.ContainsKey($name)) {
        [Environment]::SetEnvironmentVariable($name, $settings[$name], 'Process')
    } else {
        Remove-Item -LiteralPath "Env:$name" -ErrorAction SilentlyContinue
    }
}
$env:AZURE_EXTENSION_USE_DYNAMIC_INSTALL = 'no'
Write-Host 'Loaded validated settings into this process; no authentication or Azure changes performed.'
