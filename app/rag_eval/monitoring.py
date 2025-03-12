import streamlit as st
import pandas as pd
import plotly.express as px

# Charger les données de monitoring
csv_path = "app/rag_eval/monitoring.csv"
df = pd.read_csv(csv_path)

# Interface Streamlit
st.title("📊 Monitoring du LLM RAG")

# Afficher les données sous forme de tableau interactif
st.dataframe(df)
# Convertir la colonne Timestamp en format datetime
df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# Interface Streamlit
st.title("📊 Monitoring du LLM RAG")
st.markdown("Analyse des similarités et de la latence du modèle.")

# Afficher les données brutes
st.subheader("📂 Données de monitoring")
st.dataframe(df)

# 📈 **1️⃣ Analyse des Similarités**
st.subheader("🔍 Évolution des Similarités")

# Courbe des similarités
fig_sim = px.line(df, x="Timestamp", 
                  y=["Similarity Query-Response", "Similarity Response-Source"],
                  labels={"value": "Score de Similarité"},
                  title="Évolution des Scores de Similarité")
st.plotly_chart(fig_sim)

# Histogramme des similarités
fig_hist_sim = px.histogram(df, x=["Similarity Query-Response", "Similarity Response-Source"],
                            title="Distribution des Scores de Similarité", barmode="overlay")
st.plotly_chart(fig_hist_sim)

# 📊 **2️⃣ Analyse de la Latence**
st.subheader("⏳ Analyse de la Latence")

# Courbe d'évolution de la latence
fig_latency = px.line(df, x="Timestamp", y="Latency (ms)", 
                      title="Évolution de la Latence (ms)",
                      labels={"Latency (ms)": "Latence en millisecondes"})
st.plotly_chart(fig_latency)

# Histogramme de la latence
fig_hist_latency = px.histogram(df, x="Latency (ms)", 
                                title="Distribution de la Latence",
                                nbins=20, opacity=0.7)
st.plotly_chart(fig_hist_latency)

# 📊 **3️⃣ Statistiques Globales**
st.subheader("📊 Statistiques Globales")

col1, col2, col3 = st.columns(3)

col1.metric("🔹 Moyenne Similarité Q-R", f"{df['Similarity Query-Response'].mean():.2f}")
col2.metric("🔹 Moyenne Similarité R-S", f"{df['Similarity Response-Source'].mean():.2f}")
col3.metric("⏳ Latence Moyenne (ms)", f"{df['Latency (ms)'].mean():.2f} ms")

# Bouton pour recharger les données
if st.button("🔄 Rafraîchir les données"):
    df = pd.read_csv(csv_path)
    st.rerun()  # ✅ Remplace st.experimental_rerun() par st.rerun(

st.write("🚀 Monitoring en temps réel avec Streamlit")
