#!/bin/sh

echo "→ Aplicando migraciones..."
python manage.py migrate

echo "→ Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "→ Iniciando servidor Gunicorn..."
gunicorn django_crud.wsgi:application --bind 0.0.0.0:8000
