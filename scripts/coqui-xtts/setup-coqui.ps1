# Coqui XTTS v2 Setup Script
# Run this on your Windows machine (PowerShell as Admin)

# Create project folder on D drive
$ProjectDir = "D:\coqui-xtts"
if (!(Test-Path $ProjectDir)) {
    New-Item -ItemType Directory -Path $ProjectDir -Force
}

# Create models subfolder
$ModelsDir = "$ProjectDir\models"
if (!(Test-Path $ModelsDir)) {
    New-Item -ItemType Directory -Path $ModelsDir -Force
}

# Copy docker-compose.yml to project folder
$ComposeSrc = "$PSScriptRoot\docker-compose.yml"
if (Test-Path $ComposeSrc) {
    Copy-Item $ComposeSrc "$ProjectDir\docker-compose.yml" -Force
    Write-Host "[+] Copied docker-compose.yml to D:\coqui-xtts"
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Coqui XTTS v2 Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To start the container:" -ForegroundColor Yellow
Write-Host "  cd D:\coqui-xtts"
Write-Host "  docker-compose up -d"
Write-Host ""
Write-Host "To check logs:" -ForegroundColor Yellow
Write-Host "  docker logs coqui-xtts"
Write-Host ""
Write-Host "To stop:" -ForegroundColor Yellow
Write-Host "  docker-compose down"
Write-Host ""
Write-Host "The API will be available at: http://localhost:5002" -ForegroundColor Cyan
Write-Host ""
Write-Host "To clone your voice (3+ sec audio):" -ForegroundColor Yellow
Write-Host '  curl -X POST http://localhost:5002/clone -F "audio_file=@voice.wav" -F "reference_text=text in audio"'
Write-Host ""
