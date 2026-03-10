# Hope Begins Backend

A modular Django-based REST API for the Hope Begins project, providing features for user management, prayer tracking, hopecasts, and a 21-day "Daily Hope" journey.

---

## 🛠 Features

- **User Management**: Role-based access (Admin, Carrier, User), registration (with admin approval), and JWT authentication.
- **Prayer Requests**: Public prayer submission and prayer response tracking.
- **Hopecasts**: Management of audio content with multi-category support.
- **Daily Hope**: A 21-day automated email journey powered by Celery & Redis.
- **Standardized API**: Consistent response format: `{ "status": boolean, "message": string, "data": any }`.

---

## 🚀 Setup & Running

For detailed instructions, see the specific guides in the `docs/` folder:

### [Running Locally](./docs/RUNNING_LOCALLY.md)
Learn how to:
1. Set up your virtual environment.
2. Configure your local `.env` and database.
3. Start the Django server on **Port 3003**.
4. Run Celery workers and beat for automated emails.

### [Running on a Server (Production)](./docs/RUNNING_ON_SERVER.md)
Learn how to:
1. Set up systemd services for production.
2. Configure Nginx and Gunicorn.
3. Manage production environment variables.

### [Redis Troubleshooting](./docs/REDIS_TROUBLESHOOTING.md)
Learn how to check if Redis is working correctly on your server.

---

## 📁 Project Structure

```text
backend/
├── manage.py            # Entry point for Django commands
├── config/              # Project-wide settings and configuration
│   ├── settings/        # Environment-specific settings
│   │   ├── base.py      # Common settings
│   │   ├── dev.py       # Development settings (DEBUG=True)
│   │   └── prod.py      # Production settings (DEBUG=False)
│   ├── celery.py        # Celery application configuration
│   ├── asgi.py          # ASGI config
│   ├── wsgi.py          # WSGI config
│   └── urls.py          # Root URL routing
├── apps/                # Business logic separated into apps
│   ├── users/           # User management, auth, and carrier applications
│   ├── prayers/         # Prayer requests and tracking
│   ├── hopecasts/       # Podcast/audio content management
│   ├── daily_hope/      # 21-day Daily Hope automated emails
│   └── donations/       # Donation processing and history
├── common/              # Shared utilities (e.g., custom BaseJSONRenderer)
├── requirements/        # Dependency management
│   ├── base.txt         # Core dependencies
│   ├── dev.txt          # Development dependencies
│   └── prod.txt         # Production dependencies
└── .env                 # Environment variables
```

---

## 📧 Email & Celery

The "Daily Hope" feature uses **Celery Beat** to schedule daily tasks at 8:00 AM. 

- **Celery Broker**: Redis (`redis://localhost:6379/0`)
- **Celery Result Backend**: Redis
- **Email**: SMTP backend configured via `.env` (currently set to console for dev, can be switched to SMTP).

---

## 📜 API Documentation

All API endpoints are prefixed with `/api/`.

-   `/api/users/`: User registration and management.
-   `/api/prayers/requests/`: Prayer request submission and listing.
-   `/api/hopecasts/`: Hopecasts and categories.
-   `/api/hopecasts/{id}/play/`: Increment the play count for a hopecast.
-   `/api/daily-hope/journeys/`: Sign up for the 21-day Hope Journey.
-   `/api/users/login/`: Obtain JWT token pair.
-   `/api/users/logout/`: Blacklist refresh tokens.
-   `/api/users/overview/`: Admin dashboard statistics (Admin only).
-   `/admin/`: Django Admin interface.
