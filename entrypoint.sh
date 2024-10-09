#!/bin/bash
echo "Collect static files"
uv run manage.py collectstatic --no-input

echo "Apply database migrations"
uv run manage.py migrate --no-input


# uv run manage.py runserver 0.0.0.0:8000
uv run gunicorn -c gunicorn.conf.py
