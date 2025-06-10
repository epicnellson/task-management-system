from flask import Blueprint, render_template
from flask_login import current_user, login_required
from app.models import Task

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    if current_user.is_authenticated:
        return dashboard()
    return render_template('main/index.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.created_at.desc()).all()
    return render_template('main/dashboard.html', tasks=tasks) 