# ms_compras/apis/producto_api.py

from flask import Blueprint, request, jsonify
from services.producto_service import ProductoService

producto_bp = Blueprint('producto_bp', __name__)
producto_service = ProductoService()

@producto_bp.route('/fabricante/<int:fabricante_id>', methods=['POST'])
def crear_producto(fabricante_id):
    data = request.get_json() or {}
    nombre        = data.get('nombre')
    descripcion   = data.get('descripcion')
    precio_compra = data.get('precioCompra')
    moneda        = data.get('moneda')

    prod = producto_service.crear_producto(
        fabricante_id=fabricante_id,
        nombre=nombre,
        descripcion=descripcion,
        precio_compra=precio_compra,
        moneda=moneda
    )
    return jsonify({
        "id":           prod.id,
        "nombre":       prod.nombre,
        "descripcion":  prod.descripcion,
        "precioCompra": prod.precio_compra,
        "moneda":       prod.moneda,
        "fabricanteId": prod.fabricante_id
    }), 201