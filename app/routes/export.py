from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from app.models.task import Task
from datetime import datetime

export = Blueprint('export', __name__)

@export.route('/export/tasks')
@login_required
def export_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return jsonify([task.to_dict() for task in tasks]) 