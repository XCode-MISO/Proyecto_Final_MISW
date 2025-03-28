import threading
from flask import Flask
from logistica.infrastructure.config import Config
from logistica.infrastructure.pub_sub import consume_pedido_creado
from logistica.application.command.generate_route import comandos_bp
from logistica.infrastructure.db.model import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(comandos_bp)

    with app.app_context() as context:
        db.create_all()
        thread = threading.Thread(target=lambda: consume_pedido_creado(context))
        thread.setDaemon(True)
        thread.start()

    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"

    @app.route("/health")
    def health_check():
        return "Ok"
    return app

