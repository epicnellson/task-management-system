from app import db
from datetime import datetime

class TaskTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.String(20), default='medium')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    category = db.relationship('Category', backref=db.backref('templates', lazy=True))
    user = db.relationship('User', backref=db.backref('templates', lazy=True))
    
    def __repr__(self):
        return f'<TaskTemplate {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'category_id': self.category_id,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M')
        }
    
    def create_task(self, user_id):
        """Create a new task from this template"""
        from app.models.task import Task
        
        task = Task(
            title=self.title,
            description=self.description,
            priority=self.priority,
            category_id=self.category_id,
            user_id=user_id
        )
        
        db.session.add(task)
        db.session.commit()
        
        return task 