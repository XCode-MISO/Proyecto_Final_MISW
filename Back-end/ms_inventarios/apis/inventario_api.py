from flask import Blueprint, jsonify
from models.producto_inventario import ProductoInventario

inventario_bp = Blueprint('inventario_bp', __name__)

@inventario_bp.route('/ping', methods=['GET'])
def ping():
    return jsonify({"msg": "ms_inventarios alive"}), 200

@inventario_bp.route('/productos', methods=['GET'])
def listar_productos_inventario():
    """
    Endpoint para listar todos los registros de la tabla productos_inventario.
    """
    productos = ProductoInventario.query.all()
    result = []
    for prod in productos:
        result.append({
            "id": prod.id,
            "producto_id": prod.producto_id,
            "stock": prod.stock
        })
    return jsonify(result), 200