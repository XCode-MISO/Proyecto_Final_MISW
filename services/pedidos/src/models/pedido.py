import uuid
from datetime import datetime, timedelta
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from .model import Base,Model 
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


class Pedido(Base, Model):
    __tablename__ = 'pedidos'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False)
    clientId = Column(String(36), ForeignKey('clientes.id'), nullable=False)  # Almacena el ID del cliente
    price = Column(Float, nullable=False)
    state = Column(String(50), default="Pendiente", nullable=False)
    delivery_date = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relaciones
    client = relationship("Cliente", back_populates="pedidos", uselist=False)  # Relación opcional
    products = relationship("Producto", secondary=pedido_producto, back_populates="pedidos")

    def __init__(self, name, clientId, products, price, state, delivery_date):
        super().__init__() # Llama al constructor de Model
        self.name = name
        self.clientId = clientId
        self.products = products
        self.price = price
        self.state = state
        self.delivery_date = delivery_date


# Esquema para la  visualizacion de productos en un pedido

class ProductoSchema(Schema):
    id = fields.UUID()
    name = fields.Str()
    price = fields.Float()

class ProductosSchema(Schema):
    id = fields.UUID()
class ClientSchema(Schema):
    id = fields.UUID()
    name = fields.Str()

# Esquema para serializar un pedido completo como JSON
class PedidoJsonSchema(Schema):
    id = fields.Str()
    name = fields.Str(required=True)
    ## clientId = fields.Str() # Almacena el ID del cliente
    client = fields.Nested(ClientSchema) # Relación opcional
    products = fields.Nested(ProductoSchema, many=True)
    price = fields.Float(required=True)
    state = fields.Str(required=True)
    deliveryDate = fields.DateTime(required=True, format="iso", validate=validate_delivery_date)
    createdAt = fields.DateTime(dump_only=True)  # Solo se devuelve al serializar


# Esquema para la creación de un nuevo pedido (sin ID y fechas generadas automáticamente)
class PedidoSchema(Schema):
    name = fields.Str(required=True)
    clientId = fields.Str(required=True)
    products = fields.List(fields.UUID(), required=True)
    state = fields.Str(missing="Pendiente")
    price = fields.Float(required=True)
    deliveryDate = fields.DateTime(required=True, format="iso", validate=validate_delivery_date)

