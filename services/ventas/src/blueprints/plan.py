from flask import Flask, jsonify, request, Blueprint
from ..commands.create_plan import CreatePlan
from ..commands.get_plan import GetPlan
from ..commands.get_all_plans import GetAllPlans

plan_blueprint = Blueprint('plan', __name__)

@plan_blueprint.route('/api/plan', methods=['POST'])
def create():
    plan = CreatePlan(request.get_json()).execute()
    return jsonify(plan), 201

@plan_blueprint.route('/api/plan/<id>', methods=['GET'])
def getPlan(id):
    client = GetPlan(id).execute()
    return jsonify(client)

@plan_blueprint.route('/api/plan', methods=['GET'])
def getAllPlans():
    clients = GetAllPlans().execute()
    return jsonify(clients)
