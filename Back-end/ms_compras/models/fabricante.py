from .db import db

class Fabricante(db.Model):
    __tablename__ = 'fabricantes'

    id       = db.Column(db.Integer, primary_key=True)
    nombre   = db.Column(db.String(150), nullable=False)
    correo   = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(15),  nullable=False)
    empresa  = db.Column(db.String(150), nullable=False)

    productos = db.relationship('Producto', backref='fabricante', lazy=True)