$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$python = Join-Path $repoRoot ".venv-build\Scripts\python.exe"
$distDir = Join-Path $repoRoot "dist\TecsoLetolto"
$releaseRoot = Join-Path $repoRoot "release"
$releaseDir = Join-Path $releaseRoot "TecsoLetolto"
$buildDir = Join-Path $repoRoot "build"

function Remove-RepoChild {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    if (-not (Test-Path -LiteralPath $Path)) {
        return
    }
    $resolved = Resolve-Path -LiteralPath $Path
    if (-not $resolved.Path.StartsWith($repoRoot.Path, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing to remove path outside repo: $($resolved.Path)"
    }
    Remove-Item -LiteralPath $resolved.Path -Recurse -Force
}

Set-Location $repoRoot

& (Join-Path $repoRoot "scripts\build_dev.bat")
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

& $python -m pip install -e ".[build]"
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

& (Join-Path $repoRoot "scripts\fetch_ytdlp_vendor.bat")
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

& (Join-Path $repoRoot "scripts\fetch_ffmpeg_vendor.bat")
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Remove-RepoChild -Path $distDir
Remove-RepoChild -Path $releaseDir
New-Item -ItemType Directory -Force -Path $releaseRoot | Out-Null

$iconPath = Join-Path $repoRoot "assets\tecsoo-letolto.ico"
$entryPath = Join-Path $repoRoot "scripts\tools\pyinstaller-entry.py"

& $python -m PyInstaller `
    --noconfirm `
    --clean `
    --onedir `
    --windowed `
    --name TecsoLetolto `
    --paths (Join-Path $repoRoot "src") `
    --icon $iconPath `
    --distpath (Join-Path $repoRoot "dist") `
    --workpath $buildDir `
    $entryPath
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

if (-not (Test-Path -LiteralPath (Join-Path $distDir "TecsoLetolto.exe"))) {
    throw "PyInstaller output missing TecsoLetolto.exe"
}

New-Item -ItemType Directory -Force -Path $releaseDir | Out-Null
Get-ChildItem -LiteralPath $distDir -Force | ForEach-Object {
    Copy-Item -LiteralPath $_.FullName -Destination $releaseDir -Recurse -Force
}

New-Item -ItemType Directory -Force -Path (Join-Path $releaseDir "vendor\yt-dlp") | Out-Null
Copy-Item -LiteralPath (Join-Path $repoRoot "vendor\yt-dlp\yt-dlp.exe") -Destination (Join-Path $releaseDir "vendor\yt-dlp\yt-dlp.exe") -Force

New-Item -ItemType Directory -Force -Path (Join-Path $releaseDir "vendor\ffmpeg\bin") | Out-Null
Copy-Item -LiteralPath (Join-Path $repoRoot "vendor\ffmpeg\bin\ffmpeg.exe") -Destination (Join-Path $releaseDir "vendor\ffmpeg\bin\ffmpeg.exe") -Force
Copy-Item -LiteralPath (Join-Path $repoRoot "vendor\ffmpeg\bin\ffprobe.exe") -Destination (Join-Path $releaseDir "vendor\ffmpeg\bin\ffprobe.exe") -Force

Set-Content -Encoding UTF8 -Path (Join-Path $releaseDir "VERSION.txt") -Value ((Get-Content -Path (Join-Path $repoRoot "src\tecsoo_letolto\version.py") -Raw) -replace '(?s).*__version__\s*=\s*"', '' -replace '".*', '')
Set-Content -Encoding UTF8 -Path (Join-Path $releaseDir "README_PORTABLE.txt") -Value "TecsoLetolto portable build. Inditas: TecsoLetolto.exe"

New-Item -ItemType Directory -Force -Path (Join-Path $releaseDir "licenses") | Out-Null
Copy-Item -LiteralPath (Join-Path $repoRoot "docs\THIRD_PARTY_LICENSES.md") -Destination (Join-Path $releaseDir "licenses\THIRD_PARTY_LICENSES.md") -Force

& (Join-Path $repoRoot "scripts\write_build_manifest.bat")
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

& (Join-Path $repoRoot "scripts\verify_release.bat")
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

$version = (Get-Content -Path (Join-Path $releaseDir "VERSION.txt") -Raw).Trim()
$zipPath = Join-Path $repoRoot "artifacts\TecsoLetolto-$version.zip"
if (Test-Path -LiteralPath $zipPath) {
    Remove-Item -LiteralPath $zipPath -Force
}
Compress-Archive -Path $releaseDir -DestinationPath $zipPath -CompressionLevel Optimal

Write-Host "Release build ready: $releaseDir"
Write-Host "Release ZIP ready: $zipPath"
