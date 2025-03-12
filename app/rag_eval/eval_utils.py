# evaluation.py
import logging
import time
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import os



# Créer le dossier log s'il n'existe pas
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configurer le logger pour enregistrer dans log/model_performance.log
logging.basicConfig(
    filename=os.path.join(log_dir, 'model_performance.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

# Initialiser le modèle
model = SentenceTransformer('all-MiniLM-L6-v2')

# Fonction de vérification des métriques et de journalisation
def check_and_log(similarity_query_response, latency):
    similarity_threshold = 0.1  # Très bas pour tester
    latency_threshold = 10  # Très bas pour tester

    # Journalisation pour la similarité
    if similarity_query_response < similarity_threshold:
        logging.warning(f"⚠️ La similarité est trop faible : {similarity_query_response:.2f}.")

    # Journalisation pour la latence
    if latency > latency_threshold:
        logging.error(f"❌ La latence est trop élevée : {latency:.2f} ms.")

# Fonction d'évaluation et de sauvegarde des résultats
def run_evaluation(DATA_PATH, CSV_PATH):
    """Exécute l'évaluation et met à jour le fichier CSV."""
    if not os.path.exists(DATA_PATH):
        logging.error("❌ Le fichier recommendations.csv est introuvable !")
        return

    # Charger les données
    df = pd.read_csv(DATA_PATH)
    queries = df['Question'].tolist()
    responses = df['Response'].tolist()
    sources = df['Document Content'].tolist()

    results = []
    for query, response, source in zip(queries, responses, sources):
        start_time = time.time()

        embeddings = model.encode([query, response, source])
        similarity_query_response = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
        similarity_response_source = cosine_similarity([embeddings[1]], [embeddings[2]])[0][0]

        latency = (time.time() - start_time) * 1000

        # Vérifier et journaliser
        check_and_log(similarity_query_response, latency)

        # Ajouter les résultats à la liste
        results.append([time.strftime("%Y-%m-%d %H:%M:%S"), query, response, source, 
                        similarity_query_response, similarity_response_source, latency])

    # Sauvegarder les résultats
    columns = ["Timestamp", "Query", "Response", "Source", "Similarity Query-Response", "Similarity Response-Source", "Latency (ms)"]
    pd.DataFrame(results, columns=columns).to_csv(CSV_PATH, index=False)

    logging.info("✅ Données de monitoring mises à jour !")

# Exemple d'appel de la fonction

