import random
import uuid
from datetime import datetime, timedelta
from faker import Faker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exists

from src.database import Session, engine  # <- Usa tu engine y Session definidos
from src.models.model import Base
from src.models.producto import Producto
from src.models.pedido import Pedido

# Crea las tablas (si no existen)
Base.metadata.create_all(engine)

fake = Faker()
session = Session()

def seed_database_if_empty():
    states = ["Pendiente", "En camino", "Entregado"]
    # Validar si ya hay datos
    has_clients = session.query(exists().where(Cliente.id != None)).scalar()
    has_products = session.query(exists().where(Producto.id != None)).scalar()
    has_orders = session.query(exists().where(Pedido.id != None)).scalar()

    if has_clients or has_products or has_orders:
        print("Datos ya existentes. No se insertará nueva información.")
    else:
        print("Insertando datos de prueba...")

        # Crear 10 clientes
        clientes = [Cliente(name=fake.name()) for _ in range(5)]
        session.add_all(clientes)
        session.commit()

        # Crear 20 productos
        productos = [
            Producto(
                name=fake.word().capitalize(),
                price=round(random.uniform(5.0, 100.0), 2),
                amount=random.randint(1, 100)
            )
            for _ in range(5)
        ]
        session.add_all(productos)
        session.commit()

        # Crear 50 pedidos con productos
        for _ in range(5):
            client = random.choice(clientes)
            selected_products = random.sample(productos, k=random.randint(1, 5))
            total_price = sum(p.price for p in selected_products)
            deliveryDate = datetime.utcnow() + timedelta(days=random.randint(2, 10))

            pedido = Pedido(
                name=f"Pedido #{random.randint(1, 1000)}",
                clientId=client.id,
                products=selected_products,
                price=total_price,
                state=random.choice(states),
                deliveryDate=deliveryDate
            )
            session.add(pedido)

        session.commit()
        print("✅ 50 pedidos creados exitosamente.")

    session.close()
