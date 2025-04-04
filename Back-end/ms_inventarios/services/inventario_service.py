from models.db import db
from models.producto_inventario import ProductoInventario

class InventarioService:
    def incrementar_stock(self, producto_id, cantidad):
        item = ProductoInventario.query.filter_by(producto_id=producto_id).first()
        if not item:
            item = ProductoInventario(producto_id=producto_id, stock=0)
            db.session.add(item)
        item.stock += cantidad
        db.session.commit()
        print(f"[INVENTARIOS] productoId={producto_id}, +{cantidad}, total={item.stock}")