from src.commands.get_client import GetClient
from src.commands.create_client import CreateClient
from src.session import Session, engine
from src.models.model import Base
from src.models.client import Client
from src.models.visit import Visit
from unittest.mock import patch

class TestGetClient():

    def setup_method(self):
        Base.metadata.create_all(engine)
        self.session = Session()

        # Create a sample client
        self.client_data = {
            "nombre": "Sofia Ramirez",
            "correo": "sramirez@gmail.com",
            "direccion": "Carrera 45 #12-34",
            "telefono": "123-456-789",
            "latitud": 5.6789,
            "longitud": 10.1234
        }
        with patch('src.commands.create_client.registrarUsuarioEnFirebase', return_value="xxxxxxxxxxxxxx"):
            self.client = CreateClient(self.client_data).execute()

    def test_get_client(self):
        client = GetClient(self.client['id']).execute()

        assert client['id'] == self.client['id']
        assert client['nombre'] == "Sofia Ramirez"
        assert client['correo'] == "sramirez@gmail.com"

    def teardown_method(self):
        self.session.close()
        Base.metadata.drop_all(bind=engine)