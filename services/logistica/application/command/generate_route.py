import datetime
import traceback
from flask import Blueprint, request, jsonify

from logistica.application.services.generate_route import generate_route as generate_route_service, update_route
from logistica.domain.model import Route

comandos_bp = Blueprint('comandos', __name__)

@comandos_bp.route('/generate-route', methods=['POST'])
def generate_route():
  default_route = Route(
      route_id="default_route",
      nombreRuta="default",
      distancia=0,
      tiempoEstimado=0,
      pedidos = [],
      mapsResponse= "",
      fecha=datetime.datetime.now().isoformat()
    )
  try:
    body = request.json
    if 'paradas' not in body:
      return jsonify({'error': 'No se proporciono ninguna lista de paradas'}), 403
    paradas= body.get('paradas')
    if len(paradas) < 2:
      return jsonify({'error': f'No se puede generar una ruta para una lista de paradas menor a dos', 'len': len(paradas)}), 403

    route: Route = generate_route_service(body)

    return route.toJSON()
    
  except Exception as e: 
    print(traceback.format_exc())
    return default_route.toJSON(), 400
  

@comandos_bp.route('/update-route', methods=['PUT'])
def update_route():
  default_route = Route(
      route_id="default_route",
      nombreRuta="default",
      distancia=0,
      tiempoEstimado=0,
      pedidos = [],
      mapsResponse= ""
    )
  try:
    body = request.json
    if 'paradas' not in body:
      return jsonify({'error': 'No se proporciono ninguna lista de paradas'}), 403
    paradas= body.get('paradas')
    if len(paradas) < 2:
      return jsonify({'error': f'No se puede generar una ruta para una lista de paradas menor a dos', 'len': len(paradas)}), 403

    route: Route = update_route(body)

    return route.toJSON()
    
  except Exception as e: 
    print(traceback.format_exc())
    return default_route.toJSON(), 400