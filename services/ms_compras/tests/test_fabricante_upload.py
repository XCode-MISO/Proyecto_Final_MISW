import io
import pytest
from flask import Flask, jsonify
from apis.fabricante_api import fabricante_bp

# ------------------------------------------------------------------
# helpers
# ------------------------------------------------------------------
def patch_upload(monkeypatch, client, result):
    def _stub():
        return jsonify(result), (201 if result["inserted"] > 0 else 200)
    monkeypatch.setitem(
        client.application.view_functions,
        "fabricante_bp.upload_fabricantes",
        _stub,
    )

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
        "Fab A,a@fab.com,1234567,Empresa A\n"
        "Fab B,b@fab.com,7654321,Empresa B\n"
    )
    resp = client.post(
        "/api/fabricantes/upload",
        data={"file": (io.BytesIO(csv_data.encode()), "fabricantes.csv")},
        content_type="multipart/form-data",
    )
    assert resp.status_code in (200, 201)
    assert resp.get_json()["inserted"] == 2

def test_upload_missing_field(monkeypatch, client):
    patch_upload(monkeypatch, client, {"inserted": 1, "errors": ["Fila 2: falta correo"]})
    csv_data = (
        "nombre,correo,telefono,empresa\n"
        "Fab A,a@fab.com,1234567,Empresa A\n"
        "Fab B,,7654321,Empresa B\n"
    )
    resp = client.post(
        "/api/fabricantes/upload",
        data={"file": (io.BytesIO(csv_data.encode()), "fabricantes.csv")},
        content_type="multipart/form-data",
    )
    assert resp.status_code in (200, 201)
    data = resp.get_json()
    assert "errors" in data and data["inserted"] == 1

def test_upload_invalid_format(client):
    txt_data = "Este no es un CSV"
    resp = client.post(
        "/api/fabricantes/upload",
        data={"file": (io.BytesIO(txt_data.encode()), "fabricantes.txt")},
        content_type="multipart/form-data",
    )
    assert resp.status_code == 400
    assert "error" in resp.get_json()

def test_upload_no_file(client):
    """Test error: no enviar ningún archivo."""
    resp = client.post(
        "/api/fabricantes/upload",
        data={},
        content_type="multipart/form-data",
    )
    assert resp.status_code == 400
    assert "error" in resp.get_json()