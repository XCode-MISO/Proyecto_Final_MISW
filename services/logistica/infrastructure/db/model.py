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
    Column("pedido_id", ForeignKey("pedido.pedido_id"), primary_key=True),)

class Pedido(db.Model):
    __tablename__ = 'pedido'
    pedido_id = db.Column(String, primary_key=True)
    direccion = db.Column(String)
    
class Route(db.Model):
    __tablename__ = 'route'
    route_id = db.Column(String, primary_key=True)
    nombreRuta = db.Column(String)
    distancia = db.Column(Float)
    tiempoEstimado = db.Column(Integer)
    pedidos: Mapped[List[Pedido]] = relationship(secondary=association_table)
    mapsResponse = db.Column(String)