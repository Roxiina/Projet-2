"""Module contenant les fonctions mathématiques de base."""


def add(a: float, b: float) -> float:
    """Additionne deux nombres.

    Args:
        a: Premier nombre
        b: Deuxième nombre

    Returns:
        La somme de a et b
    """
    return a + b


def sub(a: float, b: float) -> float:
    """Soustrait deux nombres.

    Args:
        a: Premier nombre
        b: Deuxième nombre

    Returns:
        La différence de a et b
    """
    return a - b


def square(a: float) -> float:
    """Calcule le carré d'un nombre.

    Args:
        a: Le nombre à élever au carré

    Returns:
        Le carré de a
    """
    return a * a


def print_data(data: list[dict]) -> None:
    """Affiche les données formatées.

    Args:
        data: Liste de dictionnaires contenant les données
    """
    for item in data:
        print(f"ID: {item.get('id')}, Valeur: {item.get('value')}")
