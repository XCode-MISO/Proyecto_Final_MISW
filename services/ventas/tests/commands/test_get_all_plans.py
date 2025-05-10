from src.commands.get_all_plans import GetAllPlans
from src.commands.create_plan import CreatePlan
from src.session import Session, engine
from src.models.model import Base
from src.models.plan import Plan
from src.models.visit import Visit
from unittest.mock import patch

class TestGetAllPlans():

    def setup_method(self):
        Base.metadata.create_all(engine)
        self.session = Session()

        # Create sample plans
        self.plan_data_1 = {
            "fecha": "2020-08-10T13:00:00.000Z",
            "descripcion": "cgomez@gmail.com",
            "vendedores": [{"id":"9a04bf1b-fd15-4877-9c46-d6309e1b26fb"}]
        }
        self.plan_data_2 = {
            "fecha": "2020-08-10T12:00:00.000Z",
            "descripcion": "atorres@gmail.com",
            "vendedores": [{"id":"9a04bf1b-fd15-4877-9c46-d6309e1b26fb"}]
        }
        CreatePlan(self.plan_data_1).execute()
        CreatePlan(self.plan_data_2).execute()

    def test_get_all_plans(self):
        plans = GetAllPlans().execute()

        assert len(plans) == 2
        assert plans[0]['fecha'] == "2020-08-10T13:00:00.000Z"
        assert plans[1]['fecha'] == "2020-08-10T12:00:00.000Z"

    def teardown_method(self):
        self.session.close()
        Base.metadata.drop_all(bind=engine)