#./blueprints/pedidos.py
from flask import Flask, jsonify, request, Blueprint
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import uuid
from datetime import datetime, timezone

from src.commands.get_productos import GetProductos

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

    return jsonify({ 
        "clientId": newPedido['clientId'],
        "products": newPedido['products'],
        "price": newPedido['price'],
    }), 201

## Obtener Pedidos
@operations_blueprint.route('/pedidos', methods=['GET'])
def get_pedidos():
    ##auth_header = request.headers.get('Authorization')
    ##user_id = ValidateToken(auth_header).execute()
    ##data=request.args.to_dict()
    result = request.args.to_dict()
    result = GetPedidos().execute()
    return jsonify(result), 200

## Obtener productos
@operations_blueprint.route('/productos', methods=['GET'])
def get_productos():
    ##auth_header = request.headers.get('Authorization')
    ##user_id = ValidateToken(auth_header).execute()
    ##data=request.args.to_dict()
    result = request.args.to_dict()
    result = GetProductos().execute()
    return jsonify(result), 200