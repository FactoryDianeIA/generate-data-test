import os
import shutil

def reject_file(file_path, reason, reject_root="reject/rap"):

    os.makedirs(reject_root, exist_ok=True)

    target = os.path.join(
        reject_root,
        os.path.basename(file_path)
    )

    shutil.move(file_path, target)

    print("FICHIER REJETE :", target)
    print("RAISON :", reason)

    return target