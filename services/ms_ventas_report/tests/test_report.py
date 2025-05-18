import unittest
from unittest.mock import patch, MagicMock, call
import json
from datetime import datetime, date
import sys
import os
import warnings


warnings.filterwarnings("ignore", category=ResourceWarning)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from models.reporte import ReporteVentas
from events.subscriber_pedidos import get_producto_nombre, simular_eventos_pedidos

class TestReporteVentas(unittest.TestCase):
    """Pruebas para el microservicio de reportes de ventas"""
    
    @classmethod
    def setUpClass(cls):
        """Configuración inicial para todas las pruebas"""
        warnings.filterwarnings("ignore", category=ResourceWarning)

    def setUp(self):
        """Crear una nueva aplicación para cada prueba"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        self.client = self.app.test_client()
        
        from models.db import db
        db.create_all()

    def tearDown(self):
        """Limpiar después de cada prueba"""
        from models.db import db
        db.session.remove()
        db.drop_all()
        
        self.app_context.pop()
    
    def test_health_check(self):
        """Prueba del endpoint de salud"""
        response = self.client.get('/')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['status'], 'ok')
        self.assertEqual(data['service'], 'ms_ventas_report')
    
    def test_get_reportes_por_vendedor(self):
        """Prueba de obtención de reportes por vendedor"""
        from models.db import db
        
        reportes = [
            ReporteVentas(
                producto="Producto Test 1",
                cantidad=10,
                fecha=date(2025, 5, 10),
                vendedor_id="vendedor-123"
            ),
            ReporteVentas(
                producto="Producto Test 2",
                cantidad=5,
                fecha=date(2025, 5, 11),
                vendedor_id="vendedor-123"
            ),
            ReporteVentas(
                producto="Producto Test 3",
                cantidad=8,
                fecha=date(2025, 5, 12),
                vendedor_id="vendedor-456"
            )
        ]
        
        for reporte in reportes:
            db.session.add(reporte)
        db.session.commit()
        
        response = self.client.get('/api/reportes/vendedor/vendedor-123')
        
        self.assertEqual(response.status_code, 200)
        
        try:
            data = json.loads(response.data)
            # Verifica que la respuesta tenga dos elementos
            self.assertEqual(len(data), 2)
        except (json.JSONDecodeError, TypeError):

            respuesta_texto = response.data.decode('utf-8')
            self.assertIn("Producto Test 1", respuesta_texto)
            self.assertIn("Producto Test 2", respuesta_texto)
            self.assertNotIn("Producto Test 3", respuesta_texto)
    
    def test_get_reportes_filtrado_por_fecha(self):
        """Prueba de filtrado de reportes por fecha"""
        from models.db import db
        
        reportes = [
            ReporteVentas(
                producto="Producto Filtro 1",
                cantidad=10,
                fecha=date(2025, 5, 10),
                vendedor_id="vendedor-123"
            ),
            ReporteVentas(
                producto="Producto Filtro 2",
                cantidad=5,
                fecha=date(2025, 5, 11),
                vendedor_id="vendedor-123"
            )
        ]
        
        for reporte in reportes:
            db.session.add(reporte)
        db.session.commit()
        

        response = self.client.get('/api/reportes/vendedor/vendedor-123?fecha_inicio=2025-05-11')
        
        self.assertEqual(response.status_code, 200)
        
        respuesta_texto = response.data.decode('utf-8')
        
        self.assertIn("Producto Filtro 2", respuesta_texto)
        
        self.assertNotIn("Producto Filtro 1", respuesta_texto)
    
    def test_get_resumen_por_vendedor(self):
        """Prueba de obtención del resumen por vendedor"""
        from models.db import db
        
        reportes = [
            ReporteVentas(
                producto="Producto Resumen A",
                cantidad=10,
                fecha=date(2025, 5, 10),
                vendedor_id="vendedor-123"
            ),
            ReporteVentas(
                producto="Producto Resumen B",
                cantidad=5,
                fecha=date(2025, 5, 11),
                vendedor_id="vendedor-123"
            ),
            ReporteVentas(
                producto="Producto Resumen A",
                cantidad=8,
                fecha=date(2025, 5, 12),
                vendedor_id="vendedor-123"
            )
        ]
        
        for reporte in reportes:
            db.session.add(reporte)
        db.session.commit()
        
        response = self.client.get('/api/reportes/vendedor/vendedor-123/resumen')
        
        self.assertEqual(response.status_code, 200)
        
        respuesta_texto = response.data.decode('utf-8')
        
        self.assertIn("Producto Resumen A", respuesta_texto)
        self.assertIn("Producto Resumen B", respuesta_texto)
        

        self.assertIn("18", respuesta_texto)  
        self.assertIn("5", respuesta_texto)   
    
    @patch('events.subscriber_pedidos.get_producto_nombre')
    @patch('events.subscriber_pedidos.db.session.add')
    @patch('events.subscriber_pedidos.db.session.commit')
    def test_callback_procesa_mensaje_simple(self, mock_commit, mock_add, mock_get_nombre):
        """Prueba que callback procesa correctamente un mensaje simple de Pub/Sub"""
        mock_get_nombre.return_value = "Producto Mocked 101"
        
        from events.subscriber_pedidos import callback
        
        mock_message = MagicMock()
        mock_message.data = json.dumps({
            "id": "pedido-test-123",
            "productId": "producto-101",
            "quantity": 3,
            "sellerId": "vendedor-789",
            "deliveryDate": "2025-05-18"
        }).encode('utf-8')
        
        callback(mock_message)
        
        mock_get_nombre.assert_called_once_with("producto-101")
        mock_add.assert_called_once()
        mock_commit.assert_called_once()
        mock_message.ack.assert_called_once()
    
    @patch('events.subscriber_pedidos.get_producto_nombre')
    @patch('events.subscriber_pedidos.db.session.add')
    @patch('events.subscriber_pedidos.db.session.commit')
    def test_callback_procesa_mensaje_con_productos(self, mock_commit, mock_add, mock_get_nombre):
        """Prueba que callback procesa correctamente un mensaje con múltiples productos"""
        mock_get_nombre.return_value = "Producto Mocked"
        
        from events.subscriber_pedidos import callback
        
        mock_message = MagicMock()
        mock_message.data = json.dumps({
            "id": "pedido-test-456",
            "products": [
                {"id": 101, "amount": 2},
                {"id": 102, "amount": 1}
            ],
            "deliveryDate": "2025-05-19",
            "vendedor": {"id": "vendedor-555", "name": "Vendedor Test"}
        }).encode('utf-8')
        
        callback(mock_message)
        
        self.assertEqual(mock_get_nombre.call_count, 2)
        self.assertEqual(mock_add.call_count, 2)
        mock_commit.assert_called_once()
        mock_message.ack.assert_called_once()
    
    @patch('requests.get')
    def test_get_producto_nombre(self, mock_get):
        """Prueba la función get_producto_nombre"""
        mock_response = MagicMock()
        mock_response.json.return_value = {"nombre": "Smartphone Test"}
        mock_get.return_value = mock_response
        
        nombre = get_producto_nombre("producto-999")
        
        self.assertEqual(nombre, "Smartphone Test")
        mock_get.assert_called_once()
    
    @patch('events.subscriber_pedidos.db.session.add')
    @patch('events.subscriber_pedidos.db.session.commit')
    def test_simular_eventos_pedidos(self, mock_commit, mock_add):
        """Prueba la función de simulación de eventos"""
        simular_eventos_pedidos()
        
        self.assertEqual(mock_add.call_count, 2) 
        mock_commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()