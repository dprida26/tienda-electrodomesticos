#!/bin/bash
set -e

echo "=========================================="
echo "START: run.sh wrapper"
echo "DATABASE_URL: ${DATABASE_URL:0:60}..."
echo "=========================================="

if [ -z "$DATABASE_URL" ]; then
    echo "ERROR: DATABASE_URL is not set!"
    exit 1
fi

echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting Gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:10000 --workers 2
