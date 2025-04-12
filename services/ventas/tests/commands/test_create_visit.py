from src.commands.create_visit import CreateVisit
from src.commands.create_client import CreateClient
from src.session import Session, engine
from src.models.model import Base
from src.models.client import Client
from src.models.visit import Visit
from unittest.mock import patch

class TestCreateVisit():

  def setup_method(self):
    Base.metadata.create_all(engine)
    self.session = Session()
    
    self.data = {
      "nombre":"Juan Perez",
      "correo": "jperez@gmail.com",
      "direccion": "Recoleta 211",
      "telefono": "999-000-111",
      "latitud":12.3454,
      "longitud":43.987
    }
    with patch('src.commands.create_client.registrarUsuarioEnFirebase', return_value="xxxxxxxxxxxxxx"):
        self.client = CreateClient(self.data).execute()

  def test_create_visit(self):
    data = {
      "client_id":self.client['id'],
      "fechaVisita": "2023-10-27T12:00:00",
      "informe": "Informe de visita numero 1",
      "latitud":12.3454,
      "longitud":43.987
    }
    visit = CreateVisit(data).execute()

    assert 'id' in visit
    assert 'createdAt' in visit

    visits = self.session.query(Visit).all()
    assert len(visits) == 1

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)