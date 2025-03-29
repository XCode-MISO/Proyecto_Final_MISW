from flask import Blueprint, request, jsonify
from marshmallow import Schema, fields, validate, ValidationError
from services.fabricante_service import FabricanteService

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

    nuevo_fab = fabricante_service.crear_fabricante(
        nombre   = validated['nombre'],
        correo   = validated['correo'],
        telefono = validated['telefono'],
        empresa  = validated['empresa']
    )

    return jsonify({
        "id":       nuevo_fab.id,
        "nombre":   nuevo_fab.nombre,
        "correo":   nuevo_fab.correo,
        "telefono": nuevo_fab.telefono,
        "empresa":  nuevo_fab.empresa
    }), 201