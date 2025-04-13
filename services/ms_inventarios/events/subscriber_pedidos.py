import os
import json
from google.cloud import pubsub_v1
from services.inventario_service import InventarioService
from models.db import db
from app import create_app

# Configurar credenciales si es necesario (o via variable de entorno GOOGLE_APPLICATION_CREDENTIALS)
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/esneiderrestrepo/Documents/credentials.json"

# Creamos la aplicación una sola vez para usar su contexto
app = create_app()

inventario_service = InventarioService()

def callback(message):
    with app.app_context():
        try:
            data_str = message.data.decode('utf-8')
            event_data = json.loads(data_str)
            print(f"[PUBSUB] Mensaje recibido: {event_data}")
            # Validamos que sea un evento de pedido
            if event_data.get("eventType") == "PedidoCreadoInventarios":
                items = event_data.get("items", [])
                for item in items:
                    producto_id = item.get("productoId")
                    cantidad = item.get("cantidad", 0)
                    # Decrementamos el stock para cada producto
                    try:
                        inventario_service.decrementar_stock(producto_id, cantidad)
                    except Exception as dec_e:
                        logger.error(f"Error al decrementar stock para producto_id {producto_id}: {dec_e}")

        except Exception as e:
            # Puedes registrar el error y/o reenviar el mensaje según convenga
            print(f"[PUBSUB] Error en el callback de pedidos: {e}")
        finally:
            message.ack()

def start_pedidos_subscriber():
    project_id = os.getenv('GCP_PROJECT_ID', 'misw-4301-native-cloud-433702')
    subscription_id = os.getenv('PEDIDOS_SUBSCRIPTION_ID', 'logistica')
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)
    print(f"[PUBSUB] Escuchando suscripción de pedidos: {subscription_path}")
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()
        subscriber.close()


   