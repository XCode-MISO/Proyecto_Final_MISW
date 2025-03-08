import os
from google.cloud import storage
from src.models import db, VideoProcess

def upload_to_cloud_storage(file_path, job_id):
    """
    Sube el archivo al bucket de Cloud Storage, añade el job_id como metadato
    y devuelve la URL pública del objeto.
    """
    bucket_name = os.environ.get("VIDEO_BUCKET")
    if not bucket_name:
        raise Exception("VIDEO_BUCKET no está definido en las variables de entorno.")
    
    project = os.environ.get("GCP_PROJECT")
    if not project:
        raise Exception("GCP_PROJECT no está definido en las variables de entorno.")
    
    client = storage.Client(project=project)
    bucket = client.bucket(bucket_name)
    blob_name = os.path.basename(file_path)
    blob = bucket.blob(blob_name)

    blob.upload_from_filename(file_path, predefined_acl="publicRead")
    
    blob.metadata = {"job_id": str(job_id)}
    blob.patch()  
    
    return blob.public_url

def register_video(video_file_path, db, VideoProcess):
    """
    Registra el video en la base de datos con estado 'pending',
    genera un job_id, sube el video a Cloud Storage (incluyendo el job_id como metadato)
    y actualiza el registro con la URL pública del video.
    """
    video = VideoProcess(video_url=video_file_path, status='pending')
    db.session.add(video)
    db.session.commit()  

    public_url = upload_to_cloud_storage(video_file_path, video.job_id)
    
    video.video_url = public_url
    db.session.commit()
    
    return video.job_id, video.status