============================
Configuration Codecov
============================

Guide complet pour configurer Codecov et obtenir des rapports de couverture de code automatiques.

.. note::
   Le badge affiche "unknown" car le repository n'est pas encore configuré sur Codecov.
   Suivez ce guide pour l'activer en 5 minutes.

Vue d'Ensemble
==============

**Codecov** est un service qui :

* 📊 **Analyse** la couverture de code de vos tests
* 🎯 **Affiche** les statistiques de couverture avec des badges
* 📈 **Suit** l'évolution de la couverture dans le temps
* 🔍 **Identifie** les parties de code non testées

Notre Couverture Actuelle
==========================

.. code-block:: text

   =============================== tests coverage ================================
   Name                  Stmts   Miss  Cover
   -----------------------------------------
   main.py                  43      5    88%
   maths\__init__.py         2      0   100%
   maths\mon_module.py       9      2    78%
   models\__init__.py        2      0   100%
   models\models.py         13      0   100%
   modules\__init__.py       3      0   100%
   modules\connect.py       40      9    78%
   modules\crud.py          20      0   100%
   -----------------------------------------
   TOTAL                   132     16    88%

✅ **88% de couverture** (objectif : >80%)

Configuration Rapide
====================

Étape 1 : Activer Codecov
--------------------------

1. **Allez sur** : https://codecov.io
2. **Cliquez sur** "Sign up" (ou "Log in" si vous avez déjà un compte)
3. **Connectez-vous avec GitHub**
4. **Autorisez Codecov** à accéder à vos repositories

.. tip::
   Utilisez le même compte GitHub que celui du repository pour simplifier l'accès.

Étape 2 : Ajouter le Repository
--------------------------------

1. **Cliquez sur** "+ Add new repository"
2. **OU allez directement sur** : https://app.codecov.io/gh/Roxiina
3. **Recherchez** "Projet-2" dans la liste
4. **Activez** le repository en cliquant dessus

.. image:: https://img.shields.io/badge/Repository-Projet--2-blue
   :alt: Repository

Étape 3 : Copier le Token
--------------------------

1. Une fois le repository activé, **copiez le token** qui s'affiche
   
   Format : ``xxxxx-xxxx-xxxx-xxxx-xxxxxxxxx``

2. **Conservez ce token** pour l'étape suivante

.. warning::
   Ne partagez jamais votre token Codecov publiquement !
   Il sera stocké de manière sécurisée dans les secrets GitHub.

Étape 4 : Ajouter le Token aux Secrets GitHub
----------------------------------------------

1. **Allez sur GitHub** : 
   
   https://github.com/Roxiina/Projet-2/settings/secrets/actions

2. **Cliquez sur** "New repository secret"

3. **Remplissez** :
   
   * **Name** : ``CODECOV_TOKEN``
   * **Secret** : Collez le token copié à l'étape 3

4. **Cliquez sur** "Add secret"

.. code-block:: text

   Secrets / Actions
   ├── CODECOV_TOKEN : ••••••••••••••••••••
   └── (autres secrets...)

Étape 5 : Vérification
-----------------------

1. Le workflow CI se lance automatiquement après le prochain push
2. **Attendez** quelques minutes que le workflow se termine
3. Le badge devrait afficher **88%** de couverture
4. **Rechargez** la page du README : https://github.com/Roxiina/Projet-2

Configuration du Workflow CI
=============================

Notre workflow CI inclut déjà l'upload vers Codecov :

.. code-block:: yaml

   - name: Tests avec Pytest et couverture
     working-directory: ./app_api
     run: |
       uv run pytest ../tests/ -v \
         --cov=. \
         --cov-report=xml \
         --cov-report=html \
         --cov-report=term \
         --cov-fail-under=80
   
   - name: Upload de la couverture vers Codecov
     uses: codecov/codecov-action@v4
     env:
       CODECOV_TOKEN: ${{ secrets.CODECOV_TOKEN }}
     with:
       files: ./app_api/coverage.xml
       flags: unittests
       name: codecov-umbrella
       fail_ci_if_error: false
       verbose: true

Points Importants
-----------------

* 📁 **Fichier de couverture** : ``./app_api/coverage.xml``
* 🏷️ **Flags** : ``unittests`` (pour différencier types de tests)
* 🔊 **Verbose** : Activé pour debugger les problèmes
* ⚠️ **fail_ci_if_error** : Désactivé pour ne pas bloquer le CI

Vérifier l'Upload
=================

Après le prochain push :

1. **Allez sur** : https://github.com/Roxiina/Projet-2/actions
2. **Cliquez sur** le dernier workflow "CI Standardisation Projet 2"
3. **Ouvrez** l'étape "Upload de la couverture vers Codecov"
4. **Vérifiez** qu'il n'y a pas d'erreurs

Logs Attendus
-------------

.. code-block:: text

   [info] Uploading coverage to Codecov
   [info] Processing file: ./app_api/coverage.xml
   [info] ✅ Successfully uploaded coverage report
   [info] View report at: https://codecov.io/gh/Roxiina/Projet-2

