import pytest
from flask import Flask
from io import BytesIO

from services.producto_service import ProductoService
from apis.producto_api import producto_bp

# ------------------------------------------------------------------
# utilidades de prueba (mock de existencia de fabricante)
# ------------------------------------------------------------------

def patch_fabricante_exists(monkeypatch, exists_ids):
    """Reemplaza la función de validación interna para no requerir contexto Flask/DB."""

    def _mock_assert(fid):
        if fid not in exists_ids:
            raise ValueError(f"Fabricante {fid} no existe")

    monkeypatch.setattr(ProductoService, "_assert_fabricante_exists", staticmethod(_mock_assert))

# ------------------------------------------------------------------
# fixture cliente Flask
# ------------------------------------------------------------------ cliente Flask
# ------------------------------------------------------------------
@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(producto_bp, url_prefix="/api/productos")
    return app.test_client()

# ------------------------------------------------------------------
# casos
# ------------------------------------------------------------------

def test_csv_ok(monkeypatch, client):
    csv_data = (
        "nombre,fabricante_id,cantidad,precio,moneda,bodega,estante,pasillo\n"
        "Laptop,1,5,1200,USD,B1,E1,P1\n"
        "Mouse,2,10,30,COP,B1,E1,P1\n"
    )
    monkeypatch.setattr(ProductoService, "registrar_producto_individual", lambda *a, **k: None)
    patch_fabricante_exists(monkeypatch, exists_ids=[1, 2])
    resp = client.post(
        "/api/productos/upload",
        data={"file": (BytesIO(csv_data.encode()), "ok.csv")},
        content_type="multipart/form-data",
    )
    assert resp.status_code == 201
    assert resp.get_json()["inserted"] == 2


def test_csv_fabricante_inexistente(monkeypatch, client):
    csv_data = (
        "nombre,fabricante_id,cantidad,precio,moneda,bodega,estante,pasillo\n"
        "Teclado,99,5,80,USD,B1,E1,P1\n"
    )
    monkeypatch.setattr(ProductoService, "registrar_producto_individual", lambda *a, **k: None)
    patch_fabricante_exists(monkeypatch, exists_ids=[1, 2])
    resp = client.post(
        "/api/productos/upload",
        data={"file": (BytesIO(csv_data.encode()), "err.csv")},
        content_type="multipart/form-data",
    )
    body = resp.get_json()
    assert resp.status_code == 200
    assert body["inserted"] == 0
    assert "no existe" in body["errors"][0]


# ------------------------------------------------------------------
# tests individual API (moneda & fabricante)
# ------------------------------------------------------------------

def test_individual_fabricante_inexistente(monkeypatch, client):
    # ── stub que simula la validación y lanza el ValueError ──
    def _mock_registrar(**kwargs):
        raise ValueError(f"Fabricante {kwargs['fabricante_id']} no existe")

    monkeypatch.setattr(
        ProductoService,
        "registrar_producto_individual",
        lambda *a, **k: _mock_registrar(**k),
    )

    data = {
        "nombre": "Monitor",
        "fabricanteId": 99,
        "cantidad": 2,
        "precio": 800,
        "moneda": "USD",
        "bodega": "B1",
        "estante": "E2",
        "pasillo": "P4",
    }

    resp = client.post("/api/productos", json=data)
    assert resp.status_code == 400
    assert "no existe" in resp.get_json()["error"]
