import random
import uuid
from datetime import datetime, timedelta
from faker import Faker
from sqlalchemy import exists

from src.database import Session, engine
from src.models.model import Base
from src.models.pedido import Pedido
from src.models.pedido_producto import PedidoProducto

# Crear las tablas si no existen
Base.metadata.create_all(engine)

fake = Faker()
session = Session()

def seed_database_if_empty():
    # Verificar si ya existen pedidos en la base de datos
    has_orders = session.query(exists().where(Pedido.id != None)).scalar()

    if has_orders:
        print("Ya hay pedidos existentes. No se insertará nueva información.")
        session.close()
        return

    print("Insertando datos de prueba...")

    estados = ["Pendiente", "En camino", "Entregado"]

    for _ in range(10):  # 10 pedidos de ejemplo
        # Simular cliente y vendedor
        client_id = str(uuid.uuid4())
        client_name = fake.name()
        vendedor_id = str(uuid.uuid4())
        vendedor_name = fake.name()

        # Simular entre 1 y 5 productos
        productos = []
        total_price = 0.0
        for _ in range(random.randint(1, 5)):
            product_id = random.randint(1, 100)
            precio = round(random.uniform(5.0, 100.0), 2)
            cantidad = random.randint(1, 10)
            total_price += precio * cantidad

            # Crear el producto
            producto = PedidoProducto(
                productId=product_id,
                amount=cantidad
            )
            productos.append(producto)

        # Crear el pedido
        pedido = Pedido(
            name=f"Pedido #{random.randint(1, 1000)}",
            clientId=client_id,
            clientName=client_name,
            vendedorId=vendedor_id,
            vendedorName=vendedor_name,
            price=round(total_price, 2),
            state=random.choice(estados),
            deliveryDate=(datetime.utcnow() + timedelta(days=random.randint(0, 2))).date()
        )

        # Asociar productos al pedido
        for producto in productos:
            producto.pedido = pedido  # Aseguramos que cada producto tenga la referencia correcta al pedido

        session.add(pedido)

    session.commit()
    session.close()
    print("Datos de prueba insertados correctamente.")

# Ejecutar el seeding
if __name__ == "__main__":
    seed_database_if_empty()
