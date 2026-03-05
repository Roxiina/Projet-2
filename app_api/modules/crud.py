"""Module CRUD pour les opérations sur la base de données."""
from sqlalchemy.orm import Session
from typing import List, Optional
from .connect import DataModel


def create_data(db: Session, value: float, description: Optional[str] = None) -> DataModel:
    """Crée une nouvelle entrée dans la base de données.
    
    Args:
        db: Session de base de données
        value: Valeur numérique à stocker
        description: Description optionnelle
        
    Returns:
        L'objet DataModel créé
    """
    db_data = DataModel(value=value, description=description)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


def get_all_data(db: Session, skip: int = 0, limit: int = 100) -> List[DataModel]:
    """Récupère toutes les données de la base.
    
    Args:
        db: Session de base de données
        skip: Nombre d'éléments à ignorer
        limit: Nombre maximum d'éléments à retourner
        
    Returns:
        Liste des objets DataModel
    """
    return db.query(DataModel).offset(skip).limit(limit).all()


def get_data_by_id(db: Session, data_id: int) -> Optional[DataModel]:
    """Récupère une donnée par son ID.
    
    Args:
        db: Session de base de données
        data_id: ID de la donnée à récupérer
        
    Returns:
        L'objet DataModel ou None si non trouvé
    """
    return db.query(DataModel).filter(DataModel.id == data_id).first()


def delete_data(db: Session, data_id: int) -> bool:
    """Supprime une donnée par son ID.
    
    Args:
        db: Session de base de données
        data_id: ID de la donnée à supprimer
        
    Returns:
        True si supprimé avec succès, False sinon
    """
    db_data = get_data_by_id(db, data_id)
    if db_data:
        db.delete(db_data)
        db.commit()
        return True
    return False
