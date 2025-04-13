from .db import db

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)  # Clave interna
    producto_id = db.Column(db.Integer, unique=True, nullable=False)  # ID del producto proveniente de ms_compras
    nombre = db.Column(db.String(150), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    moneda = db.Column(db.String(10))