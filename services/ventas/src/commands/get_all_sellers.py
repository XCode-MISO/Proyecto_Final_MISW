from .base_command import BaseCommannd
from ..models.seller import Seller, SellerJsonSchema
from ..session import Session
from ..errors.errors import IncompleteParams
from sqlalchemy import or_

class GetAllSellers(BaseCommannd):
    def __init__(self):
        pass

    def execute(self):
        session = Session()
        sellers = session.query(Seller).all()
        session.close()

        schema = SellerJsonSchema(many=True)
        sellers_data = schema.dump(sellers)
        
        return sellers_data