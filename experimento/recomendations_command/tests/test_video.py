import io
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

def test_upload_video(client):
    data = {
        'video': (io.BytesIO(b"fake video content"), 'video.mp4')
    }
    response = client.post('/api/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 201
    resp_json = json.loads(response.data)
    assert 'job_id' in resp_json
    assert resp_json['status'] == 'pending'
