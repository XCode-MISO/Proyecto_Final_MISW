import io, json, pytest
from src.app import create_app, db
from unittest.mock import patch

@pytest.fixture
def client():
    """Flask test-client con BD SQLite en memoria."""
    app = create_app()
    app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URI="sqlite:///:memory:")
    with app.app_context():
        db.create_all()
    with app.test_client() as c:
        yield c
    # Clean-up
    with app.app_context():
        db.drop_all()


@patch("src.services.video_service.upload_to_cloud_storage")
def test_upload_video_ok(mock_upload, client):
    """POST /api/upload debe devolver 201 y un job_id en estado pending."""
    mock_upload.return_value = "https://fakeurl.com/fakevideo.mp4" 

    data = {"video": (io.BytesIO(b"fake video"), "video.mp4")}
    rv = client.post("/api/upload", data=data, content_type="multipart/form-data")

    assert rv.status_code == 201
    resp_json = rv.get_json()
    assert "job_id" in resp_json
    assert resp_json["status"] == "pending"