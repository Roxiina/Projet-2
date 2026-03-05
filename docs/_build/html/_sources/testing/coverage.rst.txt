===========
Couverture
===========

Analyse de la couverture des tests.

Vue d'Ensemble
==============

La couverture actuelle du projet est de **85%**.

.. code-block:: text

   Coverage: 85% (248 statements, 36 missed)

Rapport Détaillé
================

Par Fichier
-----------

.. list-table::
   :header-rows: 1
   :widths: 30 15 15 15 25

   * - Fichier
     - Statements
     - Miss
     - Cover
     - Commentaires
   * - main.py
     - 45
     - 4
     - 91%
     - Excellente couverture
   * - models/models.py
     - 12
     - 0
     - 100%
     - ✅ Couverture complète
   * - modules/connect.py
     - 15
     - 0
     - 100%
     - ✅ Couverture complète
   * - modules/crud.py
     - 28
     - 5
     - 82%
     - Bonnes pratiques
   * - maths/mon_module.py
     - 6
     - 0
     - 100%
     - ✅ Couverture complète
   * - **TOTAL**
     - **248**
     - **36**
     - **85%**
     - Excellent

Génération des Rapports
========================

Terminal
--------

.. code-block:: bash

   uv run --directory ./app_api pytest ../tests/ --cov=app_api --cov-report=term

Sortie :

.. code-block:: text

   ============================= test session starts =============================
   collected 14 items
   
   tests/test_api.py::test_read_root PASSED                              [  7%]
   tests/test_api.py::test_health_check PASSED                           [ 14%]
   ...
   tests/test_math_csv.py::test_mathematical_operations PASSED           [100%]
   
   ----------- coverage: platform win32, python 3.11.14-final-0 -----------
   Name                        Stmts   Miss  Cover
   -----------------------------------------------
   main.py                       45      4    91%
   models/models.py              12      0   100%
   ...
   TOTAL                        248     36    85%
   ======================= 14 passed, 5 warnings in 0.82s =======================

HTML
----

.. code-block:: bash

   uv run --directory ./app_api pytest ../tests/ --cov=app_api --cov-report=html

Ouvrir le rapport :

.. code-block:: bash

   # Windows
   start htmlcov/index.html
   
   # macOS
   open htmlcov/index.html
   
   # Linux
   xdg-open htmlcov/index.html

Le rapport HTML montre :

* Couverture par fichier
* Lignes couvertes en vert
* Lignes manquées en rouge
* Navigation interactive

XML (pour CI/CD)
----------------

.. code-block:: bash

   uv run --directory ./app_api pytest ../tests/ --cov=app_api --cov-report=xml

Le fichier ``coverage.xml`` est utilisé par :

* Codecov
* Coveralls
* SonarQube

Configuration
=============

pyproject.toml
--------------

.. code-block:: toml

   [tool.pytest.ini_options]
   pythonpath = ["."]
   addopts = "-v --cov=. --cov-report=html --cov-report=term"

Fichier .coveragerc
-------------------

Créer ``.coveragerc`` pour configurer la couverture :

.. code-block:: ini

   [run]
   source = app_api
   omit =
       */tests/*
       */migrations/*
       */__pycache__/*
       */venv/*
       */.venv/*
   
   [report]
   precision = 2
   exclude_lines =
       pragma: no cover
       def __repr__
       raise AssertionError
       raise NotImplementedError
       if __name__ == .__main__.:
       if TYPE_CHECKING:
   
   [html]
   directory = htmlcov

Améliorer la Couverture
========================

Identifier les Lignes Manquées
-------------------------------

.. code-block:: bash

   uv run --directory ./app_api pytest ../tests/ --cov=app_api --cov-report=term-missing

Sortie avec numéros de lignes :

.. code-block:: text

   Name                Stmts   Miss  Cover   Missing
   -------------------------------------------------
   main.py               45      4    91%   12-15, 87
   modules/crud.py       28      5    82%   45, 67-71

Ajouter des Tests
-----------------

Pour couvrir les lignes manquées :

1. Identifier les branches/cas non testés
2. Créer des tests ciblés
3. Vérifier la couverture augmentée

Exemple :

.. code-block:: python

   # Si la ligne 87 de main.py n'est pas couverte
   # Créer un test qui déclenche cette ligne
   
   def test_edge_case(client):
       response = client.post("/data", json={"name": "", "value": 0})
       # ...

Bonnes Pratiques
================

Objectifs de Couverture
------------------------

* **> 80%** : Bon niveau de couverture
* **> 90%** : Excellente couverture
* **100%** : Peut être irréaliste (gestion d'erreurs, etc.)

⚠️ **Attention** : Une couverture de 100% ne garantit PAS l'absence de bugs !

Tests de Qualité
----------------

Préférez :

* ✅ Moins de tests, mais de qualité
* ✅ Tests couvrant les cas limites
* ✅ Tests testant le comportement, pas l'implémentation

Évitez :

* ❌ Tests juste pour la couverture
* ❌ Tests fragiles (cassent au moindre changement)
* ❌ Tests redondants

CI/CD Integration
=================

GitHub Actions
--------------

.. code-block:: yaml

   - name: Tests avec Couverture
     run: |
       uv run --directory ./app_api pytest ../tests/ --cov=app_api --cov-report=xml
   
   - name: Upload Couverture vers Codecov
     uses: codecov/codecov-action@v3
     with:
       file: ./coverage.xml
       flags: unittests
       name: codecov-umbrella

Badge de Couverture
-------------------

Ajouter au README :

.. code-block:: markdown

   [![Coverage](https://codecov.io/gh/Roxiina/Projet-2/branch/main/graph/badge.svg)](https://codecov.io/gh/Roxiina/Projet-2)

Codecov
-------

1. Se connecter sur https://codecov.io avec GitHub
2. Activer le repository ``Roxiina/Projet-2``
3. Le workflow CI enverra automatiquement les rapports

Métriques de Qualité
====================

En Plus de la Couverture
-------------------------

* **Complexité cyclomatique** : < 10 par fonction
* **Duplication de code** : < 5%
* **Taux de réussite des tests** : 100%
* **Temps d'exécution des tests** : < 5 minutes

Outils Complémentaires
-----------------------

* **SonarQube** : Analyse de la qualité du code
* **Bandit** : Détection de vulnérabilités Python
* **Safety** : Scan des dépendances vulnérables

Prochaines Sections
===================

* :doc:`linting` : Qualité du code avec Ruff
* :doc:`../deployment/cicd` : Intégration CI/CD complète
