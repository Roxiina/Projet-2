# Guide de Dépannage

Ce guide vous aide à résoudre les problèmes courants.

## 🔴 Problèmes de Démarrage

### Les conteneurs ne démarrent pas

**Symptômes** :
```bash
docker-compose ps
# Montre des conteneurs "Exited" ou "Restarting"
```

**Solutions** :

1. **Vérifier les logs** :
   ```bash
   docker-compose logs
   ```

2. **Ports déjà utilisés** :
   ```bash
   # Windows
   netstat -ano | findstr "8000"
   netstat -ano | findstr "8501"
   netstat -ano | findstr "5432"
   
   # Linux/Mac
   lsof -i :8000
   lsof -i :8501
   lsof -i :5432
   ```
   
   **Solution** : Arrêtez le processus ou changez le port dans `docker-compose.yml`

3. **Fichier .env manquant ou incorrect** :
   ```bash
   # Vérifier que .env existe
   ls .env
   
   # Si non, créer depuis .env.example
   cp .env.example .env
   ```

4. **Volumes corrompus** :
   ```bash
   docker-compose down -v
   docker-compose up -d
   ```

### La base de données ne démarre pas

**Symptômes** :
```bash
docker-compose logs db
# Erreurs PostgreSQL ou redémarrage en boucle
```

**Solutions** :

1. **Permission sur les volumes** :
   ```bash
   docker-compose down -v
   docker volume rm postgres_data
   docker-compose up -d
   ```

2. **Variables d'environnement incorrectes** :
   - Vérifier `.env`
   - Vérifier que POSTGRES_PASSWORD est défini

3. **Attendre plus longtemps** :
   PostgreSQL prend du temps au premier démarrage (30-60 secondes)

### L'API ne se connecte pas à la BDD

**Symptômes** :
```bash
docker-compose logs api
# Erreurs de connexion PostgreSQL
```

**Solutions** :

1. **Vérifier le réseau** :
   ```bash
   docker network ls
   docker network inspect api-db
   ```

2. **Vérifier les variables d'environnement** :
   ```bash
   docker-compose exec api env | grep POSTGRES
   ```

3. **Tester la connexion manuellement** :
   ```bash
   docker-compose exec api ping db
   ```

4. **Attendre le health check** :
   ```bash
   docker-compose ps
   # Attendre que db soit "healthy"
   ```

## 🌐 Problèmes d'Accès

### Le frontend ne charge pas

**Symptômes** :
- http://localhost:8501 ne répond pas
- Page blanche ou erreur de connexion

**Solutions** :

1. **Vérifier que le conteneur tourne** :
   ```bash
   docker-compose ps front
   ```

2. **Vérifier les logs** :
   ```bash
   docker-compose logs front
   ```

3. **Vérifier le port** :
   ```bash
   curl http://localhost:8501
   ```

4. **Redémarrer le service** :
   ```bash
   docker-compose restart front
   ```

### L'API ne répond pas

**Symptômes** :
- http://localhost:8000 ne répond pas
- Frontend affiche "API non accessible"

**Solutions** :

1. **Tester le health check** :
   ```bash
   curl http://localhost:8000/health
   ```

2. **Vérifier les logs** :
   ```bash
   docker-compose logs api
   ```

3. **Tester depuis l'intérieur du conteneur** :
   ```bash
   docker-compose exec api curl http://localhost:8000/health
   ```

### Le frontend ne peut pas communiquer avec l'API

**Symptômes** :
- Frontend charge mais affiche "API non accessible"
- Erreurs de connexion dans les logs du frontend

**Solutions** :

1. **Vérifier la variable API_URL** :
   ```bash
   docker-compose exec front env | grep API_URL
   # Doit être : http://api:8000
   ```

2. **Vérifier le réseau** :
   ```bash
   docker-compose exec front ping api
   ```

3. **Vérifier que l'API est sur le bon réseau** :
   ```bash
   docker network inspect front-api
   # Doit voir api et front
   ```

## 🐛 Problèmes de Données

### Les données ne persistent pas

**Symptômes** :
- Après `docker-compose down` et `up`, les données disparaissent

**Solutions** :

1. **Vérifier que vous n'utilisez pas -v** :
   ```bash
   # ❌ Mauvais (supprime les volumes)
   docker-compose down -v
   
   # ✅ Bon
   docker-compose down
   ```

2. **Vérifier les volumes** :
   ```bash
   docker volume ls | grep postgres
   # Doit voir postgres_data
   ```

3. **Inspecter le volume** :
   ```bash
   docker volume inspect postgres_data
   ```

### Erreur "Donnée non trouvée"

**Symptômes** :
- L'API retourne 404 pour des données qui existent

**Solutions** :

1. **Vérifier la base de données** :
   ```bash
   docker-compose exec db psql -U postgres -d appdb -c "SELECT * FROM data;"
   ```

2. **Vérifier les migrations** :
   Les tables sont créées automatiquement au démarrage de l'API

3. **Recréer les tables** :
   ```bash
   docker-compose down
   docker-compose up -d
   ```

## 🔒 Problèmes de Sécurité

### Gitleaks détecte des faux positifs

**Solutions** :

