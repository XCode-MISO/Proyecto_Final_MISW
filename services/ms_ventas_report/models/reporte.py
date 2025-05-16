from .db import db
from datetime import datetime
class ReporteVentas(db.Model):
    __tablename__ = 'reporte_ventas'
    id = db.Column(db.Integer, primary_key=True)
    prducto = db.Column(db.String(150), nullable=False)
    cantidad = db.Column(db.Integer, default=0)
    fecha = db.Column(db.Date, nullable=False, default= datetime.utcnow())