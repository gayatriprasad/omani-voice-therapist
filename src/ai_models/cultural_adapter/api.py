# src/ai_models/cultural_adapter/api.py

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal
import httpx
from cli_adapter import adapt_to_omani_dialect, mock_gpt_response

app = FastAPI(title="Cultural Adaptation Service", version="1.0")


class UserContext(BaseModel):
    cultural_background: Literal["omani"] = "omani"
    religiosity_level: Literal["secular", "moderate", "practicing"] = "moderate"
    honor_sensitivity: Literal["low", "high"] = "low"
    gender: Literal["male", "female"] = "male"
    family_role: Literal[
        "eldest_son", "younger_son", "eldest_daughter", "younger_daughter"
    ] = "eldest_son"


class AdaptationRequest(BaseModel):
    input_text: str
    user_context: UserContext


class AdaptationResponse(BaseModel):
    raw_response: str
    culturally_adapted_response: str


@app.get("/health")
def health_check():
    return {"status": "ok"}


async def call_intent_engine(text: str) -> dict:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:8010/analyze-intent", json={"text": text}, timeout=5.0
            )
            return response.json()
    except Exception:
        return {
            "intent": "emotional_distress",
            "emotion_state": {"anxiety_level": 5, "depression_indicators": False},
            "risk_level": "medium",
        }


@app.post("/generate", response_model=AdaptationResponse)
async def generate_response(payload: AdaptationRequest):
    raw = await mock_gpt_response(payload.input_text)
    intent = await call_intent_engine(payload.input_text)

    context = {
        **payload.user_context.dict(),
        "detected_intent": intent["intent"],
        "anxiety_level": intent["emotion_state"]["anxiety_level"],
        "risk_level": intent["risk_level"],
    }

    adapted = adapt_to_omani_dialect(raw, context)
    return AdaptationResponse(raw_response=raw, culturally_adapted_response=adapted)
