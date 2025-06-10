from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models.notification import Notification
from app import db, limiter
from datetime import datetime, timedelta
from app.models.task import Task

notifications = Blueprint('notifications', __name__)

@notifications.route('/notifications')
@login_required
@limiter.limit("30/minute")
def get_notifications():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    notifications = Notification.query.filter_by(user_id=current_user.id)\
        .order_by(Notification.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'notifications': [n.to_dict() for n in notifications.items],
        'total': notifications.total,
        'pages': notifications.pages,
        'current_page': notifications.page
    })

@notifications.route('/notifications/mark-read', methods=['POST'])
@login_required
@limiter.limit("30/minute")
def mark_notifications_read():
    notification_ids = request.json.get('notification_ids', [])
    
    if not notification_ids:
        return jsonify({'error': 'No notification IDs provided'}), 400
    
    Notification.query.filter(
        Notification.id.in_(notification_ids),
        Notification.user_id == current_user.id
    ).update({Notification.is_read: True}, synchronize_session=False)
    
    db.session.commit()
    return jsonify({'message': 'Notifications marked as read'})

@notifications.route('/notifications/check-due-tasks')
@login_required
@limiter.limit("5/minute")
def check_due_tasks():
    # Check for tasks due in the next 24 hours
    tomorrow = datetime.utcnow() + timedelta(days=1)
    due_tasks = current_user.tasks.filter(
        Task.due_date <= tomorrow,
        Task.status != 'completed'
    ).all()
    
    for task in due_tasks:
        notification = Notification(
            user_id=current_user.id,
            task_id=task.id,
            message=f'Task "{task.title}" is due soon!',
            type='task_due'
        )
        db.session.add(notification)
    
    db.session.commit()
    return jsonify({'message': 'Due task check completed'})

@notifications.route('/notifications/clear-all', methods=['POST'])
@login_required
@limiter.limit("5/minute")
def clear_all_notifications():
    Notification.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    return jsonify({'message': 'All notifications cleared'}) 