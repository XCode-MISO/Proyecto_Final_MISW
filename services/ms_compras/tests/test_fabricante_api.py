import pytest
from flask import Flask
from apis.fabricante_api import fabricante_bp
from services.fabricante_service import FabricanteService

# ------------------------------------------------------------------
# utilidades de prueba
# ------------------------------------------------------------------
class DummyFabricante(dict):
    def __init__(self, id_, nombre, correo, telefono, empresa):
        super().__init__(id=id_, nombre=nombre, correo=correo, telefono=telefono, empresa=empresa)
        self.id = id_
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono
        self.empresa = empresa


FAKE_FABS = [
    DummyFabricante(1, "Fab Uno", "uno@fab.com", "1234567", "Emp Uno"),
    DummyFabricante(2, "Fab Dos", "dos@fab.com", "7654321", "Emp Dos"),
]


def patch_listar(monkeypatch, client, result):
    """Reemplaza la función de lista registrada en el blueprint dentro de la app."""
    from flask import jsonify
    def _stub():
        return jsonify(result), 200
    monkeypatch.setitem(
        client.application.view_functions,
        "fabricante_bp.listar_fabricantes",
        _stub,
    )
    


def patch_crear(monkeypatch, *, should_fail=False):
    def _ok(**kwargs):
        return DummyFabricante(3, **kwargs)

    def _fail(**kwargs):
        raise ValueError("Datos inválidos")

    monkeypatch.setattr(
        FabricanteService,
        "crear_fabricante",
        staticmethod(_fail if should_fail else _ok),
    )

# ------------------------------------------------------------------
# fixture cliente Flask
# ------------------------------------------------------------------
@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(fabricante_bp, url_prefix="/api/fabricantes")
    return app.test_client()

# ------------------------------------------------------------------
# casos
# ------------------------------------------------------------------

def test_listar_ok(monkeypatch, client):
    patch_listar(monkeypatch, client, FAKE_FABS)
    resp = client.get("/api/fabricantes")
    assert resp.status_code == 200
    body = resp.get_json()
    assert isinstance(body, list) and len(body) == 2
    for fab in body:
        for field in ("id", "nombre", "correo", "telefono", "empresa"):
            assert field in fab


def test_listar_vacio(monkeypatch, client):
    patch_listar(monkeypatch, client, [])
    resp = client.get("/api/fabricantes")
    assert resp.status_code == 200
    assert resp.get_json() == []


def test_crear_ok(monkeypatch, client):
    patch_crear(monkeypatch)
    payload = {
        "nombre": "Fábrica Tres",
        "correo": "tres@fab.com",
        "telefono": "987654321",
        "empresa": "Empresa Tres",
    }
    resp = client.post("/api/fabricantes", json=payload)
    assert resp.status_code == 201
    body = resp.get_json()
    assert body.get("id") == 3
    for k, v in payload.items():
        assert body[k] == v


def test_crear_validacion(monkeypatch, client):
    patch_crear(monkeypatch, should_fail=True)
    payload = {
        "nombre": "Fábrica Incompleta",
        "telefono": "123123123",
        "empresa": "Empresa Inc",
    }
    resp = client.post("/api/fabricantes", json=payload)
    assert resp.status_code == 400
    body = resp.get_json()
    assert "error" in body or "errors" in body

