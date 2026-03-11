FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# NEW: Install system dependencies for SSL/TLS and Postgres
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    libssl-dev \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements/ ./requirements/
RUN pip install --upgrade pip && pip install -r requirements/prod.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Optimization: Increase timeout slightly for SMTP handshakes if not using Celery
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "90"]