# src/speech_processing/whisper_service/transcriber.py

from faster_whisper import WhisperModel

# Use base model; adjust to "medium" or "large-v2" if needed
model = WhisperModel("base", compute_type="auto")


def transcribe_audio(audio_bytes: bytes) -> dict:
    import tempfile

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as tmp:
        tmp.write(audio_bytes)
        tmp.flush()

        segments, info = model.transcribe(tmp.name, beam_size=5)

        text_segments = [seg.text for seg in segments]
        return {
            "text": " ".join(text_segments),
            "language": info.language,
            "segments": text_segments,
        }
