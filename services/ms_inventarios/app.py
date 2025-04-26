import json
import os, sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from flask import Flask, jsonify
from models.db import init_db
from apis.inventario_api import inventario_bp
from werkzeug.exceptions import HTTPException
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"

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

  
    if app.config.get('TESTING'):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    else:
        db_host = os.getenv('DB_HOST', '34.171.48.199')
        db_port = os.getenv('DB_PORT', '5432')
        db_user = os.getenv('DB_USER', 'admin_write')
        db_pass = os.getenv('DB_PASS', 'PASSWORD_123')
        db_name = os.getenv('DB_NAME', 'inventarios_db')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "pool_recycle": 300, 
        "pool_pre_ping": True  
        }

    init_db(app)
    

    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            return jsonify({"error": e.description}), e.code
        return jsonify({"error": str(e)}), 500

    app.register_blueprint(inventario_bp, url_prefix='/api/inventarios')

    CORS(app)
    return app

if __name__ == '__main__':
    flask_app = create_app()
    # Iniciar el subscriber en un hilo aparte
    from events.subscriber_compras import start_subscriber
    from events.subscriber_pedidos import start_pedidos_subscriber
    import threading
    sub_thread_compras = threading.Thread(target=start_subscriber, daemon=True)
    sub_thread_compras.start()
    sub_thread_pedidos = threading.Thread(target=start_pedidos_subscriber, daemon=True)
    sub_thread_pedidos.start()

    flask_app.run(host='0.0.0.0', port=5002, debug=True)