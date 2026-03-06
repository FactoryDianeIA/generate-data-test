import tarfile
import os
import time

def create_archive(file_paths, env, output_dir):
    """
    Prend une liste de chemins de fichiers CSV et les compresse 
    dans un .tar.gz avec un horodatage précis.
    """
    if not file_paths:
        return None

    # On s'assure que le dossier de sortie existe
    os.makedirs(output_dir, exist_ok=True)

    # Extraction intelligente du nom de base :
    # Au lieu de split('_'), on retire l'extension et le suffixe de fin de fichier
    # pour garder le "Nom_Du_Flux" complet.
    first_file = os.path.basename(file_paths[0])
    base_name = first_file.replace(".csv", "")
    
    # Nettoyage optionnel : on enlève la date et l'environnement du nom du fichier 
    # pour que l'archive ait un nom propre.
    # Si le fichier est "RH_PAIE_DEV_20240304.csv", on veut "RH_PAIE"
    if f"_{env}" in base_name:
        base_name = base_name.split(f"_{env}")[0]

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    archive_filename = f"ARCHIVE_{base_name}_{env}_{timestamp}.tar.gz"
    archive_path = os.path.join(output_dir, archive_filename)

    try:
        with tarfile.open(archive_path, "w:gz") as tar:
            for f in file_paths:
                if os.path.exists(f):
                    # arcname permet de ne pas inclure toute l'arborescence des dossiers dans l'archive
                    tar.add(f, arcname=os.path.basename(f))
                else:
                    print(f"⚠️ Avertissement : Le fichier {f} n'existe pas et ne sera pas ajouté.")

        return archive_path
    except Exception as e:
        print(f"❌ Erreur lors de la création de l'archive : {e}")
        return None