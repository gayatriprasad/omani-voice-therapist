import pytest
from httpx import AsyncClient, ASGITransport
from src.speech_processing.whisper_service.api import app

transport = ASGITransport(app=app)


@pytest.mark.asyncio
async def test_transcription_endpoint():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        with open("sample.wav", "rb") as f:
            response = await ac.post(
                "/transcribe", files={"file": ("sample.wav", f, "audio/wav")}
            )
        assert response.status_code == 200
        body = response.json()
        assert "text" in body
        assert isinstance(body["text"], str)
