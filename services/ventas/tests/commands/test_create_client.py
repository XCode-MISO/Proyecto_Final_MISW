from src.commands.create_client import CreateClient
from src.session import Session, engine
from src.models.model import Base
from src.models.client import Client

class TestCreateClient():

    def setup_method(self):
        Base.metadata.create_all(engine)
        self.session = Session()

    def test_create_client(self):
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

    def teardown_method(self):
        self.session.close()
        Base.metadata.drop_all(bind=engine)