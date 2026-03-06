import csv
import json
import os
import random
import string
import re
from datetime import date, timedelta

def generate_from_regex(pattern, max_len):
    """Moteur universel : Décompose la Regex pour reconstruire la donnée."""
    if not pattern or not isinstance(pattern, str) or not pattern.startswith("^"):
        return "".join(random.choices(string.digits, k=max_len))

    # --- 1. GESTION DES DATES ---
    if "(19|20)" in pattern or "AAAAMMJJ" in pattern.upper():
        start_date = date(1995, 1, 1)
        target_date = start_date + timedelta(days=random.randint(0, 11000))
        return target_date.strftime("%Y%m%d")

    # --- 2. EXTRACTION DU PRÉFIXE DYNAMIQUE (ex: FID4_, MIX_, 004) ---
    prefix = ""
    prefix_match = re.search(r"\^([^\[\{]+)", pattern)
    if prefix_match:
        prefix = prefix_match.group(1)

    # --- 3. GESTION DES CLASSES (ex: [56]) ---
    char_class_val = ""
    if not prefix:
        class_match = re.search(r"\[([a-zA-Z0-9-]+)\]", pattern)
        if class_match:
            choices = class_match.group(1).replace("-", "")
            char_class_val = random.choice(list(choices))

    # --- 4. CALCUL DE LA LONGUEUR RESTANTE ---
    len_match = re.search(r"\{(\d+)\}", pattern)
    if len_match:
        needed = int(len_match.group(1))
    else:
        current_len = len(prefix) + len(char_class_val)
        needed = max(0, max_len - current_len)

    # --- 5. GÉNÉRATION DU CORPS ---
    pool = string.digits
    if "A-Z" in pattern or "a-z" in pattern:
        pool = string.ascii_uppercase + string.digits

    body = "".join(random.choices(pool, k=needed))
    
    # --- 6. ASSEMBLAGE ET NETTOYAGE ---
    result = prefix + char_class_val + body
    return result[:max_len]

def generate_dynamic_value(col):
    """Récupère le pattern du JSON et lance la génération."""
    if not isinstance(col, dict):
        return ""
        
    pattern = str(col.get("pattern", "")).strip()
    try:
        max_len_str = str(col.get("max_length", "10")).split(',')[0]
        max_len = int(re.sub(r'[^0-9]', '', max_len_str))
    except:
        max_len = 10

    if pattern and pattern != "None" and pattern.startswith("^"):
        return generate_from_regex(pattern, max_len)
    
    return "".join(random.choices(string.digits, k=max_len))

def generate_csv(contract_path, output_dir, env, rows=100, user_prefix=None, suffix="", **kwargs):
    print(f"🚀 Lecture du fichier structuré : {contract_path}")
    
    with open(contract_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # --- GESTION FLEXIBLE DE LA STRUCTURE (Correction Erreur 'list') ---
    if isinstance(data, list):
        # Si Gemini renvoie une liste directe de colonnes
        cols = data
        flux_name_from_json = "DATA"
    elif isinstance(data, dict):
        # Si Gemini renvoie l'objet structuré attendu
        cols = data.get("columns", [])
        flux_name_from_json = data.get("flux_name", "DATA")
    else:
        print("❌ Format de données JSON non reconnu.")
        return None

    if not cols:
        print("⚠️ Aucune colonne détectée dans le fichier JSON.")
        return None

    # Détermination du nom du fichier
    flux_name = (user_prefix or flux_name_from_json).strip().upper()
    filename = f"{flux_name}{suffix}_{env}_{date.today().strftime('%Y%m%d')}.csv"
    path = os.path.join(output_dir, filename)

    os.makedirs(output_dir, exist_ok=True)
    
    print(f"⚙️ Génération de {rows} lignes dans {filename}...")
    
    with open(path, "w", encoding="utf-8", newline="") as f:
        # Utilisation de QUOTE_MINIMAL pour éviter les guillemets superflus
        writer = csv.writer(f, delimiter=";", quoting=csv.QUOTE_MINIMAL)
        
        # En-têtes
        writer.writerow([str(c.get("name", "UNKNOWN")) for c in cols])
        
        # Données
        for _ in range(rows):
            writer.writerow([generate_dynamic_value(col) for col in cols])
            
    print(f"✅ Fichier CSV créé avec succès : {path}")
    return path