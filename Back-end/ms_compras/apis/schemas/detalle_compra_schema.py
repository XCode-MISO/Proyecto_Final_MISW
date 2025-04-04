from marshmallow import Schema, fields, validate

class DetalleCompraSchema(Schema):
    nombre = fields.Str(required=True, validate=validate.Length(min=1, max=150))
    fabricanteId = fields.Int(required=True)
    cantidad = fields.Int(required=True, validate=validate.Range(min=1, error="La cantidad debe ser un entero positivo."))
    precio = fields.Float(required=True, validate=validate.Range(min=0.01, error="El precio debe ser un decimal positivo."))