from .db import db

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.String(300))
    precio_compra = db.Column(db.Float)
    moneda = db.Column(db.String(10))
    fabricante_id = db.Column(db.Integer, db.ForeignKey('fabricantes.id'), nullable=False)