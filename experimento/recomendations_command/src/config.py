import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('WRITE_DB_URI', 'postgresql://user:password@db_write/recomendaciones_command_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
