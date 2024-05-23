set -o errexit
pip install -r requirements.txt 
python manage.py migrate

if [[-z $CREATE_SUPERUSER]]; then python manage.py createsuperuserfi
