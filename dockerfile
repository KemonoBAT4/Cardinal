FROM python:3.13-slim

# Aggiorna pip e pacchetti base
RUN pip install --upgrade pip setuptools wheel psutil

LABEL maintainer="kemono.bat.4@gmail.com"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# CMD ["python", "run.py"]
