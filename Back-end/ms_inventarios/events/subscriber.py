# ms_inventarios/events/subscriber.py
import os
import json
from google.cloud import pubsub_v1

# Importa el servicio que usas
from services.inventario_service import InventarioService

# Crea una instancia global del servicio (esto no necesita contexto)
inventario_service = InventarioService()

def callback(message):
    # Importamos create_app para poder crear un contexto de aplicación
    from app import create_app
    app = create_app()  # Se crea la aplicación
    with app.app_context():
        data_str = message.data.decode('utf-8')
        event_data = json.loads(data_str)
        print(f"[PUBSUB] Mensaje recibido: {event_data}")
        if event_data.get("eventType") == "DetalleCompraCreado":
            producto_id = event_data.get("productoId")
            cantidad = event_data.get("cantidad", 0)
            # Aquí ya estamos en un contexto de aplicación, por lo que podemos usar db queries
            inventario_service.incrementar_stock(producto_id, cantidad)
    message.ack()

def start_subscriber():
    project_id = os.getenv('GCP_PROJECT_ID', 'my-project')
    subscription_id = os.getenv('PUBSUB_SUBSCRIPTION_ID', 'inventarios-sub')
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)
    print(f"[PUBSUB] Escuchando suscripción: {subscription_path}")
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()
        subscriber.close()