Badge de Couverture
===================

Le badge dans le README se met à jour automatiquement :

.. code-block:: markdown

   [![codecov](https://codecov.io/gh/Roxiina/Projet-2/branch/main/graph/badge.svg)](https://codecov.io/gh/Roxiina/Projet-2)

Résultat Attendu
----------------

.. image:: https://img.shields.io/badge/coverage-88%25-brightgreen
   :alt: Coverage 88%

Le badge affiche **88%** en vert (>80% requis) ✅

Alternative : Repository Public
================================

Si votre repository est **public**, Codecov peut fonctionner **sans token** (avec des limitations) :

* ✅ Upload automatique des rapports
* ✅ Badge de couverture fonctionnel
* ❌ Pas d'accès aux fonctionnalités premium
* ❌ Limites de requêtes API

Dans ce cas
-----------

**Attendez simplement** que le workflow CI se termine après un push.
Codecov détectera automatiquement le repository et créera les rapports.

.. note::
   Pour les repositories publics éducatifs, Codecov offre souvent des fonctionnalités gratuites supplémentaires.

Problèmes Fréquents
===================

Badge affiche "unknown"
-----------------------

**Solutions** :

✅ Vérifiez que le token est bien ajouté aux secrets GitHub

.. code-block:: bash

   # Vérifier dans : Settings > Secrets > Actions
   CODECOV_TOKEN: ••••••••••••••••••••

✅ Vérifiez que le workflow CI s'est terminé **sans erreur**

✅ **Attendez** 5-10 minutes pour la synchronisation

✅ **Videz le cache** du navigateur (Ctrl+F5 ou Cmd+Shift+R)

Upload Codecov échoue
---------------------

**Diagnostic** :

1. Vérifiez que ``coverage.xml`` est bien généré :

.. code-block:: bash

   cd app_api
   uv run pytest ../tests/ --cov=. --cov-report=xml
   ls -la coverage.xml  # Le fichier doit exister

2. Vérifiez les logs du workflow CI

3. Vérifiez que le token est **correct** dans les secrets

4. Essayez avec ``fail_ci_if_error: true`` pour voir l'erreur complète

Erreur "File not found"
-----------------------

**Cause** : Le chemin vers ``coverage.xml`` est incorrect

**Solution** : Vérifiez le ``working-directory`` dans le workflow

.. code-block:: yaml

   # Le fichier est généré dans app_api/
   working-directory: ./app_api
   
   # Donc le chemin dans l'upload est :
   files: ./app_api/coverage.xml

Dashboard Codecov
=================

Une fois configuré, accédez au dashboard :

🔗 https://app.codecov.io/gh/Roxiina/Projet-2

Fonctionnalités
---------------

* 📊 **Graphiques** de couverture dans le temps
* 📁 **Vue par fichier** : quelle partie du code est testée
* 🔍 **Comparaison** entre branches
* 📈 **Statistiques** détaillées par commit
* 💬 **Commentaires** automatiques sur les Pull Requests

Intégration Pull Request
=========================

Codecov commente automatiquement vos PR avec :

* 📊 Différence de couverture (+/- %)
* 🎯 Fichiers impactés
* ✅ Validation du seuil de couverture

Exemple de Commentaire
-----------------------

.. code-block:: text

   ## [Codecov](https://codecov.io) Report
   > Merging #123 feature/new-endpoint will **increase** coverage by `2.5%`.
   > The diff coverage is `95.0%`.
   
   | Files | Coverage Δ | Complexity Δ |
   |-------|-----------|--------------|
   | main.py | `90.0% (+2.5%)` | - |
   
   ✅ Coverage threshold met: 88% > 80%

Ressources
==========

Documentation
-------------

* 📚 `Documentation Codecov <https://docs.codecov.com/docs>`_
* 🔧 `GitHub Actions + Codecov <https://github.com/codecov/codecov-action>`_
* 📊 `Dashboard Codecov <https://app.codecov.io/gh/Roxiina/Projet-2>`_

Support
-------

* 💬 `Support Codecov <https://codecov.io/support>`_
* 🐛 `GitHub Issues <https://github.com/codecov/codecov-action/issues>`_
* 📖 `FAQ Codecov <https://docs.codecov.com/docs/frequently-asked-questions>`_

Commandes Utiles
================

Générer un rapport local
-------------------------

.. code-block:: bash

   # Test avec couverture
   cd app_api
   uv run pytest ../tests/ --cov=. --cov-report=html
   
   # Ouvrir le rapport
   open htmlcov/index.html  # macOS/Linux
   start htmlcov/index.html # Windows

Vérifier le seuil de couverture
--------------------------------

.. code-block:: bash

   # Le CI échouera si < 80%
   uv run pytest ../tests/ --cov=. --cov-fail-under=80

Upload manuel (debug)
---------------------

.. code-block:: bash

   # Installer codecov CLI
   pip install codecov
   
   # Upload manuel
   codecov -t $CODECOV_TOKEN -f ./app_api/coverage.xml

.. tip::
   L'upload manuel est utile pour debugger les problèmes de configuration locale.
