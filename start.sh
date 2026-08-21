#!/bin/bash
set -e

echo "=== Ejecutando migraciones ==="
python manage.py migrate --noinput || echo "Migraciones ya ejecutadas o no necesarias"

echo "=== Iniciando Gunicorn ==="
gunicorn config.wsgi:application --bind 0.0.0.0:10000 --workers 2
