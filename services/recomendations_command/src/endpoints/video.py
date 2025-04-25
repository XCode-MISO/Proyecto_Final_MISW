import os
import uuid
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from src.models import db, VideoProcess
from src.services.video_service import register_video

video_bp = Blueprint('video', __name__)

@video_bp.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No se proporcionó ningún archivo de video.'}), 400

    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No se seleccionó ningún archivo.'}), 400

    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4().hex}_{filename}"

    job_id, status = register_video(file, unique_filename, db, VideoProcess)
    return jsonify({'job_id': job_id, 'status': status}), 201

@video_bp.route('/health', methods=['GET'])
def health():
    return "OK", 200