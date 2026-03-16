===================================================
Projet 2 : Orchestration, Sécurité et Livraison Continue
===================================================

Vue d'ensemble complète du projet et de sa réalisation.

1. Objectifs du Projet
=======================

* **Orchestration** : Piloter plusieurs services (Front, API, BDD) simultanément.
* **Persistance** : Gérer les données avec PostgreSQL et les volumes Docker.
* **Sécurité** : Maîtriser les variables d'environnement et la détection de fuites de secrets.
* **Livraison (CD)** : Automatiser la création et le stockage de vos images sur DockerHub.

2. L'Architecture Cible
=========================

L'application est composée de trois services distincts :

1. **Frontend (Streamlit)** : Interface utilisateur (Page 0 : Saisie / Page 1 : Affichage).
2. **API (FastAPI)** : Le cerveau qui traite les requêtes et parle à la BDD.
3. **Database (PostgreSQL)** : Le stockage persistant des données.

.. note::
   Chaque partie a son propre ``pyproject.toml`` (API et Frontend), la base de données est lancée depuis son image docker officielle.

3. Étapes de Développement Réalisées
=====================================

Phase A : La Logique Métier (Local) ✅
---------------------------------------

* ✅ **SQLite de test** : Module SQLAlchemy fonctionnel avec base SQLite locale
* ✅ **API FastAPI** : Routes ``POST /data``, ``GET /data``, ``DELETE /data/{id}``
* ✅ **Logique métier** : Code séparé dans des dossiers (maths, connexion, crud, data)
* ✅ **Frontend Streamlit** : Deux pages fonctionnelles (insertion et lecture)
* ✅ **Tests** : 45 tests pytest avec 88% de couverture

Configuration pytest
~~~~~~~~~~~~~~~~~~~~

Fichier ``app_api/pyproject.toml`` :

.. code-block:: toml

   [tool.pytest.ini_options]
   # On force pytest à considérer le dossier app_api comme une source
   pythonpath = ["."] 
   testpaths = ["tests"]

Lancement des tests :

.. code-block:: bash

   uv run --directory ./app_api pytest ../tests/

Phase B : Variables d'Environnement et Hygiène ✅
--------------------------------------------------

* ✅ **Extraction** : URLs, logins et mots de passe externalisés
* ✅ **Gestion des fichiers** :

  * ``.env`` : Contient les secrets (exclu par ``.gitignore``)
  * ``.env.example`` : Template pour les variables nécessaires
  * ``.dockerignore`` : Empêche l'envoi de ``.env``, ``.venv`` et ``__pycache__``

Phase C : Orchestration Docker Compose ✅
------------------------------------------

* ✅ **Réseaux (Networks)** :

  * ``front-api`` : Pour la communication Streamlit ↔ FastAPI
  * ``api-db`` : Pour la communication FastAPI ↔ PostgreSQL (la BDD est invisible pour le Front)

* ✅ **Volumes** : Configuration pour que les données PostgreSQL persistent au redémarrage
* ✅ **Multi-stage builds** : Optimisation des images Docker avec étapes builder et runtime

4. Automatisation et Distribution
==================================

CI Améliorée (Gitleaks) ✅
---------------------------

Workflow ``.github/workflows/ci.yml`` avec :

* ✅ Tests automatiques avec pytest
* ✅ Linting avec Ruff
* ✅ Couverture de code (≥80%)
* ✅ Upload vers Codecov

Workflow ``.github/workflows/security.yml`` avec :

* ✅ Scan **Gitleaks** pour vérifier qu'aucun secret n'est présent
* ✅ Configuration ``.gitleaks.toml`` pour allowlist des exemples de documentation

Livraison Continue (CD) ✅
---------------------------

Workflow ``.github/workflows/cd.yml`` :

* **Déclenchement** : Uniquement si la CI est "Verte" sur la branche ``main``
* **Action** : Connexion à DockerHub via les **GitHub Secrets**
* **Versioning** : Build et push avec deux tags :

  * ``latest`` : Dernière version stable
  * ``${{ github.sha }}`` : Tag spécifique au commit

.. code-block:: yaml

   steps:
   - name: Build and Push
       uses: docker/build-push-action@v5
       with:
         context: ./app_api
         push: true
         tags: |
           ${{ secrets.DOCKERHUB_USERNAME }}/projet-2-api:latest
           ${{ secrets.DOCKERHUB_USERNAME }}/projet-2-api:${{ github.sha }}

Condition de déclenchement :

.. code-block:: yaml

   on:
     workflow_run:
       workflows: ["CI Standardisation Projet 2"]
       types:
         - completed
       branches:
         - main

