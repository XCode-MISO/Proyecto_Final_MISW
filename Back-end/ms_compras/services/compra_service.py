from models.db import db
from models.compra import Compra
from models.compra_detalle import CompraDetalle
from datetime import datetime
from events.publisher import publish_compra_realizada

class CompraService:
    def crear_compra_con_detalles(self, lista_productos):
        nueva_compra = Compra(
            fecha_compra=datetime.now(),
            estado='CREADA'
        )
        db.session.add(nueva_compra)
        db.session.commit()  # para asignar ID

        detalles = []
        for item in lista_productos:
            producto_id = item.get('productoId')
            cantidad = item.get('cantidad', 0)
            det = CompraDetalle(
                compra_id=nueva_compra.id,
                producto_id=producto_id,
                cantidad=cantidad
            )
            db.session.add(det)
            detalles.append({"productoId": producto_id, "cantidad": cantidad})
        db.session.commit()

        event_data = {
            "eventType": "CompraRealizadaEvent",
            "compraId": nueva_compra.id,
            "productos": detalles,
            "fechaCompra": str(nueva_compra.fecha_compra)
        }
        publish_compra_realizada(event_data)
        return nueva_compra