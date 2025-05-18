from flask import Blueprint, jsonify, request
from datetime import datetime
from service.reporte_service import ReporteService

reporte_bp = Blueprint('reportes', __name__, url_prefix='/api/reportes')

@reporte_bp.route('/vendedor/<string:vendedor_id>', methods=['GET'])
def get_reportes_por_vendedor(vendedor_id):
    """
    Obtener reportes de ventas filtrados por vendedor con opción de filtro por fechas
    """
    try:
        fecha_inicio_str = request.args.get('fecha_inicio')
        fecha_fin_str = request.args.get('fecha_fin')
        
        fecha_inicio = None
        fecha_fin = None
        
        if fecha_inicio_str:
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
        
        if fecha_fin_str:
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
            
        reportes = ReporteService.get_reportes_por_vendedor(vendedor_id, fecha_inicio, fecha_fin)
        
        resultado = []
        for r in reportes:
            resultado.append({
                'id': r.id,
                'producto': r.producto,
                'cantidad': r.cantidad,
                'fecha': r.fecha.isoformat() if r.fecha else None
            })
            
        return jsonify({
            'vendedor_id': vendedor_id,
            'reportes': resultado
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reporte_bp.route('/vendedor/<string:vendedor_id>/resumen', methods=['GET'])
def get_resumen_vendedor(vendedor_id):
    """
    Obtener un resumen de las ventas por producto para un vendedor
    """
    try:
        dias = request.args.get('dias', default=30, type=int)
        
        resumen = ReporteService.get_resumen_por_vendedor(vendedor_id, dias)
            
        return jsonify({
            'vendedor_id': vendedor_id,
            'periodo_dias': dias,
            'productos': resumen
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500