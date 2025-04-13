##src\models\pedido.py
from sqlite3 import Date
import uuid
from datetime import date, datetime, timedelta
from sqlalchemy import Column, String, Float, Date, ForeignKey, Table
from sqlalchemy.orm import relationship
from .model import Base,Model 
from marshmallow import Schema, fields, ValidationError
from .pedido_producto import PedidoProducto


# Función de validación para deliveryDate (+2 días Maximo)
def validate_deliveryDate(value):
    if isinstance(value, datetime):
        value = value.date()  # 💡 convertir si viene como datetime

    today = datetime.utcnow().date()
    max_date = today + timedelta(days=2)

    if not (today <= value <= max_date):
        raise ValidationError(
            f"La fecha de entrega debe ser entre hoy ({today}) y {max_date} inclusive (UTC)."
        )

class Pedido(Base, Model):
    __tablename__ = 'pedidos'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False)
    clientId = Column(String(36), ForeignKey('clientes.id'), nullable=False)  # Almacena el ID del cliente
    clientName = Column(String(50), nullable=False)  # Almacena el nombre del cliente
    vendedorId = Column(String(36), ForeignKey('vendedores.id'), nullable=False)  # Almacena el ID del vendedor
    vendedorName = Column(String(50), nullable=False)  # Almacena el nombre del vendedor
    price = Column(Float, nullable=False)
    state = Column(String(50), default="Pendiente", nullable=False)
    deliveryDate = Column(Date, nullable=False, default=lambda: (datetime.utcnow() + timedelta(days=2)).date()) # Sumar 2 días
 # Sumar 2 días


    # Relaciones
    client = relationship("Cliente", back_populates="pedidos", uselist=False)  # Relación opcional
    pedido_productos = relationship("PedidoProducto", back_populates="pedido")



    def __init__(self, name, clientId, clientName, products, price, state, deliveryDate, vendedorId=None, vendedorName=None):
        super().__init__()
        self.name = name
        self.clientId = clientId
        self.clientName = clientName
        self.vendedorId = vendedorId
        self.vendedorName = vendedorName
        self.price = price
        self.state = state
        self.deliveryDate = deliveryDate


# Esquema para la  visualizacion de productos en un pedido

class ProductoSchema(Schema):
    id = fields.UUID()
    name = fields.Str()
    price = fields.Float()
    amount = fields.Int()


# Esquema para serializar un pedido completo como JSON
class PedidoJsonSchema(Schema):
    id = fields.Str()
    name = fields.Str(required=True)    
    clientId = fields.Str()
    clientName = fields.Str()    
    vendedorId = fields.Str(allow_none=True)
    vendedorName = fields.Str(allow_none=True)
    products = fields.Nested(ProductoSchema, many=True)
    price = fields.Float(required=True)
    state = fields.Str(required=True)
    deliveryDate = fields.Date(required=True, format="iso", validate=validate_deliveryDate)
    createdAt = fields.DateTime(dump_only=True)  # Solo se devuelve al serializar


# Esquema para la creación de un nuevo pedido (sin ID y fechas generadas automáticamente)
class PedidoSchema(Schema):
    name = fields.Str(required=True)
    clientId = fields.Str(required=True)
    clientName = fields.Str(required=True)    
    vendedorId = fields.Str(required=False, allow_none=True)
    vendedorName = fields.Str(required=False, allow_none=True)
    products = fields.List(fields.Dict(keys=fields.Str(), values=fields.Raw()), required=True)
    state = fields.Str(missing="Pendiente")
    price = fields.Float(required=True)
    deliveryDate = fields.Date(required=True, format="iso", validate=validate_deliveryDate)

