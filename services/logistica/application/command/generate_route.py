from functools import reduce
from flask import Blueprint, request, jsonify
import more_itertools

from logistica.infrastructure.db.model import Route
from logistica.infrastructure.maps.maps import getRouteFromListOfRoutes

comandos_bp = Blueprint('comandos', __name__)

@comandos_bp.route('/generate-route', methods=['POST'])
def generate_route():
  default_route = Route(
      route_id="default_route",
      nombreRuta="default",
      distancia=0,
      tiempoEstimado=0
    )
  try:
    body = request.json
    if 'pedidos' not in body:
      return jsonify({'error': 'No se proporciono ninguna lista de pedidos'})
    pedidos= body.get('pedidos')
    if len(pedidos) < 2:
      return jsonify({'error': f'No se puede generar una ruta para una lista de pedidos menor a dos', 'len': len(pedidos)})
    
    def route(pedidosPair):
      return pedidosPair.get("cliente").get("direccion")
      
    listOfPoints = list(map(route, pedidos))
    calculatedRoute = getRouteFromListOfRoutes(listOfPoints)
    return jsonify(calculatedRoute)
    
  except Exception as e: 
    print(e)
    return e, 400