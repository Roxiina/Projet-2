# Lance les tests de l'API
Write-Host "Lancement des tests..." -ForegroundColor Yellow
Write-Host ""

# Installation des dependances si necessaire
if (-not (Test-Path "app_api\.venv")) {
    Write-Host "Installation des dependances..." -ForegroundColor Cyan
    Set-Location app_api
    uv sync --extra dev
    Set-Location ..
}

# Lancement des tests depuis la racine
uv run --directory ./app_api pytest ../tests/ -v

Write-Host ""
Write-Host "Tests termines!" -ForegroundColor Green
