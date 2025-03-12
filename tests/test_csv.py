import pytest
import pandas as pd
import re

@pytest.fixture
def load_data():
    # Charge les données avant chaque test
    df = pd.read_csv("app/rag_csv.csv") 
    return df

def test_no_missing_values(load_data):
    df = load_data
    # Colonnes importantes qui ne doivent pas contenir de valeurs manquantes
    important_columns = ['nom_produit', 'prix_produit', 'contenance', 'saveur', 'description', 'gout']
    
    for col in important_columns:
        assert df[col].isna().sum() == 0, f"Des valeurs manquantes ont été trouvées dans la colonne {col}"

def test_column_data_types(load_data):
    df = load_data
    # Types de données attendus pour chaque colonne
    expected_types = {
        
        'url': 'object',
        'nom_produit': 'object',
        'img_produit': 'object',
        'prix_produit': 'float64',
        'contenance': 'object',
        'pg_vg': 'object',
        'origine': 'object',
        'frais': 'object',
        'surbooste': 'object',
        'saveur': 'object',
        'description': 'object',
        'brand': 'object',
        'gout': 'object',
        'info_brand': 'object',
        'id_produit': 'int64'
    }
    for col, expected_type in expected_types.items():
        assert df[col].dtype == expected_type, f"Le type de la colonne {col} est incorrect. Attendu {expected_type}, mais obtenu {df[col].dtype}"

def test_positive_price(load_data):
    df = load_data
    assert (df['prix_produit'] >= 0).all(), "Certains prix sont négatifs dans la colonne 'prix_produit'"

def test_valid_urls(load_data):
    df = load_data
    url_pattern = re.compile(r'http[s]?://.*')
    invalid_urls = df[~df['url'].str.match(url_pattern)].shape[0]
    assert invalid_urls == 0, f"Il y a {invalid_urls} URL invalides dans la colonne 'url'"

def test_no_duplicates(load_data):
    df = load_data
    duplicate_rows = df[df.duplicated(subset=['nom_produit', 'id_produit'])]
    assert duplicate_rows.empty, f"Il y a des doublons dans les colonnes 'nom_produit' et 'id_produit': {duplicate_rows}"