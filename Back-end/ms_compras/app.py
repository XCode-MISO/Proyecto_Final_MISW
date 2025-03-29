
from flask import Flask, jsonify
from models.db import init_db
from apis.fabricante_api import fabricante_bp
from apis.producto_api import producto_bp
from apis.compra_api import compra_bp
from werkzeug.exceptions import HTTPException
import os

def create_app():
    app = Flask(__name__)

    # Variables de entorno para Postgres
    db_host = os.getenv('DB_HOST', 'db')       
    db_port = os.getenv('DB_PORT', '5432')
    db_user = os.getenv('DB_USER', 'postgres')
    db_pass = os.getenv('DB_PASS', 'postgres')
    db_name = os.getenv('DB_NAME', 'compras_db')

    # Config de SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar DB
    init_db(app)

    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            return jsonify({"error": e.description}), e.code
        return jsonify({"error": str(e)}), 500

    # Registrar Blueprints
    app.register_blueprint(fabricante_bp, url_prefix='/api/fabricantes')
    app.register_blueprint(producto_bp,    url_prefix='/api/productos')
    app.register_blueprint(compra_bp,      url_prefix='/api/compras')

    return app

if __name__ == '__main__':
    flask_app = create_app()
    flask_app.run(host='0.0.0.0', port=5001, debug=True)