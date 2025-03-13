import streamlit as st
import pandas as pd
import time
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os
import torch
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import subprocess
import logging


torch.classes.__path__ = [os.path.join(torch.__path__[0], torch.classes.__file__)] 
os.environ["STREAMLIT_WATCHER_ENFORCE_POLLING"] = "true"
# Configurer le logger
logging.basicConfig(
    filename="logs/model_performance.log",  # Fichier où les logs seront sauvegardés
    level=logging.INFO,  # Niveau de log (INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Format du log
    datefmt="%Y-%m-%d %H:%M:%S"  # Format de la date
)

#  ---------------------------------------------------------------------------------------------------------------------------------------------------------------
#  ---------------------------------------------------------------------------------------------------------------------------------------------------------------
# Charger le modèle SentenceTransformer
@st.cache_resource
def load_model():
    logging.info("Chargement du modèle SentenceTransformer.")
    return SentenceTransformer('all-MiniLM-L6-v2')

# Charger les données de monitoring
@st.cache_data
def load_data():
    logging.info("Chargement des données de monitoring.")
    df = pd.read_csv("app/rag_eval/monitoring.csv")
    return df
#  ---------------------------------------------------------------------------------------------------------------------------------------------------------------
#  ---------------------------------------------------------------------------------------------------------------------------------------------------------------

# Fonction pour exécuter le script de monitoring
def run_monitoring_script():
    try:
        logging.info("Lancement du script rag_monitoring.py...")
        subprocess.run(["python", "app/rag_eval/rag_monitoring.py"], check=True)
        logging.info("Le script rag_monitoring.py a été exécuté avec succès.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Erreur lors de l'exécution de rag_monitoring.py : {e}")
        st.error("Une erreur est survenue lors de l'exécution du script.")

#  ---------------------------------------------------------------------------------------------------------------------------------------------------------------
#  ---------------------------------------------------------------------------------------------------------------------------------------------------------------

# Initialisation de l'état des alertes dans st.session_state
if "alerts_shown" not in st.session_state:
    st.session_state.alerts_shown = False

# Fonction pour vérifier la latence et la similarité et déclencher des alertes
def check_alerts(df):
    for index, row in df.iterrows():
        # Utiliser l'index comme identifiant unique pour chaque ligne
        unique_id = index
        
        # Vérifier la latence
        if row["Latency (ms)"] > 30000:  # Latence supérieure à 30 secondes
            log_message = f"ALERTE: Latence élevée ({row['Latency (ms)']} ms) pour l'index {unique_id}"
            logging.warning(log_message)  # Log dans le fichier
            st.warning(f"ALERTE: La latence de {unique_id} dépasse les 30 secondes.")  # Affichage dans l'interface Streamlit
            st.text(log_message)  # Affichage du message d'alerte dans Streamlit

        # Vérifier la similarité
        if row["Similarity Query-Response"] < 0.6:  # Similarité inférieure à 0.7
            log_message = f"ALERTE: Similarité faible ({row['Similarity Query-Response']}) pour l'index {unique_id}"
            logging.warning(log_message)  # Log dans le fichier
            # st.warning(f"ALERTE: La similarité de {unique_id} est inférieure à 0.6.")  # Affichage dans l'interface Streamlit
            st.text(log_message)  
            st.dataframe(df.loc[index, ["Query", "Response", "Source"]])
#  ---------------------------------------------------------------------------------------------------------------------------------------------------------------
#  ---------------------------------------------------------------------------------------------------------------------------------------------------------------


df = load_data()
st.dataframe(df, width=1000)

#  ---------------------------------------------------------------------------------------------------------------------------------------------------------------
#  ---------------------------------------------------------------------------------------------------------------------------------------------------------------

# Bouton pour relancer le script et actualiser les données
if st.button("Mettre à jour les données de monitoring"):
    run_monitoring_script()
    st.success("Les données de monitoring ont été mises à jour avec succès.")




#  ---------------------------------------------------------------------------------------------------------------------------------------------------------------
#  ---------------------------------------------------------------------------------------------------------------------------------------------------------------


# Calcul des métriques principales
best_score_query_response = round(df["Similarity Query-Response"].max(), 2)
worst_score_query_response = round(df["Similarity Query-Response"].min(), 2)
average_score_query_response = round(df["Similarity Query-Response"].mean(), 2)

best_score_response_source = round(df["Similarity Response-Source"].max(), 2)
worst_score_response_source = round(df["Similarity Response-Source"].min(), 2)
average_score_response_source = round(df["Similarity Response-Source"].mean(), 2)

