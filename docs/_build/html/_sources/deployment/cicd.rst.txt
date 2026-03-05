=========
CI/CD
=========

Pipeline d'intégration et de livraison continues avec GitHub Actions.

Vue d'Ensemble
==============

Le projet utilise **GitHub Actions** pour :

* ✅ Tests automatiques (pytest)
* ✅ Linting (Ruff)
* 🔒 Scan de sécurité (Gitleaks)
* 🚀 Déploiement DockerHub

Workflows
=========

Le projet implémente 3 workflows :

1. **ci.yml** : Tests et linting
2. **security.yml** : Scan de sécurité
3. **cd.yml** : Déploiement DockerHub

Workflow CI
===========

Fichier: ``.github/workflows/ci.yml``

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
         run: curl -LsSf https://astral.sh/uv/install.sh | sh
       
       - name: Tests avec Pytest
         run: uv run --directory ./app_api pytest ../tests/ -v

Workflow Security
=================

Fichier: ``.github/workflows/security.yml``

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
