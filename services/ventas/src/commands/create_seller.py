from ..commands.util import registrarUsuarioEnFirebase
from .base_command import BaseCommannd
from ..models.seller import Seller, SellerSchema, CreatedSellerJsonSchema
from ..session import Session
from ..errors.errors import CodigoNoGenerado, IncompleteParams
from sqlalchemy import or_

class CreateSeller(BaseCommannd):
    def __init__(self, data):
        self.data = data

    def execute(self):
        try:
            posted_seller = SellerSchema(
                only=('nombre', 'correo','direccion', 
                      'telefono', 'latitud', 'longitud', 'imagen')
            ).load(self.data)
            seller = Seller(**posted_seller)

            firebse_uuid = registrarUsuarioEnFirebase(seller.correo, "vendedor", seller.nombre)  
            if firebse_uuid is None:
                raise CodigoNoGenerado()
            
            session = Session()

            session.add(seller)
            session.commit()

            new_seller = CreatedSellerJsonSchema().dump(seller)
            session.close()

            return new_seller
        except TypeError:
            raise IncompleteParams()