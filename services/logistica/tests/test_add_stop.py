import io
import json
import sys
import uuid
import pytest
from logistica.app import create_app, db
from unittest.mock import MagicMock

from logistica.tests.test_generate_route import generate_route

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


def add_stop(client, route_id):
    data = {
        "parada": {
            "cliente": {
                "direccion": "Cra. 11, 82-71, Bogotá, Colombia",
                "nombre": "Cliente 1"
            },
            "vendedor": {
                "direccion": "Calle 149, 16-56, Bogotá, Colombia",
                "nombre": "Vendedor 1"
            },
            "nombre": "Parada 3",
            "fecha": "01/02/2026"
        },
        "id": route_id

    }
    response = client.post('/api/add-stop-route', data=json.dumps(data),
                           content_type='application/json')
    return response


def test_add_stop(client):
    route_resp = generate_route(client)
    route_resp_json = json.loads(route_resp.data)
    id = route_resp_json["route_id"]
    
    
    route_resp_update = add_stop(client, id)
    route_resp_update_json = json.loads(route_resp_update.data)

    response = client.get(
        f'/route/{id}',
        content_type='application/json'
    )

    assert response.status_code == 200
    route_resp_update_json = json.loads(response.data)
    assert 'id' in route_resp_update_json
    assert 'mapsResponse' in route_resp_update_json
