# ─────────────────────────────────────────────
#  Cardinal – Dockerfile
# ─────────────────────────────────────────────

FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /Cardinal

# install deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY . .

ARG APP_NAME=moviecatalog
ENV APP_NAME=${APP_NAME}

ENTRYPOINT ["python", "run.py"]

CMD ["moviecatalog", "run"]