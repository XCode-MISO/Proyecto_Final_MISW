import pytest
from app import create_app
from models.db import db
from models.producto import Producto
from models.producto_inventario import ProductoInventario

@pytest.fixture
def client():
    # Configuramos la aplicación para pruebas usando SQLite en memoria.
    app = create_app()
    app.config['TESTING'] = True
    # Usamos una base de datos SQLite en memoria para no afectar la real
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
       
        db.create_all()

        # Insertamos dos productos de prueba.
        # Nota: en ms_inventarios no usamos 'fabricante_id'
        prod1 = Producto(producto_id=1, nombre="Producto 1", precio=100.0)
        prod2 = Producto(producto_id=2, nombre="Producto 2", precio=200.0)
        db.session.add_all([prod1, prod2])
        db.session.commit()

        # Insertamos los registros de inventario para cada producto.
        inv1 = ProductoInventario(
            producto_id=prod1.producto_id,
            stock=10,
            bodega="Bodega A",
            estante="Estante 1",
            pasillo="Pasillo X"
        )
        inv2 = ProductoInventario(
            producto_id=prod2.producto_id,
            stock=20,
            bodega="Bodega B",
            estante="Estante 2",
            pasillo="Pasillo Y"
        )
        db.session.add_all([inv1, inv2])
        db.session.commit()

    with app.test_client() as client:
        yield client

def test_listar_productos_pedido(client):
    """
    Prueba el endpoint GET /api/inventarios/pedidos.
    Se espera que se devuelvan 2 registros con los campos:
      - producto_id
      - nombre
      - precio
      - stock
    """
    response = client.get("/api/inventarios/pedidos")
    assert response.status_code == 200, f"Se esperaba 200, se obtuvo {response.status_code}"
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2, f"Se esperaban 2 registros, se obtuvieron {len(data)}"
    for prod in data:
        assert "producto_id" in prod, "Falta 'producto_id'"
        assert "nombre" in prod, "Falta 'nombre'"
        assert "precio" in prod, "Falta 'precio'"
        assert "stock" in prod, "Falta 'stock'"

def test_listar_productos_ubicacion(client):
    """
    Prueba el endpoint GET /api/inventarios/ubicacion.
    Se espera que se devuelvan 2 registros (sólo aquellos productos con inventario)
    con los campos:
      - producto_id
      - nombre
      - bodega
      - cantidad (equivalente a stock)
    """
    response = client.get("/api/inventarios/ubicacion")
    assert response.status_code == 200, f"Se esperaba 200, se obtuvo {response.status_code}"
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) == 2, f"Se esperaban 2 registros, se obtuvieron {len(data)}"
    for item in data:
        assert "producto_id" in item, "Falta 'producto_id'"
        assert "nombre" in item, "Falta 'nombre'"
        assert "bodega" in item, "Falta 'bodega'"
        assert "cantidad" in item, "Falta 'cantidad'"

def test_get_producto_existente(client):
    """
    Prueba el endpoint GET /api/inventarios/<producto_id> para un producto existente.
    Se espera que se retorne el detalle completo del producto con sus datos de inventario.
    """
    response = client.get("/api/inventarios/1")
    assert response.status_code == 200, f"Se esperaba 200, se obtuvo {response.status_code}"
    data = response.get_json()
    assert data["producto_id"] == 1, "El producto_id no coincide"
    assert "nombre" in data, "Falta 'nombre'"
    assert "precio" in data, "Falta 'precio'"
    # Si existe inventario, se deben incluir los siguientes campos.
    assert "stock" in data, "Falta 'stock'"
    assert "bodega" in data, "Falta 'bodega'"
    assert "estante" in data, "Falta 'estante'"
    assert "pasillo" in data, "Falta 'pasillo'"

def test_get_producto_no_existe(client):
    """
    Prueba el endpoint GET /api/inventarios/<producto_id> para un producto inexistente.
    Se espera que retorne 404 y un mensaje de error.
    """
    response = client.get("/api/inventarios/999")
    assert response.status_code == 404, f"Se esperaba 404, se obtuvo {response.status_code}"
    data = response.get_json()
    assert "error" in data, "No se encontró el mensaje de error"