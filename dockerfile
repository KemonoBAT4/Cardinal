


FROM python:3.13-slim

# Imposta la working dir principale
WORKDIR /app

# Installa dipendenze di base
RUN pip install --upgrade pip setuptools wheel psutil

LABEL maintainer="kemono.bat.4@gmail.com"

# Copia tutto ciò che serve (core, run.py, requirements)
COPY requirements.txt .
COPY core ./core
COPY run.py ./run.py
COPY run.sh ./run.sh
COPY application.cfg ./application.cfg
COPY cardinal.log ./cardinal.log
COPY requirements.txt ./requirements.txt
COPY setup.sh ./setup.sh
COPY cleanup.sh ./cleanup.sh

# Installa le librerie Python
RUN pip install --no-cache-dir -r requirements.txt

# Imposta il PYTHONPATH in modo che includa /app
# ENV PYTHONPATH="/app:${PYTHONPATH}"
ENV PYTHONPATH="/app:${PYTHONPATH}"

# Comando di default (sovrascrivibile dal docker-compose)
# CMD ["python", "run.py"]
