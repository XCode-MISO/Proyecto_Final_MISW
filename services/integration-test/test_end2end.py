import pytest
import requests
import time

MS_COMPRAS = "http://localhost:5001/api/productos/upload"
MS_PEDIDOS = "http://localhost:5002/api/pedidos"
MS_INVENTARIOS = "http://localhost:5003/api/inventarios"

def wait_for_product(product_id, timeout=10):
    """Espera hasta que el producto aparezca en inventarios"""
    start = time.time()
    while time.time() - start < timeout:
        resp = requests.get(f"{MS_INVENTARIOS}/{product_id}")
        if resp.status_code == 200:
            return resp.json()
        time.sleep(1)
    return None

def test_flujo_creacion_y_pedido():
    # 1. Cargar un producto al micro compras
    files = {
        'file': ('productos.csv', 
            b"nombre,fabricante_id,cantidad,precio,moneda,bodega,estante,pasillo\n"
            b"Producto Test,1,10,100,COP,B1,E1,P1", 
            'text/csv')
    }
    resp = requests.post(MS_COMPRAS, files=files)
    assert resp.status_code in (200, 201), f"Error en carga masiva: {resp.text}"

    # 2. Esperamos que llegue a inventarios (consistencia eventual)
    producto = wait_for_product(1)
    assert producto is not None, "Producto no encontrado en inventarios"
    assert producto['stock'] == 10, f"Stock incorrecto inicialmente: {producto['stock']}"

    # 3. Crear un pedido en pedidos
    pedido_payload = {
        "pedido_id": 1,
        "productos": [
            {"producto_id": 1, "cantidad": 2}
        ]
    }
    resp = requests.post(MS_PEDIDOS, json=pedido_payload)
    assert resp.status_code in (200, 201), f"Error en crear pedido: {resp.text}"

    # 4. Esperamos un pequeño tiempo a que stock se actualice
    time.sleep(3)

    # 5. Verificar que stock se descontó en inventarios
    producto_actualizado = wait_for_product(1)
    assert producto_actualizado is not None, "Producto desapareció después de pedido"
    assert producto_actualizado['stock'] == 8, f"Stock no descontado correctamente: {producto_actualizado['stock']}"