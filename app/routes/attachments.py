from flask import Blueprint, request, jsonify, send_file, current_app
from flask_login import login_required, current_user
from app.models.attachment import Attachment
from app.models.task import Task
from app import db
import os

attachments = Blueprint('attachments', __name__)

@attachments.route('/upload/<int:task_id>', methods=['POST'])
@login_required
def upload_file(task_id):
    task = Task.query.get_or_404(task_id)
    
    # Check if user has access to the task
    if task.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        attachment = Attachment.save_file(file, task_id, current_user.id)
        return jsonify(attachment.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@attachments.route('/download/<int:attachment_id>')
@login_required
def download_file(attachment_id):
    attachment = Attachment.query.get_or_404(attachment_id)
    
    # Check if user has access to the task
    if attachment.task.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        return send_file(
            attachment.file_path,
            as_attachment=True,
            download_name=attachment.original_filename
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@attachments.route('/delete/<int:attachment_id>', methods=['DELETE'])
@login_required
def delete_file(attachment_id):
    attachment = Attachment.query.get_or_404(attachment_id)
    
    # Check if user has access to the task
    if attachment.task.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        if attachment.delete_file():
            db.session.delete(attachment)
            db.session.commit()
            return jsonify({'message': 'File deleted successfully'}), 200
        return jsonify({'error': 'Failed to delete file'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@attachments.route('/list/<int:task_id>')
@login_required
def list_files(task_id):
    task = Task.query.get_or_404(task_id)
    
    # Check if user has access to the task
    if task.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    attachments = Attachment.query.filter_by(task_id=task_id).all()
    return jsonify([attachment.to_dict() for attachment in attachments]) 