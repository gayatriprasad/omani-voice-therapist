# src/ai_models/cultural_adapter/cli_adapter.py

from typing import Dict
from llm_router.openai_proxy import call_gpt_response


def adapt_to_omani_dialect(gpt_response: str, context: Dict) -> str:
    gender = context.get("gender")
    honor = context.get("honor_sensitivity")
    religiosity = context.get("religiosity_level")
    risk = context.get("risk_level")

    adapted = gpt_response

    if religiosity == "practicing":
        adapted += " Insha’Allah, things will get better."
    if honor == "high" and context.get("family_role") == "eldest_son":
        adapted = f"As the eldest, your strength matters. {adapted}"
    if gender == "female" and context.get("family_role") == "eldest_daughter":
        adapted = f"Your voice matters, even in silence. {adapted}"
    if risk == "high":
        adapted += " You're not alone — would you like to speak to someone directly?"

    return adapted


async def mock_gpt_response(text: str) -> str:
    return await call_gpt_response(text)
