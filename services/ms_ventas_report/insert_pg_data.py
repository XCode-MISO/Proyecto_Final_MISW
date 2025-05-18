import sys
import os
from datetime import date, timedelta
from app_simple import create_app
from models.db import db
from models.reporte import ReporteVentas

# Datos de prueba
test_data = [
    {
        "producto": "Smartphone Samsung Galaxy",
        "cantidad": 10,
        "fecha": date.today(),
        "vendedor_id": "vendedor-123"
    },
    {
        "producto": "iPad Pro 12.9",
        "cantidad": 5,
        "fecha": date.today() - timedelta(days=1),
        "vendedor_id": "vendedor-123"
    },
    {
        "producto": "Laptop Dell XPS",
        "cantidad": 3,
        "fecha": date.today() - timedelta(days=2),
        "vendedor_id": "vendedor-456"
    },
    {
        "producto": "AirPods Pro",
        "cantidad": 15,
        "fecha": date.today() - timedelta(days=3),
        "vendedor_id": "vendedor-456"
    }
]

# Crear app y contexto
app = create_app()

with app.app_context():
    try:
        print("Conectando a la base de datos PostgreSQL...")
        
        # Verificar si hay reportes existentes
        existing = ReporteVentas.query.count()
        print(f"Hay {existing} reportes existentes en la base de datos")
        
        # Insertar datos
        for item in test_data:
            reporte = ReporteVentas(**item)
            db.session.add(reporte)
        
        # Guardar cambios
        db.session.commit()
        print(f"✅ Se insertaron {len(test_data)} reportes de prueba en la base de datos")
        
        # Verificar los datos insertados
        reportes = ReporteVentas.query.all()
        print(f"\nReportes totales en la base de datos: {len(reportes)}")
        
        print("\nÚltimos 5 reportes:")
        for r in ReporteVentas.query.order_by(ReporteVentas.id.desc()).limit(5).all():
            print(f"ID: {r.id}, Producto: {r.producto}, Cantidad: {r.cantidad}, Vendedor: {r.vendedor_id}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        db.session.rollback()