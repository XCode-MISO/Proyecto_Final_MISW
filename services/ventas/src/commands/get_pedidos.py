from .base_command import BaseCommannd
from ..models.pedido import Pedido, PedidoJsonSchema
from src.database import db

class GetPedidos(BaseCommannd):
    def execute(self):
        print("DEBUG: Entrando en GetPedidos.execute()")

        session = db.session()
        try:
            pedidos = session.query(Pedido).all()
            print(f"DEBUG: Se encontraron {len(pedidos)} pedidos")

            # Serializar los pedidos encontrados
            pedidos_json = PedidoJsonSchema(many=True).dump(pedidos)
        except Exception as e:
            print(f"ERROR: {str(e)}")
            return {"error": "Error al obtener los pedidos"}, 500
        finally:
            session.close()

        return pedidos_json
