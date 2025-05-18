from models.db import db
from models.reporte import ReporteVentas
from datetime import datetime, timedelta
from sqlalchemy import func

class ReporteService:
    @staticmethod
    def get_reportes_por_vendedor(vendedor_id, fecha_inicio=None, fecha_fin=None):
        """
        Obtiene reportes filtrados por vendedor y fechas opcionales
        """
        query = ReporteVentas.query.filter_by(vendedor_id=vendedor_id)
        
        if fecha_inicio:
            query = query.filter(ReporteVentas.fecha >= fecha_inicio)
            
        if fecha_fin:
            query = query.filter(ReporteVentas.fecha <= fecha_fin)
            
        return query.order_by(ReporteVentas.fecha.desc()).all()
    
    @staticmethod
    def get_resumen_por_vendedor(vendedor_id, dias=30):
        """
        Obtiene un resumen de ventas por producto para un vendedor
        en los últimos X días
        """
        fecha_limite = datetime.utcnow().date() - timedelta(days=dias)
        
        result = db.session.query(
            ReporteVentas.producto,
            func.sum(ReporteVentas.cantidad).label('total')
        ).filter(
            ReporteVentas.vendedor_id == vendedor_id,
            ReporteVentas.fecha >= fecha_limite
        ).group_by(
            ReporteVentas.producto
        ).order_by(
            func.sum(ReporteVentas.cantidad).desc()
        ).all()
        
        return [{'producto': prod, 'total': total} for prod, total in result]
        
    @staticmethod
    def iniciar_subscripcion():
        print("Stub: PubSub subscription would start here")
        return True