# Usa una imagen oficial de Python
FROM python:3.13-slim

# Establece variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Establece el directorio de trabajo
WORKDIR /app

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copia el archivo de requisitos e instala las dependencias
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del proyecto
COPY . /app/

# Genera los archivos comprimidos ANTES de collectstatic
RUN python manage.py compress --force

# Expone el puerto
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && gunicorn --bind 0.0.0.0:8000 django_crud.wsgi:application"]
