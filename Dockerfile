# Usa una imagen oficial de Python
FROM python:3.10-slim

# Establece variables de entorno para evitar que Python escriba archivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Establece el directorio de trabajo
WORKDIR /app

# Instala dependencias del sistema (necesarias para psycopg2 y otras librerías)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copia el archivo de requisitos e instala las dependencias de Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del proyecto
COPY . /app/

# Recopila archivos estáticos (esto se hace durante la construcción para optimizar la imagen)
RUN python manage.py collectstatic --noinput

# Expone el puerto en el que se ejecutará la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["sh", "-c", "python manage.py migrate && gunicorn --bind 0.0.0.0:8000 django_crud.wsgi:application"]
