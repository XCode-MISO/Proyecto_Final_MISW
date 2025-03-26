from flask import Flask
from services.logistica.infrastructure.config import Config
from services.logistica.application.command.generate_route import comandos_bp
from services.logistica.infrastructure import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(comandos_bp)

    @app.route("/")
    def hello_world():
        return "<p>Hello, World!</p>"

    @app.route("/health")
    def health_check():
        return "Ok"
    
    return app

