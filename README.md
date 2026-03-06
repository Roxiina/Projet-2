# Projet 2 : Orchestration, Sécurité et Livraison Continue

[![CI](https://github.com/Roxiina/Projet-2/actions/workflows/ci.yml/badge.svg)](https://github.com/Roxiina/Projet-2/actions/workflows/ci.yml)
[![Security](https://github.com/Roxiina/Projet-2/actions/workflows/security.yml/badge.svg)](https://github.com/Roxiina/Projet-2/actions/workflows/security.yml)
[![CD](https://github.com/Roxiina/Projet-2/actions/workflows/cd.yml/badge.svg)](https://github.com/Roxiina/Projet-2/actions/workflows/cd.yml)
[![Documentation](https://github.com/Roxiina/Projet-2/actions/workflows/docs.yml/badge.svg)](https://github.com/Roxiina/Projet-2/actions/workflows/docs.yml)

Application complète de gestion de données avec architecture micro-services, orchestration Docker et CI/CD.

## 📖 Documentation

### 🌐 Documentation en ligne

📚 **[Consulter la documentation complète sur GitHub Pages](https://roxiina.github.io/Projet-2/)**

> ⚠️ **Note** : Si le lien ne fonctionne pas encore, activez GitHub Pages :
> 1. Allez dans **Settings** → **Pages**
> 2. Source : **GitHub Actions**
> 3. La documentation sera automatiquement déployée au prochain push

### 💻 Documentation locale

Pour générer et consulter la documentation en local :

**Windows :**
```bash
cd docs
pip install -r requirements.txt
make.bat html
start _build/html/index.html
```

**Linux/macOS :**
```bash
cd docs
pip install -r requirements.txt
make html
open _build/html/index.html  # ou xdg-open sur Linux
```

**🚀 Raccourci Windows (script automatisé) :**
```powershell
.\scripts\view-docs.ps1
```

### 📚 Contenu de la documentation

La documentation Sphinx couvre en détail :
- 🚀 Installation et démarrage rapide
- 🏗️ Architecture des microservices (Frontend, API, Database)
- 🧪 Tests et qualité du code (couverture > 80%)
- 🐳 Déploiement Docker et orchestration
- 🔄 CI/CD avec GitHub Actions
- 📋 Guide de contribution et troubleshooting
- 📦 Livrables du projet

## 🚀 Démarrage Rapide

### Prérequis

- Docker et Docker Compose
- uv (gestionnaire de paquets Python)
- Git

### Installation

1. **Cloner le repository**
```bash
git clone https://github.com/Roxiina/Projet-2.git
cd Projet-2
```

2. **Configurer l'environnement**
```bash
cp .env.example .env
# Éditez .env avec vos valeurs
```

3. **Lancer l'application**
```bash
docker-compose up -d
```

4. **Accéder aux services**
- **Frontend Streamlit** : [http://localhost:8501](http://localhost:8501)
- **API FastAPI** : [http://localhost:8000](http://localhost:8000)
- **Documentation API** : [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health check** : [http://localhost:8000/health](http://localhost:8000/health)

## 🏗️ Architecture

Application microservices avec 3 conteneurs Docker :
- **Streamlit** (Frontend) → Port 8501 - [http://localhost:8501](http://localhost:8501)
- **FastAPI** (Backend) → Port 8000 - [http://localhost:8000](http://localhost:8000)
  - Documentation API interactive : [http://localhost:8000/docs](http://localhost:8000/docs)
  - Health check : [http://localhost:8000/health](http://localhost:8000/health)
- **PostgreSQL** (Database) → Port 5432 (interne)

Réseaux isolés :
- `front-api` : Communication Streamlit ↔ FastAPI
- `api-db` : Communication FastAPI ↔ PostgreSQL

## 🧪 Tests et Qualité

```bash
# Tests (14 tests, 85% couverture)
uv run --directory ./app_api pytest ../tests/ -v

# Linting (Ruff)
cd app_api && uv run ruff check .
cd app_front && uv run ruff check .
```

## 🚢 CI/CD

4 workflows GitHub Actions automatisés :

### 1. **CI - Intégration Continue** ✅
- Tests unitaires (14 tests)
- Linting Ruff (API + Frontend)
- Couverture de code (pytest-cov)
- Déclenché sur : `push` et `pull_request` (branches `main` et `develop`)

### 2. **Security - Sécurité** 🔒
- Scan Gitleaks pour détecter les secrets
- Analyse de l'historique Git complet
- Déclenché sur : `push` et `pull_request` (branches `main` et `develop`)

### 3. **CD - Livraison Continue** 🚀
- Build des images Docker (API + Frontend)
- Push vers DockerHub avec tags :
  - `latest` : Dernière version stable
  - `<commit-sha>` : Version spécifique pour rollback
- Déclenché sur : `push` sur `main` (après succès de la CI)

### 4. **Documentation** 📚
- Build de la documentation Sphinx
- Déploiement automatique sur GitHub Pages
- Déclenché sur : `push` sur `main`

> 📊 Tous les statuts sont visibles via les badges en haut du README

## 📁 Structure du Projet

```
.
├── 📚 docs/                      # Documentation Sphinx
│   ├── _build/html/             # Documentation HTML générée
│   ├── architecture/            # Architecture microservices
│   ├── deployment/              # Guides déploiement
│   ├── guides/                  # Guides contribution
│   ├── testing/                 # Documentation tests
│   ├── conf.py                  # Configuration Sphinx
│   └── requirements.txt         # Dépendances doc
│
├── 🔧 .github/                  # Configuration GitHub
│   ├── workflows/               # CI/CD pipelines
│   │   ├── ci.yml              # Tests & Linting
│   │   ├── security.yml        # Gitleaks scan
│   │   ├── cd.yml              # Docker build & push
│   │   └── docs.yml            # Déploiement GitHub Pages
│   ├── CONTRIBUTING.md          # Guide contribution
│   └── CODE_OF_CONDUCT.md       # Code de conduite
│
├── 🧪 tests/                    # Tests unitaires & intégration
│   ├── test_api.py             # Tests API (9 tests)
│   └── test_math_csv.py        # Tests modules maths (5 tests)
│
├── 🔌 app_api/                  # Backend FastAPI
│   ├── maths/                   # Modules mathématiques
│   │   └── mon_module.py       # Fonctions add, sub, square
│   ├── models/                  # Modèles Pydantic v2
│   │   └── models.py           # DataCreate, DataResponse
│   ├── modules/                 # Logique métier
│   │   ├── connect.py          # Connexion DB SQLAlchemy 2.0
│   │   └── crud.py             # Opérations CRUD
│   ├── data/                    # Données de test
│   │   └── moncsv.csv
│   ├── main.py                  # Point d'entrée API
│   ├── Dockerfile               # Image Docker multi-stage
│   └── pyproject.toml           # Dépendances uv
│
├── 🖥️ app_front/                # Frontend Streamlit
│   ├── pages/                   # Pages Streamlit
│   │   ├── 0_insert.py         # Page insertion
│   │   └── 1_read.py           # Page lecture
│   ├── main.py                  # Page d'accueil
│   ├── Dockerfile               # Image Docker
│   └── pyproject.toml           # Dépendances uv
│
├── 🛠️ scripts/                  # Scripts utilitaires
│   ├── deploy.ps1               # Déploiement production
│   ├── start.ps1                # Démarrage services
│   ├── stop.ps1                 # Arrêt services
│   ├── test.ps1                 # Lancement tests
│   ├── logs.ps1                 # Consultation logs
│   └── view-docs.ps1            # Génération & ouverture doc
│
├── 🐳 docker-compose.yml        # Orchestration développement
├── 🚢 docker-compose.prod.yml   # Orchestration production
├── 📋 conftest.py               # Configuration pytest
├── 🔐 .env.example              # Template variables d'env
├── 🚫 .gitignore                # Fichiers exclus Git
├── 🚫 .dockerignore             # Fichiers exclus Docker
├── 🔒 .gitleaks.toml            # Configuration Gitleaks
├── 📖 README.md                 # Ce fichier
└── 📝 Projet_2_Orchestration.md  # Cahier des charges
```

## 🔗 Liens Utiles

- 📚 [Documentation complète](https://roxiina.github.io/Projet-2/) (GitHub Pages)
- 🤝 [Guide de contribution](.github/CONTRIBUTING.md)
- 📜 [Code de conduite](.github/CODE_OF_CONDUCT.md)
- 🎯 [Cahier des charges](Projet_2_Orchestration.md)
- 🐳 [DockerHub - API](https://hub.docker.com/r/roxiina/app-api)
- 🐳 [DockerHub - Frontend](https://hub.docker.com/r/roxiina/app-front)

## 📄 Licence

Projet pédagogique réalisé dans le cadre de la formation Simplon France.