average_latency = round(df["Latency (ms)"].mean(), 2)
#  ---------------------------------------------------------------------------------------------------------------------------------------------------------------
#  ---------------------------------------------------------------------------------------------------------------------------------------------------------------

# Affichage dans le dashboard Streamlit
st.title("Dashboard de Monitoring du Modèle")

# Cartes des scores
col1, col2 = st.columns(2)
with col1:
    st.markdown(f"""
    <div style="background-color: #000000; padding: 20px; border-radius: 10px; border: 2px solid #ffffff; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
        <h4 style="color: #4CAF50;">Meilleur score Similarity Query-Response</h4>
        <h5 style="color: #ffffff;">{best_score_query_response}</h5>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background-color: #000000; padding: 20px; border-radius: 10px; border: 2px solid #ffffff; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
        <h4 style="color: #f39c12;">Meilleur score Similarity Response-Source</h4>
        <h5 style="color: #ffffff;">{best_score_response_source}</h5>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="background-color: #000000; padding: 20px; border-radius: 10px; border: 2px solid #ffffff; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
        <h4 style="color: #e74c3c;">Pire score Similarity Query-Response</h4>
        <h5 style="color: #ffffff;">{worst_score_query_response}</h5>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background-color: #000000; padding: 20px; border-radius: 10px; border: 2px solid #ffffff; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
        <h4 style="color: #e74c3c;">Pire score Similarity Response-Source</h4>
        <h5 style="color: #ffffff;">{worst_score_response_source}</h5>
    </div>
    """, unsafe_allow_html=True)

# Cartes des moyennes
col3, col4 = st.columns(2)
with col3:
    st.markdown(f"""
    <div style="background-color: #000000; padding: 20px; border-radius: 10px; border: 2px solid #ffffff; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
        <h4 style="color: #3498db;">Moyenne Similarity Query-Response</h4>
        <h5 style="color: #ffffff;">{average_score_query_response}</h5>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background-color: #000000; padding: 20px; border-radius: 10px; border: 2px solid #ffffff; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
        <h4 style="color: #3498db;">Moyenne Similarity Response-Source</h4>
        <h5 style="color: #ffffff;">{average_score_response_source}</h5>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style="background-color: #000000; padding: 20px; border-radius: 10px; border: 2px solid #ffffff; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); margin-bottom: 20px;">
        <h4 style="color: #9b59b6;">Latence moyenne (ms)</h4>
        <h5 style="color: #ffffff;">{average_latency}</h5>
    </div>
    """, unsafe_allow_html=True)
#  ---------------------------------------------------------------------------------------------------------------------------------------------------------------
#  ---------------------------------------------------------------------------------------------------------------------------------------------------------------

# Graphiques
# Distribution des scores Similarity Query-Response
st.subheader("Distribution des scores Similarity Query-Response")
fig_query_response = px.histogram(df, x="Similarity Query-Response", nbins=20, title="Distribution des scores Query-Response")
st.plotly_chart(fig_query_response)

# Distribution des scores Similarity Response-Source
st.subheader("Distribution des scores Similarity Response-Source")
fig_response_source = px.histogram(df, x="Similarity Response-Source", nbins=20, title="Distribution des scores Response-Source")
st.plotly_chart(fig_response_source)

# Graphique de la latence
st.subheader("Distribution des latences (ms)")
fig_latency = px.histogram(df, x="Latency (ms)", nbins=20, title="Distribution des latences")
st.plotly_chart(fig_latency)

# Graphiques avec Seaborn (si vous préférez une visualisation différente)
st.subheader("Seaborn - Similarity Query-Response vs Latence")
fig, ax = plt.subplots()
sns.scatterplot(x=df["Similarity Query-Response"], y=df["Latency (ms)"], ax=ax)
ax.set_title("Similarity Query-Response vs Latence")
st.pyplot(fig)

# Affichage de la répartition globale des scores avec un graphique en boîte
st.subheader("Boîte à moustaches des scores de Similarité")
fig_boxplot = plt.figure(figsize=(10, 6))
sns.boxplot(data=df[["Similarity Query-Response", "Similarity Response-Source"]])
plt.title("Boîte à moustaches des scores de Similarité")
st.pyplot(fig_boxplot)


#  ---------------------------------------------------------------------------------------------------------------------------------------------------------------
#  ---------------------------------------------------------------------------------------------------------------------------------------------------------------


# Vérifier les alertes sur les données
st.title("Vérification des alertes")
# Ajouter un bouton pour déclencher l'affichage des alertes
if st.button('Afficher / Cacher toutes les alertes'):
    st.session_state.alerts_shown = not st.session_state.alerts_shown

# Si les alertes doivent être affichées, exécuter la fonction de vérification
if st.session_state.alerts_shown:
    check_alerts(df)