#!/bin/sh



# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn
gunicorn --bind 0.0.0.0:8000 TaskManagmentSite.wsgi