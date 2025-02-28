# app/models.py
# app/models.py

from flask import Flask
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON

app = Flask(__name__)


from flask_sqlalchemy import SQLAlchemy



# Paramètres de connexion
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "Kandinsky_95"
DB_HOST = "localhost"
DB_PORT = "5432"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Kandinsky_95@127.0.0.1:5432/postgres"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "1234"  # Nécessaire pour `flash`
user_db = SQLAlchemy(app)
# Table d'association user_produit (Many-to-Many)
user_produit = user_db.Table(
    "user_produit",
    user_db.Column("user_id", user_db.Integer, user_db.ForeignKey("user.id"), primary_key=True),
    user_db.Column("product_id", user_db.Integer, user_db.ForeignKey("produits.id_produit"), primary_key=True),
)


class Product(user_db.Model):
    __tablename__ = 'produits'  # Spécifie le nom exact de la table
    id_produit = user_db.Column(user_db.Integer, primary_key=True)
    url = user_db.Column(user_db.String, nullable=True)
    nom_produit = user_db.Column(user_db.String, nullable=False)
    img_produit = user_db.Column(user_db.String, nullable=False)
    prix_produit = user_db.Column(user_db.Float, nullable=True)
    contenance = user_db.Column(user_db.String, nullable=True)
    pg_vg = user_db.Column(user_db.String, nullable=True)
    origine = user_db.Column(user_db.String, nullable=True)
    frais = user_db.Column(user_db.String, nullable=True)
    surbooste = user_db.Column(user_db.String, nullable=True)
    saveur = user_db.Column(user_db.String, nullable=True)
    description = user_db.Column(user_db.String, nullable=True)
    brand = user_db.Column(user_db.String, nullable=True)
    gout = user_db.Column(user_db.String, nullable=True)
    info_brand = user_db.Column(user_db.String, nullable=True)

    # Relation inverse avec User via la table d'association user_produit
    users = user_db.relationship(
        "User", secondary=user_produit, back_populates="products"
    )

    def __repr__(self):
        return f"<Product {self.nom_produit}>"


class User(user_db.Model, UserMixin):
    id = user_db.Column(user_db.Integer, primary_key=True)
    username = user_db.Column(user_db.String(20), nullable=False, unique=True)
    password = user_db.Column(user_db.String(80), nullable=False)

    consent = user_db.Column(user_db.Boolean, default=False)  # Le champ pour le consentement

    # Relation Many-to-Many avec Product via la table d'association user_produit
    products = user_db.relationship(
        "Product", secondary=user_produit, back_populates="users"
    )

    def __repr__(self):
        return f'<User {self.username}>'
    
class Recommendation(user_db.Model):  # Correction ici !
    __tablename__ = 'recommendations'

    id = user_db.Column(user_db.Integer, primary_key=True)
    question = user_db.Column(user_db.Text, nullable=False)  # Texte illimité
    response = user_db.Column(user_db.JSON, nullable=False)  # Stockage JSON (nécessite PostgreSQL)
    documents = user_db.Column(user_db.JSON, nullable=False)  # Stockage JSON

    def __repr__(self):
        return f"<Recommendation(id={self.id}, question='{self.question[:50]}...')>"  # Affiche un extrait de la question
