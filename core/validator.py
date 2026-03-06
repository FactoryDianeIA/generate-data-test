import json
from jsonschema import validate

def validate_contract(contract_path, schema_path):

    with open(contract_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    validate(instance=data, schema=schema)