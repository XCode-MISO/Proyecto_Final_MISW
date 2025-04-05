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
        # Insertar un fabricante y algunos productos para probar la búsqueda
        from models.fabricante import Fabricante
        from models.producto import Producto
        fab = Fabricante(nombre="Test Fabricante", correo="test@fab.com", telefono="1234567", empresa="Test Inc")
        db.session.add(fab)
        db.session.commit()
        
        # Crear productos
        prod1 = Producto(nombre="Laptop Pro", descripcion="Laptop de alta gama", precio_compra=1500, moneda="USD", fabricante_id=fab.id)
        prod2 = Producto(nombre="Laptop Air", descripcion="Laptop ligera", precio_compra=1200, moneda="USD", fabricante_id=fab.id)
        prod3 = Producto(nombre="Smartphone X", descripcion="Teléfono inteligente", precio_compra=800, moneda="USD", fabricante_id=fab.id)
        db.session.add_all([prod1, prod2, prod3])
        db.session.commit()
    with app.test_client() as client:
        yield client

def test_buscar_producto_exitoso(client):
    # Buscar productos que contengan "Laptop" para el fabricante con ID 1
    response = client.get("/api/productos/search?nombre=Laptop&fabricanteId=1")
    assert response.status_code == 200
    data = response.get_json()
    # Debería devolver dos resultados (Laptop Pro y Laptop Air)
    assert isinstance(data, list)
    assert len(data) == 2
    for prod in data:
        assert "Laptop" in prod["nombre"]

def test_buscar_producto_falta_parametro(client):
    # Falta el parámetro fabricanteId
    response = client.get("/api/productos/search?nombre=Laptop")
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data