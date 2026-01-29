"""
Configuration de l'application avec gestion des variables d'environnement
"""
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration de l'application"""
    
    # Informations de l'application
    app_name: str = "Gemini AI API"
    app_version: str = "1.0.0"
    
    # Configuration Gemini
    gemini_api_key: str = Field(..., min_length=1)
    gemini_model: str = "gemini-2.5-flash-lite"
    
    # Configuration serveur (optionnelles, ignorées si absentes)
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    
    # ✅ Configuration Pydantic v2
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore"  # Ignore les champs inconnus du .env
    )
    
    @field_validator('gemini_api_key')
    @classmethod
    def validate_api_key(cls, v: str) -> str:
        """Valide que la clé API n'est pas vide"""
        if not v or not v.strip():
            raise ValueError("La clé API Gemini ne peut pas être vide")
        return v


def get_settings() -> Settings:
    """Factory pour obtenir les settings"""
    return Settings()


# Test de configuration
if __name__ == "__main__":
    settings = get_settings()
    print(f"\n✅ Configuration chargée :")
    print(f"   - App: {settings.app_name} v{settings.app_version}")
    print(f"   - Model: {settings.gemini_model}")
    print(f"   - API Key: ***{settings.gemini_api_key[-4:]}")
    print(f"   - Debug: {settings.debug}")
    print(f"   - Host: {settings.host}:{settings.port}")
