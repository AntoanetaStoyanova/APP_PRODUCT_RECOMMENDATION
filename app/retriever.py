from langchain.document_loaders import CSVLoader
from langchain_community.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
import pandas as pd
from app.embeddings import embeddings
from config import Config
from app.vectorstore import load_vectorstore, save_vectorstore
# Charger le DataFrame
df = pd.read_csv(Config.CSV_FILE_PATH)

# Charger les documents
loader = CSVLoader(file_path=Config.CSV_FILE_PATH, encoding='utf-8')
documents = loader.load()

# Configurer les embeddings et le vector store
# embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
# vectorstore = FAISS.from_documents(documents, embeddings)
# vectorstore.save_local('faiss_vector_store')

vectorstore = load_vectorstore()
# retriever = vectorstore.as_retriever(
#         search_type="similarity_score_threshold",
#         search_kwargs={"score_threshold": 0.1}
#     )
retriever = vectorstore.as_retriever(
    search_type="similarity",  # Recherche des voisins les plus proches
    search_kwargs={
        "k": 3,  # Retourne les 3 voisins les plus proches
    }
)

