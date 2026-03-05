=================
Démarrage Rapide
=================

Ce guide vous permet de lancer rapidement l'application en quelques minutes.

Prérequis
=========

* Docker Desktop installé et démarré
* Git
* Python 3.11+ (pour le développement)
* uv (gestionnaire de paquets Python)

Installation de uv
==================

Windows (PowerShell)
--------------------

.. code-block:: powershell

   irm https://astral.sh/uv/install.ps1 | iex

Linux/macOS
-----------

.. code-block:: bash

   curl -LsSf https://astral.sh/uv/install.sh | sh

Étape 1 : Cloner le projet
===========================

.. code-block:: bash

   git clone https://github.com/Roxiina/Projet-2.git
   cd Projet-2

Étape 2 : Configuration
========================

Créer le fichier d'environnement :

.. code-block:: bash

   cp .env.example .env

Le fichier ``.env`` contient :

.. code-block:: bash

   # PostgreSQL
   POSTGRES_DB=projet2_db
   POSTGRES_USER=projet2_user
   POSTGRES_PASSWORD=projet2_password
   
   # API
   DATABASE_URL=postgresql://projet2_user:projet2_password@db:5432/projet2_db
   API_URL=http://api:8000

Étape 3 : Lancer l'application
===============================

Mode Développement
------------------

.. code-block:: bash

   docker-compose up --build

Mode Production
---------------

.. code-block:: bash

   docker-compose -f docker-compose.prod.yml up -d

Étape 4 : Accéder aux services
===============================

Une fois tous les conteneurs démarrés (statut ``healthy``) :

* **Frontend Streamlit** : http://localhost:8501
* **API FastAPI** : http://localhost:8000
* **Documentation API** : http://localhost:8000/docs

Vérification
============

Vérifier que tous les services sont en cours d'exécution :

.. code-block:: bash

   docker-compose ps

Tous les conteneurs doivent avoir le statut ``healthy``.

Tester l'API
------------

.. code-block:: bash

   curl http://localhost:8000/health

Réponse attendue :

.. code-block:: json

   {"status": "healthy"}

Tests
=====

Lancer les tests unitaires :

.. code-block:: bash

   uv run --directory ./app_api pytest ../tests/ -v

Résultat attendu : **14 tests passed** ✅

Arrêt de l'application
=======================

.. code-block:: bash

   docker-compose down

Pour supprimer aussi les volumes (données) :

.. code-block:: bash

   docker-compose down -v

Prochaines étapes
=================

* Consultez la :doc:`installation` pour une installation détaillée
* Lisez le guide :doc:`architecture/overview` pour comprendre l'architecture
* Explorez les :doc:`testing/tests` pour les tests et la qualité du code
