from .base_command import BaseCommannd
from ..models.pedido import Pedido, PedidoSchema, PedidoJsonSchema
from ..models.pedido_producto import PedidoProducto
from marshmallow import ValidationError
from src.models.producto import Producto
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

            productos_ids = [str(prod["id"]) for prod in productos_data]
            productos_objetos = db.session.query(Producto).filter(Producto.id.in_(productos_ids)).all()

            productos_encontrados = {str(p.id) for p in productos_objetos}
            faltantes = set(productos_ids) - productos_encontrados
            if faltantes:
                raise ValueError(f"Los siguientes productos no existen en la base de datos: {faltantes}")

            # Construir lista de relaciones con cantidades
            pedido_productos = []
            for prod_data in productos_data:
                producto = next(p for p in productos_objetos if str(p.id) == str(prod_data["id"]))
                amount = prod_data["amount"]

                pedido_producto = PedidoProducto(
                    producto=producto,
                    amount=amount
                )
                pedido_productos.append(pedido_producto)

        except Exception as err:
            return {"error crear pedido": str(err)}, 500

        # Crear el pedido
        nuevo_pedido = Pedido(
            name=validated_data["name"],
            clientId=validated_data["clientId"],
            products=[pp.producto for pp in pedido_productos],  # relación many-to-many
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
