import json
from typing import List
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Column, Float, ForeignKey, String, Date, Integer, Table
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import relationship

db = SQLAlchemy()

association_table = Table(
        "association_table",
        db.Model.metadata,
        Column("route_id", ForeignKey("route.route_id"), primary_key=True),
        Column("pedido_id", ForeignKey("pedido.pedido_id"), primary_key=True),
    )

cliente_pedido = Table(
        "cliente_pedido",
        db.Model.metadata,
        Column("cliente_id", ForeignKey("cliente.cliente_id"), primary_key=True),
        Column("pedido_id", ForeignKey("pedido.pedido_id"), primary_key=True),
    )

class Cliente(db.Model):
    __tablename__ = 'cliente'
    cliente_id = db.Column(String, primary_key=True)
    direccion = db.Column(String)
    def toJSON(self):
        return {
            "id": self.cliente_id,
            "direccion": self.direccion
        }

class Pedido(db.Model):
    __tablename__ = 'pedido'
    pedido_id = db.Column(String, primary_key=True)
    nombre = db.Column(String)
    fecha = db.Column(Date)
    clientes: Mapped[List[Cliente]] = relationship(secondary=cliente_pedido)
    def toJSON(self):
        return {
            "id": self.pedido_id,
            "nombre": self.nombre,
            "fecha": self.fecha,
            "clientes": list(map(lambda cliente: cliente.toJSON(), self.clientes))
        }
    
class Route(db.Model):
    __tablename__ = 'route'
    route_id = db.Column(String, primary_key=True)
    nombreRuta = db.Column(String)
    distancia = db.Column(Float)
    tiempoEstimado = db.Column(Integer)
    pedidos: Mapped[List[Pedido]] = relationship(secondary=association_table)
    mapsResponse = db.Column(String)
    fecha=db.Column(String)
    
    def toJSON(self):
        return {
            "id": self.route_id,
            "nombreRuta": self.nombreRuta,
            "distancia": self.distancia,
            "tiempoEstimado": self.tiempoEstimado,
            "pedidos": list(map(lambda pedido: pedido.toJSON(), self.pedidos)),
            "mapsResponse": json.loads(self.mapsResponse),
            "fecha": self.fecha
        }