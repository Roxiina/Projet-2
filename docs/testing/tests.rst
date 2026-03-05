=====
Tests
=====

Guide complet des tests unitaires et d'intégration.

Vue d'Ensemble
==============

Le projet utilise **pytest** pour les tests avec :

* **14 tests** au total
* **85% de couverture** de code
* Tests API et tests unitaires
* Base de données SQLite pour les tests

Structure des Tests
===================

.. code-block:: text

   tests/
   ├── test_api.py          # 9 tests d'intégration API
   └── test_math_csv.py     # 5 tests unitaires fonctions math

Le fichier ``conftest.py`` à la racine configure le PYTHONPATH pour les imports.

Lancer les Tests
================

Commande de Base
----------------

.. code-block:: bash

   uv run --directory ./app_api pytest ../tests/ -v

Options Utiles
--------------

.. code-block:: bash

   # Tests avec sortie verbose
   uv run --directory ./app_api pytest ../tests/ -v
   
   # Tests avec couverture
   uv run --directory ./app_api pytest ../tests/ --cov=app_api
   
   # Tests d'un seul fichier
   uv run --directory ./app_api pytest ../tests/test_api.py -v
   
   # Tests d'une seule fonction
   uv run --directory ./app_api pytest ../tests/test_api.py::test_read_root -v
   
   # Arrêter au premier échec
   uv run --directory ./app_api pytest ../tests/ -x
   
   # Mode watch (relancer automatiquement)
   uv run --directory ./app_api pytest-watch ../tests/

Tests de l'API
==============

Fichier: tests/test_api.py
---------------------------

Ce fichier contient **9 tests d'intégration** de l'API FastAPI.

Configuration
~~~~~~~~~~~~~

.. code-block:: python

   import pytest
   from fastapi.testclient import TestClient
   from sqlalchemy import create_engine
   from sqlalchemy.orm import sessionmaker
   
   from main import app, get_db
   from modules.connect import Base
   
   # Base SQLite pour les tests
   DATABASE_URL = "sqlite:///./test_db.sqlite"
   
   engine = create_engine(
       DATABASE_URL,
       connect_args={"check_same_thread": False}
   )
   
   TestSessionLocal = sessionmaker(bind=engine)
   
   @pytest.fixture
   def setup_database():
       """Crée et nettoie la base de test."""
       Base.metadata.create_all(bind=engine)
       yield
       Base.metadata.drop_all(bind=engine)
   
   @pytest.fixture
   def client(setup_database):
       """Client de test FastAPI."""
       def override_get_db():
           db = TestSessionLocal()
           try:
               yield db
           finally:
               db.close()
       
       app.dependency_overrides[get_db] = override_get_db
       
       with TestClient(app) as test_client:
           yield test_client
       
       app.dependency_overrides.clear()

Tests Implémentés
~~~~~~~~~~~~~~~~~

**1. Test Route Racine**

.. code-block:: python

   def test_read_root(client):
       response = client.get("/")
       assert response.status_code == 200
       assert "message" in response.json()

**2. Test Health Check**

.. code-block:: python

   def test_health_check(client):
       response = client.get("/health")
       assert response.status_code == 200
       assert response.json() == {"status": "healthy"}

**3. Test Création de Donnée**

.. code-block:: python

   def test_create_data(client):
       response = client.post(
           "/data",
           json={"name": "Test", "value": 42, "description": "Test data"}
       )
       assert response.status_code == 201
       data = response.json()
       assert data["name"] == "Test"
       assert data["value"] == 42
       assert "id" in data

**4. Test Création Sans Description**

.. code-block:: python

   def test_create_data_without_description(client):
       response = client.post(
           "/data",
           json={"name": "NoDesc", "value": 100}
       )
       assert response.status_code == 201
       data = response.json()
       assert data["description"] is None

**5. Test Récupération de Toutes les Données**

.. code-block:: python

   def test_get_all_data(client):
       # Créer des données
       client.post("/data", json={"name": "Data1", "value": 10})
       client.post("/data", json={"name": "Data2", "value": 20})
       
       # Récupérer
       response = client.get("/data")
       assert response.status_code == 200
       data = response.json()
       assert len(data) >= 2

**6. Test Récupération par ID**

.. code-block:: python

   def test_get_data_by_id(client):
       # Créer une donnée
       create_response = client.post(
           "/data",
           json={"name": "Specific", "value": 99}
       )
       data_id = create_response.json()["id"]
       
       # Récupérer par ID
       response = client.get(f"/data/{data_id}")
       assert response.status_code == 200
       data = response.json()
       assert data["id"] == data_id
       assert data["name"] == "Specific"

**7. Test Donnée Inexistante**

