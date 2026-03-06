# Script pour générer et ouvrir la documentation Sphinx

Write-Host "📚 Génération de la documentation Sphinx..." -ForegroundColor Cyan

# Obtenir le dossier racine du projet (parent de scripts/)
$projectRoot = Split-Path -Parent $PSScriptRoot

# Aller dans le dossier docs
Set-Location -Path "$projectRoot\docs"

# Installer les dépendances si nécessaire
if (-not (Test-Path ".venv")) {
    Write-Host "Installation des dépendances..." -ForegroundColor Yellow
    python -m pip install -r requirements.txt
}

# Générer la documentation
Write-Host "Génération HTML..." -ForegroundColor Yellow
& .\make.bat html

# Ouvrir dans le navigateur
$docPath = "$projectRoot\docs\_build\html\index.html"
if (Test-Path $docPath) {
    Write-Host "✅ Documentation générée avec succès!" -ForegroundColor Green
    Write-Host "🌐 Ouverture dans le navigateur..." -ForegroundColor Cyan
    Start-Process $docPath
} else {
    Write-Host "❌ Erreur lors de la génération" -ForegroundColor Red
}

# Retourner au dossier racine
Set-Location -Path $projectRoot
