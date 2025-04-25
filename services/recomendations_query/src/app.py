from flask import Flask
from src.config import Config
from src.models import db
from src.endpoints.recommendation import recommendation_bp

import threading
from src.services.recommendation_service import pull_messages

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    app.register_blueprint(recommendation_bp, url_prefix='/api')

    @app.route('/health', methods=['GET'])
    def health():
        return "OK", 200
    
    def start_pull_worker(app):
        pull_messages(app)

    # Pasa la app al worker
    threading.Thread(target=start_pull_worker, args=(app,), daemon=True).start()
    print("Pull worker iniciado", flush=True)
    
    return app
