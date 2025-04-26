from .base_command import BaseCommannd
from ..models.pedido import Pedido, PedidoJsonSchema
from src.database import db

class GetPedidos(BaseCommannd):
    def execute(self):
        print("DEBUG: Entrando en GetPedidos.execute()")

        session = db.session()
        try:
            
            query = session.query(Pedido)
            
            if self.client_id:
                query = query.filter(Pedido.clientId == self.client_id)  # <-- filtramos por clientId si viene

            pedidos = query.all()
            
            print(f"DEBUG: Se encontraron {len(pedidos)} pedidos")

            # Serializar los pedidos incluyendo los productos
            pedidos_json = PedidoJsonSchema(many=True).dump(pedidos)
            for pedido in pedidos_json:
                if 'clientId' in pedido:
                    pedido['client'] = {
                        "id": pedido.pop("clientId"),
                        "name": pedido.pop("clientName")
                    }
                if 'vendedorId' in pedido:
                    pedido['vendedor'] = {
                        "id": pedido.pop("vendedorId"),
                        "name": pedido.pop("vendedorName")
                    }
        except Exception as e:
            print(f"ERROR: {str(e)}")
            return {"error": "Error al obtener los pedidos"}, 500
        finally:
            session.close()

        return pedidos_json
