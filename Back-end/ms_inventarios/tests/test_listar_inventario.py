import pytest
from app import create_app
from models.db import db

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    # Usamos SQLite en memoria para pruebas
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        from models.producto import Producto
        from models.producto_inventario import ProductoInventario
        prod1 = Producto(producto_id=1, nombre="Laptop Pro", precio=1500, fabricante_id=1)
        prod2 = Producto(producto_id=2, nombre="Laptop Air", precio=1200, fabricante_id=1)
        db.session.add_all([prod1, prod2])
        db.session.commit()
        # Insertar datos en productos_inventario
        inv1 = ProductoInventario(producto_id=1, stock=5)
        inv2 = ProductoInventario(producto_id=2, stock=3)
        db.session.add_all([inv1, inv2])
        db.session.commit()
    with app.test_client() as client:
        yield client

def test_listar_productos_inventario(client):
    response = client.get("/api/inventarios/productos")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    # Se deben devolver 2 productos
    assert len(data) == 2
    for prod in data:
        assert "producto_id" in prod
        assert "nombre" in prod
        assert "precio" in prod
        assert "stock" in prod