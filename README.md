# 🚀 Génération d'archive de test à l'aide de IA (Gemini AI)

Ce projet est un générateur de données de test intelligent. Il utilise l'IA (Google Gemini) pour analyser des documents Word (contrats d'interface), en extraire les règles métier complexes, et générer des fichiers CSV de test parfaitement formatés.

## 💻 Environnement de Travail

> **Important** : Ce projet a été conçu pour être exécuté et maintenu via l'IDE **Cursor**. 
> L'utilisation de Cursor est recommandée pour bénéficier de l'assistance IA sur l'indexation des contrats et la gestion des fichiers `.env`.


## 📋 Fonctionnalités
- **Analyse IA** : Lecture automatique des documents (Contrats d'interface).
- **Traduction Regex** : Conversion des descriptions humaines (ex: "Commence par 004") en expressions régulières techniques.
- **Génération Flexible** : Supporte les préfixes dynamiques (`MIX_`, `FID4_`, `004`, etc.).
- **Respect Strict** : Garantie de longueur, de type de données et suppression des caractères interdits (ex: signes négatifs).
- **Interface Streamlit** : Interface utilisateur simple pour charger le document et télécharger le CSV.

## 🛠 Architecture et Communication des Scripts

Le projet est divisé en trois couches logiques qui communiquent de façon séquentielle :



### 1. `agents/rap_contract_agent.py` (Le Cerveau)
- **Rôle** : Reçoit le texte brut extrait du Word.
- **Action** : Envoie un prompt structuré à l'API **gemini-2.5-flash**.
- **Sortie** : Génère un fichier `build/contract_structured.json`.
- **Communication** : C'est lui qui définit les "règles du jeu" pour chaque colonne (Regex, longueur, nom).

### 2. `core/csv_generator.py` (Le Moteur)
- **Rôle** : Lit le fichier JSON produit par l'agent.
- **Action** : Décompose chaque Regex pour identifier les préfixes et les formats (Dates, Classes de caractères `[56]`, etc.).
- **Sortie** : Produit le fichier CSV final dans le dossier `output/`.
- **Communication** : Il est totalement indépendant de l'IA. Il peut générer des millions de lignes localement une fois que le JSON existe.

### 3. `app.py` (L'Interface)
- **Rôle** : Orchestrateur Streamlit.
- **Action** : Gère l'upload du fichier, affiche l'avancement et permet le téléchargement du résultat.

## ⚙️ Installation

1. Cloner le projet :
   ```bash
   git clone [https://github.com/FactoryDianeIA/generate-data-test.git](https://github.com/FactoryDianeIA/generate-data-test.git)
   cd generate-data-test