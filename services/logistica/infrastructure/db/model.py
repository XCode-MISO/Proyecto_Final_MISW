from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import Float, String, Date, Integer

db = SQLAlchemy()

class Route(db.Model):
    __tablename__ = 'route'
    route_id = db.Column(String, primary_key=True)
    nombreRuta = db.Column(String)
    distancia = db.Column(Float)
    tiempoEstimado = db.Column(Integer)

def MapsToRoute(mapsRoute):
    return Route()

class Visit(db.Model):
    __tablename__ = 'visit'
    visit_id = db.Column(String, primary_key=True)
    datosPantalla = db.Column(String)
    fechaVisita = db.Column(Date)
