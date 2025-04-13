from marshmallow import Schema, fields
from sqlalchemy import Column, String, DateTime, Float, ForeignKey
from .model import Model, Base
from datetime import datetime, timedelta
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID  # Import UUID
from sqlalchemy.orm import relationship


class Visit(Model, Base):
    __tablename__ = 'visits'
    #client_id = Column(UUID(as_uuid=True), ForeignKey('clients.id'), nullable=False)  # Add this line
    client_id = Column(String(36), ForeignKey('clients.id'), nullable=False)  # Add this line
    informe  = Column(String)
    fechaVisita = Column(DateTime)    
    latitud = Column(Float)
    longitud = Column(Float)
    client = relationship("Client", back_populates="visitas")  # Add this line


    def __init__(self, client_id, informe, fechaVisita, latitud, longitud):
        Model.__init__(self)
        self.client_id = client_id
        self.informe = informe
        self.fechaVisita =fechaVisita
        self.latitud =latitud
        self.longitud =longitud

class VisitSchema(Schema):
    id = fields.Str()
    client_id = fields.Str()
    informe = fields.Str()
    fechaVisita = fields.DateTime()
    latitud = fields.Float()
    longitud = fields.Float()
    createdAt = fields.DateTime()
    updatedAt = fields.DateTime()

class CreatedVisitJsonSchema(Schema):
    id = fields.UUID()
    createdAt = fields.DateTime()

class VisitJsonSchema(Schema):
    id = fields.UUID()
    client_id = fields.UUID()
    informe = fields.Str()
    fechaVisita = fields.DateTime()
    latitud = fields.Float()
    longitud = fields.Float()