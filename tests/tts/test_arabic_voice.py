import os
from src.speech_processing.tts_service import synthesize_arabic_tts


def test_generate_arabic_tts():
    out_path = "test_tts.mp3"
    synthesize_arabic_tts("مرحبا بك", filename=out_path)
    assert os.path.exists(out_path)
    assert os.path.getsize(out_path) > 1000
    os.remove(out_path)
