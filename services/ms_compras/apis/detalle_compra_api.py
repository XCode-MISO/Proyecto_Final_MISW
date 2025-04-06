from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from apis.schemas.detalle_compra_schema import DetalleCompraSchema
from services.detalle_compra_service import DetalleCompraService

detalle_compra_bp = Blueprint('detalle_compra_bp', __name__)
schema = DetalleCompraSchema()
service = DetalleCompraService()

@detalle_compra_bp.route('', methods=['POST'])
def registrar_detalle_compra():
    """
    Endpoint: POST /api/compras/detalle
    Payload:
    {
      "nombre": "Producto Compra Ejemplo",
      "fabricanteId": 1,
      "cantidad": 10,
      "precio": 29.99
    }
    Se crea una nueva compra y se registra el detalle correspondiente.
    """
    data = request.get_json() or {}
    try:
        valid_data = schema.load(data)
    except ValidationError as err:
        return jsonify({"error": "Validación fallida", "details": err.messages}), 400
    try:
        compra, producto, detalle = service.registrar_detalle_compra_individual(
            nombre=valid_data["nombre"],
            fabricante_id=valid_data["fabricanteId"],
            cantidad=valid_data["cantidad"],
            precio=valid_data["precio"]
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error al registrar el detalle de compra", "details": str(e)}), 500

    return jsonify({
        "message": "Detalle de compra registrado exitosamente",
        "detalleCompra": {
            "compraId": compra.id,
            "productoId": producto.id,
            "fabricanteId": producto.fabricante_id,
            "cantidad": detalle.cantidad,
            "precio": float(producto.precio_compra)
        }
    }), 201