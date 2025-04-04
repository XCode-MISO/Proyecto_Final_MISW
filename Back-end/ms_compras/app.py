# ms_compras/app.py
from flask import Flask
from models.db import init_db
from apis.fabricante_api import fabricante_bp
from apis.producto_api import producto_bp
from apis.detalle_compra_api import detalle_compra_bp
from werkzeug.exceptions import HTTPException
import os
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    # Configurar conexión a la base de datos compras_db
    db_host = os.getenv('DB_HOST', 'db')
    db_port = os.getenv('DB_PORT', '5432')
    db_user = os.getenv('DB_USER', 'postgres')
    db_pass = os.getenv('DB_PASS', 'postgres')
    db_name = os.getenv('DB_NAME', 'compras_db')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    init_db(app)
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            return {"error": e.description}, e.code
        return {"error": str(e)}, 500

    # Registrar blueprints
    app.register_blueprint(fabricante_bp, url_prefix='/api/fabricantes')
    app.register_blueprint(producto_bp, url_prefix='/api/productos')
    # Nuevo endpoint para registrar la compra y su detalle
    app.register_blueprint(detalle_compra_bp, url_prefix='/api/compras/detalle')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5001, debug=True)