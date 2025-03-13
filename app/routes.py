
import csv
import os
from langchain.document_loaders import CSVLoader
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from .db import get_products, get_user_products, show_produit  # Si vous avez un fichier db.py pour gérer les interactions avec la base de données
from .retriever import retriever, vectorstore
import pandas as pd
from langchain.schema import Document
from app import bcrypt, create_app
from .forms import RegisterForm, LoginForm
from flask_login import login_user, login_required, current_user  

import requests
from config import Config
import logging
# Configurer le logging
logging.basicConfig(
    filename='app.log',  # Nom du fichier de log
    level=logging.ERROR,  # Niveau de log (ici, on capture les erreurs)
    format='%(asctime)s - %(levelname)s - %(message)s'  # Format des logs
)
from .models import User, user_db, Product, user_produit, Recommendation


from sqlalchemy.exc import IntegrityError  # Importer IntegrityError de SQLAlchemy

import re
from werkzeug.exceptions import HTTPException




main_bp = Blueprint('main', __name__)


# df = pd.read_csv('app/rag_csv.csv')
import os
import pandas as pd




df = pd.read_csv(Config.CSV_FILE_PATH)




import time



# ----------------------------------------------------------------------------------------------------------------------------------
from flask import Flask, request, jsonify, render_template
from langchain.chains import RetrievalQA
from langchain.document_loaders import CSVLoader

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

import os
import openai


from app.llm import llm
from app.vectorstore import load_vectorstore, save_vectorstore

from app.utils import search_for_flavor, add_metadata_to_documents

from app.prompt import prompt
from config import Config

# Chargement du CSV avec le chemin provenant de la configuration
df = pd.read_csv(Config.CSV_FILE_PATH)
print(df.head(1))
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

azure_openai_api_key = os.getenv('AZURE_OPENAI_API_KEY_4')
azure_openai_endpoint = os.getenv('AZURE_OPENAI_API_ENDPOINT_4')
deployment_name = os.getenv('AZURE_DEPLOYMENT_NAME_4')


# Set up Azure OpenAI API (for Azure deployment)
openai.api_type = "azure"
openai.api_key = azure_openai_api_key
openai.api_base = azure_openai_endpoint
openai.api_version = "2023-05-15"  # Ensure this is up to date

import warnings
warnings.filterwarnings('ignore')



try:
    # Charger les données avec pandas pour récupérer les colonnes nécessaires
    
    print(f"Colonnes du DataFrame : {df.columns}")

    # Charger les documents avec CSVLoader
    loader = CSVLoader(file_path=Config.CSV_FILE_PATH, encoding='utf-8')
    documents = loader.load()
    print(f"Nombre de documents chargés : {len(documents)}")

    # Vérifier les métadonnées de chaque document avant ajout
    for i, doc in enumerate(documents):
        print(f"Avant ajout - Métadonnées du document {i+1}: {doc.metadata}")

    # Ajouter les colonnes "saveur" et "id_produit" dans les métadonnées
    for doc, (_, row) in zip(documents, df.iterrows()):
        # Assure-toi que la colonne "saveur" et "id_produit" existent bien
        print(f"Row data: {row['saveur']}, {row['id_produit']}")
        
        doc.metadata["saveur"] = row.get("saveur", "Inconnu")  # Ajout de la saveur
        doc.metadata["id_produit"] = row.get("id_produit", "Inconnu")  # Ajout de l'id_produit
    
    # Vérifier les métadonnées de chaque document après ajout
    for i, doc in enumerate(documents):
        print(f"Après ajout - Métadonnées du document {i+1}: {doc.metadata}")
    
    # Sauvegarder le vectorstore avec les métadonnées mises à jour
    vectorstore = save_vectorstore(documents)

except Exception as e:
    print(f"Erreur lors du chargement du CSV : {e}")
    vectorstore = load_vectorstore()  # Charger le vectorstore déjà existant
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

qa_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough(),
    }
    | prompt
    | llm
    | StrOutputParser()
)


# Route principale
@main_bp.route('/')
def acceuil():
    return render_template('accueil.html')

@main_bp.route('/main')
def index():
    return render_template('main.html')

# @main_bp.route('/account/<int:user_id>')
# @login_required
# def account(user_id):
#     # Vérifie que l'ID de l'utilisateur dans l'URL correspond à l'utilisateur connecté
#     if current_user.id != user_id:
#         flash("Vous n'avez pas accès à ces produits.", "danger")
#         return redirect(url_for('auth.login'))  # Redirige vers la page de connexion

