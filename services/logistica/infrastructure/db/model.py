import json
from typing import List
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Column, Float, ForeignKey, String, Date, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Vendedor(db.Model):
    __tablename__ = 'vendedor'
    vendedor_id = db.Column(String, primary_key=True)
    nombre= db.Column(String)
    direccion = db.Column(String)
    parada_id: Mapped[str] = mapped_column(ForeignKey("parada.parada_id"))
    def toJSON(self):
        return {
            "id": self.vendedor_id,
            "direccion": self.direccion,
            "nombre": self.nombre
        }

class Cliente(db.Model):
    __tablename__ = 'cliente'
    cliente_id = db.Column(String, primary_key=True)
    nombre= db.Column(String)
    direccion = db.Column(String)
    parada_id: Mapped[str] = mapped_column(ForeignKey("parada.parada_id"))
    def toJSON(self):
        return {
            "id": self.cliente_id,
            "direccion": self.direccion,
            "nombre": self.nombre
        }
    

class Route(db.Model):
    __tablename__ = 'route'
    route_id = db.Column(String, primary_key=True)
    paradas = relationship("Parada")

    inicio = db.Column(String)
    fin = db.Column(String)

    nombreRuta = db.Column(String)
    distancia = db.Column(Float)
    tiempoEstimado = db.Column(Integer)
    mapsResponse = db.Column(String)
    fecha=db.Column(String)
    
    def toJSON(self):
        return {
            "id": self.route_id,
            "nombreRuta": self.nombreRuta,
            "distancia": self.distancia,
            "inicio": self.inicio,
            "fin": self.fin,
            "tiempoEstimado": self.tiempoEstimado,
            "paradas": list(map(lambda parada: parada.toJSON(), self.paradas)),
            "mapsResponse": json.loads(self.mapsResponse),
            "fecha": self.fecha
        }

class Parada(db.Model):
    __tablename__ = 'parada'
    parada_id = db.Column(String, primary_key=True)
    route_id = Column(String, ForeignKey("route.route_id"))

    nombre = db.Column(String)
    fecha = db.Column(Date)

    cliente: Mapped[Cliente] = relationship(Cliente)
    vendedor: Mapped[Vendedor] = relationship(Vendedor)

    def toJSON(self):
        return {
            "id": self.parada_id,
            "nombre": self.nombre,
            "fecha": self.fecha,
            "cliente": self.cliente.toJSON(),
            "vendedor": self.vendedor.toJSON(),
        }
    
