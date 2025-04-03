import io
import json
import sys
import uuid
import pytest
from logistica.app import create_app, db
from unittest.mock import MagicMock

sys.modules["google.cloud.pubsub_v1"] = MagicMock()
sys.modules["googlemaps"] = MagicMock()
sys.modules["googlemaps.client"] = MagicMock()


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
    with app.test_client() as client:
        yield client
    with app.app_context():
        db.drop_all()


def generate_route(client):
    data = {
        "paradas": [
            {
                "id": str(uuid.uuid4()),
                "cliente": {
                    "direccion": "Cra. 11, 82-71, Bogotá, Colombia"
                },
                "nombre":"Parada 1",
                "fecha": "01/02/2026"
            },
            {
                "id": str(uuid.uuid4()),
                "cliente": {
                    "direccion": "Calle 149, 16-56, Bogotá, Colombia"
                },
                "nombre":"Parada 2",
                "fecha": "01/02/2025"
            },
            {
                "id": str(uuid.uuid4()),
                "cliente": {
                    "direccion": "Cl. 114a #45-78, Bogota, Colombia"
                }
            }
        ],
        "inicio": "Cl. 114a #45-78, Bogota, Colombia",
        "fin": "Cl. 114a #45-78, Bogota, Colombia",
        "nombre": "Ruta 1"
    }
    response = client.post('/generate-route', data=json.dumps(data),
                           content_type='application/json')
    return response

def test_generate_route(client):
    response = generate_route(client)
    assert response.status_code == 200
    resp_json = json.loads(response.data)
    assert resp_json['distancia'] == 18458
    assert 'mapsResponse' in resp_json
    assert resp_json['tiempoEstimado'] == 2602
