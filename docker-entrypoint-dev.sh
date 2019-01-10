#!/bin/bash
# This script must not be used for production.

set -e

bash scripts/tcp-port-wait.sh $DATABASE_HOST $DATABASE_PORT

echo $(date -u) "- Migrating"
python manage.py migrate

echo $(date -u) "- Creating admin user"
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(email='admin@example.com').delete(); User.objects.create_superuser('admin', 'admin@example.com', 'admin')"

echo $(date -u) "- Running the server"
gunicorn products_service.wsgi --config products_service/gunicorn_conf.py --reload --timeout 120 -w 2
