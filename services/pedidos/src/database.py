import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class DataBase:
    def __init__(self):
        self.db_url = self.get_db_url()
        self.engine = create_engine(
            self.db_url, 
            echo=True, 
            connect_args={"check_same_thread": False} if "sqlite" in self.db_url else {}
        )
        self.Session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_db_url(self):
        """ Construye la URL de la base de datos desde variables de entorno. """
        db_type = os.getenv("DB_TYPE")
        DATABASE_USER = os.getenv("DATABASE_USER")
        db_pass = os.getenv("DATABASE_PASSWORD")
        DATABASE_URL = os.getenv("DATABASE_URL")
        DATABASE_PORT = os.getenv("DATABASE_PORT")
        DATABASE_NAME = os.getenv("DATABASE_NAME")

        print(f"DEBUG: db_type = {db_type}")

        if db_type == "":
            raise ValueError("No tiene DB Type  - no permitido en este entorno.")
        
        if not all([db_type, DATABASE_USER, db_pass, DATABASE_URL, DATABASE_PORT, DATABASE_NAME]):
            raise ValueError("Faltan variables de entorno necesarias para la conexión a la base de datos.")

        return f"{db_type}://{DATABASE_USER}:{db_pass}@{DATABASE_URL}:{DATABASE_PORT}/{DATABASE_NAME}"

# Instancia de la base de datos
database = DataBase()
Session = database.Session
engine = database.engine
