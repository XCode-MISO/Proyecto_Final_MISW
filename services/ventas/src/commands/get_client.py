from .base_command import BaseCommannd
from ..models.client import Client, ClientJsonSchema
from ..session import Session
from ..errors.errors import IncompleteParams
from sqlalchemy import or_

class GetClient(BaseCommannd):
    def __init__(self, id):
        self.id = id

    def execute(self):
        session = Session()
        client = session.query(Client).filter(Client.id == self.id).one()
        session.close()

        schema = ClientJsonSchema()
        client = schema.dump(client)
        session.close()

        return client