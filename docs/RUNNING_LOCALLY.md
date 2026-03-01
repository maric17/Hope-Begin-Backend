# Running Hope Begins Backend Locally

This guide explains how to set up and run the Hope Begins Django backend on your local machine.

## Prerequisites

- **Python 3.10+**
- **Redis**: Required as a message broker for Celery.
  - **Option A (Docker)**: `docker run -d -p 6379:6379 redis`
  - **Option B (Native)**: Install Redis on your OS and ensure it's running on port `6379`.
- **PostgreSQL**: A database is required (e.g., Supabase or local Postgres).

---

## 1. Setup Virtual Environment

If you haven't already, create and activate the virtual environment:

```powershell
# Create venv
python -m venv venv

# Activate on Windows
.\venv\Scripts\activate
```

## 2. Install Dependencies

Ensure all required packages are installed in your virtual environment:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements/base.txt
```

## 3. Environment Configuration

Copy the example environment file and fill in your values:

```powershell
cp .env.example .env
```

Key variables to check:
- `DATABASE_URL`: Your PostgreSQL connection string.
- `CELERY_BROKER_URL`: `redis://localhost:6379/0`
- `EMAIL_HOST`, `EMAIL_PORT`, etc. (for SMTP emails).

## 4. Database Migrations

Apply the database schema:

```powershell
.\venv\Scripts\python.exe manage.py migrate
```

---

## 5. Starting the Services

To run the full backend, you need **three** separate terminal windows or background processes:

### Terminal 1: Django API Server (Port 3003)
Runs the main web application.
```powershell
.\venv\Scripts\python.exe manage.py runserver 3003
```

### Terminal 2: Celery Worker
Processes background tasks like sending daily emails.
```powershell
.\venv\Scripts\python.exe -m celery -A config worker --loglevel=info -P solo
```
*(Note: `-P solo` is often required on Windows for Celery).*

### Terminal 3: Celery Beat
Triggers scheduled tasks (e.g., sending emails every morning at 8:00 AM).
```powershell
.\venv\Scripts\python.exe -m celery -A config beat --loglevel=info
```

---

## Troubleshooting

### `ModuleNotFoundError: No module named 'celery'`
This happens if you run `python manage.py` using your global Python instead of the virtual environment. Always use `.\venv\Scripts\python.exe` or ensure your venv is activated.

### Redis Connection Error
Ensure Redis is running. You can test it with:
```powershell
# If using Docker
docker ps
# If using native
redis-cli ping
```

### Standardized API Responses
All API responses follow this format:
```json
{
  "status": true,
  "message": "success",
  "data": { ... }
}
```
If you encounter an error, `status` will be `false` and `message` will contain the error details.
