from dotenv import load_dotenv, find_dotenv
import os
from pathlib import Path
from flask_cors import CORS
from .init_firebase import init_firebase

# Verificar si el archivo .env.development existe antes de cargarlo
env_path = Path('.env.test')
if env_path.is_file():
    env_file = find_dotenv('.env.test')
    load_dotenv(env_file)

from .errors.errors import ApiError
from .blueprints.clients import client_blueprint
from .blueprints.visits import visit_blueprint
from .blueprints.plan import plan_blueprint
from .blueprints.sellers import seller_blueprint
from .models.model import Base
from .session import engine
from flask import Flask, jsonify

app = Flask(__name__)
app.register_blueprint(client_blueprint)
app.register_blueprint(seller_blueprint)
app.register_blueprint(visit_blueprint)
app.register_blueprint(plan_blueprint)
CORS(app)
init_firebase()

Base.metadata.create_all(engine)

@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
        "msg": err.description
    }
    return jsonify(response), err.code