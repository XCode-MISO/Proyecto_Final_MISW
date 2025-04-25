from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Recommendation(db.Model):
    __tablename__ = 'recomendacion'
    job_id = db.Column(db.Integer, primary_key=True)
    final_state = db.Column(db.String(50), nullable=False)
    final_recommendation = db.Column(db.Text)
    recommendation_data = db.Column(db.JSON)
    identified_objects = db.Column(db.JSON) 
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
