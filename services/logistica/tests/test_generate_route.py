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


def test_generate_route(client):
    data = {
        "pedidos": [
            {
                "id": str(uuid.uuid4()),
                "cliente": {
                    "direccion": "Cra. 1 #18a-12, Bogota, Colombia"
                }
            },
            {
                "id": str(uuid.uuid4()),
                "cliente": {
                    "direccion": "Ak 7 #N. 28-66, Bogotá, Colombia"
                }
            },
            {
                "id": str(uuid.uuid4()),
                "cliente": {
                    "direccion": "Cl. 114a #45-78, Bogota, Colombia"
                }
            }
        ]
    }
    response = client.post('/generate-route', data=json.dumps(data),
                           content_type='application/json')
    assert response.status_code == 200
    resp_json = json.loads(response.data)
    assert resp_json['distancia'] == 41896
    assert 'mapsResponse' in resp_json
    assert resp_json['tiempoEstimado'] == 5305
