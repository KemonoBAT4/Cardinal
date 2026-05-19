# TODO: make the dockerfile for the modular application

# ─────────────────────────────────────────────
#  Cardinal – Generic Dockerfile
#  Build: docker build --build-arg APP_NAME=moviecatalog .
# ─────────────────────────────────────────────

FROM python:3.11-slim

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /Cardinal

# Install Python deps first (layer cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# The app to run is passed at build time and baked as ENV
ARG APP_NAME
ENV APP_NAME=${APP_NAME}

EXPOSE 5000

CMD ["sh", "-c", "python run.py ${APP_NAME} run"]