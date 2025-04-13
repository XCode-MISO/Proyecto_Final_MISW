from .db import db

class ProductoInventario(db.Model):
    __tablename__ = 'productos_inventario'

    id          = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, nullable=False)
    stock       = db.Column(db.Integer, default=0)
    bodega = db.Column(db.String(100), nullable=True)
    estante = db.Column(db.String(100), nullable=True)
    pasillo = db.Column(db.String(100), nullable=True)