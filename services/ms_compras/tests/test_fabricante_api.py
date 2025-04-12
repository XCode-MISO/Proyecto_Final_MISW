import pytest
import io
from app import create_app
from models.db import db

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    # Para pruebas se usa SQLite en memoria
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
       
        db.create_all()
        # Insertamos algunos fabricantes de prueba
        from models.fabricante import Fabricante
        fab1 = Fabricante(nombre="Fábrica Uno", correo="uno@fab.com", telefono="1234567", empresa="Empresa Uno")
        fab2 = Fabricante(nombre="Fábrica Dos", correo="dos@fab.com", telefono="7654321", empresa="Empresa Dos")
        db.session.add_all([fab1, fab2])
        db.session.commit()
    with app.test_client() as client:
        yield client

def test_listar_fabricantes(client):
    """
    Prueba el endpoint de listado de fabricantes y verifica que se obtengan al menos dos registros,
    validando que cada registro tenga los campos obligatorios.
    """
    response = client.get("/api/fabricantes")
    assert response.status_code == 200, f"Se esperaba 200, se obtuvo {response.status_code}"
    data = response.get_json()
    # Verifica que la respuesta sea una lista
    assert isinstance(data, list), f"Se esperaba una lista, se obtuvo {type(data)}"
    assert len(data) >= 2, f"Se esperaban 2 o más elementos, se obtuvo {len(data)}"
    # Validamos que cada fabricante contenga los campos obligatorios (ajusta estos nombres según tu modelo)
    required_fields = {"id", "nombre", "correo", "telefono", "empresa"}
    for fab in data:
        missing = required_fields - fab.keys()
        assert not missing, f"El fabricante {fab} no tiene los campos: {missing}"

def test_listar_fabricantes_vacio(client):
    """
    Verifica el comportamiento cuando no existen fabricantes.
    Se limpia la base de datos y se recrea sin insertar registros.
    """
    with client.application.app_context():
        db.drop_all()
        db.create_all()

    response = client.get("/api/fabricantes")
    assert response.status_code == 200, f"Se esperaba 200, se obtuvo {response.status_code}"
    data = response.get_json()
    assert isinstance(data, list), f"Se esperaba una lista, se obtuvo {type(data)}"
    assert len(data) == 0, f"Se esperaba una lista vacía, se obtuvieron {len(data)} elementos"

def test_crear_fabricante_exitoso(client):
    """
    Prueba la creación exitosa de un fabricante.
    Se espera que el endpoint retorne 201 y que en la respuesta se incluya la información creada.
    """
    payload = {
        "nombre": "Fábrica Tres",
        "correo": "tres@fab.com",
        "telefono": "987654321",
        "empresa": "Empresa Tres"
    }
    response = client.post("/api/fabricantes", json=payload)
    assert response.status_code == 201, f"Se esperaba 201, se obtuvo {response.status_code}"
    data = response.get_json()
    # Puedes validar que la respuesta contenga al menos un campo de identificación y que los datos coincidan
    assert "id" in data, "La respuesta debe incluir el campo 'id'"
    for key in payload:
        assert data.get(key) == payload[key], f"El campo {key} no coincide: se esperaba {payload[key]}, se obtuvo {data.get(key)}"

def test_crear_fabricante_falla_validacion(client):
    """
    Prueba la creación de un fabricante con datos incompletos (ejemplo, sin el campo 'correo').
    Se espera que el endpoint retorne un error 400 y detalle el problema.
    """
    payload = {
        "nombre": "Fábrica Incompleta",
        # Falta el campo 'correo'
        "telefono": "123123123",
        "empresa": "Empresa Incompleta"
    }
    response = client.post("/api/fabricantes", json=payload)
    assert response.status_code == 400, f"Se esperaba 400, se obtuvo {response.status_code}"
    data = response.get_json()
    # Se ajusta para verificar la clave 'errors'
    assert "errors" in data, "La respuesta debe contener la clave 'errors'"