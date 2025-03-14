import pytest
from app import create_app  # Assurez-vous que vous avez une fonction qui crée votre app
from flask import url_for
from flask_login import login_user
from app.models import User, Recommendation, user_db  # Importez vos modèles

@pytest.fixture
def client():
    app = create_app()  # Créez l'application Flask
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Utilisation d'une base de données SQLite pour les tests
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Désactive les notifications de modification de SQLAlchemy

    # Créez le client de test dans le contexte de l'application
    with app.app_context():  # Crée le contexte de l'application Flask
        # Réinitialisez la base de données avant chaque test
        user_db.drop_all()  # Supprime les anciennes tables
        user_db.create_all()  # Crée les tables de la base de données

        # Créez un utilisateur de test et ajoutez-le à la base de données
        user = User(id=1, username='dewaleto', password='dela', consent=False)
        user_db.session.add(user)  # Ajoutez l'utilisateur à la session
        user_db.session.commit()  # Commitez les changements dans la base de données

        yield app.test_client()  # Retourne le client de test

        # Après le test, vous pouvez réinitialiser la session ou la base de données si nécessaire
        user_db.session.remove()


def test_user_in_database(client):
    # Vérifier si l'utilisateur avec id=1 existe dans la base de données
    user = User.query.get(1)  # Récupérer l'utilisateur par son id
    assert user is not None  # L'utilisateur doit exister dans la base de données de test
    assert user.username == 'dewaleto'  # Vérifiez si le nom d'utilisateur est correct
    assert user.password == 'dela'  # Vérifiez si le mot de passe est correct


# def test_recommendation_database_insertion(client):
#     # Authentification de l'utilisateur
#     user = User.query.get(1)  # Récupérez l'utilisateur par son ID
#     with client.session_transaction() as session:
#         login_user(user)  # Connexion de l'utilisateur dans le contexte de session

#     # Simuler l'insertion d'une recommandation
#     response = client.post('/recommend', data={'question': 'Je veux un produit avec citron'})

#     # Vérifiez si la recommandation a bien été insérée dans la base de données
#     recommendation = Recommendation.query.filter_by(question='Je veux un produit avec citron').first()
    
#     # Vérifiez que la recommandation existe dans la base de données
#     assert recommendation is not None  # La recommandation doit exister
#     assert recommendation.question == 'Je veux un produit avec citron'  # Vérifiez la question de la recommandation

def test_login_success(client):
    # Simule la soumission du formulaire de connexion avec les bonnes informations d'identification
    response = client.post('/login', data={
        'username': 'dewaleto',
        'password': 'dela'
    }, follow_redirects=True)  # Suivre la redirection après une connexion réussie

    # Vérifier si l'utilisateur est redirigé vers la page d'index
    assert response.status_code == 200
    # assert 'Connexion réussie' in response.data.decode()  # Vérifier que le titre "Sélectionnez un goût" est présent
