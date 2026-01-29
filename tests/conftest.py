"""
Configuration des tests pytest
Fixtures partagées pour tous les tests
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
import google.generativeai as genai

from app.main import app
from app.config import Settings


@pytest.fixture
def mock_settings():
    """Settings de test"""
    return Settings(
        app_name="Test Gemini API",
        app_version="1.0.0-test",
        gemini_api_key="test-api-key",
        gemini_model="gemini-2.5-flash-lite"
    )


@pytest.fixture
def client(mock_settings):
    """Client de test FastAPI"""
    with patch('app.config.get_settings', return_value=mock_settings):
        with patch('google.generativeai.configure'):
            with TestClient(app) as test_client:
                yield test_client


@pytest.fixture
def mock_gemini_response():
    """Mock d'une réponse Gemini"""
    mock_response = Mock()
    mock_response.text = "Ceci est une réponse de test de Gemini"
    mock_response.usage_metadata = Mock(
        prompt_token_count=10,
        candidates_token_count=20
    )
    return mock_response
