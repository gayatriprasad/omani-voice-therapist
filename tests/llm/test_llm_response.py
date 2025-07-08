import pytest
from httpx import AsyncClient, ASGITransport
from src.llm_router.openai_proxy import app

transport = ASGITransport(app=app)


@pytest.mark.asyncio
async def test_llm_returns_response():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/generate", json={"prompt": "How do I handle anxiety?"}
        )
        assert response.status_code == 200
        body = response.json()
        assert "response" in body
        assert isinstance(body["response"], str)
