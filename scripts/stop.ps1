# Arrete l'application
param(
    [switch]$RemoveVolumes
)

if ($RemoveVolumes) {
    docker-compose down -v
    Write-Host "Application arretee et volumes supprimes!" -ForegroundColor Green
} else {
    docker-compose down
    Write-Host "Application arretee!" -ForegroundColor Green
}
