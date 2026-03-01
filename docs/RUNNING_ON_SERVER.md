# Running Hope Begins Backend on a Server

This guide provides an overview of how to deploy and run the Hope Begins Django backend in a production environment.

## 1. Prerequisites

A production server (e.g., Ubuntu 22.04+) with:
-   **Python 3.10+**
-   **Redis** (for Celery and/or Caching)
-   **PostgreSQL** (e.g., Supabase or a managed Postgres instance)
-   **Nginx** (as a reverse proxy)
-   **Gunicorn/Uvicorn** (as the application server)

---

## 2. Infrastructure Setup

### Security
-   **SSL**: Use `certbot` for Let's Encrypt certificates.
-   **Firewall**: Allow only ports 80, 443, and SSH (22).
-   **Database**: Ensure your database is accessible by the server and has a strong password.

### Environment Variables
Store production secrets in a `.env` file or as environment variables on your server:
-   `DEBUG=False`
-   `SECRET_KEY=a-long-secure-random-key`
-   `DATABASE_URL=postgres://user:password@host:5432/dbname`
-   `CELERY_BROKER_URL=redis://localhost:6379/0`
-   `EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend`
-   `EMAIL_HOST=smtp.your-provider.com`
-   `ALLOWED_HOSTS=yourdomain.com,api.yourdomain.com`

---

## 3. Application Deployment

### Setup Folder
```bash
sudo mkdir -p /var/www/hope-begins-backend
sudo chown $USER:$USER /var/www/hope-begins-backend
cd /var/www/hope-begins-backend
```

### Virtual Environment & Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements/prod.txt
```

### Static Files & Migrations
```bash
python manage.py collectstatic --noinput
python manage.py migrate
```

---

## 4. Process Management (Systemd)

To ensure the services stay running and restart after a crash or reboot, use **systemd**.

### Django API Server (`gunicorn`)
Create `/etc/systemd/system/hope-begins-api.service`:
```ini
[Unit]
Description=Hope Begins Gunicorn Service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/hope-begins-backend
ExecStart=/var/www/hope-begins-backend/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/var/www/hope-begins-backend/app.sock \
          config.wsgi:application

[Install]
WantedBy=multi-user.target
```

### Celery Worker
Create `/etc/systemd/system/hope-begins-worker.service`:
```ini
[Unit]
Description=Hope Begins Celery Worker
After=network.target redis.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/hope-begins-backend
ExecStart=/var/www/hope-begins-backend/venv/bin/celery -A config worker --loglevel=info

[Install]
WantedBy=multi-user.target
```

### Celery Beat
Create `/etc/systemd/system/hope-begins-beat.service`:
```ini
[Unit]
Description=Hope Begins Celery Beat
After=network.target redis.service

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/hope-begins-backend
ExecStart=/var/www/hope-begins-backend/venv/bin/celery -A config beat --loglevel=info

[Install]
WantedBy=multi-user.target
```

---

## 5. Reverse Proxy (Nginx)

Example Nginx configuration:
```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/hope-begins-backend/app.sock;
    }

    location /static/ {
        alias /var/www/hope-begins-backend/static/;
    }

    location /media/ {
        alias /var/www/hope-begins-backend/media/;
    }
}
```

---

## 6. Logs & Monitoring

-   **API Logs**: `journalctl -u hope-begins-api -f`
-   **Worker Logs**: `journalctl -u hope-begins-worker -f`
-   **Beat Logs**: `journalctl -u hope-begins-beat -f`

Use tools like **Sentry** for error tracking and **Prometheus/Grafana** for monitoring performance.
