import os
import json
import sys
import logging
from models.db import db
from models.producto import Producto
from google.cloud import pubsub_v1

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/esneiderrestrepo/Documents/credentials.json"

# Configuración del logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ProductoService:
    def registrar_producto_individual(
        self,
        nombre,
        fabricante_id,
        cantidad,
        precio,
        moneda,
        bodega,
        estante,
        pasillo
    ):
        # 1. Buscar o crear producto
        try:
            producto = Producto.query.filter_by(nombre=nombre, fabricante_id=fabricante_id).first()
            if producto:
                producto.precio = precio,
                producto.moneda = moneda
                db.session.commit()
                logger.debug("Producto existente actualizado: %s", producto.id)
            else:
                producto = Producto(
                    nombre=nombre,
                    fabricante_id=fabricante_id,
                    precio=precio,
                    moneda=moneda
                )
                db.session.add(producto)
                db.session.commit()
                logger.debug("Producto creado: %s", producto.id)
        except Exception as e:
            logger.exception("Error al crear o actualizar el producto")
            raise

        # 2. Publicar evento a Pub/Sub para actualizar ms_inventarios
        try:
            logger.debug("Iniciando publicación a Pub/Sub...")
            project_id = os.getenv('GCP_PROJECT_ID', 'misw-4301-native-cloud-433702')
            topic_id = os.getenv('PUBSUB_TOPIC_ID', 'compras-topic')
            publisher = pubsub_v1.PublisherClient()
            topic_path = publisher.topic_path(project_id, topic_id)

            event_data = {
                "eventType": "CompraCreada",
                "productoId": producto.id,
                "cantidad": cantidad,
                "precio": precio,
                "moneda": moneda,
                "nombre": producto.nombre,
                "bodega": bodega,
                "estante": estante,
                "pasillo": pasillo
            }
            msg_str = json.dumps(event_data)
            future = publisher.publish(topic_path, data=msg_str.encode("utf-8"))
            logger.debug("Solicitud enviada, esperando resultado...")
            # Espera un máximo de 20 segundos para obtener respuesta
            future.result(timeout=20)
            logger.debug("[PUBSUB] Evento publicado: %s", event_data)
            sys.stdout.flush()
        except Exception as e:
            logger.exception("[PUBSUB] Error publicando:")
            sys.stdout.flush()
            
        return producto