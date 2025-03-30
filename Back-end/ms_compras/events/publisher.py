import os
import sys
import json
from google.cloud import pubsub_v1

def publish_compra_realizada(event_data: dict):
    try:
        project_id = os.getenv('GCP_PROJECT_ID', 'misw-4301-native-cloud-433702')
        topic_id = os.getenv('PUBSUB_TOPIC_ID', 'compras-topic')
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(project_id, topic_id)
        msg_str = json.dumps(event_data)
        future = publisher.publish(topic_path, data=msg_str.encode('utf-8'))
        future.result()  # Espera a que el mensaje se publique
        print(f"[PUBSUB] Evento publicado: {event_data}")
        sys.stdout.flush()
    except Exception as e:
        print(f"[PUBSUB] Error publicando: {str(e)}")
        sys.stdout.flush()