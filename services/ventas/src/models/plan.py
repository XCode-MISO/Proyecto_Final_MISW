from .model import Model, Base
from marshmallow import Schema, fields
from sqlalchemy import Column, Date, ForeignKey, String, String, Table
from sqlalchemy.orm import relationship

class SellerSchema(Schema):
    id = fields.UUID()
    nombre = fields.Str()
    correo = fields.Str()
    direccion = fields.Str()
    telefono = fields.Str()
    latitud = fields.Float()
    longitud = fields.Float()
    imagen = fields.Str()

class SellerJsonSchema(Schema):
    id = fields.UUID()
    nombre = fields.Str()
    correo = fields.Str()
    direccion = fields.Str()
    telefono = fields.Str()
    latitud = fields.Float()
    longitud = fields.Float()
    imagen = fields.Str()

plan_seller_association = Table(
    'plan_seller_association',
    Base.metadata,
    Column('plan_id', String, ForeignKey('plans.id'), primary_key=True),
    Column('seller_id', String, ForeignKey('sellers.id'), primary_key=True)
)


class Plan(Model, Base):
    __tablename__ = 'plans'
    fecha = Column(Date, nullable=False)
    descripcion = Column(String)
    vendedores = relationship("Seller",
                              secondary=plan_seller_association,
                              back_populates="plans", lazy='subquery')

    def __init__(self, vendedores, fecha, descripcion):
        Model.__init__(self)
        self.vendedores = vendedores
        self.fecha = fecha
        self.descripcion = descripcion


class PlanSchema(Schema):
    id = fields.UUID()
    vendedores = fields.List(fields.Nested(SellerJsonSchema))
    fecha = fields.DateTime()
    descripcion = fields.Str()


class CreatedPlanJsonSchema(Schema):
    id = fields.UUID()
    createdAt = fields.DateTime()


class PlanJsonSchema(Schema):
    id = fields.UUID()
    vendedores = fields.List(fields.Nested(SellerJsonSchema))
    fecha = fields.Date()
    descripcion = fields.Str()
