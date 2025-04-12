put donnee dans base de donnees
terminal
psql -h localhost -U postgres -d postgres

CREATE TABLE IF NOT EXISTS public.produits (
    url VARCHAR,
    nom_produit VARCHAR,
    img_produit VARCHAR,
    prix_produit FLOAT,
    contenance VARCHAR,
    pg_vg VARCHAR,
    origine VARCHAR,
    frais VARCHAR,
    surbooste VARCHAR,
    saveur VARCHAR,
    description VARCHAR,
    brand VARCHAR,
    gout VARCHAR,
    info_brand VARCHAR,
    id_produit INT
);
faut dire que id_produit est clé unique 
ALTER TABLE public.produits ADD PRIMARY KEY (id_produit);


\COPY public.produits(url, nom_produit, img_produit, prix_produit, contenance, pg_vg, origine, frais, surbooste, saveur, description, brand, gout, info_brand, id_produit)
FROM 'RGBD/table_produits/produits.csv' DELIMITER ',' CSV HEADER;

\dt pour voir table

from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

# Configuration de la connexion à PostgreSQL
POSTGRESQL_URI = 'postgresql://postgres:Kandinsky_95@localhost:5432/postgres'

try:
    # Connexion à la base de données PostgreSQL
    connection = psycopg2.connect(POSTGRESQL_URI)
    print("Connexion à la base de données PostgreSQL réussie!")
except psycopg2.OperationalError as e:
    print(f"Erreur de connexion : {e}")

@app.route("/produit")
def show_produit():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT nom_produit FROM public.pdt;')

            produits = cursor.fetchall()
            produits_list = [produit[0] for produit in produits]  # Extracting product names from fetchall result
    return render_template('produits.html', produits=produits_list)

if __name__ == '__main__':
    app.run(debug=True)


----------------

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2

app = FastAPI()

# Configuration de la connexion à PostgreSQL
POSTGRESQL_URI = 'postgresql://postgres:Kandinsky_95@localhost:5432/postgres'

try:
    # Connexion à la base de données PostgreSQL
    connection = psycopg2.connect(POSTGRESQL_URI)
    print("Connexion à la base de données PostgreSQL réussie!")
except psycopg2.OperationalError as e:
    print(f"Erreur de connexion : {e}")

# Pydantic model pour valider les données de la requête
class GoutRequest(BaseModel):
    gout: str

@app.get("/produit")
def get_produits(gout: str):
    """ Récupère les produits correspondant au goût spécifié """
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT nom_produit, gout FROM public.pdt WHERE gout = %s;', (gout,))
            produits = cursor.fetchall()

            if not produits:
                raise HTTPException(status_code=404, detail="Aucun produit trouvé pour ce goût")

            # Création d'une liste de produits
            produits_list = [{"nom_produit": produit[0], "gout": produit[1]} for produit in produits]
            
    return {"produits": produits_list}

@app.post("/produit")
def post_produits(gout_request: GoutRequest):
    """ Recevoir un goût dans le corps de la requête et retourner les produits """
    gout = gout_request.gout
    with connection:
        with connection.cursor() as cursor:
            cursor.execute('SELECT nom_produit, gout FROM public.pdt WHERE gout = %s;', (gout,))
            produits = cursor.fetchall()

            if not produits:
                raise HTTPException(status_code=404, detail="Aucun produit trouvé pour ce goût")

            # Création d'une liste de produits
            produits_list = [{"nom_produit": produit[0], "gout": produit[1]} for produit in produits]
            
    return {"produits": produits_list}

# uvicorn app:app --host localhost --port 8000 --reload
--------

from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import psycopg2

# Initialisation de l'application FastAPI
app = FastAPI()

# Configuration de la connexion à PostgreSQL
POSTGRESQL_URI = "postgresql://postgres:Kandinsky_95@localhost:5432/postgres"

try:
    # Connexion à PostgreSQL
    connection = psycopg2.connect(POSTGRESQL_URI)
    print("Connexion réussie à la base de données PostgreSQL!")
except psycopg2.OperationalError as e:
    print(f"Erreur de connexion à PostgreSQL: {e}")

# Configuration de Jinja2 pour le dossier des templates
templates = Jinja2Templates(directory="templates")

@app.get("/produit", response_class=HTMLResponse)
def get_produits(gout: str, request: Request):
    """
    Endpoint pour afficher les produits correspondant au goût donné.
    """
    with connection:
        with connection.cursor() as cursor:
            # Requête pour récupérer les produits correspondant au goût
            cursor.execute(
                "SELECT nom_produit, gout, img_produit FROM public.pdt WHERE gout = %s;",
                (gout,)
            )
            produits = cursor.fetchall()

            # Vérification si aucun produit n'est trouvé
            if not produits:
                raise HTTPException(status_code=404, detail="Aucun produit trouvé pour ce goût.")

            # Transformer les résultats en une liste de dictionnaires
            produits_list = [
                {"nom_produit": produit[0], "gout": produit[1], "img_produit": produit[2]}
                for produit in produits
            ]

    # Retourner la page HTML avec les produits
    return templates.TemplateResponse(
        "produits.html",
        {"request": request, "produits": produits_list, "gout": gout}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)





regarde les correction de test.py 
good model model_openai.ipynb


run python run.py




user logging 
https://www.youtube.com/watch?v=71EU8gnZqZQ
user get to see it's search ( produit) 


table user ( id, username, password)
psql -h localhost -U postgres -d postgres
\dt
SELECT * FROM "user" WHERE username = 'coco';
\q


ALTER TABLE users ADD COLUMN consent BOOLEAN DEFAULT FALSE;
test - pytest tests/test_vectoristore.py et pytest tests/test_azure_chat_openai.py