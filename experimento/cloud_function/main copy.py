import os
import json
import logging

from google.cloud import videointelligence
from google.cloud import pubsub_v1
from google.protobuf.json_format import MessageToJson

def process_video(event, context):
    """
    Se activa cuando se sube un objeto (video) al bucket.
    1. Loguea el contenido completo de 'event' para inspeccionar la estructura.
    2. Lee el 'job_id' desde la metadata definida por el usuario (sin usar context.event_id).
    3. Llama a Video Intelligence API para analizar el video.
    4. Publica un mensaje en Pub/Sub con el job_id y el resultado de la anotación del video.
    """

    # 1. Loguear el contenido completo de 'event'
    logging.info("========== INICIO DE LA FUNCIÓN process_video ==========")
    logging.info(f"FULL EVENT PAYLOAD:\n{json.dumps(event, indent=2)}")
    logging.info(f"CONTEXT: event_id={context.event_id}, timestamp={context.timestamp}, event_type={context.event_type}")

    # 2. Obtener la metadata del evento (puede ser event["metadata"] o event["object"]["metadata"])
    #    Dependiendo de cómo llegue la estructura en tu proyecto. Revisa los logs para ver la ruta real.
    #    En este ejemplo, asumimos que la metadata está en event["metadata"].
    metadata_dict = event.get('metadata', {})
    job_id = metadata_dict.get('job_id')
    
    # Si tu estructura real es "object": {"metadata": {"job_id": "..." }}, usarías:
    # metadata_dict = event.get('object', {}).get('metadata', {})
    # job_id = metadata_dict.get('job_id')

    if not job_id:
        # Si no hay job_id, no hacemos fallback a context.event_id para evitar IDs gigantes.
        logging.warning(f"FULL EVENT PAYLOAD:\n{json.dumps(event, indent=2)}")
        return

    bucket = event.get('bucket')
    file_name = event.get('name')
    if not bucket or not file_name:
        logging.warning("No se encontró 'bucket' o 'name' en el evento. Se ignora este evento.")
       
        return

    video_uri = f"gs://{bucket}/{file_name}"
    logging.info(f"Procesando video_uri={video_uri} con job_id={job_id}")

    # 3. Llamar a Video Intelligence
    try:
        client = videointelligence.VideoIntelligenceServiceClient()
        features = [videointelligence.Feature.LABEL_DETECTION]
        operation = client.annotate_video(input_uri=video_uri, features=features)
        result = operation.result(timeout=300)
        annotation_results = result.annotation_results[0]

        # Convertir a JSON la parte interna _pb del mensaje protobuf
        metadata_json_str = MessageToJson(annotation_results._pb)
    except Exception as e:
        logging.error(f"Error en el procesamiento del video: {e}")
        return  # Podrías relanzar si prefieres

    # 4. Publicar el resultado en Pub/Sub
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