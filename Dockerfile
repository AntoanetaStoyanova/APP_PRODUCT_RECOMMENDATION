# Utiliser l'image Python 3.12 légère
FROM python:3.12-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système nécessaires (par exemple pour psycopg2, etc.)
RUN apt-get update && apt-get install -y gcc libpq-dev

# Copier uniquement requirements.txt en premier (optimisation du cache)
COPY requirements.txt ./

# Installer les dépendances depuis requirements.txt
RUN pip install -r requirements.txt

# Copier le reste des fichiers de l'application
COPY . .

# Définir la commande de lancement
CMD ["python", "run.py"]
