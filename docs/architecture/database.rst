==================
Base de Données
==================

Architecture et schéma de la base de données PostgreSQL.

Technologie
===========

Le projet utilise **PostgreSQL 15** (image Alpine) pour :

* ✅ Fiabilité et maturité
* ✅ Support SQL complet
* ✅ ACID compliance
* ✅ Excellent écosystème Python (psycopg2, SQLAlchemy)

Schéma de Données
=================

Table: data
-----------

.. code-block:: sql

   CREATE TABLE data (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       name VARCHAR NOT NULL,
       value INTEGER NOT NULL,
       description VARCHAR NULL
   );

Colonnes
~~~~~~~~

.. list-table::
   :header-rows: 1
   :widths: 20 20 20 40

   * - Colonne
     - Type
     - Contraintes
     - Description
   * - id
     - INTEGER
     - PRIMARY KEY, AUTO_INCREMENT
     - Identifiant unique
   * - name
     - VARCHAR
     - NOT NULL, INDEX
     - Nom de l'entité
   * - value
     - INTEGER
     - NOT NULL
     - Valeur numérique
   * - description
     - VARCHAR
     - NULL
     - Description optionnelle

Modèle SQLAlchemy
=================

.. code-block:: python

   from sqlalchemy import Column, Integer, String
   from sqlalchemy.ext.declarative import declarative_base
   
   Base = declarative_base()
   
   class DataModel(Base):
       """Modèle SQLAlchemy pour la table data."""
       
       __tablename__ = "data"
       
       id = Column(Integer, primary_key=True, index=True)
       name = Column(String, index=True, nullable=False)
       value = Column(Integer, nullable=False)
       description = Column(String, nullable=True)
       
       def __repr__(self):
           return f"<DataModel id={self.id} name={self.name} value={self.value}>"

Index
-----

Les index sont créés sur :

* ``id`` : Clé primaire (automatique)
* ``name`` : Index pour accélérer les recherches par nom

Connexion à la Base
====================

Configuration
-------------

.. code-block:: python

   from sqlalchemy import create_engine
   from sqlalchemy.orm import sessionmaker
   import os
   
   DATABASE_URL = os.getenv(
       "DATABASE_URL",
       "postgresql://projet2_user:projet2_password@db:5432/projet2_db"
   )
   
   engine = create_engine(
       DATABASE_URL,
       pool_size=5,
       max_overflow=10,
       pool_pre_ping=True  # Vérifier la connexion avant utilisation
   )
   
   SessionLocal = sessionmaker(
       autocommit=False,
       autoflush=False,
       bind=engine
   )

Pool de Connexions
------------------

SQLAlchemy utilise un **pool de connexions** pour optimiser les performances :

* ``pool_size=5`` : 5 connexions permanentes
* ``max_overflow=10`` : Jusqu'à 15 connexions au total
* ``pool_pre_ping=True`` : Vérification des connexions avant usage

Dependency Injection
--------------------

FastAPI utilise l'injection de dépendances pour gérer les sessions :

.. code-block:: python

   from fastapi import Depends
   from sqlalchemy.orm import Session
   
   def get_db():
       """Génère une session de base de données."""
       db = SessionLocal()
       try:
           yield db
       finally:
           db.close()
   
   # Utilisation dans un endpoint
   @app.get("/data")
   def get_data(db: Session = Depends(get_db)):
       return db.query(DataModel).all()

Initialisation
==============

Les tables sont créées automatiquement au démarrage de l'API :

.. code-block:: python

   from fastapi import FastAPI
   
   app = FastAPI()
   
   @app.on_event("startup")
   def startup_event():
       """Crée les tables au démarrage."""
       Base.metadata.create_all(bind=engine)

Opérations CRUD
===============

Create
------

.. code-block:: python

   from sqlalchemy.orm import Session
   
   def create_data(db: Session, name: str, value: int, description: str = None):
       db_data = DataModel(name=name, value=value, description=description)
       db.add(db_data)
       db.commit()
       db.refresh(db_data)
       return db_data

Read
----

.. code-block:: python

   # Récupérer toutes les données
   def get_all_data(db: Session, skip: int = 0, limit: int = 100):
       return db.query(DataModel).offset(skip).limit(limit).all()
   
   # Récupérer par ID
   def get_data_by_id(db: Session, data_id: int):
       return db.query(DataModel).filter(DataModel.id == data_id).first()
   
   # Recherche par nom
   def get_data_by_name(db: Session, name: str):
       return db.query(DataModel).filter(DataModel.name == name).all()

