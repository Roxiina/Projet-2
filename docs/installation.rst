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

Configuration CI/CD
-------------------

Si vous avez forké le projet, configurez les workflows GitHub Actions :

1. **Codecov** : Suivez le guide :doc:`deployment/codecov` pour activer les rapports de couverture
2. **Secrets** : Consultez :doc:`deployment/secrets` pour configurer les secrets GitHub
3. **DockerHub** : Voir :doc:`deployment/production` pour le déploiement

Documentation Locale
--------------------

Consulter et modifier la documentation :

.. code-block:: bash

   cd docs
   
   # Générer la documentation HTML
   make html
   
   # Ouvrir dans le navigateur
   open _build/html/index.html  # macOS/Linux
   start _build/html/index.html # Windows

Scripts PowerShell (Windows)
----------------------------

Le projet inclut des scripts pratiques dans ``scripts/`` :

.. code-block:: powershell

   # Démarrer tous les services
   .\scripts\start.ps1
   
   # Arrêter tous les services
   .\scripts\stop.ps1
   
   # Lancer les tests
   .\scripts\test.ps1
   
   # Voir les logs
   .\scripts\logs.ps1
   
   # Voir la documentation
   .\scripts\view-docs.ps1

Guides Détaillés
----------------

* :doc:`quickstart` pour un démarrage rapide (2 min)
* :doc:`architecture/overview` pour comprendre l'architecture
* :doc:`configuration` pour configurer votre environnement
* :doc:`testing/tests` pour lancer les tests
* :doc:`guides/contributing` pour contribuer au projet
* :doc:`guides/troubleshooting` pour résoudre les problèmes courants

Installation Complète des Outils de Développement
==================================================

VS Code Extensions
------------------

Extensions recommandées (voir ``.vscode/extensions.json``) :

* **Python** (ms-python.python) : Support Python
* **Pylance** (ms-python.vscode-pylance) : Autocomplétion intelligente  
* **Ruff** (charliermarsh.ruff) : Linting rapide
* **Docker** (ms-azuretools.vscode-docker) : Gestion Docker
* **GitLens** (eamodio.gitlens) : Git avancé
* **Thunder Client** (rangav.vscode-thunder-client) : Test d'API

Installation automatique :

.. code-block:: bash

   # Ouvre VS Code et installe les extensions recommandées
   code .

Configuration Git
-----------------

.. code-block:: bash

   # Configurer votre identité
   git config --global user.name "Votre Nom"
   git config --global user.email "votre.email@exemple.com"
   
   # Activer les couleurs
   git config --global color.ui true
   
   # Configurer l'éditeur par défaut
   git config --global core.editor "code --wait"

Pre-commit Hooks (Optionnel)
-----------------------------

Pour vérifier le code avant chaque commit :

.. code-block:: bash

   # Installer pre-commit
   pip install pre-commit
   
   # Installer les hooks
   pre-commit install
   
   # Tester sur tous les fichiers
   pre-commit run --all-files

Configuration PostgreSQL Locale (Sans Docker)
==============================================

Si vous souhaitez utiliser PostgreSQL localement sans Docker :

Windows
-------

1. **Télécharger** PostgreSQL depuis https://www.postgresql.org/download/windows/
2. **Installer** avec les paramètres par défaut
3. **Créer** la base de données :

.. code-block:: sql

   CREATE DATABASE projet2_db;
   CREATE USER projet2_user WITH PASSWORD 'projet2_password';
   GRANT ALL PRIVILEGES ON DATABASE projet2_db TO projet2_user;

4. **Configurer** l'URL dans ``.env`` :

.. code-block:: bash

   DATABASE_URL=postgresql://projet2_user:projet2_password@localhost:5432/projet2_db

macOS
-----

.. code-block:: bash

   # Avec Homebrew
   brew install postgresql@15
   brew services start postgresql@15
   
   # Créer la base
   createdb projet2_db
   psql projet2_db
   # Dans psql :
   CREATE USER projet2_user WITH PASSWORD 'projet2_password';
   GRANT ALL PRIVILEGES ON DATABASE projet2_db TO projet2_user;

Linux
-----

.. code-block:: bash

   # Ubuntu/Debian
   sudo apt update
   sudo apt install postgresql postgresql-contrib
   sudo systemctl start postgresql
   
   # Créer la base et l'utilisateur
   sudo -u postgres psql
   # Dans psql :
   CREATE DATABASE projet2_db;
   CREATE USER projet2_user WITH PASSWORD 'projet2_password';
   GRANT ALL PRIVILEGES ON DATABASE projet2_db TO projet2_user;

Vérification de l'Installation Complète
========================================

Tests Unitaires
---------------

.. code-block:: bash

   cd app_api
   uv run pytest ../tests/ -v
   
   # Avec couverture
   uv run pytest ../tests/ --cov=. --cov-report=term

Le résultat attendu est **45 tests passés** avec **88% de couverture**.

Linting
-------

.. code-block:: bash

   cd app_api
   uv run ruff check .
   
   # Avec correction automatique
   uv run ruff check . --fix

