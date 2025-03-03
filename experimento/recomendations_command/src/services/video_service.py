import os
import json
from google.cloud import pubsub_v1
from src.models import db, VideoProcess

def publish_job_id(job_id, file_info=None):
    """
    Publica un mensaje en Pub/Sub con el job_id y opcionalmente información adicional.
    """
    publisher = pubsub_v1.PublisherClient()
    project_id = os.environ.get("GCP_PROJECT")

    topic = os.environ.get("PUBSUB_TOPIC", "video-jobs-topic")
    topic_path = publisher.topic_path(project_id, topic)
    message_data = {"job_id": job_id}
    if file_info:
        message_data["file_info"] = file_info
    message_str = json.dumps(message_data)
    future = publisher.publish(topic_path, data=message_str.encode("utf-8"))
    future.result() 
    return message_str

def register_video(video_file_path, db, VideoProcess):
    """
    Registra el video en la base de datos con estado 'pending',
    genera un job_id y publica un mensaje en Pub/Sub con ese job_id.
    """

    video = VideoProcess(video_url=video_file_path, status='pending')
    db.session.add(video)
    db.session.commit()  

  
    publish_job_id(video.job_id, file_info={"local_path": video_file_path})
    
    return video.job_id, video.status