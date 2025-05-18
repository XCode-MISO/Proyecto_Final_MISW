FROM python:3.10-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código fuente
COPY . .

# Puerto para la API
EXPOSE 8080

# Comando para ejecutar
CMD ["python", "app_simple.py"]
