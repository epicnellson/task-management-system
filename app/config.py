import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:your_password@localhost/taskmanager'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # VAPID keys for push notifications
    VAPID_PUBLIC_KEY = os.environ.get('VAPID_PUBLIC_KEY') or 'your-vapid-public-key'
    VAPID_PRIVATE_KEY = os.environ.get('VAPID_PRIVATE_KEY') or 'your-vapid-private-key'
    VAPID_CLAIMS = {
        "sub": "mailto:your-email@example.com"
    }

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///task_manager.db'
    WTF_CSRF_ENABLED = False
    SERVER_NAME = 'localhost.localdomain' 