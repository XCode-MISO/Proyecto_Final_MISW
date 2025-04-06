from .db import db

class ProductoCompra(db.Model):
    __tablename__ = 'productos_compra'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    fabricante_id = db.Column(db.Integer, nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Numeric(10,2), nullable=False)