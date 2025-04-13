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
        # Insertar algunos fabricantes para probar
        from models.fabricante import Fabricante
        fab1 = Fabricante(nombre="Fábrica Uno", correo="uno@fab.com", telefono="1234567", empresa="Empresa Uno")
        fab2 = Fabricante(nombre="Fábrica Dos", correo="dos@fab.com", telefono="7654321", empresa="Empresa Dos")
        db.session.add(fab1)
        db.session.add(fab2)
        db.session.commit()
    with app.test_client() as client:
        yield client

def test_listar_fabricantes(client):
    response = client.get("/api/fabricantes")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 2

def test_crear_fabricante_success(client):
    """Prueba la creación exitosa de un fabricante mediante POST."""
    # Datos válidos para crear un nuevo fabricante
    payload = {
        "nombre": "Fábrica Tres",
        "correo": "tres@fab.com",
        "telefono": "5551234",
        "empresa": "Empresa Tres"
    }
    response = client.post("/api/fabricantes", json=payload)
    assert response.status_code == 201, f"Se esperaba 201, se obtuvo {response.status_code}"
    data = response.get_json()
    # Suponemos que el endpoint devuelve algún identificador o mensaje de éxito
    assert "id" in data or "message" in data, "La respuesta debe incluir un id o un mensaje de éxito"

def test_crear_fabricante_validation_error(client):
    """Prueba que al enviar datos incompletos se retorne un error de validación."""
    # Omitimos el campo "correo", que es obligatorio
    payload = {
        "nombre": "Fábrica Incompleta",
        "telefono": "5550000",
        "empresa": "Empresa Incompleta"
    }
    response = client.post("/api/fabricantes", json=payload)
    # Se espera 400 (o el código de error definido) por error de validación
    assert response.status_code == 400, f"Se esperaba 400, se obtuvo {response.status_code}"
    data = response.get_json()
    assert "error" in data, "La respuesta debe incluir el campo 'error'"
    # Puedes agregar comprobaciones específicas según la estructura de errores que implementes