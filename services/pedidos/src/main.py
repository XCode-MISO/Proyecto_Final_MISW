# src/main.py
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv

from flask import Flask, jsonify

from .blueprints.pedidos import operations_blueprint
from .models.model import Base
from .database import engine
from .errors.errors import ApiError
import os
from src.models.pedido import Pedido
from src.models.pedido_producto import PedidoProducto
from src.database import db, database
from src.models.seed_data import seed_database_if_empty  # Solo con importarlo se ejecutará el código del archivo

seed_database_if_empty()
# Cargar variables de entorno
dotenv_path = find_dotenv(filename=".env.development")
if dotenv_path:
    loaded=load_dotenv(dotenv_path)
    print("Variables de entorno cargadas correctamente")
else:
    print("Error: No se encontró el archivo .env.development")
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
CORS(app)
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
# print(f"DATABASE_USER: {os.getenv('DATABASE_USER')}")
# print(f"DATABASE_PASSWORD: {os.getenv('DATABASE_PASSWORD')}")
# print(f"DATABASE_URL: {os.getenv('DATABASE_URL')}")
# print(f"DATABASE_PORT: {os.getenv('DATABASE_PORT')}")
# print(f"DATABASE_NAME: {os.getenv('DATABASE_NAME')}")
# print(f"USER_PATH: {os.getenv('USER_PATH')}")
# Verifica si las variables se cargaron correctamente
print(f"VERSION: {os.getenv('VERSION')}")