import uuid
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from .model import Base,Model

class Cliente(Base,Model):
    __tablename__ = 'clientes'

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False)

    # Relación con pedidos
    pedidos = relationship("Pedido", back_populates="client")

    def __init__(self, name):
        super().__init__() # Llama al constructor de Model
        self.name = name
