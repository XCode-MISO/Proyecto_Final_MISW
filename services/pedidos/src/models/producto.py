import uuid
from sqlalchemy import Column, String, Float, Integer
from sqlalchemy.orm import relationship
from .model import Base,Model
from marshmallow import Schema, fields, ValidationError
from .pedido_producto import PedidoProducto

class Producto(Base,Model):
    __tablename__ = 'productos'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)    
    amount = Column(Integer, nullable=False) # Cantidad del producto

    # Relación con pedidos
    pedido_productos = relationship("PedidoProducto", back_populates="producto")


    def __init__(self, name, price, amount):  ##
        super().__init__() # Llama al constructor de Model
        self.name = name
        self.price = price
        self.amount = amount

class ProductoJsonSchema(Schema):
    id = fields.UUID()
    name = fields.Str()
    price = fields.Float()
    amount = fields.Int()  # Cantidad del producto
