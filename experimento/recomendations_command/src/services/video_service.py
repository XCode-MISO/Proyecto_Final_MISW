def register_video(video_file_path, db, VideoProcess):
    """
    Lógica de negocio para registrar la solicitud del video.
    """
    video = VideoProcess(video_url=video_file_path, status='pending')
    db.session.add(video)
    db.session.commit()
    return video.job_id, video.status
