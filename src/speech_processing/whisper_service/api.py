# src/speech_processing/whisper_service/api.py

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from transcriber import transcribe_audio

app = FastAPI(title="STT Service", version="1.0")


class TranscriptionResponse(BaseModel):
    text: str
    language: str
    segments: list[str]


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe(file: UploadFile = File(...)):
    content = await file.read()
    result = transcribe_audio(content)
    return result
