FROM python:3.10-slim

WORKDIR /app

COPY ./src/ai_models/cultural_adapter /app
COPY ./src/llm_router /app/llm_router
COPY ./src/ai_models/intent_analyzer /app/intent_analyzer
COPY ./src/llm_router/openai_proxy.py /app/llm_router/openai_proxy.py
COPY ./requirements.txt /app

RUN apt-get update && apt-get install -y git && apt-get clean
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
