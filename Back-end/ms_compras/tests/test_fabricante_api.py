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
    with app.test_client() as client:
        yield client

def test_crear_fabricante_valido(client):
    payload = {
        "nombre": "Fábrica Prueba",
        "correo": "prueba@ejemplo.com",
        "telefono": "1234567",
        "empresa": "Empresa Prueba"
    }
    response = client.post("/api/fabricantes", json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data
    assert data["nombre"] == payload["nombre"]

def test_crear_fabricante_telefono_invalido(client):
    payload = {
        "nombre": "Fábrica Prueba",
        "correo": "prueba@ejemplo.com",
        "telefono": "abc123",  # Inválido
        "empresa": "Empresa Prueba"
    }
    response = client.post("/api/fabricantes", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "errors" in data