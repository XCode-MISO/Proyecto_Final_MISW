def update_or_create_recommendation(data, db, Recommendation):
    job_id = data.get('job_id')
    final_state = data.get('final_state')
    final_recommendation = data.get('final_recommendation')
    recommendation_data = data.get('recommendation_data')

    if not job_id or not final_state or final_recommendation is None:
        raise ValueError("Datos insuficientes para crear/actualizar la recomendación.")

    rec = Recommendation.query.get(job_id)
    if rec:
        rec.final_state = final_state
        rec.final_recommendation = final_recommendation
        rec.recommendation_data = recommendation_data
    else:
        rec = Recommendation(
            job_id=job_id,
            final_state=final_state,
            final_recommendation=final_recommendation,
            recommendation_data=recommendation_data
        )
        db.session.add(rec)
    db.session.commit()
    return rec

def create_pending_recommendation(job_id, db, Recommendation):
    rec = Recommendation.query.get(job_id)
    if not rec:
        rec = Recommendation(
            job_id=job_id,
            final_state="pending",
            final_recommendation="",
            recommendation_data={}
        )
        db.session.add(rec)
        db.session.commit()
    return rec
