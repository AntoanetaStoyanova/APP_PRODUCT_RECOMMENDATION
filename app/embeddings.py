# from langchain.embeddings import HuggingFaceEmbeddings
from langchain_openai import AzureOpenAIEmbeddings


import sys
import os

# Ajouter le dossier parent au chemin pour pouvoir importer config.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import Config





# embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


embeddings = AzureOpenAIEmbeddings(openai_api_key=Config.AZURE_OPENAI_API_KEY,
                                    azure_deployment='text-embedding-3-large',
                                    azure_endpoint=Config.AZURE_OPENAI_ENDPOINT,
                                    openai_api_version="2023-05-15",
                                    chunk_size=500
)