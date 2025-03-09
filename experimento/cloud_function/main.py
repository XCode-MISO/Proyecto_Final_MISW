import os
import json
import logging

from google.cloud import videointelligence
from google.cloud import pubsub_v1
from google.protobuf.json_format import MessageToJson

def process_video(event, context):
    logging.info("========== INICIO DE LA FUNCIÓN process_video ==========")
    logging.info(f"FULL EVENT PAYLOAD:\n{json.dumps(event, indent=2)}")
    logging.info(f"CONTEXT: event_id={context.event_id}, timestamp={context.timestamp}, event_type={context.event_type}")

    metadata_dict = event.get('metadata', {})
    job_id = metadata_dict.get('job_id')
    
    if not job_id:
        logging.warning("No se encontró job_id en el evento.")
        return

    bucket = event.get('bucket')
    file_name = event.get('name')
    if not bucket or not file_name:
        logging.warning("No se encontró 'bucket' o 'name' en el evento.")
        return

    video_uri = f"gs://{bucket}/{file_name}"
    logging.info(f"Procesando video_uri={video_uri} con job_id={job_id}")

    # Variable para almacenar el JSON del resultado (dummy o real)
    metadata_json_str = None

    try:
        client = videointelligence.VideoIntelligenceServiceClient()
        features = [videointelligence.Feature.LABEL_DETECTION]
        operation = client.annotate_video(input_uri=video_uri, features=features)
        result = operation.result(timeout=300)
        annotation_results = result.annotation_results[0]
        metadata_json_str = MessageToJson(annotation_results._pb)
    except Exception as e:
        error_msg = str(e)
        logging.error(f"Error en el procesamiento del video: {error_msg}")
        # Si se detecta error de cuota, se envían datos dummy
        if "429" in error_msg or "RATE_LIMIT_EXCEEDED" in error_msg:
            logging.info("Capturado error de cuota (429). Se enviarán datos dummy.")
            dummy_result = {
                "dummy": True,
                "message": "No se pudo procesar el video debido a cuota excedida",
                "error_detail": error_msg
            }
            metadata_json_str = json.dumps(dummy_result)
        else:
            # Para otros tipos de error, se podría reintentar o simplemente salir
            return

    # Publicar el resultado en Pub/Sub
    event_data = {
        "job_id": job_id,
        "video_uri": video_uri,
        "metadata": json.loads(metadata_json_str)
    }
    message_data = json.dumps(event_data)
    logging.info(f"Publicando mensaje en Pub/Sub: {message_data}")

    try:
        publisher = pubsub_v1.PublisherClient()
        project_id = os.environ.get("GCP_PROJECT")
        if not project_id:
            raise Exception("GCP_PROJECT no está definido en las variables de entorno.")
        topic_name = os.environ.get("PUBSUB_TOPIC", "video-procesado-topic")
        topic_path = publisher.topic_path(project_id, topic_name)
        future = publisher.publish(topic_path, data=message_data.encode("utf-8"))
        published_id = future.result()
        logging.info(f"Mensaje publicado en Pub/Sub, ID={published_id}")
    except Exception as e:
        logging.error(f"Error publicando mensaje en Pub/Sub: {e}")
        return

    logging.info("========== FIN DE LA FUNCIÓN process_video ==========")