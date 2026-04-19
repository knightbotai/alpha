# Alpha Pipecat Setup Script for Windows
# Run as: .\setup.ps1 in PowerShell

#Requires -RunAsAdministrator

param(
    [string]$InstallPath = "D:\alpha-pipecat",
    [switch]$SkipDependencies,
    [switch]$StartServices
)

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Alpha Pipecat Bot Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "[1/6] Checking Python..." -ForegroundColor Yellow
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Host "ERROR: Python not found. Please install Python 3.10+ first." -ForegroundColor Red
    exit 1
}

$pythonVersion = python --version
Write-Host "  Found: $pythonVersion" -ForegroundColor Green

# Check pip
Write-Host "[2/6] Checking pip..." -ForegroundColor Yellow
pip --version | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: pip not found" -ForegroundColor Red
    exit 1
}
Write-Host "  pip OK" -ForegroundColor Green

# Create installation directory
Write-Host "[3/6] Creating installation directory..." -ForegroundColor Yellow
if (-not (Test-Path $InstallPath)) {
    New-Item -ItemType Directory -Path $InstallPath -Force | Out-Null
    Write-Host "  Created: $InstallPath" -ForegroundColor Green
} else {
    Write-Host "  Using: $InstallPath" -ForegroundColor Green
}

# Copy files
Write-Host "[4/6] Copying bot files..." -ForegroundColor Yellow
$scriptDir = $PSScriptRoot
if (-not $scriptDir) {
    $scriptDir = Get-Location
}

# Files to copy
$files = @(
    "bot.py",
    "state.py",
    "requirements.txt"
)

$servicesDir = Join-Path $scriptDir "services"
if (Test-Path $servicesDir) {
    $destServicesDir = Join-Path $InstallPath "services"
    if (Test-Path $destServicesDir) {
        Remove-Item $destServicesDir -Recurse -Force
    }
    Copy-Item $servicesDir -Destination $destServicesDir -Recurse
    Write-Host "  Copied services/" -ForegroundColor Green
}

foreach ($file in $files) {
    $src = Join-Path $scriptDir $file
    if (Test-Path $src) {
        Copy-Item $src -Destination $InstallPath -Force
        Write-Host "  Copied: $file" -ForegroundColor Green
    }
}

# Install dependencies
if (-not $SkipDependencies) {
    Write-Host "[5/6] Installing Python dependencies..." -ForegroundColor Yellow
    Set-Location $InstallPath

    # Upgrade pip first
    python -m pip install --upgrade pip --quiet

    # Install requirements
    pip install -r requirements.txt --quiet
    if ($LASTEXITCODE -ne 0) {
        Write-Host "WARNING: Some dependencies may have failed to install" -ForegroundColor Yellow
    } else {
        Write-Host "  Dependencies installed" -ForegroundColor Green
    }
}

# Environment setup
Write-Host "[6/6] Setting up environment..." -ForegroundColor Yellow

# Create .env file template
$envContent = @"
# Alpha Pipecat Bot Environment Configuration
# Copy this to .env and fill in your values

# Daily.co room for WebRTC (required)
DAILY_URL=https://your-domain.daily.co/your-room
DAILY_TOKEN=your-room-token

# Optional: Override default ports
# VLLM_PORT=8000
# WHISPER_PORT=8001
# KOKORO_PORT=8880
"@

$envFile = Join-Path $InstallPath ".env.example"
$envContent | Out-File $envFile -Encoding UTF8

if (-not (Test-Path ".env")) {
    Copy-Item $envFile ".env"
    Write-Host "  Created .env file - please edit with your settings" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Setup Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Installation path: $InstallPath" -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Edit $InstallPath\.env with your Daily.co settings" -ForegroundColor White
Write-Host "2. Start your local services:" -ForegroundColor White
Write-Host "   - vLLM on port 8000" -ForegroundColor Cyan
Write-Host "   - Whisper server on port 8001" -ForegroundColor Cyan
Write-Host "   - Kokoro TTS server on port 8880" -ForegroundColor Cyan
Write-Host "3. Run the bot:" -ForegroundColor White
Write-Host "   python bot.py" -ForegroundColor Cyan
Write-Host ""

# Optional: Start services
if ($StartServices) {
    Write-Host "Starting local services..." -ForegroundColor Yellow
    # This is a placeholder - you'd need actual service startup commands
    Write-Host "NOTE: Service startup not implemented - start services manually" -ForegroundColor Yellow
}