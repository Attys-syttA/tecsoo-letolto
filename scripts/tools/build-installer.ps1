$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$python = Join-Path $repoRoot ".venv-build\Scripts\python.exe"
$releaseDir = Join-Path $repoRoot "release\TecsoLetolto"
$buildRoot = Join-Path $repoRoot "build\installer"
$payloadZip = Join-Path $buildRoot "payload.zip"
$distDir = Join-Path $repoRoot "artifacts"
$workDir = Join-Path $buildRoot "pyinstaller"
$specDir = $buildRoot
$iconPath = Join-Path $repoRoot "assets\tecsoo-letolto.ico"
$entryPath = Join-Path $repoRoot "scripts\tools\installer-bootstrap.py"
$outputExe = Join-Path $distDir "TecsoLetolto-Installer.exe"
$versionFile = Join-Path $releaseDir "VERSION.txt"

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

& (Join-Path $repoRoot "scripts\build_release.bat")
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

if (-not (Test-Path -LiteralPath $releaseDir)) {
    throw "Release folder missing: $releaseDir"
}

New-Item -ItemType Directory -Force -Path $buildRoot | Out-Null
New-Item -ItemType Directory -Force -Path $distDir | Out-Null
Remove-RepoChild -Path $workDir
if (Test-Path -LiteralPath $outputExe) {
    Remove-Item -LiteralPath $outputExe -Force
}

& $python (Join-Path $repoRoot "scripts\tools\package-release.py") `
    --source $releaseDir `
    --output $payloadZip `
    --root "TecsoLetolto"
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

& $python -m PyInstaller `
    --noconfirm `
    --clean `
    --onefile `
    --windowed `
    --name "TecsoLetolto-Installer" `
    --icon $iconPath `
    --distpath $distDir `
    --workpath $workDir `
    --specpath $specDir `
    --add-data "$payloadZip;." `
    $entryPath
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

if (-not (Test-Path -LiteralPath $outputExe)) {
    throw "Installer output missing: $outputExe"
}

if (-not (Test-Path -LiteralPath $versionFile)) {
    throw "Release version file missing: $versionFile"
}

$version = (Get-Content -LiteralPath $versionFile -Raw).Trim()
$versionedOutputExe = Join-Path $distDir "TecsoLetolto-Installer-$version.exe"
Copy-Item -LiteralPath $outputExe -Destination $versionedOutputExe -Force

Write-Host "Installer build ready: $outputExe"
Write-Host "Versioned installer copy ready: $versionedOutputExe"
