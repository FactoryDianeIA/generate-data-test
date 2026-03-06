import streamlit as st
import os
import shutil
from dotenv import load_dotenv # Indispensable pour lire le fichier .env
from core.universal_extractor import extract_text_universally 
from agents.rap_contract_agent import run_agent
from core.csv_generator import generate_csv
from core.packager import create_archive

# --- CHARGEMENT DE LA CONFIGURATION ---
# Cette ligne lit le fichier .env et charge la variable GOOGLE_API_KEY en mémoire
load_dotenv() 

# Configuration de la page Streamlit
st.set_page_config(page_title="Universal Flow Generator", page_icon="⚙️", layout="wide")

st.title("🚀 Universal Flow Generator")
st.markdown("Générez des jeux de données massifs à partir de vos contrats d'interface (Word, PDF, MD).")

# --- BARRE LATÉRALE (SIDEBAR) ---
with st.sidebar:
    st.header("⚙️ Configuration")
    env = st.selectbox("Environnement cible", ["DEV", "REC", "PROD"])
    
    nb_rows = st.number_input(
        "Lignes par fichier", 
        min_value=1, 
        max_value=100_000_000, 
        value=1000,
        help="Nombre de lignes de données à générer par fichier CSV."
    )
    
    st.subheader("📦 Archive & Flux")
    user_prefix = st.text_input("Nom du flux (optionnel)", placeholder="Ex: SAP_INVOICE")
    nb_files = st.slider("Nombre de fichiers CSV", min_value=1, max_value=10, value=1)
    
    st.divider()
    uploaded_file = st.file_uploader("Charger le contrat d'interface", type=["docx", "pdf", "md", "txt"])

# --- LOGIQUE DE TRAITEMENT ---
if uploaded_file:
    # Initialisation des dossiers de travail
    for folder in ["temp", "build"]:
        os.makedirs(folder, exist_ok=True)
    
    file_path = os.path.join("temp", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    if st.button("🔥 Lancer la génération", use_container_width=True):
        try:
            with st.status("Traitement en cours...", expanded=True) as status:
                
                # 1. Extraction du texte
                st.write("🔍 **Étape 1 :** Extraction du texte du document...")
                raw_json = "build/contract_raw.json"
                extract_text_universally(file_path, raw_json)

                # 2. Analyse par l'Agent
                st.write("🤖 **Étape 2 :** Analyse sémantique (Gemini)...")
                struct_json = "build/contract_structured.json"
                
                # L'agent utilise os.getenv("GOOGLE_API_KEY") qui est maintenant chargé par load_dotenv()
                run_agent(raw_json, None, struct_json)
                
                if not os.path.exists(struct_json):
                    raise Exception("L'IA n'a pas pu structurer le contrat. Vérifiez le format du document.")

                # 3. Génération des fichiers CSV
                st.write(f"📊 **Étape 3 :** Génération de {nb_files} fichier(s)...")
                all_csv_paths = []
                
                for i in range(nb_files):
                    # Création d'un suffixe pour différencier les fichiers si nb_files > 1
                    current_suffix = f"_{i+1}" if nb_files > 1 else ""
                    
                    csv_path = generate_csv(
                        contract_path=struct_json, 
                        output_dir="build", 
                        env=env, 
                        rows=nb_rows, 
                        user_prefix=user_prefix,
                        suffix=current_suffix
                    )
                    all_csv_paths.append(csv_path)
                    st.write(f"✔️ Fichier {i+1} généré.")

                # 4. Archivage
                st.write("📦 **Étape 4 :** Création du package final...")
                archive_path = create_archive(all_csv_paths, env, "build")
                
                status.update(label="✅ Génération terminée avec succès !", state="complete")

            # --- AFFICHAGE DU RÉSULTAT ---
            st.success(f"L'archive est prête : `{os.path.basename(archive_path)}`")
            
            with open(archive_path, "rb") as f:
                st.download_button(
                    label="📥 Télécharger le package (TAR.GZ)",
                    data=f,
                    file_name=os.path.basename(archive_path),
                    mime="application/gzip",
                    use_container_width=True
                )

        except Exception as e:
            st.error(f"❌ Une erreur est survenue : {str(e)}")
            st.info("Conseil : Vérifiez que votre clé API Gemini est bien configurée dans le fichier .env à la racine du projet.")
        
        finally:
            # Nettoyage des fichiers temporaires (on garde 'build' pour archivage)
            if os.path.exists("temp"):
                shutil.rmtree("temp", ignore_errors=True)