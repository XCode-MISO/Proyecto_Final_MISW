import random
from datetime import date, timedelta
import time
import requests
import pytest
MS_COMPRAS     = "http://localhost:5001/api/productos/upload"
MS_PEDIDOS     = "http://localhost:5002/create_pedido"
MS_INVENTARIOS = "http://localhost:5003/api/inventarios"

CSV_CONTENT = (
    b"nombre,fabricante_id,cantidad,precio,moneda,bodega,estante,pasillo\n"
    b"Producto Test,1,10,100,COP,B1,E1,P1"
)

def wait_for_product(product_id: int, timeout: int = 10):
    """Espera hasta que el producto aparezca (consistencia eventual)."""
    t0 = time.time()
    while time.time() - t0 < timeout:
        r = requests.get(f"{MS_INVENTARIOS}/{product_id}")
        if r.status_code == 200:
            return r.json()
        time.sleep(1)
    return None


def test_flujo_creacion_y_pedido():

    delivery_date = (date.today() + timedelta(days=random.choice((1, 2)))).isoformat()
    
    pedido_payload = {
        "name":         "Pedido especial",
        "clientId":     "696ea246-c7d8-472b-9088-4b595fbc3a4e",
        "clientName":   "Armando Casas",
        "vendedorId":   "696ea246-c7d8-472b-9088-4b595fbc3a4e",
        "vendedorName": "Armando Casas",
        "products": [
            {"id": "1", "amount": 2}
        ],
        "price":        200.00,
        "state":        "Pendiente",
        "deliveryDate": delivery_date 
    }

    resp = requests.post(MS_PEDIDOS, json=pedido_payload)
    assert resp.status_code in (200, 201), f"Crear pedido falló: {resp.text}"

    time.sleep(3)

    # 5️⃣  Verifica que el stock se descontó
    prod_after = wait_for_product(1)
    assert prod_after, "Producto desapareció después del pedido"
    assert prod_after["stock"] == 8, f"Stock no descontado: {prod_after['stock']}"