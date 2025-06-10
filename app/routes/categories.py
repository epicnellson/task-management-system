from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.category import Category
from app.models.task import Task
from app import db
from app.forms import CategoryForm

categories = Blueprint('categories', __name__)

@categories.route('/categories')
@login_required
def index():
    categories = Category.query.filter_by(user_id=current_user.id).all()
    return render_template('categories/index.html', categories=categories)

@categories.route('/categories/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(
            name=form.name.data,
            description=form.description.data,
            color=form.color.data,
            user_id=current_user.id
        )
        db.session.add(category)
        db.session.commit()
        flash('Category created successfully!', 'success')
        return redirect(url_for('categories.index'))
    return render_template('categories/create.html', form=form)

@categories.route('/categories/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    category = Category.query.get_or_404(id)
    if category.user_id != current_user.id:
        flash('You do not have permission to edit this category.', 'danger')
        return redirect(url_for('categories.index'))
    
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        category.name = form.name.data
        category.description = form.description.data
        category.color = form.color.data
        db.session.commit()
        flash('Category updated successfully!', 'success')
        return redirect(url_for('categories.index'))
    return render_template('categories/edit.html', form=form, category=category)

@categories.route('/categories/<int:id>/delete')
@login_required
def delete(id):
    category = Category.query.get_or_404(id)
    if category.user_id != current_user.id:
        flash('You do not have permission to delete this category.', 'danger')
        return redirect(url_for('categories.index'))
    
    # Check if category has tasks
    if Task.query.filter_by(category_id=category.id).first():
        flash('Cannot delete category with associated tasks.', 'danger')
        return redirect(url_for('categories.index'))
    
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted successfully!', 'success')
    return redirect(url_for('categories.index')) 