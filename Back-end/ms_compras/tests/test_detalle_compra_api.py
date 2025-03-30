# ms_compras/tests/test_detalle_compra_api.py
import pytest
from app import create_app
from models.db import db

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        # Insertar un fabricante para validar el endpoint
        from models.fabricante import Fabricante
        fab = Fabricante(nombre="Test Fabricante", correo="test@fab.com", telefono="1234567", empresa="Test Inc")
        db.session.add(fab)
        db.session.commit()
    with app.test_client() as client:
        yield client

def test_registrar_detalle_compra_exitoso(client):
    payload = {
        "nombre": "Producto Compra Test",
        "fabricanteId": 1,
        "cantidad": 5,
        "precio": 19.99
    }
    response = client.post("/api/compras/detalle", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data.get("message") == "Detalle de compra registrado exitosamente"
    assert "detalleCompra" in data
    assert data["detalleCompra"]["compraId"] is not None
    assert data["detalleCompra"]["productoId"] is not None

def test_registrar_detalle_compra_falla_validacion(client):
    # Falta el campo "precio"
    payload = {
        "nombre": "Producto Compra Test",
        "fabricanteId": 1,
        "cantidad": 5
    }
    response = client.post("/api/compras/detalle", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data