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
            "nombre": "Carlos Gomez",
            "correo": "cgomez@gmail.com",
            "direccion": "Avenida Siempre Viva 123",
            "telefono": "111-222-333",
            "latitud": 15.6789,
            "longitud": 25.9876
        }
        self.plan_data_2 = {
            "nombre": "Ana Torres",
            "correo": "atorres@gmail.com",
            "direccion": "Calle Falsa 456",
            "telefono": "444-555-666",
            "latitud": 12.3456,
            "longitud": 34.5678
        }
        with patch('src.commands.create_plan.registrarUsuarioEnFirebase', return_value="plane_1"):
            CreatePlan(self.plan_data_1).execute()
        with patch('src.commands.create_plan.registrarUsuarioEnFirebase', return_value="plane_2"):
            CreatePlan(self.plan_data_2).execute()

    def test_get_all_plans(self):
        plans = GetAllPlans().execute()

        assert len(plans) == 2
        assert plans[0]['nombre'] == "Carlos Gomez"
        assert plans[1]['nombre'] == "Ana Torres"

    def teardown_method(self):
        self.session.close()
        Base.metadata.drop_all(bind=engine)