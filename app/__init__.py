from flask import Flask
from dotenv import load_dotenv
import os
from .models import db
from config import Config

def create_app():
    app = Flask(__name__)

    # Load environment variables from .env file
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    app.config.from_object(Config)

    # Initialize the database
    db.init_app(app)

    with app.app_context():
        # Create database tables if they don't exist
        db.create_all()

    # Import and register routes within the application context
    from . import routes
    app.register_blueprint(routes.bp)

    return app
