from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app.models.task import Task
from app.models.category import Category
from app.models.notification import Notification
from app.models.template import TaskTemplate
from app.models.activity import Activity
from app import db
from datetime import datetime, timedelta
import json

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('main/index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    # Get user's tasks
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.due_date.asc()).all()
    
    # Get user's categories
    categories = Category.query.filter_by(user_id=current_user.id).all()
    
    # Get recent notifications
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).limit(5).all()
    
    # Get task templates
    templates = TaskTemplate.query.filter_by(user_id=current_user.id).all()
    
    # Get recent activity
    activities = Activity.query.filter_by(user_id=current_user.id).order_by(Activity.timestamp.desc()).limit(10).all()
    
    # Calculate task statistics
    total_tasks = len(tasks)
    completed_tasks = len([task for task in tasks if task.status == 'completed'])
    pending_tasks = total_tasks - completed_tasks
    
    # Get tasks due today
    today = datetime.now().date()
    tasks_due_today = [task for task in tasks if task.due_date and task.due_date.date() == today]
    
    # Get upcoming tasks (next 7 days)
    next_week = today + timedelta(days=7)
    upcoming_tasks = [task for task in tasks if task.due_date and today < task.due_date.date() <= next_week]
    
    return render_template('main/dashboard.html',
                         tasks=tasks,
                         categories=categories,
                         notifications=notifications,
                         templates=templates,
                         activities=activities,
                         total_tasks=total_tasks,
                         completed_tasks=completed_tasks,
                         pending_tasks=pending_tasks,
                         tasks_due_today=tasks_due_today,
                         upcoming_tasks=upcoming_tasks)

@main.route('/search')
@login_required
def search():
    query = request.args.get('q', '')
    if not query:
        return redirect(url_for('main.dashboard'))
    
    # Search in tasks
    tasks = Task.query.filter(
        Task.user_id == current_user.id,
        (Task.title.ilike(f'%{query}%') | Task.description.ilike(f'%{query}%'))
    ).all()
    
    # Search in categories
    categories = Category.query.filter(
        Category.user_id == current_user.id,
        Category.name.ilike(f'%{query}%')
    ).all()
    
    return render_template('main/search_results.html',
                         query=query,
                         tasks=tasks,
                         categories=categories)

@main.route('/profile')
@login_required
def profile():
    return render_template('main/profile.html')

@main.route('/settings')
@login_required
def settings():
    return render_template('main/settings.html')

@main.route('/help')
def help():
    return render_template('main/help.html')

@main.route('/about')
def about():
    return render_template('main/about.html')

@main.route('/contact')
def contact():
    return render_template('main/contact.html')

@main.route('/privacy')
def privacy():
    return render_template('main/privacy.html')

@main.route('/terms')
def terms():
    return render_template('main/terms.html')

@main.route('/sitemap.xml')
def sitemap():
    return render_template('main/sitemap.xml')

@main.route('/robots.txt')
def robots():
    return render_template('main/robots.txt')

@main.route('/manifest.json')
def manifest():
    return render_template('main/manifest.json')

@main.route('/service-worker.js')
def service_worker():
    return render_template('main/service-worker.js')

@main.route('/offline')
def offline():
    return render_template('main/offline.html')

@main.route('/404')
def not_found():
    return render_template('main/404.html'), 404

@main.route('/500')
def server_error():
    return render_template('main/500.html'), 500

@main.route('/403')
def forbidden():
    return render_template('main/403.html'), 403

@main.route('/401')
def unauthorized():
    return render_template('main/401.html'), 401

@main.route('/400')
def bad_request():
    return render_template('main/400.html'), 400

@main.route('/405')
def method_not_allowed():
    return render_template('main/405.html'), 405

@main.route('/429')
def too_many_requests():
    return render_template('main/429.html'), 429

@main.route('/503')
def service_unavailable():
    return render_template('main/503.html'), 503

@main.route('/504')
def gateway_timeout():
    return render_template('main/504.html'), 504

@main.route('/505')
def http_version_not_supported():
    return render_template('main/505.html'), 505

@main.route('/507')
def insufficient_storage():
    return render_template('main/507.html'), 507

@main.route('/508')
def loop_detected():
    return render_template('main/508.html'), 508

@main.route('/510')
def not_extended():
    return render_template('main/510.html'), 510

@main.route('/511')
def network_authentication_required():
    return render_template('main/511.html'), 511

@main.route('/520')
def unknown_error():
    return render_template('main/520.html'), 520

@main.route('/521')
def web_server_is_down():
    return render_template('main/521.html'), 521

@main.route('/522')
def connection_timed_out():
    return render_template('main/522.html'), 522

@main.route('/523')
def origin_is_unreachable():
    return render_template('main/523.html'), 523

@main.route('/524')
def a_timeout_occurred():
    return render_template('main/524.html'), 524

@main.route('/525')
def ssl_handshake_failed():
    return render_template('main/525.html'), 525

@main.route('/526')
def invalid_ssl_certificate():
    return render_template('main/526.html'), 526

@main.route('/527')
def railgun_error():
    return render_template('main/527.html'), 527

@main.route('/530')
def site_is_frozen():
    return render_template('main/530.html'), 530

@main.route('/598')
def network_read_timeout_error():
    return render_template('main/598.html'), 598

@main.route('/599')
def network_connect_timeout_error():
    return render_template('main/599.html'), 599 