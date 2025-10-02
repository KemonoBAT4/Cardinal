FROM python:3.13-slim

WORKDIR /app

# Aggiorna pip e pacchetti base
RUN pip install --upgrade pip setuptools wheel psutil

LABEL maintainer="kemono.bat.4@gmail.com"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiamo il core (riutilizzabile per tutte le app)
COPY core /core
COPY run.py /app/run.py

# CMD ["python", "run.py"]

