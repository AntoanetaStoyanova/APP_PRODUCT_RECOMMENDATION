# tests/test_config.py

import os
from app.config import Config

def test_postgresql_uri():
    # Vérifiez si l'URI de la base de données est correctement chargée
    assert Config.POSTGRESQL_URI == 'postgresql://postgres:Kandinsky_95@localhost:5432/postgres'
