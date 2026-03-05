# Scripts PowerShell pour Windows

## Démarrage rapide

### start.ps1
```powershell
# Démarre l'application
docker-compose up -d
Write-Host "✅ Application démarrée!" -ForegroundColor Green
Write-Host "Frontend: http://localhost:8501" -ForegroundColor Cyan
Write-Host "API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
```

### stop.ps1
```powershell
# Arrête l'application
docker-compose down
Write-Host "✅ Application arrêtée!" -ForegroundColor Green
```

### logs.ps1
```powershell
# Affiche les logs
param(
    [string]$Service = ""
)

if ($Service -eq "") {
    docker-compose logs -f
} else {
    docker-compose logs -f $Service
}
```

### test.ps1
```powershell
# Lance les tests
Set-Location app_api
uv run pytest tests/ -v --cov
Set-Location ..
```

## Utilisation

Rendez les scripts exécutables (si nécessaire) et lancez-les :

```powershell
.\start.ps1
.\logs.ps1
.\stop.ps1
```
