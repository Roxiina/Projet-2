"""Tests pour les fonctions mathématiques."""

from app_api.maths import add, square, sub


def test_add():
    """Test de la fonction add."""
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
    assert add(2.5, 3.5) == 6.0
    assert add(-5, -3) == -8


def test_sub():
    """Test de la fonction sub."""
    assert sub(5, 3) == 2
    assert sub(0, 5) == -5
    assert sub(10, 10) == 0
    assert sub(7.5, 2.5) == 5.0
    assert sub(-3, -5) == 2


def test_square():
    """Test de la fonction square."""
    assert square(0) == 0
    assert square(1) == 1
    assert square(2) == 4
    assert square(5) == 25
    assert square(-3) == 9
    assert square(2.5) == 6.25


def test_add_with_floats():
    """Test de add avec des nombres à virgule."""
    result = add(0.1, 0.2)
    assert abs(result - 0.3) < 0.0001


def test_mathematical_operations():
    """Test combiné des opérations mathématiques."""
    # Test: (5 + 3)² - 10 = 64 - 10 = 54
    result = sub(square(add(5, 3)), 10)
    assert result == 54
