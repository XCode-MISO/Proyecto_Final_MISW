from unittest.mock import patch
from src.commands.get_all_sellers import GetAllSellers
from src.commands.create_seller import CreateSeller
from src.session import Session, engine
from src.models.model import Base
from src.models.seller import Seller

class TestGetAllSellers():

    def setup_method(self):
        Base.metadata.create_all(engine)
        self.session = Session()

        # Create sample sellers
        self.seller_data_1 = {
            "nombre": "Carlos Gomez",
            "correo": "cgomez@gmail.com",
            "direccion": "Avenida Siempre Viva 123",
            "telefono": "111-222-333",
            "latitud": 15.6789,
            "longitud": 25.9876,
            "imagen": "<url>"
        }
        self.seller_data_2 = {
            "nombre": "Ana Torres",
            "correo": "atorres@gmail.com",
            "direccion": "Calle Falsa 456",
            "telefono": "444-555-666",
            "latitud": 12.3456,
            "longitud": 34.5678,
            "imagen": "<url>"
        }
        with patch('src.commands.create_seller.registrarUsuarioEnFirebase', return_value="vendedor_1"):
            CreateSeller(self.seller_data_1).execute()
        with patch('src.commands.create_seller.registrarUsuarioEnFirebase', return_value="vendedor_2"):
            CreateSeller(self.seller_data_2).execute()

    def test_get_all_sellers(self):
        sellers = GetAllSellers().execute()

        assert len(sellers) == 2
        assert sellers[0]['nombre'] == "Carlos Gomez"
        assert sellers[1]['nombre'] == "Ana Torres"

    def teardown_method(self):
        self.session.close()
        Base.metadata.drop_all(bind=engine)