#!/bin/bash

python manage.py migrate

gunicorn products_service.wsgi --config products_service/gunicorn_conf.py
