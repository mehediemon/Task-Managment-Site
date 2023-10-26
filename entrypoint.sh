#!/bin/sh

# Apply database migrations (if necessary)
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput
# Check if the superuser exists, and create one if not
SUPERUSER_USERNAME="admin"
SUPERUSER_EMAIL="admin@example.com"
SUPERUSER_PASSWORD="12345678"

# Check if the superuser already exists
if [[ $(python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print(User.objects.filter(username='$SUPERUSER_USERNAME').exists())") == "True" ]]; then
    echo "Superuser '$SUPERUSER_USERNAME' already exists."
else
    # Create the superuser
    echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('$SUPERUSER_USERNAME', '$SUPERUSER_EMAIL', '$SUPERUSER_PASSWORD')" | python manage.py shell
    echo "Superuser '$SUPERUSER_USERNAME' created."
fi
# Start Gunicorn
gunicorn --bind 0.0.0.0:8000 TaskManagmentSite.wsgi