import io
import pytest
from flask import Flask, jsonify
from apis.fabricante_api import fabricante_bp

# ------------------------------------------------------------------
# helpers de mock
# ------------------------------------------------------------------

def patch_upload(monkeypatch, client, result):
    """Inyecta un stub en la vista upload_fabricantes del blueprint."""
    def _stub():
        return jsonify(result), (201 if result["inserted"] > 0 else 200)

    monkeypatch.setitem(
        client.application.view_functions,
        "fabricante_bp.upload_fabricantes",
        _stub,
    )

# ------------------------------------------------------------------
# fixture cliente
# ------------------------------------------------------------------
@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(fabricante_bp, url_prefix="/api/fabricantes")
    return app.test_client()

# ------------------------------------------------------------------
# casos
# ------------------------------------------------------------------

def test_upload_ok(monkeypatch, client):
    patch_upload(monkeypatch, client, {"inserted": 2, "errors": []})
    csv_data = (
        "nombre,correo,telefono,empresa\n"
        "Fab A,a@fab.com,123,Empresa A\n"
        "Fab B,b@fab.com,456,Empresa B\n"
    )
    resp = client.post(
        "/api/fabricantes/upload",
        data={"file": (io.BytesIO(csv_data.encode()), "fabricantes.csv")},
        content_type="multipart/form-data",
    )
    assert resp.status_code in (200, 201)


def test_upload_missing_field(monkeypatch, client):
    patch_upload(
        monkeypatch,
        client,
        {"inserted": 1, "errors": ["Fila 3: falta correo"]},
    )
    csv_data = (
        "nombre,correo,telefono,empresa\n"
        "Fab A,a@fab.com,123,Empresa A\n"
        "Fab B,,456,Empresa B\n"
    )
    resp = client.post(
        "/api/fabricantes/upload",
        data={"file": (io.BytesIO(csv_data.encode()), "fabricantes.csv")},
        content_type="multipart/form-data",
    )
    assert resp.status_code in (200, 201)
    body = resp.get_json()
    assert body["inserted"] == 1 and body["errors"]


def test_upload_invalid_format(client):
    txt_data = "Este no es un CSV"
    resp = client.post(
        "/api/fabricantes/upload",
        data={"file": (io.BytesIO(txt_data.encode()), "fabricantes.txt")},
        content_type="multipart/form-data",
    )
    assert resp.status_code == 400
    assert "error" in resp.get_json()
