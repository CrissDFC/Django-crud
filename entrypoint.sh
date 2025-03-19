#!/bin/sh

echo "→ Recolectando archivos estáticos..."
python manage.py collectstatic --noinput


echo "→ Aplicando migraciones..."
python manage.py migrate



# Inicia Gunicorn
exec gunicorn --bind 0.0.0.0:8000 django_crud.wsgi:application