1. **Vérifier `.gitleaks.toml`** :
   Les exemples et tests doivent être dans les allowlists

2. **Ajouter des exceptions** :
   Éditez `.gitleaks.toml` et ajoutez dans `[allowlist]`

3. **Vérifier les fichiers** :
   ```bash
   git ls-files | grep -E "\.env$"
   # Ne doit rien retourner
   ```

### Variables d'environnement non chargées

**Symptômes** :
- Erreurs de connexion
- Valeurs par défaut utilisées

**Solutions** :

1. **Vérifier le fichier .env** :
   ```bash
   cat .env
   ```

2. **Redémarrer les conteneurs** :
   ```bash
   docker-compose down
   docker-compose up -d
   ```

3. **Vérifier dans le conteneur** :
   ```bash
   docker-compose exec api env
   ```

## 🚀 Problèmes CI/CD

### La CI échoue sur GitHub

**Solutions** :

1. **Vérifier les logs GitHub Actions** :
   - Aller dans l'onglet "Actions" du repository
   - Cliquer sur le workflow en échec
   - Lire les logs

2. **Tests échouent localement** :
   ```bash
   cd app_api
   uv run pytest tests/ -v
   ```

3. **Linting échoue** :
   ```bash
   uv run ruff check .
   uv run ruff format .  # Pour corriger
   ```

### Le CD ne se déclenche pas

**Symptômes** :
- La CI passe mais le CD ne démarre pas

**Solutions** :

1. **Vérifier le nom du workflow** :
   Dans `.github/workflows/cd.yml`, vérifier :
   ```yaml
   workflows: ["CI Standardisation Projet 2"]
   ```
   Doit correspondre exactement au `name` dans `ci.yml`

2. **Vérifier la branche** :
   Le CD ne se déclenche que sur `main`

3. **Vérifier que la CI a réussi** :
   Le CD attend que la CI soit verte

### Les images ne sont pas publiées sur DockerHub

**Symptômes** :
- Le CD passe mais pas d'images sur DockerHub

**Solutions** :

1. **Vérifier les secrets GitHub** :
   Settings → Secrets → Actions
   - DOCKERHUB_USERNAME
   - DOCKERHUB_TOKEN

2. **Vérifier le token DockerHub** :
   - Le token a-t-il les bonnes permissions ?
   - Le token est-il toujours valide ?

3. **Vérifier les logs du workflow CD**

## 🐳 Problèmes Docker

### Erreur "No space left on device"

**Solutions** :

```bash
# Nettoyer Docker
docker system prune -a

# Supprimer les volumes inutilisés
docker volume prune

# Supprimer les images inutilisées
docker image prune -a
```

### Build très lent

**Solutions** :

1. **Utiliser le cache** :
   ```bash
   docker-compose build
   ```

2. **Vérifier .dockerignore** :
   Doit exclure `.venv`, `__pycache__`, etc.

3. **Nettoyer** :
   ```bash
   docker-compose build --no-cache
   ```

### Erreur "Cannot connect to Docker daemon"

**Solutions** :

1. **Windows** :
   - Vérifier que Docker Desktop est démarré
   - Redémarrer Docker Desktop

2. **Linux** :
   ```bash
   sudo systemctl start docker
   ```

3. **Permissions** :
   ```bash
   sudo usermod -aG docker $USER
   # Se déconnecter et reconnecter
   ```

## 💻 Problèmes de Développement Local

### uv n'est pas trouvé

**Solutions** :

```bash
# Installation
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
irm https://astral.sh/uv/install.ps1 | iex

# Ajouter au PATH
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Les dépendances ne s'installent pas

**Solutions** :

```bash
# Supprimer l'environnement virtuel
rm -rf .venv

# Réinstaller
uv sync

# Ou avec force
uv sync --refresh
```

### Tests échouent localement

**Solutions** :

1. **Vérifier les dépendances** :
   ```bash
   cd app_api
   uv sync
   ```

2. **Vérifier Python version** :
   ```bash
   python --version
   # Doit être 3.11 ou supérieur
   ```

3. **Nettoyer les caches** :
   ```bash
   find . -type d -name "__pycache__" -exec rm -rf {} +
   find . -type d -name ".pytest_cache" -exec rm -rf {} +
   ```

## 📞 Commandes de Diagnostic

### Vérifier l'état complet

```bash
# État des services
docker-compose ps

# Utilisation des ressources
docker stats

# Réseaux
docker network ls

# Volumes
docker volume ls

# Logs de tous les services
docker-compose logs --tail=50
```

### Reset complet

```bash
# ATTENTION : Supprime TOUT (données incluses)
docker-compose down -v
docker system prune -af
docker volume prune -f
docker-compose up -d --build
```

## 🆘 Obtenir de l'Aide

Si rien ne fonctionne :

1. **Collecter les logs** :
   ```bash
   docker-compose logs > logs.txt
   ```

2. **Créer une issue GitHub** avec :
   - Description du problème
   - Logs pertinents
   - Commandes exécutées
   - Système d'exploitation
   - Version de Docker

3. **Vérifier la documentation** :
   - README.md
   - QUICKSTART.md
   - TESTING.md

---

**Bon débogage ! 🔧**
