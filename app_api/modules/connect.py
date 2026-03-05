"""Module de connexion à la base de données avec SQLAlchemy."""
import os
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Base pour les modèles
Base = declarative_base()


class DataModel(Base):
    """Modèle SQLAlchemy pour la table data."""
    __tablename__ = "data"
    
    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


def get_database_url() -> str:
    """Récupère l'URL de la base de données depuis les variables d'environnement.
    
    Returns:
        URL de connexion à la base de données
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


def get_engine():
    """Crée et retourne un engine SQLAlchemy.
    
    Returns:
        Engine SQLAlchemy configuré
    """
    database_url = get_database_url()
    
    # Pour SQLite, on ajoute check_same_thread=False
    if database_url.startswith("sqlite"):
        engine = create_engine(
            database_url,
            connect_args={"check_same_thread": False}
        )
    else:
        engine = create_engine(database_url)
    
    return engine


def init_db():
    """Initialise la base de données en créant toutes les tables."""
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    return engine


def get_session():
    """Crée et retourne une session de base de données.
    
    Yields:
        Session SQLAlchemy
    """
    engine = get_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
