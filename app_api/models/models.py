"""Modèles Pydantic pour l'API."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class DataCreate(BaseModel):
    """Modèle pour la création de données."""

    value: float = Field(..., description="Valeur numérique à stocker")
    description: Optional[str] = Field(None, description="Description optionnelle")

    model_config = ConfigDict(
        json_schema_extra={"example": {"value": 42.5, "description": "Une valeur de test"}}
    )


class DataResponse(BaseModel):
    """Modèle pour la réponse contenant les données."""

    id: int = Field(..., description="Identifiant unique")
    value: float = Field(..., description="Valeur numérique")
    description: Optional[str] = Field(None, description="Description")
    created_at: datetime = Field(..., description="Date de création")

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
