class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', "postgresql://user:password@db_write/recomendaciones_command_db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
