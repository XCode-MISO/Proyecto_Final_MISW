from flask import Blueprint, request, jsonify
from services.producto_service import ProductoService
from models.producto import Producto

producto_bp = Blueprint('producto_bp', __name__)
producto_service = ProductoService()

@producto_bp.route('/fabricante/<int:fabricante_id>', methods=['POST'])
def crear_producto(fabricante_id):
    data = request.get_json() or {}
    nombre = data.get('nombre')
    cantidad = data.get('cantidad')
    precio_compra = data.get('precioCompra')
    moneda = data.get('moneda')
    prod = producto_service.crear_producto(
        fabricante_id=fabricante_id,
        nombre=nombre,
        cantidad=cantidad,
        precio_compra=precio_compra,
        moneda=moneda
    )
    return jsonify({
        "id": prod.id,
        "nombre": prod.nombre,
        "cantidad": prod.cantidad,
        "precioCompra": prod.precio_compra,
        "moneda": prod.moneda,
        "fabricanteId": prod.fabricante_id
    }), 201

@producto_bp.route('/search', methods=['GET'])
def buscar_producto():
    """
    Endpoint para buscar productos por nombre y fabricante.
    Parámetros de consulta:
      - nombre: texto para la búsqueda (usamos ilike para autocompletar)
      - fabricanteId: ID del fabricante (entero)
    """
    nombre = request.args.get('nombre')
    fabricante_id = request.args.get('fabricanteId')
    
    if not nombre or not fabricante_id:
        return jsonify({"error": "Se requieren los parámetros 'nombre' y 'fabricanteId'"}), 400

    try:
        fabricante_id = int(fabricante_id)
    except ValueError:
        return jsonify({"error": "El parámetro 'fabricanteId' debe ser un entero"}), 400

   
    # Buscar productos cuyo nombre contenga el texto (fuzzy search) y que pertenezcan al fabricante
    productos = Producto.query.filter(
        Producto.nombre.ilike(f"%{nombre}%"),
        Producto.fabricante_id == fabricante_id
    ).all()
    
    result = []
    for p in productos:
        result.append({
            "id": p.id,
            "nombre": p.nombre,
            "descripcion": p.descripcion,
            "precioCompra": p.precio_compra,
            "moneda": p.moneda,
            "fabricanteId": p.fabricante_id
        })
    return jsonify(result), 200