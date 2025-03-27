import traceback
from flask import Blueprint, request, jsonify

from logistica.application.services.generate_route import generate_route as generate_route_service

comandos_bp = Blueprint('comandos', __name__)

@comandos_bp.route('/generate-route', methods=['POST'])
def generate_route():
  default_route = Route(
      route_id="default_route",
      nombreRuta="default",
      distancia=0,
      tiempoEstimado=0,
      pedidos = []
    )
  try:
    body = request.json
    if 'pedidos' not in body:
      return jsonify({'error': 'No se proporciono ninguna lista de pedidos'})
    pedidos= body.get('pedidos')
    if len(pedidos) < 2:
      return jsonify({'error': f'No se puede generar una ruta para una lista de pedidos menor a dos', 'len': len(pedidos)})
    
    def route(pedido):
      return pedido.get("cliente").get("direccion")
      
    listOfPoints = list(map(route, pedidos))

    route = generate_route_service(listOfPoints, pedidos)

    return route.toJSON()
    
  except Exception as e: 
    print(traceback.format_exc())
    return default_route.toJSON(), 400