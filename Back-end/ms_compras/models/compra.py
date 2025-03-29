from .db import db
from datetime import datetime

class Compra(db.Model):
    __tablename__ = 'compras'

    id           = db.Column(db.Integer, primary_key=True)
    fecha_compra = db.Column(db.DateTime, default=datetime.utcnow)
    estado       = db.Column(db.String(20), default='CREADA')

    detalles = db.relationship('CompraDetalle', backref='compra', lazy=True)