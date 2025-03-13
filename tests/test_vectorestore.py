# # test sur save_vectorstore et load_vectorstore
# import pytest
# from unittest.mock import patch, MagicMock
# from app.vectorstore import load_vectorstore, save_vectorstore
# from config import Config
# from langchain_community.vectorstores import FAISS
# from app.embeddings import embeddings

# @pytest.fixture
# def mock_load_local():
#     with patch.object(FAISS, 'load_local') as mock_load_local:
#         yield mock_load_local

# def test_load_vectorstore(mock_load_local):
#     # Préparer le mock pour load_local
#     mock_vectorstore = MagicMock()
#     mock_load_local.return_value = mock_vectorstore

#     # Appeler la fonction load_vectorstore
#     vectorstore = load_vectorstore()

#     # Vérifier que load_local a été appelé avec les bons paramètres
#     mock_load_local.assert_called_once_with(Config.VECTORSTORE_PATH, embeddings=embeddings, allow_dangerous_deserialization=True)

#     # Vérifier que la fonction retourne bien le mock du vectorstore
#     assert vectorstore == mock_vectorstore


# @pytest.fixture
# def mock_from_documents_and_save_local():
#     with patch('app.vectorstore.FAISS.from_documents') as mock_from_documents, \
#          patch('app.vectorstore.FAISS.save_local') as mock_save_local:
#         yield mock_from_documents, mock_save_local

# def test_save_vectorstore(mock_from_documents_and_save_local):
#     mock_from_documents, mock_save_local = mock_from_documents_and_save_local

#     # Préparer les documents mockés et le mock du vectorstore
#     mock_documents = ['doc1', 'doc2']
#     mock_vectorstore = MagicMock()
#     mock_from_documents.return_value = mock_vectorstore

#     # Appeler la fonction save_vectorstore
#     vectorstore = save_vectorstore(mock_documents)

#     # Vérifier que from_documents a été appelé avec les bons paramètres
#     mock_from_documents.assert_called_once_with(mock_documents, embeddings)

#     # Vérifier que save_local a été appelé sur le vectorstore
#     mock_vectorstore.save_local.assert_called_once_with(Config.VECTORSTORE_PATH)

#     # Vérifier que la fonction retourne le vectorstore
#     assert vectorstore == mock_vectorstore



import pytest
from unittest.mock import patch, MagicMock
from app.vectorstore import load_vectorstore, save_vectorstore
from config import Config
from langchain_community.vectorstores import FAISS
from app.embeddings import embeddings

# Fixture pour mocker le chargement local du vectorstore
@pytest.fixture
def mock_load_local():
    with patch.object(FAISS, 'load_local') as mock_load_local:
        yield mock_load_local

def test_load_vectorstore(mock_load_local):
    # Préparer le mock pour load_local
    mock_vectorstore = MagicMock()
    mock_load_local.return_value = mock_vectorstore

    # Appeler la fonction load_vectorstore
    vectorstore = load_vectorstore()

    # Vérifier que load_local a été appelé avec les bons paramètres
    mock_load_local.assert_called_once_with(Config.VECTORSTORE_PATH, embeddings=embeddings, allow_dangerous_deserialization=True)

    # Vérifier que la fonction retourne bien le mock du vectorstore
    assert vectorstore == mock_vectorstore


# Fixture pour mocker la création et la sauvegarde du vectorstore
@pytest.fixture
def mock_from_documents_and_save_local():
    with patch('app.vectorstore.FAISS.from_documents') as mock_from_documents, \
         patch('app.vectorstore.FAISS.save_local') as mock_save_local:
        yield mock_from_documents, mock_save_local

def test_save_vectorstore(mock_from_documents_and_save_local):
    mock_from_documents, mock_save_local = mock_from_documents_and_save_local

    # Préparer les documents mockés et le mock du vectorstore
    mock_documents = ['doc1', 'doc2']
    mock_vectorstore = MagicMock()
    mock_from_documents.return_value = mock_vectorstore

    # Appeler la fonction save_vectorstore
    vectorstore = save_vectorstore(mock_documents)

    # Vérifier que from_documents a été appelé avec les bons paramètres
    mock_from_documents.assert_called_once_with(mock_documents, embeddings)

    # Vérifier que save_local a été appelé sur le vectorstore
    mock_vectorstore.save_local.assert_called_once_with(Config.VECTORSTORE_PATH)

    # Vérifier que la fonction retourne le vectorstore
    assert vectorstore == mock_vectorstore

    # Ajouter un test d'erreur pour simuler une exception sur save_local
    mock_vectorstore.save_local.side_effect = Exception("Erreur de sauvegarde")
    with pytest.raises(Exception, match="Erreur de sauvegarde"):
        save_vectorstore(mock_documents)
