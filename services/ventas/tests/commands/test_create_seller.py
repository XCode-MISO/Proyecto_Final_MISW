from src.commands.create_seller import CreateSeller
from src.session import Session, engine
from src.models.model import Base
from src.models.seller import Seller
from unittest.mock import patch

class TestCreateSeller():

    def setup_method(self):
        Base.metadata.create_all(engine)
        self.session = Session()

    @patch('src.commands.create_client.registrarUsuarioEnFirebase', return_value="seller_1")
    def test_create_seller(self, mock_registrar_usuario):
        data = {
            "nombre": "Maria Lopez",
            "correo": "mlopez@gmail.com",
            "direccion": "Calle 123",
            "telefono": "123-456-789",
            "latitud": 10.1234,
            "longitud": 20.5678,
            "imagen": "<url>"
        }
        seller = CreateSeller(data).execute()

        assert 'id' in seller
        assert 'createdAt' in seller

        sellers = self.session.query(Seller).all()
        assert len(sellers) == 1
        assert sellers[0].nombre == "Maria Lopez"

        # Ensure the mocked function was called
        mock_registrar_usuario.assert_called_once_with(data["correo"], 'vendedor')

    def teardown_method(self):
        self.session.close()
        Base.metadata.drop_all(bind=engine)