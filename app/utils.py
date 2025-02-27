import pandas as pd
import re
from langchain.schema import Document
# Fonction pour interroger le retriever et obtenir les produits associés
def query_retriever(question):
    products = []
    # Logique pour interroger le retriever et récupérer les produits
    # Exemple de code:
    # products = df[df['question_column'].str.contains(question)]
    return products

def parse_products(response_text):
    products = []
    products_data = response_text.split("\n\n")

    for product in products_data:
        lines = product.strip().split("\n")

        if len(lines) > 0 and (lines[0].startswith(("1.", "2.", "3.")) or "**" in lines[0]):
            name = lines[0].strip().replace("**", "").lstrip("1234567890. ")
            products.append({'nom_produit': name})

    print("Produits extraits:", products)
    return products

# Fonction pour extraire les saveurs de la requête et les rechercher dans les résultats
def extract_flavors_from_query(query):
    """
    Cette fonction extrait les saveurs présentes dans la requête `query`
    et retourne une liste des saveurs trouvées parmi celles définies dans `flavor_list`.
    """
    # Liste des saveurs disponibles
    flavor_list = ["cassis", "lime", "fraise", "menthe", "mangue", "pêche"]

    found_flavors = []
    
    # Pour chaque saveur de la liste, vérifier si elle est mentionnée dans la requête
    for flavor in flavor_list:
        if re.search(rf'\b{flavor}\b', query, re.IGNORECASE):
            found_flavors.append(flavor)

    return found_flavors


# Fonction pour interroger le vecteur et récupérer les saveurs associées à la requête
def search_for_flavor(query):
    # Extraire les saveurs mentionnées dans la requête
    flavors_in_query = extract_flavors_from_query(query)

    # Afficher uniquement les saveurs extraites
    print(f"Saveurs extraites de la requête : {flavors_in_query}")

    # Retourner les saveurs extraites sous forme de chaîne, séparées par des virgules
    return ", ".join(flavors_in_query)


# # Fonction pour ajouter des métadonnées aux documents existants
# def add_metadata_to_documents(documents, csv_path):
#     modified_documents = []
    
#     # Charger le CSV pour ajouter des informations supplémentaires
#     df = pd.read_csv("../../RGBD/table_produits/produits.csv")
    
#     for index, row in df.iterrows():
#         # Récupérer le document original
#         document = documents[index]  # Assurez-vous que l'index correspond à la ligne dans le CSV
#         modified_documents = []
#         for index, row in df.iterrows():
#             metadata = documents[index].metadata
#             metadata["row"] = index
#             # Ajouter l'ID du produit aux métadonnées
#             if "id_produit" in row:
#                 metadata["id_produit"] = row["id_produit"]
            
#             # Ajouter la saveur si elle existe
#             if "saveur" in row:
#                 metadata["saveur"] = str(row["saveur"])
        
#         # Créer un nouveau document avec les métadonnées mises à jour
#         modified_document = Document(page_content=document.page_content, metadata=metadata)
#         modified_documents.append(modified_document)

#     return modified_documents




def add_metadata_to_documents(documents):
    """Ajoute des métadonnées aux documents existants en récupérant les informations du contenu du document lui-même."""
    
    modified_documents = []

    for index, document in enumerate(documents):
        metadata = document.metadata.copy()  # Copier les métadonnées existantes
        metadata["row"] = index  # Ajouter l'index du document
        
        # Tenter d'extraire les métadonnées à partir du contenu du document
        try:
            df = pd.read_csv(document.metadata["source"])  # Récupérer le CSV depuis le document
            row = df.iloc[index]  # Sélectionner la ligne correspondant au document

            if "id_produit" in row:
                metadata["id_produit"] = row["id_produit"]
            
            if "saveur" in row:
                metadata["saveur"] = str(row["saveur"])

        except Exception as e:
            print(f"⚠️ Erreur lors de l'ajout des métadonnées au document {index} : {e}")

        # Créer un nouveau document avec les métadonnées mises à jour
        modified_document = Document(page_content=document.page_content, metadata=metadata)
        modified_documents.append(modified_document)

    print(f"✅ Métadonnées ajoutées à {len(modified_documents)} documents.")
    return modified_documents