Orchestration Finale ✅
-----------------------

Fichier **``docker-compose.prod.yml``** qui charge les versions ``latest`` des images depuis DockerHub.

5. Structure Finale du Dépôt
==============================

.. code-block:: plaintext

   .
   ├── .github/
   │   ├── workflows/
   │   │   ├── ci.yml          # Linting, Tests, Coverage
   │   │   ├── security.yml    # Scan Gitleaks
   │   │   ├── cd.yml          # Build & Push DockerHub
   │   │   └── docs.yml        # Déploiement GitHub Pages
   ├── app_front/              # Service Streamlit
   │   ├── main.py
   │   ├── pages/
   │   │   ├── 0_insert.py
   │   │   └── 1_read.py
   │   ├── pyproject.toml
   │   ├── uv.lock
   │   └── Dockerfile
   ├── app_api/                # Service FastAPI
   │   ├── Dockerfile
   │   ├── pyproject.toml
   │   ├── uv.lock
   │   ├── models/             # Modèles Pydantic
   │   │   ├── __init__.py
   │   │   └── models.py
   │   ├── modules/            # Logique métier
   │   │   ├── __init__.py
   │   │   ├── connect.py
   │   │   └── crud.py
   │   ├── maths/              # Fonctions mathématiques
   │   │   ├── __init__.py
   │   │   └── mon_module.py
   │   ├── data/
   │   │   └── moncsv.csv
   │   └── main.py
   ├── tests/
   │   ├── test_api.py
   │   ├── test_delete.py
   │   ├── test_coverage.py
   │   └── test_math_csv.py
   ├── docs/                   # Documentation Sphinx
   ├── docker-compose.yml      # Pour le développement (build: .)
   ├── docker-compose.prod.yml # Pour la prod (image: user/repo:tag)
   ├── conftest.py
   ├── .gitignore
   ├── .dockerignore
   ├── .gitleaks.toml
   ├── codecov.yml
   └── .env.example

6. Badges de Statut Implémentés
=================================

Le projet dispose de **5 badges de statut** :

Badges GitHub Actions
----------------------

1. **CI (Continuous Integration)**

   * Workflow : ``.github/workflows/ci.yml``
   * Vérifie : Tests pytest, linting Ruff, couverture de code
   * Déclenchement : Push sur ``main`` et ``develop``

2. **Security (Gitleaks)**

   * Workflow : ``.github/workflows/security.yml``
   * Vérifie : Détection de secrets dans le code
   * Déclenchement : Push et pull requests

3. **CD (Continuous Deployment)**

   * Workflow : ``.github/workflows/cd.yml``
   * Action : Build et push des images Docker sur DockerHub
   * Déclenchement : Après succès de la CI sur ``main``

4. **Documentation**

   * Workflow : ``.github/workflows/docs.yml``
   * Action : Déploiement Sphinx sur GitHub Pages
   * Déclenchement : Push sur ``main``

5. **Code Coverage (Codecov)**

   * Intégration : Codecov via ci.yml
   * Affiche : Pourcentage de couverture de code (actuellement **88%**)
   * Seuil requis : ≥ 80%

Résultats Actuels
-----------------

* ✅ **45/45 tests** passent avec succès
* ✅ **88% de couverture** (dépasse l'objectif de 80%)
* ✅ **Sécurité** : Aucun secret détecté par Gitleaks
* ✅ **Docker** : Images publiées sur DockerHub
* ✅ **Documentation** : Déployée sur GitHub Pages

7. Livrables Attendus
======================

Livrable 1 : Dépôt GitHub avec Badges ✅
-----------------------------------------

* ✅ Repository GitHub public
* ✅ README avec badges (CI, Security, CD, Documentation, Codecov)
* ✅ Tous les badges au vert
* ✅ Workflows GitHub Actions fonctionnels

**URL** : https://github.com/Roxiina/Projet-2

Livrable 2 : docker-compose.prod.yml ✅
----------------------------------------

* ✅ Fichier ``docker-compose.prod.yml`` fonctionnel
* ✅ Lance l'application complète en téléchargeant uniquement les images depuis DockerHub
* ✅ Tags ``latest`` et commit SHA disponibles

**Emplacement** : ``docker-compose.prod.yml``

Livrable 3 : Gitleaks Actif ✅
-------------------------------

* ✅ Workflow de sécurité actif
* ✅ Scan Gitleaks intégré dans la pipeline
* ✅ Configuration ``.gitleaks.toml`` avec allowlist
* ✅ Aucun secret exposé dans l'historique Git

**Emplacement** : ``.github/workflows/security.yml``
