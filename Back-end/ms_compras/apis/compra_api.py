from flask import Blueprint, request, jsonify
from services.compra_service import CompraService

compra_bp = Blueprint('compra_bp', __name__)
compra_service = CompraService()

@compra_bp.route('', methods=['POST'])
def crear_compra():
    """
    body JSON: {
      "productos": [
        { "productoId": 1, "cantidad": 10 },
        { "productoId": 2, "cantidad": 5 }
      ]
    }
    """
    data = request.get_json() or {}
    productos = data.get('productos', [])

    nueva_compra = compra_service.crear_compra_con_detalles(productos)

    return jsonify({
        "msg":       "Compra creada y evento publicado",
        "compraId":  nueva_compra.id
    }), 201