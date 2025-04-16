# ./models/model.py

from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import declarative_base
import uuid
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()


class Model():
    # Definir las columnas
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    createdAt = Column(DateTime, default=datetime.utcnow)  # Usa default para crear automáticamente el valor
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # El valor se actualiza automáticamente
