import pytest
from httpx import AsyncClient, ASGITransport
from src.ai_models.cultural_adapter.api import app

transport = ASGITransport(app=app)


@pytest.mark.asyncio
async def test_generate_basic_low_risk():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {
            "input_text": "I'm just a bit stressed about work.",
            "user_context": {
                "cultural_background": "omani",
                "religiosity_level": "moderate",
                "honor_sensitivity": "low",
                "gender": "male",
                "family_role": "eldest_son",
            },
        }
        response = await ac.post("/generate", json=payload)
        assert response.status_code == 200
        body = response.json()
        assert "raw_response" in body
        assert "culturally_adapted_response" in body


@pytest.mark.asyncio
async def test_generate_high_risk_case():
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {
            "input_text": "I feel hopeless and I don’t want to live anymore.",
            "user_context": {
                "cultural_background": "omani",
                "religiosity_level": "practicing",
                "honor_sensitivity": "high",
                "gender": "female",
                "family_role": "eldest_daughter",
            },
        }
        response = await ac.post("/generate", json=payload)
        assert response.status_code == 200
        body = response.json()
        assert "culturally_adapted_response" in body
        assert (
            "Allah" in body["culturally_adapted_response"]
            or "الله" in body["culturally_adapted_response"]
        )
