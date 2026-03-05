=======
Linting
=======

Qualité du code avec Ruff.

Vue d'Ensemble
==============

Le projet utilise **Ruff** comme linter et formatter Python.

Ruff est :

* ⚡ **10-100x plus rapide** que Flake8/Black
* 🔧 Compatible avec tous les outils classiques
* ✅ Installé via ``uv`` (pas besoin de pip)

Installation
============

Ruff est inclus dans les dépendances de développement :

.. code-block:: toml

   [project.optional-dependencies]
   dev = [
       "ruff>=0.1.0",
       ...
   ]

Installation :

.. code-block:: bash

   cd app_api
   uv sync --extra dev

Utilisation
===========

Linting
-------

Vérifier le code sans modifier :

.. code-block:: bash

   cd app_api
   uv run ruff check .

Sortie :

.. code-block:: text

   All checks passed!

Avec erreurs :

.. code-block:: text

   main.py:15:1: F401 [*] `os` imported but unused
   main.py:42:80: E501 Line too long (95 > 100 characters)
   Found 2 errors.

Formatting
----------

Formater automatiquement le code :

.. code-block:: bash

   uv run ruff format .

Sortie :

.. code-block:: text

   2 files reformatted, 10 files left unchanged

Fix Automatique
---------------

Corriger automatiquement les erreurs simples :

.. code-block:: bash

   uv run ruff check --fix .

Mode Watch
----------

Relancer automatiquement à chaque modification :

.. code-block:: bash

   uv run ruff check --watch .

Configuration
=============

Fichier: pyproject.toml
------------------------

.. code-block:: toml

   [tool.ruff]
   line-length = 100
   target-version = "py311"
   
   [tool.ruff.lint]
   select = ["E", "F", "I", "N", "W"]
   ignore = [
       "N806",  # Variable in function should be lowercase
   ]

Options
~~~~~~~

* ``line-length`` : Longueur maximale des lignes (100 caractères)
* ``target-version`` : Version Python cible
* ``select`` : Règles à activer
* ``ignore`` : Règles à désactiver

Règles Activées
===============

Catégories
----------

.. list-table::
   :header-rows: 1
   :widths: 15 85

   * - Code
     - Description
   * - E
     - **pycodestyle errors** : Erreurs de style (PEP 8)
   * - F
     - **Pyflakes** : Erreurs logiques (imports inutilisés, variables non définies)
   * - I
     - **isort** : Tri des imports
   * - N
     - **pep8-naming** : Convention de nommage
   * - W
     - **pycodestyle warnings** : Avertissements de style

Exemples de Règles
------------------

**E501** : Ligne trop longue

.. code-block:: python

   # ❌ Mauvais (> 100 caractères)
   result = some_function(param1, param2, param3, param4, param5, param6, param7, param8, param9)
   
   # ✅ Bon
   result = some_function(
       param1, param2, param3,
       param4, param5, param6,
       param7, param8, param9
   )

**F401** : Import inutilisé

.. code-block:: python

   # ❌ Mauvais
   import os
   import sys  # Non utilisé
   
   print(os.name)
   
   # ✅ Bon
   import os
   
   print(os.name)

**F841** : Variable assignée mais jamais utilisée

.. code-block:: python

   # ❌ Mauvais
   def calculate():
       result = 42  # Non utilisé
       return 10
   
   # ✅ Bon
   def calculate():
       return 42

**I001** : Imports mal triés

.. code-block:: python

   # ❌ Mauvais
   from fastapi import FastAPI
   import os
   from sqlalchemy import Column
   
   # ✅ Bon (ordre : stdlib, tiers, local)
   import os
   
   from fastapi import FastAPI
   from sqlalchemy import Column

Règles Ignorées
===============

N806
----

**Raison** : SQLAlchemy utilise ``SessionLocal`` (PascalCase pour une variable).

.. code-block:: python

   # Sans N806 ignoré, Ruff signalerait une erreur
   SessionLocal = sessionmaker(bind=engine)

Correction des Erreurs
======================

