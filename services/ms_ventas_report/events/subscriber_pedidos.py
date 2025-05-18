import os
import json
import logging
from datetime import datetime
import threading
import traceback

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Determinar si estamos en Docker
in_docker = os.path.exists("/.dockerenv")

# Importar modelos siempre
from models.db import db
from models.reporte import ReporteVentas

# Intentar importar Pub/Sub solo si estamos en Docker
if in_docker:
    try:
        from google.cloud import pubsub_v1
        PUBSUB_AVAILABLE = True
    except ImportError:
        logger.warning("⚠️ Google Cloud Pub/Sub no disponible")
        PUBSUB_AVAILABLE = False
else:
    PUBSUB_AVAILABLE = False

# URL base para consultar el inventario
INVENTORY_BASE = os.getenv("INVENTORY_BASE", "http://kubernetes-gateway.cppxcode.shop/inventario")
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "/app/credentials.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_CREDENTIALS

# Variables para Pub/Sub
PROJECT_ID = os.getenv("GCP_PROJECT_ID", "misw-4301-native-cloud-433702")
SUBSCRIPTION_ID = os.getenv("PEDIDOS_VENTAS_SUBSCRIPTION_ID", "PedidoCreado-ventas-sub")


def get_producto_nombre(producto_id):
    """Función para obtener el nombre del producto desde la API de inventario"""
    import requests
    
    try:
        url = f"{INVENTORY_BASE}/api/inventarios/{producto_id}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        producto_data = response.json()
        nombre = producto_data.get("nombre", f"Producto {producto_id}")
        logger.info(f"Obtenido nombre '{nombre}' para producto ID {producto_id}")
        return nombre
    except Exception as e:
        logger.error(f"Error al obtener información del producto {producto_id}: {e}")
        return f"Producto {producto_id}"


def callback(message):
    """Procesa los mensajes recibidos del tópico de pedidos"""
    from app import create_app
    app = create_app()
    
    with app.app_context():
        try:
            data_str = message.data.decode('utf-8')
            pedido = json.loads(data_str)
            logger.info(f"[PUBSUB] Mensaje de pedido recibido: {pedido}")

            # Extraer la fecha del pedido
            delivery_date_str = pedido.get("deliveryDate")
            if delivery_date_str:
                # Formatear la fecha correctamente
                if "T" in delivery_date_str:  # Formato ISO
                    delivery_date = datetime.fromisoformat(delivery_date_str.replace('Z', '+00:00'))
                else:  # Formato YYYY-MM-DD
                    delivery_date = datetime.strptime(delivery_date_str, '%Y-%m-%d')
            else:
                delivery_date = datetime.utcnow()
                
            # Extraer el ID del vendedor
            vendedor_id = None
            
            # Primera opción: campo sellerId
            if "sellerId" in pedido:
                vendedor_id = pedido.get("sellerId")
            # Segunda opción: objeto vendedor
            elif "vendedor" in pedido and isinstance(pedido["vendedor"], dict):
                vendedor_id = pedido["vendedor"].get("id")
            else:
                vendedor_id = "desconocido"
            
            # Procesar los productos
            productos = []
            
            # Verificar si hay un campo products que sea una lista
            if "products" in pedido and isinstance(pedido["products"], list):
                # Iterar por cada producto en la lista
                for producto in pedido["products"]:
                    # Obtener ID y cantidad
                    producto_id = producto.get("id")
                    cantidad = producto.get("amount", 1)
                    
                    if producto_id:
                        productos.append({
                            "id": producto_id,
                            "cantidad": cantidad
                        })
            # Verificar si hay un campo productId directo
            elif "productId" in pedido:
                producto_id = pedido.get("productId")
                cantidad = pedido.get("quantity", 1)
                productos.append({
                    "id": producto_id,
                    "cantidad": cantidad
                })
            
            # Si no hay productos, reportar y confirmar mensaje
            if not productos:
                logger.warning("El mensaje no contiene productos válidos, ignorando")
                message.ack()
                return
            
            # Procesar cada producto como un reporte separado
            for producto_info in productos:
                producto_id = producto_info["id"]
                cantidad = producto_info["cantidad"]
                
                # Obtener el nombre del producto
                producto_nombre = get_producto_nombre(producto_id)
                
                # Crear el registro para el reporte
                reporte = ReporteVentas(
                    producto=producto_nombre,
                    cantidad=cantidad,
                    fecha=delivery_date.date(),  # Solo la fecha, no la hora
                    vendedor_id=vendedor_id
                )
                
                # Guardar en la base de datos
                db.session.add(reporte)
            
            # Hacer commit de todos los reportes a la vez
            db.session.commit()
            logger.info(f"[PUBSUB] {len(productos)} reportes creados para el pedido {pedido.get('id', 'N/A')}")
            
            # Confirmar procesamiento del mensaje
            message.ack()
            
        except Exception as e:
            logger.error(f"[PUBSUB] Error procesando mensaje: {e}")
            import traceback
            traceback.print_exc()
            # No confirmar el mensaje para reprocesarlo
            message.nack()


