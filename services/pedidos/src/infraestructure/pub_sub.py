import json
import os
from google.cloud import pubsub_v1

from src.models.pedido import Pedido, PedidoInvetnacioSchema


def publish_pedido_creado(pedido: Pedido):
  publisher = pubsub_v1.PublisherClient()
  topic_name = 'projects/{project_id}/topics/{topic}'.format(
      project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
      topic=os.getenv('PEDIDO_DESPACHADO_TOPIC')
  )
  future = publisher.publish(
      topic_name, 
      data=pedido.toJSON().encode()
    )
  try:
    future.result()
  except:
     future.cancel()

def publish_pedido_creado_inventario(pedidoInventario: PedidoInvetnacioSchema):
  publisher = pubsub_v1.PublisherClient()
  topic_name = 'projects/{project_id}/topics/{topic}'.format(
      project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
      topic=os.getenv('PEDIDO_DESPACHADO_TOPIC')
  )
  future = publisher.publish(
      topic_name, 
      data=pedidoInventario.toJSON().encode()
    )
  try:
    future.result()
  except:
     future.cancel()