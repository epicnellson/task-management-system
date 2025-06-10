from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateTimeField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description')
    status = SelectField('Status', choices=[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ])
    priority = SelectField('Priority', choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ])
    due_date = DateTimeField('Due Date', format='%Y-%m-%dT%H:%M', validators=[Optional()])
    category_id = SelectField('Category', coerce=int, validators=[Optional()])
    submit = SubmitField('Save')

class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=50)])
    description = TextAreaField('Description')
    color = StringField('Color', validators=[DataRequired()])
    submit = SubmitField('Save')

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('New Password', validators=[Optional(), Length(min=6)])
    confirm_password = PasswordField('Confirm New Password', validators=[Optional(), EqualTo('password')])
    submit = SubmitField('Update Profile') 