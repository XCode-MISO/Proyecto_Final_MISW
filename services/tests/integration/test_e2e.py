import pytest
import requests
import random
import string
import time
from datetime import date, timedelta


COMPRAS_BASE    = "http://kubernetes-gateway.cppxcode.shop/compras"
INVENTARIO_BASE = "http://kubernetes-gateway.cppxcode.shop/inventario"
PEDIDOS_BASE    = "http://kubernetes-gateway.cppxcode.shop/pedidos"

POLL_INTERVAL   = 1      
POLL_TIMEOUT    = 15     


def random_name(prefix="Producto"):
    suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return f"{prefix}-{suffix}"

def create_product(nombre: str, fabricante_id: int, cantidad: int, precio: float):
    payload = {
        "nombre":       nombre,
        "fabricanteId": fabricante_id,
        "cantidad":     cantidad,
        "precio":       precio,
        "moneda":       "COP",
        "bodega":       "B1",
        "estante":      "E1",
        "pasillo":      "P1",
    }
    resp = requests.post(f"{COMPRAS_BASE}/api/productos", json=payload)
    resp.raise_for_status()
    data = resp.json()["Compra"]
    return int(data["productoId"]), int(data["cantidad"]), float(data["precio"])

def get_stock(producto_id: int) -> int:
    resp = requests.get(f"{INVENTARIO_BASE}/api/inventarios/{producto_id}")
    resp.raise_for_status()
    return int(resp.json().get("stock", 0))

def wait_for_stock(producto_id: int, expected: int, timeout=POLL_TIMEOUT):
    time.sleep(POLL_INTERVAL)
    start = time.time()
    while True:
        stock = get_stock(producto_id)
        if stock == expected:
            return stock
        if time.time() - start > timeout:
            pytest.fail(
                f"Timeout {timeout}s: stock para producto {producto_id} = {stock}, "
                f"pero esperaba {expected}"
            )
        time.sleep(POLL_INTERVAL)

def create_order(producto_id: int, amount: int, unit_price: float):
    delivery_date = (date.today() + timedelta(days=random.choice((1, 2)))).isoformat()
    total_price   = round(unit_price * amount, 2)
    payload = {
        "name":          "Pedido E2E",
        "clientId":      "696ea246-c7d8-472b-9088-4b595fbc3a4e",
        "clientName":    "Armando Casas",
        "vendedorId":    "696ea246-c7d8-472b-9088-4b595fbc3a4e",
        "vendedorName":  "Armando Casas",
        "products":      [{"id": str(producto_id), "amount": amount}],
        "price":         total_price,
        "state":         "Pendiente",
        "deliveryDate":  delivery_date
    }
    resp = requests.post(f"{PEDIDOS_BASE}/create_pedido", json=payload)
    resp.raise_for_status()
    return resp.json()


# ── TEST ────────────────────────────────────────────────────────────────────────

@pytest.mark.integration
def test_e2e_stock_consistency():
    INITIAL_STOCK = 100
    ORDER_AMOUNT  = 10

    # 1) Crear producto
    nombre = random_name()
    prod_id, stock_before, unit_price = create_product(
        nombre=nombre,
        fabricante_id=1,
        cantidad=INITIAL_STOCK,
        precio=120.00
    )
    assert stock_before == INITIAL_STOCK

    # 2) Verificar stock inicial en micro ms_inventarios
    assert wait_for_stock(prod_id, INITIAL_STOCK) == INITIAL_STOCK

    # 3) Crear pedido
    pedido = create_order(prod_id, ORDER_AMOUNT, unit_price)
    assert pedido.get("id") is not None 

    # 4) Verificar stock luego del pedido
    expected = INITIAL_STOCK - ORDER_AMOUNT
    assert wait_for_stock(prod_id, expected) == expected