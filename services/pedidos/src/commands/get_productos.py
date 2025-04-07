from .base_command import BaseCommannd
from ..models.producto import Producto, ProductoJsonSchema
from src.database import db

class GetProductos(BaseCommannd):
    def execute(self):
        print("DEBUG: Entrando en GetProductos.execute()")

        session = db.session()
        try:
            productos = session.query(Producto).all()
            print(f"DEBUG: Se encontraron {len(productos)} productos")

            # Serializar los productos
            productos_json = ProductoJsonSchema(many=True).dump(productos)
        except Exception as e:
            print(f"ERROR: {str(e)}")
            return {"error": "Error al obtener los productos"}, 500
        finally:
            session.close()

        return productos_json