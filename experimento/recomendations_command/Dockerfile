FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el contenido de src/ en /app/src
COPY src/ /app/src

# Copiamos el script de entrypoint y lo hacemos ejecutable
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Añadimos /app al PYTHONPATH para que "src" sea un paquete importable
ENV PYTHONPATH=/app

# Definimos la aplicación Flask
ENV FLASK_APP=src.app

EXPOSE 8080

CMD ["/app/entrypoint.sh"]
