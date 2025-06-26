from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from config import Config
from flask_migrate import Migrate # Import Migrate


# --- GLOBAL INSTANCES ---
# These must be defined BEFORE create_app() or any usage
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # --- INITIALIZE EXTENSIONS WITH THE APP ---
  
    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db) # Initialize Flask-Migrate with app and db

    # Explicitly attach db to the app object for easy access (e.g., current_app.db)
    # This comes AFTER db.init_app(app)
    app.db = db # CORRECT: Assign after db is an instance and initialized with app

    # --- FLASK-LOGIN CONFIGURATION ---
    login_manager.init_app(app) # Initialize login_manager with the app
    login_manager.login_view = 'main.login' # Set login_view after init_app
    login_manager.login_message_category = 'info'

    # --- USER LOADER ---
    # Move the user_loader function here (from models.py)
    # Import User model here to avoid circular imports
    from app.models import User 
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # --- REGISTER BLUEPRINTS ---
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # --- CREATE DATABASE TABLES ---
    
    with app.app_context():
        db.create_all()

    
    # --- DISABLE CACHING (security fix for back button after logout) ---
    @app.after_request
    def add_header(response):
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, maxx-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "-1"
        return response
    
    
    return app









