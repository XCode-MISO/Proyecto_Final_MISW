from flask import Blueprint, request, jsonify
from src.models import db, Recommendation
from src.services.recommendation_service import update_or_create_recommendation

recommendation_bp = Blueprint('recommendation', __name__)

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

@recommendation_bp.route('/update_recommendation', methods=['POST'])
def update_recommendation():
    data = request.get_json()
    rec = update_or_create_recommendation(data, db, Recommendation)
    return jsonify({
        'message': 'Recomendación actualizada exitosamente',
        'job_id': rec.job_id
    }), 200
