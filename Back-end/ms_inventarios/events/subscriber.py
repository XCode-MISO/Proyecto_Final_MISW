import os
import json
from google.cloud import pubsub_v1
from services.inventario_service import InventarioService

inventario_service = InventarioService()

def callback(message):
    data_str   = message.data.decode('utf-8')
    event_data = json.loads(data_str)
    print(f"[PUBSUB] Mensaje recibido: {event_data}")

    if event_data.get("eventType") == "CompraRealizadaEvent":
        for p in event_data.get("productos", []):
            producto_id = p.get("productoId")
            cantidad    = p.get("cantidad", 0)
            inventario_service.incrementar_stock(producto_id, cantidad)

    message.ack()

def start_subscriber():
    project_id       = os.getenv('GCP_PROJECT_ID', 'misw-4301-native-cloud-433702')
    subscription_id  = os.getenv('PUBSUB_SUBSCRIPTION_ID', 'inventarios-sub')

    subscriber       = pubsub_v1.SubscriberClient()
    subscription_path= subscriber.subscription_path(project_id, subscription_id)

    print(f"[PUBSUB] Escuchando suscripción: {subscription_path}")
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)

    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()
        subscriber.close()