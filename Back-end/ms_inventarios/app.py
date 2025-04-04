import os, sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from flask import Flask, jsonify
from models.db import init_db
from apis.inventario_api import inventario_bp
from werkzeug.exceptions import HTTPException
import threading
from events.subscriber import start_subscriber  

def create_app():
    app = Flask(__name__)

    db_host = os.getenv('DB_HOST', 'db')
    db_port = os.getenv('DB_PORT', '5432')
    db_user = os.getenv('DB_USER', 'postgres')
    db_pass = os.getenv('DB_PASS', 'postgres')
    db_name = os.getenv('DB_NAME', 'inventarios_db')

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    init_db(app)

    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            return jsonify({"error": e.description}), e.code
        return jsonify({"error": str(e)}), 500

    app.register_blueprint(inventario_bp, url_prefix='/api/inventarios')
    return app

if __name__ == '__main__':
    flask_app = create_app()
    # Iniciar el subscriber en un hilo aparte
    sub_thread = threading.Thread(target=start_subscriber, daemon=True)
    sub_thread.start()
    flask_app.run(host='0.0.0.0', port=5002, debug=True)