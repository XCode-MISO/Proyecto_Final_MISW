## src\commands\create_pedido.py
from .base_command import BaseCommannd
from ..models.pedido import Pedido, PedidoSchema, PedidoJsonSchema
from ..models.pedido_producto import PedidoProducto
from marshmallow import ValidationError
from src.database import db
from src.infraestructure.pub_sub import publish_pedido_creado, publish_pedido_creado_inventario

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
                    productId=prod_data["id"],
                    amount=prod_data["amount"]
                )
                pedido_productos.append(pedido_producto)

        except Exception as err:
            return {"error crear pedido": str(err)}, 500

        # Crear el pedido
        nuevo_pedido = Pedido(
            name=validated_data["name"],
            clientId=validated_data["clientId"],
            clientName=validated_data["clientName"],
            vendedorId=validated_data["vendedorId"],
            vendedorName=validated_data["vendedorName"],
            price=validated_data["price"],
            state=validated_data.get("state", "Pendiente"),
            deliveryDate=validated_data["deliveryDate"]
        ) # relación intermedia

        # Guardar en la base de datos
        session = db.session()
        session.add(nuevo_pedido)
        session.commit()
        
        for prod_data in productos_data:
            pedido_producto = PedidoProducto(
                pedidoId=nuevo_pedido.id,  # Asegura la relación
                productId=prod_data["id"],
                amount=prod_data["amount"]
            )
            session.add(pedido_producto)

        session.commit()
        session.refresh(nuevo_pedido)

        # Serializar y devolver
        pedido_json = PedidoJsonSchema().dump(nuevo_pedido)

        
        # Crear el formato deseado para client y vendedor
        if 'clientId' in pedido_json:
            pedido_json['client'] = {
                "id": pedido_json.pop("clientId"),
                "name": pedido_json.pop("clientName")
            }
        
        if 'vendedorId' in pedido_json:
            pedido_json['vendedor'] = {
                "id": pedido_json.pop("vendedorId"),
                "name": pedido_json.pop("vendedorName")
            }

        print("DEBUG: Pedido_Json",pedido_json)

        # Publicar el evento de pedido creado
        publish_pedido_creado(pedido_json)
        # Publicar el evento de inventario
        pedido_inventario_json = {
            "items": pedido_json.get("products", [])
        }

        print("DEBUG: Pedido_Inventario_Json",pedido_inventario_json)
        publish_pedido_creado_inventario(pedido_inventario_json)

        session.close()

        return pedido_json
