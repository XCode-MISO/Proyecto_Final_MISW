import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', "postgresql://user:admin@localhost:5432/routes_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
