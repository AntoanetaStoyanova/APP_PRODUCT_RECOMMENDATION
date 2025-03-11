import os
from dotenv import load_dotenv, find_dotenv

# Charger les variables d'environnement
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# # Charger les variables d'environnement à partir du fichier .env
# load_dotenv(find_dotenv())

class Config:
    POSTGRESQL_URI = os.getenv('POSTGRESQL_URI', 'postgresql://postgres:Kandinsky_95@localhost:5432/postgres')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:Kandinsky_95@localhost:5432/postgres')

    # POSTGRESQL_URI = os.getenv("POSTGRESQL_URI")
    # SQLALCHEMY_DATABASE_URI = os.getenv("POSTGRESQL_URI")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY")  # Make sure this is in your .env file

    # Configuration Azure OpenAIpig
    AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY_4')
    AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_API_ENDPOINT_4')
    AZURE_DEPLOYMENT_NAME = os.getenv('AZURE_DEPLOYMENT_NAME_4')

    # Vérification stricte
    if not AZURE_OPENAI_API_KEY or not AZURE_OPENAI_ENDPOINT or not AZURE_DEPLOYMENT_NAME:
        raise ValueError("Les variables d'environnement nécessaires sont manquantes !")

    # # Autres configurations
    # CSV_FILE_PATH = "app/rag_csv.csv"
    # VECTORSTORE_PATH = "app/faiss_vector_store"
    # 🔥 Définir le chemin absolu du fichier CSV
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Récupère le dossier du projet
    CSV_FILE_PATH = os.path.join(BASE_DIR, 'app', 'rag_csv.csv')  
    VECTORSTORE_PATH = os.path.join(BASE_DIR, 'app', 'faiss_vector_store')
    # Construire le chemin absolu du fichier CSV
    RECOMMENDATIONS_CSV = os.path.join(BASE_DIR, "app", "recommendations.csv")  