set -o errexit
pip install -r requirements.txt 
python manage.py migrate


# Debug print statement to check the environment variable
echo "CREATE_SUPERUSER is set to: $CREATE_SUPERUSER"

# Check if CREATE_SUPERUSER variable is set and not empty
if [[ -n $CREATE_SUPERUSER ]]; then
  python manage.py createsuperuser --no-input
fi
