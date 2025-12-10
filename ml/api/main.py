from typing import Any, Dict, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from ml.prompt_templates import PitchDeckPromptConfig
from ml.models.baseline import generate_deck, regenerate_slide


app = FastAPI(title="AI Pitch Deck Generator API", version="0.1.0")


class Slide(BaseModel):
    id: int
    section: str
    title: str
    bullets: List[str]


class GenerateDeckRequest(BaseModel):
    brief: str = Field(..., description="Описание стартапа на английском")
    target_slide_count: int = 10
    tone: str = "formal"
    audience: str = "early-stage VC"
    language: str = "en"


class GenerateDeckResponse(BaseModel):
    slides: List[Slide]


class RegenerateSlideRequest(BaseModel):
    brief: str
    existing_deck: Dict[str, Any] = Field(..., description="JSON дека (как возвращает /generate_deck)")
    slide_id: int
    tone: str = "formal"
    audience: str = "early-stage VC"
    language: str = "en"


class RegenerateSlideResponse(Slide):
    pass


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/generate_deck", response_model=GenerateDeckResponse)
def generate_deck_endpoint(req: GenerateDeckRequest) -> Dict[str, Any]:
    config = PitchDeckPromptConfig(
        target_slide_count=req.target_slide_count,
        tone=req.tone,
        audience=req.audience,
        language=req.language,
    )
    try:
        deck = generate_deck(brief=req.brief, config=config)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return deck


@app.post("/regenerate_slide", response_model=RegenerateSlideResponse)
def regenerate_slide_endpoint(req: RegenerateSlideRequest) -> Dict[str, Any]:
    config = PitchDeckPromptConfig(
        target_slide_count=len(req.existing_deck.get("slides", []) or []),
        tone=req.tone,
        audience=req.audience,
        language=req.language,
    )
    try:
        slide = regenerate_slide(
            brief=req.brief,
            existing_deck=req.existing_deck,
            slide_id=req.slide_id,
            config=config,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return slide
