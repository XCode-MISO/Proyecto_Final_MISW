from .db import db
from datetime import datetime

class ReporteVentas(db.Model):
    __tablename__ = 'reporte_ventas'
    id = db.Column(db.Integer, primary_key=True)
    producto = db.Column(db.String(150), nullable=False)
    cantidad = db.Column(db.Integer, default=0)
    fecha = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    vendedor_id = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f'<ReporteVentas {self.producto} - {self.cantidad}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'producto': self.producto,
            'cantidad': self.cantidad,
            'fecha': self.fecha.isoformat() if self.fecha else None,
            'vendedor_id': self.vendedor_id
        }