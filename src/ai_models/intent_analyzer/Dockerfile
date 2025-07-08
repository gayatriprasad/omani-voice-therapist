FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install git (if future dependencies need it) and pip deps
RUN apt-get update && apt-get install -y git && apt-get clean

# Copy source code
COPY ./src/ai_models/intent_analyzer /app

# Install requirements (inline for now, or you can create requirements.txt)
RUN pip install --no-cache-dir fastapi uvicorn pydantic

# Expose port
EXPOSE 8001

# Run app
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8001"]
