from unittest.mock import patch
from src.session import Session, engine
from src.models.model import Base
from src.main import app
import json

class TestSellers():
    def setup_method(self):
        Base.metadata.create_all(engine)
        self.session = Session()

    @patch('src.commands.create_seller.registrarUsuarioEnFirebase', return_value="seller_1")
    def test_create_client(self, mock_registrar_usuario):
        with app.test_client() as test_client:
            response = test_client.post(
                '/api/vendedores', json={
                    "nombre": "Maria Lopez",
                    "correo": "mlopez@gmail.com",
                    "direccion": "Calle 123",
                    "telefono": "123-456-789",
                    "latitud": 10.1234,
                    "longitud": 20.5678,
                    "imagen": "<img>"
                }
            )
            response_json = json.loads(response.data)

            assert response.status_code == 201
            assert 'id' in response_json
            assert 'createdAt' in response_json
            mock_registrar_usuario.assert_called_once_with(data["correo"], 'seller_1')

    def teardown_method(self):
        self.session.close()
        Base.metadata.drop_all(bind=engine)