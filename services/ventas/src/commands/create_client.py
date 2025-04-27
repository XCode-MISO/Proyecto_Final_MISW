from .base_command import BaseCommannd
from ..models.client import Client, ClientSchema, CreatedClientJsonSchema
from ..session import Session
from ..errors.errors import IncompleteParams, CodigoNoGenerado
from sqlalchemy import or_
from .util import registrarUsuarioEnFirebase

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

            firebse_uuid = registrarUsuarioEnFirebase(client.correo, "cliente", client.nombre)  
            if firebse_uuid is None:
                raise CodigoNoGenerado()

            client.id = firebse_uuid
            session = Session()

            session.add(client)
            session.commit()

            new_client = CreatedClientJsonSchema().dump(client)
            session.close()

            return new_client
        except TypeError:
            raise IncompleteParams()