# Checklist du Projet 2

Utilisez cette checklist pour suivre votre progression.

## ✅ Phase A : La Logique Métier (Local)

- [x] SQLite de test : Module SQLAlchemy fonctionnel avec SQLite
- [x] API FastAPI : Routes `POST /data` et `GET /data` créées
- [x] Logique métier : Code organisé en modules (maths, connexion, crud, data)
- [x] Frontend Streamlit : Deux pages (Insert et Read)
- [x] Tests : Tests Pytest pour l'API et les maths
- [ ] SQLite non versionnée : Vérifier `.gitignore`
- [ ] Tests lancés : `uv run pytest app_api/tests`

## ✅ Phase B : Variables d'Environnement et Hygiène

- [x] Extraction : Variables sensibles dans `.env`
- [x] `.env` : Fichier créé et exclu par `.gitignore`
- [x] `.env.example` : Template avec variables nécessaires
- [x] `.dockerignore` : Exclusion de `.env`, `.venv`, `__pycache__`

## ✅ Phase C : Orchestration Docker Compose

- [x] Réseau `front-api` : Communication Streamlit ↔ FastAPI
- [x] Réseau `api-db` : Communication FastAPI ↔ PostgreSQL
- [x] BDD invisible au Front : PostgreSQL uniquement sur `api-db`
- [x] Volumes : Configuration de la persistance PostgreSQL
- [ ] Test de persistance : Éteindre/rallumer et vérifier les données
- [ ] `docker-compose.yml` : Fonctionnel en local
- [ ] Application lancée : `docker-compose up -d`

## ✅ Automatisation et Distribution

### CI Améliorée

- [x] `.github/workflows/ci.yml` : Workflow CI créé
- [x] Tests automatisés : Pytest dans la CI
- [x] Linting : Ruff dans la CI
- [x] Build Docker : Test de build des images
- [x] `.github/workflows/security.yml` : Scan Gitleaks
- [ ] Gitleaks testé : Commit avec secret + correction
- [ ] CI au vert : Tous les tests passent

### Livraison Continue (CD)

- [x] `.github/workflows/cd.yml` : Workflow CD créé
- [x] Déclenchement conditionnel : Uniquement si CI verte sur `main`
- [x] Tags Docker : `latest` et `${{ github.sha }}`
- [ ] Secrets GitHub : `DOCKERHUB_USERNAME` et `DOCKERHUB_TOKEN` configurés
- [ ] CD testé : Push sur `main` déclenche le CD
- [ ] Images DockerHub : Vérifier sur hub.docker.com

### Orchestration Finale

- [x] `docker-compose.prod.yml` : Utilise les images DockerHub
- [ ] Test en production : Lancer avec `docker-compose -f docker-compose.prod.yml up -d`
- [ ] Partage : Tester avec un autre groupe

## ✅ Structure et Documentation

- [x] Structure respectée : Voir `Projet_2_Orchestration.md`
- [x] README.md : Documentation complète
- [x] CONTRIBUTING.md : Guide de contribution
- [x] CODE_OF_CONDUCT.md : Code de conduite
- [x] QUICKSTART.md : Guide de démarrage rapide
- [x] Badges : CI, Security, CD dans le README
- [ ] Documentation des services : README dans `app_api/` et `app_front/`

## ✅ Livrables Finaux

### Obligatoires

- [ ] Repository GitHub : Avec tous les fichiers
- [ ] Badges au vert : CI, Coverage, Security
- [ ] `docker-compose.prod.yml` : Fonctionnel
- [ ] Images DockerHub : Publiées et accessibles
- [ ] Gitleaks actif : Dans le pipeline CI

### Bonus

- [x] Makefile : Commandes automatisées
- [x] Scripts PowerShell : Pour Windows
- [x] `.gitleaks.toml` : Configuration personnalisée
- [x] Health checks : Dans Docker Compose
- [x] READMEs détaillés : Pour chaque service

## 🎯 Tests de Validation Finale

Avant de considérer le projet terminé, vérifiez :

1. [ ] **Test Local** :
   ```bash
   docker-compose up -d
   # Accéder à http://localhost:8501
   # Insérer des données
   # Vérifier qu'elles apparaissent dans Read
   docker-compose down
   docker-compose up -d
   # Vérifier que les données sont toujours là (persistance)
   ```

2. [ ] **Test CI** :
   ```bash
   git push origin main
   # Vérifier que la CI passe au vert sur GitHub
   ```

3. [ ] **Test CD** :
   ```bash
   # Après que la CI soit verte
   # Vérifier que le CD se déclenche
   # Vérifier les images sur DockerHub
   ```

4. [ ] **Test Production** :
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   # Vérifier que l'application fonctionne
   # Tester insertion et lecture
   ```

5. [ ] **Test Gitleaks** :
   ```bash
   # Créer une branche
   git checkout -b test-gitleaks
   # Ajouter un secret dans un fichier
   echo "password=mon_secret_123" >> test.txt
   git add test.txt
   git commit -m "test: secret"
   git push origin test-gitleaks
   # Vérifier que Gitleaks détecte le secret
   # Nettoyer la branche
   git checkout main
   git branch -D test-gitleaks
   ```

## 📊 Critères de Réussite

- ✅ Tous les tests passent
- ✅ L'application fonctionne en local
- ✅ L'application fonctionne avec les images DockerHub
- ✅ La CI/CD est fonctionnelle
- ✅ Gitleaks détecte les secrets
- ✅ La documentation est complète
- ✅ Le code est propre et bien organisé

## 🚀 Prêt pour la Présentation

- [ ] Démo de l'application fonctionnelle
- [ ] Explication de l'architecture
- [ ] Présentation du pipeline CI/CD
- [ ] Démonstration de la persistance des données
- [ ] Code source propre et documenté

---

**Bon courage ! 💪**
