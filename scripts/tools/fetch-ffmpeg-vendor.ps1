$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$vendorRoot = Join-Path $repoRoot "vendor\ffmpeg"
$binDir = Join-Path $vendorRoot "bin"
$assetName = "ffmpeg-master-latest-win64-lgpl.zip"
$apiUrl = "https://api.github.com/repos/BtbN/FFmpeg-Builds/releases/latest"
$decisionPath = "docs\codex-tasks\pending\not-started\vendor-and-local-media-decision-2026-06-24.md"

$zipPath = Join-Path $vendorRoot $assetName
$extractDir = Join-Path $vendorRoot "_extract"
$ffmpegPath = Join-Path $binDir "ffmpeg.exe"
$ffprobePath = Join-Path $binDir "ffprobe.exe"
$sourceUrlPath = Join-Path $vendorRoot "ffmpeg.source-url.txt"
$assetNamePath = Join-Path $vendorRoot "ffmpeg.asset-name.txt"
$ffmpegVersionPath = Join-Path $vendorRoot "ffmpeg.version.txt"
$ffprobeVersionPath = Join-Path $vendorRoot "ffprobe.version.txt"
$ffmpegHashPath = Join-Path $vendorRoot "ffmpeg.sha256.txt"
$ffprobeHashPath = Join-Path $vendorRoot "ffprobe.sha256.txt"

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

function Find-ExtractedFile {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Root,
        [Parameter(Mandatory = $true)]
        [string]$FileName
    )

    $matches = Get-ChildItem -Path $Root -Recurse -File -Filter $FileName
    if (($matches | Measure-Object).Count -ne 1) {
        throw "Expected exactly one $FileName in $assetName, found $(($matches | Measure-Object).Count)"
    }
    return $matches[0].FullName
}

New-Item -ItemType Directory -Force -Path $vendorRoot | Out-Null
New-Item -ItemType Directory -Force -Path $binDir | Out-Null

Write-Host "Resolving BtbN FFmpeg latest release asset..."
$release = Invoke-RestMethod -Uri $apiUrl -Headers @{ "User-Agent" = "TecsoLetolto-build" }
$asset = $release.assets | Where-Object { $_.name -eq $assetName } | Select-Object -First 1
if (-not $asset) {
    Write-Error "Required asset '$assetName' was not found in BtbN/FFmpeg-Builds latest release. Do not choose GPL/full/nonfree automatically. Document this in $decisionPath and ask for a decision."
    exit 1
}

Write-Host "Downloading $assetName..."
Invoke-WebRequest -Uri $asset.browser_download_url -OutFile $zipPath

if (Test-Path $extractDir) {
    Remove-Item -LiteralPath $extractDir -Recurse -Force
}
New-Item -ItemType Directory -Force -Path $extractDir | Out-Null

Write-Host "Extracting selected FFmpeg asset..."
Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::ExtractToDirectory($zipPath, $extractDir)

$extractedFfmpeg = Find-ExtractedFile -Root $extractDir -FileName "ffmpeg.exe"
$extractedFfprobe = Find-ExtractedFile -Root $extractDir -FileName "ffprobe.exe"

Copy-Item -LiteralPath $extractedFfmpeg -Destination $ffmpegPath -Force
Copy-Item -LiteralPath $extractedFfprobe -Destination $ffprobePath -Force

Write-Host "Checking ffmpeg.exe version..."
$ffmpegOutput = & $ffmpegPath -version 2>&1
$ffmpegExitCode = $LASTEXITCODE
$ffmpegVersion = $ffmpegOutput | Select-Object -First 1
if ($ffmpegExitCode -ne 0 -or [string]::IsNullOrWhiteSpace($ffmpegVersion)) {
    throw "vendor\ffmpeg\bin\ffmpeg.exe -version failed"
}

Write-Host "Checking ffprobe.exe version..."
$ffprobeOutput = & $ffprobePath -version 2>&1
$ffprobeExitCode = $LASTEXITCODE
$ffprobeVersion = $ffprobeOutput | Select-Object -First 1
if ($ffprobeExitCode -ne 0 -or [string]::IsNullOrWhiteSpace($ffprobeVersion)) {
    throw "vendor\ffmpeg\bin\ffprobe.exe -version failed"
}

$ffmpegHash = Get-Sha256Hex -Path $ffmpegPath
$ffprobeHash = Get-Sha256Hex -Path $ffprobePath

$asset.browser_download_url | Set-Content -Encoding UTF8 -Path $sourceUrlPath
$assetName | Set-Content -Encoding UTF8 -Path $assetNamePath
$ffmpegVersion.Trim() | Set-Content -Encoding UTF8 -Path $ffmpegVersionPath
$ffprobeVersion.Trim() | Set-Content -Encoding UTF8 -Path $ffprobeVersionPath
$ffmpegHash | Set-Content -Encoding UTF8 -Path $ffmpegHashPath
$ffprobeHash | Set-Content -Encoding UTF8 -Path $ffprobeHashPath

Remove-Item -LiteralPath $extractDir -Recurse -Force

Write-Host "FFmpeg asset: $assetName"
Write-Host "FFmpeg source: $($asset.browser_download_url)"
Write-Host "ffmpeg version: $($ffmpegVersion.Trim())"
Write-Host "ffprobe version: $($ffprobeVersion.Trim())"
Write-Host "ffmpeg SHA256: $ffmpegHash"
Write-Host "ffprobe SHA256: $ffprobeHash"
