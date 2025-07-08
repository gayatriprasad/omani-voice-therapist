import pytest
from httpx import AsyncClient, ASGITransport
from src.ai_models.intent_analyzer.api import app

transport = ASGITransport(app=app)


@pytest.mark.asyncio
async def test_detect_emotional_intent():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/intent", json={"text": "I feel overwhelmed and sad"})
        assert response.status_code == 200
        body = response.json()
        assert "intent" in body
        assert isinstance(body["intent"], str)
