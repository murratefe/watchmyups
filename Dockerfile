FROM python:3.12.3-slim

LABEL org.opencontainers.image.title="watchmyups" \
      org.opencontainers.image.description="WatchMyUPS - A FastAPI application to expose data from UPS devices via NUT" \
      org.opencontainers.image.source="https://github.com/murratefe/watchmyups" \
      org.opencontainers.image.url="https://github.com/murratefe/watchmyups" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.licenses="GPL-3.0" \
      maintainer="Murat EFE"



WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
COPY LICENSE .

COPY src/watchmyups ./src/watchmyups

RUN pip install --no-cache-dir .

EXPOSE 9999

CMD ["python", "-m", "watchmyups", "--docker_mode"]
