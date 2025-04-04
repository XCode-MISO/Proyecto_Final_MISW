import uuid
from sqlalchemy import Column, String, Float
from sqlalchemy.orm import relationship
from .model import Base,Model
from .pedido import pedido_producto  # Importamos la tabla intermedia

class Producto(Base,Model):
    __tablename__ = 'productos'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)

    # Relación con pedidos
    pedidos = relationship("Pedido", secondary=pedido_producto, back_populates="products")

    def __init__(self, name, price):  ##
        super().__init__() # Llama al constructor de Model
        self.name = name
        self.price = price
