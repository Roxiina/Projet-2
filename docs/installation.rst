============
Installation
============

Ce guide détaille l'installation complète du projet pour le développement.

Prérequis Système
=================

Logiciels Obligatoires
----------------------

* **Docker Desktop** 4.0+
* **Git** 2.0+
* **Python** 3.11+
* **uv** (gestionnaire de paquets)

Logiciels Optionnels
--------------------

* **VS Code** avec extensions :
  
  * Python
  * Docker
  * GitLens
  * Ruff

Vérification des prérequis
---------------------------

.. code-block:: bash

   # Python
   python --version
   # Output: Python 3.11.x ou supérieur

   # Docker
   docker --version
   docker-compose --version

   # Git
   git --version

   # uv
   uv --version

Installation de uv
==================

Windows
-------

**PowerShell (Administrateur)** :

.. code-block:: powershell

   irm https://astral.sh/uv/install.ps1 | iex

**Vérification** :

.. code-block:: powershell

   uv --version

Linux/macOS
-----------

.. code-block:: bash

   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Ajouter au PATH (si nécessaire)
   export PATH="$HOME/.cargo/bin:$PATH"
   
   # Vérification
   uv --version

Clonage du Projet
=================

.. code-block:: bash

   git clone https://github.com/Roxiina/Projet-2.git
   cd Projet-2

Installation des Dépendances
=============================

Backend (API FastAPI)
---------------------

.. code-block:: bash

   cd app_api
   uv sync --extra dev
   cd ..

Cette commande installe :

* FastAPI, Uvicorn, SQLAlchemy, Psycopg2
* Pytest, Ruff (outils de développement)

Frontend (Streamlit)
--------------------

.. code-block:: bash

   cd app_front
   uv sync --extra dev
   cd ..

Documentation (Sphinx)
----------------------

.. code-block:: bash

   cd docs
   pip install -r requirements.txt
   cd ..

Configuration
=============

Variables d'Environnement
--------------------------

Créer le fichier ``.env`` :

.. code-block:: bash

   cp .env.example .env

Contenu du fichier ``.env`` :

.. code-block:: bash

   # PostgreSQL Configuration
   POSTGRES_DB=projet2_db
   POSTGRES_USER=projet2_user
   POSTGRES_PASSWORD=projet2_password
   POSTGRES_PORT=5432
   
   # API Configuration
   DATABASE_URL=postgresql://projet2_user:projet2_password@db:5432/projet2_db
   API_URL=http://api:8000
   API_PORT=8000
   
   # Frontend Configuration
   STREAMLIT_PORT=8501

Base de Données
---------------

PostgreSQL sera créée automatiquement au lancement de Docker Compose.

Build des Images Docker
========================

.. code-block:: bash

   # Build de toutes les images
   docker-compose build
   
   # Build d'un service spécifique
   docker-compose build api
   docker-compose build front

Lancement
=========

Mode Développement
------------------

.. code-block:: bash

   docker-compose up

Les logs s'affichent dans le terminal. Utilisez ``Ctrl+C`` pour arrêter.

Mode Détaché (Background)
--------------------------

.. code-block:: bash

   docker-compose up -d

Pour voir les logs :

.. code-block:: bash

   docker-compose logs -f

Vérification
============

Santé des Services
------------------

.. code-block:: bash

   docker-compose ps

Tous les services doivent afficher ``healthy``.

Test de l'API
-------------

.. code-block:: bash

   curl http://localhost:8000/health

Test du Frontend
----------------

Ouvrir http://localhost:8501 dans le navigateur.

Développement Local (Sans Docker)
==================================

API
---

.. code-block:: bash

   cd app_api
   
   # Créer une base SQLite pour le dev
   export DATABASE_URL=sqlite:///./dev.db
   
   # Lancer l'API
   uv run uvicorn main:app --reload --port 8000

Frontend
--------

.. code-block:: bash

   cd app_front
   
   # Configurer l'URL de l'API
   export API_URL=http://localhost:8000
   
   # Lancer Streamlit
   uv run streamlit run main.py

Dépannage
=========

Docker Desktop n'est pas démarré
---------------------------------

**Erreur** : ``error during connect: this error may indicate that the docker daemon is not running``

**Solution** : Démarrer Docker Desktop manuellement.

Port déjà utilisé
-----------------

**Erreur** : ``Bind for 0.0.0.0:8501 failed: port is already allocated``

**Solution** : Modifier les ports dans ``docker-compose.yml`` ou arrêter le processus utilisant le port.

.. code-block:: bash

   # Windows
   netstat -ano | findstr :8501
   
   # Linux/macOS
   lsof -i :8501

uv non trouvé
-------------

**Erreur** : ``uv: command not found``

**Solution** : Réinstaller uv et vérifier le PATH.

Prochaines Étapes
=================

* Consultez le :doc:`quickstart` pour un démarrage rapide
* Explorez l'architecture dans :doc:`architecture/overview`
* Configurez votre environnement de développement dans :doc:`configuration`
