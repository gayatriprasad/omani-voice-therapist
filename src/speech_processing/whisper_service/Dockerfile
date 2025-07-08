FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y git ffmpeg && apt-get clean

# Copy source code
COPY ./src/speech_processing/whisper_service /app

# Copy root requirements (assumes all services share one)
COPY ./requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8004"]
