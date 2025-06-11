from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail
from flask_caching import Cache
from dotenv import load_dotenv
import os
from config import Config

# Load environment variables
load_dotenv()

# Initialize Flask extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
limiter = Limiter(key_func=get_remote_address)
mail = Mail()
cache = Cache()

def create_app(config_class=Config):
    app = Flask(__name__)
    
    # Configure the app
    app.config.from_object(config_class)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-123')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:1234@localhost:5432/taskmanager')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Mail configuration
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
    
    # Cache configuration
    app.config['CACHE_TYPE'] = 'simple'
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300

    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    mail.init_app(app)
    cache.init_app(app)

    # Set up login view
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    # Register blueprints
    from app.routes.main import bp as main_bp
    from app.routes.auth import auth as auth_bp
    from app.routes.tasks import tasks as tasks_bp
    from app.routes.categories import categories as categories_bp
    from app.routes.comments import comments as comments_bp
    from app.routes.notifications import notifications as notifications_bp
    from app.routes.attachments import attachments as attachments_bp
    from app.routes.templates import templates as templates_bp
    from app.routes.export import export as export_bp
    from app.routes.activity import activity as activity_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(comments_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(attachments_bp)
    app.register_blueprint(templates_bp)
    app.register_blueprint(export_bp)
    app.register_blueprint(activity_bp)

    # Register custom filters
    @app.template_filter('status_color')
    def status_color(status):
        colors = {
            'pending': 'warning',
            'in_progress': 'info',
            'completed': 'success'
        }
        return colors.get(status, 'secondary')

    @app.template_filter('priority_color')
    def priority_color(priority):
        colors = {
            'low': 'success',
            'medium': 'warning',
            'high': 'danger'
        }
        return colors.get(priority, 'secondary')

    # Create database tables
    with app.app_context():
        db.create_all()

    # Add custom CLI commands
    @app.cli.command("reset-db")
    def reset_db():
        """Reset the database to a fresh state."""
        from app.models.user import User
        from app.models.task import Task
        from app.models.category import Category
        from app.models.comment import Comment
        from app.models.notification import Notification
        from app.models.attachment import Attachment
        from app.models.template import TaskTemplate
        from app.models.activity import Activity
        with app.app_context():
            print("Starting database reset...")
            
            # Delete all data from tables
            print("Deleting all data...")
            Attachment.query.delete()
            Comment.query.delete()
            Notification.query.delete()
            Task.query.delete()
            Category.query.delete()
            TaskTemplate.query.delete()
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

    return app 