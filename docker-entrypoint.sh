#!/bin/bash

# It is responsability of the deployment orchestration to execute before
# migrations, create default admin user, populate minimal data, etc.

gunicorn products_service.wsgi --config products_service/gunicorn_conf.py
