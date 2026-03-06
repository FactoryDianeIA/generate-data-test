import csv

EXPECTED_COLUMNS = [
    "COL1","COL2","COL3","COL4","COL5",
    "COL6","COL7","COL8","COL9","COL10"
]

def validate_csv(path, expected_rows=100_000):

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")

        header = next(reader, None)

        if header != EXPECTED_COLUMNS:
            raise Exception("Header CSV non conforme")

        count = 0

        for line_num, row in enumerate(reader, start=2):

            if len(row) != 10:
                raise Exception(f"Ligne {line_num} : nombre de colonnes incorrect")

            # COL1
            if not row[0] or len(row[0]) > 50:
                raise Exception(f"Ligne {line_num} : COL1 invalide")

            # COL2
            if not row[1] or len(row[1]) > 50:
                raise Exception(f"Ligne {line_num} : COL2 invalide")

            # COL3
            if len(row[2]) > 100:
                raise Exception(f"Ligne {line_num} : COL3 trop long")

            # COL4
            if not row[3].isdigit() or len(row[3]) > 10:
                raise Exception(f"Ligne {line_num} : COL4 invalide")

            # COL5
            if len(row[4]) != 10 or row[4][4] != "-" or row[4][7] != "-":
                raise Exception(f"Ligne {line_num} : COL5 format invalide")

            # COL6
            if len(row[5]) > 20:
                raise Exception(f"Ligne {line_num} : COL6 trop long")

            # COL7
            try:
                float(row[6])
            except:
                raise Exception(f"Ligne {line_num} : COL7 invalide")

            # COL8
            if not row[7] or len(row[7]) > 10:
                raise Exception(f"Ligne {line_num} : COL8 invalide")

            # COL9
            if len(row[8]) > 255:
                raise Exception(f"Ligne {line_num} : COL9 trop long")

            # COL10
            if row[9] not in ("true", "false"):
                raise Exception(f"Ligne {line_num} : COL10 invalide")

            count += 1

        if count != expected_rows:
            raise Exception(
                f"Nombre de lignes incorrect : {count} au lieu de {expected_rows}"
            )