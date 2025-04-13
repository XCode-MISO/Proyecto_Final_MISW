import os
import json
from google.cloud import pubsub_v1
from services.inventario_service import InventarioService
from models.db import db
from models.producto import Producto
from app import create_app

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/esneiderrestrepo/Documents/credentials.json"

app = create_app()

inventario_service = InventarioService()

def callback(message):
    # Crear un contexto de aplicación para este hilo
    with app.app_context():
        try:
            data_str = message.data.decode('utf-8')
            event_data = json.loads(data_str)
            print(f"[PUBSUB] Mensaje recibido: {event_data}")

            if event_data.get("eventType") == "CompraCreada":
                producto_id = event_data.get("productoId")
                cantidad = event_data.get("cantidad")
                nombre = event_data.get("nombre")
                precio = event_data.get("precio")
                moneda = event_data.get("moneda")
                bodega = event_data.get("bodega")
                estante = event_data.get("estante")
                pasillo = event_data.get("pasillo")
                
                # Actualizar el stock en la tabla de inventario (incluye ubicación)
                inventario_service.incrementar_stock(producto_id, cantidad, bodega, estante, pasillo)

                # Actualizar (o insertar) en la tabla desnormalizada de productos
                prod = Producto.query.filter_by(producto_id=producto_id).first()
                if prod:
                    prod.precio = precio,
                    prod.moneda = moneda
                    db.session.merge(prod) 
                else:
                    prod = Producto(
                        producto_id=producto_id,
                        nombre=nombre,
                        moneda=moneda,
                        precio=precio                    )
                    db.session.add(prod)
                db.session.commit()

        except Exception as e:
            print(f"[PUBSUB] Error en callback: {e}")
        finally:
            message.ack()

def start_subscriber():
    project_id = os.getenv('GCP_PROJECT_ID', 'misw-4301-native-cloud-433702')
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