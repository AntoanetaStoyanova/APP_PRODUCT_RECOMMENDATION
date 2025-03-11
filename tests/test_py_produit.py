# tests/test_routes.py

def test_show_produits(client):
    # Test pour une page valide
    response = client.get('/produit?gout=Fraise&page=1')
    assert response.status_code == 200
    assert b'Fraise' in response.data  # Vérifiez que le goût est affiché sur la page

    # Test avec un goût non défini (devrait renvoyer une erreur ou une page vide)
    response = client.get('/produit?gout=NonExistant&page=1')
    assert response.status_code == 200  # La page peut encore exister, mais sans produits
    assert b'NonExistant' not in response.data
