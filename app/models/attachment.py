from app import db
from datetime import datetime
import os
from werkzeug.utils import secure_filename

class Attachment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(512), nullable=False)
    file_type = db.Column(db.String(50), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)  # Size in bytes
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    task = db.relationship('Task', backref='task_attachments', overlaps="attachments,task_attachments")
    user = db.relationship('User', backref='attachments')
    
    def __repr__(self):
        return f'<Attachment {self.original_filename}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'file_type': self.file_type,
            'file_size': self.file_size,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M'),
            'task_id': self.task_id,
            'user_id': self.user_id
        }
    
    @staticmethod
    def save_file(file, task_id, user_id):
        if not file:
            return None
            
        filename = secure_filename(file.filename)
        file_ext = os.path.splitext(filename)[1]
        unique_filename = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{filename}"
        
        # Create upload directory if it doesn't exist
        upload_dir = os.path.join('uploads', str(task_id))
        os.makedirs(upload_dir, exist_ok=True)
        
        file_path = os.path.join(upload_dir, unique_filename)
        file.save(file_path)
        
        attachment = Attachment(
            filename=unique_filename,
            original_filename=filename,
            file_path=file_path,
            file_type=file.content_type,
            file_size=os.path.getsize(file_path),
            task_id=task_id,
            user_id=user_id
        )
        
        db.session.add(attachment)
        db.session.commit()
        
        return attachment
    
    def delete_file(self):
        try:
            if os.path.exists(self.file_path):
                os.remove(self.file_path)
            return True
        except Exception as e:
            print(f"Error deleting file: {str(e)}")
            return False 