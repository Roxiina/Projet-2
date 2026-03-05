# Guide de Démarrage Rapide

## 🚀 Démarrage en 5 minutes

### Option 1 : Avec Docker Compose (Recommandé)

1. **Clonez et préparez l'environnement** :
```bash
git clone https://github.com/VOTRE_USERNAME/VOTRE_REPO.git
cd VOTRE_REPO
cp .env.example .env
```

2. **Lancez l'application** :
```bash
docker-compose up -d
```

3. **Accédez à l'application** :
- Frontend: http://localhost:8501
- API: http://localhost:8000
- Documentation API: http://localhost:8000/docs

### Option 2 : Développement Local (sans Docker)

#### API

```bash
cd app_api

# Installation de uv (si pas déjà installé)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Installation des dépendances
uv sync

# Lancement de l'API
uv run uvicorn main:app --reload --port 8000
```

#### Frontend

```bash
cd app_front

# Installation des dépendances
uv sync

# Lancement du frontend
export API_URL=http://localhost:8000
uv run streamlit run main.py
```

## 🧪 Tests

```bash
cd app_api
uv run pytest tests/ -v --cov
```

## 🛑 Arrêt de l'application

```bash
docker-compose down
```

Pour arrêter ET supprimer les volumes (données) :
```bash
docker-compose down -v
```

## 🔍 Logs

Voir les logs en temps réel :
```bash
docker-compose logs -f

# Logs d'un service spécifique
docker-compose logs -f api
docker-compose logs -f front
docker-compose logs -f db
```

## 🔄 Mise à jour

```bash
git pull
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 📊 Vérification de l'état des services

```bash
docker-compose ps
```

## ❓ Problèmes courants

### Port déjà utilisé

Si un port est déjà utilisé, modifiez dans `docker-compose.yml` :
```yaml
ports:
  - "8000:8000"  # Changez 8000 par 8001 par exemple
```

### Base de données ne démarre pas

Attendez quelques secondes, PostgreSQL prend un peu de temps au premier démarrage.

### API ne se connecte pas à la BDD

Vérifiez les variables d'environnement dans `.env`.

## 🎯 Commandes utiles

```bash
# Reconstruire les images
docker-compose build

# Redémarrer un service
docker-compose restart api

# Voir l'utilisation des ressources
docker stats

# Nettoyer Docker
docker system prune -a
```
