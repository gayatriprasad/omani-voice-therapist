FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

COPY ./tts_app.py /app/tts_app.py

RUN pip install --no-cache-dir gTTS fastapi uvicorn

EXPOSE 8005

CMD ["uvicorn", "tts_app:app", "--host", "0.0.0.0", "--port", "8005"]
