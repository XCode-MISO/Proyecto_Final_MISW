from flask import Blueprint, request, jsonify, current_app
from src.models import db, Recommendation
from src.services.recommendation_service import create_pending_recommendation

recommendation_bp = Blueprint('recommendation', __name__)

@recommendation_bp.route('/pubsub_update', methods=['POST'])
def pubsub_update():
    data = request.get_json()
    current_app.logger.info("Mensaje recibido de Pub/Sub: %s", data)
    if not data or "job_id" not in data:
        return jsonify({"error": "Falta job_id en el mensaje"}), 400
    try:
        job_id = data["job_id"]
        rec = create_pending_recommendation(job_id, db, Recommendation)
        return jsonify({"message": "Recomendación pendiente creada", "job_id": rec.job_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@recommendation_bp.route('/recommend', methods=['GET'])
def get_recommendation():
    job_id = request.args.get('job_id')
    if not job_id:
        return jsonify({'error': 'job_id es requerido'}), 400
    rec = Recommendation.query.get(job_id)
    if not rec:
        return jsonify({'error': f'No se encontró recomendación para job_id {job_id}'}), 404
    return jsonify({
        'job_id': rec.job_id,
        'final_state': rec.final_state,
        'final_recommendation': rec.final_recommendation,
        'recommendation_data': rec.recommendation_data
    })

@recommendation_bp.route('/health', methods=['GET'])
def health():
    return "OK", 200