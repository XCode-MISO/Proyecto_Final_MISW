import io, json, pytest
import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent / "src"))

from src.app import create_app, db


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


def test_upload_video_ok(client):
    """POST /api/upload debe devolver 201 y un job_id en estado pending."""
    data = {"video": (io.BytesIO(b"fake video"), "video.mp4")}
    rv = client.post("/api/upload", data=data, content_type="multipart/form-data")

    assert rv.status_code == 201
    resp = json.loads(rv.data)
    assert resp.get("status") == "pending" and "job_id" in resp