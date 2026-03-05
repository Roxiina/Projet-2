==================
Aspects Techniques
==================

Détails techniques des livrables.

Architecture
============

* **Backend** : FastAPI 0.104+ avec SQLAlchemy 2.0
* **Frontend** : Streamlit 1.28+
* **Database** : PostgreSQL 15-alpine
* **Orchestration** : Docker Compose avec réseaux isolés
* **CI/CD** : GitHub Actions (3 workflows)

Réseaux Docker
==============

* ``front-api`` : Communication Streamlit ↔ FastAPI
* ``api-db`` : Communication FastAPI ↔ PostgreSQL

Health Checks
=============

Tous les services implémentent des health checks :

* API : ``curl http://localhost:8000/health``
* Database : ``pg_isready``

Tests
=====

* **14 tests** au total
* **85% de couverture**
* Base SQLite pour les tests

Qualité du Code
===============

* Linting avec Ruff
* Configuration dans pyproject.toml
* Vérification automatique dans CI

Sécurité
========

* Gitleaks pour la détection de secrets
* Réseaux Docker isolés
* Variables d'environnement pour les secrets
* Scan automatique dans le CI
