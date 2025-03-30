from marshmallow import Schema, fields
from sqlalchemy import Column, String, DateTime, Float
from .model import Model, Base
from datetime import datetime, timedelta
from uuid import uuid4
from sqlalchemy.orm import relationship

class Client(Model, Base):
    __tablename__ = 'clients'
    nombre = Column(String)
    correo = Column(String)
    direccion = Column(String)
    telefono = Column(String)
    latitud = Column(Float)
    longitud = Column(Float)
    visitas = relationship("Visit", back_populates="client")  # Add this line


    def __init__(self, nombre, correo, direccion, telefono, latitud, longitud):
        Model.__init__(self)
        self.nombre = nombre
        self.correo = correo
        self.direccion = direccion
        self.telefono = telefono
        self.latitud = latitud
        self.longitud = longitud


class ClientSchema(Schema):
    id = fields.UUID()
    nombre = fields.Str()
    correo = fields.Str()
    direccion = fields.Str()
    telefono = fields.Str()
    latitud = fields.Float()
    longitud = fields.Float()
    createdAt = fields.DateTime()
    updatedAt = fields.DateTime()

class CreatedClientJsonSchema(Schema):
    id = fields.UUID()
    createdAt = fields.DateTime()

class ClientJsonSchema(Schema):
    id = fields.UUID()
    nombre = fields.Str()
    correo = fields.Str()
    direccion = fields.Str()
    telefono = fields.Str()
    latitud = fields.Float()
    longitud = fields.Float()