from .base_command import BaseCommannd
from src.models.pedido import ClientSchema
from src.database import db

class GetClientes(BaseCommannd):
    def execute(self):
        print("DEBUG: Entrando en GetClientes.execute()")
        try:
            print(f"DEBUG: Se encontraron {len()} clientes")

        except Exception as e:
            print(f"ERROR: {str(e)}")
            return {"error": "Error al obtener los clientes"}, 500
        return {"clientes"}, 200