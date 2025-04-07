from datetime import datetime, timedelta
from dateutil import parser
from marshmallow import ValidationError
from ..errors.errors import MissingField, DateInvalid, DatePast

class ValidatePedidoFields:
    def __init__(self, data):
        self.data = data
    
    def execute(self):
        try:
            name= self.data['name']
            if not name:
                raise MissingField()
            clientId = self.data['clientId']
            if not clientId:
                raise MissingField()
            products = self.data['products']
            if not products:
                raise MissingField()            
            price = self.data['price']
            if not price:
                raise MissingField()
            deliveryDate_str = self.data['deliveryDate']
            if not deliveryDate_str:
                raise MissingField()            
            if not name or not clientId or not products or not price or not deliveryDate_str:
                raise MissingField()
        except KeyError:
            raise MissingField()
        
        try:
            if not self.valid_deliveryDate():
                raise DatePast()
        except ValueError:
            raise DateInvalid()
        
        return {
            "name": name,
            "clientId": clientId,
            "products": products,
            "price": price,
            "deliveryDate": deliveryDate_str
        }
    
    def valid_deliveryDate(self):
        try:
            deliveryDate = parser.parse(self.data['deliveryDate']).date()
            today = datetime.utcnow().date()
            max_date = today + timedelta(days=2)
            return today <= deliveryDate <= max_date
        except:
            return False