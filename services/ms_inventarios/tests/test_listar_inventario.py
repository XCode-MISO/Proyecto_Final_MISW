import os
import pytest
from app import create_app
from models.db import db

@pytest.fixture
def client():
    os.environ["DATABASE_URI"] = "sqlite:///:memory:"
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.drop_all()
        db.create_all()
    with app.test_client() as client:
        yield client

def test_listar_productos_inventario_vacio(client):
    response = client.get("/api/inventarios/productos")
    assert response.status_code == 200, f"Se esperaba 200, se obtuvo {response.status_code}"
    data = response.get_json()
    assert isinstance(data, list), "La respuesta no es una lista"
    assert len(data) == 0, f"Se esperaba una lista vacía, se obtuvieron {len(data)} elementos"