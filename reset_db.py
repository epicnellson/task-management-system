from app import create_app, db
from app.models.user import User
from app.models.task import Task
from app.models.category import Category
from app.models.comment import Comment
from app.models.notification import Notification
from app.models.attachment import Attachment
from app.models.template import Template
from app.models.activity import Activity
import os

def reset_database():
    app = create_app()
    
    with app.app_context():
        print("Starting database reset...")
        
        # Delete all data from tables
        print("Deleting all data...")
        Attachment.query.delete()
        Comment.query.delete()
        Notification.query.delete()
        Task.query.delete()
        Category.query.delete()
        Template.query.delete()
        Activity.query.delete()
        User.query.delete()
        
        # Commit the changes
        db.session.commit()
        
        # Remove uploaded files
        uploads_dir = os.path.join(app.root_path, 'uploads')
        if os.path.exists(uploads_dir):
            print("Cleaning uploads directory...")
            for filename in os.listdir(uploads_dir):
                file_path = os.path.join(uploads_dir, filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")
        
        print("Database reset complete!")

if __name__ == '__main__':
    reset_database() 