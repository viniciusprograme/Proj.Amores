#!/bin/bash

# Market Solutions Platform - Initialization Script
# This script sets up the Django project for development

set -e

echo " Initializing Market Solutions Platform..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo " Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo " Activating virtual environment..."
source venv/Scripts/activate

# Install dependencies
echo " Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo " Running database migrations..."
python sistemaLogin/manage.py migrate

# Create superuser if it doesn't exist
echo " Creating superuser (if needed)..."
echo "from apps.users.models import User; User.objects.filter(email='admin@marketsolutions.com').exists() or User.objects.create_superuser('admin@marketsolutions.com', 'admin@marketsolutions.com', 'Admin123!')" | python sistemaLogin/manage.py shell

# Collect static files
echo " Collecting static files..."
python sistemaLogin/manage.py collectstatic --noinput

# Create logs directory
mkdir -p logs

echo " Initialization complete!"
echo ""
echo " To start the development server:"
echo "   source venv/Scripts/activate"
echo "   cd sistemaLogin"
echo "   python manage.py runserver"
echo ""
echo " API Documentation available at:"
echo "   http://localhost:8000/api/schema/swagger-ui/"
echo ""
echo " Admin panel:"
echo "   http://localhost:8000/admin/"
echo "   Email: admin@marketsolutions.com"
echo "   Password: Admin123!"