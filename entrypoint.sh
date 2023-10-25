#!/bin/sh

# Apply database migrations (if necessary)
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn
exec gunicorn --bind 0.0.0.0:8000 TaskManagmentSite.wsgi