from marshmallow import Schema, fields, validate

class ProductoSchema(Schema):
    nombre = fields.Str(required=True, validate=validate.Length(min=1, max=150))
    fabricanteId = fields.Int(required=True)
    cantidad = fields.Int(required=True, validate=validate.Range(min=1, error="La cantidad debe ser un entero positivo."))
    precio = fields.Float(required=True, validate=validate.Range(min=0.01, error="El precio debe ser un decimal positivo."))
    moneda = fields.String(required=True, validate=validate.Length(max=10))
    bodega = fields.String(required=True, validate=validate.Length(max=100))
    estante = fields.String(required=True, validate=validate.Length(max=100))
    pasillo = fields.String(required=True, validate=validate.Length(max=100))