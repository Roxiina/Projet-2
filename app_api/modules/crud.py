"""Module CRUD pour les opérations sur la base de données.

Ce module fournit les fonctions Create, Read, Update, Delete
pour manipuler les données dans la base.

Exemple d'utilisation:
    >>> from modules.crud import create_data, get_all_data
    >>> from modules.connect import get_session
    >>> for db in get_session():
    ...     data = create_data(db, value=42.5, description="Test")
    ...     all_data = get_all_data(db)
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from .connect import DataModel


def create_data(db: Session, value: float, description: Optional[str] = None) -> DataModel:
    """Crée une nouvelle entrée dans la base de données.

    Args:
        db: Session de base de données active
        value: Valeur numérique à stocker (float)
        description: Description optionnelle de la valeur

    Returns:
        DataModel: L'objet créé avec son ID et sa date de création
    
    Example:
        >>> data = create_data(db, value=42.5, description="Température")
        >>> print(f"ID créé: {data.id}")
    """
    # Créer une nouvelle instance du modèle
    db_data = DataModel(value=value, description=description)
    
    # Ajouter à la session et commiter
    db.add(db_data)
    db.commit()
    
    # Rafraîchir pour obtenir l'ID généré et la date
    db.refresh(db_data)
    return db_data


def get_all_data(db: Session, skip: int = 0, limit: int = 100) -> List[DataModel]:
    """Récupère toutes les données de la base avec pagination.

    Args:
        db: Session de base de données active
        skip: Nombre d'éléments à ignorer (défaut: 0)
        limit: Nombre maximum d'éléments à retourner (défaut: 100)

    Returns:
        List[DataModel]: Liste des objets DataModel, ordonnés par ID
    
    Example:
        >>> # Récupérer les 50 premiers résultats
        >>> data = get_all_data(db, skip=0, limit=50)
        >>> # Récupérer la page 2 (résultats 50-100)
        >>> data_page2 = get_all_data(db, skip=50, limit=50)
    """
    return db.query(DataModel).offset(skip).limit(limit).all()


def get_data_by_id(db: Session, data_id: int) -> Optional[DataModel]:
    """Récupère une donnée par son ID.

    Args:
        db: Session de base de données active
        data_id: ID de la donnée recherchée

    Returns:
        Optional[DataModel]: L'objet DataModel si trouvé, None sinon
    
    Example:
        >>> data = get_data_by_id(db, data_id=1)
        >>> if data:
        ...     print(f"Valeur: {data.value}")
        ... else:
        ...     print("Donnée introuvable")
    """
    return db.query(DataModel).filter(DataModel.id == data_id).first()


def delete_data(db: Session, data_id: int) -> bool:
    """Supprime une donnée par son ID.

    Args:
        db: Session de base de données active
        data_id: ID de la donnée à supprimer

    Returns:
        bool: True si supprimé avec succès, False si donnée introuvable
    
    Example:
        >>> if delete_data(db, data_id=1):
        ...     print("Donnée supprimée")
        ... else:
        ...     print("Donnée introuvable")
    """
    # Rechercher la donnée
    db_data = get_data_by_id(db, data_id)
    
    if db_data:
        # Supprimer et commiter
        db.delete(db_data)
        db.commit()
        return True
    
    return False
