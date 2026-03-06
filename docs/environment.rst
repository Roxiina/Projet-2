====================================
Environnement de Développement
====================================

Ce guide explique comment créer un environnement virtuel Python pour le développement local.

Pourquoi un environnement virtuel ?
===================================

L'environnement virtuel permet de :

* Lancer tous les tests depuis la racine du projet
* Avoir accès à tous les outils (pytest, ruff, sphinx) en une seule fois
* Développer sans basculer entre les environnements app_api et app_front
* Isoler les dépendances du projet de votre système

Installation
============

Prérequis
---------

* Python 3.11 ou supérieur installé
* uv (gestionnaire de paquets Python)

Installer uv
------------

**Windows (PowerShell)** :

.. code-block:: powershell

   irm https://astral.sh/uv/install.ps1 | iex

**Linux/macOS** :

.. code-block:: bash

   curl -LsSf https://astral.sh/uv/install.sh | sh

**Vérification** :

.. code-block:: bash

   uv --version

Créer l'environnement virtuel
==============================

Depuis la racine du projet :

.. code-block:: bash

   uv venv

Cela crée un dossier ``.venv/`` à la racine du projet.

Activer l'environnement
========================

**Windows (PowerShell)** :

.. code-block:: powershell

   .\.venv\Scripts\activate

**Linux/macOS** :

.. code-block:: bash

   source .venv/bin/activate

Une fois activé, votre prompt devrait afficher ``(.venv)`` au début de la ligne.

Installer les dépendances
==========================

.. code-block:: bash

   uv pip install -r requirements.txt

Cela installe :

* **Backend (API)** : FastAPI, SQLAlchemy, Pydantic, psycopg2
* **Frontend** : Streamlit, requests, pandas
* **Tests et Qualité** : pytest, pytest-cov, httpx, ruff
* **Documentation** : Sphinx, sphinx-rtd-theme, sphinx-autodoc-typehints

Utilisation
===========

Une fois l'environnement activé, vous pouvez utiliser tous les outils de développement :

Tests
-----

.. code-block:: bash

   # Tous les tests
   pytest tests/ -v
   
   # Tests avec couverture
   pytest tests/ --cov=app_api/maths --cov=app_api/models --cov=app_api/modules --cov=app_api/main
   
   # Rapport de couverture HTML
   pytest tests/ --cov=app_api --cov-report=html

Linting
-------

.. code-block:: bash

   # Vérifier le code API
   ruff check app_api/
   
   # Vérifier le code Frontend
   ruff check app_front/
   
   # Vérifier tout le projet
   ruff check .

Documentation
-------------

.. code-block:: bash

   cd docs
   make html        # Linux/macOS
   make.bat html    # Windows
   
   # Ouvrir la documentation générée
   start _build/html/index.html  # Windows
   open _build/html/index.html   # macOS
   xdg-open _build/html/index.html  # Linux

Alternative : Environnements par service
=========================================

Si vous préférez utiliser des environnements séparés pour chaque service :

API (Backend)
-------------

.. code-block:: bash

   cd app_api
   uv venv
   uv sync --extra dev

Frontend
--------

.. code-block:: bash

   cd app_front
   uv venv
   uv sync

Avantages :

* Isolation complète entre les services
* Dépendances minimales par service

Inconvénients :

* Doit basculer entre les environnements
* Plus complexe pour lancer les tests

Fichiers de configuration
==========================

pyproject.toml (racine)
-----------------------

Le fichier ``pyproject.toml`` à la racine définit toutes les dépendances du projet.

.. note::
   Ce fichier ne crée pas de package installable. C'est normal pour un projet d'orchestration.
   Utilisez uniquement ``requirements.txt`` pour installer les dépendances.

requirements.txt
----------------

Le fichier ``requirements.txt`` contient la liste complète des dépendances avec leurs versions.

C'est le fichier recommandé pour l'installation :

.. code-block:: bash

   uv pip install -r requirements.txt

pyproject.toml (par service)
-----------------------------

Chaque service (``app_api/`` et ``app_front/``) a son propre ``pyproject.toml`` avec ses dépendances spécifiques.

Désactivation de l'environnement
=================================

Pour désactiver l'environnement virtuel :

.. code-block:: bash

   deactivate

Bonnes Pratiques
================

.. tip::
   **Activez toujours l'environnement avant de travailler** :
   
   .. code-block:: bash
   
      # Windows
      .\.venv\Scripts\activate
      
      # Linux/macOS
      source .venv/bin/activate

.. warning::
   **N'oubliez pas d'installer les nouvelles dépendances** :
   
   Si le fichier ``requirements.txt`` est mis à jour, réinstallez les dépendances :
   
   .. code-block:: bash
   
      uv pip install -r requirements.txt

.. important::
   **Les environnements virtuels ne sont jamais commités** :
   
   * ``.venv/`` à la racine → Ignoré par ``.gitignore``
   * ``app_api/.venv`` → Ignoré par ``.gitignore``
   * ``app_front/.venv`` → Ignoré par ``.gitignore``

Résolution de problèmes
========================

L'environnement ne s'active pas
--------------------------------

**Windows** : Assurez-vous que l'exécution de scripts est autorisée :

.. code-block:: powershell

   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

**Linux/macOS** : Vérifiez les permissions :

.. code-block:: bash

   chmod +x .venv/bin/activate

Erreur "No module named..."
----------------------------

Vérifiez que l'environnement est activé (votre prompt doit afficher ``(.venv)``).

Si oui, réinstallez les dépendances :

.. code-block:: bash

   uv pip install -r requirements.txt

Conflit de versions
--------------------

Supprimez l'environnement et recréez-le :

.. code-block:: bash

   # Désactiver l'environnement
   deactivate
   
   # Supprimer l'environnement
   rm -rf .venv  # Linux/macOS
   Remove-Item -Recurse -Force .venv  # Windows
   
   # Recréer l'environnement
   uv venv
   .\.venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/macOS
   
   # Réinstaller les dépendances
   uv pip install -r requirements.txt

Voir aussi
==========

* :doc:`installation` - Installation complète du projet
* :doc:`testing/tests` - Guide des tests
* :doc:`guides/contributing` - Guide de contribution
