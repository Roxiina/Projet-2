# Guide de Test et Validation

Ce guide vous aide à tester et valider chaque partie du projet.

## 🧪 Tests Unitaires

### Tests de l'API

```bash
cd app_api
uv sync
uv run pytest tests/ -v --cov
```

**Ce qui est testé** :
- ✅ Fonctions mathématiques (add, sub, square)
- ✅ Routes de l'API (GET, POST)
- ✅ Gestion des erreurs
- ✅ Validation des données
- ✅ Pagination

**Couverture attendue** : > 80%

### Linting

```bash
# API
cd app_api
uv run ruff check .

# Frontend
cd app_front
uv run ruff check .
```

## 🐳 Tests Docker

### Build des images

```bash
# API
docker build -t app-api:test ./app_api

# Frontend
docker build -t app-front:test ./app_front
```

**Vérifications** :
- ✅ Les images se construisent sans erreur
- ✅ Pas de warnings critiques
- ✅ Taille des images raisonnable

### Test avec Docker Compose (Local)

```bash
# Démarrage
docker-compose up -d

# Vérifier l'état
docker-compose ps

# Tous les services doivent être "Up"
```

**Vérifications** :
1. **Base de données** :
   ```bash
   docker-compose logs db
   # Doit voir "database system is ready to accept connections"
   ```

2. **API** :
   ```bash
   curl http://localhost:8000/health
   # Doit retourner: {"status":"healthy","service":"api"}
   ```

3. **Frontend** :
   - Ouvrir http://localhost:8501
   - Vérifier que la page charge
   - Vérifier que "API connectée" apparaît dans la sidebar

## 🔄 Tests de Fonctionnalités

### Test d'insertion de données

1. Accéder à http://localhost:8501
2. Cliquer sur "Insert" dans la sidebar
3. Entrer une valeur : `42.5`
4. Entrer une description : `Test de validation`
5. Cliquer sur "Enregistrer"

**Résultat attendu** :
- ✅ Message de succès avec ballons 🎈
- ✅ ID de la donnée créée affiché
- ✅ Valeur et date affichées

### Test de lecture de données

1. Cliquer sur "Read" dans la sidebar
2. Vérifier que les données apparaissent

**Résultat attendu** :
- ✅ Tableau avec les données
- ✅ Statistiques affichées
- ✅ Options d'affichage fonctionnelles

### Test de persistance

```bash
# Insérer des données via l'interface
# Puis arrêter les conteneurs
docker-compose down

# Redémarrer
docker-compose up -d

# Vérifier que les données sont toujours là
# Accéder à http://localhost:8501 et aller sur "Read"
```

**Résultat attendu** :
- ✅ Les données insérées avant l'arrêt sont toujours présentes

### Test de la pagination

1. Insérer plus de 10 données
2. Aller sur "Read"
3. Modifier les paramètres de pagination

**Résultat attendu** :
- ✅ La pagination fonctionne
- ✅ Skip et limit fonctionnent correctement

## 🌐 Tests Réseau

### Isolation des réseaux

```bash
# Le frontend ne doit PAS pouvoir accéder directement à la BDD
docker-compose exec front sh -c "ping db" 
# Doit échouer (Name or service not known)

# L'API doit pouvoir accéder à la BDD
docker-compose exec api sh -c "ping db"
# Doit réussir
```

**Vérifications** :
- ✅ Frontend isolé de la BDD
- ✅ API peut communiquer avec la BDD
- ✅ Frontend peut communiquer avec l'API

## 🔒 Tests de Sécurité

### Test Gitleaks Local

```bash
# Installer gitleaks
# Windows (avec Chocolatey): choco install gitleaks
# Mac: brew install gitleaks
# Linux: voir https://github.com/gitleaks/gitleaks

# Scanner le repo
gitleaks detect --source . -v
```

**Résultat attendu** :
- ✅ Aucun secret détecté (sauf dans .env.example)

### Test des variables d'environnement

```bash
# Vérifier qu'aucun .env n'est commité
git ls-files | grep "\.env$"
# Ne doit rien retourner

# Vérifier que .env.example existe
ls .env.example
```

