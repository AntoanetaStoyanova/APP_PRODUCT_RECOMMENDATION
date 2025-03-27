import time
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os

# Charger le modèle SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

# Charger les données
df = pd.read_csv("app/recommendations.csv")

# Récupérer les valeurs des colonnes
queries = df['Question'].tolist()
responses = df['Response'].tolist()
sources = df['Source'].tolist()



# Initialiser une liste pour stocker les résultats
results = []



for query, response, source in zip(queries, responses, sources):
    start_time = time.time()  

    # Encodage des textes
    embeddings = model.encode([query, response, source])

    # Calcul des similarités
    similarity_query_response = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    similarity_response_source = cosine_similarity([embeddings[1]], [embeddings[2]])[0][0]

    end_time = time.time()  
    latency = (end_time - start_time) * 1000  

    # Ajouter les résultats avec timestamp
    results.append([time.strftime("%Y-%m-%d %H:%M:%S"), 
                    query, response, source, similarity_query_response, 
                    similarity_response_source, latency])



# Sauvegarde dans un CSV
csv_path = "app/rag_eval/monitoring.csv"
columns = ["Timestamp", "Query", "Response", "Source", "Similarity Query-Response", "Similarity Response-Source", "Latency (ms)"]

# Vérifier si le fichier existe
if not os.path.exists(csv_path):
    pd.DataFrame(results, columns=columns).to_csv(csv_path, index=False)
else:
    pd.DataFrame(results, columns=columns).to_csv(csv_path, mode='a', header=False, index=False)

print("Données de monitoring mises à jour dans monitoring.csv")
