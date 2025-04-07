from src.commands.get_all_visits import GetAllVisits
from src.commands.create_client import CreateClient
from src.commands.create_visit import CreateVisit
from src.session import Session, engine
from src.models.model import Base
from src.models.visit import Visit

class TestGetAllVisits():

    def setup_method(self):
        Base.metadata.create_all(engine)
        self.session = Session()

        # Create a sample client
        self.client_data = {
            "nombre": "Luis Martinez",
            "correo": "lmartinez@gmail.com",
            "direccion": "Calle Principal 789",
            "telefono": "777-888-999",
            "latitud": 10.1234,
            "longitud": 20.5678
        }
        self.client = CreateClient(self.client_data).execute()

        # Create sample visits
        self.visit_data_1 = {
            "client_id": self.client['id'],
            "fechaVisita": "2023-10-27T12:00:00",
            "informe": "Informe de visita 1",
            "latitud": 10.1234,
            "longitud": 20.5678
        }
        self.visit_data_2 = {
            "client_id": self.client['id'],
            "fechaVisita": "2023-10-28T14:00:00",
            "informe": "Informe de visita 2",
            "latitud": 11.1234,
            "longitud": 21.5678
        }
        CreateVisit(self.visit_data_1).execute()
        CreateVisit(self.visit_data_2).execute()

    def test_get_all_visits(self):
        visits = GetAllVisits().execute()

        assert len(visits) == 2
        assert visits[0]['informe'] == "Informe de visita 1"
        assert visits[1]['informe'] == "Informe de visita 2"

    def teardown_method(self):
        self.session.close()
        Base.metadata.drop_all(bind=engine)