## 🚀 Tests CI/CD

### Test CI sur GitHub

1. Créer une branche :
   ```bash
   git checkout -b test/ci-validation
   ```

2. Faire un changement mineur :
   ```bash
   echo "# Test" >> README.md
   git add README.md
   git commit -m "test: validation CI"
   git push origin test/ci-validation
   ```

3. Créer une Pull Request

**Vérifications** :
- ✅ Les tests passent
- ✅ Le linting passe
- ✅ Le build Docker réussit
- ✅ Gitleaks passe

### Test CD sur GitHub

1. Merger la PR dans `main`

**Vérifications** :
- ✅ Le workflow CD se déclenche
- ✅ Les images sont publiées sur DockerHub
- ✅ Deux tags existent : `latest` et `<commit-sha>`

### Vérification DockerHub

1. Aller sur https://hub.docker.com/
2. Se connecter
3. Vérifier vos repositories

**Résultat attendu** :
- ✅ Repository `app-api` existe
- ✅ Repository `app-front` existe
- ✅ Tag `latest` présent
- ✅ Tag avec SHA du commit présent

## 🌍 Test Production (DockerHub)

```bash
# Créer un fichier .env
cp .env.example .env
# Éditer .env et ajouter :
# DOCKERHUB_USERNAME=votre_username

# Lancer en mode production
docker-compose -f docker-compose.prod.yml up -d

# Vérifier
docker-compose -f docker-compose.prod.yml ps
```

**Vérifications** :
- ✅ Images téléchargées depuis DockerHub
- ✅ Application fonctionnelle
- ✅ Données persistantes

## 📊 Tests de Performance (Bonus)

### Test de charge API

```bash
# Installer apache bench
# apt-get install apache2-utils  (Linux)
# brew install httpd             (Mac)

# Test simple
ab -n 100 -c 10 http://localhost:8000/data
```

### Test de montée en charge

```bash
# Créer beaucoup de données
for i in {1..100}; do
  curl -X POST http://localhost:8000/data \
    -H "Content-Type: application/json" \
    -d "{\"value\": $i, \"description\": \"Test $i\"}"
done

# Vérifier que l'application reste responsive
```

## ✅ Checklist de Validation Complète

Avant de considérer le projet terminé :

- [ ] Tous les tests unitaires passent
- [ ] Le linting ne retourne aucune erreur
- [ ] Les images Docker se construisent
- [ ] Docker Compose fonctionne en local
- [ ] Les données persistent après redémarrage
- [ ] L'isolation réseau est respectée
- [ ] Aucun secret n'est détecté par Gitleaks
- [ ] La CI passe au vert sur GitHub
- [ ] Le CD publie les images sur DockerHub
- [ ] Docker Compose prod fonctionne
- [ ] L'interface est fonctionnelle et intuitive
- [ ] La documentation est complète

## 🐛 Débogage

### Logs utiles

```bash
# Tous les logs
docker-compose logs -f

# Logs spécifiques
docker-compose logs -f api
docker-compose logs -f db
docker-compose logs -f front

# Logs avec timestamp
docker-compose logs -f --timestamps
```

### Inspect des conteneurs

```bash
# État détaillé
docker-compose ps -a

# Inspecter un conteneur
docker inspect <container_name>

# Entrer dans un conteneur
docker-compose exec api sh
docker-compose exec db psql -U postgres -d appdb
```

### Vérification de la base de données

```bash
# Se connecter à PostgreSQL
docker-compose exec db psql -U postgres -d appdb

# Dans psql:
\dt              # Lister les tables
SELECT * FROM data LIMIT 10;  # Voir les données
\q               # Quitter
```

## 📞 Support

Si vous rencontrez des problèmes :

1. Vérifiez les logs : `docker-compose logs -f`
2. Vérifiez l'état : `docker-compose ps`
3. Arrêtez tout : `docker-compose down -v`
4. Reconstruisez : `docker-compose build --no-cache`
5. Redémarrez : `docker-compose up -d`

---

**Bon courage pour les tests ! 🧪**
