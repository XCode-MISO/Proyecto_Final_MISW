from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from apis.schemas.producto_compra_schema import ProductoCompraSchema
from services.producto_compra_service import ProductoCompraService

producto_compra_bp = Blueprint('producto_compra_bp', __name__)
schema = ProductoCompraSchema()
service = ProductoCompraService()

@producto_compra_bp.route('', methods=['POST'])
def registrar_producto_compra():
    data = request.get_json() or {}
    try:
        valid_data = schema.load(data)
    except ValidationError as err:
        return jsonify({"error": "Validación fallida", "details": err.messages}), 400

    try:
        nuevo = service.crear_producto_compra(
            nombre=valid_data['nombre'],
            fabricante_id=valid_data['fabricanteId'],
            cantidad=valid_data['cantidad'],
            precio=valid_data['precio']
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error al registrar producto", "details": str(e)}), 500

    return jsonify({
        "message": "Producto de compra registrado exitosamente",
        "producto": {
            "id": nuevo.id,
            "nombre": nuevo.nombre,
            "fabricanteId": nuevo.fabricante_id,
            "cantidad": nuevo.cantidad,
            "precio": float(nuevo.precio)
        }
    }), 201