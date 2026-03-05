# Affiche les logs
param(
    [string]$Service = ""
)

Write-Host "Affichage des logs..." -ForegroundColor Yellow
Write-Host ""

if ($Service -eq "") {
    docker-compose logs -f
} else {
    docker-compose logs -f $Service
}
