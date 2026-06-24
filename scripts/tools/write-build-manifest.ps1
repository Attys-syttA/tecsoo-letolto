$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$artifactsDir = Join-Path $repoRoot "artifacts"
$manifestPath = Join-Path $artifactsDir "build_manifest.json"

function Read-TextValue {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    if (-not (Test-Path $Path)) {
        throw "Missing manifest input: $Path"
    }
    return ((Get-Content -Path $Path -Raw).Trim())
}

function Get-GitCommit {
    try {
        $commit = (& git -C $repoRoot rev-parse HEAD)
        if ($LASTEXITCODE -eq 0) {
            return $commit.Trim()
        }
    }
    catch {
        return $null
    }
    return $null
}

New-Item -ItemType Directory -Force -Path $artifactsDir | Out-Null

$pythonVersion = (& py -3.12 --version)
if ($LASTEXITCODE -ne 0) {
    $pythonVersion = (& python --version)
}
if ($LASTEXITCODE -ne 0) {
    throw "Could not determine Python version for build manifest"
}

$manifest = [ordered]@{
    appName = "TecsoLetolto"
    version = Read-TextValue -Path (Join-Path $repoRoot "src\tecsoo_letolto\version.py")
    buildTime = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    gitCommit = Get-GitCommit
    pythonVersion = $pythonVersion.Trim()
    ytDlpVersion = Read-TextValue -Path (Join-Path $repoRoot "vendor\yt-dlp\yt-dlp.version.txt")
    ytDlpSha256 = Read-TextValue -Path (Join-Path $repoRoot "vendor\yt-dlp\yt-dlp.sha256.txt")
    ytDlpSourceUrl = Read-TextValue -Path (Join-Path $repoRoot "vendor\yt-dlp\yt-dlp.source-url.txt")
    ffmpegAssetName = Read-TextValue -Path (Join-Path $repoRoot "vendor\ffmpeg\ffmpeg.asset-name.txt")
    ffmpegSourceUrl = Read-TextValue -Path (Join-Path $repoRoot "vendor\ffmpeg\ffmpeg.source-url.txt")
    ffmpegVersion = Read-TextValue -Path (Join-Path $repoRoot "vendor\ffmpeg\ffmpeg.version.txt")
    ffmpegSha256 = Read-TextValue -Path (Join-Path $repoRoot "vendor\ffmpeg\ffmpeg.sha256.txt")
    ffprobeVersion = Read-TextValue -Path (Join-Path $repoRoot "vendor\ffmpeg\ffprobe.version.txt")
    ffprobeSha256 = Read-TextValue -Path (Join-Path $repoRoot "vendor\ffmpeg\ffprobe.sha256.txt")
    files = @()
}

$manifest.version = ($manifest.version -replace '(?s).*__version__\s*=\s*"', '' -replace '".*', '')

$manifest | ConvertTo-Json -Depth 5 | Set-Content -Encoding UTF8 -Path $manifestPath
Write-Host "Wrote $manifestPath"
