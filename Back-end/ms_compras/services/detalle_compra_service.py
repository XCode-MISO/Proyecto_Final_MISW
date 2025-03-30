from models.db import db
from models.compra import Compra
from models.producto import Producto
from models.detalle_compra import DetalleCompra

class DetalleCompraService:
    def registrar_detalle_compra_individual(self, nombre, fabricante_id, cantidad, precio):
        # 1. Crear una nueva compra
        compra = Compra(estado="CREADA")
        db.session.add(compra)
        db.session.commit()  # Asigna compra.id

        # 2. Buscar si existe un producto con ese nombre y fabricante
        producto = Producto.query.filter_by(nombre=nombre, fabricante_id=fabricante_id).first()
        if producto:
            # Actualizar el precio (opcionalmente se podría comparar)
            producto.precio_compra = precio
            db.session.commit()
        else:
            # Crear el producto
            producto = Producto(
                nombre=nombre,
                fabricante_id=fabricante_id,
                precio_compra=precio,
                moneda="COP"  # Valor fijo o configurable
            )
            db.session.add(producto)
            db.session.commit()

        # 3. Crear el detalle de compra
        detalle = DetalleCompra(
            compra_id=compra.id,
            producto_id=producto.id,
            cantidad=cantidad
        )
        db.session.add(detalle)
        db.session.commit()

        # 4. Publicar evento para ms_inventarios 
        from events.publisher import publish_compra_realizada
        event_data = {
            "eventType": "DetalleCompraCreado",
            "compraId": compra.id,
            "productoId": producto.id,
            "cantidad": cantidad,
            "precio": precio
        }
        publish_compra_realizada(event_data)

        return compra, producto, detalle