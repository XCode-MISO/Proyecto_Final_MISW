from dotenv import load_dotenv, find_dotenv
import os
from pathlib import Path
from flask_cors import CORS

# Verificar si el archivo .env.development existe antes de cargarlo
env_path = Path('.env.development')
if env_path.is_file():
    env_file = find_dotenv('.env.development')
    load_dotenv(env_file)

from .errors.errors import ApiError
from .blueprints.clients import client_blueprint
from .blueprints.visits import visit_blueprint
from .models.model import Base
from .session import engine
from flask import Flask, jsonify

app = Flask(__name__)
app.register_blueprint(client_blueprint)
app.register_blueprint(visit_blueprint)
CORS(app)

Base.metadata.create_all(engine)

@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
        "msg": err.description
    }
    return jsonify(response), err.code