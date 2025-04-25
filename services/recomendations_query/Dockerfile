FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/src

COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

ENV PYTHONPATH=/app
ENV FLASK_APP=src.app

EXPOSE 8080

CMD ["/app/entrypoint.sh"]
