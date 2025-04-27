# ms_compras/app.py
import json
from flask import Flask
from models.db import init_db
from apis.fabricante_api import fabricante_bp
from apis.producto_api import producto_bp
from werkzeug.exceptions import HTTPException
import os
import logging
from flask_cors import CORS

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)


    if app.config.get('TESTING'):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    else:
        db_host = os.getenv('DB_HOST', '34.171.48.199')
        db_port = os.getenv('DB_PORT', '5432')
        db_user = os.getenv('DB_USER', 'admin_write')
        db_pass = os.getenv('DB_PASS', 'PASSWORD_123')
        db_name = os.getenv('DB_NAME', 'compras_db')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'

        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "pool_recycle": 300, 
        "pool_pre_ping": True  
        }
    
    init_db(app)
    
    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            return {"error": e.description}, e.code
        return {"error": str(e)}, 500

    # Registrar blueprints
    app.register_blueprint(fabricante_bp, url_prefix='/api/fabricantes')
    app.register_blueprint(producto_bp, url_prefix='/api/productos')
    
    @app.route("/")
    def root_path():
        return "<p>Servicio de Compras</p>"

    @app.route("/health")
    def health_check():
        return "Ok"

    @app.route("/info")
    def info_path():
        try:
            return json.load(open(os.path.join("version.json"), "r"))
        except Exception as e:
            print(str(e))
            return "No version.json, this means this deployment was manual or there is an error."

    
    CORS(app)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5001, debug=True)