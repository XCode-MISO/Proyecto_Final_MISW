import json
import os
import threading
from flask import Flask
from logistica.infrastructure.config import Config
from logistica.infrastructure.pub_sub import consume_pedido_creado
from logistica.application.command.generate_route import comandos_bp
from logistica.application.query.get_routes import query_bp
from logistica.infrastructure.db.model import db
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(comandos_bp)
    app.register_blueprint(query_bp)
    CORS(app)
    db.create_all()

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

    return app

if __name__ == '__main__':
    flask_app = create_app()
    # Iniciar el subscriber en un hilo aparte
    with flask_app.app_context() as context:
        thread = threading.Thread(target=lambda: consume_pedido_creado(context))
        thread.daemon = True
        thread.start()

    flask_app.run(host='0.0.0.0', port=8080, debug=True)