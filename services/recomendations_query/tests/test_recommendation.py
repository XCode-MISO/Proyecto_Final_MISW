
import json, pytest
from src.app import create_app, db
from src.models import Recommendation


@pytest.fixture
def client():
    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    with app.app_context():
        db.create_all()
        rec = Recommendation(
            job_id=1,                  
            final_state="pending",
            final_recommendation="",
            recommendation_data={},
            identified_objects=[],
        )
        db.session.add(rec)
        db.session.commit()

    with app.test_client() as c:
        yield c

    with app.app_context():
        db.drop_all()


def test_health_ok(client):
    rv = client.get("/api/health")      
    assert rv.status_code == 200
    assert rv.data == b"OK"


def test_get_recommendation_ok(client):
    rv = client.get("/api/recommend", query_string={"job_id": "1"})
    assert rv.status_code == 200
    data = json.loads(rv.data)
    assert data["job_id"] == 1
    assert data["final_state"] == "pending"


def test_get_recommendation_not_found(client):
    rv = client.get("/api/recommend", query_string={"job_id": "999"})
    assert rv.status_code == 404
    assert "error" in rv.get_json()

def test_recommendation_has_suggestions(client, monkeypatch):

    monkeypatch.setattr(
        'src.services.recommendation_service.fetch_inventory_for_orders',
        lambda: [
            {"producto_id": 1, "nombre": "pan", "precio": 2.5, "stock": 10},
            {"producto_id": 2, "nombre": "jabon", "precio": 3.0, "stock": 15},
        ]
    )
    resp = client.get('/recommend?job_id=123')
    data = resp.get_json()
    assert 'recommended_products' in data
    assert len(data['recommended_products']) > 0