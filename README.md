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
- Frontend : http://localhost:8501
- API : http://localhost:8000
- Documentation API : http://localhost:8000/docs

## 🏗️ Architecture

Application microservices avec 3 conteneurs Docker :
- **Streamlit** (Frontend) → Port 8501
- **FastAPI** (Backend) → Port 8000
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

3 workflows GitHub Actions :
- **CI** : Tests automatiques et linting
- **Security** : Scan Gitleaks pour détecter les secrets
- **CD** : Build et push vers DockerHub (tags `latest` + SHA)

## 📁 Structure du Projet

```
.
├── docs/                  # 📚 Documentation Sphinx
├── .github/workflows/     # CI/CD pipelines
├── tests/                 # Tests unitaires et d'intégration
├── app_api/              # Backend FastAPI
├── app_front/            # Frontend Streamlit
├── docker-compose.yml    # Orchestration development
└── docker-compose.prod.yml # Orchestration production
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

