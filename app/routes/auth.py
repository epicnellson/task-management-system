from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app import db
from urllib.parse import urlparse
from app.forms import ProfileForm
import os

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('auth.register'))

        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'danger')
            return redirect(url_for('auth.register'))

        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'danger')
            return redirect(url_for('auth.register'))

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember', False)

        user = User.query.filter_by(username=username).first()
        
        if user is None or not user.check_password(password):
            flash('Invalid username or password!', 'danger')
            return redirect(url_for('auth.login'))

        login_user(user, remember=remember)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)

    return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.password.data:
            current_user.password = generate_password_hash(form.password.data)
        db.session.commit()
        flash('Your profile has been updated.', 'success')
        return redirect(url_for('auth.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('auth/profile.html', form=form)

@auth.route('/delete-account', methods=['GET', 'POST'])
@login_required
def delete_account():
    if request.method == 'POST':
        # Verify password before deletion
        if not check_password_hash(current_user.password, request.form.get('password')):
            flash('Incorrect password. Please try again.', 'danger')
            return redirect(url_for('auth.delete_account'))
        
        # Delete user's tasks, comments, and other related data
        for task in current_user.tasks:
            # Delete task attachments
            for attachment in task.attachments:
                if attachment.file_path and os.path.exists(attachment.file_path):
                    os.remove(attachment.file_path)
                db.session.delete(attachment)
            
            # Delete task comments
            for comment in task.comments:
                db.session.delete(comment)
            
            db.session.delete(task)
        
        # Delete user's categories
        for category in current_user.categories:
            db.session.delete(category)
        
        # Delete user's notifications
        for notification in current_user.notifications:
            db.session.delete(notification)
        
        # Delete user's templates
        for template in current_user.templates:
            db.session.delete(template)
        
        # Delete the user
        db.session.delete(current_user)
        db.session.commit()
        
        flash('Your account has been permanently deleted.', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('auth/delete_account.html') 