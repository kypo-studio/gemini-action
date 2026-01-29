"""
Routes pour l'interaction avec l'API Gemini
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import google.generativeai as genai

# Créer le routeur
router = APIRouter(prefix="/gemini", tags=["Gemini AI"])


# Modèles de données
class PromptRequest(BaseModel):
    """Structure de la requête"""
    prompt: str = Field(..., min_length=1, max_length=5000, description="Texte à envoyer à Gemini")
    temperature: Optional[float] = Field(0.7, ge=0.0, le=1.0, description="Créativité (0=précis, 1=créatif)")
    max_tokens: Optional[int] = Field(1000, ge=1, le=8000, description="Nombre maximum de tokens")


class PromptResponse(BaseModel):
    """Structure de la réponse"""
    response: str
    model: str
    prompt_tokens: int
    completion_tokens: int


@router.post("/generate", response_model=PromptResponse, summary="Générer une réponse avec Gemini")
async def generate_text(request: PromptRequest):
    """
    Envoie un prompt à Gemini et retourne la réponse générée
    
    - **prompt**: Le texte à envoyer à l'IA
    - **temperature**: Niveau de créativité (0.0 à 1.0)
    - **max_tokens**: Longueur maximale de la réponse
    """
    try:
        # Récupérer le modèle configuré
        model = genai.GenerativeModel(router.model_name)
        
        # Générer la réponse
        response = model.generate_content(
            request.prompt,
            generation_config=genai.GenerationConfig(
                temperature=request.temperature,
                max_output_tokens=request.max_tokens,
            )
        )
        
        # Extraire les informations
        return PromptResponse(
            response=response.text,
            model=router.model_name,
            prompt_tokens=response.usage_metadata.prompt_token_count,
            completion_tokens=response.usage_metadata.candidates_token_count
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la génération : {str(e)}"
        )


@router.get("/models", summary="Lister les modèles disponibles")
async def list_models():
    """
    Retourne la liste des modèles Gemini disponibles
    """
    try:
        models = genai.list_models()
        return {
            "models": [
                {
                    "name": model.name,
                    "display_name": model.display_name,
                    "description": model.description
                }
                for model in models
                if "generateContent" in model.supported_generation_methods
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération des modèles : {str(e)}"
        )
