import unittest
from unittest.mock import patch, MagicMock
from app.retriever import retriever

class TestRetriever(unittest.TestCase):
    @patch('app.retriever.retriever.invoke')
    def test_query_retriever(self, mock_invoke):
        """Tester la fonction de récupération avec un mock"""
        # Simuler une réponse
        mock_invoke.return_value = [
            MagicMock(metadata={'row': 0}),
            MagicMock(metadata={'row': 1}),
        ]

        # Appeler le retriever
        result = retriever.invoke('Je veux eliquide avec lime.')

        # Vérifier que le retriever a été invoqué
        mock_invoke.assert_called_once_with('Je veux eliquide avec lime.')
        self.assertEqual(len(result), 2)

if __name__ == '__main__':
    unittest.main()
