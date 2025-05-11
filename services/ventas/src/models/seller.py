from marshmallow import Schema, fields
from sqlalchemy import Column, String, Float
from sqlalchemy.orm import relationship
from .model import Model, Base
from .plan import plan_seller_association

class Seller(Model, Base):
    __tablename__ = 'sellers'
    nombre = Column(String)
    correo = Column(String)
    direccion = Column(String)
    telefono = Column(String)
    latitud = Column(Float)
    longitud = Column(Float)
    imagen= Column(String)

    plans = relationship(
        "Plan",
        secondary=plan_seller_association,
        back_populates="vendedores"
    )


    def __init__(self, nombre, correo, direccion, telefono, latitud, longitud, imagen):
        Model.__init__(self)
        self.nombre = nombre
        self.correo = correo
        self.direccion = direccion
        self.telefono = telefono
        self.latitud = latitud
        self.longitud = longitud
        self.imagen = imagen


class SellerSchema(Schema):
    id = fields.UUID()
    nombre = fields.Str()
    correo = fields.Str()
    direccion = fields.Str()
    telefono = fields.Str()
    latitud = fields.Float()
    longitud = fields.Float()
    createdAt = fields.DateTime()
    updatedAt = fields.DateTime()
    imagen = fields.Str()

class CreatedSellerJsonSchema(Schema):
    id = fields.UUID()
    createdAt = fields.DateTime()

class SellerJsonSchema(Schema):
    id = fields.UUID()
    nombre = fields.Str()
    correo = fields.Str()
    direccion = fields.Str()
    telefono = fields.Str()
    latitud = fields.Float()
    longitud = fields.Float()
    imagen = fields.Str()