# import unittest
# from flask_testing import TestCase
# from unittest.mock import patch, MagicMock
# from app import create_app  # Importation de la fonction create_app
# import requests
# import sys
# import os
# # Ajout du répertoire racine au chemin d'importation
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
# from config import Config  # Correctement importé depuis la racine

# class TestRecommendRoute(TestCase):

#     def create_app(self):
#         app = create_app()  # Crée l'application via create_app()
#         app.config['TESTING'] = True
#         return app

#     @patch('app.routes.qa_chain.invoke', autospec=True)
#     @patch('app.routes.retriever.invoke', autospec=True)
#     @patch('app.routes.user_db.session.commit', autospec=True)
#     def test_recommend_valid_question(self, mock_commit, mock_retriever, mock_qa_chain):
#         mock_qa_chain.return_value = "Recommandation réussie"
#         mock_retriever.return_value = ["id_produit: 5", "id_produit: 7"]
#         response = self.client.post('/recommend', json={'question': 'Quel est le meilleur e-liquide avec citron?'})

#         mock_qa_chain.assert_called_once_with('Quel est le meilleur e-liquide avec citron?')
#         mock_retriever.assert_called_once_with('Quel est le meilleur e-liquide avec citron?')

#         self.assertEqual(response.status_code, 200)
#         self.assertIn("Recommandation réussie", response.data.decode('utf-8'))

#     @patch('app.routes.qa_chain.invoke', autospec=True)
#     @patch('app.routes.retriever.invoke', autospec=True)
#     def test_recommend_empty_question(self, mock_retriever, mock_qa_chain):
#         response = self.client.post('/recommend', json={'question': ''})

#         self.assertEqual(response.status_code, 400)
#         self.assertIn(b"Veuillez entrer une question.", response.data)

#     @patch('app.routes.qa_chain.invoke', autospec=True)
#     @patch('app.routes.retriever.invoke', autospec=True)
#     def test_recommend_api_error(self, mock_retriever, mock_qa_chain):
#         mock_qa_chain.side_effect = requests.exceptions.RequestException("Erreur API")

#         response = self.client.post('/recommend', json={'question': 'Quel est le meilleur e-liquide avec citron?'})

#         self.assertEqual(response.status_code, 500)
#         self.assertIn(b"Une erreur inattendue est survenue", response.data)

#     @patch('app.routes.qa_chain.invoke', autospec=True)
#     @patch('app.routes.retriever.invoke', autospec=True)
#     @patch('time.sleep', autospec=True)
#     def test_recommend_retry_on_429_error(self, mock_sleep, mock_retriever, mock_qa_chain):
#         exception = requests.exceptions.RequestException()
#         exception.response = MagicMock()
#         exception.response.status_code = 429
#         mock_qa_chain.side_effect = exception

#         response = self.client.post('/recommend', json={'question': 'Quel est le meilleur e-liquide avec citron?'})

#         mock_sleep.assert_called_once_with(1)
#         self.assertEqual(response.status_code, 500)
#         self.assertIn("Impossible de récupérer les données après plusieurs tentatives.", response.data)

# if __name__ == '__main__':
#     unittest.main()

# # pytest tests/test_routes_api.py


import unittest
from flask_testing import TestCase
from unittest.mock import patch, MagicMock
from app import create_app  # Importation de la fonction create_app
import requests
import sys
import os
# Ajout du répertoire racine au chemin d'importation
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from config import Config  # Correctement importé depuis la racine

class TestRecommendRoute(TestCase):

    def create_app(self):
        app = create_app()  # Crée l'application via create_app()
        app.config['TESTING'] = True
        return app

    @patch('app.routes.qa_chain.invoke', autospec=True)
    @patch('app.routes.retriever.retrieve', autospec=True)  # Mock the method on retriever, not FAISS directly
    @patch('app.routes.user_db.session.commit', autospec=True)
    def test_recommend_valid_question(self, mock_commit, mock_retrieve, mock_qa_chain):
        mock_qa_chain.return_value = "Recommandation réussie"
        mock_retrieve.return_value = ["id_produit: 5", "id_produit: 7"]  # mock return value for retrieve
        response = self.client.post('/recommend', json={'question': 'Quel est le meilleur e-liquide avec citron?'})

        mock_qa_chain.assert_called_once_with('Quel est le meilleur e-liquide avec citron?')
        mock_retrieve.assert_called_once_with('Quel est le meilleur e-liquide avec citron?')

        self.assertEqual(response.status_code, 200)
        self.assertIn("Recommandation réussie", response.data.decode('utf-8'))

    @patch('app.routes.qa_chain.invoke', autospec=True)
    @patch('app.routes.retriever.retrieve', autospec=True)  # Mock the method on retriever
    def test_recommend_empty_question(self, mock_retrieve, mock_qa_chain):
        response = self.client.post('/recommend', json={'question': ''})

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Veuillez entrer une question.", response.data)

    @patch('app.routes.qa_chain.invoke', autospec=True)
    @patch('app.routes.retriever.retrieve', autospec=True)  # Mock the method on retriever
    def test_recommend_api_error(self, mock_retrieve, mock_qa_chain):
        mock_qa_chain.side_effect = requests.exceptions.RequestException("Erreur API")

        response = self.client.post('/recommend', json={'question': 'Quel est le meilleur e-liquide avec citron?'})

        self.assertEqual(response.status_code, 500)
        self.assertIn(b"Une erreur inattendue est survenue", response.data)

    @patch('app.routes.qa_chain.invoke', autospec=True)
    @patch('app.routes.retriever.retrieve', autospec=True)  # Mock the method on retriever
    @patch('time.sleep', autospec=True)
    def test_recommend_retry_on_429_error(self, mock_sleep, mock_retrieve, mock_qa_chain):
        exception = requests.exceptions.RequestException()
        exception.response = MagicMock()
        exception.response.status_code = 429
        mock_qa_chain.side_effect = exception

        response = self.client.post('/recommend', json={'question': 'Quel est le meilleur e-liquide avec citron?'})

        mock_sleep.assert_called_once_with(1)
        self.assertEqual(response.status_code, 500)
        self.assertIn("Impossible de récupérer les données après plusieurs tentatives.", response.data)

if __name__ == '__main__':
    unittest.main()
