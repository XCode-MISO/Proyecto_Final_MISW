import os
import json
import sys
import logging
import csv
import io
from models.db import db
from models.producto import Producto
from models.fabricante import Fabricante
from google.cloud import pubsub_v1

from typing import Dict, List
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/esneiderrestrepo/Documents/credentials.json"

# Configuración del logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

EXPECTED_HEADERS = [
    "nombre",
    "fabricante_id",
    "cantidad",
    "precio",
    "moneda",
    "bodega",
    "estante",
    "pasillo",
]
HEADER_ALIASES: Dict[str, str] = {"fabricanteId": "fabricante_id"}
VALID_CURRENCIES = {"COP", "USD"}


class ProductoService:

     # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _assert_fabricante_exists(fabricante_id: int):
        if Fabricante.query.get(fabricante_id) is None:
            raise ValueError(f"Fabricante {fabricante_id} no existe")


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
                producto.precio = precio
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
    

    @staticmethod
    def upload_productos_from_file(file_content: str) -> dict:
        reader = csv.DictReader(io.StringIO(file_content))
        headers_original = reader.fieldnames or []
        mapped = [HEADER_ALIASES.get(h, h) for h in headers_original]
        reader.fieldnames = mapped
        faltantes = [h for h in EXPECTED_HEADERS if h not in mapped]
        if faltantes:
            return {"inserted": 0, "errors": [f"Faltan columnas: {faltantes}"]}

        service = ProductoService()
        inserted, errors = 0, []
        for line_num, row in enumerate(reader, start=2):
            try:
                moneda = row["moneda"].strip().upper()
                if moneda not in VALID_CURRENCIES:
                    raise ValueError("Moneda inválida (COP o USD)")
                fabricante_id = int(row["fabricante_id"])
                service._assert_fabricante_exists(fabricante_id)
                service.registrar_producto_individual(
                    nombre=row["nombre"].strip(),
                    fabricante_id=fabricante_id,
                    cantidad=int(row["cantidad"]),
                    precio=float(row["precio"]),
                    moneda=moneda,
                    bodega=row["bodega"].strip(),
                    estante=row["estante"].strip(),
                    pasillo=row["pasillo"].strip(),
                )
                inserted += 1
            except Exception as exc:
                errors.append(f"Fila {line_num}: {exc}")
        return {"inserted": inserted, "errors": errors}

