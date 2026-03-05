======
Docker
======

Déploiement avec Docker et Docker Compose.

Introduction
============

Le projet utilise **Docker** et **Docker Compose** pour :

* Isolation des services
* Reproductibilité des environnements
* Facilité de déploiement
* Portabilité (Windows, Linux, macOS)

Architecture Docker
===================

Trois Services
--------------

.. code-block:: text

   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
   │  Streamlit  │────▶│   FastAPI   │────▶│ PostgreSQL  │
   │   (front)   │     │    (api)    │     │    (db)     │
   └─────────────┘     └─────────────┘     └─────────────┘
      Port 8501          Port 8000           Port 5432

Images Docker
=============

API (FastAPI)
-------------

Fichier: ``app_api/Dockerfile``

.. code-block:: dockerfile

   FROM python:3.11-slim
   
   # Install curl for health checks
   RUN apt-get update && \\
       apt-get install -y curl && \\
       rm -rf /var/lib/apt/lists/*
   
   # Install uv
   COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
   
   WORKDIR /app
   
   # Copy dependency files
   COPY pyproject.toml uv.lock ./
   
   # Install dependencies
   RUN uv sync --frozen --no-dev
   
   # Copy application
   COPY . .
   
   EXPOSE 8000
   
   CMD ["uv", "run", "uvicorn", "main:app", \\
        "--host", "0.0.0.0", "--port", "8000"]

Frontend (Streamlit)
--------------------

Fichier: ``app_front/Dockerfile``

.. code-block:: dockerfile

   FROM python:3.11-slim
   
   COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
   
   WORKDIR /app
   
   COPY pyproject.toml uv.lock ./
   RUN uv sync --frozen --no-dev
   
   COPY . .
   
   EXPOSE 8501
   
   CMD ["uv", "run", "streamlit", "run", "main.py", \\
        "--server.port", "8501", \\
        "--server.address", "0.0.0.0"]

Docker Compose
==============

Fichier de Développement
-------------------------

``docker-compose.yml`` - Build local :

.. code-block:: yaml

   version: '3.8'
   
   services:
     db:
       image: postgres:15-alpine
       environment:
         POSTGRES_DB: ${POSTGRES_DB}
         POSTGRES_USER: ${POSTGRES_USER}
         POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
       volumes:
         - postgres_data:/var/lib/postgresql/data
       networks:
         - api-db
       healthcheck:
         test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
         interval: 10s
         timeout: 5s
         retries: 5
     
     api:
       build:
         context: ./app_api
         dockerfile: Dockerfile
       ports:
         - "8000:8000"
       environment:
         DATABASE_URL: ${DATABASE_URL}
       depends_on:
         db:
           condition: service_healthy
       networks:
         - front-api
         - api-db
       healthcheck:
         test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
         interval: 30s
         timeout: 10s
         retries: 3
         start_period: 40s
     
     front:
       build:
         context: ./app_front
         dockerfile: Dockerfile
       ports:
         - "8501:8501"
       environment:
         API_URL: ${API_URL}
       depends_on:
         api:
           condition: service_healthy
       networks:
         - front-api
   
   volumes:
     postgres_data:
       driver: local
   
   networks:
     front-api:
       driver: bridge
     api-db:
       driver: bridge

Fichier de Production
----------------------

``docker-compose.prod.yml`` - Images DockerHub :

.. code-block:: yaml

   version: '3.8'
   
   services:
     db:
       image: postgres:15-alpine
       # ... même config ...
     
     api:
       image: roxiina/projet-2-api:latest
       # ... même config SAUF build ...
     
     front:
       image: roxiina/projet-2-front:latest
       # ... même config SAUF build ...

Commandes Docker Compose
=========================

Développement
-------------

**Démarrer** (avec build) :

.. code-block:: bash

   docker-compose up --build

**Démarrer en arrière-plan** :

.. code-block:: bash

   docker-compose up -d

**Arrêter** :

.. code-block:: bash

   docker-compose down

**Arrêter et supprimer les volumes** :

.. code-block:: bash

   docker-compose down -v

Production
----------

**Démarrer avec les images** :

.. code-block:: bash

   docker-compose -f docker-compose.prod.yml up -d

Logs
----

**Voir tous les logs** :

.. code-block:: bash

   docker-compose logs -f

**Logs d'un service** :

.. code-block:: bash

   docker-compose logs -f api

Santé des Services
------------------

**Statut des conteneurs** :

.. code-block:: bash

   docker-compose ps

Sortie :

.. code-block:: text

   NAME           IMAGE       STATUS                   PORTS
   api            app-api     Up (healthy)             0.0.0.0:8000->8000/tcp
   db             postgres    Up (healthy)             5432/tcp
   front          app-front   Up                       0.0.0.0:8501->8501/tcp

Rebuild
-------

**Reconstruire les images** :

.. code-block:: bash

   docker-compose build --no-cache

Health Checks
=============

API
---

.. code-block:: yaml

   healthcheck:
     test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
     interval: 30s
     timeout: 10s
     retries: 3
     start_period: 40s

* Vérifie ``/health`` toutes les 30s
* Attend 40s avant de commencer (temps de démarrage)
* 3 tentatives avant de marquer comme ``unhealthy``

Database
--------

.. code-block:: yaml

   healthcheck:
     test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
     interval: 10s
     timeout: 5s
     retries: 5

Réseaux
=======

Isolation
---------

Deux réseaux isolés :

**front-api** : Streamlit ↔ FastAPI

.. code-block:: yaml

   networks:
     front-api:
       driver: bridge

**api-db** : FastAPI ↔ PostgreSQL

.. code-block:: yaml

   networks:
     api-db:
       driver: bridge

Le frontend ne peut PAS accéder directement à la base.

Volumes
=======

Persistance des Données
------------------------

.. code-block:: yaml

   volumes:
     postgres_data:
       driver: local

Les données PostgreSQL sont persistées dans ce volume.

Inspection
----------

.. code-block:: bash

   # Lister les volumes
   docker volume ls
   
   # Inspecter un volume
   docker volume inspect projet_2_postgres_data

Backup
------

.. code-block:: bash

   docker run --rm \\
     -v projet_2_postgres_data:/data \\
     -v $(pwd):/backup \\
     alpine tar czf /backup/postgres_backup.tar.gz /data

Optimisations
=============

Multi-stage Build
-----------------

Réduire la taille des images :

.. code-block:: dockerfile

   # Stage 1: Builder
   FROM python:3.11 AS builder
   COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
   WORKDIR /app
   COPY pyproject.toml uv.lock ./
   RUN uv sync --frozen --no-dev
   
   # Stage 2: Runtime
   FROM python:3.11-slim
   COPY --from=builder /app/.venv /app/.venv
   COPY . .
   CMD ["/app/.venv/bin/uvicorn", "main:app"]

.dockerignore
-------------

Créer ``.dockerignore`` pour exclure fichiers inutiles :

.. code-block:: text

   .git
   .venv
   __pycache__
   *.pyc
   .pytest_cache
   .ruff_cache
   htmlcov
   .coverage
   *.md

Dépannage
=========

Port Déjà Utilisé
-----------------

**Erreur** : ``Bind for 0.0.0.0:8501 failed: port is already allocated``

**Solution** :

.. code-block:: bash

   # Windows
   netstat -ano | findstr :8501
   taskkill /PID <PID> /F
   
   # Linux/macOS
   lsof -ti:8501 | xargs kill -9

Service Unhealthy
-----------------

**Problème** : Un service reste ``starting`` ou passe à ``unhealthy``

**Solution** :

1. Vérifier les logs :

.. code-block:: bash

   docker-compose logs api

2. Vérifier le health check manuellement :

.. code-block:: bash

   docker-compose exec api curl http://localhost:8000/health

3. Augmenter ``start_period`` si nécessaire

Build Lent
----------

**Solution** :

* Utiliser les caches Docker
* Ordonner les ``COPY`` (dépendances avant code)
* Utiliser ``.dockerignore``

Prochaines Sections
===================

* :doc:`cicd` : CI/CD avec GitHub Actions
* :doc:`production` : Déploiement en production
* :doc:`secrets` : Gestion des secrets
