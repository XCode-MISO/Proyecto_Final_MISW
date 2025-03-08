from flask import Flask
from src.config import Config
from src.models import db
from src.endpoints.recommendation import recommendation_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(recommendation_bp, url_prefix='/api')

    @app.route('/health', methods=['GET'])
    def health():
        return "OK", 200
    
    return app