.. code-block:: python

   def test_get_nonexistent_data(client):
       response = client.get("/data/99999")
       assert response.status_code == 404

**8. Test Validation des Données**

.. code-block:: python

   def test_create_data_invalid(client):
       response = client.post(
           "/data",
           json={"name": "Invalid", "value": "not_a_number"}
       )
       assert response.status_code == 422  # Unprocessable Entity

**9. Test Pagination**

.. code-block:: python

   def test_pagination(client):
       # Créer plusieurs données
       for i in range(15):
           client.post("/data", json={"name": f"Data{i}", "value": i})
       
       # Test pagination
       response = client.get("/data?skip=5&limit=5")
       assert response.status_code == 200
       data = response.json()
       assert len(data) == 5

Tests des Fonctions Math
=========================

Fichier: tests/test_math_csv.py
--------------------------------

Ce fichier contient **5 tests unitaires** des fonctions mathématiques.

Tests Implémentés
~~~~~~~~~~~~~~~~~

**1. Test Addition**

.. code-block:: python

   from maths.mon_module import add
   
   def test_add():
       assert add(2, 3) == 5
       assert add(-1, 1) == 0
       assert add(0, 0) == 0

**2. Test Soustraction**

.. code-block:: python

   from maths.mon_module import sub
   
   def test_sub():
       assert sub(5, 3) == 2
       assert sub(0, 5) == -5
       assert sub(10, 10) == 0

**3. Test Carré**

.. code-block:: python

   from maths.mon_module import square
   
   def test_square():
       assert square(4) == 16
       assert square(0) == 0
       assert square(-3) == 9

**4. Test avec Nombres Flottants**

.. code-block:: python

   def test_add_with_floats():
       result = add(1.5, 2.5)
       assert result == 4.0

**5. Test Opérations Mathématiques**

.. code-block:: python

   def test_mathematical_operations():
       assert add(square(2), sub(10, 5)) == 9
       # (2² = 4) + (10 - 5 = 5) = 9

Couverture de Code
==================

Générer un Rapport de Couverture
---------------------------------

.. code-block:: bash

   # Rapport terminal
   uv run --directory ./app_api pytest ../tests/ --cov=app_api --cov-report=term
   
   # Rapport HTML
   uv run --directory ./app_api pytest ../tests/ --cov=app_api --cov-report=html
   
   # Ouvrir le rapport
   open htmlcov/index.html  # macOS/Linux
   start htmlcov/index.html # Windows

Résultats Actuels
-----------------

.. code-block:: text

   Name                        Stmts   Miss  Cover
   -----------------------------------------------
   main.py                       45      4    91%
   models/models.py              12      0   100%
   modules/connect.py            15      0   100%
   modules/crud.py               28      5    82%
   maths/mon_module.py           6       0   100%
   -----------------------------------------------
   TOTAL                        248     36    85%

Configuration pytest
====================

Fichier conftest.py
-------------------

À la racine du projet :

.. code-block:: python

   import sys
   from pathlib import Path
   
   # Ajouter app_api au PYTHONPATH
   api_path = Path(__file__).parent / "app_api"
   sys.path.insert(0, str(api_path))

Ce fichier permet aux tests de la racine d'importer les modules de ``app_api/``.

CI/CD
=====

GitHub Actions
--------------

Les tests sont exécutés automatiquement sur GitHub Actions :

.. code-block:: yaml

   - name: Tests avec Pytest
     run: |
       uv run --directory ./app_api pytest ../tests/ -v

Badges
------

Ajouter un badge de tests au README :

.. code-block:: markdown

   ![Tests](https://github.com/Roxiina/Projet-2/actions/workflows/ci.yml/badge.svg)

Bonnes Pratiques
================

1. **Tests Isolés** : Chaque test doit être indépendant
2. **Fixtures** : Utiliser des fixtures pour la configuration commune
3. **Nommage** : ``test_<fonction>_<cas>``
4. **Assertions** : Une assertion principale par test
5. **Cleanup** : Toujours nettoyer après les tests (fixtures)

Dépannage
=========

Import Errors
-------------

**Erreur** : ``ModuleNotFoundError: No module named 'main'``

**Solution** : Vérifier que ``conftest.py`` existe à la racine.

Database Errors
---------------

**Erreur** : ``no such table: data``

**Solution** : Utiliser une base SQLite fichier (``sqlite:///./test_db.sqlite``) au lieu de mémoire (``:memory:``).

Test Isolation
--------------

**Problème** : Les tests s'influencent mutuellement

**Solution** : Utiliser des fixtures pour créer/détruire la base entre chaque test.

Prochaines Sections
===================

* :doc:`coverage` : Analyse détaillée de la couverture
* :doc:`linting` : Qualité du code avec Ruff
