import os
import threading
from flask import Flask
from models.db import db
from api.reporte_controller import reporte_bp
import logging
from flask_cors import CORS
# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    
  
    postgres_uri = "postgresql+pg8000://admin_read:PASSWORD_123@35.202.68.237:5432/reportes_db"
    
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', postgres_uri)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    #  la DB
    db.init_app(app)
    
    app.register_blueprint(reporte_bp)
    
    with app.app_context():
        db.create_all()
    
    @app.route('/')
    def health_check():
        return {"status": "ok", "service": "ms_ventas_report"}
    
    
    CORS(app)
    return app

def start_subscribers():
    in_docker = os.path.exists("/.dockerenv")
    
    if in_docker:
        logger.info("🐳 Ejecutando en Docker, intentando iniciar Pub/Sub real")
        try:
            from events.subscriber_pedidos import start_pedidos_subscriber
            subscriber_thread = threading.Thread(target=start_pedidos_subscriber)
            subscriber_thread.daemon = True
            subscriber_thread.start()
            logger.info("✅ Suscriptor Pub/Sub iniciado correctamente")
        except Exception as e:
            logger.error(f"❌ Error iniciando Pub/Sub: {e}")
    else:
        logger.info("💻 Ejecutando en local, usando simulador de eventos")
        try:
            from events.subscriber_pedidos import simular_eventos_pedidos
            simular_eventos_pedidos()
            logger.info("✅ Eventos simulados procesados correctamente")
        except Exception as e:
            logger.error(f"❌ Error en simulación de eventos: {e}")

if __name__ == "__main__":
    app = create_app()
    
    if os.getenv('ENABLE_PUBSUB', 'false').lower() == 'true':
        start_subscribers()
    else:
        logger.info("ℹ️ Pub/Sub desactivado. Establece ENABLE_PUBSUB=true para activarlo.")
    
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))