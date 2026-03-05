================
Vue d'Ensemble
================

Architecture générale du projet microservices.

Vue d'Ensemble
==============

Le projet implémente une **architecture microservices** avec trois composants principaux :

* **Frontend** : Interface utilisateur Streamlit
* **Backend** : API REST FastAPI
* **Base de données** : PostgreSQL avec persistance

Diagramme d'Architecture
=========================

.. code-block:: text

   ┌─────────────────┐
   │  Utilisateur    │
   └────────┬────────┘
            │ Port 8501
            ▼
   ┌─────────────────┐
   │   Streamlit     │◄──── Réseau front-api
   │   (Frontend)    │
   └────────┬────────┘
            │ HTTP
            ▼
   ┌─────────────────┐
   │    FastAPI      │◄──── Réseau api-db
   │   (Backend)     │
   └────────┬────────┘
            │ SQL
            ▼
   ┌─────────────────┐
   │   PostgreSQL    │
   │  (Database)     │◄──── Volume postgres_data
   └─────────────────┘

Flux de Données
===============

1. **Utilisateur** → Accède au frontend Streamlit (port 8501)
2. **Frontend** → Envoie des requêtes HTTP à l'API FastAPI
3. **Backend** → Effectue des opérations CRUD sur PostgreSQL
4. **Database** → Persiste les données dans un volume Docker

Isolation Réseau
================

Le projet utilise **deux réseaux Docker isolés** :

front-api
---------

* Relie le frontend Streamlit au backend FastAPI
* Permet la communication HTTP entre les services
* Isolé de la base de données

.. code-block:: yaml

   networks:
     front-api:
       driver: bridge

api-db
------

* Relie le backend FastAPI à la base de données PostgreSQL
* Permet les requêtes SQL
* Isolé du frontend (sécurité)

.. code-block:: yaml

   networks:
     api-db:
       driver: bridge

Cette isolation garantit que :

* Le frontend ne peut PAS accéder directement à la base de données
* Seule l'API peut communiquer avec PostgreSQL
* Principe de moindre privilège respecté

Gestion de la Persistance
==========================

Volume Docker
-------------

Les données PostgreSQL sont persistées dans un volume Docker nommé :

.. code-block:: yaml

   volumes:
     postgres_data:
       driver: local

Avantages :

* ✅ Données conservées après ``docker-compose down``
* ✅ Performances optimales
* ✅ Indépendant du conteneur

Pour supprimer les données :

.. code-block:: bash

   docker-compose down -v

Health Checks
=============

Chaque service implémente des health checks pour vérifier son état.

API Health Check
----------------

.. code-block:: yaml

   healthcheck:
     test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
     interval: 30s
     timeout: 10s
     retries: 3
     start_period: 40s

L'API expose un endpoint ``/health`` :

.. code-block:: python

   @app.get("/health")
   def health():
       return {"status": "healthy"}

Database Health Check
---------------------

.. code-block:: yaml

   healthcheck:
     test: ["CMD-SHELL", "pg_isready -U projet2_user"]
     interval: 10s
     timeout: 5s
     retries: 5

Dépendances entre Services
===========================

L'ordre de démarrage est géré par Docker Compose :

.. code-block:: yaml

   services:
     db:
       # Démarre en premier
     
     api:
       depends_on:
         db:
           condition: service_healthy  # Attend que DB soit saine
     
     front:
       depends_on:
         api:
           condition: service_healthy  # Attend que API soit saine

Cette configuration garantit un démarrage ordonné et fiable.

Scalabilité
===========

L'architecture permet de scaler horizontalement :

.. code-block:: bash

   # Lancer 3 instances de l'API
   docker-compose up --scale api=3

Considérations :

* Ajouter un load balancer (nginx, traefik)
* Gérer les sessions (Redis, JWT)
* Pool de connexions PostgreSQL

Sécurité
========

Bonnes Pratiques Implémentées
------------------------------

✅ Réseaux isolés (segmentation)
✅ Variables d'environnement pour secrets
✅ Health checks pour haute disponibilité
✅ Images Docker officielles et slim
✅ Principe de moindre privilège
✅ Scan de secrets avec Gitleaks

Améliorations Possibles
------------------------

* HTTPS avec certificats TLS
* Authentification avec JWT
* Rate limiting
* WAF (Web Application Firewall)
* Logging centralisé

Technologies Utilisées
======================

Backend
-------

* **FastAPI** 0.104+ : Framework web moderne, rapide
* **Uvicorn** : Serveur ASGI haute performance
* **SQLAlchemy** 2.0 : ORM Python puissant
* **Pydantic** 2.5+ : Validation de données

Frontend
--------

* **Streamlit** 1.28+ : Framework Python pour dashboards
* **Pandas** : Manipulation de données
* **Requests** : Client HTTP

Database
--------

* **PostgreSQL** 15 : Base de données relationnelle
* **psycopg2** : Driver PostgreSQL pour Python

DevOps
------

* **Docker** : Conteneurisation
* **Docker Compose** : Orchestration
* **uv** : Gestionnaire de paquets Python moderne
* **GitHub Actions** : CI/CD
* **Gitleaks** : Détection de secrets

Prochaines Sections
====================

* :doc:`backend` : Architecture détaillée du backend
* :doc:`frontend` : Architecture du frontend
* :doc:`database` : Modèle de données et schéma
