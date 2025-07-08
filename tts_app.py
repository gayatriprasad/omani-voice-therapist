from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from gtts import gTTS
import uuid

app = FastAPI(title="TTS Service")


class TTSRequest(BaseModel):
    text: str


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/speak")
async def speak(payload: TTSRequest):
    tts = gTTS(payload.text)
    filename = f"tts_output_{uuid.uuid4().hex}.mp3"
    tts.save(filename)
    return FileResponse(filename, media_type="audio/mpeg", filename=filename)
