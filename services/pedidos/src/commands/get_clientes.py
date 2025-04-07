from .base_command import BaseCommannd
from ..models.cliente import Cliente, ClienteJsonSchema
from src.database import db

class GetClientes(BaseCommannd):
    def execute(self):
        print("DEBUG: Entrando en GetClientes.execute()")

        session = db.session()
        try:
            clientes = session.query(Cliente).all()
            print(f"DEBUG: Se encontraron {len(clientes)} clientes")

            # Serializar los clientes
            clientes_json = ClienteJsonSchema(many=True).dump(clientes)
        except Exception as e:
            print(f"ERROR: {str(e)}")
            return {"error": "Error al obtener los clientes"}, 500
        finally:
            session.close()

        return clientes_json