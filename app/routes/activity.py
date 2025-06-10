from flask import Blueprint, jsonify
from flask_login import login_required
from app import db
from app.models import Activity

activity = Blueprint('activity', __name__)

@activity.route('/activities')
@login_required
def get_activities():
    """Get all activities"""
    activities = Activity.query.all()
    return jsonify([{
        'id': activity.id,
        'action': activity.action,
        'timestamp': activity.timestamp.isoformat(),
        'user_id': activity.user_id
    } for activity in activities]) 