import traceback
from flask import Blueprint, Response, request, jsonify

from logistica.application.services.generate_route import generate_route as generate_route_service, update_route as update_route_service, add_stop_route as add_stop_route_service
from logistica.domain.model import Route
from logistica.infrastructure.db.model import Route as RouteDB

comandos_bp = Blueprint('comandos', __name__)

@comandos_bp.route('/generate-route', methods=['POST'])
def generate_route():
  try:
    body = request.json
    if 'paradas' not in body:
      return jsonify({'error': 'No se proporciono ninguna lista de paradas'}), 403

    route: Route = generate_route_service(body)

    return route.toJSON()
    
  except MyException as e: 
     return e.as_http_error()
  

@comandos_bp.route('/update-route', methods=['PUT'])
def update_route():
  
  try:
    body = request.json
    if 'id' not in body:
      return jsonify({'error': 'ningún id de ruta'}), 403

    route: Route = update_route_service(body)

    return route.toJSON()
    
  except MyException as e: 
     return e.as_http_error()

class MyException(Exception):
    """ Binds optional status code and encapsulates returing Response when error is caught """
    def __init__(self, *args, **kwargs):
        code = kwargs.pop('code', 400)
        Exception.__init__(self)
        self.code = code

    def as_http_error(self):
        return Response(str(self), self.code)
    
    
@comandos_bp.route('/add-stop-route', methods=['POST'])
def add_stop_route():
  
  try:
    body = request.json
    if 'id' not in body:
      return jsonify({'error': 'ningún id de ruta'}), 403

    route: Route = add_stop_route_service(body.get("id"), body.get("parada"))

    return route.toJSON()
    
  except MyException as e: 
     return e.as_http_error()

class MyException(Exception):
    """ Binds optional status code and encapsulates returing Response when error is caught """
    def __init__(self, *args, **kwargs):
        code = kwargs.pop('code', 400)
        Exception.__init__(self)
        self.code = code

    def as_http_error(self):
        return Response(str(self), self.code)