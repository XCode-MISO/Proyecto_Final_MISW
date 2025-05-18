from app_simple import create_app
from models.db import db
from models.reporte import ReporteVentas
from datetime import date, timedelta

# Datos de prueba
test_data = [
    {
        "producto": "Producto Test 1",
        "cantidad": 10,
        "fecha": date.today(),
        "vendedor_id": "vendedor-123"
    },
    {
        "producto": "Producto Test 2",
        "cantidad": 5,
        "fecha": date.today() - timedelta(days=1),
        "vendedor_id": "vendedor-123"
    },
    {
        "producto": "Producto Test 3",
        "cantidad": 8,
        "fecha": date.today() - timedelta(days=2),
        "vendedor_id": "vendedor-456"
    }
]

# Crear app y contexto
app = create_app()

with app.app_context():
    # Insertar datos
    for item in test_data:
        reporte = ReporteVentas(**item)
        db.session.add(reporte)
    
    # Guardar cambios
    db.session.commit()
    print(f"✅ Se insertaron {len(test_data)} registros de prueba en la base de datos")
