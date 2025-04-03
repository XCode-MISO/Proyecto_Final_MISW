from src.session import Session, engine
from src.models.model import Base
from src.models.visit import Visit
from src.main import app
from src.commands.create_visit import CreateVisit
from src.commands.create_client import CreateClient
import json
from datetime import datetime, timedelta

class TestVisits():
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
    self.client = CreateClient(self.data).execute()

  def test_create_visit(self):
    with app.test_client() as test_client:
      response = test_client.post(
        '/visits', json={
          "client_id":f"{self.client['id']}",
          "fechaVisita": "2023-10-27T12:00:00",
          "informe": "Informe de visita numero 1",
          "latitud":12.3454,
          "longitud":43.987
        }
      )
      response_json = json.loads(response.data)

      assert response.status_code == 201
      assert 'id' in response_json
      assert 'createdAt' in response_json

  def teardown_method(self):
    self.session.close()
    Base.metadata.drop_all(bind=engine)