def start_pedidos_subscriber():
    """Inicia la suscripción a eventos de pedidos si Pub/Sub está disponible"""
    if not PUBSUB_AVAILABLE:
        logger.warning("⚠️ No se puede iniciar el suscriptor: Pub/Sub no disponible")
        # Ejecutar simulador como alternativa
        simular_eventos_pedidos()
        return
    
    try:
        logger.info(f"Iniciando suscriptor de pedidos: {SUBSCRIPTION_ID}")
        
        subscriber = pubsub_v1.SubscriberClient()
        subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)
        
        # Callback y opciones de flujo
        streaming_pull_future = subscriber.subscribe(
            subscription_path, 
            callback=callback,
            flow_control=pubsub_v1.types.FlowControl(max_messages=10)
        )
        
        logger.info(f"Escuchando mensajes en {subscription_path}")
        
        # Esperar por mensajes de forma indefinida
        try:
            # Bloquear hasta que ocurra una excepción o se cancele
            streaming_pull_future.result()
        except Exception as e:
            streaming_pull_future.cancel()
            logger.error(f"Excepción en suscripción: {e}")
            
    except Exception as e:
        logger.error(f"Error iniciando suscriptor: {e}")
        # Ejecutar simulador como alternativa
        simular_eventos_pedidos()


def simular_eventos_pedidos():
    """Simula la recepción de eventos de pedidos para pruebas"""
    from app import create_app  # Cambiado de app_simple a app
    app = create_app()
    
    # Eventos simulados
    eventos_simulados = [
        {
            "id": "pedido-simulado-001",
            "productId": "producto-simulado-101",
            "quantity": 2,
            "sellerId": "vendedor-simulado-001",
            "deliveryDate": datetime.utcnow().isoformat() + "Z"
        },
        {
            "id": "pedido-simulado-002",
            "productId": "producto-simulado-102",
            "quantity": 5,
            "sellerId": "vendedor-simulado-002",
            "deliveryDate": datetime.utcnow().isoformat() + "Z"
        }
    ]
    
    with app.app_context():
        for evento in eventos_simulados:
            try:
                # Crear reporte a partir del evento simulado
                reporte = ReporteVentas(
                    producto=f"Producto Simulado {evento['productId']}",
                    cantidad=evento['quantity'],
                    fecha=datetime.utcnow().date(),
                    vendedor_id=evento['sellerId']
                )
                
                db.session.add(reporte)
                logger.info(f"✅ Creado registro simulado para: {reporte.producto}")
            
            except Exception as e:
                logger.error(f"❌ Error procesando evento simulado: {e}")
                db.session.rollback()
        
        # Commit de todos los cambios
        db.session.commit()
        logger.info("✅ Todos los eventos simulados procesados correctamente")