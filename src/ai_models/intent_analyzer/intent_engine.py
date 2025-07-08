from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal, Optional
import re

app = FastAPI(title="Intent Analysis Engine", version="0.1.0")


# Request
class IntentRequest(BaseModel):
    text: str


# Response models
class EmotionState(BaseModel):
    anxiety_level: int  # scale 1–10
    depression_indicators: bool


class CulturalContext(BaseModel):
    mentions_family_duty: bool
    gender_specific_concern: Optional[str]


class IntentResponse(BaseModel):
    intent: str
    emotion_state: EmotionState
    cultural_context: CulturalContext
    risk_level: Literal["low", "medium", "high"]


# Heuristic Rules
INTENT_PATTERNS = {
    "crisis_situation": [r"(suicide|kill myself|end it all)"],
    "family_issues": [r"(father|mother|pressure|expectations|marriage)"],
    "relationship_concerns": [r"(partner|love|divorce|boyfriend|girlfriend)"],
    "work_stress": [r"(boss|job|colleagues|burnout|deadlines)"],
    "greeting": [r"(hello|hi|assalamu)"],
}


def detect_intent(text: str) -> str:
    text = text.lower()
    for label, patterns in INTENT_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text):
                return label
    return "emotional_distress"


def analyze_emotion(text: str) -> EmotionState:
    anxiety = sum(w in text.lower() for w in ["worried", "anxious", "nervous", "panic"])
    depressed = any(w in text.lower() for w in ["worthless", "hopeless", "empty"])
    return EmotionState(
        anxiety_level=min(10, 3 + anxiety * 2), depression_indicators=depressed
    )


def extract_context(text: str) -> CulturalContext:
    has_duty = bool(
        re.search(r"(duty|honor|obligation|responsibility)", text, re.IGNORECASE)
    )
    if re.search(r"(man|son|husband)", text):
        g = "male_role_expectation"
    elif re.search(r"(woman|daughter|wife)", text):
        g = "female_role_conflict"
    else:
        g = None
    return CulturalContext(mentions_family_duty=has_duty, gender_specific_concern=g)


def determine_risk(intent: str, emotion: EmotionState) -> str:
    if intent == "crisis_situation" or emotion.depression_indicators:
        return "high"
    if emotion.anxiety_level >= 7:
        return "medium"
    return "low"


@app.post("/analyze-intent", response_model=IntentResponse)
def analyze(payload: IntentRequest):
    intent = detect_intent(payload.text)
    emotion = analyze_emotion(payload.text)
    context = extract_context(payload.text)
    risk = determine_risk(intent, emotion)
    return IntentResponse(
        intent=intent,
        emotion_state=emotion,
        cultural_context=context,
        risk_level=risk,
    )
