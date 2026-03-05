# Script de déploiement final - Projet 2
# Exécutez ce script pour pousser le projet vers GitHub

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  DEPLOIEMENT FINAL - PROJET 2" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Étape 1 : Vérifier l'état de Git
Write-Host "[1/5] Verification de l'état Git..." -ForegroundColor Yellow
git status --short

Write-Host ""
Write-Host "ATTENTION : Avant de continuer, assurez-vous d'avoir configure :" -ForegroundColor Red
Write-Host "  1. GitHub Secrets : DOCKERHUB_USERNAME et DOCKERHUB_TOKEN" -ForegroundColor Red
Write-Host "  2. Fichier .env avec DOCKERHUB_USERNAME" -ForegroundColor Red
Write-Host ""

$continue = Read-Host "Voulez-vous continuer ? (O/N)"
if ($continue -ne "O" -and $continue -ne "o") {
    Write-Host "Deploiement annule." -ForegroundColor Yellow
    exit 0
}

# Étape 2 : Ajouter tous les fichiers
Write-Host ""
Write-Host "[2/5] Ajout des fichiers au commit..." -ForegroundColor Yellow
git add .

# Étape 3 : Créer le commit
Write-Host ""
Write-Host "[3/5] Creation du commit..." -ForegroundColor Yellow
git commit -m "feat: projet 2 complet - tous les livrables prets

- Architecture micro-services complete (API FastAPI + Frontend Streamlit + PostgreSQL)
- Orchestration Docker avec reseaux isoles (front-api, api-db)
- Persistance des donnees avec volumes PostgreSQL
- CI/CD complet avec GitHub Actions
- Security scan avec Gitleaks
- Images DockerHub avec versioning (latest + SHA)
- Documentation complete (README, QUICKSTART, TESTING, etc.)
- docker-compose.prod.yml pour deploiement production

Livrables conformes aux specifications du projet 2."

# Étape 4 : Pousser vers GitHub
Write-Host ""
Write-Host "[4/5] Push vers GitHub..." -ForegroundColor Yellow
git push origin main

# Étape 5 : Résumé
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  DEPLOIEMENT TERMINE !" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Prochaines etapes :" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Verifier les workflows GitHub Actions :" -ForegroundColor White
Write-Host "   https://github.com/Roxiina/Projet-2/actions" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Attendre que la CI passe au vert" -ForegroundColor White
Write-Host ""
Write-Host "3. Le CD se declenchera automatiquement" -ForegroundColor White
Write-Host ""
Write-Host "4. Verifier les images sur DockerHub :" -ForegroundColor White
Write-Host "   https://hub.docker.com" -ForegroundColor Gray
Write-Host ""
Write-Host "5. Tester en mode production :" -ForegroundColor White
Write-Host "   docker-compose -f docker-compose.prod.yml up -d" -ForegroundColor Gray
Write-Host ""
Write-Host "Les badges dans le README passeront au vert automatiquement !" -ForegroundColor Green
Write-Host ""
