import pytest
from app import create_app
from models.db import db

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    # Usamos SQLite en memoria para las pruebas
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        # Insertar un fabricante para poder crear un producto
        from models.fabricante import Fabricante
        fab = Fabricante(nombre="Test Fabricante", correo="test@fab.com", telefono="1234567", empresa="Test Inc")
        db.session.add(fab)
        db.session.commit()
    with app.test_client() as client:
        yield client

def test_crear_producto_exitoso(client):
    payload = {
        "nombre": "Producto Test",
        "descripcion": "Descripción de producto test",
        "precioCompra": 100.0,
        "moneda": "USD"
    }
    
    response = client.post("/api/productos/fabricante/1", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data.get("id") is not None
    assert data["nombre"] == payload["nombre"]

def test_crear_producto_sin_nombre(client):
    payload = {
        "descripcion": "Sin nombre",
        "precioCompra": 100.0,
        "moneda": "USD"
    }
    response = client.post("/api/productos/fabricante/1", json=payload)
    # Como 'nombre' es obligatorio, debe retornar error
    assert response.status_code == 400