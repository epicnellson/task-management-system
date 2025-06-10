from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models.task import Task
from app import db
from datetime import datetime, timedelta
from sqlalchemy import case
from app.models.category import Category
from app.forms import TaskForm
from app.models.attachment import Attachment

tasks = Blueprint('tasks', __name__)

@tasks.route('/tasks')
@login_required
def index():
    # Get filter parameters
    search = request.args.get('search', '')
    status = request.args.get('status', '')
    priority = request.args.get('priority', '')
    due_date = request.args.get('due_date', '')
    category_id = request.args.get('category', type=int)
    sort_by = request.args.get('sort_by', 'due_date')
    sort_order = request.args.get('sort_order', 'asc')
    page = request.args.get('page', 1, type=int)
    per_page = 9  # 3 tasks per row, 3 rows per page
    
    # Base query
    query = Task.query.filter_by(user_id=current_user.id)
    
    # Apply filters
    if search:
        query = query.filter(
            (Task.title.ilike(f'%{search}%')) |
            (Task.description.ilike(f'%{search}%'))
        )
    if status:
        query = query.filter_by(status=status)
    if priority:
        query = query.filter_by(priority=priority)
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    # Apply due date filters
    if due_date:
        today = datetime.utcnow().date()
        if due_date == 'today':
            query = query.filter(db.func.date(Task.due_date) == today)
        elif due_date == 'week':
            week_start = today - timedelta(days=today.weekday())
            week_end = week_start + timedelta(days=6)
            query = query.filter(db.func.date(Task.due_date).between(week_start, week_end))
        elif due_date == 'month':
            month_start = today.replace(day=1)
            if today.month == 12:
                month_end = today.replace(year=today.year + 1, month=1, day=1) - timedelta(days=1)
            else:
                month_end = today.replace(month=today.month + 1, day=1) - timedelta(days=1)
            query = query.filter(db.func.date(Task.due_date).between(month_start, month_end))
    
    # Apply sorting
    if sort_by == 'due_date':
        if sort_order == 'asc':
            query = query.order_by(Task.due_date.asc().nullslast())
        else:
            query = query.order_by(Task.due_date.desc().nullslast())
    elif sort_by == 'priority':
        priority_order = case(
            {'high': 1, 'medium': 2, 'low': 3},
            value=Task.priority
        )
        if sort_order == 'asc':
            query = query.order_by(priority_order.asc())
        else:
            query = query.order_by(priority_order.desc())
    elif sort_by == 'status':
        status_order = case(
            {'pending': 1, 'in_progress': 2, 'completed': 3},
            value=Task.status
        )
        if sort_order == 'asc':
            query = query.order_by(status_order.asc())
        else:
            query = query.order_by(status_order.desc())
    
    # Get paginated results
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    tasks = pagination.items
    
    # Get categories for the filter dropdown
    categories = Category.query.filter_by(user_id=current_user.id).all()
    
    return render_template('tasks/index.html',
                         tasks=tasks,
                         categories=categories,
                         pagination=pagination,
                         sort_by=sort_by,
                         sort_order=sort_order)

@tasks.route('/tasks/create', methods=['GET', 'POST'])
@login_required
def create():
    form = TaskForm()
    categories = Category.query.filter_by(user_id=current_user.id).all()
    form.category_id.choices = [(c.id, c.name) for c in categories]
    
    if form.validate_on_submit():
        try:
            # Convert the datetime string to a datetime object
            due_date = None
            if form.due_date.data:
                try:
                    due_date = datetime.strptime(form.due_date.data, '%Y-%m-%dT%H:%M')
                except ValueError:
                    flash('Invalid date format. Please use the date picker.', 'danger')
                    return render_template('tasks/create.html', form=form, categories=categories)
            
            # Validate category ownership
            if form.category_id.data:
                category = Category.query.get(form.category_id.data)
                if not category or category.user_id != current_user.id:
                    flash('Invalid category selected.', 'danger')
                    return render_template('tasks/create.html', form=form, categories=categories)
            
            task = Task(
                title=form.title.data,
                description=form.description.data,
                status=form.status.data,
                priority=form.priority.data,
                due_date=due_date,
                category_id=form.category_id.data,
                user_id=current_user.id
            )
            db.session.add(task)
            db.session.commit()
            flash('Task created successfully!', 'success')
            return redirect(url_for('tasks.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating task: {str(e)}', 'danger')
    
    return render_template('tasks/create.html', form=form, categories=categories)

@tasks.route('/tasks/<int:id>')
@login_required
def view(id):
    task = Task.query.get_or_404(id)
    if task.user_id != current_user.id:
        flash('You do not have permission to view this task.', 'danger')
        return redirect(url_for('tasks.index'))
    return render_template('tasks/view.html', task=task)

@tasks.route('/tasks/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    task = Task.query.get_or_404(id)
    if task.user_id != current_user.id:
        flash('You do not have permission to edit this task.', 'danger')
        return redirect(url_for('tasks.index'))
    
    form = TaskForm(obj=task)
    categories = Category.query.filter_by(user_id=current_user.id).all()
    form.category_id.choices = [(c.id, c.name) for c in categories]
    
    if form.validate_on_submit():
        try:
            # Convert the datetime string to a datetime object
            due_date = None
            if form.due_date.data:
                try:
                    due_date = datetime.strptime(form.due_date.data, '%Y-%m-%dT%H:%M')
                except ValueError:
                    flash('Invalid date format. Please use the date picker.', 'danger')
                    return render_template('tasks/edit.html', form=form, task=task)
            
            # Validate category ownership
            if form.category_id.data:
                category = Category.query.get(form.category_id.data)
                if not category or category.user_id != current_user.id:
                    flash('Invalid category selected.', 'danger')
                    return render_template('tasks/edit.html', form=form, task=task)
            
            task.title = form.title.data
            task.description = form.description.data
            task.status = form.status.data
            task.priority = form.priority.data
            task.due_date = due_date
            task.category_id = form.category_id.data
            db.session.commit()
            flash('Task updated successfully!', 'success')
            return redirect(url_for('tasks.view', id=task.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating task: {str(e)}', 'danger')
    
    return render_template('tasks/edit.html', form=form, task=task)

@tasks.route('/tasks/<int:id>/delete')
@login_required
def delete(id):
    task = Task.query.get_or_404(id)
    if task.user_id != current_user.id:
        flash('You do not have permission to delete this task.', 'danger')
        return redirect(url_for('tasks.index'))
    
    try:
        # Delete all attachments
        for attachment in task.attachments:
            attachment.delete_file()
        
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting task: {str(e)}', 'danger')
    
    return redirect(url_for('tasks.index'))

@tasks.route('/tasks/<int:id>/status', methods=['POST'])
@login_required
def update_status(id):
    task = Task.query.get_or_404(id)
    
    if task.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    new_status = request.json.get('status')
    if new_status in ['pending', 'in_progress', 'completed']:
        task.status = new_status
        db.session.commit()
        return jsonify(task.to_dict())
    
    return jsonify({'error': 'Invalid status'}), 400

@tasks.route('/tasks/search')
@login_required
def search():
    query = request.args.get('q', '')
    if query:
        tasks = Task.query.filter(
            Task.user_id == current_user.id,
            (Task.title.ilike(f'%{query}%') |
             Task.description.ilike(f'%{query}%'))
        ).all()
    else:
        tasks = []
    return render_template('tasks/index.html', tasks=tasks, query=query) 