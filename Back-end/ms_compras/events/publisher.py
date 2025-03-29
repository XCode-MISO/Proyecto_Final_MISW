import os
import json
from google.cloud import pubsub_v1

def publish_compra_realizada(event_data: dict):
    """
    Publica el evento en Google Pub/Sub (tópico = PUBSUB_TOPIC_ID)
    """
    project_id = os.getenv('GCP_PROJECT_ID', 'misw-4301-native-cloud-433702')
    topic_id   = os.getenv('PUBSUB_TOPIC_ID', 'compras-topic')

    publisher  = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    msg_str = json.dumps(event_data)
    future  = publisher.publish(topic_path, data=msg_str.encode('utf-8'))
    future.result()  # bloquear hasta publicarse
    print(f"[PUBSUB] Evento publicado: {event_data}")