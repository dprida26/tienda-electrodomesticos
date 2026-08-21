#!/bin/bash
set -e

echo "=== Instalando dependencias ==="
pip install --upgrade pip
pip install -r requirements.txt

echo "=== Ejecutando migraciones ==="
python manage.py migrate --noinput || true

echo "=== Recopilando archivos estáticos ==="
python manage.py collectstatic --noinput --clear

echo "=== Build completado exitosamente ==="
