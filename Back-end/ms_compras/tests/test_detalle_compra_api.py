import pytest
from app import create_app
from models.db import db

@pytest.fixture
def client():
    # Crea la app y configura el ambiente de test
    app = create_app()

    # Configura la app para testing y usa SQLite en memoria
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    # Dentro del application context, inicializa la base de datos con la configuración actualizada
    with app.app_context():
        # Asegurarse de que la DB se inicialice con la URI de test
        db.init_app(app)
        db.drop_all()
        db.create_all()

        # Inserta un fabricante de prueba (esto dependerá de cómo esté definido tu modelo)
        from models.fabricante import Fabricante
        fab = Fabricante(nombre="Test Fabricante", correo="test@fab.com", telefono="1234567", empresa="Test Inc")
        db.session.add(fab)
        db.session.commit()

    # Crea el test client y lo retorna para que las pruebas lo usen
    with app.test_client() as client:
        yield client

def test_registrar_detalle_compra_exitoso(client):
    payload = {
        "nombre": "Producto Compra Test",
        "fabricanteId": 1,   # Se asume que el fabricante insertado tiene ID 1
        "cantidad": 5,
        "precio": 19.99
    }
    response = client.post("/api/compras/detalle", json=payload)
    assert response.status_code == 201, f"Se esperaba 201, se obtuvo {response.status_code}"
    data = response.get_json()
    assert data.get("message") == "Detalle de compra registrado exitosamente"
    assert "detalleCompra" in data
    assert data["detalleCompra"].get("compraId") is not None
    assert data["detalleCompra"].get("productoId") is not None

def test_registrar_detalle_compra_falla_validacion(client):
    # Falta el campo "precio"
    payload = {
        "nombre": "Producto Compra Test",
        "fabricanteId": 1,
        "cantidad": 5
    }
    response = client.post("/api/compras/detalle", json=payload)
    assert response.status_code == 400, f"Se esperaba 400, se obtuvo {response.status_code}"
    data = response.get_json()
    assert "error" in data


def test_registrar_detalle_compra_error_interno(monkeypatch, client):
    # Utilizamos monkeypatch para forzar que la función del servicio lance un error inesperado.
    from services.detalle_compra_service import DetalleCompraService

    def fake_registrar_detalle_compra(*args, **kwargs):
        raise Exception("Error simulado en el servicio")

    monkeypatch.setattr(DetalleCompraService, "registrar_detalle_compra_individual", fake_registrar_detalle_compra)

    payload = {
        "nombre": "Producto Compra Ejemplo",
        "fabricanteId": 1,
        "cantidad": 10,
        "precio": 29.99
    }
    response = client.post("/api/compras/detalle", json=payload)
    assert response.status_code == 500, f"Se esperaba 500, se obtuvo {response.status_code}"
    data = response.get_json()
    assert "error" in data, "Se esperaba un mensaje de error en la respuesta"
    assert "Error al registrar el detalle de compra" in data.get("error"), "El mensaje de error no es el esperado"