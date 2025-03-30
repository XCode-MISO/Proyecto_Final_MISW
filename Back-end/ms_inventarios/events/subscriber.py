import os
import sys
import json
from google.cloud import pubsub_v1
from services.inventario_service import InventarioService
from models.db import db
from models.producto import Producto

inventario_service = InventarioService()

def callback(message):
    # Para usar el ORM de Flask, creamos un contexto de aplicación
    from app import create_app
    app = create_app()
    with app.app_context():
        data_str = message.data.decode('utf-8')
        event_data = json.loads(data_str)
        print(f"[PUBSUB] Mensaje recibido: {event_data}")
        if event_data.get("eventType") == "DetalleCompraCreado":
            producto_id = event_data.get("productoId")
            cantidad = event_data.get("cantidad", 0)
            nombre = event_data.get("nombre")
            precio = event_data.get("precio")
            fabricante_id = event_data.get("fabricanteId")
            # Actualizar el stock en la tabla de inventario
            inventario_service.incrementar_stock(producto_id, cantidad)
            # Actualizar (o insertar) en la tabla desnormalizada de productos
            prod = Producto.query.filter_by(producto_id=producto_id).first()
            if prod:
                prod.nombre = nombre
                prod.precio = precio
                prod.fabricante_id = fabricante_id
            else:
                prod = Producto(producto_id=producto_id, nombre=nombre, precio=precio, fabricante_id=fabricante_id)
                db.session.add(prod)
            db.session.commit()
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