#     # Si l'utilisateur est authentifié et a le bon ID, récupère les informations de l'utilisateur
#     user = User.query.get_or_404(user_id)
#     # Appeler la fonction pour récupérer les produits de cet utilisateur
#     produits = get_user_products(user_id)
#     return render_template('user_account.html', user=user, produits=produits)

@main_bp.route('/account/<int:user_id>')
@login_required
def account(user_id):
    # Vérifie que l'ID de l'utilisateur dans l'URL correspond à l'utilisateur connecté
    if current_user.id != user_id:
        flash("Vous n'avez pas accès à ces produits.", "danger")
        return redirect(url_for('auth.login'))  # Redirige vers la page de connexion

    # Si l'utilisateur est authentifié et a le bon ID, récupère les informations de l'utilisateur
    user = User.query.get_or_404(user_id)
    # Appeler la fonction pour récupérer les produits de cet utilisateur
    produits = get_user_products(user_id)
    
    return render_template('user_account.html', user=user, produits=produits[:3])


# Route pour la connexion
@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Connexion réussie !", "success")
            return redirect(url_for('main.index'))
        else:
            flash("Nom d'utilisateur ou mot de passe incorrect.", "danger")
    return render_template('login.html', form=form)

# Route pour l'inscription
# @main_bp.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegisterForm()
#     if form.validate_on_submit():
#         # Vérifier si le consentement a été donné
#         if not form.consent.data:
#             flash("Vous devez accepter les termes et conditions.", "danger")
#             return render_template('register.html', form=form)
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
#         new_user = User(
#             username=form.username.data, 
#             password=hashed_password,
#             consent=form.consent.data
#             )
#         user_db.session.add(new_user)
#         user_db.session.commit()
#         flash(f"Utilisateur {new_user.username} créé avec succès !", "success")
#         return redirect(url_for('main.login'))
#     return render_template('register.html', form=form)
# Route pour l'inscription
@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        # Vérifier si le consentement a été donné
        if not form.consent.data:
            flash("Vous devez accepter les termes et conditions.", "danger")
            return render_template('register.html', form=form)

        # Vérifier si le nom d'utilisateur est déjà pris
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("Ce nom d'utilisateur est déjà pris. Veuillez en choisir un autre.", "danger")
            return render_template('register.html', form=form)

        # Vérifier si le mot de passe est vide
        if not form.password.data.strip():
            flash("Le mot de passe ne peut pas être vide.", "danger")
            return render_template('register.html', form=form)

        # Vérifier si le nom d'utilisateur est vide
        if not form.username.data.strip():
            flash("Le nom d'utilisateur ne peut pas être vide.", "danger")
            return render_template('register.html', form=form)

        # Hacher le mot de passe et enregistrer l'utilisateur
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(
            username=form.username.data, 
            password=hashed_password,
            consent=form.consent.data
        )
        user_db.session.add(new_user)
        user_db.session.commit()
        
        flash(f"Utilisateur {new_user.username} créé avec succès !", "success")
        return redirect(url_for('main.login'))

    return render_template('register.html', form=form)


@main_bp.route('/delete_account', methods=['GET', 'POST'])
@login_required  # Assurez-vous que l'utilisateur est authentifié
def delete_account():
    if request.method == 'POST':
        try:
            # Supprimer les produits associés à l'utilisateur
            user_db.session.query(user_produit).filter_by(user_id=current_user.id).delete()
            # Supprimer l'utilisateur de la base de données
            user_db.session.delete(current_user)
            user_db.session.commit()

            flash("Votre compte a été supprimé avec succès.", "success")
            return redirect(url_for('main.index'))  # Rediriger vers la page d'accueil ou une autre page
        except Exception as e:
            flash(f"Erreur lors de la suppression du compte : {str(e)}", "danger")
            return redirect(url_for('main.index'))  
    else:
        return render_template('delete_account.html') 

