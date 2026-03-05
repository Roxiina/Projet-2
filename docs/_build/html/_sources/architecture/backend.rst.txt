==================
Backend (FastAPI)
==================

Architecture détaillée du backend FastAPI.

Structure du Backend
====================

.. code-block:: text

   app_api/
   ├── maths/              # Modules mathématiques
   │   ├── __init__.py
   │   └── mon_module.py   # Fonctions add, sub, square
   ├── models/             # Modèles Pydantic
   │   ├── __init__.py
   │   └── models.py       # DataCreate, DataResponse
   ├── modules/            # Logique métier
   │   ├── __init__.py
   │   ├── connect.py      # Connexion DB, modèle SQLAlchemy
   │   └── crud.py         # Opérations CRUD
   ├── data/               # Données CSV
   │   └── moncsv.csv
   ├── main.py             # Point d'entrée FastAPI
   ├── Dockerfile
   └── pyproject.toml

Endpoints API
=============

Route Racine
------------

.. code-block:: python

   @app.get("/")
   def read_root():
       return {
           "message": "API Projet 2 - Gestion de données",
           "version": "1.0.0",
           "endpoints": "/docs"
       }

Health Check
------------

.. code-block:: python

   @app.get("/health")
   def health():
       return {"status": "healthy"}

Utilisé par Docker pour vérifier la santé du service.

Créer une Donnée
----------------

**POST** ``/data``

.. code-block:: python

   @app.post("/data", response_model=DataResponse, status_code=201)
   def create_data(data: DataCreate, db: Session = Depends(get_db)):
       return crud_create_data(db, data)

**Request Body** :

.. code-block:: json

   {
     "name": "Alice",
     "value": 42,
     "description": "Test data"
   }

**Response** :

.. code-block:: json

   {
     "id": 1,
     "name": "Alice",
     "value": 42,
     "description": "Test data"
   }

Récupérer des Données
---------------------

**GET** ``/data``

Paramètres query :

* ``skip`` (int, default=0) : Nombre d'éléments à sauter
* ``limit`` (int, default=100) : Nombre max d'éléments

.. code-block:: python

   @app.get("/data", response_model=List[DataResponse])
   def get_all_data(
       skip: int = 0,
       limit: int = 100,
       db: Session = Depends(get_db)
   ):
       return crud_get_all_data(db, skip, limit)

Récupérer une Donnée par ID
----------------------------

**GET** ``/data/{data_id}``

.. code-block:: python

   @app.get("/data/{data_id}", response_model=DataResponse)
   def get_data_by_id(data_id: int, db: Session = Depends(get_db)):
       data = crud_get_data_by_id(db, data_id)
       if not data:
           raise HTTPException(status_code=404, detail="Data not found")
       return data

Modèles de Données
==================

Pydantic Models (Validation)
-----------------------------

.. code-block:: python

   from pydantic import BaseModel
   
   class DataCreate(BaseModel):
       name: str
       value: int
       description: str | None = None
   
       class Config:
           from_attributes = True
   
   class DataResponse(BaseModel):
       id: int
       name: str
       value: int
       description: str | None
   
       class Config:
           from_attributes = True

SQLAlchemy Models (Base de données)
------------------------------------

.. code-block:: python

   from sqlalchemy import Column, Integer, String
   from sqlalchemy.ext.declarative import declarative_base
   
   Base = declarative_base()
   
   class DataModel(Base):
       __tablename__ = "data"
   
       id = Column(Integer, primary_key=True, index=True)
       name = Column(String, index=True)
       value = Column(Integer)
       description = Column(String, nullable=True)

Opérations CRUD
===============

Le module ``crud.py`` implémente les opérations :

Create
------

.. code-block:: python

   def create_data(db: Session, data: DataCreate) -> DataModel:
       db_data = DataModel(**data.dict())
       db.add(db_data)
       db.commit()
       db.refresh(db_data)
       return db_data

Read
----

.. code-block:: python

   def get_all_data(db: Session, skip: int = 0, limit: int = 100):
       return db.query(DataModel).offset(skip).limit(limit).all()
   
   def get_data_by_id(db: Session, data_id: int):
       return db.query(DataModel).filter(DataModel.id == data_id).first()

Gestion de la Base de Données
==============================

Connexion
---------

.. code-block:: python

   from sqlalchemy import create_engine
   from sqlalchemy.orm import sessionmaker
   import os
   
   DATABASE_URL = os.getenv(
       "DATABASE_URL",
       "postgresql://projet2_user:projet2_password@db:5432/projet2_db"
   )
   
   engine = create_engine(DATABASE_URL)
   SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Dependency Injection
--------------------

.. code-block:: python

   def get_db():
       db = SessionLocal()
       try:
           yield db
       finally:
           db.close()

Initialisation
--------------

.. code-block:: python

   @app.on_event("startup")
   def startup_event():
       Base.metadata.create_all(bind=engine)

Les tables sont créées automatiquement au démarrage.

Modules Mathématiques
=====================

Le module ``maths/mon_module.py`` fournit des fonctions utilitaires :

.. code-block:: python

   def add(a: float, b: float) -> float:
       """Addition de deux nombres."""
       return a + b
   
   def sub(a: float, b: float) -> float:
       """Soustraction de deux nombres."""
       return a - b
   
   def square(x: float) -> float:
       """Carré d'un nombre."""
       return x * x

Ces fonctions sont testées dans ``tests/test_math_csv.py``.

Gestion des Erreurs
===================

Validation Pydantic
-------------------

FastAPI valide automatiquement les données avec Pydantic :

.. code-block:: python

   # Si un champ "value" n'est pas un int
   # Retourne automatiquement 422 Unprocessable Entity

Exceptions HTTP
---------------

.. code-block:: python

   from fastapi import HTTPException
   
   @app.get("/data/{data_id}")
   def get_data(data_id: int, db: Session = Depends(get_db)):
       data = crud_get_data_by_id(db, data_id)
       if not data:
           raise HTTPException(
               status_code=404,
               detail="Data not found"
           )
       return data

Configuration
=============

Variables d'Environnement
--------------------------

* ``DATABASE_URL`` : URL de connexion PostgreSQL
* ``API_PORT`` : Port d'écoute (défaut : 8000)

Voir :doc:`../configuration` pour plus de détails.

CORS
----

Si nécessaire, activer CORS pour les appels cross-origin :

.. code-block:: python

   from fastapi.middleware.cors import CORSMiddleware
   
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["http://localhost:8501"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )

Documentation Auto-générée
===========================

FastAPI génère automatiquement la documentation :

* **Swagger UI** : http://localhost:8000/docs
* **ReDoc** : http://localhost:8000/redoc
* **OpenAPI JSON** : http://localhost:8000/openapi.json

Prochaines Sections
===================

* :doc:`frontend` : Architecture du frontend Streamlit
* :doc:`database` : Schéma de base de données détaillé
