import os

from core.word_extractor import extract_word_contract
from agents.rap_contract_agent import run_agent
from core.validator import validate_contract
from core.csv_generator import generate_csv
from core.csv_validator import validate_csv
from core.packager import create_archive
from core.reject import reject_file

RAW = "build/contract_raw.json"
STRUCT = "build/contract_structured.json"

def main():

    os.makedirs("build", exist_ok=True)

    try:
        extract_word_contract(
            "contracts/Contrat_RAP.docx",
            RAW
        )

        run_agent(
            RAW,
            "core/contract_schema.json",
            STRUCT
        )

        validate_contract(
            STRUCT,
            "core/contract_schema.json"
        )

        csv_path = generate_csv(
            STRUCT,
            "build",
            env="DEV",
            rows=100_000
        )

        # Contrôles chapitre 10
        validate_csv(csv_path, expected_rows=100_000)

        archive = create_archive(
            csv_path,
            env="DEV",
            output_dir="build"
        )

        print("Archive générée :", archive)

    except Exception as e:

        if os.path.exists("build"):
            for f in os.listdir("build"):
                if f.endswith(".csv"):
                    reject_file(
                        os.path.join("build", f),
                        str(e)
                    )

        raise

if __name__ == "__main__":
    main()