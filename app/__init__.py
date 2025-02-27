# from flask import Flask
# from dotenv import load_dotenv
# import os

# from flask import Flask

# def create_app():
#     app = Flask(__name__)

#     # Importer et enregistrer le blueprint
#     from .routes import main_bp
#     app.register_blueprint(main_bp)

#     return app


# app/__init__.py

# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_bcrypt import Bcrypt
# from flask_login import LoginManager
# from config import Config


# # Initialiser les extensions
# db = SQLAlchemy()
# bcrypt = Bcrypt()
# login_manager = LoginManager()

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)  # Appliquer la configuration
#     # Configurer votre base de données
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Kandinsky_95@localhost:5432/postgres'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     # Initialiser les extensions avec l'application Flask
#     db.init_app(app)
#     bcrypt.init_app(app)
#     login_manager.init_app(app)

#     # Définir la fonction de chargement de l'utilisateur
#     @login_manager.user_loader
#     def load_user(user_id):
#         return User.query.get(int(user_id))  # Charger l'utilisateur à partir de la base de données

#     from .routes import main_bp
#     app.register_blueprint(main_bp)

#     return app

# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from .models import user_db

import os
# Initialiser les extensions
import sys


sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/../'))
from config import Config
bcrypt = Bcrypt()
login_manager = LoginManager()

# Fonction de chargement de l'utilisateur (user_loader)
@login_manager.user_loader
def load_user(user_id):
    from .models import User 
    return User.query.get(int(user_id))  # Charge un utilisateur par son ID

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Kandinsky_95@localhost:5432/postgres'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    app.config.from_object('config.Config')

    user_db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from .routes import main_bp  # Import inside create_app to avoid circular import
    app.register_blueprint(main_bp)

    return app