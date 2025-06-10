from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from app.models.template import TaskTemplate
from app.models.category import Category
from app import db

templates = Blueprint('templates', __name__)

@templates.route('/')
@login_required
def index():
    templates = TaskTemplate.query.filter_by(user_id=current_user.id).all()
    categories = Category.query.filter_by(user_id=current_user.id).all()
    return render_template('templates/index.html', templates=templates, categories=categories)

@templates.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        data = request.form
        
        template = TaskTemplate(
            title=data['title'],
            description=data['description'],
            priority=data['priority'],
            category_id=data.get('category_id'),
            user_id=current_user.id
        )
        
        db.session.add(template)
        db.session.commit()
        
        return jsonify(template.to_dict()), 201
    
    categories = Category.query.filter_by(user_id=current_user.id).all()
    return render_template('templates/create.html', categories=categories)

@templates.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    template = TaskTemplate.query.get_or_404(id)
    
    if template.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if request.method == 'POST':
        data = request.form
        
        template.title = data['title']
        template.description = data['description']
        template.priority = data['priority']
        template.category_id = data.get('category_id')
        
        db.session.commit()
        
        return jsonify(template.to_dict())
    
    categories = Category.query.filter_by(user_id=current_user.id).all()
    return render_template('templates/edit.html', template=template, categories=categories)

@templates.route('/delete/<int:id>', methods=['DELETE'])
@login_required
def delete(id):
    template = TaskTemplate.query.get_or_404(id)
    
    if template.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(template)
    db.session.commit()
    
    return jsonify({'message': 'Template deleted successfully'})

@templates.route('/use/<int:id>', methods=['POST'])
@login_required
def use_template(id):
    template = TaskTemplate.query.get_or_404(id)
    
    if template.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    task = template.create_task(current_user.id)
    
    return jsonify({
        'message': 'Task created successfully',
        'task_id': task.id
    }) 