# from flask import Flask, render_template, url_for, redirect
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin
# from flask_wtf import FlaskForm
# from wtforms import SearchField, PasswordField, SubmitField
# from wtforms.validators import InputRequired, Length, ValidationError
# from flask_bcrypt import Bcrypt

# app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app.config['SECRET_KEY'] = '12345'
# db = SQLAlchemy(app)
# bcrypt = Bcrypt(app)

# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), nullable=False, unique=False)
#     password = db.Column(db.String(80), nullable=False)  # 80 for hashes

# class RegisterForm(FlaskForm):
#     username = SearchField(validators=[InputRequired(), Length(
#         min=4, max=20)], render_kw={"placeholder": "Username"})
    
#     password = PasswordField(validators=[InputRequired(), Length(
#         min=4, max=20)], render_kw={"placeholder": "Password"})
    
#     submit = SubmitField("Register")

#     def validate_username(self, username):
#         existing_user_username = User.query.filter_by(username=username.data).first()
#         if existing_user_username:
#             raise ValidationError("Ce username existe déjà. Choisissez un autre.")


# class LoginForm(FlaskForm):
#     username = SearchField(validators=[InputRequired(), Length(
#         min=4, max=20)], render_kw={"placeholder": "Username"})
    
#     password = PasswordField(validators=[InputRequired(), Length(
#         min=4, max=20)], render_kw={"placeholder": "Password"})
    
#     submit = SubmitField("Register")


# @app.route('/')
# def home():
#     return render_template('main.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     return render_template('login.html', form=form)

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegisterForm()

#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data)
#         new_user = User(username=form.username.data, password=hashed_password)
#         db.session.add(new_user)
#         db.session.commit()
#         return redirect(url_for('login'))
#     return render_template('register.html', form=form)


# if __name__== '__main__':
#     # with app.app_context():  # Ensure this runs within the Flask app context
#     #     db.create_all()  # Create database tables
#     #     print("Database tables created!")
#     app.run(debug=True)



from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
import logging

# Configuration de l'application Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Kandinsky_95@localhost:5432/postgres'
app.config['SECRET_KEY'] = '12345'

# Initialisation des extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Configuration des logs
logging.basicConfig(level=logging.INFO)

# Modèle de la table User
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # Clé primaire
    username = db.Column(db.String(20), nullable=False, unique=True)  # Nom d'utilisateur unique
    password = db.Column(db.String(80), nullable=False)  # Mot de passe hashé

# Formulaire pour l'inscription
class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)],
                           render_kw={"placeholder": "Nom d'utilisateur"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)],
                             render_kw={"placeholder": "Mot de passe"})
    submit = SubmitField("S'inscrire")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            # Utilisation de flash pour afficher un message d'avertissement
            flash("Ce nom d'utilisateur existe déjà. Veuillez en choisir un autre.", "warning")
            raise ValidationError("Ce nom d'utilisateur existe déjà. Veuillez en choisir un autre.")
# Formulaire pour la connexion
class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)],
                           render_kw={"placeholder": "Nom d'utilisateur"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)],
                             render_kw={"placeholder": "Mot de passe"})
    submit = SubmitField("Se connecter")

# Route principale
@app.route('/')
def home():
    return render_template('main.html')

# Route pour la connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Logique de connexion ici
        logging.info(f"Tentative de connexion pour l'utilisateur : {form.username.data}")
        return redirect(url_for('home'))
    return render_template('login.html', form=form)



def sashboard():
    return render_template('dashboard.html')

# Route pour l'inscription
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Hash du mot de passe
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        # Création de l'utilisateur
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)  # Ajoute l'utilisateur à la session
        db.session.commit()  # Enregistre l'utilisateur dans la base de données
        logging.info(f"Nouvel utilisateur ajouté : {new_user.username}")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Lancer l'application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crée les tables si elles n'existent pas encore
        logging.info("Tables créées avec succès dans PostgreSQL.")
    app.run(debug=True)
