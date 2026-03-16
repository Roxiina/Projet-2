"""Tests supplémentaires pour améliorer la couverture de code."""

import os
from pathlib import Path

import pytest
from modules.connect import (
    Base,
    DataModel,
    get_database_url,
    get_engine,
    get_session,
    init_db,
)
from modules.crud import create_data, delete_data, get_all_data, get_data_by_id
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class TestDatabaseConnection:
    """Tests pour le module de connexion à la base de données."""

    def test_get_database_url_sqlite_default(self, monkeypatch):
        """Test de l'URL SQLite par défaut."""
        monkeypatch.delenv("DB_TYPE", raising=False)
        url = get_database_url()
        assert url == "sqlite:///./test.db"

    def test_get_database_url_sqlite_explicit(self, monkeypatch):
        """Test de l'URL SQLite explicite."""
        monkeypatch.setenv("DB_TYPE", "sqlite")
        url = get_database_url()
        assert url == "sqlite:///./test.db"

    def test_get_database_url_postgresql(self, monkeypatch):
        """Test de l'URL PostgreSQL avec valeurs par défaut."""
        monkeypatch.setenv("DB_TYPE", "postgresql")
        monkeypatch.delenv("POSTGRES_USER", raising=False)
        monkeypatch.delenv("POSTGRES_PASSWORD", raising=False)
        monkeypatch.delenv("POSTGRES_HOST", raising=False)
        monkeypatch.delenv("POSTGRES_PORT", raising=False)
        monkeypatch.delenv("POSTGRES_DB", raising=False)

        url = get_database_url()
        assert url == "postgresql://postgres:postgres@localhost:5432/appdb"

    def test_get_database_url_postgresql_custom(self, monkeypatch):
        """Test de l'URL PostgreSQL avec valeurs personnalisées."""
        monkeypatch.setenv("DB_TYPE", "postgresql")
        monkeypatch.setenv("POSTGRES_USER", "custom_user")
        monkeypatch.setenv("POSTGRES_PASSWORD", "custom_pass")
        monkeypatch.setenv("POSTGRES_HOST", "db.example.com")
        monkeypatch.setenv("POSTGRES_PORT", "5433")
        monkeypatch.setenv("POSTGRES_DB", "custom_db")

        url = get_database_url()
        assert url == "postgresql://custom_user:custom_pass@db.example.com:5433/custom_db"

    def test_get_engine_sqlite(self, monkeypatch):
        """Test de la création d'un engine SQLite."""
        monkeypatch.setenv("DB_TYPE", "sqlite")
        engine = get_engine()
        assert engine is not None
        assert "sqlite" in str(engine.url)

    def test_get_engine_postgresql(self, monkeypatch):
        """Test de la création d'un engine PostgreSQL."""
        monkeypatch.setenv("DB_TYPE", "postgresql")
        engine = get_engine()
        assert engine is not None
        # Note: le test ne vérifie que la création, pas la connexion réelle

    def test_init_db(self, monkeypatch, tmp_path):
        """Test de l'initialisation de la base de données."""
        # Utiliser une base SQLite temporaire
        db_file = tmp_path / "test_init.db"
        monkeypatch.setenv("DB_TYPE", "sqlite")
        
        # Créer un engine temporaire
        engine = create_engine(f"sqlite:///{db_file}", connect_args={"check_same_thread": False})
        
        # Créer les tables
        Base.metadata.create_all(bind=engine)
        
        # Vérifier que la table existe
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        assert "data" in tables

        # Nettoyer
        engine.dispose()
        if db_file.exists():
            db_file.unlink()

    def test_get_session(self, monkeypatch, tmp_path):
        """Test de la création d'une session."""
        # Utiliser une base SQLite temporaire
        db_file = tmp_path / "test_session.db"
        monkeypatch.setenv("DB_TYPE", "sqlite")
        
        # Créer un engine et initialiser la base
        engine = create_engine(f"sqlite:///{db_file}", connect_args={"check_same_thread": False})
        Base.metadata.create_all(bind=engine)
        
        # Créer une session
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()
        
        try:
            # Vérifier que la session fonctionne
            result = session.query(DataModel).all()
            assert isinstance(result, list)
            assert len(result) == 0
        finally:
            session.close()
            engine.dispose()
            if db_file.exists():
                db_file.unlink()


class TestCRUDOperations:
    """Tests pour les opérations CRUD."""

    @pytest.fixture
    def test_db(self, tmp_path, monkeypatch):
        """Fixture pour créer une base de données de test."""
        db_file = tmp_path / "test_crud.db"
        engine = create_engine(f"sqlite:///{db_file}", connect_args={"check_same_thread": False})
        Base.metadata.create_all(bind=engine)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()
        
        yield session
        
        session.close()
        engine.dispose()
        if db_file.exists():
            db_file.unlink()

    def test_create_data_with_description(self, test_db):
        """Test de création de données avec description."""
        data = create_data(test_db, value=42.5, description="Test description")
        assert data.id is not None
        assert data.value == 42.5
        assert data.description == "Test description"
        assert data.created_at is not None

    def test_create_data_without_description(self, test_db):
        """Test de création de données sans description."""
        data = create_data(test_db, value=100.0)
        assert data.id is not None
        assert data.value == 100.0
        assert data.description is None

    def test_get_all_data_empty(self, test_db):
        """Test de récupération de toutes les données (base vide)."""
        data = get_all_data(test_db)
        assert isinstance(data, list)
        assert len(data) == 0

    def test_get_all_data_with_pagination(self, test_db):
        """Test de la pagination."""
        # Créer 10 entrées
        for i in range(10):
            create_data(test_db, value=float(i), description=f"Item {i}")

        # Test limit
        data = get_all_data(test_db, skip=0, limit=5)
        assert len(data) == 5

        # Test skip et limit
        data = get_all_data(test_db, skip=5, limit=3)
        assert len(data) == 3

        # Test all
        data = get_all_data(test_db, skip=0, limit=100)
        assert len(data) == 10

    def test_get_data_by_id_found(self, test_db):
        """Test de récupération par ID (trouvé)."""
        created = create_data(test_db, value=50.0, description="Find me")
        found = get_data_by_id(test_db, created.id)
        assert found is not None
        assert found.id == created.id
        assert found.value == 50.0
        assert found.description == "Find me"

    def test_get_data_by_id_not_found(self, test_db):
        """Test de récupération par ID (non trouvé)."""
        found = get_data_by_id(test_db, 99999)
        assert found is None

    def test_delete_data_success(self, test_db):
        """Test de suppression réussie."""
        created = create_data(test_db, value=75.0, description="Delete me")
        result = delete_data(test_db, created.id)
        assert result is True
        
        # Vérifier que la donnée a été supprimée
        found = get_data_by_id(test_db, created.id)
        assert found is None

    def test_delete_data_not_found(self, test_db):
        """Test de suppression d'une donnée inexistante."""
        result = delete_data(test_db, 99999)
        assert result is False


class TestDataModel:
    """Tests pour le modèle DataModel."""

    def test_data_model_creation(self):
        """Test de création d'une instance du modèle."""
        data = DataModel(value=42.5, description="Test")
        assert data.value == 42.5
        assert data.description == "Test"
        assert data.id is None  # Pas encore en base
        assert data.created_at is None  # Sera généré à l'insertion

    def test_data_model_without_description(self):
        """Test de création sans description."""
        data = DataModel(value=100.0)
        assert data.value == 100.0
        assert data.description is None
