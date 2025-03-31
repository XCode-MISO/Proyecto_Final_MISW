from .base_command import BaseCommannd
from ..models.pedido import Pedido, PedidoSchema, PedidoJsonSchema
from marshmallow import ValidationError
from src.models.producto import Producto
from src.database import db

class CreatePedido(BaseCommannd):
    def __init__(self, data):
        self.data = data

    def execute(self):
        print("DEBUG: Entrando en execute()",self.data)
        # Validar los datos del pedido con el esquema
        try:
            print("DEBUG: Antes de productos_objetos",self.data)
            product_ids = self.data.get("products", [])
            print("DEBUG: Antes de product_ids",product_ids)
            # Validar que product_ids no esté vacío
            if not product_ids:
                raise ValueError("No se han proporcionado IDs de productos.")
            print ("DEBUG: db.session", db.session)
            print("DEBUG: Database URL =", db.engine.url)
            productos_objetos = db.session.query(Producto).filter(Producto.id.in_(product_ids)).all()            
            print("DEBUG: Despues de productos_objetos =", productos_objetos)
            # Validar que todos los productos existan en la base de datos
            productos_encontrados = {producto.id for producto in productos_objetos}
            print("DEBUG: Despues de productos_encontrados =",productos_encontrados)
        except ValidationError as err:
            return {"error crear pedido": str(err)}, 500 
        schema = PedidoSchema()
        try:
            validated_data = schema.load(self.data)
        except ValidationError as err:
            return {"error": err.messages}, 400 
        
        # Crear instancia del pedido
        nuevo_pedido = Pedido(
            name=validated_data["name"],
            clientId=validated_data["clientId"], 
            products=productos_objetos, 
            price=validated_data["price"],
            delivery_date=validated_data["deliveryDate"]  
        )
        print("DEBUG: nuevo_pedido =", nuevo_pedido)

        # Guardar en la base de datos
        session = db.session()
        session.add(nuevo_pedido)
        session.commit()
        session.refresh(nuevo_pedido)  # Importante para actualizar los valores generados

        # Serializar y devolver el pedido creado
        pedido_json = PedidoJsonSchema().dump(nuevo_pedido)
        session.close()
        return pedido_json
