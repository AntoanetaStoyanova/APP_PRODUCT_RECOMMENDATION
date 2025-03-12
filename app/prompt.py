# from langchain.prompts import ChatPromptTemplate

# prompt_template = """
# You are an assistant for question-answering tasks.
# Use the following pieces of retrieved context to answer the question.
# If you don't know the answer, just say that you don't know.

# Question: {question}

# Context: {context}

# Answer:
# """

# prompt = ChatPromptTemplate.from_template(prompt_template)

from langchain.prompts import ChatPromptTemplate

prompt_template = """
Vous êtes un assistant pour des tâches de recommandation de produits.
Utilisez les informations suivantes sur les produits pour répondre à la question de l'utilisateur.
Si vous ne connaissez pas la réponse, dites simplement que vous ne savez pas.

Question : {question}

Contexte (produits) : {context}

Réponse : 
"""

prompt = ChatPromptTemplate.from_template(prompt_template)