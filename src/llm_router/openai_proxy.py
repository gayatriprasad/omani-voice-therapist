import os
import openai
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Load environment
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env")
openai.api_key = OPENAI_API_KEY

SYSTEM_PROMPT = (
    "You are a culturally sensitive and emotionally intelligent mental health assistant. "
    "Keep responses brief, supportive, and contextually grounded."
)


class PromptInput(BaseModel):
    prompt: str


@app.post("/generate")
async def generate_response(data: PromptInput):
    return {"response": await call_gpt_response(data.prompt)}


async def call_gpt_response(prompt: str) -> str:
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=300,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("[GPT ERROR]", str(e))
        return "I'm here to support you, even if I didn’t fully understand. Could you tell me more?"


@app.get("/health")
def health_check():
    return {"status": "ok"}
