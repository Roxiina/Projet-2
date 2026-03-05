=============
Configuration
=============

Guide de configuration pour différents environnements.

Variables d'Environnement
==========================

Fichier .env Principal
----------------------

Ce fichier contient toutes les variables d'environnement pour Docker Compose.

.. code-block:: bash

   # PostgreSQL
   POSTGRES_DB=projet2_db
   POSTGRES_USER=projet2_user
   POSTGRES_PASSWORD=projet2_password
   POSTGRES_PORT=5432
   
   # API
   DATABASE_URL=postgresql://projet2_user:projet2_password@db:5432/projet2_db
   API_URL=http://api:8000
   API_PORT=8000
   
   # Frontend
   STREAMLIT_PORT=8501

Configuration par Service
==========================

API FastAPI
-----------

Le fichier ``app_api/pyproject.toml`` configure les dépendances et outils :

.. code-block:: toml

   [project]
   name = "app-api"
   version = "1.0.0"
   requires-python = ">=3.11"
   dependencies = [
       "fastapi>=0.104.0",
       "uvicorn[standard]>=0.24.0",
       "sqlalchemy>=2.0.0",
       "psycopg2-binary>=2.9.9",
       "python-dotenv>=1.0.0",
       "pydantic>=2.5.0",
   ]
   
   [project.optional-dependencies]
   dev = [
       "pytest>=7.4.0",
       "pytest-cov>=4.1.0",
       "httpx>=0.25.0",
       "ruff>=0.1.0",
   ]

Configuration Ruff (Linting)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: toml

   [tool.ruff]
   line-length = 100
   target-version = "py311"
   
   [tool.ruff.lint]
   select = ["E", "F", "I", "N", "W"]
   ignore = [
       "N806",  # Variable in function should be lowercase
   ]

Configuration Pytest
~~~~~~~~~~~~~~~~~~~~

Les tests utilisent ``conftest.py`` à la racine pour configurer le PYTHONPATH.

Frontend Streamlit
------------------

Configuration dans ``app_front/pyproject.toml`` :

.. code-block:: toml

   [project]
   name = "app-front"
   version = "1.0.0"
   requires-python = ">=3.11"
   dependencies = [
       "streamlit>=1.28.0",
       "requests>=2.31.0",
       "pandas>=2.1.0",
   ]

Configuration Streamlit
~~~~~~~~~~~~~~~~~~~~~~~

Créer ``.streamlit/config.toml`` pour personnaliser :

.. code-block:: toml

   [theme]
   primaryColor = "#0066cc"
   backgroundColor = "#ffffff"
   secondaryBackgroundColor = "#f0f2f6"
   textColor = "#262730"
   font = "sans serif"
   
   [server]
   port = 8501
   enableCORS = false
   enableXsrfProtection = true

Base de Données
===============

PostgreSQL (Production)
-----------------------

Configuration dans ``docker-compose.yml`` :

.. code-block:: yaml

   db:
     image: postgres:15-alpine
     environment:
       POSTGRES_DB: ${POSTGRES_DB}
       POSTGRES_USER: ${POSTGRES_USER}
       POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
     volumes:
       - postgres_data:/var/lib/postgresql/data

SQLite (Développement/Tests)
-----------------------------

Pour les tests, une base SQLite est utilisée :

.. code-block:: python

   # Dans conftest.py ou test files
   DATABASE_URL = "sqlite:///./test_db.sqlite"

Docker
======

Dockerfile API
--------------

Multi-stage build pour optimiser la taille :

.. code-block:: dockerfile

   FROM python:3.11-slim
   
   # Install curl for health checks
   RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
   
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
   
   CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

Docker Compose
--------------

Réseaux isolés pour la sécurité :

.. code-block:: yaml

   networks:
     front-api:
       driver: bridge
     api-db:
       driver: bridge

Health Checks
~~~~~~~~~~~~~

.. code-block:: yaml

   healthcheck:
     test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
     interval: 30s
     timeout: 10s
     retries: 3
     start_period: 40s

GitHub Actions
==============

Configuration CI/CD
-------------------

Fichiers dans ``.github/workflows/`` :

* ``ci.yml`` : Tests et linting
* ``security.yml`` : Scan Gitleaks
* ``cd.yml`` : Déploiement DockerHub

Secrets Requis
~~~~~~~~~~~~~~

Configuration dans GitHub Settings > Secrets :

.. code-block:: text

   DOCKERHUB_USERNAME : Nom d'utilisateur DockerHub
   DOCKERHUB_TOKEN    : Token d'accès DockerHub

Voir :doc:`../deployment/secrets` pour plus de détails.

Gitleaks
========

Configuration dans ``.gitleaks.toml`` :

.. code-block:: toml

   [extend]
   useDefault = true
   
   [[rules]]
   id = "custom-password-rule"
   description = "Custom password detection"
   regex = '''(?i)(password|passwd|pwd)\s*[:=]\s*["']?[^"\s]+["']?'''
   
   [allowlist]
   paths = [
       '''\\.env\\.example$''',
       '''test.*''',
   ]

IDE Configuration
=================

VS Code
-------

Créer ``.vscode/settings.json`` :

.. code-block:: json

   {
     "python.defaultInterpreterPath": "./app_api/.venv/bin/python",
     "python.formatting.provider": "none",
     "python.linting.enabled": true,
     "python.linting.ruffEnabled": true,
     "editor.formatOnSave": true,
     "files.exclude": {
       "**/__pycache__": true,
       "**/*.pyc": true,
       ".pytest_cache": true,
       ".ruff_cache": true
     }
   }

PyCharm
-------

1. Ouvrir le projet
2. File > Settings > Project > Python Interpreter
3. Ajouter l'interpréteur : ``app_api/.venv/bin/python``
4. Activer Ruff : Settings > Tools > Ruff

Configuration de Production
============================

Voir le guide :doc:`../deployment/production` pour :

* Configuration des secrets
* Optimisations de performance
* Monitoring et logs
* Backup et restauration
