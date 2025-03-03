import os
import json
import logging
from google.cloud import videointelligence
from google.cloud import pubsub_v1

def process_video(event, context):
    """
    Se activa cuando se sube un video al bucket.
    Lee el job_id de la metadata del objeto, analiza el video mediante la Video Intelligence API,
    y publica un mensaje en Pub/Sub con el job_id y el resultado.
    """
    bucket = event.get('bucket')
    file_name = event.get('name')
    
    custom_metadata = event.get('metadata', {})
    job_id = custom_metadata.get('job_id') if custom_metadata else None
    if not job_id:
        job_id = context.event_id

    video_uri = f"gs://{bucket}/{file_name}"
    logging.info(f"Procesando video: {video_uri} con job_id: {job_id}")

    client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.LABEL_DETECTION]
    operation = client.annotate_video(input_uri=video_uri, features=features)
    result = operation.result(timeout=300)
    annotation_results = result.annotation_results[0]
    metadata_json = videointelligence.types.VideoAnnotationResults.to_json(annotation_results)

    event_data = {
        "job_id": job_id,
        "video_uri": video_uri,
        "metadata": json.loads(metadata_json)
    }
    message_data = json.dumps(event_data)
    logging.info(f"Publicando mensaje en Pub/Sub: {message_data}")

    publisher = pubsub_v1.PublisherClient()
    project_id = os.environ.get("GCP_PROJECT")
    topic = os.environ.get("PUBSUB_TOPIC", "video-procesado-topic")
    topic_path = publisher.topic_path(project_id, topic)
    future = publisher.publish(topic_path, data=message_data.encode("utf-8"))
    logging.info(f"Mensaje publicado, ID: {future.result()}")