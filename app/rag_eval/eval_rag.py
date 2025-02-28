import time
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Charger le modèle SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

# Je recupere le query de l'user, la reponse et la source de l'application dans un csv afin d'évaluer le rag avec bulk eval
df = pd.read_csv("app/recommendations.csv", delimiter=";")


# recuperer les valeurs des colonnes dans des listes python
queries = df['Question'].tolist()
responses = df['Response'].tolist()
sources = df['Document Content'].tolist()


# Initialiser une liste pour stocker les résultats
results = []

# Boucle d'évaluation
for query, response, source in zip(queries, responses, sources):
    start_time = time.time()  # Début du chronomètre

    # Encodage des textes
    embeddings = model.encode([query, response, source])

    # Calcul des similarités
    similarity_query_response = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    similarity_response_source = cosine_similarity([embeddings[1]], [embeddings[2]])[0][0]

    end_time = time.time()  # Fin du chronomètre
    latency = (end_time - start_time) * 1000  # Latence en ms

    # Ajouter les résultats à la liste
    results.append([query, response, source, similarity_query_response, similarity_response_source, latency])

# Créer un DataFrame Pandas
df = pd.DataFrame(results, columns=["Query", "Response", "Source", "Similarity Query-Response", "Similarity Response-Source", "Latency (ms)"])

# Afficher les résultats
print(df)

# Vérification d'un seuil de performance (exemple)
assert df["Similarity Query-Response"].mean() > 0.5, "⚠️ La similarité moyenne Query-Response est trop faible !"
assert df["Similarity Response-Source"].mean() > 0.5, "⚠️ La similarité moyenne Response-Source est trop faible !"
assert df["Latency (ms)"].mean() < 500, "⚠️ La latence moyenne est trop élevée !"