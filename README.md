# Projet 2 : Orchestration, Sécurité et Livraison Continue

[![CI](https://github.com/Roxiina/Projet-2/actions/workflows/ci.yml/badge.svg)](https://github.com/Roxiina/Projet-2/actions/workflows/ci.yml)
[![Security](https://github.com/Roxiina/Projet-2/actions/workflows/security.yml/badge.svg)](https://github.com/Roxiina/Projet-2/actions/workflows/security.yml)
[![CD](https://github.com/Roxiina/Projet-2/actions/workflows/cd.yml/badge.svg)](https://github.com/Roxiina/Projet-2/actions/workflows/cd.yml)

Application complète de gestion de données avec architecture micro-services, orchestration Docker et CI/CD.

## 📖 Documentation

📚 **Documentation complète disponible dans le dossier [`docs/`](docs/_build/html/index.html)**

La documentation Sphinx couvre en détail :
- 🚀 Installation et démarrage rapide
- 🏗️ Architecture des microservices
- 🧪 Tests et qualité (14 tests, 85% couverture)
- 🐳 Déploiement Docker et CI/CD
- 📋 Guide de contribution et troubleshooting
- 📦 Livrables du projet

Pour consulter la documentation localement :
```bash
cd docs
make.bat html  # Windows
# ou
make html      # Linux/macOS
```

Puis ouvrir `docs/_build/html/index.html` dans votre navigateur.

## 🚀 Démarrage Rapide

### Prérequis

- Docker et Docker Compose
- uv (gestionnaire de paquets Python)
- Git

### Installation

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

- 📚 [Documentation complète](docs/_build/html/index.html)
- 🤝 [Guide de contribution](.github/CONTRIBUTING.md)
- 📜 [Code de conduite](.github/CODE_OF_CONDUCT.md)
- 🎯 [Cahier des charges](Projet_2_Orchestration.md)

## 📄 Licence

Projet pédagogique réalisé dans le cadre de la formation Simplon France.

