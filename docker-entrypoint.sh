#!/bin/bash

# It is responsibility of the deployment orchestration to execute before
# migrations, collect static files, create default admin user, etc.

#!/bin/bash

echo $(date -u) "- Migrating"
python manage.py migrate

echo $(date -u) "- Creating admin user"
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(email='admin@example.com').delete(); User.objects.create_superuser('admin', 'admin@example.com', 'admin')"

echo $(date -u) "- Collect Static"
python manage.py collectstatic

echo $(date -u) "- Running the server"
gunicorn -b 0.0.0.0:8080 products_service.wsgi
