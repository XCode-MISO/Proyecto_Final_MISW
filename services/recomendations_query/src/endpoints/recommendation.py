from flask import Blueprint, request, jsonify, current_app
from src.models import db, Recommendation
from src.services.recommendation_service import create_pending_recommendation

recommendation_bp = Blueprint('recommendation', __name__)


@recommendation_bp.route('/recommend', methods=['GET'])
def get_recommendation():
    job_id = request.args.get('job_id')
    if not job_id:
        return jsonify({'error': 'job_id es requerido'}), 400

    rec: Recommendation | None = Recommendation.query.get(job_id)
    if rec is None:
        return jsonify({'error': f'No se encontró recomendación para job_id {job_id}'}), 404

    from src.services.recommendation_service import recommend_products 
    suggested_products = recommend_products(rec.identified_objects or [])

    return jsonify({
        'job_id':               rec.job_id,
        'final_state':          rec.final_state,
        'final_recommendation': rec.final_recommendation,
        'identified_objects':   rec.identified_objects,
        'recommended_products': suggested_products
    })

@recommendation_bp.route('/health', methods=['GET'])
def health():
    return "OK", 200