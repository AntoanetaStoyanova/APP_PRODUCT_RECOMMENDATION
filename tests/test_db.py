import unittest
from unittest.mock import patch, MagicMock
from app.db import get_products

class TestDB(unittest.TestCase):
    @patch('app.db.psycopg2.connect')  # Mock de psycopg2.connect
    def test_get_products(self, mock_connect):
        """Tester la fonction get_products"""
        # Mock de la connexion à la base de données
        mock_cursor = MagicMock()
        
        # Simuler le retour de fetchall pour les produits (avec URL d'image complète)
        mock_cursor.fetchall.return_value = [
            ('https://assets.aromes-et-liquides.fr/53645-thickbox_default/e-liquide-ultimate-ragnarok-par-al.jpg', 'Ragnarok Ultimate A&L')
        ]
        
        # Simuler le retour de la fonction fetchone pour le total_count
        mock_cursor.fetchone.return_value = [1]  # Nombre total de produits
        
        # Configurer le mock pour retourner le curseur simulé
        mock_connect.return_value.__enter__.return_value.cursor.return_value = mock_cursor

        # Appeler la fonction avec des paramètres fictifs
        produits, total_count = get_products('lime', 10, 0)

        # Vérifier les résultats
        print(produits)  # Ajouter un print pour examiner les valeurs retournées
        self.assertEqual(produits, [
            ('https://assets.aromes-et-liquides.fr/53645-thickbox_default/e-liquide-ultimate-ragnarok-par-al.jpg', 'Ragnarok Ultimate A&L')
        ])
        self.assertEqual(total_count, 1)

if __name__ == '__main__':
    unittest.main()
