from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient()
voices = client.list_voices()
for v in voices.voices:
    if "ar-XA" in v.language_codes:
        print(v.name, v.language_codes)
