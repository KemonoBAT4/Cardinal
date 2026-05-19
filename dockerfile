FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG APP_NAME
ENV APP_NAME=${APP_NAME}

# default command
ENTRYPOINT ["python", "run.py"]

# default args (fallback)
CMD ["moviecatalog", "run"]