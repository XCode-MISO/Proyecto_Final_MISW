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