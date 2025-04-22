import json
import os
from google.cloud import pubsub_v1

def publish_pedido_creado(pedido_dict: dict):
    publisher = pubsub_v1.PublisherClient()
    topic_name = 'projects/{project_id}/topics/{topic}'.format(
        project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
        topic=os.getenv('PEDIDO_CREADO_TOPIC')
    )
    future = publisher.publish(
        topic_name,
        data=json.dumps(pedido_dict).encode("utf-8")
    )    

    print("DEBUG: Pedido_Dict",pedido_dict)
    try:
        future.result()
    except:
        future.cancel()

def publish_pedido_creado_inventario(inventario_dict: dict):
    publisher = pubsub_v1.PublisherClient()
    topic_name = 'projects/{project_id}/topics/{topic}'.format(
        project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
        topic=os.getenv('PEDIDO_INVENTARIO_TOPIC')
    )
    future = publisher.publish(
        topic_name,
        data=json.dumps(inventario_dict).encode("utf-8")
    )
    print("DEBUG: Inventario_Dict",inventario_dict)
    try:
        future.result()
    except:
        future.cancel()
