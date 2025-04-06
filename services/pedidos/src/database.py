import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class DataBase:
    def __init__(self):
        self.db_url = self.get_db_url()
        self.engine = create_engine(self.db_url, echo=True, connect_args={"check_same_thread": False} if "sqlite" in self.db_url else {}) ##echo=True para ver las consultas SQL // false para no verlas
        self.Session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)


    def get_db_url(self):
        """ Construye la URL de la base de datos desde variables de entorno. """
        db_type = os.getenv("DB_TYPE", "sqlite")  # Por defecto usa SQLite
        db_user = os.getenv("DB_USER", "")
        db_pass = os.getenv("DB_PASSWORD", "")
        db_host = os.getenv("DB_HOST", "")
        db_port = os.getenv("DB_PORT", "")
        db_name = os.getenv("DB_NAME", "database")
        print(f"DEBUG: db_type 1 = {db_type}")

        if db_type == "sqlite":
            return f"sqlite:///./{db_name}.db"  # Base de datos local
        return f"{db_type}://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

    def create_engine(self):
        """ Crea el motor de SQLAlchemy basado en la URL de la base de datos. """
        db_url = self.get_db_url()
        return create_engine(db_url, echo=True, connect_args={"check_same_thread": False} if "sqlite" in db_url else {})

# Instancia de la base de datos
database = DataBase()
Session = database.Session
engine = database.engine