import pytest
from flask import Flask
from services.producto_service import ProductoService
from apis.producto_api import producto_bp

# ------------------------------------------------------------------
# utilidades de prueba
# ------------------------------------------------------------------
class DummyProducto:
    def __init__(self, id_):
        self.id = id_
        self.fabricante_id = 1
        self.precio = 100


def patch_registrar(monkeypatch, *, should_fail=False, exists_ids=(1,)):
    """Mock de ProductoService.registrar_producto_individual."""

    def _mock_assert(fid):
        if fid not in exists_ids:
            raise ValueError(f"Fabricante {fid} no existe")

    monkeypatch.setattr(ProductoService, "_assert_fabricante_exists", staticmethod(_mock_assert))

    def _ok(**kwargs):
        return DummyProducto(42)

    def _fail(**kwargs):
        raise ValueError(f"Fabricante {kwargs['fabricante_id']} no existe")

    monkeypatch.setattr(
        ProductoService,
        "registrar_producto_individual",
        staticmethod(_fail if should_fail else _ok),
    )

# ------------------------------------------------------------------
# fixture cliente Flask
# ------------------------------------------------------------------
@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(producto_bp, url_prefix="/api/productos")
    return app.test_client()

# ------------------------------------------------------------------
# casos
# ------------------------------------------------------------------

def test_registro_ok(monkeypatch, client):
    patch_registrar(monkeypatch, exists_ids=(1,))
    data = {
        "nombre": "Laptop",
        "fabricanteId": 1,
        "cantidad": 3,
        "precio": 1200,
        "moneda": "USD",
        "bodega": "B1",
        "estante": "E1",
        "pasillo": "P1",
    }
    resp = client.post("/api/productos", json=data)
    assert resp.status_code == 201
    body = resp.get_json()
    producto_id = body.get("productoId") or body.get("Compra", {}).get("productoId")
    assert producto_id == 42


def test_registro_validation(monkeypatch, client):
    # Sin precio
    data = {
        "nombre": "Laptop",
        "fabricanteId": 1,
        "cantidad": 3,
        "moneda": "USD",
        "bodega": "B1",
        "estante": "E1",
        "pasillo": "P1",
    }
    resp = client.post("/api/productos", json=data)
    assert resp.status_code == 400


def test_registro_fabricante_inexistente(monkeypatch, client):
    patch_registrar(monkeypatch, should_fail=True, exists_ids=(1,))
    data = {
        "nombre": "Mouse",
        "fabricanteId": 99,
        "cantidad": 2,
        "precio": 20,
        "moneda": "USD",
        "bodega": "B1",
        "estante": "E1",
        "pasillo": "P1",
    }
    resp = client.post("/api/productos", json=data)
    assert resp.status_code == 400
    assert "no existe" in resp.get_json()["error"]

