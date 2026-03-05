"""Configuration pytest pour les tests."""
import pytest
import sys
from pathlib import Path

# Ajouter le dossier app_api au PYTHONPATH
api_path = Path(__file__).parent / "app_api"
sys.path.insert(0, str(api_path))
