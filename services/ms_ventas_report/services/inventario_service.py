from models.db import db
from models.producto_inventario import ProductoInventario

class InventarioService:
    def incrementar_stock(self, producto_id, cantidad, bodega=None, estante=None, pasillo=None):
        # Busca el registro de inventario para el producto
        item = ProductoInventario.query.filter_by(producto_id=producto_id).first()
        if not item:
            # Si no existe, lo crea usando la cantidad recibida como stock inicial
            item = ProductoInventario(
                producto_id=producto_id,
                stock=cantidad,
                bodega=bodega,
                estante=estante,
                pasillo=pasillo
            )
            db.session.add(item)
        else:
            # Si ya existe, se incrementa el stock
            item.stock += cantidad
            # Actualiza los datos de ubicación en caso de que se envíen nuevos valores
            if bodega is not None:
                item.bodega = bodega
            if estante is not None:
                item.estante = estante
            if pasillo is not None:
                item.pasillo = pasillo
        db.session.commit()
        print(f"[INVENTARIOS] productoId={producto_id}, +{cantidad}, total={item.stock}")
    
    def decrementar_stock(self, producto_id, cantidad):
        # Busca el registro de inventario para el producto
        item = ProductoInventario.query.filter_by(producto_id=producto_id).first()
        if not item:
            # Se decide qué hacer en caso de no encontrar el registro (por ejemplo, loggear y/o crear uno nuevo)
            raise ValueError(f"No se encontró inventario para el producto_id {producto_id}")
        # Resta la cantidad vendida
        if item.stock < cantidad:
            # Podrías manejar el caso de stock insuficiente, por ejemplo:
            raise ValueError(f"Stock insuficiente para el producto_id {producto_id}")
        item.stock -= cantidad
        db.session.commit()
        print(f"[INVENTARIOS] productoId={producto_id}, -{cantidad}, stock actual={item.stock}")
        return item