Build Docker
------------

.. code-block:: bash

   # Build des images
   docker-compose build
   
   # Vérifier que les images sont créées
   docker images | grep projet-2

Santé des Services
------------------

.. code-block:: bash

   # Démarrer les services
   docker-compose up -d
   
   # Attendre 30 secondes
   sleep 30
   
   # Vérifier la santé
   docker-compose ps
   
   # Les services doivent afficher "healthy"

Tests d'Intégration
-------------------

.. code-block:: bash

   # API Health Check
   curl http://localhost:8000/health
   # Output: {"status":"healthy"}
   
   # API Root
   curl http://localhost:8000/
   # Output: Message de bienvenue
   
   # Créer une donnée
   curl -X POST http://localhost:8000/data \
     -H "Content-Type: application/json" \
     -d '{"value": 42.5, "description": "Test"}'
   
   # Récupérer les données
   curl http://localhost:8000/data

Frontend
--------

1. Ouvrir http://localhost:8501
2. Vérifier que l'interface Streamlit s'affiche
3. Tester les pages "Insert" et "Read"

Documentation
-------------

.. code-block:: bash

   cd docs
   make html
   
   # Vérifier qu'aucune erreur ne s'affiche
   # Ouvrir _build/html/index.html

Checklist d'Installation
=========================

Avant de Commencer le Développement
------------------------------------

☑️ Docker Desktop installé et démarré

☑️ Python 3.11+ installé

☑️ uv installé et dans le PATH

☑️ Git configuré avec votre identité

☑️ Projet cloné depuis GitHub

☑️ Dépendances installées (``uv sync --extra dev``)

☑️ Fichier ``.env`` créé et configuré

☑️ Services Docker démarrent sans erreur (``docker-compose up``)

☑️ Tests passent avec succès (``pytest``)

☑️ API accessible sur http://localhost:8000

☑️ Frontend accessible sur http://localhost:8501

☑️ Documentation générée sans erreur (``make html``)

Pour Contribuer au Projet
--------------------------

☑️ Fork du repository créé

☑️ Remote "upstream" configuré

☑️ VS Code avec extensions recommandées

☑️ Pre-commit hooks installés (optionnel)

☑️ Branch de développement créée

☑️ Codecov configuré (voir :doc:`deployment/codecov`)

☑️ Tests lancés avant chaque commit

☑️ Linting passé (``ruff check``)

Résolution de Problèmes Courants
=================================

Erreurs lors de l'installation de uv
-------------------------------------

**Windows** :

.. code-block:: powershell

   # Si erreur "impossible d'exécuter des scripts"
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   
   # Puis réessayer l'installation
   irm https://astral.sh/uv/install.ps1 | iex

**Linux/macOS** :

.. code-block:: bash

   # Si erreur de permission
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Ajouter au .bashrc ou .zshrc
   echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
   source ~/.bashrc

Erreurs Docker sous Windows
----------------------------

**WSL 2 non configuré** :

.. code-block:: powershell

   # Activer WSL 2
   wsl --install
   
   # Redémarrer l'ordinateur
   # Puis configurer Docker Desktop pour utiliser WSL 2

**Virtualisation non activée** :

1. Redémarrer l'ordinateur
2. Entrer dans le BIOS (F2, F10, ou Del au démarrage)
3. Activer "Intel VT-x" ou "AMD-V"
4. Sauvegarder et redémarrer

Erreurs de Permission sous Linux
---------------------------------

.. code-block:: bash

   # Ajouter votre utilisateur au groupe docker
   sudo usermod -aG docker $USER
   
   # Déconnexion/reconnexion nécessaire
   newgrp docker
   
   # Vérifier
   docker run hello-world

Base de Données PostgreSQL ne démarre pas
------------------------------------------

.. code-block:: bash

   # Voir les logs
   docker-compose logs db
   
   # Supprimer le volume et recréer
   docker-compose down -v
   docker-compose up -d db
   
   # Attendre le démarrage
   docker-compose logs -f db

Tests échouent avec "no such table"
-----------------------------------

.. code-block:: bash

   # Supprimer les fichiers de base de données de test
   rm -f app_api/test_db.sqlite
   rm -f app_api/test_delete_db.sqlite
   
   # Relancer les tests
   cd app_api
   uv run pytest ../tests/ -v

Support et Aide
===============

En cas de problème non résolu :

* 📖 Consultez :doc:`guides/troubleshooting`
* 🐛 Ouvrez une issue sur GitHub avec :
  
  * Description du problème
  * Étapes pour reproduire
  * Logs d'erreur complets
  * Votre environnement (OS, versions)

* 💬 Contactez l'équipe de développement

Prochaines Étapes (Après Installation)
=======================================

* :doc:`quickstart` pour un démarrage rapide (2 min)
* :doc:`architecture/overview` pour comprendre l'architecture  
* :doc:`configuration` pour personnaliser vote environnement
* :doc:`testing/tests` pour comprendre les tests
* :doc:`deployment/codecov` pour configurer la couverture de code
* :doc:`guides/contributing` pour contribuer au projet
