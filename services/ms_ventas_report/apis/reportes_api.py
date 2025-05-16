from flask import Blueprint, jsonify, request, current_app
from services.ms_ventas_report.models.reporte import Producto
from models.producto_inventario import ProductoInventario

inventario_bp = Blueprint('inventario_bp', __name__)

@inventario_bp.route('/ping', methods=['GET'])
def ping():
    return jsonify({"msg": "ms_inventarios alive"}), 200

@inventario_bp.route('/pedidos', methods=['GET'])
def listar_productos_pedido():
    """
    Si se envía el parámetro opcional "nombre", se filtra la búsqueda.
    URL: GET /api/inventarios/pedidos?nombre=<texto>
    """
    nombre_query = request.args.get('nombre')
    if nombre_query:
        productos = Producto.query.filter(Producto.nombre.ilike(f"%{nombre_query}%")).all()
    else:
        productos = Producto.query.all()

    result = []
    for prod in productos:
        inv = ProductoInventario.query.filter_by(producto_id=prod.producto_id).first()
        stock = inv.stock if inv else 0
        result.append({
            "producto_id": prod.producto_id,
            "nombre": prod.nombre,
            "precio": prod.precio,
            "stock": stock
        })
    return jsonify(result), 200

