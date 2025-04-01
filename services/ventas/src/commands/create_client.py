from .base_command import BaseCommannd
from ..models.client import Client, ClientSchema, CreatedClientJsonSchema
from ..session import Session
from ..errors.errors import IncompleteParams
from sqlalchemy import or_

class CreateClient(BaseCommannd):
    def __init__(self, data):
        self.data = data

    def execute(self):
        try:
            posted_client = ClientSchema(
                only=('nombre', 'correo','direccion', 
                      'telefono', 'latitud', 'longitud')
            ).load(self.data)
            client = Client(**posted_client)
            session = Session()

            session.add(client)
            session.commit()

            new_client = CreatedClientJsonSchema().dump(client)
            session.close()

            return new_client
        except TypeError:
            raise IncompleteParams()