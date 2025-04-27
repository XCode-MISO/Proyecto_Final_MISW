import os
from google.cloud import storage
from src.models import db, VideoProcess

def upload_to_cloud_storage(file_obj, blob_name, job_id):
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
    blob = bucket.blob(blob_name)
    blob.metadata = {"job_id": str(job_id)}
    
    # Asegurarse de que el puntero del archivo esté al inicio.
    file_obj.seek(0)
    blob.upload_from_file(file_obj, predefined_acl="publicRead")
    
    blob.patch()  
    return blob.public_url

def register_video(file_obj, filename, db, VideoProcess):
    """
    Registra el video en la base de datos con estado 'pending',
    genera un job_id, sube el video a Cloud Storage (incluyendo el job_id como metadato)
    y actualiza el registro con la URL pública del video.
    """
    video = VideoProcess(video_url=filename, status='pending')
    db.session.add(video)
    db.session.commit()  

    public_url = upload_to_cloud_storage(file_obj, filename, video.job_id)
    
    video.video_url = public_url
    db.session.commit()
    
    return video.job_id, video.status