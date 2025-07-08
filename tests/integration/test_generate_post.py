import pytest
import requests


@pytest.mark.skip(reason="Requires running service on http://localhost:8000")
def test_post_to_generate_returns_expected_fields():
    payload = {
        "input_text": "I feel overwhelmed",
        "user_context": {
            "cultural_background": "omani",
            "religiosity_level": "moderate",
            "honor_sensitivity": "high",
            "gender": "female",
            "family_role": "eldest_daughter",
        },
    }
    response = requests.post("http://localhost:8000/generate", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert "raw_response" in body
    assert "culturally_adapted_response" in body
