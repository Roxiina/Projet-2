# Demarre l'application
docker-compose up -d
Write-Host "Application demarree!" -ForegroundColor Green
Write-Host ""
Write-Host "Accedez aux services:" -ForegroundColor Yellow
Write-Host "  Frontend: http://localhost:8501" -ForegroundColor Cyan
Write-Host "  API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "  API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Pour voir les logs: docker-compose logs -f" -ForegroundColor Gray
Write-Host "Pour arreter: docker-compose down" -ForegroundColor Gray
