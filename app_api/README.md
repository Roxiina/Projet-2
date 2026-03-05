# API FastAPI - Backend

API REST développée avec FastAPI pour gérer les données.

## 🚀 Démarrage

### Avec uv (recommandé)

```bash
# Installation des dépendances
uv sync

# Lancement en mode développement
uv run uvicorn main:app --reload --port 8000
```

### Avec pip

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

## 📚 Documentation

Une fois l'API lancée, accédez à :
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🧪 Tests

Les tests sont situés à la racine du projet dans le dossier `tests/`.

```bash
# Tests depuis la racine du projet
uv run --directory ./app_api pytest ../tests/ -v

# Avec rapport de couverture
cd ..
uv run --directory ./app_api pytest ../tests/ -v
```

## 📁 Structure

```
app_api/
├── maths/              # Modules mathématiques
│   ├── __init__.py
│   └── mon_module.py
├── models/             # Modèles Pydantic
│   ├── __init__.py
│   └── models.py
├── modules/            # Logique métier
│   ├── __init__.py
│   ├── connect.py      # Connexion DB
│   └── crud.py         # Opérations CRUD
├── data/              # Données de test
│   └── moncsv.csv
├── main.py            # Point d'entrée
├── Dockerfile
└── pyproject.toml

Note: Les tests sont situés dans tests/ à la racine du projet.
```

## 🔌 Endpoints

### GET /
Information sur l'API

### POST /data
Créer une nouvelle donnée
```json
{
  "value": 42.5,
  "description": "Ma description"
}
```

### GET /data
Récupérer toutes les données (avec pagination)

### GET /data/{id}
Récupérer une donnée par ID

### GET /health
Health check de l'API

## 🔧 Configuration

Variables d'environnement (`.env`) :
```
DB_TYPE=postgresql
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=appdb
ENVIRONMENT=development
```

Pour SQLite (développement local) :
```
DB_TYPE=sqlite
```

## 🐳 Docker

```bash
# Build
docker build -t app-api .

# Run
docker run -p 8000:8000 app-api
```
