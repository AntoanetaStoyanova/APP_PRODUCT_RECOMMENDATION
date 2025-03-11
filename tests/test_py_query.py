# tests/test_routes.py

def test_query(client):
    # Test avec une question valide
    response = client.post('/query', data={'question': 'Quel est le produit avec le goût de Fraise ?'})
    assert response.status_code == 200
    assert b'produit' in response.data  # Vérifiez que la réponse contient le mot "produit"

    # Test avec une question vide
    response = client.post('/query', data={'question': ''})
    assert response.status_code == 400
    assert b'Veuillez entrer une question.' in response.data
