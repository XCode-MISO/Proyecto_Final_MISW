from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

class SessionConfig():
    def __init__(self):
        ...

    def url(self):
        db_user = os.environ['DATABASE_USER']
        db_pass = os.environ['DATABASE_PASSWORD']
        db_host = os.environ['DATABASE_URL']
        db_port = os.environ['DATABASE_PORT']
        db_name = os.environ['DATABASE_NAME']
        return f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'


session_config = SessionConfig()
engine = create_engine(session_config.url())
Session = sessionmaker(bind=engine)