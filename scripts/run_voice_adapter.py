# scripts/run_voice_adapter.py

import sys
import httpx
import json

STT_URL = "http://localhost:8020/transcribe"
ADAPTER_URL = "http://localhost:8000/generate"

DEFAULT_CONTEXT = {
    "cultural_background": "omani",
    "religiosity_level": "moderate",
    "honor_sensitivity": "high",
    "gender": "male",
    "family_role": "eldest_son",
}


async def run_pipeline(audio_path: str):
    print(f"[INFO] Uploading audio: {audio_path}")
    async with httpx.AsyncClient() as client:
        try:
            with open(audio_path, "rb") as f:
                stt_resp = await client.post(
                    STT_URL, files={"file": (audio_path, f, "audio/wav")}, timeout=30.0
                )
            stt_data = stt_resp.json()
            print(f"[INFO] Transcription: {stt_data['text']}")
        except Exception as e:
            print("[ERROR] STT failed:", e)
            return

        try:
            gen_resp = await client.post(
                ADAPTER_URL,
                json={"input_text": stt_data["text"], "user_context": DEFAULT_CONTEXT},
                timeout=30.0,
            )
            gen_data = gen_resp.json()
            print("\n[✅ RAW GPT-4o]:", gen_data["raw_response"])
            print("[🎯 Adapted]:", gen_data["culturally_adapted_response"])
        except Exception as e:
            print("[ERROR] Cultural adapter failed:", e)


if __name__ == "__main__":
    import asyncio

    if len(sys.argv) != 2:
        print("Usage: python scripts/run_voice_adapter.py sample.wav")
    else:
        asyncio.run(run_pipeline(sys.argv[1]))
