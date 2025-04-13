from flask import Blueprint, jsonify, request, current_app
from models.producto import Producto
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

@inventario_bp.route('/ubicacion', methods=['GET'])
def listar_productos_ubicacion():
    """
    URL: GET /api/inventarios/ubicacion?nombre=<texto>
    """
    nombre_query = request.args.get('nombre')
    if nombre_query:
        productos = Producto.query.filter(Producto.nombre.ilike(f"%{nombre_query}%")).all()
    else:
        productos = Producto.query.all()

    result = []
    for prod in productos:
        inv = ProductoInventario.query.filter_by(producto_id=prod.producto_id).first()
        if inv:
            result.append({
                "producto_id": prod.producto_id,
                "nombre": prod.nombre,
                "bodega": inv.bodega,
                "cantidad": inv.stock
            })
    return jsonify(result), 200

@inventario_bp.route('/<int:producto_id>', methods=['GET'])
def get_producto(producto_id):
    """
    Retorna el detalle completo de un producto, incluyendo datos del producto y del inventario (si existe).
    URL: GET /api/inventarios/<producto_id>
    """
    try:
        prod = Producto.query.filter_by(producto_id=producto_id).first()
        if not prod:
            return jsonify({"error": "Producto no encontrado"}), 404

        response = {
            "producto_id": prod.producto_id,
            "nombre": prod.nombre,
            "precio": prod.precio,
            "moneda": prod.moneda,
        }
        inv = ProductoInventario.query.filter_by(producto_id=producto_id).first()
        if inv:
            response.update({
                "stock": inv.stock,
                "bodega": inv.bodega,
                "estante": inv.estante,
                "pasillo": inv.pasillo
            })
        return jsonify(response), 200
    except Exception as e:
        current_app.logger.error(f"Error en get_producto: {e}")
        return jsonify({"error": "Error interno al obtener el producto"}), 500