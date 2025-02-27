from langchain.chat_models import AzureChatOpenAI

import sys
import os

# Ajouter le dossier parent au chemin pour pouvoir importer config.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import Config


llm = AzureChatOpenAI(
    api_key=Config.AZURE_OPENAI_API_KEY,  # Clé API Azure depuis la configuration
    api_version="2023-12-01-preview",  # Version de l'API (ajuste-la si nécessaire)
    azure_endpoint=Config.AZURE_OPENAI_ENDPOINT,  # Endpoint Azure depuis la configuration
    deployment_name=Config.AZURE_DEPLOYMENT_NAME,  # Nom du déploiement depuis la configuration
    temperature=0  # Optionnel : Ajuste la température pour la variabilité des réponses
)

# Test de fonctionnement du LLM (optionnel)
if __name__ == "__main__":
    try:
        response = llm.invoke("Recommandes moi un liquide avec citron?")
        print("Réponse du LLM :", response)
    except Exception as e:
        print("Erreur lors de l'invocation du LLM :", e)