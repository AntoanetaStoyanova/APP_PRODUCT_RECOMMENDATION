from config import Config
from langchain_community.vectorstores import FAISS

from app.embeddings import embeddings


def load_vectorstore():
    vectorstore_path = Config.VECTORSTORE_PATH 
    return FAISS.load_local(vectorstore_path, embeddings=embeddings, allow_dangerous_deserialization=True)
    


def save_vectorstore(documents):
    vectorstore_path = Config.VECTORSTORE_PATH 
    vectorstore = FAISS.from_documents(documents, embeddings)
    vectorstore.save_local(vectorstore_path)
    return vectorstore