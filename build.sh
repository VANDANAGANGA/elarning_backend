#!/bin/bash

# Exit script immediately if a command exits with a non-zero status
set -o errexit

# Install Python dependencies
pip install -r requirements.txt
python manage.py collectstatic --noinput
# Apply database migrations
python manage.py migrate

# Set environment variables for superuser creation
CREATE_SUPERUSER=True
DJANGO_SUPERUSER_EMAIL="admin@gmail.com"
DJANGO_SUPERUSER_PASSWORD="admin*123"
DJANGO_SUPERUSER_FULL_NAME="Admin"
DJANGO_SUPERUSER_PHONE_NUMBER="+918281821211"

# Debug print statements to check the environment variables
echo "CREATE_SUPERUSER is set to: $CREATE_SUPERUSER"
echo "DJANGO_SUPERUSER_EMAIL is set to: $DJANGO_SUPERUSER_EMAIL"
echo "DJANGO_SUPERUSER_PASSWORD is set to: $DJANGO_SUPERUSER_PASSWORD"
echo "DJANGO_SUPERUSER_FULL_NAME is set to: $DJANGO_SUPERUSER_FULL_NAME"
echo "DJANGO_SUPERUSER_PHONE_NUMBER is set to: $DJANGO_SUPERUSER_PHONE_NUMBER"

# Check if CREATE_SUPERUSER variable is set and not empty
if [ -n "$CREATE_SUPERUSER" ]; then
  python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email="$DJANGO_SUPERUSER_EMAIL").exists():
    User.objects.create_superuser("$DJANGO_SUPERUSER_EMAIL", "$DJANGO_SUPERUSER_PASSWORD", full_name="$DJANGO_SUPERUSER_FULL_NAME", phone_number="$DJANGO_SUPERUSER_PHONE_NUMBER")
else:
    print("Superuser already exists.")
EOF
fi
