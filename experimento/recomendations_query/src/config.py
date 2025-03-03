import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI', 'postgresql://user:password@db_read/recomendaciones_query_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
