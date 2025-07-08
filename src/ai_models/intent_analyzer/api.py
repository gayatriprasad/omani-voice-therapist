from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class IntentRequest(BaseModel):
    text: str


@app.post("/analyze-intent")
def analyze_intent(req: IntentRequest):
    text = req.text.lower()
    intent = "emotional_distress" if "anxious" in text else "general_concern"
    return {
        "intent": intent,
        "emotion_state": {"anxiety_level": 5, "depression_indicators": False},
        "risk_level": "medium",
    }


@app.get("/health")
def health():
    return {"status": "ok"}
