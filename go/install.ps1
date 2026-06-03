$ErrorActionPreference = "Stop"

$repo = "SCE-Development/SCE-CLI"
$installDir = "$env:LOCALAPPDATA\sce"

# Detect architecture
$arch = if ([Environment]::Is64BitOperatingSystem) { "amd64" } else { "amd64" }
if ($env:PROCESSOR_ARCHITECTURE -eq "ARM64") { $arch = "arm64" }

$binary = "sce-windows-$arch.exe"
$url = "https://github.com/$repo/releases/latest/download/$binary"

Write-Host "downloading sce for windows/$arch..."
New-Item -ItemType Directory -Path $installDir -Force | Out-Null
Invoke-WebRequest -Uri $url -OutFile "$installDir\sce.exe" -UseBasicParsing

# Add to PATH if not already there
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -notlike "*$installDir*") {
    [Environment]::SetEnvironmentVariable("Path", "$userPath;$installDir", "User")
    Write-Host "added $installDir to your PATH."
}

Write-Host "sce installed successfully! restart your terminal and run 'sce --help' to get started."
