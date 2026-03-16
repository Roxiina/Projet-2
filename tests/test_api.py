"""Tests pour l'API FastAPI."""

import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from modules.connect import Base, get_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Définir la variable d'environnement avant d'importer l'application
os.environ["DB_TYPE"] = "sqlite"

# Importer l'application après avoir défini les variables d'environnement 
from main import app  # noqa: E402

# Base de données de test
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.sqlite"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


def override_get_session():
    """Override de la session de base de données pour les tests."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Override session pour les tests
app.dependency_overrides[get_session] = override_get_session

# Créer les tables avant de créer le client
Base.metadata.create_all(bind=engine)

# Créer le client de test
client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def cleanup_database():
    """Fixture pour nettoyer le fichier de base de données après tous les tests."""
    yield
    # Fermer toutes les connexions
    Base.metadata.drop_all(bind=engine)
    engine.dispose()
    # Supprimer le fichier de test après tous les tests du module
    db_file = Path("./test_db.sqlite")
    try:
        if db_file.exists():
            db_file.unlink()
    except PermissionError:
        # Sur Windows, le fichier peut encore être verrouillé
        pass


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Fixture pour nettoyer la base de données entre chaque test."""
    yield
    # Nettoyer les données après chaque test (mais pas les tables)
    with TestingSessionLocal() as db:
        db.execute(Base.metadata.tables['data'].delete())
        db.commit()


def test_read_root():
    """Test de la route racine."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "version" in response.json()


def test_health_check():
    """Test du health check."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "api"}


def test_create_data():
    """Test de la création de données."""
    data = {"value": 42.5, "description": "Test data"}
    response = client.post("/data", json=data)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["value"] == 42.5
    assert response_data["description"] == "Test data"
    assert "id" in response_data
    assert "created_at" in response_data


def test_create_data_without_description():
    """Test de la création de données sans description."""
    data = {"value": 100.0}
    response = client.post("/data", json=data)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["value"] == 100.0
    assert response_data["description"] is None


def test_get_all_data():
    """Test de la récupération de toutes les données."""
    # Créer quelques données de test
    client.post("/data", json={"value": 10.0, "description": "First"})
    client.post("/data", json={"value": 20.0, "description": "Second"})

    response = client.get("/data")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_get_data_by_id():
    """Test de la récupération d'une donnée par ID."""
    # Créer une donnée
    create_response = client.post("/data", json={"value": 50.0, "description": "Test by ID"})
    created_id = create_response.json()["id"]

    # Récupérer par ID
    response = client.get(f"/data/{created_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_id
    assert data["value"] == 50.0
    assert data["description"] == "Test by ID"


def test_get_nonexistent_data():
    """Test de la récupération d'une donnée inexistante."""
    response = client.get("/data/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Donnée non trouvée"


def test_create_data_invalid():
    """Test de la création de données avec des données invalides."""
    # Valeur manquante
    response = client.post("/data", json={"description": "No value"})
    assert response.status_code == 422  # Unprocessable Entity

    # Type incorrect
    response = client.post("/data", json={"value": "not a number"})
    assert response.status_code == 422


def test_pagination():
    """Test de la pagination."""
    # Créer plusieurs données
    for i in range(10):
        client.post("/data", json={"value": float(i), "description": f"Data {i}"})

    # Test avec limit
    response = client.get("/data?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 5

    # Test avec skip et limit
    response = client.get("/data?skip=5&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 5
