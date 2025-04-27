## src\blueprints\pedidos.py
import json
from flask import Flask, jsonify, request, Blueprint
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import uuid
from datetime import datetime, timezone

from src.commands.get_pedido import GetPedido


from ..commands.fields_pedido import ValidatePedidoFields
from ..commands.create_pedido import CreatePedido
from ..commands.get_pedidos import GetPedidos
from ..models.pedido import Pedido

import os



operations_blueprint = Blueprint('operations', __name__)

## Crear Pedido
@operations_blueprint.route('/create_pedido', methods=['POST'])
def pedidos():
    ##auth_header = request.headers.get('Authorization')
    ##user_id = ValidateToken(auth_header).execute()
    data = request.get_json()
    print("DEBUG: data =", data) 
    dataPedido=ValidatePedidoFields(data).execute()
    print("DEBUG: dataPedido =", dataPedido) 
    newPedido = CreatePedido(dataPedido).execute()
    print("DEBUG: new_pedido =", newPedido) 


    
    if isinstance(newPedido, tuple) and len(newPedido) == 2 and isinstance(newPedido[0], dict):
        return jsonify(newPedido[0]), newPedido[1]

    return jsonify(newPedido), 201



## Obtener Pedidos
@operations_blueprint.route('/pedidos', methods=['GET'])
def get_pedidos():
    ##auth_header = request.headers.get('Authorization')
    ##user_id = ValidateToken(auth_header).execute()
    ##data=request.args.to_dict()
    
    client_id = request.args.get('clientid') 
    result = GetPedidos(client_id).execute()
    return jsonify(result), 200



## Obtener Pedidos
@operations_blueprint.route('/pedido/<id>', methods=['GET'])
def get_pedido(id):
    ##auth_header = request.headers.get('Authorization')
    ##user_id = ValidateToken(auth_header).execute()
    ##data=request.args.to_dict()
    result = GetPedido(id).execute()
    return jsonify(result), 200

@operations_blueprint.route("/info")
def info_path():
    try:
        return json.load(open(os.path.join("version.json"), "r"))
    except Exception as e:
        print(str(e))
        return "No version.json, this means this deployment was manual or there is an error."
