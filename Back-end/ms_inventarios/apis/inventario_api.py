from flask import Blueprint, jsonify
from models.producto import Producto

inventario_bp = Blueprint('inventario_bp', __name__)

@inventario_bp.route('/ping', methods=['GET'])
def ping():
    return jsonify({"msg": "ms_inventarios alive"}), 200

@inventario_bp.route('/productos', methods=['GET'])
def listar_productos():
    """
    Lista todos los productos desnormalizados con nombre, precio y stock.
    Se realiza un JOIN entre la tabla productos y productos_inventario.
    """
    from models.producto_inventario import ProductoInventario
    productos = Producto.query.all()
    result = []
    for prod in productos:
        # Consultar el stock en la tabla de inventario
        inv = ProductoInventario.query.filter_by(producto_id=prod.producto_id).first()
        stock = inv.stock if inv else 0
        result.append({
            "producto_id": prod.producto_id,
            "nombre": prod.nombre,
            "precio": prod.precio,
            "fabricanteId": prod.fabricante_id,
            "stock": stock
        })
    return jsonify(result), 200