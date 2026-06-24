$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$vendorDir = Join-Path $repoRoot "vendor\yt-dlp"
$exePath = Join-Path $vendorDir "yt-dlp.exe"
$checksumPath = Join-Path $vendorDir "SHA2-256SUMS"
$versionPath = Join-Path $vendorDir "yt-dlp.version.txt"
$hashPath = Join-Path $vendorDir "yt-dlp.sha256.txt"
$sourceUrlPath = Join-Path $vendorDir "yt-dlp.source-url.txt"

$downloadUrl = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"
$checksumUrl = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/SHA2-256SUMS"

function Get-Sha256Hex {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    $stream = [System.IO.File]::OpenRead($Path)
    try {
        $sha256 = [System.Security.Cryptography.SHA256]::Create()
        try {
            $hashBytes = $sha256.ComputeHash($stream)
            return ([System.BitConverter]::ToString($hashBytes) -replace "-", "").ToLowerInvariant()
        }
        finally {
            $sha256.Dispose()
        }
    }
    finally {
        $stream.Dispose()
    }
}

New-Item -ItemType Directory -Force -Path $vendorDir | Out-Null

Write-Host "Downloading official yt-dlp stable release..."
Invoke-WebRequest -Uri $downloadUrl -OutFile $exePath

Write-Host "Downloading SHA2-256SUMS..."
$checksumVerified = $false
try {
    Invoke-WebRequest -Uri $checksumUrl -OutFile $checksumPath
    $actualHash = Get-Sha256Hex -Path $exePath
    $expectedLine = Get-Content -Path $checksumPath | Where-Object { $_ -match "(^|[\s\*])yt-dlp\.exe$" } | Select-Object -First 1
    if (-not $expectedLine) {
        throw "SHA2-256SUMS does not contain yt-dlp.exe"
    }
    $expectedHash = (($expectedLine -split "\s+")[0]).ToLowerInvariant()
    if ($actualHash -ne $expectedHash) {
        throw "yt-dlp.exe SHA256 mismatch. Expected $expectedHash, got $actualHash"
    }
    $actualHash | Set-Content -Encoding UTF8 -Path $hashPath
    $checksumVerified = $true
    Write-Host "SHA256 verified: $actualHash"
}
catch {
    Write-Warning "SHA256 verification could not be completed: $($_.Exception.Message)"
    Write-Warning "Stopping because release builds must use verified yt-dlp.exe when SHA2-256SUMS is available."
    exit 1
}

Write-Host "Checking yt-dlp.exe version..."
$version = (& $exePath --version)
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace($version)) {
    throw "vendor\yt-dlp\yt-dlp.exe --version failed"
}

$version.Trim() | Set-Content -Encoding UTF8 -Path $versionPath
$downloadUrl | Set-Content -Encoding UTF8 -Path $sourceUrlPath

Write-Host "yt-dlp version: $($version.Trim())"
Write-Host "yt-dlp source: $downloadUrl"
Write-Host "yt-dlp checksum verified: $checksumVerified"
