from .db import db

class ReporteVentas(db.Model):
    __tablename__ = 'reporte_ventas'
    id = db.Column(db.Integer, primary_key=True) 
    producto_id = db.Column(db.Integer, unique=True, nullable=False)
    nombre = db.Column(db.String(150), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    moneda = db.Column(db.String(10))