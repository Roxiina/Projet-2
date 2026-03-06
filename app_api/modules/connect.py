"""Module de connexion à la base de données avec SQLAlchemy.

Ce module gère la connexion à la base de données (PostgreSQL ou SQLite)
et définit le modèle de données principal.

Exemple d'utilisation:
    >>> from modules.connect import get_session, init_db
    >>> init_db()  # Créer les tables
    >>> for db in get_session():  # Obtenir une session
    ...     # Utiliser la session
    ...     pass
"""

import os
from datetime import datetime
from typing import Generator

from sqlalchemy import Column, DateTime, Float, Integer, String, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

# Base pour les modèles
Base = declarative_base()


class DataModel(Base):
    """Modèle SQLAlchemy pour la table data.

    Attributes:
        id: Identifiant unique auto-incrémenté
        value: Valeur numérique stockée
        description: Description optionnelle de la valeur
        created_at: Date et heure de création (UTC)
    """

    __tablename__ = "data"

    id = Column(Integer, primary_key=True, index=True, comment="Identifiant unique")
    value = Column(Float, nullable=False, comment="Valeur numérique")
    description = Column(String, nullable=True, comment="Description optionnelle")
    created_at = Column(DateTime, default=datetime.utcnow, comment="Date de création")


def get_database_url() -> str:
    """Récupère l'URL de la base de données depuis les variables d'environnement.

    Lit la variable DB_TYPE pour déterminer le type de base (postgresql ou sqlite).
    Pour PostgreSQL, lit POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST,
    POSTGRES_PORT et POSTGRES_DB.

    Returns:
        str: URL de connexion au format SQLAlchemy
            - PostgreSQL: postgresql://user:pass@host:port/db
            - SQLite: sqlite:///./test.db

    Example:
        >>> os.environ["DB_TYPE"] = "postgresql"
        >>> url = get_database_url()
        >>> print(url)  # postgresql://postgres:postgres@localhost:5432/appdb
    """
    db_type = os.getenv("DB_TYPE", "sqlite")

    if db_type == "postgresql":
        user = os.getenv("POSTGRES_USER", "postgres")
        password = os.getenv("POSTGRES_PASSWORD", "postgres")
        host = os.getenv("POSTGRES_HOST", "localhost")
        port = os.getenv("POSTGRES_PORT", "5432")
        database = os.getenv("POSTGRES_DB", "appdb")
        return f"postgresql://{user}:{password}@{host}:{port}/{database}"
    else:
        # SQLite par défaut pour le développement
        return "sqlite:///./test.db"


def get_engine() -> Engine:
    """Crée et retourne un engine SQLAlchemy.

    Configure automatiquement l'engine selon le type de base de données.
    Pour SQLite, ajoute check_same_thread=False pour permettre
    l'utilisation multi-thread.

    Returns:
        Engine: Engine SQLAlchemy configuré et prêt à l'emploi
    """
    database_url = get_database_url()

    # Pour SQLite, on ajoute check_same_thread=False pour FastAPI
    if database_url.startswith("sqlite"):
        engine = create_engine(database_url, connect_args={"check_same_thread": False})
    else:
        engine = create_engine(database_url)

    return engine


def init_db() -> Engine:
    """Initialise la base de données en créant toutes les tables.

    Crée automatiquement toutes les tables définies par les modèles
    qui héritent de Base. Si les tables existent déjà, ne fait rien.

    Returns:
        Engine: Engine SQLAlchemy utilisé pour l'initialisation
    """
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    return engine


def get_session() -> Generator[Session, None, None]:
    """Crée et retourne une session de base de données.

    Générateur qui crée une session, la yield pour utilisation,
    puis la ferme automatiquement. Utilisé avec Depends() dans FastAPI.

    Yields:
        Session: Session SQLAlchemy pour interagir avec la base

    Example:
        >>> @app.get("/data")
        >>> async def read_data(db: Session = Depends(get_session)):
        ...     return db.query(DataModel).all()
    """
    engine = get_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
