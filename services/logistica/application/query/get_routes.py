from typing import List
from flask import Blueprint, jsonify

from logistica.infrastructure.db.model import Route

query_bp = Blueprint('query', __name__)

@query_bp.route('/api/route', methods=['GET'])
def get_routes():
    routes: List[Route] = Route.query.all()
    return list(map(lambda route: route.toJSON(), routes))


@query_bp.route('/api/route/<string:route_id>', methods=['GET'])
def get_route(route_id):
    route: Route = Route.query.get(route_id)
    if route:
        return route.toJSON()
    else:
        return jsonify({'error': 'Route not found'}), 404
    