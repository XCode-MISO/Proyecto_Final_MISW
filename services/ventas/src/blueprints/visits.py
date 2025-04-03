from flask import Flask, jsonify, request, Blueprint
from ..commands.create_visit import CreateVisit
from ..commands.get_all_visits import GetAllVisits

visit_blueprint = Blueprint('visits', __name__)

@visit_blueprint.route('/visits', methods=['POST'])
def create():
    visit = CreateVisit(request.get_json()).execute()
    return jsonify(visit), 201


@visit_blueprint.route('/visits', methods=['GET'])
def getAllClients():
    visits = GetAllVisits().execute()
    return jsonify(visits)
