FROM python:3.10-slim

# Set workdir
WORKDIR /app

# Copy only what we need
COPY ./src/llm_router /app
COPY ./requirements.txt /app

# 🔧 Add git (needed for faster-whisper or any git-based installs)
RUN apt-get update && apt-get install -y git && apt-get clean

# Install deps
RUN pip install --no-cache-dir -r requirements.txt

# Set OpenAI env var (docker-compose overrides this in prod)
ENV OPENAI_API_KEY=""

EXPOSE 8000

CMD ["uvicorn", "openai_proxy:app", "--host", "0.0.0.0", "--port", "8003"]
