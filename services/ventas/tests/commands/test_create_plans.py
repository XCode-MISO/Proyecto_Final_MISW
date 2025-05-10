from src.commands.create_plan import CreatePlan
from src.session import Session, engine
from src.models.model import Base
from src.models.plan import Plan
from src.models.visit import Visit
from unittest.mock import patch

class TestCreatePlan():

    def setup_method(self):
        Base.metadata.create_all(engine)
        self.session = Session()

    def test_create_plan(self):
        data = {
            "nombre": "Maria Lopez",
            "correo": "mlopez@gmail.com",
            "direccion": "Calle 123",
            "telefono": "123-456-789",
            "latitud": 10.1234,
            "longitud": 20.5678
        }
        plan = CreatePlan(data).execute()

        assert 'id' in plan
        assert 'createdAt' in plan

        plans = self.session.query(Plan).all()
        assert len(plans) == 1
        assert plans[0].nombre == "Maria Lopez"

    def teardown_method(self):
        self.session.close()
        Base.metadata.drop_all(bind=engine)