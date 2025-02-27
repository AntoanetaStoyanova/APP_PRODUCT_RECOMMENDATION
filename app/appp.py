import os
import logging
import psycopg2
import numpy as np
from flask import Flask, render_template, request, jsonify
import pandas as pd
import sqlite3 







app = Flask(__name__)




# Connexion à la base de données PostgreSQL
POSTGRESQL_URI = 'postgresql://postgres:Kandinsky_95@localhost:5432/postgres'
try:
    connection = psycopg2.connect(POSTGRESQL_URI)
    print("Connexion à la base de données PostgreSQL réussie!")
except psycopg2.OperationalError as e:
    print(f"Erreur de connexion : {e}")




@app.route("/", methods=["GET"])
def show_gouts():
    """Affiche les goûts disponibles sous forme d'images cliquables."""
    return render_template('index.html')

@app.route("/produit", methods=["GET"])
def show_produits():
    """Affiche les produits en fonction du goût sélectionné."""
    gout = request.args.get('gout')  # Récupérer le paramètre 'gout'
    page = int(request.args.get('page', 1))  # Récupérer le numéro de page, par défaut 1
    per_page = 9  # Nombre de produits par page
    offset = (page - 1) * per_page  # Calculer l'offset pour la pagination

    produits_list = []
    total_pages = 0

    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute('SELECT img_produit, nom_produit FROM public.produits WHERE gout = %s LIMIT %s OFFSET %s;',
                               (gout, per_page, offset))
                rows = cursor.fetchall()
                for row in rows:
                    produits_list.append({
                        'img_produit': row[0],
                        'nom_produit': row[1]
                    })
                cursor.execute('SELECT COUNT(*) FROM public.produits WHERE gout = %s;', (gout,))
                total_count = cursor.fetchone()[0]
                total_pages = (total_count // per_page) + (1 if total_count % per_page != 0 else 0)
    except Exception as e:
        print(f"Erreur lors de la récupération des produits : {e}")
        produits_list = []

    return render_template('produits.html', produits=produits_list, gout=gout, page=page, total_pages=total_pages)



if __name__ == "__main__":
    app.run(debug=True)




