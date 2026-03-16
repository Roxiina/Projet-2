"""Tests pour les endpoints de suppression et fonctionnalités additionnelles."""

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
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_delete_db.sqlite"

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
    db_file = Path("./test_delete_db.sqlite")
    try:
        if db_file.exists():
            db_file.unlink()
    except PermissionError:
        pass


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Fixture pour nettoyer la base de données entre chaque test."""
    yield
    # Nettoyer les données après chaque test (mais pas les tables)
    with TestingSessionLocal() as db:
        db.execute(Base.metadata.tables['data'].delete())
        db.commit()



def test_delete_data_success():
    """Test de la suppression réussie d'une donnée."""
    # Créer une donnée
    create_response = client.post("/data", json={"value": 42.0, "description": "To delete"})
    created_id = create_response.json()["id"]

    # Supprimer la donnée
    delete_response = client.delete(f"/data/{created_id}")
    assert delete_response.status_code == 204

    # Vérifier qu'elle n'existe plus
    get_response = client.get(f"/data/{created_id}")
    assert get_response.status_code == 404


def test_delete_nonexistent_data():
    """Test de la suppression d'une donnée inexistante."""
    response = client.delete("/data/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Donnée non trouvée"


def test_create_multiple_data():
    """Test de la création de plusieurs données."""
    data_list = [
        {"value": 10.0, "description": "First"},
        {"value": 20.0, "description": "Second"},
        {"value": 30.0, "description": "Third"},
    ]

    for data in data_list:
        response = client.post("/data", json=data)
        assert response.status_code == 201

    # Récupérer toutes les données
    response = client.get("/data")
    assert response.status_code == 200
    all_data = response.json()
    assert len(all_data) >= 3


def test_get_data_with_large_limit():
    """Test de récupération avec une large limite."""
    # Créer 20 données
    for i in range(20):
        client.post("/data", json={"value": float(i), "description": f"Data {i}"})

    # Récupérer avec limite de 200
    response = client.get("/data?limit=200")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 20


def test_get_data_with_zero_limit():
    """Test de récupération avec limite zéro."""
    # Créer quelques données
    for i in range(5):
        client.post("/data", json={"value": float(i)})

    # Récupérer avec limite 0 devrait retourner une liste vide
    response = client.get("/data?limit=0")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0


def test_create_data_with_negative_value():
    """Test de création de données avec une valeur négative."""
    data = {"value": -42.5, "description": "Negative value"}
    response = client.post("/data", json=data)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["value"] == -42.5


def test_create_data_with_zero_value():
    """Test de création de données avec une valeur nulle."""
    data = {"value": 0.0, "description": "Zero value"}
    response = client.post("/data", json=data)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["value"] == 0.0


def test_create_data_with_very_large_value():
    """Test de création de données avec une très grande valeur."""
    data = {"value": 1e308, "description": "Very large value"}
    response = client.post("/data", json=data)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["value"] == 1e308


def test_create_data_with_long_description():
    """Test de création de données avec une longue description (dans la limite)."""
    long_description = "A" * 400  # Sous la limite de 500
    data = {"value": 42.0, "description": long_description}
    response = client.post("/data", json=data)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["description"] == long_description


def test_create_data_with_too_long_description():
    """Test de création de données avec une description trop longue (validation échoue)."""
    too_long_description = "A" * 600  # Au-dessus de la limite de 500
    data = {"value": 42.0, "description": too_long_description}
    response = client.post("/data", json=data)
    assert response.status_code == 422  # Unprocessable Entity - validation error


def test_get_data_pagination_edge_cases():
    """Test des cas limites de la pagination."""
    # Créer 10 données
    for i in range(10):
        client.post("/data", json={"value": float(i)})

    # Skip plus grand que le nombre total
    response = client.get("/data?skip=100&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0

    # Skip négatif (devrait être traité comme 0)
    response = client.get("/data?skip=-5&limit=5")
    assert response.status_code == 200


def test_create_data_with_empty_description():
    """Test de création de données avec une description vide."""
    data = {"value": 42.0, "description": ""}
    response = client.post("/data", json=data)
    assert response.status_code == 201
    response_data = response.json()
    assert response_data["description"] == ""


def test_api_cors_headers():
    """Test de la présence des headers CORS."""
    response = client.get("/")
    # FastAPI/TestClient automatically handles CORS in tests
    assert response.status_code == 200
