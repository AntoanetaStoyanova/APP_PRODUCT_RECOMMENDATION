
import os
from dotenv import load_dotenv

# Charger les variables de .env
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

class Config:
    # Récupérer l'URL de connexion à la base de données depuis les variables d'environnement
    POSTGRESQL_URI = os.getenv('POSTGRESQL_URI')
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SECRET_KEY = os.getenv("SECRET_KEY")  
    SQLALCHEMY_TRACK_MODIFICATIONS = False
 
    # Configuration Azure OpenAIpig
    AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY_4')
    AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_API_ENDPOINT_4')
    AZURE_DEPLOYMENT_NAME = os.getenv('AZURE_DEPLOYMENT_NAME_4')

    # Vérification stricte
    if not AZURE_OPENAI_API_KEY or not AZURE_OPENAI_ENDPOINT or not AZURE_DEPLOYMENT_NAME:
        raise ValueError("Les variables d'environnement nécessaires sont manquantes !")

    # # Autres configurations
    
    # 🔥 Définir le chemin absolu du fichier CSV
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Récupère le dossier du projet
    CSV_FILE_PATH = os.path.join(BASE_DIR, 'app', 'rag_csv.csv')  
    VECTORSTORE_PATH = os.path.join(BASE_DIR, 'app', 'faiss_vector_store')
    # Construire le chemin absolu du fichier CSV
    RECOMMENDATIONS_CSV = os.path.join(BASE_DIR, "app", "recommendations.csv")  
    RAG_EVAL_MONITORING_CSV = os.path.join(BASE_DIR, "app", "rag_eval", "monitoring.csv")

    LANGFUSE_SECRET_KEY= os.getenv('LANGFUSE_SECRET_KEY')
    LANGFUSE_PUBLIC_KEY= os.getenv('LANGFUSE_PUBLIC_KEY')
    LANGFUSE_HOST= os.getenv('LANGFUSE_HOST')