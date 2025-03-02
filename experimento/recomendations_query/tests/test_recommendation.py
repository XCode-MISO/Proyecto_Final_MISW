import json
import pytest
from src.app import create_app, db

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

def test_update_and_get_recommendation(client):
    payload = {
        'job_id': 1,
        'final_state': 'processed',
        'final_recommendation': 'Reorganiza las estanterías para mejorar la visibilidad.',
        'recommendation_data': {"heuristics": "Simple ratio analysis"}
    }
    response = client.post('/api/update_recommendation', json=payload)
    assert response.status_code == 200

    response = client.get('/api/recommend?job_id=1')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data['job_id'] == 1
    assert data['final_state'] == 'processed'
    assert data['final_recommendation'] == 'Reorganiza las estanterías para mejorar la visibilidad.'
    assert 'heuristics' in data['recommendation_data']
