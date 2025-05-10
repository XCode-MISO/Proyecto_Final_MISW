from src.session import Session, engine
from src.models.model import Base
from src.main import app
import json
from unittest.mock import patch

class TestPlans():
    def setup_method(self):
        Base.metadata.create_all(engine)
        self.session = Session()

    def test_create_plan(self):
        with app.test_plan() as test_plan:
            response = test_plan.post(
                '/api/plans', json={
                    "fecha": "2020-08-10T12:00:00.000Z",
                    "descripcion": "Plan de prueba",
                    "vendedores": [{
                        id: "1234",
                    }]
                }
            )
            response_json = json.loads(response.data)

            assert response.status_code == 201
            assert 'id' in response_json
            assert 'createdAt' in response_json

    def teardown_method(self):
        self.session.close()
        Base.metadata.drop_all(bind=engine)