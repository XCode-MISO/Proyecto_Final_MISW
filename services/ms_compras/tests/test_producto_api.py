import json
import io
import pytest
from unittest.mock import patch, MagicMock
from app import create_app

# Configuración del fixture para el cliente de prueba (usando SQLite en memoria)
@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.app_context():
        from models.db import db
        db.create_all()
    
        from models.fabricante import Fabricante
        fab = Fabricante(nombre="Test Fabricante", correo="test@fab.com", telefono="1234567", empresa="Test Inc")
        db.session.add(fab)
        db.session.commit()
    with app.test_client() as client:
        yield client

@patch("services.producto_service.pubsub_v1.PublisherClient")
def test_registrar_producto_con_ubicacion_success(mock_pub_client, client):
    mock_instance = MagicMock()
    mock_instance.publish.return_value.result.return_value = "mensaje_id"
    mock_pub_client.return_value = mock_instance

    payload = {
        "nombre": "Producto Compra Ejemplo",
        "fabricanteId": 1,
        "cantidad": 5,
        "precio": 29.99,
        "moneda": "USD",
        "bodega": "Bodega Central",
        "estante": "Estante 1",
        "pasillo": "Pasillo A"
    }
    response = client.post("/api/productos", json=payload)
    assert response.status_code == 201, f"Se esperaba 201, se obtuvo {response.status_code}"
    data = response.get_json()
    assert "message" in data, "Falta la clave 'message' en la respuesta."
    assert "Compra" in data, "Falta la clave 'Compra' en la respuesta."
    detalle = data["Compra"]
    # Verificamos que se devuelven los campos básicos:
    assert "productoId" in detalle, "Falta 'productoId' en la respuesta."
    assert "fabricanteId" in detalle, "Falta 'fabricanteId' en la respuesta."
    assert "cantidad" in detalle, "Falta 'cantidad' en la respuesta."
    assert "precio" in detalle, "Falta 'precio' en la respuesta."

@patch("services.producto_service.pubsub_v1.PublisherClient")
def test_registrar_producto_validation_error(mock_pub_client, client):
    mock_instance = MagicMock()
    mock_pub_client.return_value = mock_instance

    # Payload sin "precio"
    payload = {
        "nombre": "Producto Compra Ejemplo",
        "fabricanteId": 1,
        "cantidad": 5,
        "moneda": "USD",
        "bodega": "Bodega Central",
        "estante": "Estante 1",
        "pasillo": "Pasillo A"
    }
    response = client.post("/api/productos", json=payload)
    assert response.status_code == 400, f"Se esperaba 400, se obtuvo {response.status_code}"
    data = response.get_json()
    assert "error" in data or "details" in data, "La respuesta debe indicar error de validación."

def test_registrar_producto_without_pubsub(client):
    
    client.application.config["DISABLE_PUBSUB"] = True

    payload = {
        "nombre": "Producto Compra Ejemplo Sin PubSub",
        "fabricanteId": 1,
        "cantidad": 5,
        "precio": 29.99,
        "moneda": "USD",
        "bodega": "Bodega Central",
        "estante": "Estante 1",
        "pasillo": "Pasillo A"
    }
    response = client.post("/api/productos", json=payload)
    assert response.status_code == 201, f"Se esperaba 201, se obtuvo {response.status_code}"
    data = response.get_json()
    # Verificamos que la respuesta contiene la estructura esperada
    assert "message" in data, "Falta 'message' en la respuesta"
    assert "Compra" in data, "Falta 'Compra' en la respuesta"
    detalle = data["Compra"]
    assert detalle.get("productoId") is not None, "Falta productoId"
    assert detalle.get("fabricanteId") is not None, "Falta fabricanteId"
    assert detalle.get("cantidad") == 5, "La cantidad no es la esperada"
    assert float(detalle.get("precio")) == 29.99, "El precio no es el esperado"