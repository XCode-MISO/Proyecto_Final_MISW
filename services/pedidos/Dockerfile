FROM python:latest

WORKDIR /app

RUN pip install pipenv && \
  apt-get update && \
  apt-get install -y libpq-dev gcc && \
  apt-get install -y --no-install-recommends gcc python3-dev libssl-dev

RUN pip install pipenv psycopg2

COPY Pipfile ./

RUN pipenv install

COPY . .

EXPOSE 3001

ENV FLASK_APP="./src/main.py"

ENTRYPOINT ["pipenv", "run", "flask", "run", "-h", "0.0.0.0", "--port=3001"]