Update
------

.. code-block:: python

   def update_data(db: Session, data_id: int, name: str, value: int):
       db_data = db.query(DataModel).filter(DataModel.id == data_id).first()
       if db_data:
           db_data.name = name
           db_data.value = value
           db.commit()
           db.refresh(db_data)
       return db_data

Delete
------

.. code-block:: python

   def delete_data(db: Session, data_id: int):
       db_data = db.query(DataModel).filter(DataModel.id == data_id).first()
       if db_data:
           db.delete(db_data)
           db.commit()
       return db_data

Configuration Docker
====================

docker-compose.yml
------------------

.. code-block:: yaml

   services:
     db:
       image: postgres:15-alpine
       environment:
         POSTGRES_DB: ${POSTGRES_DB}
         POSTGRES_USER: ${POSTGRES_USER}
         POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
       volumes:
         - postgres_data:/var/lib/postgresql/data
       networks:
         - api-db
       healthcheck:
         test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
         interval: 10s
         timeout: 5s
         retries: 5
   
   volumes:
     postgres_data:
       driver: local
   
   networks:
     api-db:
       driver: bridge

Persistance
-----------

Le volume ``postgres_data`` persiste les données :

* Données conservées après ``docker-compose down``
* Supprimées uniquement avec ``docker-compose down -v``

Variables d'Environnement
==========================

Fichier .env
------------

.. code-block:: bash

   # PostgreSQL
   POSTGRES_DB=projet2_db
   POSTGRES_USER=projet2_user
   POSTGRES_PASSWORD=projet2_password
   POSTGRES_PORT=5432
   
   # API
   DATABASE_URL=postgresql://projet2_user:projet2_password@db:5432/projet2_db

⚠️ **Sécurité** : Ne jamais commiter ``.env`` ! Utiliser ``.env.example``.

Tests
=====

SQLite pour les Tests
---------------------

Les tests utilisent SQLite en mémoire pour éviter les dépendances :

.. code-block:: python

   import pytest
   from sqlalchemy import create_engine
   from sqlalchemy.orm import sessionmaker
   
   # Base SQLite fichier pour TestClient
   DATABASE_URL = "sqlite:///./test_db.sqlite"
   
   engine = create_engine(
       DATABASE_URL,
       connect_args={"check_same_thread": False}
   )
   
   TestSessionLocal = sessionmaker(bind=engine)
   
   @pytest.fixture
   def setup_database():
       Base.metadata.create_all(bind=engine)
       yield
       Base.metadata.drop_all(bind=engine)

Migration de Schéma
===================

Pour les migrations, utiliser **Alembic** (non inclus dans ce projet) :

.. code-block:: bash

   # Installation
   pip install alembic
   
   # Initialisation
   alembic init alembic
   
   # Créer une migration
   alembic revision --autogenerate -m "Create data table"
   
   # Appliquer les migrations
   alembic upgrade head

Backup et Restauration
=======================

Backup
------

.. code-block:: bash

   docker-compose exec db pg_dump -U projet2_user projet2_db > backup.sql

Restauration
------------

.. code-block:: bash

   docker-compose exec -T db psql -U projet2_user projet2_db < backup.sql

Monitoring
==========

Connexion à la Base
--------------------

.. code-block:: bash

   # Via Docker
   docker-compose exec db psql -U projet2_user -d projet2_db
   
   # Commandes SQL
   \dt              # Lister les tables
   \d data          # Décrire la table data
   SELECT * FROM data;

Logs PostgreSQL
---------------

.. code-block:: bash

   docker-compose logs db

Optimisation
============

Index
-----

Créer des index pour les colonnes fréquemment recherchées :

.. code-block:: python

   class DataModel(Base):
       __tablename__ = "data"
       
       id = Column(Integer, primary_key=True, index=True)
       name = Column(String, index=True)  # Index pour recherche rapide
       value = Column(Integer)

Pool de Connexions
------------------

Ajuster selon la charge :

.. code-block:: python

   engine = create_engine(
       DATABASE_URL,
       pool_size=20,        # Plus de connexions permanentes
       max_overflow=50,     # Plus de connexions temporaires
       pool_recycle=3600   # Recycler toutes les heures
   )

Prochaines Sections
===================

* :doc:`../testing/tests` : Tests de la base de données
* :doc:`../deployment/production` : Configuration production
