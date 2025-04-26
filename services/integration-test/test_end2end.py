"""
Escenario E2E:
1) ms_compras publica un producto nuevo con stock 10
2) ms_inventarios lo persiste vía Pub/Sub
3) pedidos descuenta 3 unidades
4) ms_inventarios muestra stock final 7
"""
import io, time, requests

BASE = {
    "compras":     "http://localhost:5001/api",
    "pedidos":     "http://localhost:5003/api",
    "inventarios": "http://localhost:5002/api",
}

def wait_until(predicate, timeout=10, step=0.5):
    end = time.time() + timeout
    while time.time() < end:
        if predicate():
            return True
        time.sleep(step)
    return False

def test_flujo_creacion_y_pedido(create_topics):
    # 1. carga masiva (stock inicial 10)
    csv = ("nombre,fabricante_id,cantidad,precio,moneda,bodega,estante,pasillo\n"
           "Laptop,1,10,1000,USD,B1,E1,P1\n")
    files = {"file": ("prod.csv", io.BytesIO(csv.encode()))}
    r = requests.post(f"{BASE['compras']}/productos/upload", files=files)
    assert r.ok

    # 2. esperar consistencia eventual
    assert wait_until(
        lambda: requests.get(f"{BASE['inventarios']}/inventarios/1").status_code == 200
    ), "El producto no llegó a ms_inventarios"

    # 3. crear pedido que descuenta 3 unidades
    body_pedido = {"productoId": 1, "cantidad": 3}
    r = requests.post(f"{BASE['pedidos']}/pedidos", json=body_pedido)
    assert r.ok

    # 4. stock final = 7
    def stock_es_7():
        det = requests.get(f"{BASE['inventarios']}/inventarios/1")
        return det.ok and det.json().get("stock") == 7

    assert wait_until(stock_es_7), "Stock final distinto de 7"