# Hope Begins Backend

A modular Django-based REST API for the Hope Begins project.

## Project Structure

```text
backend/
├── manage.py            # Entry point for Django commands
├── config/              # Project-wide settings and configuration
│   ├── settings/        # Environment-specific settings
│   │   ├── base.py      # Common settings
│   │   ├── dev.py       # Development settings (DEBUG=True)
│   │   └── prod.py      # Production settings (DEBUG=False)
│   ├── asgi.py          # ASGI config
│   ├── wsgi.py          # WSGI config
│   └── urls.py          # Root URL routing
├── apps/                # Business logic separated into apps
│   ├── users/           # User management and authentication
│   ├── prayers/         # Prayer requests and tracking
│   ├── hopecasts/       # Podcast/audio content management
│   ├── donations/       # Donation processing and history
│   └── hope_ai/         # AI integration features
├── common/              # Shared utilities and helpers
├── requirements/        # Dependency management
│   ├── base.txt         # Core dependencies
│   ├── dev.txt          # Development dependencies
│   └── prod.txt         # Production dependencies
└── .env                 # Environment variables
```

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd hopebeginbackend
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements/dev.txt
    ```

4.  **Environment Variables:**
    Create a `.env` file in the root directory (one has been provided as a template).

5.  **Run migrations:**
    ```bash
    python manage.py migrate
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

## API Endpoints

All API endpoints are prefixed with `/api/`.

-   `/api/users/`
-   `/api/prayers/`
-   `/api/hopecasts/`
-   `/api/donations/`
-   `/api/hope-ai/`
-   `/api/token/`: Obtain JWT token pair.
-   `/api/token/refresh/`: Refresh access token.
-   `/admin/`: Django Admin interface.
