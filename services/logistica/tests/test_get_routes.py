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

def test_get_route(client):
    route_resp = generate_route(client)
    route_resp_json = json.loads(route_resp.data)
    id = route_resp_json["route_id"]
    response = client.get(
            f'/route/{id}',
            content_type='application/json'
        )
    assert response.status_code == 200
    resp_json = json.loads(response.data)
    assert 'id' in resp_json
    assert resp_json["id"] == id

def test_get_routes(client):
    generate_route(client)
    response = client.get(
            f'/api/route',
            content_type='application/json'
        )
    assert response.status_code == 200
    resp_json = json.loads(response.data)
    assert len(resp_json) == 1
