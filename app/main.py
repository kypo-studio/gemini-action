"""
Point d'entrée principal de l'API FastAPI
Gère le cycle de vie de l'application et configure Gemini
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import google.generativeai as genai

from app.config import get_settings
from app.routes import gemini

# Charger la configuration
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gère le cycle de vie de l'application
    - Startup : Configuration de Gemini
    - Shutdown : Nettoyage des ressources
    """
    # STARTUP
    print(f"🚀 Démarrage de {settings.app_name} v{settings.app_version}")
    
    # Configurer l'API Gemini
    genai.configure(api_key=settings.gemini_api_key)
    
    # Stocker le nom du modèle dans le routeur
    gemini.router.model_name = settings.gemini_model
    
    print(f"✅ Gemini configuré avec le modèle : {settings.gemini_model}")
    
    yield
    
    # SHUTDOWN
    print("🛑 Arrêt de l'application")


# Créer l'application FastAPI
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API REST pour interagir avec Google Gemini AI",
    lifespan=lifespan
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enregistrer les routes
app.include_router(gemini.router)


@app.get("/", tags=["Health"])
async def root():
    """Page d'accueil de l'API"""
    return {
        "message": f"Bienvenue sur {settings.app_name}",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Endpoint de vérification de santé"""
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version,
        "model": settings.gemini_model
    }
