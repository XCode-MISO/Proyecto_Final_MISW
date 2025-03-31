# src/main.py
from dotenv import load_dotenv, find_dotenv

from flask import Flask, jsonify

from .blueprints.pedidos import operations_blueprint
from .models.model import Base
from .database import engine
from .errors.errors import ApiError
import os
from src.models.pedido import Pedido
from src.models.producto import Producto
from src.models.cliente import Cliente
from src.database import db, database

# Cargar variables de entorno
dotenv_path = find_dotenv(filename=".env.development")
if dotenv_path:
    loaded=load_dotenv(dotenv_path)
    print("Variables de entorno cargadas correctamente")
else:
    print("Error: No se encontró el archivo .env.development")

print(os.getenv("DB_NAME"))
if loaded:
    print("Variables de entorno cargadas correctamente")
else: 
    print("Error: No se pudieron cargar las variables de entorno")
    

app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config["SQLALCHEMY_DATABASE_URI"] = database.get_db_url()
db.init_app(app)



app.register_blueprint(operations_blueprint)
try:
  with app.app_context():  
    Base.metadata.create_all(engine)  # Crea las tablas
except Exception as e:
  print(f"Error al crear tablas: {e}")


if not loaded:
    print("Error: No se pudieron cargar las variables de entorno")


@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
      "msg": err.description
    }
    return jsonify(response), err.code


# print("Variables de Entorno:")
# print(f"VERSION: {os.getenv('VERSION')}")
# print(f"DB_USER: {os.getenv('DB_USER')}")
# print(f"DB_PASSWORD: {os.getenv('DB_PASSWORD')}")
# print(f"DB_HOST: {os.getenv('DB_HOST')}")
# print(f"DB_PORT: {os.getenv('DB_PORT')}")
# print(f"DB_NAME: {os.getenv('DB_NAME')}")
# print(f"USER_PATH: {os.getenv('USER_PATH')}")
# Verifica si las variables se cargaron correctamente
print(f"VERSION: {os.getenv('VERSION')}")