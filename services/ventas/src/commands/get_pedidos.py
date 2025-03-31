from .base_command import BaseCommannd
from ..models.pedido import Pedido, PedidoJsonSchema
from src.database import db

class GetPedidos(BaseCommannd):
    def __init__(self, pedido_id=None):
        self.pedido_id = pedido_id

    def execute(self):
        print("DEBUG: Entrando en execute() de GetPedidos")
        session = db.session()
        
        if self.pedido_id:
            print(f"DEBUG: Buscando pedido con ID {self.pedido_id}")
            pedido = session.query(Pedido).filter_by(id=self.pedido_id).first()
            if not pedido:
                print("DEBUG: Pedido no encontrado")
                return {"error": "Pedido no encontrado"}, 404
            pedido_json = PedidoJsonSchema().dump(pedido)
            session.close()
            return pedido_json
        
        print("DEBUG: Obteniendo todos los pedidos")
        pedidos = session.query(Pedido).all()
        pedidos_json = PedidoJsonSchema(many=True).dump(pedidos)
        session.close()
        return pedidos_json
