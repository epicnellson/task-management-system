from app import db
from datetime import datetime

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    priority = db.Column(db.String(20), default='medium')
    due_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    
    # Relationships
    category = db.relationship('Category', backref=db.backref('tasks', lazy=True))
    comments = db.relationship('Comment', backref='task', lazy=True, cascade='all, delete-orphan')
    attachments = db.relationship('Attachment', backref=db.backref('task_attachments', overlaps="attachments,task_attachments"), lazy=True, cascade='all, delete-orphan', overlaps="attachments,task_attachments")
    
    def __repr__(self):
        return f'<Task {self.title}>'
    
    @property
    def status_color(self):
        status_colors = {
            'pending': 'warning',
            'in_progress': 'primary',
            'completed': 'success'
        }
        return status_colors.get(self.status, 'secondary')
    
    @property
    def priority_color(self):
        priority_colors = {
            'low': 'success',
            'medium': 'warning',
            'high': 'danger'
        }
        return priority_colors.get(self.priority, 'secondary')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'due_date': self.due_date.strftime('%Y-%m-%d %H:%M') if self.due_date else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M'),
            'user_id': self.user_id,
            'category_id': self.category_id,
            'category': self.category.to_dict() if self.category else None,
            'comments_count': len(self.comments)
        } 