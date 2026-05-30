# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Abhängigkeiten installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Den Code kopieren
COPY . .

# FastAPI auf Port 8000 starten
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]