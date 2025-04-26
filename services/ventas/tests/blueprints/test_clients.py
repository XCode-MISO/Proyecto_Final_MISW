from src.session import Session, engine
from src.models.model import Base
from src.models.client import Client
from src.main import app
import json
from unittest.mock import patch

class TestClients():
    def setup_method(self):
        Base.metadata.create_all(engine)
        self.session = Session()

    @patch('src.commands.create_client.registrarUsuarioEnFirebase', return_value="test_client")
    def test_create_client(self, mock_registrar_usuario):
        with app.test_client() as test_client:
            response = test_client.post(
                '/api/clients', json={
                    "nombre": "Maria Lopez",
                    "correo": "mlopez@gmail.com",
                    "direccion": "Calle 123",
                    "telefono": "123-456-789",
                    "latitud": 10.1234,
                    "longitud": 20.5678
                }
            )
            response_json = json.loads(response.data)

            assert response.status_code == 201
            assert 'id' in response_json
            assert 'createdAt' in response_json

            # Ensure the mocked function was called
            mock_registrar_usuario.assert_called_once_with("mlopez@gmail.com", "cliente")

    def teardown_method(self):
        self.session.close()
        Base.metadata.drop_all(bind=engine)