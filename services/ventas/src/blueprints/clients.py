import json
import os
from flask import Flask, jsonify, request, Blueprint
from ..commands.create_client import CreateClient
from ..commands.get_client import GetClient
from ..commands.get__all_clients import GetAllClients

client_blueprint = Blueprint('clients', __name__)

@client_blueprint.route('/api/clients', methods=['POST'])
def create():
    client = CreateClient(request.get_json()).execute()
    return jsonify(client), 201

@client_blueprint.route('/api/clients/<id>', methods=['GET'])
def getClient(id):
    client = GetClient(id).execute()
    return jsonify(client)

@client_blueprint.route('/api/clients', methods=['GET'])
def getAllClients():
    clients = GetAllClients().execute()
    return jsonify(clients)

@client_blueprint.route("/")
def root_path():
    return "<p>Servicio de Ventas</p>"

@client_blueprint.route("/info")
def info_path():
    try:
        return json.load(open(os.path.join("version.json"), "r"))
    except Exception as e:
        print(str(e))
        return "No version.json, this means this deployment was manual or there is an error."

@client_blueprint.route("/health")
def health_check():
    return "Ok"