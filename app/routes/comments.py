from flask import Blueprint, jsonify, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.models.comment import Comment
from app.models.task import Task
from app import db
from datetime import datetime

comments = Blueprint('comments', __name__)

@comments.route('/comments/create', methods=['POST'])
@login_required
def create():
    data = request.get_json()
    task_id = data.get('task_id')
    content = data.get('content')
    
    if not content:
        return jsonify({'error': 'Comment content is required'}), 400
    
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return jsonify({'error': 'You do not have permission to comment on this task'}), 403
    
    comment = Comment(
        content=content,
        task_id=task_id,
        user_id=current_user.id
    )
    
    db.session.add(comment)
    db.session.commit()
    
    return jsonify({
        'id': comment.id,
        'content': comment.content,
        'username': current_user.username,
        'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M')
    })

@comments.route('/comments/<int:id>/delete', methods=['DELETE'])
@login_required
def delete(id):
    comment = Comment.query.get_or_404(id)
    if comment.user_id != current_user.id:
        return jsonify({'error': 'You do not have permission to delete this comment'}), 403
    
    db.session.delete(comment)
    db.session.commit()
    
    return jsonify({'message': 'Comment deleted successfully'})

@comments.route('/tasks/<int:task_id>/comments')
@login_required
def get_comments(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        return jsonify({'error': 'You do not have permission to view comments for this task'}), 403
    
    comments = Comment.query.filter_by(task_id=task_id).order_by(Comment.created_at.desc()).all()
    return jsonify([{
        'id': comment.id,
        'content': comment.content,
        'username': comment.user.username,
        'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M')
    } for comment in comments]) 