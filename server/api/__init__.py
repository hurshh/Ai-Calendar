"""
API package initialization
"""

from flask import Flask
from flask_cors import CORS
from api.routes.calendar_routes import calendar_routes
from api.routes.chat_routes import chat_routes
from config.settings import DEBUG, HOST, PORT

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__, template_folder='../templates')
    CORS(app)

    # Register blueprints
    app.register_blueprint(calendar_routes, url_prefix='/api')
    app.register_blueprint(chat_routes, url_prefix='/api')

    # Register main route
    @app.route('/')
    def index():
        """Serve the main calendar interface"""
        return app.send_static_file('index.html')

    return app 