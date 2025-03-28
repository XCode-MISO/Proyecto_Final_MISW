import json
import os
from logistica.application.services.generate_route import generate_route
from google.cloud import pubsub_v1

from logistica.domain.model import Route

def publish_pedido_despachado(route: Route):
  publisher = pubsub_v1.PublisherClient()
  topic_name = 'projects/{project_id}/topics/{topic}'.format(
      project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
      topic=os.getenv('PEDIDO_DESPACHADO_TOPIC')
  )
  future = publisher.publish(
      topic_name, 
      data=route.toJSON().encode()
    )
  try:
    future.result()
  except:
     future.cancel()

def consume_pedido_creado(appContext):
  subscription_name = 'projects/{project_id}/subscriptions/{sub}'.format(
      project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
      sub=os.getenv('PEDIDO_CREADO_SUB')
  )

  def callback(message):
    # TODO: parse message
    with appContext:
      print(message)
      def route(pedido):
        return pedido.get("cliente").get("direccion")
      pedidos = json.loads(message.data).get("pedidos")
        
      listOfPoints = list(map(route, pedidos))
      route = generate_route(listOfPoints, pedidos)
      publish_pedido_despachado(route)
      message.ack()

  with pubsub_v1.SubscriberClient() as subscriber:
      print(f'Subscribed succesfully to :{subscription_name}')
      future = subscriber.subscribe(subscription_name, callback)
      try:
          future.result()
      except KeyboardInterrupt:
          future.cancel()
