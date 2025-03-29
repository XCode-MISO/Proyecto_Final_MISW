from .db import db

class CompraDetalle(db.Model):
    __tablename__ = 'compras_detalle'

    id = db.Column(db.Integer, primary_key=True)

    compra_id   = db.Column(db.Integer, db.ForeignKey('compras.id'),    nullable=False)
    producto_id = db.Column(db.Integer, nullable=False)
    cantidad    = db.Column(db.Integer, default=0)