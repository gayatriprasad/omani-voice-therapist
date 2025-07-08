cat > README.md << 'EOF'
# OMANI Voice Therapist MVP

## 1. Project Overview

This project delivers a functioning MVP for a real-time, voice-driven mental health support assistant. The assistant is designed to understand and respond empathetically to user speech using modular, containerized services. The current implementation focuses on English for testing, with a long-term vision of supporting Omani Arabic dialects and culturally contextual therapy-grade responses.

The goal is to validate the core speech-to-response-to-speech pipeline, enabling real-time therapeutic interactions entirely through audio. The system provides a practical baseline for expanding into multilingual, clinically informed, and culturally sensitive use cases.

## 2. Background and Motivation

Mental health services in many regions, including the Gulf, remain stigmatized or under-accessed. Voice interfaces offer a discreet, natural way to reach people in distress, especially those less comfortable with written forms of communication. This MVP explores whether a responsive and supportive agent can be built by integrating state-of-the-art STT, intent detection, and LLM-based empathy generation into a seamless voice-based experience.

The motivation extends beyond proof-of-concept: the design choices prioritize modularity, testability, and extendibility for future clinical and cultural adaptation.

## 3. System Architecture

### 3.1 Component Overview

The system comprises four independently containerized services:

- Speech-to-Text (STT): Transcribes user audio using `faster-whisper`.
- LLM Router: Sends transcribed text to GPT-based models to generate a culturally sensitive, empathetic response.
- Text-to-Speech (TTS): Converts model-generated text to natural-sounding speech using `gTTS`.
- Streamlit UI: Provides a test interface to interact with the voice loop.

Each service runs in its own container and communicates via REST endpoints.

### 3.2 Service Interactions and Flow

1. User speaks into microphone or uploads a sample audio.
2. The STT service returns a transcription, language, and segment metadata.
3. The transcription is passed to the LLM router, which generates a supportive response.
4. The response is sent to the TTS service, which produces an MP3 file.
5. The UI plays the audio back to the user.

## 4. Design Approach and Rationale

### 4.1 Technology Selection

- FastAPI was used for each microservice for its simplicity, speed, and built-in OpenAPI documentation.
- Docker Compose allowed independent service development and testing.
- faster-whisper provided a balance between speed and accuracy for transcription.
- gTTS was chosen for rapid prototyping of voice output, with a plan to evolve to an Arabic neural TTS model.
- Streamlit provided a lightweight interface for interactive roundtrip testing.

### 4.2 Microservice Modularity

Each core function (STT, LLM, TTS) runs in its own service, making it easy to swap components (e.g., Whisper → Azure STT, GPT-4 → Claude) without affecting others. This modular approach improves testability and aligns with production deployment patterns like auto-scaling and rate-limiting per service.

### 4.3 Design Tradeoffs

The MVP optimizes for clarity and maintainability rather than minimal footprint. It favors explicit REST APIs over event-driven messaging for simplicity, knowing that a message bus (e.g., Kafka) may be introduced later. TTS quality is limited to English in early stages while waiting on voice localization efforts.

## 5. Getting Started

### 5.1 Prerequisites

- Docker and Docker Compose
- A valid `OPENAI_API_KEY` from OpenAI
- Python 3.10+ (if running Streamlit or services locally)

### 5.2 Environment Setup

Create a `.env` file in the root directory:

```bash
OPENAI_API_KEY=sk-...
```

A .env.example file is provided to indicate required variables without secrets.

### 5.3 Running with Docker Compose

From the root of the project, run:

```bash
docker compose up --build
```

This will build and start the following containers:

- tts_service on port 8005
- whisper_service on port 8020
- llm_router on port 8003
- streamlit_ui on port 8501

Visit: http://localhost:8501 to begin interaction.

### 5.4 Testing the Voice Pipeline
You can also test services individually using curl:

STT
```bash
curl -X POST http://localhost:8020/transcribe \
  -F "file=@sample.wav"
```

LLM
```bash
curl -X POST http://localhost:8003/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "I feel tired"}'
```

TTS
```bash
curl -X POST http://localhost:8005/speak \
  -H "Content-Type: application/json" \
  -d '{"text": "You are not alone."}' \
  --output response.mp3
```

## 6. API Reference

### 6.1 STT Service – /transcribe
Method: POST

Form field: file (audio file)

Returns: { text: str, language: str, segments: [...] }

### 6.2 LLM Router – /generate
Method: POST

Body: { prompt: str }

Returns: { response: str }

### 6.3 TTS Service – /speak
Method: POST

Body: { text: str }

Returns: MP3 audio stream

## 7. Sample Inputs and Expected Outputs
Sample file sample.wav is included in the data/audio-samples/ folder. The system should return a transcription, generate an empathetic response, and speak it back clearly using synthesized audio.

## 8. Scaling Toward Production

### 8.1 Latency and Throughput
Each container can be individually scaled based on CPU/GPU availability. Real-time performance can be enhanced with model quantization, batch inference, or GPU-backed deployments.

### 8.2 Arabic Language and Voice Customization
Replacing gTTS with a neural Arabic TTS model will enable localized voice output. Whisper's multilingual capabilities can be tuned or swapped for fine-tuned STT models on Omani Arabic.

### 8.3 Monitoring, Logging, and Observability
Future versions will include structured logging, centralized monitoring (e.g., Prometheus), and error tracking via Sentry or OpenTelemetry.

### 8.4 Security and Data Privacy
For production, HTTPS termination, input sanitization, and PII masking will be essential. Conversations may need anonymization or audit logging to support clinical use.

## 9. Known Limitations and Next Steps

- STT performance is English-optimized in this MVP
- TTS is basic and not expressive or multilingual
- No real-time voice capture from microphone yet (uploads only)
- No user session tracking or feedback loop
- Crisis escalation and safety monitoring modules are stubbed

Next steps include:

- Incorporating Gulf Arabic STT/TTS
- Adding therapeutic intent chaining
- Deploying safety classifiers and escalation rules

## 10. Troubleshooting

- Port already in use: Adjust exposed ports in docker-compose.yml
- No response from LLM: Check if .env has valid OPENAI_API_KEY
- Audio not playing: Verify MP3 file is generated and not empty
- Docker build fails: Ensure git is installed for faster-whisper

## 11. License and Acknowledgements
This codebase is for research and prototyping purposes. It uses open-source components including faster-whisper, gTTS, and FastAPI. OpenAI APIs are governed by their own usage terms.
EOF