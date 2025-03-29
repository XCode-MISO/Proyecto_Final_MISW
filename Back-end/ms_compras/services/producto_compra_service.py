from models.db import db
from models.producto_compra import ProductoCompra
from models.fabricante import Fabricante

class ProductoCompraService:
    def crear_producto_compra(self, nombre, fabricante_id, cantidad, precio):
        fabricante = Fabricante.query.get(fabricante_id)
        if not fabricante:
            raise ValueError("El fabricante no existe.")
        nuevo = ProductoCompra(
            nombre=nombre,
            fabricante_id=fabricante_id,
            cantidad=cantidad,
            precio=precio
        )
        db.session.add(nuevo)
        db.session.commit()
        return nuevo