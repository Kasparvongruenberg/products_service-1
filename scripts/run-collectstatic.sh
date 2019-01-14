#!/bin/bash

# All this environment variables need to be defined to run collectstatic
export DATABASE_ENGINE=postgresql
export DATABASE_NAME=nothing
export DATABASE_PORT=nothing
export DATABASE_USER=nothing

pip install -r requirements/base.txt
python manage.py collectstatic --no-input
