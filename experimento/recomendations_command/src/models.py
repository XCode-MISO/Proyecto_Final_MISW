from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class VideoProcess(db.Model):
    __tablename__ = 'video_process'
    job_id = db.Column(db.Integer, primary_key=True)
    video_url = db.Column(db.String, nullable=False)
    status = db.Column(db.String(50), nullable=False)  # 'pending', 'processing'
    video_metadata = db.Column(db.JSON)  # Renombrado, antes 'metadata'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
