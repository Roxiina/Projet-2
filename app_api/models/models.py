"""Modèles Pydantic pour l'API.

Ce module définit les schémas de validation des données
pour les requêtes et réponses de l'API.

Exemple d'utilisation:
    >>> from models import DataCreate, DataResponse
    >>> data = DataCreate(value=42.5, description="Test")
    >>> print(data.model_dump_json())
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class DataCreate(BaseModel):
    """Modèle pour la création de données.
    
    Utilisé pour valider les données reçues dans les requêtes POST.
    
    Attributes:
        value: Valeur numérique à stocker (obligatoire)
        description: Description textuelle optionnelle
    """

    value: float = Field(..., description="Valeur numérique à stocker", examples=[42.5])
    description: Optional[str] = Field(
        None, 
        description="Description optionnelle",
        max_length=500,
        examples=["Température moyenne"]
    )

    model_config = ConfigDict(
        json_schema_extra={"example": {"value": 42.5, "description": "Une valeur de test"}}
    )


class DataResponse(BaseModel):
    """Modèle pour la réponse contenant les données.
    
    Utilisé pour sérialiser les données retournées par l'API.
    
    Attributes:
        id: Identifiant unique auto-généré
        value: Valeur numérique stockée
        description: Description optionnelle
        created_at: Date et heure de création (UTC)
    """

    id: int = Field(..., description="Identifiant unique", examples=[1])
    value: float = Field(..., description="Valeur numérique", examples=[42.5])
    description: Optional[str] = Field(
        None, 
        description="Description",
        examples=["Température moyenne"]
    )
    created_at: datetime = Field(
        ..., 
        description="Date de création",
        examples=["2026-03-05T10:00:00"]
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "value": 42.5,
                "description": "Une valeur de test",
                "created_at": "2026-03-05T10:00:00",
            }
        },
    )
