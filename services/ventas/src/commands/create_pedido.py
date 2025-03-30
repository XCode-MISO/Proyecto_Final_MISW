from .base_command import BaseCommannd
from ..models.pedido import Pedido, PedidoSchema, PedidoJsonSchema
from marshmallow import ValidationError
from src.models.producto import Producto
from src.database import db

class CreatePedido(BaseCommannd):
    def __init__(self, data):
        self.data = data

    def execute(self):
        print("DEBUG: Entrando en execute()",self.data)
        # Validar los datos del pedido con el esquema
        try:
            productos_objetos = db.session.query(Producto).filter(Producto.id.in_(self.data["products"])).all()
            print("DEBUG: productos_objetos =", productos_objetos)
        except ValidationError as err:
                    return {"error": err.messages}, 400 
        schema = PedidoSchema()
        try:
            validated_data = schema.load(self.data)
        except ValidationError as err:
            return {"error": err.messages}, 400 
        
        # Crear instancia del pedido
        nuevo_pedido = Pedido(
            name=validated_data["name"],
            client_id=validated_data["clientId"], 
            products=productos_objetos, 
            price=validated_data["price"],
            delivery_date=validated_data["deliveryDate"]  
        )
        print("DEBUG: nuevo_pedido =", nuevo_pedido)

        # Guardar en la base de datos
        session = db.session()
        session.add(nuevo_pedido)
        session.commit()
        session.refresh(nuevo_pedido)  # Importante para actualizar los valores generados

        # Serializar y devolver el pedido creado
        pedido_json = PedidoJsonSchema().dump(nuevo_pedido)
        session.close()
        return pedido_json
