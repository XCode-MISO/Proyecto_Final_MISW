FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencia
COPY requirements.txt ./

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

COPY ./keys.json /app/

# Copiar el código fuente de la aplicación
COPY src/ ./src

# Configurar la variable de entorno para Flask
ENV PYTHONPATH=/app/src

# Exponer el puerto de la aplicación
EXPOSE 8080

# Comando para ejecutar la aplicación con gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "src.main:app"]