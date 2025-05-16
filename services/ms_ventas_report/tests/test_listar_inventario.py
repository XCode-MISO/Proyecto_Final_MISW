import pytest
from flask import Flask, jsonify
from services.ms_ventas_report.apis.reportes_api import inventario_bp  

# ------------------------------------------------------------------
# datos dummy
# ------------------------------------------------------------------
PEDIDOS_DUMMY = [
    {"producto_id": 1, "nombre": "Prod 1", "precio": 100, "stock": 10},
    {"producto_id": 2, "nombre": "Prod 2", "precio": 200, "stock": 20},
]

UBICACION_DUMMY = [
    {"producto_id": 1, "nombre": "Prod 1", "bodega": "B1", "cantidad": 10},
    {"producto_id": 2, "nombre": "Prod 2", "bodega": "B2", "cantidad": 20},
]

DETALLE_OK = {
    "producto_id": 1,
    "nombre": "Prod 1",
    "precio": 100,
    "stock": 10,
    "bodega": "B1",
    "estante": "E1",
    "pasillo": "P1",
}

# ------------------------------------------------------------------
# patch helpers
# ------------------------------------------------------------------

def patch_view(monkeypatch, client, endpoint, result, status=200):
    def _stub(**kwargs):
        return jsonify(result), status

    monkeypatch.setitem(client.application.view_functions, endpoint, _stub)

# ------------------------------------------------------------------
# fixture
# ------------------------------------------------------------------
@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(inventario_bp, url_prefix="/api/inventarios")
    return app.test_client()

# ------------------------------------------------------------------
# casos
# ------------------------------------------------------------------

def test_pedidos_ok(monkeypatch, client):
    patch_view(monkeypatch, client, "inventario_bp.listar_productos_pedido", PEDIDOS_DUMMY)
    resp = client.get("/api/inventarios/pedidos")
    assert resp.status_code == 200
    body = resp.get_json()
    assert body == PEDIDOS_DUMMY


def test_ubicacion_ok(monkeypatch, client):
    patch_view(monkeypatch, client, "inventario_bp.listar_productos_ubicacion", UBICACION_DUMMY)
    resp = client.get("/api/inventarios/ubicacion")
    assert resp.status_code == 200
    assert resp.get_json() == UBICACION_DUMMY


def test_get_existente(monkeypatch, client):
    patch_view(
        monkeypatch,
        client,
        "inventario_bp.get_producto",
        DETALLE_OK,
        status=200,
    )
    resp = client.get("/api/inventarios/1")
    assert resp.status_code == 200
    assert resp.get_json()["producto_id"] == 1


def test_get_no_existente(monkeypatch, client):
    patch_view(
        monkeypatch,
        client,
        "inventario_bp.get_producto",
        {"error": "Producto no encontrado"},
        status=404,
    )
    resp = client.get("/api/inventarios/999")
    assert resp.status_code == 404
    assert "error" in resp.get_json()

