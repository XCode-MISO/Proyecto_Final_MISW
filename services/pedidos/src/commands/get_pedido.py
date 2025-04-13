from .base_command import BaseCommannd
from ..models.pedido import Pedido, PedidoJsonSchema
from src.database import db

class GetPedidos(BaseCommannd):
    def __init__(self):
        super().__init__()
        self.id = id

    def execute(self, id):
        print("DEBUG: Entrando en GetPedidos.execute()")

        session = db.session()
        try:
            pedido = session.query(Pedido).filter(Pedido.id == self.id).one()
            print(f"DEBUG: Se encontraron {len(pedido)} pedidos")

            # Serializar los pedidos incluyendo los productos
            pedido_json = PedidoJsonSchema().dump(pedido)
        except Exception as e:
            print(f"ERROR: {str(e)}")
            return {"error": "Error al obtener los pedidos"}, 500
        finally:
            session.close()

        return pedido_json
