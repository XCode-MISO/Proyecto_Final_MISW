from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from apis.schemas.producto_schema import ProductoSchema
from services.producto_service import ProductoService

# Primero, se define el Blueprint
producto_bp = Blueprint('producto_bp', __name__)

schema = ProductoSchema()
service = ProductoService()

@producto_bp.route('', methods=['POST'])
def registrar_producto():
    """
    Endpoint: POST /api/productos
    Payload esperado:
    {
      "nombre": "Producto Compra Ejemplo",
      "fabricanteId": 1,
      "cantidad": 10,
      "precio": 29.99,
      "moneda": "USD",
      "bodega": "Bodega 1",
      "estante": "Estante A",
      "pasillo": "Pasillo 3"
    }
    """
    data = request.get_json() or {}
    try:
        valid_data = schema.load(data)
    except ValidationError as err:
        return jsonify({"error": "Validación fallida", "details": err.messages}), 400
    try:
        producto = service.registrar_producto_individual(
            nombre=valid_data["nombre"],
            fabricante_id=valid_data["fabricanteId"],
            cantidad=valid_data["cantidad"],
            precio=valid_data["precio"],
            moneda=valid_data["moneda"],
            bodega=valid_data["bodega"],
            estante=valid_data["estante"],
            pasillo=valid_data["pasillo"]
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error al registrar el detalle de compra", "details": str(e)}), 500

    return jsonify({
        "message": "Producto registrado exitosamente",
        "Compra": {
            "productoId": producto.id,
            "fabricanteId": producto.fabricante_id,
            "precio": float(producto.precio),
            "cantidad": valid_data.get("cantidad"),
            "moneda": valid_data.get("moneda"),
            "bodega": valid_data.get("bodega"),
            "estante": valid_data.get("estante"),
            "pasillo": valid_data.get("pasillo")
        }
    }), 201

@producto_bp.route("/upload", methods=["POST"])
def carga_masiva_productos():
    """Endpoint: POST /api/productos/upload

    Espera *multipart/form-data* con un campo **file** que sea un `.csv`.
    """
    file = request.files.get("file")
    if file is None:
        return jsonify({"error": "Debe enviar un archivo CSV en el campo 'file'"}), 400

    if not file.filename.lower().endswith(".csv"):
        return jsonify({"error": "El archivo debe ser un CSV"}), 400

    try:
        content = file.read().decode("utf-8")
    except Exception as exc:
        return jsonify({"error": f"Error al leer el archivo: {exc}"}), 400

    result = ProductoService.upload_productos_from_file(content)
    status = 201 if result["inserted"] > 0 else 200
    return jsonify(result), status