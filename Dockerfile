FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Copy the entire requirements folder
COPY requirements/ ./requirements/

# Install prod dependencies
RUN pip install --upgrade pip && pip install -r requirements/prod.txt

# Copy project files
COPY . .

# Collect static files if using Django static
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "hope_begins_api.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]