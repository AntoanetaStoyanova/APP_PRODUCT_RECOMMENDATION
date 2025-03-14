# llm_connection.py

from langchain.chat_models import AzureChatOpenAI
from config import Config
import logging

# Configurer le logging
logging.basicConfig(filename='logs/llm_connection.log', level=logging.INFO)

# Fonction pour obtenir la connexion Azure OpenAI
def get_llm_connection():
    try:
        llm = AzureChatOpenAI(
            api_key=Config.AZURE_OPENAI_API_KEY,
            api_version="2023-12-01-preview",
            azure_endpoint=Config.AZURE_OPENAI_ENDPOINT,
            deployment_name=Config.AZURE_DEPLOYMENT_NAME,
            temperature=0
        )
        # Test de la connexion avec une simple requête
        response = llm.invoke("Recommandes moi un liquide avec citron?")
        logging.info(f"Réponse du modèle : {response}")
        return llm
    except Exception as e:
        logging.error(f"Erreur lors de la connexion à Azure OpenAI: {e}")
        return None
