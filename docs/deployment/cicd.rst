=========
CI/CD
=========

Pipeline d'intégration et de livraison continues avec GitHub Actions.

.. image:: https://github.com/Roxiina/Projet-2/actions/workflows/ci.yml/badge.svg
   :target: https://github.com/Roxiina/Projet-2/actions/workflows/ci.yml
   :alt: CI Status

.. image:: https://github.com/Roxiina/Projet-2/actions/workflows/security.yml/badge.svg
   :target: https://github.com/Roxiina/Projet-2/actions/workflows/security.yml
   :alt: Security Status

.. image:: https://github.com/Roxiina/Projet-2/actions/workflows/cd.yml/badge.svg
   :target: https://github.com/Roxiina/Projet-2/actions/workflows/cd.yml
   :alt: CD Status

.. image:: https://github.com/Roxiina/Projet-2/actions/workflows/docs.yml/badge.svg
   :target: https://github.com/Roxiina/Projet-2/actions/workflows/docs.yml
   :alt: Documentation Status

Vue d'Ensemble
==============

Le projet utilise **GitHub Actions** pour :

* ✅ Tests automatiques (pytest)
* ✅ Linting (Ruff)
* 📊 Couverture de code (Codecov)
* 🔒 Scan de sécurité (Gitleaks)
* 📚 Déploiement documentation (GitHub Pages)
* 🚀 Déploiement DockerHub

Workflows
=========

Le projet implémente 4 workflows :

1. **ci.yml** : Tests, linting et couverture
2. **security.yml** : Scan de sécurité
3. **cd.yml** : Déploiement DockerHub
4. **docs.yml** : Déploiement documentation

Workflow CI
===========

Fichier: ``.github/workflows/ci.yml``

Ce workflow effectue :

* 🧪 **Linting du code** avec Ruff (analyse statique : PEP 8, imports inutilisés, erreurs potentielles)
* ✅ **Tests unitaires** avec Pytest (45 tests)
* 📊 **Calcul de la couverture de code** (>80% requis)
* 📤 **Upload des rapports** vers Codecov

.. note::
   Le badge **CI** regroupe 3 vérifications :
   
   1. **Linting Ruff** : Vérifie la qualité et le style du code Python
   2. **Tests** : Exécution de tous les tests pytest
   3. **Coverage** : Vérification du pourcentage de couverture
   
   Le badge est vert ✅ uniquement si les 3 passent avec succès.

.. code-block:: yaml

   name: CI Standardisation Projet 2
   
   on:
     push:
       branches: [ main, develop ]
     pull_request:
       branches: [ main, develop ]
   
   jobs:
     lint-and-test:
       runs-on: ubuntu-latest
       steps:
       - uses: actions/checkout@v4
       - uses: actions/setup-python@v5
         with:
           python-version: '3.11'
       
       - name: Installation de uv
         run: |
           curl -LsSf https://astral.sh/uv/install.sh | sh
           echo "$HOME/.cargo/bin" >> $GITHUB_PATH
       
       - name: Installation des dépendances
         working-directory: ./app_api
         run: uv sync --extra dev
       
       - name: Linting avec Ruff
         working-directory: ./app_api
         run: uv run ruff check .
       
       - name: Tests avec Pytest et couverture
         working-directory: ./app_api
         run: |
           uv run pytest ../tests/ -v \
             --cov=. \
             --cov-report=xml \
             --cov-report=html \
             --cov-report=term \
             --cov-fail-under=80
       
       - name: Upload vers Codecov
         uses: codecov/codecov-action@v4
         with:
           files: ./app_api/coverage.xml
           flags: unittests
           fail_ci_if_error: false
           verbose: true

Points Clés
-----------

* 🎯 **Seuil de couverture** : 80% minimum requis
* 📊 **Codecov** : Upload automatique des rapports
* 🔄 **Branches** : CI s'exécute sur main et develop
* ⚡ **uv** : Gestionnaire de paquets Python moderne

Workflow Security
=================

Fichier: ``.github/workflows/security.yml``

Ce workflow effectue :

* 🔒 Détection de secrets exposés avec Gitleaks
* 📝 Rapport SARIF pour GitHub Security
* ⚠️ Alerte en cas de découverte de secrets

.. code-block:: yaml

   name: Sécurité Gitleaks
   
   on: [push, pull_request]
   
   jobs:
     gitleaks:
       runs-on: ubuntu-latest
       steps:
       - uses: actions/checkout@v4
         with:
           fetch-depth: 0
       
       - name: Gitleaks
         uses: gitleaks/gitleaks-action@v2
         env:
           GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

Configuration Gitleaks
----------------------

Le fichier ``.gitleaks.toml`` définit :

* 🎯 Les patterns à détecter (API keys, tokens, passwords)
* ✅ Les fichiers à ignorer (documentation, exemples)
* 📋 Les valeurs autorisées (credentials de test)

Workflow Documentation
======================

Fichier: ``.github/workflows/docs.yml``

Ce workflow déploie automatiquement la documentation Sphinx sur GitHub Pages.

.. code-block:: yaml

   name: Documentation
   
   on:
     push:
       branches: [ main ]
   
   permissions:
     contents: read
     pages: write
     id-token: write
   
   jobs:
     build:
       runs-on: ubuntu-latest
       steps:
       - uses: actions/checkout@v4
       
       - name: Setup Python
         uses: actions/setup-python@v5
         with:
           python-version: '3.11'
       
       - name: Install dependencies
         run: |
           cd docs
           pip install -r requirements.txt
       
       - name: Build HTML
         run: |
           cd docs
           make html
       
       - name: Upload artifact
         uses: actions/upload-pages-artifact@v3
         with:
           path: 'docs/_build/html'
     
     deploy:
       needs: build
       runs-on: ubuntu-latest
       steps:
       - name: Deploy to GitHub Pages
         uses: actions/deploy-pages@v4

La documentation est accessible sur :

📚 **https://roxiina.github.io/Projet-2/**

Workflow CD
===========

Fichier: ``.github/workflows/cd.yml``

.. code-block:: yaml

   name: CD DockerHub
   
   on:
     push:
       branches: [ main ]
   
   jobs:
     deploy:
       runs-on: ubuntu-latest
       steps:
       - uses: actions/checkout@v4
       
       - name: Login to DockerHub
         uses: docker/login-action@v3
         with:
           username: ${{ secrets.DOCKERHUB_USERNAME }}
           token: ${{ secrets.DOCKERHUB_TOKEN }}
       
       - name: Build and Push API
         uses: docker/build-push-action@v5
         with:
           context: ./app_api
           push: true
           tags: |
             roxiina/projet-2-api:latest
             roxiina/projet-2-api:${{ github.sha }}

Configuration
=============

Voir :doc:`secrets` pour configurer les secrets GitHub.

Badges
======

Ajouter au README :

.. code-block:: markdown

   ![CI](https://github.com/Roxiina/Projet-2/actions/workflows/ci.yml/badge.svg)
   ![Security](https://github.com/Roxiina/Projet-2/actions/workflows/security.yml/badge.svg)
   ![CD](https://github.com/Roxiina/Projet-2/actions/workflows/cd.yml/badge.svg)

Prochaines Sections
===================

* :doc:`production` : Déploiement production
* :doc:`secrets` : Configuration des secrets
