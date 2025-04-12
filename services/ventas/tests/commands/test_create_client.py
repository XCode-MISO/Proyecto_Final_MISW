from src.commands.create_client import CreateClient
from src.session import Session, engine
from src.models.model import Base
from src.models.client import Client
from src.models.visit import Visit
from unittest.mock import patch

class TestCreateClient():

    def setup_method(self):
        Base.metadata.create_all(engine)
        self.session = Session()

    @patch('src.commands.create_client.registrarUsuarioEnFirebase', return_value="test_client")
    def test_create_client(self, mock_registrar_usuario):
        data = {
            "nombre": "Maria Lopez",
            "correo": "mlopez@gmail.com",
            "direccion": "Calle 123",
            "telefono": "123-456-789",
            "latitud": 10.1234,
            "longitud": 20.5678
        }
        client = CreateClient(data).execute()

        assert 'id' in client
        assert 'createdAt' in client

        clients = self.session.query(Client).all()
        assert len(clients) == 1
        assert clients[0].nombre == "Maria Lopez"

        # Ensure the mocked function was called
        mock_registrar_usuario.assert_called_once_with(data["correo"], 'cliente')

    def teardown_method(self):
        self.session.close()
        Base.metadata.drop_all(bind=engine)