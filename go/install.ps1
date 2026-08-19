$ErrorActionPreference = "Stop"

$repo = "SCE-Development/SCE-CLI"
$installDir = "$env:LOCALAPPDATA\sce"
$target = Join-Path $installDir "sce.exe"
$staged = Join-Path $installDir "sce.exe.new"
$helper = Join-Path $env:TEMP "sce-update-$PID.ps1"

# Detect architecture
$arch = if ([Environment]::Is64BitOperatingSystem) { "amd64" } else { "amd64" }
if ($env:PROCESSOR_ARCHITECTURE -eq "ARM64") { $arch = "arm64" }

$binary = "sce-windows-$arch.exe"
$url = "https://github.com/$repo/releases/latest/download/$binary"

Write-Host "downloading sce for windows/$arch..."
New-Item -ItemType Directory -Path $installDir -Force | Out-Null
Remove-Item -Path $staged -Force -ErrorAction SilentlyContinue
Invoke-WebRequest -Uri $url -OutFile $staged -UseBasicParsing

$replaceScript = @"
param(
    [string]
    `$Target,
    [string]
    `$Source
)

while (`$true) {
    try {
        if (-not (Test-Path -Path `$Target)) {
            break
        }

        `$stream = [System.IO.File]::Open(`$Target, 'Open', 'ReadWrite', 'None')
        `$stream.Close()
        break
    } catch {
        Start-Sleep -Milliseconds 250
    }
}

Move-Item -Force -Path `$Source -Destination `$Target
"@

Set-Content -Path $helper -Value $replaceScript -Encoding UTF8
Start-Process powershell -WindowStyle Hidden -ArgumentList @(
    "-NoProfile",
    "-ExecutionPolicy",
    "Bypass",
    "-File",
    $helper,
    "-Target",
    $target,
    "-Source",
    $staged
) | Out-Null

Write-Host "update downloaded; applying it after this command exits..."

# Add to PATH if not already there
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -notlike "*$installDir*") {
    [Environment]::SetEnvironmentVariable("Path", "$userPath;$installDir", "User")
    Write-Host "added $installDir to your PATH."
}

Write-Host "sce installed successfully! restart your terminal and run 'sce --help' to get started."
