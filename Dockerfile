# Basis-Image
FROM python:3.11-slim

# Git installieren
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Arbeitsverzeichnis erstellen
WORKDIR /app

# Abhängigkeiten kopieren und installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Skript kopieren
COPY script.py .

# Container-Einstiegspunkt
CMD ["python", "script.py"]
