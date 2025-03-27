import os
from logistica.application.services.generate_route import generate_route
from google.cloud import pubsub_v1

def publish_pedido_despachado(route):
  publisher = pubsub_v1.PublisherClient()
  topic_name = 'projects/{project_id}/topics/{topic}'.format(
      project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
      topic='MY_TOPIC_NAME',  # Set this to something appropriate.
  )
  publisher.create_topic(name=topic_name)
  future = publisher.publish(topic_name, b'My first message!', spam='eggs')
  future.result()

def consume_pedido_creado():
  topic_name = 'projects/{project_id}/topics/{topic}'.format(
      project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
      topic='MY_TOPIC_NAME',  # Set this to something appropriate.
  )

  subscription_name = 'projects/{project_id}/subscriptions/{sub}'.format(
      project_id=os.getenv('GOOGLE_CLOUD_PROJECT'),
      sub='MY_SUBSCRIPTION_NAME',  # Set this to something appropriate.
  )

  def callback(message):
    # TODO: parse message
    route = generate_route()
    publish_pedido_despachado(route)
    message.ack()

  with pubsub_v1.SubscriberClient() as subscriber:
      subscriber.create_subscription(
          name=subscription_name, topic=topic_name)
      subscriber.subscribe(subscription_name, callback)