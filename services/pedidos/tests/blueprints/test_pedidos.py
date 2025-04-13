# tests/blueprints/test_pedidos.py

import json
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
