import uuid
from datetime import datetime, timedelta
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from .model import Base  
from marshmallow import Schema, fields, ValidationError


# Función de validación para deliveryDate (+2 días mínimo)
def validate_delivery_date(value):
    min_date = datetime.utcnow() + timedelta(days=2)
    if value < min_date:
        raise ValidationError(f"🚨 La fecha de entrega debe ser al menos {min_date.strftime('%Y-%m-%d %H:%M:%S')} UTC")


# Tabla intermedia para la relación muchos a muchos entre Pedido y Producto
pedido_producto = Table(
    'pedido_producto', Base.metadata,
    Column('pedido_id', String(36), ForeignKey('pedidos.id'), primary_key=True),
    Column('producto_id', String(36), ForeignKey('productos.id'), primary_key=True)
)


class Pedido(Base):
    __tablename__ = 'pedidos'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False)
    client_id = Column(String(36), ForeignKey('clientes.id'), nullable=False)  # Almacena el ID del cliente
    price = Column(Float, nullable=False)
    delivery_date = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relaciones
    client = relationship("Cliente", back_populates="pedidos", uselist=False)  # Relación opcional
    products = relationship("Producto", secondary=pedido_producto, back_populates="pedidos")

    def __init__(self, name, client_id, products, price, delivery_date):
        self.name = name
        self.client_id = client_id
        self.products = products
        self.price = price
        self.delivery_date = delivery_date


# Esquema para serializar un pedido completo como JSON
class PedidoJsonSchema(Schema):
    id = fields.Str()
    name = fields.Str(required=True)
    clientId = fields.Str(required=True)
    products = fields.List(fields.Str(), required=True)  # Lista de productos
    price = fields.Float(required=True)
    deliveryDate = fields.DateTime(required=True, format="iso", validate=validate_delivery_date)
    createdAt = fields.DateTime(dump_only=True)  # Solo se devuelve al serializar


# Esquema para la creación de un nuevo pedido (sin ID y fechas generadas automáticamente)
class PedidoSchema(Schema):
    name = fields.Str(required=True)
    clientId = fields.Str(required=True)
    products = fields.List(fields.Str(), required=True)
    price = fields.Float(required=True)
    deliveryDate = fields.DateTime(required=True, format="iso", validate=validate_delivery_date)
