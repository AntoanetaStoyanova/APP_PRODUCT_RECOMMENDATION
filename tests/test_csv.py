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

def test_valid_urls(load_data):
    df = load_data
    url_pattern = re.compile(r'http[s]?://.*')
    invalid_urls = df[~df['url'].str.match(url_pattern)].shape[0]
    assert invalid_urls == 0, f"Il y a {invalid_urls} URL invalides dans la colonne 'url'"

def test_no_duplicates(load_data):
    df = load_data
    duplicate_rows = df[df.duplicated(subset=['nom_produit', 'id_produit'])]
    assert duplicate_rows.empty, f"Il y a des doublons dans les colonnes 'nom_produit' et 'id_produit': {duplicate_rows}"