## src\commands\get_pedido.py
from .base_command import BaseCommannd
from ..models.pedido import Pedido, PedidoJsonSchema
from src.database import db

class GetPedido(BaseCommannd):
    def __init__(self, id):
        super().__init__()
        self.id = id

    def execute(self):
        print("DEBUG: Entrando en GetPedidos.execute()")

        session = db.session()
        try:
            pedido = session.query(Pedido).filter(Pedido.id == self.id).one()
            print(f"DEBUG: Se encontro {pedido} pedido")

            # Serializar los pedidos incluyendo los productos
            pedido_json = PedidoJsonSchema().dump(pedido)
            
            
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
                
        except Exception as e:
            print(f"ERROR: {str(e)}")
            return {"error": "Error al obtener el pedido"}, 500
        finally:
            session.close()

        return pedido_json
