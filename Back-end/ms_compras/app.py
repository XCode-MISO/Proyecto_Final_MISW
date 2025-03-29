
from flask import Flask
from models.db import init_db
from apis.fabricante_api import fabricante_bp
from apis.producto_api import producto_bp
from apis.compra_api import compra_bp
from apis.producto_compra_api import producto_compra_bp 
from werkzeug.exceptions import HTTPException
import os

def create_app():
    app = Flask(__name__)
    
    # Configuración de la base de datos (se espera conectarse a Postgres)
    db_host = os.getenv('DB_HOST', 'db')
    db_port = os.getenv('DB_PORT', '5432')
    db_user = os.getenv('DB_USER', 'postgres')
    db_pass = os.getenv('DB_PASS', 'postgres')
    # Para ms_compras se usa la base "compras_db"
    db_name = os.getenv('DB_NAME', 'compras_db')
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    init_db(app)

    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            return {"error": e.description}, e.code
        return {"error": str(e)}, 500

    # Registrar los endpoints
    app.register_blueprint(fabricante_bp, url_prefix='/api/fabricantes')
    app.register_blueprint(producto_bp, url_prefix='/api/productos')
    app.register_blueprint(compra_bp, url_prefix='/api/compras')
    # Nuevo endpoint para registrar producto de compra
    app.register_blueprint(producto_compra_bp, url_prefix='/api/compras/productos')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5001, debug=True)