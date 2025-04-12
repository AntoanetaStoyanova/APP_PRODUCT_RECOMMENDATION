from config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from .models import user_db
import os
bcrypt = Bcrypt()
# Initializer for extensions
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('POSTGRESQL_URI')
    app.config.from_object(Config)
    

    # Initialize extensions inside create_app
    bcrypt = Bcrypt(app)
    
    user_db.init_app(app)
    login_manager.init_app(app)

    # Import routes inside create_app to avoid circular import
    from .routes import main_bp
    app.register_blueprint(main_bp, url_prefix='/')

    return app

