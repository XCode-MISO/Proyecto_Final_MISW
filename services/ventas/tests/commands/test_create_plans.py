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
            "fecha": "2020-08-10T12:00:00.000Z",
            "descripcion": "atorres@gmail.com",
            "vendedores": [{"id":"9a04bf1b-fd15-4877-9c46-d6309e1b26fb"}]
        }
        plan = CreatePlan(data).execute()

        assert 'id' in plan
        assert 'createdAt' in plan

        plans = self.session.query(Plan).all()
        assert len(plans) == 1
        assert plans[0].fecha == "2020-08-10T12:00:00.000Z"

    def teardown_method(self):
        self.session.close()
        Base.metadata.drop_all(bind=engine)