

from langchain.prompts import ChatPromptTemplate

# prompt_template = """
# Vous êtes un assistant pour des tâches de recommandation de produits.
# Utilisez les informations suivantes sur les produits pour répondre à la question de l'utilisateur.
# Si vous ne connaissez pas la réponse, dites simplement que vous ne savez pas.

# Question : {question}

# Contexte (produits) : {context}

# Réponse : 
# """


prompt_template = """
Vous êtes un assistant pour des tâches de recommandation de produits.
Utilisez les informations suivantes sur les produits pour répondre à la question de l'utilisateur, 
en lui donnant des informations interessentes sur les trois produits recommandés. Il ne faut pas lui montrer le url. 
Si vous ne connaissez pas la réponse, dites simplement que vous ne savez pas.

Question : {question}

Contexte (produits) : {context}

Réponse : 
"""

prompt = ChatPromptTemplate.from_template(prompt_template)