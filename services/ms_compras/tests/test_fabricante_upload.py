import io
import pytest
from app import create_app
from models.db import db
import os

@pytest.fixture
def client():
 
    # Crear la app
    app = create_app()

    # Forzar la configuración de test: usa SQLite en memoria
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        # En caso de usar SQLite en memoria, es recomendable hacer drop_all() y create_all()
        # si se quiere partir de una base limpia. (Ten en cuenta que si existen restricciones en cascada,
        # drop_all() podría fallar. En tal caso, podrías omitir drop_all())
      
        db.create_all()
    with app.test_client() as client:
        yield client

def test_upload_fabricantes_success(client):
    """
    Prueba la carga masiva exitosa de fabricantes con un archivo CSV válido.
    Se espera que se inserten 2 fabricantes y que no haya errores.
    """
    csv_content = (
        "nombre,correo,telefono,empresa\n"
        "Fabricante A,contactoA@example.com,1234567,Empresa A\n"
        "Fabricante B,contactoB@example.com,7654321,Empresa B\n"
    )
    data = {
        "file": (io.BytesIO(csv_content.encode('utf-8')), "fabricantes.csv")
    }
    response = client.post("/api/fabricantes/upload", content_type="multipart/form-data", data=data)
    print("Respuesta:", response.get_json())
    # Aceptamos 200 o 201
    assert response.status_code in (200, 201), f"Se esperaba 200 o 201, se obtuvo {response.status_code}"

def test_upload_fabricantes_with_missing_field(client):
    """
    Prueba la carga masiva con error: una fila sin el campo 'correo'.
    Se espera que se inserte solamente la fila completa y se reporte el error en la fila incompleta.
    """
    csv_content = (
        "nombre,correo,telefono,empresa\n"
        "Fabricante A,contactoA@example.com,1234567,Empresa A\n"
        "Fabricante B,,7654321,Empresa B\n"  # Falta el correo en la fila 2
    )
    data = {
        "file": (io.BytesIO(csv_content.encode('utf-8')), "fabricantes.csv")
    }
    response = client.post("/api/fabricantes/upload", content_type="multipart/form-data", data=data)
    print("Respuesta:", response.get_json())
    # Aquí decidimos que en carga parcial se retorne 200 (o 201) según lo que definas en el endpoint
    assert response.status_code in (200, 201), f"Se esperaba 200 o 201, se obtuvo {response.status_code}"
    result = response.get_json()
    # Por ejemplo, se espera que solo se haya insertado 1 registro y se reporte al menos un error
    assert result.get("inserted") == 1, f"Se esperaba 1 inserción, se obtuvo {result.get('inserted')}"
    assert "errors" in result and len(result["errors"]) > 0, "Se esperaba la lista de errores"

def test_upload_fabricante_invalid_format(client):
    """
    Prueba la carga masiva con un archivo que no tiene formato CSV (por ejemplo, un archivo de texto sin delimitadores).
    Se espera que el endpoint rechace la carga y retorne un error 400 con un mensaje adecuado.
    """
    # El contenido no tiene estructura CSV válida
    csv_content = "Este no es un archivo CSV válido"
    data = {
        "file": (io.BytesIO(csv_content.encode("utf-8")), "fabricantes.txt")
    }
    response = client.post("/api/fabricantes/upload", data=data, content_type="multipart/form-data")
    json_data = response.get_json()
    # Se espera un error 400 indicando problema en el formato o en los campos
    assert response.status_code == 400, f"Se esperaba 400, se obtuvo {response.status_code}"
    assert "error" in json_data, "La respuesta debe contener una clave 'error' que indique la falla en el formato"