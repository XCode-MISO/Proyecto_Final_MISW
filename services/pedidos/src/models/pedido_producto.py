# src/models/pedido_producto.py
import uuid
from sqlalchemy import Column,Float, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .model import Base

class PedidoProducto(Base):
    __tablename__ = 'pedido_producto'

    pedido_id = Column(String(36), ForeignKey('pedidos.id'), primary_key=True)
    producto_id = Column(String(36), ForeignKey('productos.id'), primary_key=True)
    productoName = Column(String, nullable=False)
    productoPrice = Column(Float, nullable=False)
    amount = Column(Integer, nullable=False)

    pedido = relationship("Pedido", back_populates="pedido_productos")
