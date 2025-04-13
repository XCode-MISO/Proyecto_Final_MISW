from flask import Flask, jsonify, request, Blueprint
from ..commands.create_seller import CreateSeller
from ..commands.get_seller import GetSeller
from ..commands.get_all_sellers import GetAllSellers

seller_blueprint = Blueprint('vendedores', __name__)

@seller_blueprint.route('/api/vendedores', methods=['POST'])
def create():
    seller = CreateSeller(request.get_json()).execute()
    return jsonify(seller), 201

@seller_blueprint.route('/api/vendedores/<id>', methods=['GET'])
def getSeller(id):
    client = GetSeller(id).execute()
    return jsonify(client)

@seller_blueprint.route('/api/vendedores', methods=['GET'])
def getAllSellers():
    clients = GetAllSellers().execute()
    return jsonify(clients)
