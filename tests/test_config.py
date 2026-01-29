"""
Tests de la configuration
"""
import pytest
from pydantic import ValidationError
from app.config import Settings


def test_settings_valid():
    """Test avec des valeurs valides"""
    settings = Settings(
        app_name="Test App",
        app_version="1.0.0",
        gemini_api_key="test-key-123",
        gemini_model="gemini-2.5-flash-lite"
    )
    
    assert settings.app_name == "Test App"
    assert settings.app_version == "1.0.0"
    assert settings.gemini_api_key == "test-key-123"
    assert settings.gemini_model == "gemini-2.5-flash-lite"


def test_settings_missing_api_key():
    """Test sans clé API"""
    with pytest.raises(ValidationError) as exc_info:
        Settings(
            app_name="Test App",
            app_version="1.0.0",
            gemini_api_key="",  # Clé vide
            gemini_model="gemini-2.5-flash-lite"
        )
    
    # Vérifier que l'erreur concerne bien la clé API
    assert "gemini_api_key" in str(exc_info.value)


def test_settings_whitespace_api_key():
    """Test avec une clé API contenant seulement des espaces"""
    with pytest.raises(ValidationError) as exc_info:
        Settings(
            app_name="Test App",
            app_version="1.0.0",
            gemini_api_key="   ",  # Seulement des espaces
            gemini_model="gemini-2.5-flash-lite"
        )
    
    assert "gemini_api_key" in str(exc_info.value)


def test_settings_default_values():
    """Test des valeurs par défaut"""
    settings = Settings(
        gemini_api_key="test-key-123"
    )
    
    assert settings.app_name == "Gemini AI API"
    assert settings.app_version == "1.0.0"
    assert settings.gemini_model == "gemini-2.5-flash-lite"
    assert settings.debug is False
    assert settings.host == "0.0.0.0"
    assert settings.port == 8000


def test_settings_custom_server_config():
    """Test de configuration serveur personnalisée"""
    settings = Settings(
        gemini_api_key="test-key-123",
        debug=True,
        host="127.0.0.1",
        port=9000
    )
    
    assert settings.debug is True
    assert settings.host == "127.0.0.1"
    assert settings.port == 9000