Workflow Typique
----------------

1. **Lancer Ruff** :

   .. code-block:: bash

      uv run ruff check .

2. **Voir les erreurs** :

   .. code-block:: text

      main.py:15:1: F401 [*] `os` imported but unused
      main.py:42:80: E501 Line too long (95 > 100 characters)

3. **Corriger automatiquement** (si possible) :

   .. code-block:: bash

      uv run ruff check --fix .

4. **Corriger manuellement** les erreurs restantes

5. **Reformater** :

   .. code-block:: bash

      uv run ruff format .

6. **Vérifier** :

   .. code-block:: bash

      uv run ruff check .
      # All checks passed!

Exemples de Corrections
-----------------------

**Import inutilisé** :

.. code-block:: python

   # Avant
   import os
   import sys  # F401: unused import
   
   # Après
   import os

**Ligne trop longue** :

.. code-block:: python

   # Avant (E501)
   engine = create_engine("postgresql://user:password@localhost:5432/db", pool_size=10, max_overflow=20)
   
   # Après
   engine = create_engine(
       "postgresql://user:password@localhost:5432/db",
       pool_size=10,
       max_overflow=20
   )

CI/CD
=====

GitHub Actions
--------------

Vérification automatique dans le workflow :

.. code-block:: yaml

   - name: Linting avec Ruff (API)
     working-directory: ./app_api
     run: |
       uv run ruff check .

Le workflow échoue si Ruff trouve des erreurs.

Pre-commit Hook
---------------

Installer un hook pour vérifier avant chaque commit :

.. code-block:: bash

   # Créer .git/hooks/pre-commit
   #!/bin/sh
   
   cd app_api
   uv run ruff check .
   RUFF_EXIT=$?
   
   if [ $RUFF_EXIT -ne 0 ]; then
       echo "❌ Ruff check failed. Please fix errors before committing."
       exit 1
   fi
   
   # Rendre exécutable
   chmod +x .git/hooks/pre-commit

Intégration IDE
===============

VS Code
-------

Installer l'extension **Ruff** :

.. code-block:: json

   {
     "extensions.recommendations": [
       "charliermarsh.ruff"
     ],
     "python.linting.enabled": true,
     "python.linting.ruffEnabled": true,
     "editor.formatOnSave": true,
     "[python]": {
       "editor.defaultFormatter": "charliermarsh.ruff"
     }
   }

PyCharm
-------

1. Settings > Tools > External Tools
2. Ajouter Ruff :
   
   - Program: ``uv``
   - Arguments: ``run ruff check $FilePath$``
   - Working directory: ``$ProjectFileDir$``

Vim/Neovim
----------

Avec ALE :

.. code-block:: vim

   let g:ale_linters = {'python': ['ruff']}
   let g:ale_fixers = {'python': ['ruff']}

Comparaison avec Autres Outils
===============================

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 20 20

   * - Outil
     - Vitesse
     - Features
     - Maintenance
     - Recommandation
   * - **Ruff**
     - ⚡⚡⚡⚡⚡
     - Linting + Format
     - Active
     - ✅ Recommandé
   * - Black
     - ⚡⚡⚡
     - Format uniquement
     - Active
     - Remplacé par Ruff
   * - Flake8
     - ⚡⚡
     - Linting
     - Active
     - Remplacé par Ruff
   * - Pylint
     - ⚡
     - Linting détaillé
     - Active
     - Trop lent

Bonnes Pratiques
================

1. **Lancer Ruff** avant chaque commit
2. **Corriger** les erreurs immédiatement
3. **Configurer** l'IDE pour le linting en temps réel
4. **Utiliser** ``.ruff_cache/`` dans ``.gitignore``
5. **Activer** Ruff dans le CI/CD

À Éviter
--------

* ❌ Ignorer trop de règles
* ❌ Augmenter ``line-length`` > 120
* ❌ Désactiver Ruff dans le CI

Prochaines Sections
===================

* :doc:`../deployment/cicd` : CI/CD complet
* :doc:`../guides/contributing` : Guide de contribution