# Route pour afficher les produits en fonction du goût
@main_bp.route('/produit', methods=['GET'])
def show_produits():
    """Affiche les produits en fonction du goût sélectionné."""
    gout = request.args.get('gout')  # Récupérer le paramètre 'gout'
    page = int(request.args.get('page', 1))  # Numéro de page, par défaut 1
    per_page = 10  # Nombre de produits par page
    offset = (page - 1) * per_page  # Calculer l'offset pour la pagination

    produits_list = []
    total_pages = 0

    try:
        produits_list, total_count = get_products(gout, per_page, offset)
        total_pages = (total_count // per_page) + (1 if total_count % per_page != 0 else 0)
    except Exception as e:
        print(f"Erreur lors de la récupération des produits : {e}")
        produits_list = []

    return render_template(
        'produits.html',
        produits=produits_list,
        gout=gout,
        page=page,
        total_pages=total_pages
    )

# sans llm affiche les produits recommender + sauvegarder user_id et produit_id dans la table user_produit
# Route pour interroger la base de données ou le système de recherche
@main_bp.route('/query', methods=['POST'])
def query():
    question = request.form.get('question')

    if not question:
        return jsonify({"error": "Veuillez entrer une question."}), 400

    try:
        # Appeler le système de recherche ou le retrieveur
        # Utilisation de la fonction search_for_flavor dans retriever.invoke
        flavors_in_query = search_for_flavor(question)
        response = retriever.invoke(question, filter={"saveur": flavors_in_query})  # À configurer dans votre projet
        
        products = []
        if isinstance(response, list) and all(isinstance(doc, Document) for doc in response):
            for doc in response:
                row_value = doc.metadata.get('row')
                if row_value is not None and row_value < len(df):  # Assurez-vous que row_value est valide
                    nom_produit = df.loc[row_value, 'nom_produit']
                    saveur = df.loc[row_value, 'saveur']
                    img_produit = df.loc[row_value, 'img_produit']
                    # product_id = df.loc[row_value, 'id_produit']  # Récupère l'id_produit du DataFrame
                    product_id = int(df.loc[row_value, 'id_produit'])

                    products.append({
                        'nom_produit': nom_produit,
                        'saveur': saveur,
                        'img_produit': img_produit,
                        'id_produit': product_id 
                    })

                    # Si l'utilisateur est connecté, on sauvegarde la relation dans la table user_produit
                    if current_user.is_authenticated:
                        # Vérifier si la relation existe déjà
                        existing_relation = user_db.session.query(user_produit).filter_by(user_id=current_user.id, product_id=product_id).first()
                        if not existing_relation:  # Si la relation n'existe pas
                            user_product = user_produit.insert().values(user_id=current_user.id, product_id=product_id)
                            user_db.session.execute(user_product)
                            user_db.session.commit()

            return render_template('product_results.html', products=products)
        else:
            return jsonify({"error": "Unexpected response format."}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500




        
# avec llm affiche les produits recommender + sauvegarder user_id et produit_id dans la table user_produit

@main_bp.route('/recommend', methods=['POST'])
@login_required  # Assurez-vous que l'utilisateur est connecté
def recommend():
    question = request.form.get('question')

    
    # Vérifier si la question est vide (Code 400)
    if not question:
        error_message = "Veuillez entrer une question."
        logging.error(f"Erreur 400: {error_message}")
        return render_template('error_page.html', error_message=error_message), 400
    
    retries = 5  # Nombre maximum de tentatives
    backoff_time = 1  # Temps de pause initial (en secondes)

    
    for attempt in range(retries):
        try:
            # Utilisation de la fonction search_for_flavor dans retriever.invoke
            flavors_in_query = search_for_flavor(question)
            # Essayer d'obtenir la réponse
            response = qa_chain.invoke(question, filter={"saveur": flavors_in_query})
            
            docs = retriever.invoke(question)
            for doc in docs:
                print(f"Document ID: {doc.id}, Métadonnées: {doc.metadata}")

            

            id_produit_list = []
            for doc in docs:
                # Accéder à la valeur de id_produit dans les métadonnées
                id_produit = doc.metadata.get("id_produit")
                
                if id_produit is not None:
                    id_produit_list.append(id_produit)
        

            # 🔥 **Insertion des recommandations en base de données**
            new_recommendation = Recommendation(
                question=question,
                response=response,  # JSON attendu
                documents=[doc.page_content for doc in docs]  # Liste des contenus de documents
            )
            user_db.session.add(new_recommendation)
            user_db.session.commit()
            logging.info(f"Valeurs de 'id_produit' extraites : {id_produit_list}")
            logging.info(f"Réponse générée : {response}")
            print("Valeurs de 'id_produit' extraites :", id_produit_list)
            print(docs)
            # Enregistrer les produits consultés par l'utilisateur connecté
            if current_user.is_authenticated:
                for product_id in id_produit_list:
                    # Log de l'ajout de produits
                    logging.info(f"Ajout du produit {product_id} pour l'utilisateur {current_user.id}")
                    # Vérifier si la relation existe déjà
                    existing_relation = user_db.session.query(user_produit).filter_by(
                        user_id=current_user.id, product_id=product_id
                    ).first()

                    if not existing_relation:  # Si la relation n'existe pas, on l'insère
                        user_product = user_produit.insert().values(
                            user_id=current_user.id, product_id=product_id
                        )
                        user_db.session.execute(user_product)

                user_db.session.commit()  # Commit après avoir ajouté tous les produits

            # 🔥 Appel de la fonction SQL pour récupérer les images des produits
            img_produit_values = show_produit(id_produit_list)

            # -----------------------
            # Vérifier les données avant l'écriture dans le CSV
            csv_file_path = './app/recommendations.csv'  
            csv_headers = ['Question', 'Response', 'Document Content']

            # Vérifier si le fichier CSV existe déjà
            file_exists = os.path.isfile(csv_file_path)

            # Vérifier le contenu des données
            csv_data = [{
                'Question': question,
                'Response': response,
                'Document Content': '\n'.join(doc.page_content for doc in docs)
            }]

            logging.info(f"Data to write to CSV: {csv_data}")

            # Ouvrir le fichier CSV en mode 'a' (ajouter)
            try:
                with open(csv_file_path, mode='a', newline='', encoding='utf-8') as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
                    
                    # Écrire les en-têtes seulement si le fichier n'existe pas déjà
                    if not file_exists:
                        writer.writeheader()

                    # Ajouter les nouvelles données
                    writer.writerows(csv_data)
                logging.info(f"Nouvelles données ajoutées au fichier CSV : {csv_file_path}")
            except Exception as e:
                logging.error(f"Erreur lors de l'écriture dans le fichier CSV : {str(e)}")
                error_message = f"Erreur lors de l'écriture dans le fichier CSV : {str(e)}"
                return render_template('error_page.html', error_message=error_message), 500
            #--------------------------


            return render_template(
                'product_results.html',
                recommendation=response,
                img_produit=img_produit_values,
                id_produit_list=id_produit_list
            )

        except HTTPException as http_err:
            # Log de l'erreur HTTP
            logging.error(f"Erreur HTTP: {str(http_err)}")
            # Afficher une page d'erreur spécifique pour les erreurs HTTP
            error_message = f"Erreur HTTP: {str(http_err)}"
            return render_template('error_page.html', error_message=error_message), http_err.code

        except requests.exceptions.RequestException as e:
            # Si une erreur de type 429 est rencontrée
            if e.response and e.response.status_code == 429:
                retry_after = int(e.response.headers.get('Retry-After', backoff_time))  # Attendre le temps indiqué
                logging.warning(f"Quota dépassé, attente de {retry_after} secondes avant de réessayer...")
                time.sleep(retry_after)  # Attendre avant de réessayer
                backoff_time *= 2  # Augmenter exponentiellement le délai pour la prochaine tentative
                continue  # Refaire la requête après l'attente

            # Log de l'erreur générale
            logging.error(f"Erreur inattendue lors de l'appel API : {str(e)}")
            # Afficher une page d'erreur générique pour les autres erreurs
            error_message = f"Une erreur inattendue est survenue : {str(e)}"
            return render_template('error_page.html', error_message=error_message), 500

    # Si le nombre de tentatives est épuisé sans succès
    error_message = "Impossible de récupérer les données après plusieurs tentatives."
    logging.error(error_message)
    return render_template('error_page.html', error_message=error_message), 500


# afficher tous produits recomandés a l'user connecté

@main_bp.route('/user_products/<int:user_id>')
@login_required  # Assurez-vous que l'utilisateur est connecté
# def user_products(user_id):
#     # Récupérer l'utilisateur
#     user = User.query.get_or_404(user_id)
    
    
#     # Appeler la fonction pour récupérer les produits de cet utilisateur
#     produits = get_user_products(user_id)
#     # Passer les product_ids au template
#     return render_template('user_products.html', user=user, produits=produits)

def user_products(user_id):
    # Vérifie que l'ID de l'utilisateur dans l'URL correspond à l'utilisateur connecté
    if current_user.id != user_id:
        flash("Vous n'avez pas accès à ces produits.", "danger")
        return redirect(url_for('auth.login'))  # Redirige vers la page de connexion

    # Si l'utilisateur est authentifié et a le bon ID, récupère les informations de l'utilisateur
    user = User.query.get_or_404(user_id)

    # Appeler la fonction pour récupérer les produits de cet utilisateur
    produits = get_user_products(user_id)

    # Passer les informations au template
    return render_template('user_products.html', user=user, produits=produits)
        