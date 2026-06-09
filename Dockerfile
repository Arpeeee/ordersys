# Stage 1: install Python dependencies
FROM python:3.10-slim-bookworm AS builder
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: final image with GIS system libraries
FROM python:3.10-slim-bookworm
WORKDIR /app

# GDAL, GEOS, PROJ required for django.contrib.gis (PointField)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgdal-dev \
    libgeos-dev \
    libproj-dev \
    binutils \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /install /usr/local
COPY . .

# collectstatic runs at build time — no DB connection needed
ARG SECRET_KEY=build-time-placeholder
ENV SECRET_KEY=${SECRET_KEY} \
    DEBUG=False \
    GCS_BUCKET_NAME= \
    ALLOWED_HOSTS=localhost \
    DB_NAME=placeholder \
    DB_USER=placeholder \
    DB_PASSWORD=placeholder \
    DB_HOST=placeholder \
    DB_SSLMODE=disable

RUN python manage.py collectstatic --noinput

RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "120", "coffeedb.wsgi:application"]
