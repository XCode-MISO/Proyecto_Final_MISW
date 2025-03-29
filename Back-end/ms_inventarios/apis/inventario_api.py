from flask import Blueprint, jsonify

inventario_bp = Blueprint('inventario_bp', __name__)

@inventario_bp.route('/ping', methods=['GET'])
def ping():
    return jsonify({"msg": "ms_inventarios alive"}), 200