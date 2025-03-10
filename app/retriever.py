from langchain.document_loaders import CSVLoader
import pandas as pd
from config import Config
from app.vectorstore import load_vectorstore
# Charger le DataFrame
df = pd.read_csv(Config.CSV_FILE_PATH)

# Charger les documents
loader = CSVLoader(file_path=Config.CSV_FILE_PATH, encoding='utf-8')
documents = loader.load()



vectorstore = load_vectorstore()

retriever = vectorstore.as_retriever(
    search_type="similarity",  # Recherche des voisins les plus proches
    search_kwargs={
        "k": 3,  # Retourne les 3 voisins les plus proches
    }
)

