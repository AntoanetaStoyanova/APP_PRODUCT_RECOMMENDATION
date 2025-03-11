# tests/test_azure_chat_openai.py

import pytest
from unittest.mock import patch, MagicMock
from langchain.chat_models import AzureChatOpenAI
from config import Config

# Tester la fonctionnalité d'AzureChatOpenAI
@pytest.fixture
def mock_azure_chat_openai():
    # Mock AzureChatOpenAI pour éviter de faire des appels réels à l'API Azure
    with patch.object(AzureChatOpenAI, 'invoke') as mock_invoke:
        yield mock_invoke

def test_azure_chat_openai(mock_azure_chat_openai):
    # Préparer la réponse simulée
    mock_response = "Je te recommande un liquide avec du citron."
    mock_azure_chat_openai.return_value = mock_response

    # Créer une instance du modèle LLM
    llm = AzureChatOpenAI(
        api_key=Config.AZURE_OPENAI_API_KEY,
        api_version="2023-12-01-preview",
        azure_endpoint=Config.AZURE_OPENAI_ENDPOINT,
        deployment_name=Config.AZURE_DEPLOYMENT_NAME,
        temperature=0
    )

    # Appeler la méthode invoke
    question = "Recommandes moi un liquide avec citron?"
    response = llm.invoke(question)

    # Vérifier que la méthode invoke a été appelée avec la bonne question
    mock_azure_chat_openai.assert_called_once_with(question)

    # Vérifier la réponse
    assert response == mock_response
