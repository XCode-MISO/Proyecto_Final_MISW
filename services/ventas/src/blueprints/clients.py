from flask import Flask, jsonify, request, Blueprint
from ..commands.create_client import CreateClient
from ..commands.get_client import GetClient
from ..commands.get__all_clients import GetAllClients

client_blueprint = Blueprint('clients', __name__)

@client_blueprint.route('/clients', methods=['POST'])
def create():
    client = CreateClient(request.get_json()).execute()
    return jsonify(client), 201

@client_blueprint.route('/clients/<id>', methods=['GET'])
def getClient(id):
    client = GetClient(id).execute()
    return jsonify(client)

@client_blueprint.route('/clients', methods=['GET'])
def getAllClients():
    clients = GetAllClients().execute()
    return jsonify(clients)
