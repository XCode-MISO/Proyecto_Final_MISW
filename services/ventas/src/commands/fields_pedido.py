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
            delivery_date_str = self.data['deliveryDate']
            if not delivery_date_str:
                raise MissingField()            
            if not name or not clientId or not products or not price or not delivery_date_str:
                raise MissingField()
        except KeyError:
            raise MissingField()
        
        try:
            if not self.valid_delivery_date():
                raise DatePast()
        except ValueError:
            raise DateInvalid()
        
        return {
            "name": name,
            "clientId": clientId,
            "products": products,
            "price": price,
            "deliveryDate": delivery_date_str
        }
    
    def valid_delivery_date(self):
        try:
            delivery_date = parser.parse(self.data['deliveryDate']).date()
            min_date = datetime.utcnow().date() + timedelta(days=2)
            return delivery_date >= min_date
        except:
            return False