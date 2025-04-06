import pytest
from app import create_app
from models.db import db

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    # Para pruebas usamos SQLite en memoria
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
    with app.test_client() as client:
        yield client

def test_ping(client):
    response = client.get("/api/inventarios/ping")
    assert response.status_code == 200
    data = response.get_json()
    assert data.get("msg") == "ms_inventarios alive"