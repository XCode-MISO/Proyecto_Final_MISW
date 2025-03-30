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