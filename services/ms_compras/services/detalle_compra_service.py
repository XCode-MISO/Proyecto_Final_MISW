# ms_compras/services/detalle_compra_service.py

import os
import json
import sys
import logging
from models.db import db
from models.compra import Compra
from models.producto import Producto
from models.detalle_compra import DetalleCompra
from google.cloud import pubsub_v1

# Configuración del logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class DetalleCompraService:
    def registrar_detalle_compra_individual(self, nombre, fabricante_id, cantidad, precio):
        # 1. Crear una nueva compra
        try:
            compra = Compra(estado="CREADA")
            db.session.add(compra)
            db.session.commit()  # Asigna compra.id
            logger.debug("Compra creada con ID: %s", compra.id)
        except Exception as e:
            logger.exception("Error al crear la compra")
            raise

        # 2. Buscar o crear producto
        try:
            producto = Producto.query.filter_by(nombre=nombre, fabricante_id=fabricante_id).first()
            if producto:
                producto.precio_compra = precio
                db.session.commit()
                logger.debug("Producto existente actualizado: %s", producto.id)
            else:
                producto = Producto(
                    nombre=nombre,
                    fabricante_id=fabricante_id,
                    precio_compra=precio,
                    moneda="COP"  # Puedes parametrizar este valor
                )
                db.session.add(producto)
                db.session.commit()
                logger.debug("Producto creado: %s", producto.id)
        except Exception as e:
            logger.exception("Error al crear o actualizar el producto")
            raise

        # 3. Crear el detalle de compra
        try:
            detalle = DetalleCompra(
                compra_id=compra.id,
                producto_id=producto.id,
                cantidad=cantidad
            )
            db.session.add(detalle)
            db.session.commit()
            logger.debug("Detalle de compra creado con ID: %s", detalle.id)
        except Exception as e:
            logger.exception("Error al crear el detalle de compra")
            raise

        # 4. Publicar evento a Pub/Sub para actualizar ms_inventarios
        try:
            logger.debug("Iniciando publicación a Pub/Sub...")
            project_id = os.getenv('GCP_PROJECT_ID', 'misw-4301-native-cloud-433702')
            topic_id = os.getenv('PUBSUB_TOPIC_ID', 'compras-topic')
            publisher = pubsub_v1.PublisherClient()
            topic_path = publisher.topic_path(project_id, topic_id)
            
            event_data = {
                "eventType": "DetalleCompraCreado",
                "compraId": compra.id,
                "productoId": producto.id,
                "cantidad": cantidad,
                "precio": precio,
                "nombre": producto.nombre,
                "fabricanteId": producto.fabricante_id
            }
            msg_str = json.dumps(event_data)
            
            future = publisher.publish(topic_path, data=msg_str.encode('utf-8'))
            logger.debug("Solicitud enviada, esperando resultado...")
            # Se espera un máximo de 10 segundos para obtener respuesta
            future.result(timeout=20)
            logger.debug("[PUBSUB] Evento publicado: %s", event_data)
            sys.stdout.flush()
        except Exception as e:
            logger.exception("[PUBSUB] Error publicando:")
            sys.stdout.flush()

        return compra, producto, detalle