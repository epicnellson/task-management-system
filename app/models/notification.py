from app import db
from datetime import datetime

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    message = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # 'task_due', 'comment', 'mention', etc.
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('notifications', lazy=True))
    task = db.relationship('Task', backref=db.backref('notifications', lazy=True))
    
    def __repr__(self):
        return f'<Notification {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'message': self.message,
            'type': self.type,
            'is_read': self.is_read,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M'),
            'task_id': self.task_id,
            'task_title': self.task.title if self.task else None
        } 