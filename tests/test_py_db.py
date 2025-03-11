# Fichier : tests/test_db.py
import pytest
from app.db import get_products

@pytest.fixture
def setup_database():
    # Initialisation de la base de données pour les tests si nécessaire
    # Par exemple, en utilisant pytest-postgresql pour une base de données temporaire
    yield
    # Nettoyage après les tests si nécessaire

def test_get_products(setup_database):
    # Test de la fonction get_products
    gout = 'fruit'
    per_page = 10
    offset = 0

    produits_list, total_count = get_products(gout, per_page, offset)

    assert len(produits_list) == per_page
    assert total_count >= per_page
