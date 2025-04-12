from flask import Blueprint, request, jsonify
from marshmallow import Schema, fields, validate, ValidationError
from services.fabricante_service import FabricanteService
from models.fabricante import Fabricante

fabricante_bp = Blueprint('fabricante_bp', __name__)
fabricante_service = FabricanteService()

class FabricanteSchema(Schema):
    nombre = fields.Str(required=True, validate=validate.Length(max=150))
    correo = fields.Email(required=True)
    telefono = fields.Str(required=True, validate=[
        validate.Regexp(r'^\d+$', error="El teléfono debe contener solo dígitos."),
        validate.Length(min=7, max=15, error="El teléfono debe tener entre 7 y 15 dígitos.")
    ])
    empresa = fields.Str(required=True, validate=validate.Length(max=150))

@fabricante_bp.route('', methods=['POST'])
def crear_fabricante():
    data = request.get_json()
    schema = FabricanteSchema()
    try:
        validated = schema.load(data)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    nuevo = fabricante_service.crear_fabricante(
        nombre=validated['nombre'],
        correo=validated['correo'],
        telefono=validated['telefono'],
        empresa=validated['empresa']
    )
    return jsonify({
        "id": nuevo.id,
        "nombre": nuevo.nombre,
        "correo": nuevo.correo,
        "telefono": nuevo.telefono,
        "empresa": nuevo.empresa
    }), 201

@fabricante_bp.route('', methods=['GET'])
def listar_fabricantes():
    from models.fabricante import Fabricante
    fabricantes = Fabricante.query.all()
    result = []
    for fab in fabricantes:
        result.append({
            "id": fab.id,
            "nombre": fab.nombre,
            "correo": fab.correo,
            "telefono": fab.telefono,
            "empresa": fab.empresa
        })
    return jsonify(result), 200

@fabricante_bp.route('/upload', methods=['POST'])
def upload_fabricantes():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No se proporcionó ningún archivo"}), 400

    # Validar la extensión del archivo (debe ser CSV)
    if not file.filename.lower().endswith('.csv'):
        return jsonify({"error": "El archivo debe ser un CSV"}), 400

    try:
        # Leemos el contenido del archivo y lo decodificamos a UTF-8
        file_content = file.read().decode("utf-8")
    except Exception as e:
        return jsonify({"error": f"Error al leer el archivo: {str(e)}"}), 400

    # Llamamos al método de carga masiva (estático) y obtenemos el resultado
    result = FabricanteService.upload_fabricantes_from_file(file_content)
    # Si se insertó al menos un registro, retornamos 201; de lo contrario 200
    status_code = 201 if result.get("inserted", 0) > 0 else 200
    return jsonify(result), status_code
