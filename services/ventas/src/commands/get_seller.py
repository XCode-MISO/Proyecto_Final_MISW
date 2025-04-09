from .base_command import BaseCommannd
from ..models.seller import Seller, SellerJsonSchema
from ..session import Session
from ..errors.errors import IncompleteParams
from sqlalchemy import or_

class GetSeller(BaseCommannd):
    def __init__(self, id):
        self.id = id

    def execute(self):
        session = Session()
        seller = session.query(Seller).filter(Seller.id == self.id).one()
        session.close()

        schema = SellerJsonSchema()
        seller = schema.dump(seller)
        session.close()

        return seller