import json
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv  # <--- AJOUT : Importer dotenv

# Charger les variables du fichier .env situé à la racine
load_dotenv() 

def run_agent(raw_json_path, schema_path, output_path):
    # Initialisation du client (Maintenant os.environ trouvera la clé)
    api_key = os.environ.get("GOOGLE_API_KEY")
    
    if not api_key:
        raise ValueError("❌ Erreur : GOOGLE_API_KEY non trouvée. Vérifiez votre fichier .env")

    client = genai.Client(api_key=api_key)

    with open(raw_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        text_to_analyze = data.get("text", "")

    # Ton Prompt (Inchangé)
    prompt = f"""
Tu es un expert en flux de données SAP et en Expressions Régulières. Ton rôle est de générer un JSON structuré.

RÈGLES DE TRADUCTION UNIVERSELLES POUR 'pattern' :
1. PRÉFIXES : Si le document indique un préfixe (ex: "Commence par 004", "Débute par MIX_", "Préfixe FID4_"), crée une regex débutant par ce texte. 
   Tu dois soustraire la longueur du préfixe de la longueur totale (max_length) pour définir le reste {{n}}.
   Exemple : "FID4_" sur 12 car. -> "^FID4_[0-9]{{8}}$"

2. CHOIX : Si le document propose un choix (ex: "5 ou 6"), utilise les crochets [ ].
   Exemple : "^[56][0-9]{{9}}$"

3. DATES : Si c'est une date AAAAMMJJ -> "^(19|20)[0-9]{{6}}$"

4. PAR DÉFAUT : Si aucune règle n'est précisée, génère une regex de chiffres purs basée sur max_length.
   Exemple : max_length 5 -> "^[0-9]{{5}}$"

POUR CHAQUE COLONNE :
- name : Nom technique
- type : VARCHAR, INTEGER ou DECIMAL
- max_length : Nombre entier
- mandatory : "OUI" ou "NON"
- pattern : LA REGEX GÉNÉRÉE (commençant par ^ et finissant par $)
- example : L'exemple du document

DOCUMENT À ANALYSER : 
{text_to_analyze}
"""

    try:
        # Note : gemini-2.0-flash est le dernier modèle stable. 
        # Si gemini-2.5-flash n'est pas encore dispo sur ton compte, 
        # tu peux redescendre à 'gemini-2.0-flash' ou 'gemini-1.5-flash'.
        response = client.models.generate_content(
            model='gemini-2.0-flash', 
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type='application/json',
                temperature=0.1
            )
        )
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(response.text)
            
        print(f"✅ Analyse et structuration Regex terminées : {output_path}")
            
    except Exception as e:
        print(f"❌ Erreur Gemini : {e}")
        raise e