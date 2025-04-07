from src.commands.get__all_clients import GetAllClients
from src.commands.create_client import CreateClient
from src.session import Session, engine
from src.models.model import Base
from src.models.client import Client

class TestGetAllClients():

    def setup_method(self):
        Base.metadata.create_all(engine)
        self.session = Session()

        # Create sample clients
        self.client_data_1 = {
            "nombre": "Carlos Gomez",
            "correo": "cgomez@gmail.com",
            "direccion": "Avenida Siempre Viva 123",
            "telefono": "111-222-333",
            "latitud": 15.6789,
            "longitud": 25.9876
        }
        self.client_data_2 = {
            "nombre": "Ana Torres",
            "correo": "atorres@gmail.com",
            "direccion": "Calle Falsa 456",
            "telefono": "444-555-666",
            "latitud": 12.3456,
            "longitud": 34.5678
        }
        CreateClient(self.client_data_1).execute()
        CreateClient(self.client_data_2).execute()

    def test_get_all_clients(self):
        clients = GetAllClients().execute()

        assert len(clients) == 2
        assert clients[0]['nombre'] == "Carlos Gomez"
        assert clients[1]['nombre'] == "Ana Torres"

    def teardown_method(self):
        self.session.close()
        Base.metadata.drop_all(bind=engine)