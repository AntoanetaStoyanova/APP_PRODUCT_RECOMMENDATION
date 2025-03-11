import pytest
from flask import Flask
from app import main_bp  # Assure-toi d'importer ton blueprint correctement

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(main_bp)  # Associe ton blueprint ici
    app.config['TESTING'] = True  # Active le mode test
    client = app.test_client()
    yield client  # Le client est disponible pour les tests

# Test de la route d'accueil
def test_acceuil(client, mocker):
    # Mock de render_template
    mocker.patch('app.routes.render_template', return_value='Some HTML content')

    # Effectuer la requête GET
    response = client.get('/')

    # Vérification que le code de statut est 200
    assert response.status_code == 200
    # Vérification que le contenu retourné est celui du mock
    assert response.data == b'Some HTML content'
