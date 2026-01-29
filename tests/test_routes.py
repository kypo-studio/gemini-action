"""
Tests des routes de l'API
"""
import pytest
from unittest.mock import patch, Mock


def test_root_endpoint(client):
    """Test de la page d'accueil"""
    response = client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["docs"] == "/docs"


def test_health_check(client):
    """Test du health check"""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "app" in data
    assert "version" in data
    assert "model" in data


def test_generate_text_success(client, mock_gemini_response):
    """Test de génération de texte réussie"""
    with patch('google.generativeai.GenerativeModel') as mock_model:
        # Configurer le mock
        mock_instance = Mock()
        mock_instance.generate_content.return_value = mock_gemini_response
        mock_model.return_value = mock_instance
        
        # Faire la requête
        response = client.post(
            "/gemini/generate",
            json={
                "prompt": "Test prompt",
                "temperature": 0.7,
                "max_tokens": 1000
            }
        )
        
        # Vérifications
        assert response.status_code == 200
        data = response.json()
        assert "response" in data
        assert "model" in data
        assert data["prompt_tokens"] == 10
        assert data["completion_tokens"] == 20


def test_generate_text_missing_prompt(client):
    """Test sans prompt"""
    response = client.post(
        "/gemini/generate",
        json={}
    )
    
    assert response.status_code == 422  # Validation error


def test_generate_text_invalid_temperature(client):
    """Test avec température invalide"""
    response = client.post(
        "/gemini/generate",
        json={
            "prompt": "Test",
            "temperature": 2.0  # > 1.0
        }
    )
    
    assert response.status_code == 422


def test_generate_text_api_error(client):
    """Test d'erreur de l'API Gemini"""
    with patch('google.generativeai.GenerativeModel') as mock_model:
        mock_instance = Mock()
        mock_instance.generate_content.side_effect = Exception("API Error")
        mock_model.return_value = mock_instance
        
        response = client.post(
            "/gemini/generate",
            json={"prompt": "Test"}
        )
        
        assert response.status_code == 500
        assert "Erreur lors de la génération" in response.json()["detail"]


def test_list_models_success(client):
    """Test de la liste des modèles"""
    with patch('google.generativeai.list_models') as mock_list:
        # Mock de la réponse
        mock_model = Mock()
        mock_model.name = "models/gemini-2.5-flash-lite"
        mock_model.display_name = "Gemini 2.5 Flash Lite"
        mock_model.description = "Fast and efficient"
        mock_model.supported_generation_methods = ["generateContent"]
        
        mock_list.return_value = [mock_model]
        
        response = client.get("/gemini/models")
        
        assert response.status_code == 200
        data = response.json()
        assert "models" in data
        assert len(data["models"]) > 0
        assert data["models"][0]["name"] == "models/gemini-2.5-flash-lite"
