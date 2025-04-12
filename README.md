# Recommandation d'e-liquides basée sur les goûts utilisateurs

## Introduction:

Ce projet vise à faciliter la recherche et la recommandation de produits e-liquides en fonction des goûts de l’utilisateur. Il s'agit d'une application locale développée principalement en Python, intégrant le web scraping, le traitement de données, l'intelligence artificielle et une base de données PostgreSQL pour offrir une expérience personnalisée.

## Fonctionnalités principales

- Récupération de données via le scraping du site spécialisé [Aromes et Liquides](https://www.aromes-et-liquides.fr/).
- Nettoyage, structuration et stockage des données dans une base de données PostgreSQL.
- Interface utilisateur simple pour obtenir des recommandations personnalisées basées sur les préférences de goût de l'utilisateur.
- Utilisation d'un modèle RAG intégré pour améliorer les recommandations.

- Création et connexion à un compte utilisateur.
- Choix d’un goût préféré (fruit, menthe, dessert, etc.) pour filtrer les produits.
- Visualisation des produits associés à un goût ou une demande spécifique.
- Possibilité d’entrer une requête libre du type : "Je cherche un produit au citron vert".
- Réponse générée de manière intelligente grâce au modèle Azure OpenAI.


## Technologies Utilisées

Le projet a été entièrement développé en **Python** avec l’utilisation des bibliothèques telles que0 :

- **BeautifulSoup** & **Selenium** : pour le scraping web des données produits.
- **Requests** : pour les appels HTTP aux pages web.
- **Pandas** : pour la manipulation et la visualisation des données.
- **Logging** : pour tracer les événements importants de l'application.
- **FAISS** : pour l’indexation vectorielle des embeddings générés.
- **ChatPromptTemplate** *(Langchain)* : pour générer dynamiquement des prompts pour le modèle de langage.
- **Flask** : pour la création de l’application web et la définition des routes.
- **SQLAlchemy** : pour la gestion de la base de données et des tables.
- **AzureChatOpenAI** : pour l’utilisation du modèle GPT via Azure OpenAI.
etc...


## Prérequis

- **Python** version : `3.10.6`
- `pip` ou `pipenv` installé localement

---

## Installation du projet
```bash
git clone https://github.com/AntoanetaStoyanova/APP_PRODUCT_RECOMMENDATION.git
cd APP_PRODUCT_RECOMMENDATION
```

### Option 1 : avec Pipenv
```bash
pip install pipenv
pipenv install
pipenv shell
```
### Option 2 : avec pip
```bash
pip install -r requirements.txt
```

## Structure du projet
```powershell
tree /F
```
```powershell
.
│   .env
│   .gitignore
│   config.py
│   Pipfile
│   Pipfile.lock
│   requirements.txt
│   run.py
│
├───.github
│   └───workflows
│           monitoring_metrics.yml
│           test.yml
│           test_csv.yml
│           test_rag.yml
│
├───app
│   │   db.py
│   │   embeddings.py
│   │   forms.py
│   │   llm.py
│   │   llm_connection.py
│   │   models.py
│   │   prompt.py
│   │   rag_csv.csv
│   │   README.md
│   │   recommendations.csv
│   │   retriever.py
│   │   routes.py
│   │   utils.py
│   │   vectorstore.py
│   │   __init__.py
│   │
│   ├───faiss_vector_store
│   │       index.faiss
│   │       index.pkl
│   │
│   ├───instance
│   │       database.db
│   │
│   ├───rag_eval
│   │       eval_rag.py
│   │       eval_utils.py
│   │       monitoring.csv
│   │       monitoring.py
│   │       QA_test_samples.csv
│   │       rag.ipynb
│   │       rag_eval.ipynb
│   │       rag_monitoring.py
│   │
│   ├───static
│   │   └───gout_img
│   │           age-limit-18-icon.png
│   │           boisson.png
│   │           classique.png
│   │           dessert.png
│   │           frais.png
│   │           fruit.png
│   │           menthes.png
│   │           user.png
│   │
│   ├───templates
│   │       accueil.html
│   │       dashboard.html
│   │       delete_account.html
│   │       error_page.html
│   │       index.html
│   │       index_produit.html
│   │       login.html
│   │       main.html
│   │       product_results.html
│   │       produits.html
│   │       recherche.html
│   │       register.html
│   │       resultats_recherche.html
│   │       test.html
│   │       user_account.html
│   │       user_products.html
│   │
│
├───instance
├───logs
│       llm_connection.log
│       model_performance.log
│
├───RGBD
│   │   tables.ipynb
│   │
│   └───table_produits
│           produits.csv
│
├───scrap_final
│   │   produits_eliquide.csv
│   │   produits_eliquide_avec_details.csv
│   │   produits_eliquide_filtrés.csv
│   │   scrapboissonA&L.ipynb
│   │   scrapclassiqueA&L.ipynb
│   │   scrapdessertA&L.ipynb
│   │   scrapfraisA&L.ipynb
│   │   scrapfruitA&L.ipynb
│   │   scrapfruitpetitvap.ipynb
│   │   scrapmenthesA&L.ipynb
│   │   traitement.ipynb
│   │
│   ├───csv_clean
│   │       A&L.csv
│   │
│   ├───donnees_scrappes
│   │       produits_boisson_A&L.csv
│   │       produits_classique_A&L.csv
│   │       produits_dessert_A&L.csv
│   │       produits_frais_A&L.csv
│   │       produits_fruit_A&L.csv
│   │       produits_menthe_A&L.csv
│   │
│   └───links
│           link_produits_boissons_a&i.csv
│           link_produits_classiques_a&i.csv
│           link_produits_desserts_a&i.csv
│           link_produits_frais_a&i.csv
│           link_produits_fruits_a&i.csv
│           link_produits_menthes_a&i.csv
│
├───tests
│       test_azure_chat_openai.py
│       test_csv.py
│       test_db.py
│       test_py_config.py
│       test_py_db.py
│       test_py_produit.py
│       test_py_query.py
│       test_py_routes.py
│       test_retriever.py
│       test_routes.py
│       test_routes_api.py
│       test_routes_recommend.py
│       test_vectorestore.py
│       __init__.py

```


## Connection avec la DB

- configurer la connection 
```bash
psql -h localhost -U postgres -d postgres
```
* Création de la table produit

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
    id_produit INT PRIMARY KEY
);

* envoyer les données scrapper dans la table produits

\COPY public.produits(url, nom_produit, img_produit, prix_produit, contenance, pg_vg, origine, frais, surbooste, saveur, description, brand, gout, info_brand, id_produit)
FROM 'RGBD/table_produits/produits.csv' DELIMITER ',' CSV HEADER;

- \dt (pour voir table)



## Exécution

```bash
pipenv shell
python run.py
```