## src\commands\create_pedido.py
from .base_command import BaseCommannd
from ..models.pedido import Pedido, PedidoSchema, PedidoJsonSchema
from ..models.pedido_producto import PedidoProducto
from marshmallow import ValidationError
from src.database import db

class CreatePedido(BaseCommannd):
    def __init__(self, data):
        self.data = data

    def execute(self):
        print("DEBUG: Entrando en execute()", self.data)

        # Validar los datos con el esquema de entrada
        schema = PedidoSchema()
        try:
            validated_data = schema.load(self.data)
        except ValidationError as err:
            return {"error": err.messages}, 400

        try:
            
            productos_data = validated_data.get("products", [])
            if not productos_data:
                raise ValueError("No se han proporcionado productos con cantidad.")

            pedido_productos = []
            for prod_data in productos_data:
                pedido_producto = PedidoProducto(
                    productoId=prod_data["id"],
                    productoName=prod_data["name"],
                    productoPrice=prod_data["price"],
                    amount=prod_data["amount"]
                )
                pedido_productos.append(pedido_producto)

        except Exception as err:
            return {"error crear pedido": str(err)}, 500

        # Crear el pedido
        nuevo_pedido = Pedido(
            name=validated_data["name"],
            clientId=validated_data["clientId"],
            clientName=validated_data.get("clientName"),
            vendedorId=validated_data.get("vendedorId"),
            vendedorName=validated_data.get("vendedorName"),
            price=validated_data["price"],
            state=validated_data.get("state", "Pendiente"),
            deliveryDate=validated_data["deliveryDate"]
        )
        nuevo_pedido.pedido_productos = pedido_productos  # relación intermedia

        # Guardar en la base de datos
        session = db.session()
        session.add(nuevo_pedido)
        session.commit()
        session.refresh(nuevo_pedido)

        # Serializar y devolver
        pedido_json = PedidoJsonSchema().dump(nuevo_pedido)
        session.close()
        return pedido_json
