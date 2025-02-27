import pandas as pd
import os
import psycopg2
from dotenv import load_dotenv
from pathlib import Path

# Chargement des variables d'environnement depuis le fichier .env
env_path = Path('../.env')
load_dotenv(dotenv_path=env_path)

# Paramètres de connexion à la base de données
conn_params = {
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'connect_timeout': os.getenv('DB_TIMEOUT'),
    'sslmode': os.getenv('DB_SSLMODE')
}

# Connexion à la base de données PostgreSQL
try:
    conn = psycopg2.connect(**conn_params)
    cursor = conn.cursor()
    print("Connexion à la base de données réussie.")
except Exception as e:
    print(f"Erreur de connexion : {e}")
    exit()

# Chargement du fichier CSV
df = pd.read_csv("../RGBD/table_produits/produits.csv")
replacement = {
    'int64': 'int',
    'object': 'varchar',
    'float64': 'float',
    'datetime64': 'timestamp',
    'timedelta64[ns]': 'varchar'
}

# Fonction pour générer la chaîne de colonnes et types pour la table
def generate_column_string(df, replacement):
    return ', '.join("{} {}".format(n, d) for n, d in zip(df.columns, df.dtypes.replace(replacement)))

# Exemple d'utilisation
col_str_produit = generate_column_string(df, replacement)
print(col_str_produit)

# Supprimer la table si elle existe déjà
cursor.execute("DROP TABLE IF EXISTS pdt;")

# Création de la table produits avec les colonnes spécifiées
cursor.execute(f"""
CREATE TABLE pdt (
    url VARCHAR,
    nom_produit VARCHAR,
    img_produit VARCHAR,
    prix_produit FLOAT,
    contenance VARCHAR,
    pg_vg VARCHAR,
    origine VARCHAR,
    frais VARCHAR,
    surbooste VARCHAR,
    saveur VARCHAR,
    description TEXT,
    brand VARCHAR,
    gout VARCHAR,
    info_brand TEXT,
    id_produit SERIAL PRIMARY KEY
);
""")
print("Table pdt créée.")

# Ouverture du fichier CSV pour insérer les données dans la table
with open('../RGBD/table_produits/produits.csv', 'r') as my_file:
    print('File opened in memory')

    # SQL pour insérer les données dans la table
    SQL_STATEMENT_PRODUITS = """
    COPY pdt FROM STDIN WITH
        CSV
        HEADER
        DELIMITER AS ','
        QUOTE '"'
    """
    cursor.copy_expert(sql=SQL_STATEMENT_PRODUITS, file=my_file)
    print('Fichier copié dans la base de données.')

# Fermer la connexion à la base de données
conn.commit()
cursor.close()
conn.close()
print("Connexion fermée.")

