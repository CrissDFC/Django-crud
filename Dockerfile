# Usa una imagen oficial de Python
FROM python:3.13-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos del proyecto
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . /app/

# Copiar el script de inicio
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Exponer el puerto
EXPOSE 8000

# Ejecutar el script al arrancar el contenedor
CMD ["/app/entrypoint.sh"]
