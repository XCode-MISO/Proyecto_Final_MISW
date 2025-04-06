from .db import db

class ProductoInventario(db.Model):
    __tablename__ = 'productos_inventario'

    id          = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, nullable=False)
    stock       = db.Column(db.Integer, default=0)