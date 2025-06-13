import os
import sys

# Add the project directory to the Python path
path = os.path.dirname(os.path.abspath(__file__))
if path not in sys.path:
    sys.path.append(path)

# Set environment variables
os.environ['FLASK_APP'] = 'app'
os.environ['FLASK_ENV'] = 'production'

# Import the Flask app
from app import create_app
application = create_app() 