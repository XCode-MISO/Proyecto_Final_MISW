from .base_command import BaseCommannd
from ..models.client import Client, ClientJsonSchema
from ..session import Session
from ..errors.errors import IncompleteParams
from sqlalchemy import or_

class GetAllClients(BaseCommannd):
    def __init__(self):
        pass

    def execute(self):
        session = Session()
        clients = session.query(Client).all()
        session.close()

        schema = ClientJsonSchema(many=True)
        clients_data = schema.dump(clients)
        
        return clients_data