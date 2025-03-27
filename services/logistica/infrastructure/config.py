import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', "postgresql://user:password@localhost:5433/db-routes")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
