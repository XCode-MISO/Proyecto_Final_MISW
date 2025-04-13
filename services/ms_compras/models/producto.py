from .db import db

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    precio = db.Column(db.Float)
    moneda = db.Column(db.String(10))
    fabricante_id = db.Column(db.Integer, nullable=False)