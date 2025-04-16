# src/models/pedido_producto.py
import uuid
from src.database import db
from sqlalchemy import Column,Float, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .model import Base

class PedidoProducto(Base):
    __tablename__ = 'pedido_producto'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    pedidoId = Column(String(36), ForeignKey('pedidos.id'), nullable=False)
    productId = Column(String(36),  nullable=False)
    amount = Column(Integer, nullable=False)

    pedido = relationship("Pedido", back_populates="products")