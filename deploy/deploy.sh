#!/bin/bash

# Configuration
APP_DIR="/var/www/hopebeginbackend"
VENV_DIR="$APP_DIR/venv"

echo "🚀 Starting deployment to api.hopebegins.today..."

cd $APP_DIR

# 1. Pull latest code (assuming git is used)
# git pull origin main

# 2. Activate virtual environment
source $VENV_DIR/bin/activate

# 3. Install/Update dependencies
echo "📦 Installing dependencies..."
pip install -r requirements/prod.txt

# 4. Run migrations
echo "🗄️ Running database migrations..."
python manage.py migrate --noinput

# 5. Collect static files
echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

# 6. Restart services
echo "🔄 Restarting services..."
sudo systemctl restart hope-begins-api
sudo systemctl restart hope-begins-worker
sudo systemctl restart hope-begins-beat

echo "✅ Deployment complete!"
