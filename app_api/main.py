"""API FastAPI pour gérer les données."""
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os

from models import DataCreate, DataResponse
from modules import get_session, init_db, create_data, get_all_data, get_data_by_id

# Créer l'application FastAPI
app = FastAPI(
    title="Data Management API",
    description="API pour gérer les données avec persistance en base de données",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier les origines autorisées
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialise la base de données au démarrage."""
    init_db()
    print("🚀 Base de données initialisée")
    print(f"📊 Environnement: {os.getenv('ENVIRONMENT', 'development')}")


@app.get("/")
async def root():
    """Route racine de l'API."""
    return {
        "message": "Bienvenue sur l'API de gestion de données",
        "version": "1.0.0",
        "endpoints": {
            "POST /data": "Créer une nouvelle donnée",
            "GET /data": "Récupérer toutes les données",
            "GET /data/{id}": "Récupérer une donnée par ID"
        }
    }


@app.post("/data", response_model=DataResponse, status_code=201)
async def create_new_data(
    data: DataCreate,
    db: Session = Depends(get_session)
):
    """Crée une nouvelle entrée de données.
    
    Args:
        data: Données à créer (valeur et description optionnelle)
        db: Session de base de données
        
    Returns:
        Les données créées avec leur ID
    """
    db_data = create_data(
        db=db,
        value=data.value,
        description=data.description
    )
    return db_data


@app.get("/data", response_model=List[DataResponse])
async def read_all_data(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_session)
):
    """Récupère toutes les données.
    
    Args:
        skip: Nombre d'éléments à ignorer (pagination)
        limit: Nombre maximum d'éléments à retourner
        db: Session de base de données
        
    Returns:
        Liste de toutes les données
    """
    data = get_all_data(db=db, skip=skip, limit=limit)
    return data


@app.get("/data/{data_id}", response_model=DataResponse)
async def read_data(
    data_id: int,
    db: Session = Depends(get_session)
):
    """Récupère une donnée par son ID.
    
    Args:
        data_id: ID de la donnée à récupérer
        db: Session de base de données
        
    Returns:
        La donnée correspondante
        
    Raises:
        HTTPException: Si la donnée n'existe pas
    """
    data = get_data_by_id(db=db, data_id=data_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Donnée non trouvée")
    return data


@app.get("/health")
async def health_check():
    """Vérifie l'état de santé de l'API."""
    return {"status": "healthy", "service": "api"}
