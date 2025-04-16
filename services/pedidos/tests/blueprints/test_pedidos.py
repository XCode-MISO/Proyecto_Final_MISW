# tests/blueprints/test_pedidos.py

import json
import pytest
from unittest.mock import patch
from src.main import app
from src.models.model import  Base
from src.database import Session, engine
from datetime import datetime, timedelta

class TestPedidos:
    def setup_method(self):
        Base.metadata.create_all(bind=engine)
        self.session = Session()

    def teardown_method(self):
        self.session.close()
        Base.metadata.drop_all(bind=engine)

    def test_create_pedido_success_mock(self):
        fecha_hoy_plus_2 = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
        mock_result = {
            "name": "Pedido Test",
            "client": {
                "id": "123",
                "name": "Cliente Test"
            },
            "vendedor": {
                "id": "456",
                "name": "Vendedor Test"
            },
            "products": [
                {"id": "prod1", "amount": 2}
            ],
            "price": 100.0,
            "deliveryDate": fecha_hoy_plus_2
        }

        with patch('src.commands.create_pedido.CreatePedido.execute') as mock_execute:
            mock_execute.return_value = mock_result

            with app.test_client() as client:
                response = client.post('/create_pedido', json={
                    "name": "Pedido Test",
                    "clientId": "123",
                    "clientName": "Cliente Test",
                    "vendedorId": "456",
                    "vendedorName": "Vendedor Test",
                    "products": [{"id": "prod1", "amount": 2}],
                    "price": 100.0,
                    "deliveryDate": fecha_hoy_plus_2
                })

                assert response.status_code == 201
                data = response.get_json()
                assert data["client"]["name"] == "Cliente Test"
                assert data["vendedor"]["id"] == "456"
                assert data["price"] == 100.0

    def test_create_pedido_validation_error_mock(self):
        mock_result = ({"error": {"name": ["Missing field"]}}, 400)

        with patch('src.commands.create_pedido.CreatePedido.execute') as mock_execute:
            mock_execute.return_value = mock_result

            with app.test_client() as client:
                response = client.post('/create_pedido', json={})  # vacío para provocar error

                assert response.status_code == 400
                data = response.get_json()
                assert "msg" in data  # Cambié 'error' por 'msg' según la respuesta
                assert data["msg"] == "Faltan campos requeridos."

    def test_create_pedido_error(self):
        with patch('src.commands.create_pedido.CreatePedido.execute') as mock_execute:
            mock_execute.return_value = ({"error": "Validation failed"}, 400)

            with app.test_client() as client:
                res = client.post('/create_pedido', json={})
                assert res.status_code == 400
                data = res.get_json()
                assert "msg" in data
                assert data["msg"] == "Faltan campos requeridos."


    def test_get_all_pedidos(self):
        # Primero crea un pedido (básico, directo a la DB sin mocks)
        pedido = {
            "name": "Pedido de prueba",
            "clientId": "cli-1",
            "clientName": "Cliente Uno",
            "vendedorId": "ven-1",
            "vendedorName": "Vendedor Uno",
            "price": 50.0,
            "deliveryDate": datetime.now().strftime("%Y-%m-%d"),
            "state": "Pendiente"
        }

        from src.models.pedido import Pedido
        self.session.add(Pedido(**pedido))
        self.session.commit()

        with app.test_client() as client:
            response = client.get('/pedidos')
            assert response.status_code == 200
            data = response.get_json()
            assert isinstance(data, list)

    def test_get_pedido_by_id(self):
        pedido = {
            "name": "Pedido individual",
            "clientId": "cli-2",
            "clientName": "Cliente Dos",
            "vendedorId": "ven-2",
            "vendedorName": "Vendedor Dos",
            "price": 75.0,
            "deliveryDate": datetime.now().strftime("%Y-%m-%d"),
            "state": "Pendiente"
        }

        from src.models.pedido import Pedido
        # Add and commit the pedido to the database
        self.session.add(Pedido(**pedido))
        self.session.commit()

        # Now retrieve the 'id' of the newly inserted pedido
        added_pedido = self.session.query(Pedido).filter_by(name=pedido["name"]).first()

        with app.test_client() as client:
            # Use the 'id' of the added pedido in the URL
            response = client.get(f'/pedido/{added_pedido.id}')
            assert response.status_code == 200
            data = response.get_json()
            assert data["client"]["name"] == "Cliente Dos"
            assert data["vendedor"]["name"] == "Vendedor Dos"
            assert data["state"] == "Pendiente"

    