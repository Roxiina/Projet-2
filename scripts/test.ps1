# Lance les tests de l'API
Write-Host "Lancement des tests..." -ForegroundColor Yellow
Write-Host ""

Set-Location app_api

# Installation des dependances si necessaire
if (-not (Test-Path ".venv")) {
    Write-Host "Installation des dependances..." -ForegroundColor Cyan
    uv sync
}

# Lancement des tests
uv run pytest tests/ -v --cov

Set-Location ..

Write-Host ""
Write-Host "Tests termines!" -ForegroundColor Green
