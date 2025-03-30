from models.db import db
from models.fabricante import Fabricante
from models.producto import Producto

class ProductoService:
    def crear_producto(self, fabricante_id, nombre, descripcion, precio_compra, moneda):
        fab = Fabricante.query.get(fabricante_id)
        if not fab:
            raise ValueError("Fabricante no encontrado")
        nuevo = Producto(
            nombre=nombre,
            descripcion=descripcion,
            precio_compra=precio_compra or 0.0,
            moneda=moneda or "COP",
            fabricante_id=fabricante_id
        )
        db.session.add(nuevo)
        db.session.commit()
        return nuevo