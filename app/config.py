import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:your_password@localhost/taskmanager'
    SQLALCHEMY_TRACK_MODIFICATIONS = False 